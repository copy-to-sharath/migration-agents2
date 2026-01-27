from __future__ import annotations

import argparse
import hashlib
import math
from functools import partial
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_multiprocessing import process_map, resolve_workers
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.state import finalize_state, start_state, write_state

from .config import LogicManifesterConfig, load_config


def _sanitize_value(value):
    """Convert NaN/None float values to appropriate defaults."""
    if value is None:
        return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _sanitize_int(value, default=0):
    """Convert value to int, handling NaN/None."""
    if value is None:
        return default
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return default
        return int(value)
    return value


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_workers(config: LogicManifesterConfig) -> int:
    return resolve_workers(config.workers)


def _with_metadata(
    rows: list[dict],
    config: LogicManifesterConfig,
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


def _hash_rule_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _truncate(value: str, limit: int) -> str:
    cleaned = " ".join(value.split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3] + "..."


def _group_by_slice(rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        slice_id = row.get("slice_id")
        if slice_id:
            grouped[slice_id].append(row)
    return grouped


def _build_rules(
    slice_context: list[dict],
    slice_manifest: list[dict],
    max_rule_text_chars: int,
) -> list[dict]:
    manifest_by_slice = _group_by_slice(slice_manifest)
    rows: list[dict] = []
    for ctx in slice_context:
        slice_id = ctx.get("slice_id")
        if not slice_id:
            continue
        summary = ctx.get("summary", "")
        risks = ctx.get("risks", "")
        assumptions = ctx.get("assumptions", "")
        tables = sorted(
            {
                row.get("table_name")
                for row in manifest_by_slice.get(slice_id, [])
                if row.get("table_name")
            }
        )
        inputs = ", ".join(tables)
        rule_text = summary
        if risks:
            rule_text = f"{rule_text} Risks: {risks}"
        if assumptions:
            rule_text = f"{rule_text} Assumptions: {assumptions}"
        rule_text = _truncate(rule_text, max_rule_text_chars)
        rows.append(
            {
                "rule_id": _hash_rule_id(f"{slice_id}:{rule_text}"),
                "slice_id": slice_id,
                "rule_text": rule_text,
                "inputs": inputs,
                "outputs": "",
                "invariants": "",
                "source_ref": ctx.get("source_ref", "slice_context"),
            }
        )
    return rows


def _build_rule_for_ctx(
    ctx: dict,
    tables_by_slice: dict[str, list[str]],
    max_rule_text_chars: int,
) -> dict | None:
    slice_id = ctx.get("slice_id")
    if not slice_id:
        return None
    summary = ctx.get("summary", "")
    risks = ctx.get("risks", "")
    assumptions = ctx.get("assumptions", "")
    inputs = ", ".join(tables_by_slice.get(slice_id, []))
    rule_text = summary
    if risks:
        rule_text = f"{rule_text} Risks: {risks}"
    if assumptions:
        rule_text = f"{rule_text} Assumptions: {assumptions}"
    rule_text = _truncate(rule_text, max_rule_text_chars)
    return {
        "rule_id": _hash_rule_id(f"{slice_id}:{rule_text}"),
        "slice_id": slice_id,
        "rule_text": rule_text,
        "inputs": inputs,
        "outputs": "",
        "invariants": "",
        "source_ref": ctx.get("source_ref", "slice_context"),
    }


def _build_logic_edges(rules: list[dict], slice_manifest: list[dict]) -> list[dict]:
    rules_by_slice = {row["slice_id"]: row["rule_id"] for row in rules}
    rows: list[dict] = []
    for item in slice_manifest:
        slice_id = item.get("slice_id")
        symbol_id = _sanitize_value(item.get("symbol_id"))
        file_path = _sanitize_value(item.get("file_path"))
        # Skip if slice_id or symbol_id is missing/NaN
        if not slice_id or not symbol_id or (isinstance(symbol_id, float) and math.isnan(symbol_id)):
            continue
        rule_id = rules_by_slice.get(slice_id)
        if not rule_id:
            continue
        rows.append(
            {
                "rule_id": rule_id,
                "symbol_id": str(symbol_id) if symbol_id else "",
                "file_path": str(file_path) if file_path else "",
                "line": 0,
                "evidence": _sanitize_value(item.get("external_ref")) or "",
                "source_ref": _sanitize_value(item.get("source_ref")) or str(file_path) if file_path else "",
            }
        )
    return rows


def _build_trace_map(
    rules: list[dict],
    slice_source_refs: list[dict],
    max_trace_refs_per_rule: int,
) -> list[dict]:
    refs_by_slice = _group_by_slice(slice_source_refs)
    rows: list[dict] = []
    for rule in rules:
        slice_id = rule.get("slice_id")
        rule_id = rule.get("rule_id")
        if not slice_id or not rule_id:
            continue
        refs = refs_by_slice.get(slice_id, [])
        for row in refs[:max_trace_refs_per_rule]:
            rows.append(
                {
                    "rule_id": rule_id,
                    "file_path": row.get("file_path"),
                    "line": _sanitize_int(row.get("line"), 0),
                    "rationale": _sanitize_value(row.get("excerpt")) or "",
                    "source_ref": _sanitize_value(row.get("source_ref")) or row.get("file_path", ""),
                }
            )
    return rows


def _build_trace_for_rule(
    rule: dict,
    refs_by_slice: dict[str, list[dict]],
    max_trace_refs_per_rule: int,
) -> list[dict]:
    slice_id = rule.get("slice_id")
    rule_id = rule.get("rule_id")
    if not slice_id or not rule_id:
        return []
    refs = refs_by_slice.get(slice_id, [])
    rows: list[dict] = []
    for row in refs[:max_trace_refs_per_rule]:
        rows.append(
            {
                "rule_id": rule_id,
                "file_path": row.get("file_path"),
                "line": _sanitize_int(row.get("line"), 0),
                "rationale": _sanitize_value(row.get("excerpt")) or "",
                "source_ref": _sanitize_value(row.get("source_ref")) or row.get("file_path", ""),
            }
        )
    return rows


def run(config: LogicManifesterConfig) -> None:
    created_at = _created_at()
    _ = _resolve_workers(config)
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    config = config.model_copy(update={"run_id": run_id})
    output_root = config.output_root / config.run_id / "step_4"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("logic_manifester", config.run_id, config.artifact_version)
    client = get_mcp_client()

    slice_context = _fetch_rows(client, "slice_context", config.run_id, config.artifact_version)
    slice_manifest = _fetch_rows(client, "slice_manifest", config.run_id, config.artifact_version)
    slice_source_refs = _fetch_rows(
        client, "slice_source_refs", config.run_id, config.artifact_version
    )
    workers = _resolve_workers(config)
    manifest_by_slice = _group_by_slice(slice_manifest)
    tables_by_slice: dict[str, list[str]] = {}
    for slice_id, rows in manifest_by_slice.items():
        tables_by_slice[slice_id] = sorted(
            {
                row.get("table_name")
                for row in rows
                if row.get("table_name")
            }
        )

    if workers > 1 and slice_context:
        rule_worker = partial(
            _build_rule_for_ctx,
            tables_by_slice=tables_by_slice,
            max_rule_text_chars=config.max_rule_text_chars,
        )
        rule_rows = [
            row for row in process_map(rule_worker, slice_context, workers) if row
        ]
    else:
        rule_rows = _build_rules(slice_context, slice_manifest, config.max_rule_text_chars)
    edge_rows = _build_logic_edges(rule_rows, slice_manifest)
    refs_by_slice = _group_by_slice(slice_source_refs)
    if workers > 1 and rule_rows:
        trace_worker = partial(
            _build_trace_for_rule,
            refs_by_slice=refs_by_slice,
            max_trace_refs_per_rule=config.max_trace_refs_per_rule,
        )
        trace_batches = process_map(trace_worker, rule_rows, workers)
        trace_rows = [row for batch in trace_batches for row in batch]
    else:
        trace_rows = _build_trace_map(
            rule_rows, slice_source_refs, config.max_trace_refs_per_rule
        )

    if rule_rows:
        write_parquet(
            output_root,
            "logic_rules",
            _with_metadata(rule_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if edge_rows:
        write_parquet(
            output_root,
            "logic_edges",
            _with_metadata(edge_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if trace_rows:
        write_parquet(
            output_root,
            "trace_map",
            _with_metadata(trace_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    state = finalize_state(
        state,
        processed_count=len(rule_rows),
        outputs={
            "logic_rules": len(rule_rows),
            "logic_edges": len(edge_rows),
            "trace_map": len(trace_rows),
        },
        notes={"output_root": str(output_root)},
    )
    write_state("logic_manifester", state)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 4 Logic Manifester pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
