from __future__ import annotations

import argparse
import logging
import math
from functools import partial
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.logging_utils import setup_logging
from migration_agents.shared_multiprocessing import process_map, resolve_workers
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.state import finalize_state, start_state, write_state

from .config import SliceExtractorConfig, load_config

LOGGER = logging.getLogger("migration_agents.slice_extractor")


def _sanitize_value(value):
    """Convert NaN/None float values to None for parquet compatibility."""
    if value is None:
        return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_workers(config: SliceExtractorConfig) -> int:
    return resolve_workers(config.workers)


def _with_metadata(
    rows: list[dict],
    config: SliceExtractorConfig,
    created_at: str,
) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("slice_id", None)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _fetch_rows(client, table: str, run_id: str, artifact_version: int) -> list[dict]:
    sql = f"""
        select *
        from {table}
        where run_id = '{run_id}' and artifact_version = {artifact_version}
    """
    return client.query(sql)


def _parse_source_ref(value: str) -> tuple[str | None, int | None]:
    if not value:
        return None, None
    if ":" not in value:
        return value, None
    path, suffix = value.rsplit(":", 1)
    suffix = suffix.strip()
    if not suffix:
        return value, None
    if "-" in suffix:
        start, _, _ = suffix.partition("-")
        if start.isdigit():
            return path, int(start)
    if suffix.isdigit():
        return path, int(suffix)
    return value, None


def _index_chunks(chunks: Iterable[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in chunks:
        grouped[row["file_path"]].append(row)
    for entries in grouped.values():
        entries.sort(key=lambda item: item.get("line_start", 0))
    return grouped


def _excerpt_for(
    chunk_index: dict[str, list[dict]],
    file_path: str,
    line: int | None,
    max_excerpt_chars: int,
) -> str:
    if not file_path or line is None:
        return ""
    entries = chunk_index.get(file_path)
    if not entries:
        return ""
    for row in entries:
        start = row.get("line_start")
        end = row.get("line_end")
        if start is None or end is None:
            continue
        if start <= line <= end:
            content = row.get("content", "")
            content = " ".join(content.split())
            if len(content) > max_excerpt_chars:
                return content[: max_excerpt_chars - 3] + "..."
            return content
    return ""


def _build_symbol_lookup(symbols: Iterable[dict]) -> dict[str, tuple[str, int]]:
    lookup: dict[str, tuple[str, int]] = {}
    for row in symbols:
        symbol_id = row.get("symbol_id")
        file_path = row.get("file_path")
        line = row.get("line")
        if symbol_id and file_path and isinstance(line, int):
            lookup[symbol_id] = (file_path, line)
    return lookup


def _build_table_lookup(data_access: Iterable[dict]) -> dict[str, tuple[str, int]]:
    lookup: dict[str, tuple[str, int]] = {}
    for row in data_access:
        table_name = row.get("table_name") or ""
        file_path = row.get("file_path")
        line = row.get("line")
        if table_name and file_path and isinstance(line, int):
            key = table_name.strip().lower()
            if key not in lookup:
                lookup[key] = (file_path, line)
    return lookup


def _node_file_line(
    node: dict,
    symbol_lookup: dict[str, tuple[str, int]],
    table_lookup: dict[str, tuple[str, int]],
) -> tuple[str | None, int | None]:
    source_ref = node.get("source_ref", "")
    file_path, line = _parse_source_ref(source_ref)
    if file_path and line is not None:
        return file_path, line

    symbol_id = node.get("symbol_id")
    if symbol_id and symbol_id in symbol_lookup:
        return symbol_lookup[symbol_id]

    table_name = node.get("table_name")
    if table_name:
        key = table_name.strip().lower()
        if key in table_lookup:
            return table_lookup[key]

    return file_path, line


def _build_slice_manifest(
    slices: dict[str, list[dict]],
    symbol_lookup: dict[str, tuple[str, int]],
    table_lookup: dict[str, tuple[str, int]],
) -> list[dict]:
    rows: list[dict] = []
    for slice_id, nodes in slices.items():
        for node in nodes:
            file_path, _ = _node_file_line(node, symbol_lookup, table_lookup)
            if not file_path:
                continue
            node_type = node.get("node_type")
            external_ref = ""
            if node_type in {"callsite", "callee", "sql_site"}:
                external_ref = node.get("label", "")
            if node_type == "table":
                external_ref = node.get("table_name", node.get("label", ""))
            rows.append(
                {
                    "slice_id": slice_id,
                    "file_path": file_path,
                    "symbol_id": _sanitize_value(node.get("symbol_id")),
                    "table_name": _sanitize_value(node.get("table_name")),
                    "external_ref": _sanitize_value(external_ref) or "",
                    "source_ref": _sanitize_value(node.get("source_ref", file_path)),
                }
            )
    return rows


def _build_slice_manifest_for_slice(
    item: tuple[str, list[dict]],
    symbol_lookup: dict[str, tuple[str, int]],
    table_lookup: dict[str, tuple[str, int]],
) -> list[dict]:
    slice_id, nodes = item
    rows: list[dict] = []
    for node in nodes:
        file_path, _ = _node_file_line(node, symbol_lookup, table_lookup)
        if not file_path:
            continue
        node_type = node.get("node_type")
        external_ref = ""
        if node_type in {"callsite", "callee", "sql_site"}:
            external_ref = node.get("label", "")
        if node_type == "table":
            external_ref = node.get("table_name", node.get("label", ""))
        rows.append(
            {
                "slice_id": slice_id,
                "file_path": file_path,
                "symbol_id": _sanitize_value(node.get("symbol_id")),
                "table_name": _sanitize_value(node.get("table_name")),
                "external_ref": _sanitize_value(external_ref) or "",
                "source_ref": _sanitize_value(node.get("source_ref", file_path)),
            }
        )
    return rows


def _build_slice_context(
    slices: dict[str, list[dict]],
    data_access_nodes: set[str],
) -> list[dict]:
    rows: list[dict] = []
    for slice_id, nodes in slices.items():
        files = {node.get("source_ref", "").split(":", 1)[0] for node in nodes}
        files = {file_path for file_path in files if file_path}
        tables = [node.get("table_name") for node in nodes if node.get("table_name") and isinstance(node.get("table_name"), str)]
        table_preview = ", ".join(sorted(set(tables))[:3])
        summary = (
            f"Slice {slice_id} covers {len(nodes)} nodes across {len(files)} files."
            f" Tables: {table_preview}" if table_preview else
            f"Slice {slice_id} covers {len(nodes)} nodes across {len(files)} files."
        )
        risks = ""
        if not any(node.get("node_id") in data_access_nodes for node in nodes):
            risks = "No data access nodes detected in this slice."
        assumptions = "Slice boundaries derived from graph communities; validate scope."
        rows.append(
            {
                "slice_id": slice_id,
                "summary": summary,
                "risks": risks,
                "assumptions": assumptions,
                "source_ref": "graph_metadata",
            }
        )
    return rows


def _build_slice_context_for_slice(
    item: tuple[str, list[dict]],
    data_access_nodes: set[str],
) -> dict:
    slice_id, nodes = item
    files = {node.get("source_ref", "").split(":", 1)[0] for node in nodes}
    files = {file_path for file_path in files if file_path}
    tables = [node.get("table_name") for node in nodes 
              if node.get("table_name") and isinstance(node.get("table_name"), str)]
    table_preview = ", ".join(sorted(set(tables))[:3])
    summary = (
        f"Slice {slice_id} covers {len(nodes)} nodes across {len(files)} files."
        f" Tables: {table_preview}" if table_preview else
        f"Slice {slice_id} covers {len(nodes)} nodes across {len(files)} files."
    )
    risks = ""
    if not any(node.get("node_id") in data_access_nodes for node in nodes):
        risks = "No data access nodes detected in this slice."
    assumptions = "Slice boundaries derived from entry graphs; validate scope."
    return {
        "slice_id": slice_id,
        "summary": summary,
        "risks": risks,
        "assumptions": assumptions,
        "source_ref": "graph_metadata",
    }


def _build_slice_context_worker(
    item: tuple[str, list[dict]],
    data_access_nodes: set[str],
) -> dict:
    return _build_slice_context_for_slice(item, data_access_nodes)


def _build_slice_source_refs(
    slices: dict[str, list[dict]],
    chunk_index: dict[str, list[dict]],
    symbol_lookup: dict[str, tuple[str, int]],
    table_lookup: dict[str, tuple[str, int]],
    max_refs_per_slice: int,
    max_excerpt_chars: int,
) -> list[dict]:
    rows: list[dict] = []
    for slice_id, nodes in slices.items():
        seen: set[tuple[str, int]] = set()
        for node in nodes:
            file_path, line = _node_file_line(node, symbol_lookup, table_lookup)
            if not file_path or line is None:
                continue
            key = (file_path, line)
            if key in seen:
                continue
            seen.add(key)
            excerpt = _excerpt_for(chunk_index, file_path, line, max_excerpt_chars)
            rows.append(
                {
                    "slice_id": slice_id,
                    "file_path": file_path,
                    "line": line,
                    "excerpt": excerpt,
                    "source_ref": node.get("source_ref", file_path),
                }
            )
            if len(seen) >= max_refs_per_slice:
                break
    return rows


def _group_slices_by_community(
    nodes: list[dict],
    graph_meta: list[dict],
) -> dict[str, list[dict]]:
    """Group nodes into slices by community detection results."""
    community_map: dict[str, int] = {}
    for row in graph_meta:
        node_id = row.get("node_id")
        community_id = row.get("community_id")
        if node_id and isinstance(community_id, int) and community_id > 0:
            community_map[node_id] = community_id

    slices: dict[str, list[dict]] = defaultdict(list)
    for node in nodes:
        node_id = node.get("node_id")
        community_id = community_map.get(node_id)
        if not community_id:
            continue
        slice_id = f"slice_{community_id}"
        slices[slice_id].append(node)
    return slices


def _filter_entry_graphs(
    entry_graphs: list[dict],
    symbols: list[dict],
    calls: list[dict],
    nodes: list[dict],
    config,
) -> list[dict]:
    """Filter entry graphs to only include top-level entry points.
    
    Filters based on:
    - entry_filter_top_level_only: Only entries not called by other entries
    - entry_filter_min_depth: Minimum call graph depth
    - entry_filter_kinds: Symbol kinds to include
    - entry_filter_patterns: Name patterns indicating entry points
    """
    import logging
    log = logging.getLogger(__name__)
    
    if not entry_graphs:
        return []
    
    # Build symbol lookup by symbol_id
    symbol_lookup = {s.get("symbol_id"): s for s in symbols}
    
    # Build node_id -> symbol_id lookup (entry_key is a node_id, not symbol_id)
    node_to_symbol = {n.get("node_id"): n.get("symbol_id") for n in nodes if n.get("symbol_id")}
    
    # Build set of entry keys that are called by other entries
    entry_keys = {eg.get("entry_key") for eg in entry_graphs}
    called_by_entries = set()
    if config.entry_filter_top_level_only:
        for call in calls:
            caller_id = call.get("caller_id")
            callee_id = call.get("callee_id")
            if caller_id in entry_keys and callee_id in entry_keys:
                called_by_entries.add(callee_id)
    
    filtered = []
    for entry in entry_graphs:
        entry_key = entry.get("entry_key")
        capped_depth = entry.get("capped_depth", 0) or 0
        
        # Filter by depth
        if capped_depth < config.entry_filter_min_depth:
            continue
        
        # Filter by top-level only
        if config.entry_filter_top_level_only and entry_key in called_by_entries:
            continue
        
        # Get symbol info via node_id -> symbol_id lookup
        symbol_id = node_to_symbol.get(entry_key)
        sym = symbol_lookup.get(symbol_id) if symbol_id else None
        
        # If no symbol info and filters are specified, skip; otherwise include
        if not sym:
            # If no filters specified, include entry even without symbol info
            if not config.entry_filter_kinds and not config.entry_filter_patterns:
                filtered.append(entry)
            continue
        
        sym_name = sym.get("name", "")
        sym_kind = sym.get("kind", "")
        
        # Filter by kind
        if config.entry_filter_kinds and sym_kind not in config.entry_filter_kinds:
            continue
        
        # Filter by patterns (if patterns specified, name must match at least one)
        if config.entry_filter_patterns:
            matches_pattern = any(
                pattern.lower() in sym_name.lower() 
                for pattern in config.entry_filter_patterns
            )
            if not matches_pattern:
                continue
        
        filtered.append(entry)
    
    log.info(f"slice_entry_filter total={len(entry_graphs)} filtered={len(filtered)}")
    return filtered


def _group_slices_by_entry_graph(
    nodes: list[dict],
    entry_graphs: list[dict],
) -> dict[str, list[dict]]:
    """Group nodes into slices using entry graphs (each entry = 1 slice).
    
    Each entry graph defines a slice containing its entry node and all
    reachable nodes. Nodes may appear in multiple slices if they're 
    reachable from multiple entries.
    """
    import json
    
    # Build node lookup by node_id
    node_lookup: dict[str, dict] = {}
    for node in nodes:
        node_id = node.get("node_id")
        if node_id:
            node_lookup[node_id] = node
    
    slices: dict[str, list[dict]] = {}
    for idx, entry in enumerate(entry_graphs):
        entry_key = entry.get("entry_key", f"entry_{idx}")
        source_ref = entry.get("source_ref", "")
        
        # Parse reachable nodes JSON
        reachable_nodes_str = entry.get("reachable_nodes", "[]")
        try:
            reachable_node_ids = json.loads(reachable_nodes_str) if reachable_nodes_str else []
        except json.JSONDecodeError:
            reachable_node_ids = []
        
        # Build slice from reachable nodes
        slice_nodes = []
        for node_id in reachable_node_ids:
            if node_id in node_lookup:
                slice_nodes.append(node_lookup[node_id])
        
        if slice_nodes:
            # Use short slice ID (first 8 chars of entry_key)
            short_key = entry_key[:8] if len(entry_key) > 8 else entry_key
            slice_id = f"entry_{short_key}"
            slices[slice_id] = slice_nodes
    
    return slices


def _group_slices(
    nodes: list[dict],
    graph_meta: list[dict],
    entry_graphs: list[dict] | None = None,
    slicing_mode: str = "auto",
) -> dict[str, list[dict]]:
    """Group nodes into slices based on the slicing mode.
    
    Args:
        nodes: List of code graph nodes
        graph_meta: Graph metadata with community detection results
        entry_graphs: Entry graph data for entry-based slicing
        slicing_mode: 'auto', 'entry_graph', or 'community'
    
    Returns:
        Dictionary mapping slice_id to list of nodes
    """
    if slicing_mode == "entry_graph":
        # Force entry graph-based slicing
        if entry_graphs and len(entry_graphs) > 0:
            return _group_slices_by_entry_graph(nodes, entry_graphs)
        # No entry graphs available, fall back but log warning
        import logging
        logging.getLogger(__name__).warning(
            "slicing_mode='entry_graph' but no entry graphs found, falling back to community"
        )
        return _group_slices_by_community(nodes, graph_meta)
    
    elif slicing_mode == "community":
        # Force community-based slicing
        return _group_slices_by_community(nodes, graph_meta)
    
    else:  # auto mode
        # Prefer entry graph-based slicing if available
        if entry_graphs and len(entry_graphs) > 0:
            return _group_slices_by_entry_graph(nodes, entry_graphs)
        # Fall back to community-based slicing
        return _group_slices_by_community(nodes, graph_meta)


def run(config: SliceExtractorConfig) -> None:
    """Run the slice extractor pipeline.
    
    Supports both full and incremental modes:
    - Full mode: run_id='auto' uses latest run, processes all entries
    - Incremental mode: specific run_id, only processes new/changed data
    """
    created_at = _created_at()
    _ = _resolve_workers(config)
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    config = config.model_copy(update={"run_id": run_id})
    output_root = config.output_root / config.run_id / "step_3"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("slice_extractor", config.run_id, config.artifact_version)
    
    # Pass run_id and parquet_root to client for proper mode handling
    client = get_mcp_client(
        run_id=run_id,
        parquet_root=str(config.output_root),
    )

    nodes = _fetch_rows(client, "code_graph_nodes", config.run_id, config.artifact_version)
    graph_meta = _fetch_rows(client, "graph_metadata", config.run_id, config.artifact_version)
    symbols = _fetch_rows(client, "symbols", config.run_id, config.artifact_version)
    data_access = _fetch_rows(client, "data_access", config.run_id, config.artifact_version)
    chunks = _fetch_rows(client, "intake_source_chunks", config.run_id, config.artifact_version)
    
    # Try to fetch entry graphs and calls for entry-based slicing
    try:
        entry_graphs_raw = _fetch_rows(client, "entry_graphs", config.run_id, config.artifact_version)
    except Exception:
        entry_graphs_raw = []
    
    try:
        calls = _fetch_rows(client, "calls", config.run_id, config.artifact_version)
    except Exception:
        calls = []
    
    # Log RAW depth distribution before filtering
    raw_depth_distribution: dict[int, int] = defaultdict(int)
    raw_max_depth = 0
    if entry_graphs_raw:
        for eg in entry_graphs_raw:
            d = int(eg.get("capped_depth") or eg.get("depth") or 0)
            raw_depth_distribution[d] += 1
            if d > raw_max_depth:
                raw_max_depth = d
    
    if raw_depth_distribution:
        LOGGER.info("=" * 60)
        LOGGER.info("RAW ENTRY GRAPH DEPTH DISTRIBUTION (before filtering)")
        LOGGER.info("=" * 60)
        LOGGER.info("raw_depth_max=%d", raw_max_depth)
        raw_total = sum(raw_depth_distribution.values())
        for d in sorted(raw_depth_distribution.keys()):
            count = raw_depth_distribution[d]
            pct = (count / raw_total * 100) if raw_total > 0 else 0
            LOGGER.info("raw_depth_%d_entries=%d (%.1f%%)", d, count, pct)
        LOGGER.info("raw_total_entries=%d", raw_total)
        LOGGER.info("=" * 60)
    
    # Filter entry graphs to only include top-level entry points
    entry_graphs = entry_graphs_raw
    if entry_graphs and config.slicing_mode in ("auto", "entry_graph"):
        entry_graphs = _filter_entry_graphs(entry_graphs, symbols, calls, nodes, config)

    # Compute and log FILTERED depth distribution
    depth_distribution: dict[int, int] = defaultdict(int)
    max_depth = 0
    if entry_graphs:
        for eg in entry_graphs:
            d = int(eg.get("capped_depth") or eg.get("depth") or 0)
            depth_distribution[d] += 1
            if d > max_depth:
                max_depth = d
    
    if depth_distribution:
        LOGGER.info("=" * 60)
        LOGGER.info("FILTERED ENTRY GRAPH DEPTH DISTRIBUTION (after filtering)")
        LOGGER.info("=" * 60)
        LOGGER.info("filtered_depth_max=%d", max_depth)
        total_entries = sum(depth_distribution.values())
        for d in sorted(depth_distribution.keys()):
            count = depth_distribution[d]
            pct = (count / total_entries * 100) if total_entries > 0 else 0
            LOGGER.info("filtered_depth_%d_entries=%d (%.1f%%)", d, count, pct)
        LOGGER.info("filtered_total_entries=%d", total_entries)
        LOGGER.info("=" * 60)

    slices = _group_slices(nodes, graph_meta, entry_graphs, config.slicing_mode)
    symbol_lookup = _build_symbol_lookup(symbols)
    table_lookup = _build_table_lookup(data_access)
    chunk_index = _index_chunks(chunks)

    data_access_nodes = {
        node.get("node_id") for node in nodes if node.get("node_type") == "sql_site"
    }

    slice_items = list(slices.items())
    workers = _resolve_workers(config)
    if workers > 1 and len(slice_items) > 1:
        manifest_worker = partial(
            _build_slice_manifest_for_slice,
            symbol_lookup=symbol_lookup,
            table_lookup=table_lookup,
        )
        manifest_batches = process_map(manifest_worker, slice_items, workers)
        manifest_rows = [row for batch in manifest_batches for row in batch]
        context_worker = partial(_build_slice_context_worker, data_access_nodes=data_access_nodes)
        context_rows = process_map(context_worker, slice_items, workers)
    else:
        manifest_rows = _build_slice_manifest(slices, symbol_lookup, table_lookup)
        context_rows = _build_slice_context(slices, data_access_nodes)
    source_rows = _build_slice_source_refs(
        slices,
        chunk_index,
        symbol_lookup,
        table_lookup,
        config.max_source_refs_per_slice,
        config.max_excerpt_chars,
    )

    if manifest_rows:
        write_parquet(
            output_root,
            "slice_manifest",
            _with_metadata(manifest_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if context_rows:
        write_parquet(
            output_root,
            "slice_context",
            _with_metadata(context_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if source_rows:
        write_parquet(
            output_root,
            "slice_source_refs",
            _with_metadata(source_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    state = finalize_state(
        state,
        processed_count=len(slices),
        outputs={
            "slice_manifest": len(manifest_rows),
            "slice_context": len(context_rows),
            "slice_source_refs": len(source_rows),
        },
        notes={"output_root": str(output_root)},
    )
    write_state("slice_extractor", state)

    # Generate coverage summary for slice stage
    try:
        from migration_agents.coverage import generate_slice_coverage
        if generate_slice_coverage(config.output_root):
            LOGGER.info("slice_coverage_summary_written=1")
    except Exception as exc:
        LOGGER.warning("slice_coverage_summary_failed error=%s", exc)

    # Log deterministic summary
    LOGGER.info("=" * 60)
    LOGGER.info("SLICE EXTRACTOR SUMMARY")
    LOGGER.info("=" * 60)
    LOGGER.info("slice_total_slices=%d", len(slices))
    LOGGER.info("slice_manifest_rows=%d", len(manifest_rows))
    LOGGER.info("slice_context_rows=%d", len(context_rows))
    LOGGER.info("slice_source_refs=%d", len(source_rows))
    LOGGER.info("slice_entry_graphs_input=%d", len(entry_graphs) if entry_graphs else 0)
    LOGGER.info("slice_max_depth=%d", max_depth)
    if depth_distribution:
        depth_str = ", ".join(f"d{d}:{depth_distribution[d]}" for d in sorted(depth_distribution.keys()))
        LOGGER.info("slice_depth_distribution=%s", depth_str)
    LOGGER.info("slice_symbols_input=%d", len(symbols))
    LOGGER.info("slice_nodes_input=%d", len(nodes))
    LOGGER.info("=" * 60)


def main() -> None:
    from migration_agents.constants import ensure_directories
    ensure_directories()
    
    setup_logging("slice_extractor")
    parser = argparse.ArgumentParser(description="Stage 3 Slice Extractor pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
