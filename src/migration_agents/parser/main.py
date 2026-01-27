from __future__ import annotations

import argparse
import glob
import hashlib
import json
import logging
import math
import os
import re
import shutil
import subprocess
import urllib.request
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from functools import partial

import duckdb

import networkx as nx

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet

from .config import ParserConfig, load_config
from .coverage_summary import generate_coverage_summary
from .build_languages import build_languages, load_config as load_languages_config
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.shared_multiprocessing import process_map
from migration_agents.state import finalize_state, start_state, write_state
from migration_agents.ingestion.config import load_config as load_ingestion_config
from migration_agents.ingestion.main import run as run_ingestion
from .extractors import (
    CallRow,
    ConditionRow,
    ConstantRow,
    DataAccessRow,
    extract_calls,
    extract_conditions,
    extract_constants,
    extract_data_access,
)
from .query_loader import load_query
from .roslyn_runner import RoslynResult, load_roslyn_parquet, run_roslyn
from .semantic_resolver import (
    FileContext,
    SemanticContext,
    build_semantic_context,
    extract_file_context,
    resolve_method_calls,
)
from .symbol_extractor import SymbolRow, extract_symbols
from .tree_sitter_loader import build_parser, load_language

LOGGER = logging.getLogger("migration_agents.parser")


# Content-based language detection patterns for extensionless mainframe files
_MAINFRAME_LANGUAGE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # COBOL - look for division headers, sections, level numbers with PIC, or statements
    # COBOL uses columns 7-72, so there's typically 6-7 leading spaces
    ("cobol", re.compile(
        r"(IDENTIFICATION\s+DIVISION|PROGRAM-ID\.|DATA\s+DIVISION|PROCEDURE\s+DIVISION|"
        r"WORKING-STORAGE\s+SECTION|LINKAGE\s+SECTION|FILE\s+SECTION|"
        r"^\s+0[1-9]\s+[\w-]+.*PIC\s|^\s+[1-4][0-9]\s+[\w-]+.*PIC\s|"
        r"^\s+MOVE\s+|^\s+PERFORM\s+|^\s+IF\s+|^\s+CALL\s+'|"
        r"^\s+REDEFINES\s+|^\s+OCCURS\s+|^\s+VALUE\s+)",
        re.MULTILINE | re.IGNORECASE
    )),
    # JCL - look for // in column 1-2 with JCL keywords
    ("jcl", re.compile(
        r"^//[\w@#$]+\s+(JOB|EXEC|DD|PROC|SET|IF|ELSE|ENDIF|INCLUDE|JCLLIB)\s",
        re.MULTILINE
    )),
    # HLASM - look for column 1 labels with assembler mnemonics or CSECT/DSECT
    ("hlasm", re.compile(
        r"^[A-Z@#$]\w*\s+(CSECT|DSECT|START|USING|EQU|DC|DS|END)\s|"
        r"^\s{8,9}(L\s|LA\s|ST\s|BAL\s|BASR|MVC\s|CLC\s|B\s|BR\s|BCT\s)",
        re.MULTILINE
    )),
    # BMS - CICS map definitions
    ("bms", re.compile(
        r"(DFHMSD|DFHMDI|DFHMDF)\s+TYPE=",
        re.MULTILINE
    )),
    # CICS - EXEC CICS commands
    ("cics", re.compile(
        r"EXEC\s+CICS\s+(SEND|RECEIVE|READ|WRITE|REWRITE|DELETE|START|LINK|XCTL)",
        re.MULTILINE | re.IGNORECASE
    )),
    # Easytrieve
    ("easytrieve", re.compile(
        r"^\s*(FILE|JOB|SORT|REPORT|DEFINE|GET|PUT|PRINT)\s+\w+",
        re.MULTILINE
    )),
]


def detect_mainframe_language(content: str) -> str | None:
    """Detect mainframe language from file content for extensionless files.
    
    Returns the language name if detected, None otherwise.
    """
    # Check first 5000 chars for efficiency
    sample = content[:5000]
    for lang_name, pattern in _MAINFRAME_LANGUAGE_PATTERNS:
        if pattern.search(sample):
            return lang_name
    return None


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_workers(config: ParserConfig) -> int:
    if config.workers != "auto":
        return int(config.workers)
    # Use all available CPUs for parsing which is CPU-bound
    return max(1, os.cpu_count() or 2)


def _with_metadata(rows: list[dict], config: ParserConfig, created_at: str) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("slice_id", None)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _hash_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _entry_graph_depth_metrics(
    adjacency: dict[str, list[str]],
    entry: str,
    max_depth: int,
    node_limit: int,
) -> tuple[dict[str, float], set[str]]:
    max_depth_seen = 0
    reachable: set[str] = set()
    stack: list[tuple[str, int, set[str]]] = [(entry, 0, {entry})]
    while stack:
        node, depth, path = stack.pop()
        reachable.add(node)
        if depth > max_depth_seen:
            max_depth_seen = depth
        if depth >= max_depth:
            continue
        for neighbor in adjacency.get(node, []):
            if neighbor in path:
                continue
            stack.append((neighbor, depth + 1, path | {neighbor}))
    capped_depth = min(max_depth_seen, max_depth)
    normalized = capped_depth / max_depth if max_depth else 0.0
    log_scaled = math.log1p(capped_depth) / math.log1p(max_depth) if max_depth else 0.0
    capped_nodes = min(len(reachable), node_limit)
    depth_breadth = (capped_depth * capped_nodes) / node_limit if node_limit else 0.0
    return {
        "max_depth": float(max_depth_seen),
        "capped_depth": float(capped_depth),
        "normalized": float(normalized),
        "log_scaled": float(log_scaled),
        "depth_breadth": float(depth_breadth),
        "reachable_nodes": float(len(reachable)),
    }, reachable


def _compute_nodes_by_depth(
    adjacency: dict[str, list[str]],
    entry: str,
    max_depth: int,
) -> dict[int, set[str]]:
    """Compute nodes at each depth level from entry using BFS."""
    nodes_by_depth: dict[int, set[str]] = defaultdict(set)
    visited: set[str] = set()
    queue: list[tuple[str, int]] = [(entry, 0)]
    visited.add(entry)
    nodes_by_depth[0].add(entry)
    
    while queue:
        node, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                nodes_by_depth[depth + 1].add(neighbor)
                queue.append((neighbor, depth + 1))
    
    return dict(nodes_by_depth)


def _format_depth_graph_dot(
    graph_nodes: list[dict],
    graph_edges: list[dict],
    entry_node: str,
    nodes_at_depth: set[str],
    exit_nodes: set[str],
    current_depth: int,
    title: str,
    label_map: dict[str, str] | None = None,
) -> str:
    """Format a DOT graph showing only nodes at a specific depth level."""
    node_types = {node.get("node_id"): node.get("node_type", "symbol") for node in graph_nodes}
    pagerank = {node.get("node_id"): node.get("pagerank", 0.0) for node in graph_nodes}
    
    # Get edges that connect nodes within this depth scope
    relevant_nodes = nodes_at_depth | {entry_node}
    
    # Collect edges and determine which nodes actually participate in edges
    seen_edges: set[tuple[str, str]] = set()
    nodes_with_edges: set[str] = set()
    for e in graph_edges:
        from_id = e.get("from_id")
        to_id = e.get("to_id")
        if from_id and to_id and from_id in relevant_nodes and to_id in relevant_nodes:
            edge = (from_id, to_id)
            if edge not in seen_edges:
                seen_edges.add(edge)
                nodes_with_edges.add(from_id)
                nodes_with_edges.add(to_id)
    
    # Only include nodes that have edges (no orphaned nodes)
    active_nodes = nodes_at_depth & nodes_with_edges
    
    lines = ["digraph G {"]
    lines.append('  labelloc="t";')
    lines.append(f'  label="{title}";')
    lines.append('  rankdir="TB";')
    
    # Add entry node only if it has edges
    if entry_node and entry_node in nodes_with_edges:
        display = label_map.get(entry_node, entry_node) if label_map else entry_node
        display = display.replace('"', "'")
        pr = float(pagerank.get(entry_node, 0.0) or 0.0)
        lines.append(f'  "{entry_node}" [label="{display}\\nENTRY\\npr={pr:.4f}" style="filled" fillcolor="lightgreen"];')
    
    # Add nodes at this depth that have edges
    for node in sorted(active_nodes):
        if node == entry_node:
            continue
        node_type = node_types.get(node, "symbol")
        pr = float(pagerank.get(node, 0.0) or 0.0)
        display = label_map.get(node, node) if label_map else node
        display = display.replace('"', "'")
        
        if node in exit_nodes:
            lines.append(f'  "{node}" [label="{display}\\nEXIT\\n{node_type}\\npr={pr:.4f}" style="filled" fillcolor="lightcoral"];')
        else:
            lines.append(f'  "{node}" [label="{display}\\ndepth={current_depth}\\n{node_type}\\npr={pr:.4f}"];')
    
    # Add edges
    for from_id, to_id in sorted(seen_edges):
        lines.append(f'  "{from_id}" -> "{to_id}";')
    
    lines.append("}")
    return "\n".join(lines)


def _make_readable_id(node_id: str, label_map: dict[str, str] | None) -> str:
    """Create a short readable ID from label or hash prefix."""
    if label_map and node_id in label_map:
        label = label_map[node_id]
        # Skip if label is just the hash itself
        if label == node_id or (len(label) == 64 and label.isalnum()):
            return f"ext_{node_id[:8]}"
        # Extract method@file format
        if "@" in label:
            method, rest = label.split("@", 1)
            file_part = rest.split("#")[0] if "#" in rest else rest
            # Clean up the file part
            file_part = file_part.replace(".cs.cs", ".cs").replace("/", "_")
            return f"{method}_{file_part}".replace(" ", "_").replace("-", "_")
        elif ":" in label:
            # Callsite format: file:line
            return label.replace("/", "_").replace(":", "_L").replace(" ", "_")
        else:
            return label.replace(" ", "_").replace("/", "_")[:40]
    # Fallback to hash prefix for external/unresolved nodes
    return f"ext_{node_id[:8]}"


def _format_cumulative_depth_dot(
    graph_nodes: list[dict],
    edges: list[tuple[str, str]],
    entry_node: str,
    exit_nodes: set[str],
    target_depth: int,
    title: str,
    label_map: dict[str, str] | None = None,
    nodes_by_depth: dict[int, set[str]] | None = None,
) -> str:
    """Format a DOT graph showing all nodes from entry up to target_depth."""
    node_types = {node.get("node_id"): node.get("node_type", "symbol") for node in graph_nodes}
    pagerank = {node.get("node_id"): node.get("pagerank", 0.0) for node in graph_nodes}
    node_ids = {node.get("node_id") for node in graph_nodes}
    
    # Create readable ID mapping
    readable_ids: dict[str, str] = {}
    used_ids: set[str] = set()
    for node in sorted(node_ids):
        base_id = _make_readable_id(node, label_map)
        # Ensure uniqueness
        final_id = base_id
        counter = 1
        while final_id in used_ids:
            final_id = f"{base_id}_{counter}"
            counter += 1
        readable_ids[node] = final_id
        used_ids.add(final_id)
    
    # Determine depth for each node
    node_depth: dict[str, int] = {}
    if nodes_by_depth:
        for depth, nodes in nodes_by_depth.items():
            for n in nodes:
                node_depth[n] = depth
    
    lines = ["digraph G {"]
    lines.append('  labelloc="t";')
    lines.append(f'  label="{title}";')
    lines.append('  rankdir="TB";')
    
    # Add all nodes with readable IDs
    for node in sorted(node_ids):
        node_type = node_types.get(node, "symbol")
        pr = float(pagerank.get(node, 0.0) or 0.0)
        depth = node_depth.get(node, 0)
        rid = readable_ids[node]
        
        # Use readable display - clean up the label
        raw_label = label_map.get(node, node) if label_map else node
        # If label is just a hash, use the readable ID instead
        if raw_label == node or (len(raw_label) == 64 and raw_label.isalnum()):
            display = rid
        else:
            # Clean up .cs.cs duplication
            display = raw_label.replace(".cs.cs", ".cs").replace('"', "'")
        
        if node == entry_node:
            lines.append(f'  "{rid}" [label="{display}\\nENTRY\\npr={pr:.4f}" style="filled" fillcolor="lightgreen"];')
        elif node in exit_nodes:
            lines.append(f'  "{rid}" [label="{display}\\nEXIT\\n{node_type}\\npr={pr:.4f}" style="filled" fillcolor="lightcoral"];')
        else:
            lines.append(f'  "{rid}" [label="{display}\\nd={depth}\\n{node_type}\\npr={pr:.4f}"];')
    
    # Add edges with readable IDs (deduplicated)
    seen_edges: set[tuple[str, str]] = set()
    for from_id, to_id in edges:
        edge = (from_id, to_id)
        if edge not in seen_edges:
            seen_edges.add(edge)
            from_rid = readable_ids.get(from_id, from_id[:12])
            to_rid = readable_ids.get(to_id, to_id[:12])
            lines.append(f'  "{from_rid}" -> "{to_rid}";')
    
    lines.append("}")
    return "\n".join(lines)


def _entry_graph_edges(
    edges: list[tuple[str, str]],
    reachable: set[str],
    entry_nodes: set[str],
    entry_type: str,
) -> list[tuple[str, str]]:
    if entry_type == "entry_group":
        return [
            (source, target)
            for source, target in edges
            if source in reachable
            and target in reachable
            and not (target in entry_nodes and source not in entry_nodes)
        ]
    return [
        (source, target)
        for source, target in edges
        if source in reachable and target in reachable and target not in entry_nodes
    ]


def _entry_graph_candidates(
    graph_nodes: list[dict],
    graph_edges: list[dict],
    entry_graph_max_depth: int,
    entry_graph_node_limit: int,
    entry_graph_depth_threshold: int,
    entry_graph_top_k: int | None,
) -> tuple[list[dict], dict[str, object]]:
    node_ids = [row.get("node_id") for row in graph_nodes if row.get("node_id")]
    edges = [
        (row.get("from_id"), row.get("to_id"))
        for row in graph_edges
        if row.get("from_id") and row.get("to_id")
    ]
    out_degree_counts: dict[str, int] = defaultdict(int)
    in_degree_counts: dict[str, int] = defaultdict(int)
    for from_id, to_id in edges:
        out_degree_counts[from_id] += 1
        in_degree_counts[to_id] += 1

    adjacency: dict[str, list[str]] = {node: [None] * count for node, count in out_degree_counts.items()}
    reverse_adjacency: dict[str, list[str]] = {node: [None] * count for node, count in in_degree_counts.items()}
    out_pos: dict[str, int] = defaultdict(int)
    in_pos: dict[str, int] = defaultdict(int)
    for from_id, to_id in edges:
        idx = out_pos[from_id]
        adjacency[from_id][idx] = to_id
        out_pos[from_id] += 1
        ridx = in_pos[to_id]
        reverse_adjacency[to_id][ridx] = from_id
        in_pos[to_id] += 1
    in_degree: dict[str, int] = defaultdict(int, in_degree_counts)
    out_degree: dict[str, int] = defaultdict(int, out_degree_counts)
    for key, vals in adjacency.items():
        adjacency[key] = [v for v in vals if v]
    for key, vals in reverse_adjacency.items():
        reverse_adjacency[key] = [v for v in vals if v]
    sccs = _strongly_connected_components(node_ids, adjacency)
    entry_candidates = [
        node_id
        for node_id in node_ids
        if in_degree.get(node_id, 0) == 0 and out_degree.get(node_id, 0) > 0
    ]
    entry_groups: list[dict[str, object]] = []
    entry_group_nodes: set[str] = set()
    for comp in sccs:
        if len(comp) == 1:
            continue
        has_incoming = False
        for node in comp:
            for pred in reverse_adjacency.get(node, []):
                if pred not in comp:
                    has_incoming = True
                    break
            if has_incoming:
                break
        if not has_incoming:
            group_nodes = sorted(comp)
            group_id = "scc_" + "_".join(group_nodes)
            entry_groups.append({"group_id": group_id, "nodes": group_nodes})
            entry_group_nodes.update(group_nodes)
    recursive: set[str] = set()
    for node in node_ids:
        if node in adjacency.get(node, []):
            recursive.add(node)
    for comp in sccs:
        if len(comp) > 1:
            recursive |= comp
    exit_nodes = {
        node_id for node_id in node_ids if out_degree.get(node_id, 0) == 0 or node_id in recursive
    }
    entry_cache: dict[str, tuple[dict[str, float], set[str]]] = {}
    candidates: list[dict] = []
    reachable_sets: list[set[str]] = []
    excluded: list[dict] = []
    for entry in entry_candidates:
        metrics, reachable = _entry_graph_depth_metrics(
            adjacency,
            entry,
            entry_graph_max_depth,
            entry_graph_node_limit,
        )
        entry_cache[entry] = (metrics, reachable)
        if not reachable & exit_nodes:
            excluded.append(
                {
                    "entry_key": entry,
                    "entry_type": "entry",
                    "reason": "no_exit",
                    "metrics": metrics,
                    "entry_nodes": [entry],
                }
            )
            continue
        if metrics["capped_depth"] < entry_graph_depth_threshold:
            excluded.append(
                {
                    "entry_key": entry,
                    "entry_type": "entry",
                    "reason": "below_threshold",
                    "metrics": metrics,
                    "entry_nodes": [entry],
                }
            )
            continue
        if any(reachable < other for other in reachable_sets):
            continue
        candidates.append(
            {
                "entry_key": entry,
                "entry_type": "entry",
                "entry_nodes": [entry],
                "reachable": reachable,
                "metrics": metrics,
            }
        )
        reachable_sets.append(reachable)
    for group in entry_groups:
        group_id = str(group.get("group_id", "group"))
        group_nodes = set(group.get("nodes", []))
        if not group_nodes:
            continue
        reachable = set(group_nodes)
        metrics_by_node: list[dict[str, float]] = []
        for entry in group_nodes:
            metrics, entry_reachable = entry_cache.get(entry) or _entry_graph_depth_metrics(
                adjacency,
                entry,
                entry_graph_max_depth,
                entry_graph_node_limit,
            )
            entry_cache[entry] = (metrics, entry_reachable)
            metrics_by_node.append(metrics)
            reachable |= entry_reachable
        if not reachable & exit_nodes:
            excluded.append(
                {
                    "entry_key": group_id,
                    "entry_type": "entry_group",
                    "reason": "no_exit",
                    "metrics": metrics_by_node[0] if metrics_by_node else {},
                    "entry_nodes": sorted(group_nodes),
                }
            )
            continue
        metrics = max(metrics_by_node, key=lambda item: item["max_depth"]) if metrics_by_node else {}
        if metrics.get("capped_depth", 0.0) < entry_graph_depth_threshold:
            excluded.append(
                {
                    "entry_key": group_id,
                    "entry_type": "entry_group",
                    "reason": "below_threshold",
                    "metrics": metrics,
                    "entry_nodes": sorted(group_nodes),
                }
            )
            continue
        if any(reachable < other for other in reachable_sets):
            continue
        candidates.append(
            {
                "entry_key": group_id,
                "entry_type": "entry_group",
                "entry_nodes": sorted(group_nodes),
                "reachable": reachable,
                "metrics": metrics,
            }
        )
        reachable_sets.append(reachable)
    eligible = list(candidates)
    if entry_graph_top_k is not None:
        candidates = sorted(
            candidates,
            key=lambda item: (
                float(item["metrics"]["capped_depth"]),
                float(item["metrics"]["depth_breadth"]),
            ),
            reverse=True,
        )[: entry_graph_top_k]
    summary = {
        "exit_nodes": exit_nodes,
        "excluded": excluded,
        "eligible": eligible,
        "entry_candidates": entry_candidates,
        "entry_groups": entry_groups,
        "edges": edges,
    }
    return candidates, summary


def _strongly_connected_components(
    node_ids: list[str], adjacency: dict[str, list[str]]
) -> list[set[str]]:
    graph = nx.DiGraph()
    graph.add_nodes_from(node_ids)
    for src, targets in adjacency.items():
        for dst in targets:
            graph.add_edge(src, dst)
    return [set(comp) for comp in nx.strongly_connected_components(graph)]


def _entry_graph_state_map(
    client,
    output_root: Path,
    run_id: str,
    artifact_version: int,
    incremental: bool,
) -> dict[str, dict]:
    if not incremental:
        return {}
    try:
        rows = _fetch_rows(client, output_root, "entry_graph_state", run_id, artifact_version)
    except ValueError:
        rows = []
    state_map: dict[str, dict] = {}
    for row in rows:
        entry_key = row.get("entry_key")
        if entry_key:
            state_map[str(entry_key)] = row
    return state_map


def _entry_graph_item_result(
    item: dict,
    edges_summary: list,
    processed_existing: set[str],
    entry_graph_incremental: bool,
) -> tuple[dict | None, dict, str, str]:
    entry_key = str(item["entry_key"])
    entry_type = str(item["entry_type"])
    entry_nodes = set(item.get("entry_nodes", []))
    reachable = item.get("reachable", set())
    metrics = item.get("metrics", {})
    if entry_graph_incremental and entry_key in processed_existing:
        entry_state_row = {
            "entry_key": entry_key,
            "entry_type": entry_type,
            "status": "skipped",
            "reason": "already_processed",
            "metrics": json.dumps(metrics, ensure_ascii=True),
            "source_ref": entry_key,
        }
        return None, entry_state_row, "skipped", entry_key

    edges = _entry_graph_edges(
        edges_summary,
        reachable,
        entry_nodes,
        entry_type,
    )
    entry_graph_row = {
        "entry_key": entry_key,
        "entry_type": entry_type,
        "entry_nodes": json.dumps(sorted(entry_nodes), ensure_ascii=True),
        "reachable_nodes": json.dumps(sorted(reachable), ensure_ascii=True),
        "reachable_edges": json.dumps(edges, ensure_ascii=True),
        "metrics": json.dumps(metrics, ensure_ascii=True),
        "capped_depth": metrics.get("capped_depth", 0.0),
        "normalized_depth": metrics.get("normalized", 0.0),
        "log_scaled_depth": metrics.get("log_scaled", 0.0),
        "depth_breadth": metrics.get("depth_breadth", 0.0),
        "reachable_nodes_count": metrics.get("reachable_nodes", 0.0),
        "edge_count": len(edges),
        "source_ref": entry_key,
    }
    entry_state_row = {
        "entry_key": entry_key,
        "entry_type": entry_type,
        "status": "processed",
        "reason": "processed",
        "metrics": json.dumps(metrics, ensure_ascii=True),
        "source_ref": entry_key,
    }
    return entry_graph_row, entry_state_row, "processed", entry_key


def _entry_graph_worker(args: tuple[dict, list, set[str], bool]) -> tuple[dict | None, dict, str, str]:
    item, edges_summary, processed_existing, entry_graph_incremental = args
    return _entry_graph_item_result(item, edges_summary, processed_existing, entry_graph_incremental)


def _symbol_ext_map(symbols: list[dict]) -> dict[str, str]:
    ext_map: dict[str, str] = {}
    for row in symbols:
        symbol_id = row.get("symbol_id")
        if not symbol_id:
            continue
        file_path = row.get("file_path", "")
        ext = Path(file_path).suffix.lower()
        if ext:
            ext_map[symbol_id] = ext
    return ext_map


def _llm_response_text(config: ParserConfig, prompt: str) -> str:
    if config.llm_cmd:
        result = subprocess.run(
            config.llm_cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=config.llm_timeout_sec,
            check=True,
        )
        return result.stdout.strip()
    provider = (config.llm_provider or "copilot").lower()
    if provider in ("copilot", "github"):
        # Use GitHub/Copilot LLM via models.inference.ai.azure.com
        api_key = os.environ.get("GITHUB_TOKEN")
        if not api_key:
            raise RuntimeError("GITHUB_TOKEN environment variable is required for Copilot LLM")
        base_url = config.llm_base_url if config.llm_base_url else "https://models.inference.ai.azure.com/chat/completions"
        model = config.llm_model or "gpt-4o-mini"
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }).encode("utf-8")
        request = urllib.request.Request(
            base_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("Copilot LLM response missing choices")
        return str(choices[0].get("message", {}).get("content", "")).strip()
    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI LLM calls")
        if not config.llm_model:
            raise RuntimeError("llm_model is required for OpenAI LLM calls")
        payload = json.dumps(
            {
                "model": config.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("OpenAI response missing choices")
        return str(choices[0].get("message", {}).get("content", "")).strip()
    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is required for Gemini LLM calls")
        if not config.llm_model:
            raise RuntimeError("llm_model is required for Gemini LLM calls")
        payload = json.dumps(
            {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2},
            }
        ).encode("utf-8")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{config.llm_model}:generateContent?key={api_key}"
        )
        request = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini response missing candidates")
        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            raise ValueError("Gemini response missing content parts")
        return str(parts[0].get("text", "")).strip()
    if provider == "ollama":
        if not config.llm_model:
            raise RuntimeError("llm_model is required for Ollama LLM calls")
        base_url = (config.llm_base_url or "http://localhost:11434").rstrip("/")
        def _ollama_call(format_value: str | None) -> dict:
            payload_dict = {
                "model": config.llm_model,
                "prompt": prompt,
                "stream": False,
            }
            if format_value:
                payload_dict["format"] = format_value
            payload = json.dumps(payload_dict).encode("utf-8")
            request = urllib.request.Request(
                f"{base_url}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
                return json.load(response)

        data = _ollama_call("json")
        response_text = data.get("response") if isinstance(data, dict) else None
        response_error = None
        if isinstance(data, dict) and isinstance(data.get("error"), str):
            response_error = data["error"]
        elif isinstance(response_text, str):
            try:
                parsed = json.loads(response_text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, dict) and isinstance(parsed.get("error"), str):
                response_error = parsed["error"]
        if response_error:
            data = _ollama_call(None)
            if isinstance(data, dict) and isinstance(data.get("error"), str):
                raise ValueError(f"Ollama error: {data['error']}")
            response_text = data.get("response") if isinstance(data, dict) else None
        text = response_text
        if not isinstance(text, str):
            raise ValueError("Ollama response missing 'response' text")
        return text.strip()
    raise RuntimeError("llm_cmd or supported llm_provider is required for LLM calls")


def _extract_json_fragment(text: str) -> object:
    start_brace = text.find("{")
    end_brace = text.rfind("}")
    if start_brace != -1 and end_brace > start_brace:
        return json.loads(text[start_brace : end_brace + 1])
    raise ValueError("LLM response is not JSON")


def _parse_llm_json(text: str) -> dict:
    try:
        payload = json.loads(text)
        if isinstance(payload, dict) and isinstance(payload.get("response"), str):
            response_text = payload["response"]
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return _extract_json_fragment(response_text)
        if isinstance(payload, dict):
            if isinstance(payload.get("error"), str):
                raise ValueError(f"LLM error: {payload['error']}")
            return payload
    except json.JSONDecodeError:
        pass
    result = _extract_json_fragment(text)
    if not isinstance(result, dict):
        raise ValueError("LLM response JSON is not an object")
    return result


def _call_llm_json(config: ParserConfig, prompt: str) -> dict:
    text = _llm_response_text(config, prompt)
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    return _parse_llm_json(text)


def _call_llm_json_with_text(config: ParserConfig, prompt: str) -> tuple[dict, str]:
    text = _llm_response_text(config, prompt)
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    return _parse_llm_json(text), text


def _debug_llm_error(
    rows: list[dict],
    entry_key: str,
    prompt: str,
    exc: Exception,
    response_text: str | None = None,
) -> None:
    row = {
        "entry_key": entry_key,
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "prompt": prompt,
        "source_ref": entry_key,
    }
    if response_text:
        row["response"] = response_text
    rows.append(row)


def _debug_llm_issue(
    rows: list[dict],
    entry_key: str,
    prompt: str,
    error_type: str,
    message: str,
    response_text: str | None = None,
) -> None:
    row = {
        "entry_key": entry_key,
        "error_type": error_type,
        "error_message": message,
        "prompt": prompt,
        "source_ref": entry_key,
    }
    if response_text:
        row["response"] = response_text
    rows.append(row)


def _entry_graph_summary_batch_prompt(
    items: list[dict],
    max_chars: int,
    fields: list[str],
) -> str:
    payload = json.dumps(items, ensure_ascii=True)
    extra = "\n".join(f"- {field}" for field in fields)
    prompt = f"""
You are a software analyst. Summarize each graph slice in clear English and a compact math description.

Return JSON array with objects:
- entry_key
- summary_en (plain English, <= {max_chars} chars)
- summary_math (math-style, mention G=(V,E), entry set, exit set, depth/breadth, <= {max_chars} chars)
- actor_hints
- business_rule_hint
- language_tags
{extra}

Items: {payload}
"""
    return prompt.strip()


def _node_symbol_maps(nodes: list[dict], symbols: list[dict]) -> tuple[dict[str, str], dict[str, tuple[str, int]]]:
    node_to_sym: dict[str, str] = {}
    for row in nodes:
        nid = row.get("node_id")
        sym = row.get("symbol_id")
        if nid and sym:
            node_to_sym[str(nid)] = str(sym)
    sym_to_src: dict[str, tuple[str, int]] = {}
    for row in symbols:
        sym_id = row.get("symbol_id")
        file_path = row.get("file_path")
        line = row.get("line")
        if sym_id and file_path and isinstance(line, int):
            sym_to_src[str(sym_id)] = (str(file_path), int(line))
    return node_to_sym, sym_to_src


def _read_snippet(file_path: str, line: int, context: int = 4) -> str:
    try:
        lines = Path(file_path).read_text(errors="ignore").splitlines()
        start = max(0, line - 1 - context)
        end = min(len(lines), line + context)
        return "\n".join(lines[start:end])
    except OSError as exc:
        LOGGER.debug("read_snippet_failed path=%s line=%s error=%s", file_path, line, exc)
        return ""


def _load_entry_graph_candidates_from_parquet(
    client,
    config: ParserConfig,
) -> tuple[
    list[dict],
    set[str],
    dict[str, str],
    dict[str, str],
    list[dict],
    list[dict],
    dict[str, float],
]:
    code_graph_nodes = _fetch_rows(
        client, config.output_root, "code_graph_nodes", config.run_id, config.artifact_version
    )
    code_graph_edges = _fetch_rows(
        client, config.output_root, "code_graph_edges", config.run_id, config.artifact_version
    )
    symbols = _fetch_rows(client, config.output_root, "symbols", config.run_id, config.artifact_version)
    entry_graphs = _fetch_rows(
        client, config.output_root, "entry_graphs", config.run_id, config.artifact_version
    )
    graph_metadata = _fetch_rows(
        client, config.output_root, "graph_metadata", config.run_id, config.artifact_version
    )
    graph_label_map = _graph_label_map(symbols, code_graph_nodes)
    symbol_exts = _symbol_ext_map(symbols)
    pagerank_by_node = {str(row.get("node_id")): float(row.get("pagerank", 0.0)) for row in graph_metadata}
    # compute exit_nodes (out_degree==0 or recursive)
    graph = nx.DiGraph()
    for node in code_graph_nodes:
        node_id = node.get("node_id")
        if node_id:
            graph.add_node(node_id)
    for edge in code_graph_edges:
        u = edge.get("from_id")
        v = edge.get("to_id")
        if u and v:
            graph.add_edge(u, v)
    recursive = {n for n in graph.nodes if graph.has_edge(n, n)}
    for comp in nx.strongly_connected_components(graph):
        if len(comp) > 1:
            recursive |= set(comp)
    out_degree = dict(graph.out_degree())
    exit_nodes = {
        node for node in graph.nodes if out_degree.get(node, 0) == 0 or node in recursive
    }
    candidates: list[dict] = []
    for row in entry_graphs:
        entry_key = str(row.get("entry_key", ""))
        entry_type = str(row.get("entry_type", "entry"))
        entry_nodes = json.loads(row.get("entry_nodes") or "[]")
        reachable = set(json.loads(row.get("reachable_nodes") or "[]"))
        metrics = json.loads(row.get("metrics") or "{}")
        candidates.append(
            {
                "entry_key": entry_key,
                "entry_type": entry_type,
                "entry_nodes": entry_nodes,
                "reachable": reachable,
                "metrics": metrics,
            }
        )
    pagerank_by_node = {str(row.get("node_id")): float(row.get("pagerank", 0.0)) for row in graph_metadata}
    return candidates, exit_nodes, graph_label_map, symbol_exts, code_graph_nodes, symbols, pagerank_by_node


def _build_entry_graph_summaries(
    candidates: list[dict],
    exit_nodes: set[str],
    label_map: dict[str, str],
    symbol_exts: dict[str, str],
    code_graph_nodes: list[dict],
    symbols: list[dict],
    pagerank_by_node: dict[str, float],
    config: ParserConfig,
) -> tuple[list[dict], list[dict]]:
    summaries: list[dict] = []
    debug_rows: list[dict] = []
    items: list[dict] = []
    field_flags = config.entry_graph_summary_fields or {}
    extra_fields = [key for key, enabled in field_flags.items() if enabled]
    node_to_sym, sym_to_src = _node_symbol_maps(code_graph_nodes, symbols)
    seen_reachable: list[set[str]] = []
    for rank, item in enumerate(candidates, start=1):
        entry_key = str(item.get("entry_key", ""))
        entry_type = str(item.get("entry_type", ""))
        entry_nodes = [str(node) for node in item.get("entry_nodes", [])]
        reachable = set(item.get("reachable", set()))
        max_depth = float(item.get("metrics", {}).get("capped_depth", 0.0))
        if max_depth < float(config.entry_graph_min_depth):
            continue
        entry_labels = [label_map.get(node, node) for node in entry_nodes]
        exit_labels = [
            label_map.get(node, node)
            for node in sorted(exit_nodes & reachable)
        ]
        entry_file_exts = sorted({symbol_exts.get(node, "") for node in entry_nodes if symbol_exts.get(node, "")})
        # Entry source
        entry_node_id = entry_nodes[0] if entry_nodes else entry_key
        entry_sym = node_to_sym.get(entry_node_id)
        entry_src = sym_to_src.get(entry_sym) if entry_sym else None
        if not entry_src:
            continue
        entry_file = entry_src[0] if entry_src else ""
        entry_line = entry_src[1] if entry_src else None
        entry_snippet = (
            _read_snippet(entry_file, entry_line, context=4) if entry_src else ""
        )
        entry_ext = Path(entry_file).suffix if entry_file else ""
        entry_pagerank = pagerank_by_node.get(entry_node_id, 0.0)
        # Deduplicate on reachable set to keep only unique graphs
        is_subset = any(reachable and reachable.issubset(prev) for prev in seen_reachable)
        if is_subset:
            continue
        seen_reachable.append(reachable)
        LOGGER.info(
            "entry_graph_unique entry_key=%s file=%s ext=%s depth=%.2f breadth=%s pagerank=%.6f",
            entry_key,
            Path(entry_file).name if entry_file else "",
            entry_ext,
            max_depth,
            item.get("metrics", {}).get("depth_breadth", ""),
            entry_pagerank,
        )
        # Exit sources
        exit_sources = []
        for exit_id in sorted(exit_nodes & reachable):
            sym = node_to_sym.get(exit_id)
            src = sym_to_src.get(sym) if sym else None
            exit_sources.append(
                {
                    "node_id": exit_id,
                    "file_path": src[0] if src else "",
                    "line": src[1] if src else None,
                    "snippet": _read_snippet(src[0], src[1], context=2) if src else "",
                }
            )
        items.append(
            {
                "entry_key": entry_key,
                "entry_type": entry_type,
                "entry_nodes": entry_labels,
                "exit_nodes": exit_labels,
                "metrics": item.get("metrics", {}),
                "entry_file_exts": entry_file_exts,
                "rank": rank,
                "entry_source": {
                    "file_path": entry_file,
                    "line": entry_line,
                    "snippet": entry_snippet,
                },
                "entry_pagerank": entry_pagerank,
                "exit_sources": exit_sources,
            }
        )
    batch_size = max(1, config.entry_graph_llm_batch_size)
    for start in range(0, len(items), batch_size):
        batch = items[start : start + batch_size]
        prompt = _entry_graph_summary_batch_prompt(
            batch,
            config.llm_max_input_chars,
            extra_fields,
        )
        batch_response_text = None
        try:
            payload_items, batch_response_text = _call_llm_json_with_text(config, prompt)
            if config.entry_graph_llm_log_response and batch_response_text:
                LOGGER.info(
                    "llm_response_batch chars=%s preview=%s",
                    len(batch_response_text),
                    batch_response_text[:400].replace("\n", " "),
                )
        except ValueError as exc:
            LOGGER.warning(
                "llm_batch_value_error batch=%s/%s error=%s",
                start // batch_size + 1,
                math.ceil(len(items) / batch_size),
                exc,
            )
            payload_items = []
            if config.entry_graph_llm_debug:
                for item in batch:
                    _debug_llm_error(
                        debug_rows,
                        str(item.get("entry_key", "")),
                        prompt,
                        exc,
                        batch_response_text,
                    )
            if config.entry_graph_llm_strict:
                raise
            continue
        except Exception as exc:  # noqa: BLE001
            LOGGER.warning(
                "llm_batch_failed batch=%s/%s error=%s",
                start // batch_size + 1,
                math.ceil(len(items) / batch_size),
                exc,
            )
            if config.entry_graph_llm_debug:
                for item in batch:
                    _debug_llm_error(
                        debug_rows,
                        str(item.get("entry_key", "")),
                        prompt,
                        exc,
                        batch_response_text,
                    )
            if config.entry_graph_llm_strict:
                raise
            payload_items = []
        if isinstance(payload_items, dict) and isinstance(payload_items.get("items"), list):
            payload_items = payload_items["items"]
        if isinstance(payload_items, dict):
            payload_items = [payload_items]
        if not isinstance(payload_items, list):
            raise ValueError("LLM summary response is not a list")
        payload_by_key: dict[str, dict] = {}
        for entry in payload_items:
            if isinstance(entry, dict):
                entry_key = str(entry.get("entry_key", "")).strip()
                if entry_key:
                    payload_by_key[entry_key] = entry
        for item in batch:
            entry_key = str(item.get("entry_key", ""))
            payload = payload_by_key.get(entry_key)
            if not payload:
                single_prompt = _entry_graph_summary_batch_prompt(
                    [item],
                    config.llm_max_input_chars,
                    extra_fields,
                )
                single_response_text = None
                try:
                    single_payload, single_response_text = _call_llm_json_with_text(
                        config, single_prompt
                    )
                except ValueError as exc:
                    LOGGER.warning("llm_single_value_error entry=%s error=%s", entry_key, exc)
                    if config.entry_graph_llm_debug:
                        _debug_llm_error(
                            debug_rows,
                            entry_key,
                            single_prompt,
                            exc,
                            single_response_text,
                        )
                    if config.entry_graph_llm_strict:
                        raise
                    summary_row = {
                        "entry_key": entry_key,
                        "entry_type": item.get("entry_type", ""),
                        "summary_en": "Summary unavailable: LLM request failed.",
                        "summary_math": "Summary unavailable: LLM request failed.",
                        "llm_error": f"value_error:{type(exc).__name__}",
                        "source_ref": entry_key,
                    }
                    if field_flags.get("rank"):
                        summary_row["rank"] = item.get("rank", 0)
                    summaries.append(summary_row)
                    continue
                except Exception as exc:  # noqa: BLE001
                    LOGGER.warning("llm_single_failed entry=%s error=%s", entry_key, exc)
                    if config.entry_graph_llm_debug:
                        _debug_llm_error(
                            debug_rows,
                            entry_key,
                            single_prompt,
                            exc,
                            single_response_text,
                        )
                    if config.entry_graph_llm_strict:
                        raise
                    summary_row = {
                        "entry_key": entry_key,
                        "entry_type": item.get("entry_type", ""),
                        "summary_en": "Summary unavailable: LLM request failed.",
                        "summary_math": "Summary unavailable: LLM request failed.",
                        "llm_error": f"exception:{type(exc).__name__}",
                        "source_ref": entry_key,
                    }
                    if field_flags.get("rank"):
                        summary_row["rank"] = item.get("rank", 0)
                    summaries.append(summary_row)
                    continue
                if isinstance(single_payload, dict) and isinstance(single_payload.get("items"), list):
                    items_list = single_payload["items"]
                    if items_list and isinstance(items_list[0], dict):
                        payload = items_list[0]
                elif isinstance(single_payload, dict):
                    payload = single_payload
            if not payload:
                if config.entry_graph_llm_strict:
                    raise ValueError(f"LLM summary missing for entry {entry_key}")
                if config.entry_graph_llm_debug:
                    _debug_llm_issue(
                        debug_rows,
                        entry_key,
                        prompt,
                        "missing_response",
                        "payload missing",
                        batch_response_text,
                    )
                summary_row = {
                    "entry_key": entry_key,
                    "entry_type": item.get("entry_type", ""),
                    "summary_en": "Summary unavailable: LLM did not return a response.",
                    "summary_math": "Summary unavailable: LLM did not return a response.",
                    "llm_error": "missing_response",
                    "source_ref": entry_key,
                }
                if field_flags.get("rank"):
                    summary_row["rank"] = item.get("rank", 0)
                summaries.append(summary_row)
                continue
            summary_en = str(payload.get("summary_en", "")).strip()
            summary_math = str(payload.get("summary_math", "")).strip()
            if not summary_en or not summary_math:
                if config.entry_graph_llm_strict:
                    raise ValueError(f"LLM summary missing for entry {entry_key}")
                if config.entry_graph_llm_debug:
                    response_text = batch_response_text
                    if not response_text:
                        try:
                            response_text = json.dumps(payload, ensure_ascii=True)
                        except TypeError:
                            response_text = None
                    _debug_llm_issue(
                        debug_rows,
                        entry_key,
                        prompt,
                        "empty_fields",
                        "summary fields empty",
                        response_text,
                    )
                summary_row = {
                    "entry_key": entry_key,
                    "entry_type": item.get("entry_type", ""),
                    "summary_en": "Summary unavailable: LLM returned empty fields.",
                    "summary_math": "Summary unavailable: LLM returned empty fields.",
                    "llm_error": "empty_fields",
                    "source_ref": entry_key,
                }
                if field_flags.get("rank"):
                    summary_row["rank"] = item.get("rank", 0)
                summaries.append(summary_row)
                continue
            summary_row = {
                "entry_key": entry_key,
                "entry_type": item.get("entry_type", ""),
                "summary_en": summary_en,
                "summary_math": summary_math,
                "source_ref": entry_key,
            }
            if config.entry_graph_llm_store_response:
                try:
                    summary_row["llm_response"] = json.dumps(payload, ensure_ascii=True)
                except TypeError:
                    summary_row["llm_response"] = str(payload)
            if field_flags.get("actor_hints"):
                summary_row["actor_hints"] = str(payload.get("actor_hints", "")).strip()
            if field_flags.get("business_rule_hint"):
                summary_row["business_rule_hint"] = str(
                    payload.get("business_rule_hint", "")
                ).strip()
            if field_flags.get("language_tags"):
                tags = payload.get("language_tags", [])
                if not isinstance(tags, list):
                    tags = []
                summary_row["language_tags"] = json.dumps(tags, ensure_ascii=True)
            if field_flags.get("rank"):
                summary_row["rank"] = item.get("rank", 0)
            summaries.append(
                summary_row
            )
    return summaries, debug_rows


def _run_entry_graph_llm_phase(
    candidates: list[dict],
    exit_nodes: set[str],
    graph_label_map: dict[str, str],
    symbol_exts: dict[str, str],
    graph_nodes: list[dict],
    symbol_rows: list[dict],
    pagerank_by_node: dict[str, float],
    output_root: Path,
    created_at: str,
    config: ParserConfig,
    state: dict,
) -> dict:
    entry_graph_summaries, entry_graph_debug = _build_entry_graph_summaries(
        candidates,
        exit_nodes,
        graph_label_map,
        symbol_exts,
        graph_nodes,
        symbol_rows,
        pagerank_by_node,
        config,
    )
    write_parquet(
        output_root,
        "entry_graph_summaries",
        _with_metadata(entry_graph_summaries, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    merged_rows: list[dict] = []
    if config.entry_graph_llm_merge_enabled:
        merged_rows = _merge_entry_graph_summaries(entry_graph_summaries, config)
        write_parquet(
            output_root,
            "entry_graph_summaries_merged",
            _with_metadata(merged_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if config.entry_graph_llm_debug and entry_graph_debug:
        write_parquet(
            output_root,
            "entry_graph_llm_debug",
            _with_metadata(entry_graph_debug, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    state = finalize_state(
        state,
        processed_count=state.get("processed_count", 0),
        outputs={
            **state.get("outputs", {}),
            "entry_graph_summaries": len(entry_graph_summaries),
            "entry_graph_summaries_merged": len(merged_rows),
            "entry_graph_llm_debug": len(entry_graph_debug),
        },
        notes={**state.get("notes", {}), "llm_phase": True},
    )
    return state


def _merge_entry_graph_summaries(
    summaries: list[dict],
    config: ParserConfig,
) -> list[dict]:
    if not summaries:
        return []
    joiner = config.entry_graph_llm_merge_join
    max_chars = config.entry_graph_llm_merge_max_chars
    entry_keys: list[str] = []
    language_tags: set[str] = set()

    def _collect_text(field: str) -> str:
        parts: list[str] = []
        for row in summaries:
            entry_key = str(row.get("entry_key", "")).strip()
            text = str(row.get(field, "")).strip()
            if not text:
                continue
            if entry_key:
                parts.append(f"{entry_key}: {text}")
            else:
                parts.append(text)
        merged = joiner.join(parts)
        if max_chars and len(merged) > max_chars:
            merged = merged[:max_chars].rstrip()
        return merged

    for row in summaries:
        entry_key = str(row.get("entry_key", "")).strip()
        if entry_key:
            entry_keys.append(entry_key)
        raw_tags = row.get("language_tags")
        if isinstance(raw_tags, str) and raw_tags:
            try:
                tags = json.loads(raw_tags)
            except json.JSONDecodeError:
                tags = []
            if isinstance(tags, list):
                for tag in tags:
                    if isinstance(tag, str) and tag:
                        language_tags.add(tag)

    return [
        {
            "merge_key": "entry_graph_summaries",
            "entry_count": len(entry_keys),
            "entry_keys": json.dumps(entry_keys, ensure_ascii=True),
            "summary_en_merged": _collect_text("summary_en"),
            "summary_math_merged": _collect_text("summary_math"),
            "actor_hints_merged": _collect_text("actor_hints"),
            "business_rule_hint_merged": _collect_text("business_rule_hint"),
            "language_tags_merged": json.dumps(sorted(language_tags), ensure_ascii=True),
            "source_ref": "entry_graph_summaries",
        }
    ]


def _write_if_changed(path: Path, content: str, incremental: bool) -> bool:
    if incremental and path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


def _graph_label_sets(
    entry_candidates: list[str],
    entry_groups: list[dict[str, object]],
    exit_nodes: set[str],
) -> tuple[set[str], set[str], set[str]]:
    entry_nodes = set(entry_candidates)
    entry_group_nodes: set[str] = set()
    for group in entry_groups:
        entry_group_nodes.update(group.get("nodes", []))
    return entry_nodes, entry_group_nodes, exit_nodes


def _graph_label_map(symbols: list[dict], graph_nodes: list[dict]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for node in graph_nodes:
        node_id = node.get("node_id")
        if node_id:
            labels[node_id] = str(node.get("label", node_id))
    for row in symbols:
        symbol_id = row.get("symbol_id")
        if not symbol_id:
            continue
        name = row.get("name") or row.get("signature") or symbol_id
        path_obj = Path(row.get("file_path", ""))
        file_name = path_obj.name
        file_ext = path_obj.suffix.lower()
        suffix = symbol_id[:6]
        if file_name:
            labels[symbol_id] = f"{name}@{file_name}{file_ext}#{suffix}"
        else:
            labels[symbol_id] = f"{name}{file_ext}#{suffix}"
    return labels


def _format_graph_dot(
    graph_nodes: list[dict],
    graph_edges: list[dict],
    entry_nodes: set[str],
    entry_group_nodes: set[str],
    exit_nodes: set[str],
    title: str,
    label_map: dict[str, str] | None = None,
) -> str:
    node_types = {node.get("node_id"): node.get("node_type", "symbol") for node in graph_nodes}
    pagerank = {node.get("node_id"): node.get("pagerank", 0.0) for node in graph_nodes}
    node_ids = set(node_types.keys())
    
    # Create readable ID mapping
    readable_ids: dict[str, str] = {}
    used_ids: set[str] = set()
    for node in sorted(node_ids):
        base_id = _make_readable_id(node, label_map)
        final_id = base_id
        counter = 1
        while final_id in used_ids:
            final_id = f"{base_id}_{counter}"
            counter += 1
        readable_ids[node] = final_id
        used_ids.add(final_id)
    
    lines = ["digraph G {"]
    lines.append('  labelloc="t";')
    lines.append(f'  label="{title}";')
    for node in sorted(node_types):
        node_type = node_types.get(node, "symbol")
        pr = float(pagerank.get(node, 0.0) or 0.0)
        rid = readable_ids[node]
        
        # Use readable display - clean up the label
        raw_label = label_map.get(node, node) if label_map else node
        if raw_label == node or (len(raw_label) == 64 and raw_label.isalnum()):
            display = rid
        else:
            display = raw_label.replace(".cs.cs", ".cs").replace('"', "'")
        
        if node in entry_nodes:
            role = "entry"
        elif node in entry_group_nodes:
            role = "entry_group"
        elif node in exit_nodes:
            role = "exit"
        else:
            role = "node"
        lines.append(
            f'  "{rid}" [label="{display}\\n{role}\\n{node_type}\\npr={pr:.4f}"];'
        )
    seen_edges: set[tuple[str, str]] = set()
    for row in graph_edges:
        from_id = row.get("from_id")
        to_id = row.get("to_id")
        if from_id and to_id:
            edge = (from_id, to_id)
            if edge not in seen_edges:
                seen_edges.add(edge)
                from_rid = readable_ids.get(from_id, from_id[:12])
                to_rid = readable_ids.get(to_id, to_id[:12])
                lines.append(f'  "{from_rid}" -> "{to_rid}";')
    lines.append("}")
    return "\n".join(lines)


def _safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)


def _display_path(file_path: str, base_dir: Path | None) -> str:
    if not file_path:
        return ""
    path_obj = Path(file_path)
    if base_dir and path_obj.is_absolute():
        try:
            return str(path_obj.relative_to(base_dir))
        except ValueError:
            return path_obj.name
    return str(path_obj)


def _entry_graph_basename(
    raw_label: str,
    entry_key: str,
    entry_type: str,
    index: int,
) -> str:
    label_part = raw_label.split("#", 1)[0]
    if entry_type == "entry" and "@" in label_part:
        name, file_part = label_part.split("@", 1)
        path_obj = Path(file_part)
        ext = path_obj.suffix.lstrip(".") or "noext"
        file_stem = path_obj.stem or "nofile"
        base = f"{file_stem}_{name}"
    elif entry_type == "entry":
        file_name = Path(label_part).name or "nofile"
        base = f"no_ext_{file_name}"
    else:
        base = f"group_{entry_key}"
    safe = _safe_filename(base)
    rand = entry_key[:8] or f"{index:02d}"
    return f"{safe}_{index:02d}_{rand}"


def _render_graph(
    dot_path: Path,
    out_path: Path,
    incremental: bool,
    engine: str,
    fmt: str,
) -> None:
    if incremental and out_path.exists():
        return
    exe = shutil.which(engine)
    if not exe:
        return
    subprocess.run([exe, f"-T{fmt}", str(dot_path), "-o", str(out_path)], check=True)


_TABLE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("select", re.compile(r"\bfrom\s+([A-Za-z0-9_\.\[\]`\"]+)", re.IGNORECASE)),
    ("insert", re.compile(r"\binto\s+([A-Za-z0-9_\.\[\]`\"]+)", re.IGNORECASE)),
    ("update", re.compile(r"\bupdate\s+([A-Za-z0-9_\.\[\]`\"]+)", re.IGNORECASE)),
    ("delete", re.compile(r"\bfrom\s+([A-Za-z0-9_\.\[\]`\"]+)", re.IGNORECASE)),
    ("merge", re.compile(r"\binto\s+([A-Za-z0-9_\.\[\]`\"]+)", re.IGNORECASE)),
]


def _normalize_label(value: str, max_chars: int) -> str:
    if not value:
        return ""
    cleaned = " ".join(value.split())
    if len(cleaned) > max_chars:
        return cleaned[: max_chars - 3] + "..."
    return cleaned


def _normalize_table_name(value: str) -> str:
    if not value:
        return ""
    cleaned = value.strip()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        cleaned = cleaned[1:-1]
    if cleaned.startswith("`") and cleaned.endswith("`"):
        cleaned = cleaned[1:-1]
    if cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1]
    return cleaned


def _extract_table_name(sql_text: str) -> str:
    if not sql_text:
        return ""
    for _, pattern in _TABLE_PATTERNS:
        match = pattern.search(sql_text)
        if match:
            return _normalize_table_name(match.group(1))
    return ""


def _build_graph_nodes(
    symbols: list[dict],
    calls: list[dict],
    data_access: list[dict],
    max_label_chars: int,
    base_dir: Path | None,
) -> tuple[list[dict], dict[str, dict]]:
    nodes: dict[str, dict] = {}
    for row in symbols:
        node_id = row.get("symbol_id")
        if not node_id:
            continue
        label = row.get("name") or row.get("signature") or row.get("file_path", "")
        nodes[node_id] = {
            "node_id": node_id,
            "node_type": "symbol",
            "symbol_id": node_id,
            "table_name": None,
            "label": _normalize_label(str(label), max_label_chars),
            "source_ref": row.get("source_ref", row.get("file_path", "")),
        }
    for row in calls:
        caller_id = row.get("caller_id")
        if caller_id and caller_id not in nodes:
            label = f"{_display_path(row.get('file_path', ''), base_dir)}:{row.get('line', '')}"
            nodes[caller_id] = {
                "node_id": caller_id,
                "node_type": "callsite",
                "symbol_id": None,
                "table_name": None,
                "label": _normalize_label(label, max_label_chars),
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
        callee_id = row.get("callee_id")
        if callee_id and callee_id not in nodes:
            nodes[callee_id] = {
                "node_id": callee_id,
                "node_type": "callee",
                "symbol_id": None,
                "table_name": None,
                "label": _normalize_label(str(callee_id), max_label_chars),
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
    for row in data_access:
        sql_node_id = row.get("symbol_id")
        sql_text = row.get("sql_text", "")
        if sql_node_id and sql_node_id not in nodes:
            label = sql_text or f"{_display_path(row.get('file_path', ''), base_dir)}:{row.get('line', '')}"
            nodes[sql_node_id] = {
                "node_id": sql_node_id,
                "node_type": "sql_site",
                "symbol_id": sql_node_id,
                "table_name": None,
                "label": _normalize_label(str(label), max_label_chars),
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
        table_name = row.get("table_name") or _extract_table_name(str(sql_text))
        table_name = _normalize_table_name(str(table_name))
        if table_name:
            table_node_id = _hash_id(f"table:{table_name}")
            if table_node_id not in nodes:
                nodes[table_node_id] = {
                    "node_id": table_node_id,
                    "node_type": "table",
                    "symbol_id": None,
                    "table_name": table_name,
                    "label": _normalize_label(table_name, max_label_chars),
                    "source_ref": row.get("source_ref", row.get("file_path", "")),
                }
    return list(nodes.values()), nodes


def _build_graph_edges(calls: list[dict], data_access: list[dict]) -> list[dict]:
    edges: list[dict] = []
    for row in calls:
        caller_id = row.get("caller_id")
        callee_id = row.get("callee_id")
        if not caller_id or not callee_id:
            continue
        edges.append(
            {
                "from_id": caller_id,
                "to_id": callee_id,
                "edge_type": "call",
                "file_path": row.get("file_path", ""),
                "line": row.get("line", 0),
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
        )
    for row in data_access:
        from_id = row.get("symbol_id")
        if not from_id:
            continue
        table_name = row.get("table_name") or _extract_table_name(str(row.get("sql_text", "")))
        table_name = _normalize_table_name(str(table_name))
        if not table_name:
            continue
        to_id = _hash_id(f"table:{table_name}")
        edges.append(
            {
                "from_id": from_id,
                "to_id": to_id,
                "edge_type": "data_access",
                "file_path": row.get("file_path", ""),
                "line": row.get("line", 0),
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
        )
    return edges


def _build_entry_exit_map(
    calls: list[dict], 
    data_access: list[dict], 
    graph_edges: list[dict]
) -> list[dict]:
    """Build entry-exit map for all edges leading to exit nodes (out_degree=0)."""
    rows: list[dict] = []
    
    # Compute out-degree for all nodes
    out_degree: dict[str, int] = {}
    for edge in graph_edges:
        from_id = edge.get("from_id")
        if from_id:
            out_degree[from_id] = out_degree.get(from_id, 0) + 1
    
    # Add data_access edges to tables (exit nodes)
    for row in data_access:
        entry_id = row.get("symbol_id")
        if not entry_id:
            continue
        table_name = row.get("table_name") or _extract_table_name(str(row.get("sql_text", "")))
        table_name = _normalize_table_name(str(table_name))
        if not table_name:
            continue
        exit_id = _hash_id(f"table:{table_name}")
        rows.append(
            {
                "entry_node_id": entry_id,
                "exit_node_id": exit_id,
                "effect_type": row.get("op", ""),
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
        )
    
    # Add call edges to callees that are exit nodes (out_degree=0)
    for row in calls:
        caller_id = row.get("caller_id")
        callee_id = row.get("callee_id")
        if not caller_id or not callee_id:
            continue
        # Only include if callee is an exit node (no outgoing edges)
        if out_degree.get(callee_id, 0) == 0:
            rows.append(
                {
                    "entry_node_id": caller_id,
                    "exit_node_id": callee_id,
                    "effect_type": "call",
                    "source_ref": row.get("source_ref", row.get("file_path", "")),
                }
            )
    
    return rows


def _build_graph_metadata(
    nodes: list[dict],
    edges: list[dict],
) -> list[dict]:
    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(node["node_id"])
    for edge in edges:
        graph.add_edge(edge["from_id"], edge["to_id"])
    
    # Compute PageRank with appropriate settings based on graph size
    pagerank_map: dict[str, float] = {}
    num_nodes = graph.number_of_nodes()
    if num_nodes > 0:
        try:
            if num_nodes < 5000:
                # Small graphs: high precision
                pagerank_map = nx.pagerank(graph, max_iter=100, tol=1e-6)
            elif num_nodes < 50000:
                # Medium graphs: balanced precision/speed
                pagerank_map = nx.pagerank(graph, max_iter=50, tol=0.001)
            else:
                # Large graphs: fast approximation
                pagerank_map = nx.pagerank(graph, max_iter=20, tol=0.01)
            LOGGER.info(
                "graph_pagerank_computed nodes=%s iterations_max=%s",
                num_nodes,
                50 if num_nodes < 50000 else 20
            )
        except Exception as exc:
            LOGGER.warning("graph_pagerank_failed nodes=%s error=%s", num_nodes, exc)
            # PageRank failed, use degree centrality as fallback
            try:
                degree_cent = nx.degree_centrality(graph)
                pagerank_map = {k: v / num_nodes for k, v in degree_cent.items()}
                LOGGER.info("graph_pagerank_fallback_degree_centrality nodes=%s", num_nodes)
            except Exception:
                pass
    
    degree_map = dict(graph.degree())
    community_map: dict[str, int] = {}
    
    # Skip expensive community detection for large graphs (>10k nodes)
    if num_nodes > 0 and num_nodes < 10000:
        undirected = graph.to_undirected()
        if undirected.number_of_edges() == 0:
            for idx, node_id in enumerate(undirected.nodes(), start=1):
                community_map[node_id] = idx
        else:
            try:
                communities = list(nx.algorithms.community.greedy_modularity_communities(undirected))
                if not communities:
                    communities = [set(undirected.nodes())]
                for idx, community in enumerate(communities, start=1):
                    for node_id in community:
                        community_map[node_id] = idx
                LOGGER.info("graph_communities_detected count=%s", len(communities))
            except Exception as exc:
                LOGGER.warning("graph_community_detection_failed error=%s", exc)
                # Community detection failed, assign all to one community
                for node_id in undirected.nodes():
                    community_map[node_id] = 1
    else:
        # For large graphs, assign all nodes to community 1
        for node_id in graph.nodes():
            community_map[node_id] = 1
        LOGGER.info("graph_community_detection_skipped nodes=%s threshold=10000", num_nodes)
    
    rows: list[dict] = []
    for node in nodes:
        node_id = node["node_id"]
        rows.append(
            {
                "node_id": node_id,
                "degree": int(degree_map.get(node_id, 0)),
                "pagerank": float(pagerank_map.get(node_id, 0.0)),
                "community_id": int(community_map.get(node_id, 1)),
                "source_ref": node.get("source_ref", ""),
            }
        )
    return rows


def _read_parquet_rows(base_dir: Path, chunk_size: int | None = None) -> list[dict]:
    paths = glob.glob(str(base_dir / "**" / "*.parquet"), recursive=True)
    if not paths:
        return []
    if chunk_size is None or chunk_size <= 0:
        chunk_size = 200
    # Extract run_id from path if possible
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    run_id = None
    for part in base_dir.parts:
        if part.startswith("run_"):
            run_id = part
            break
    parquet_root = base_dir
    while parquet_root.name and not (parquet_root / "LATEST_RUN").exists():
        parquet_root = parquet_root.parent
    con, _ = get_run_connection(parquet_root, run_id)
    try:
        rows: list[dict] = []
        for start in range(0, len(paths), chunk_size):
            batch = paths[start : start + chunk_size]
            rows.extend(con.execute("select * from read_parquet($1)", [batch]).fetchdf().to_dict(orient="records"))
        return rows
    finally:
        con.close()


def _fetch_source_chunks(client, output_root: Path, run_id: str, artifact_version: int) -> list[dict]:
    if client:
        sql = f"""
            select file_path, line_start, line_end, content, source_ref
            from intake_source_chunks
            where run_id = '{run_id}' and artifact_version = {artifact_version}
            order by file_path, line_start
        """
        return client.query(sql)
    base_dir = output_root / run_id / "step_1" / "intake_source_chunks"
    rows = _read_parquet_rows(base_dir)
    if not rows:
        raise ValueError("intake_source_chunks not found locally")
    return rows


def _fetch_rows(
    client,
    output_root: Path,
    table: str,
    run_id: str,
    artifact_version: int,
    stage: str = "step_2",
) -> list[dict]:
    if client:
        sql = f"""
            select *
            from {table}
            where run_id = '{run_id}' and artifact_version = {artifact_version}
        """
        return client.query(sql)
    base_dir = output_root / run_id / stage / table
    return _read_parquet_rows(base_dir)


def _group_file_content(chunks: list[dict]) -> dict[str, str]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for row in chunks:
        grouped[row["file_path"]].append(row["content"])
    return {path: "\n".join(parts) for path, parts in grouped.items()}


def _sanitize_aspx(content: str) -> str:
    """
    Sanitize ASPX content by replacing server-side blocks with spaces
    to allow Tree-sitter HTML parser to process the rest of the file.
    Preserves line endings and rough conceptual layout.
    """
    # Simple regex to start. Replace content with spaces to keep offsets.
    # Note: This is not a full ASPX parser and might fail on complex nested cases.
    def replace_with_spaces(match):
        orig = match.group(0)
        return "".join(c if c in ('\r', '\n') else ' ' for c in orig)

    # Pattern for <% ... %> blocks including directives, cleanups, etc.
    # We use non-greedy matching.
    pattern = re.compile(r"<%--.*?--%>|<%.*?%>", re.DOTALL)
    return pattern.sub(replace_with_spaces, content)


def _parse_file(
    file_path: str,
    content: str,
    language_name: str,
    language_library_path: Path,
    queries_dir: Path,
) -> tuple[
    list[SymbolRow],
    list[CallRow],
    list[ConditionRow],
    list[ConstantRow],
    list[DataAccessRow],
    dict,
]:
    if language_name == "text":
        return [], [], [], [], [], _audit_row(file_path, language_name, "text", "skip")
        
    if language_name == "html" and file_path.lower().endswith((".aspx", ".ascx", ".master")):
        content = _sanitize_aspx(content)

    bundle = load_language(language_library_path, language_name)
    try:
        parser = build_parser(bundle)
        tree = parser.parse(bytes(content, "utf-8", errors="ignore"))
        source_ref = file_path
        symbols_query = load_query(queries_dir, language_name, "symbols")
        calls_query = load_query(queries_dir, language_name, "calls")
        conditions_query = load_query(queries_dir, language_name, "conditions")
        constants_query = load_query(queries_dir, language_name, "constants")
        data_access_query = load_query(queries_dir, language_name, "data_access")
        symbols = list(
            extract_symbols(bundle.language, tree, symbols_query, file_path, source_ref)
        )
        calls = list(extract_calls(bundle.language, tree, calls_query, file_path))
        conditions = list(extract_conditions(bundle.language, tree, conditions_query, file_path))
        constants = list(extract_constants(bundle.language, tree, constants_query, file_path))
        data_access = list(
            extract_data_access(bundle.language, tree, data_access_query, file_path)
        )
        return (
            symbols,
            calls,
            conditions,
            constants,
            data_access,
            _audit_row(
                file_path,
                language_name,
                "tree_sitter",
                "ok",
                reason="",
            ),
        )
    except RuntimeError as exc:
        LOGGER.warning(
            "tree_sitter_parse_failed file=%s lang=%s error=%s",
            file_path,
            language_name,
            exc,
        )
        return (
            [],
            [],
            [],
            [],
            [],
            _audit_row(
                file_path,
                language_name,
                "tree_sitter",
                "error",
                reason=str(exc),
            ),
        )
    except OSError as exc:
        LOGGER.warning("tree_sitter_io_failed file=%s lang=%s error=%s", file_path, language_name, exc)
        return (
            [],
            [],
            [],
            [],
            [],
            _audit_row(
                file_path,
                language_name,
                "tree_sitter",
                "error",
                reason=f"io:{exc}",
            ),
        )


def _parse_item_worker(
    item: tuple[str, str, str],
    language_library_path: Path,
    queries_dir: Path,
):
    file_path, content, language_name = item
    return _parse_file(
        file_path,
        content,
        language_name,
        language_library_path,
        queries_dir,
    )


def run(
    config: ParserConfig,
    run_llm: bool = False,
    retry_paths: set[str] | None = None,
    retry_only: bool = False,
) -> None:
    start_time = time.monotonic()
    created_at = _created_at()
    workers = _resolve_workers(config)
    config.output_root.mkdir(parents=True, exist_ok=True)
    _ensure_language_library(config)
    _ensure_query_coverage(config)
    if config.run_id == "auto":
        try:
            run_id = resolve_run_id(config.output_root)
        except RuntimeError as exc:
            if config.auto_ingest_if_missing and config.ingestion_config_path:
                LOGGER.info(
                    "parser_missing_run auto_ingest=1 reason=%s",
                    str(exc),
                )
                ingestion_config = load_ingestion_config(config.ingestion_config_path)
                run_ingestion(ingestion_config)
                run_id = resolve_run_id(config.output_root)
            else:
                raise
    else:
        run_id = config.run_id
    config = config.model_copy(update={"run_id": run_id})
    state = start_state("parser", config.run_id, config.artifact_version)
    output_root = config.output_root / config.run_id / "step_2"
    output_root.mkdir(parents=True, exist_ok=True)
    try:
        client = get_mcp_client()
    except RuntimeError:
        LOGGER.info("parser_mcp_client_missing_using_local_parquet=1")
        client = None
    try:
        chunks = _fetch_source_chunks(client, config.output_root, config.run_id, config.artifact_version)
    except ValueError as exc:
        if (
            config.auto_ingest_if_missing
            and "intake_source_chunks" in str(exc)
            and config.ingestion_config_path
        ):
            LOGGER.info(
                "parser_missing_source_chunks auto_ingest=1 config=%s",
                config.ingestion_config_path,
            )
            ingestion_config = load_ingestion_config(config.ingestion_config_path)
            run_ingestion(ingestion_config)
            chunks = _fetch_source_chunks(client, config.output_root, config.run_id, config.artifact_version)
        else:
            raise
    files = _group_file_content(chunks)
    LOGGER.info(
        "parser_start run_id=%s workers=%s files=%s", config.run_id, workers, len(files)
    )

    # Roslyn-first pass over all solutions to build call/symbol tree centrally.
    roslyn_symbols: list[SymbolRow] = []
    roslyn_calls: list[CallRow] = []
    roslyn_conditions: list[ConditionRow] = []
    roslyn_constants: list[ConstantRow] = []
    roslyn_data_access: list[DataAccessRow] = []
    roslyn_processed_files: set[str] = set()
    roslyn_audit: list[dict] = []
    sln_paths = [p for p in files.keys() if p.lower().endswith(".sln")]
    roslyn_loaded = False
    if config.roslyn_parquet_root:
        try:
            roslyn_result = load_roslyn_parquet(
                config.roslyn_parquet_root,
                config.roslyn_parquet_run_id,
            )
            roslyn_symbols = _symbols_from_roslyn(roslyn_result, str(config.roslyn_parquet_root))
            roslyn_calls = _calls_from_roslyn(roslyn_result, str(config.roslyn_parquet_root))
            roslyn_conditions = _conditions_from_roslyn(roslyn_result, str(config.roslyn_parquet_root))
            roslyn_constants = _constants_from_roslyn(roslyn_result, str(config.roslyn_parquet_root))
            roslyn_data_access = _data_access_from_roslyn(roslyn_result, str(config.roslyn_parquet_root))
            for row in roslyn_symbols:
                if row.file_path:
                    roslyn_processed_files.add(row.file_path)
            roslyn_audit.append(
                _audit_row(
                    str(config.roslyn_parquet_root),
                    "roslyn_solution",
                    "roslyn_parquet",
                    "ok",
                )
            )
            roslyn_loaded = True
            LOGGER.info(
                "roslyn_parquet_loaded root=%s run_id=%s symbols=%s calls=%s data_access=%s",
                config.roslyn_parquet_root,
                config.roslyn_parquet_run_id or "LATEST_RUN",
                len(roslyn_symbols),
                len(roslyn_calls),
                len(roslyn_data_access),
            )
        except Exception as exc:
            roslyn_audit.append(
                _audit_row(
                    str(config.roslyn_parquet_root),
                    "roslyn_solution",
                    "roslyn_parquet",
                    "error",
                    reason=str(exc),
                )
            )
            LOGGER.warning(
                "roslyn_parquet_failed root=%s run_id=%s error=%s",
                config.roslyn_parquet_root,
                config.roslyn_parquet_run_id or "LATEST_RUN",
                exc,
            )
    if not roslyn_loaded and config.roslyn_cmd and sln_paths:
        for sln in sln_paths:
            try:
                result = _parse_roslyn(Path(sln), config.roslyn_cmd, config.roslyn_timeout_sec)
                sym_rows = _symbols_from_roslyn(result, sln)
                call_rows = _calls_from_roslyn(result, sln)
                cond_rows = _conditions_from_roslyn(result, sln)
                const_rows = _constants_from_roslyn(result, sln)
                da_rows = _data_access_from_roslyn(result, sln)
                roslyn_symbols.extend(sym_rows)
                roslyn_calls.extend(call_rows)
                roslyn_conditions.extend(cond_rows)
                roslyn_constants.extend(const_rows)
                roslyn_data_access.extend(da_rows)
                for row in sym_rows:
                    if row.file_path:
                        roslyn_processed_files.add(row.file_path)
                roslyn_audit.append(_audit_row(sln, "roslyn_solution", "roslyn", "ok"))
                LOGGER.info(
                    "roslyn_solution parsed sln=%s symbols=%s calls=%s data_access=%s",
                    sln,
                    len(sym_rows),
                    len(call_rows),
                    len(da_rows),
                )
            except Exception as exc:
                roslyn_audit.append(
                    _audit_row(sln, "roslyn_solution", "roslyn", "error", reason=str(exc))
                )
                LOGGER.warning("roslyn_solution_failed sln=%s error=%s", sln, exc)

    work_items: list[tuple[str, str, str]] = []
    extensionless_detected = 0
    for file_path, content in files.items():
        ext = Path(file_path).suffix.lower()
        language_name = config.language_map.get(ext)
        if not language_name:
            # Try content-based detection for extensionless mainframe files
            if not ext:
                language_name = detect_mainframe_language(content)
                if language_name:
                    extensionless_detected += 1
            if not language_name:
                continue
        if file_path in roslyn_processed_files and language_name in set(config.roslyn_languages):
            # Already handled via solution-level Roslyn pass.
            continue
        work_items.append((file_path, content, language_name))
    if extensionless_detected > 0:
        LOGGER.info("extensionless_mainframe_detected count=%s", extensionless_detected)
    if retry_paths:
        if retry_only:
            work_items = [item for item in work_items if item[0] in retry_paths]
        else:
            missing = retry_paths - {item[0] for item in work_items}
            if missing:
                LOGGER.warning("retry_paths_not_found count=%s", len(missing))
        LOGGER.info(
            "parser_work_items total=%s retry_paths=%s retry_only=%s",
            len(work_items),
            len(retry_paths),
            retry_only,
        )
    else:
        LOGGER.info("parser_work_items total=%s", len(work_items))

    symbol_rows: list[SymbolRow] = list(roslyn_symbols)
    call_rows: list[CallRow] = list(roslyn_calls)
    condition_rows: list[ConditionRow] = list(roslyn_conditions)
    constant_rows: list[ConstantRow] = list(roslyn_constants)
    data_access_rows: list[DataAccessRow] = list(roslyn_data_access)
    audit_rows: list[dict] = list(roslyn_audit)
    missed_rows: list[dict] = []
    if workers > 1 and work_items:
        parse_item = partial(
            _parse_item_worker,
            language_library_path=config.language_library_path,
            queries_dir=config.queries_dir,
        )
        # Optimize chunksize for better load distribution
        chunksize = max(1, len(work_items) // (workers * 2))
        results = process_map(parse_item, work_items, workers, chunksize=chunksize)
        for idx, result in enumerate(results, start=1):
            (
                symbols,
                calls,
                conditions,
                constants,
                data_access,
                audit,
            ) = result
            symbol_rows.extend(symbols)
            call_rows.extend(calls)
            condition_rows.extend(conditions)
            constant_rows.extend(constants)
            data_access_rows.extend(data_access)
            audit_rows.append(audit)
            if audit.get("status") != "ok":
                missed_rows.append(audit)
            if idx % 100 == 0 or idx == len(results):
                LOGGER.info("parser_progress parsed=%s/%s", idx, len(results))
    else:
        for idx, (file_path, content, language_name) in enumerate(work_items, start=1):
            (
                symbols,
                calls,
                conditions,
                constants,
                data_access,
                audit,
            ) = _parse_file(
                file_path,
                content,
                language_name,
                config.language_library_path,
                config.queries_dir,
            )
            symbol_rows.extend(symbols)
            call_rows.extend(calls)
            condition_rows.extend(conditions)
            constant_rows.extend(constants)
            data_access_rows.extend(data_access)
            audit_rows.append(audit)
            if audit.get("status") != "ok":
                missed_rows.append(audit)
            if idx % 100 == 0 or idx == len(work_items):
                LOGGER.info("parser_progress parsed=%s/%s", idx, len(work_items))

    rows = [
        {
            "symbol_id": row.symbol_id,
            "name": row.name,
            "kind": row.kind,
            "signature": row.signature,
            "file_path": row.file_path,
            "line": row.line,
            "source_ref": row.source_ref,
        }
        for row in symbol_rows
    ]

    LOGGER.info("parser_symbol_rows=%s", len(rows))
    write_parquet(
        output_root,
        "symbols",
        _with_metadata(rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write symbols=done")

    # Build symbol lookup for call resolution
    symbol_lookup: dict[str, str] = {}
    for row in rows:
        # Index by name and by qualified name (class.method pattern)
        symbol_lookup[row["name"]] = row["symbol_id"]
        # Also try to build qualified lookups from file context
        file_base = Path(row["file_path"]).stem
        symbol_lookup[f"{file_base}.{row['name']}"] = row["symbol_id"]

    # Build semantic context for enhanced call resolution
    file_contexts: list[FileContext] = []
    semantic_languages = {
        # Modern languages
        "c_sharp", "vbnet", "python", "java", "typescript", "javascript",
        "php", "perl",
        # Database
        "sql",
        # Mainframe
        "cobol", "jcl", "cics", "bms", "easytrieve",
        # Markup/Config
        "css", "html", "xml",
    }
    for file_path, content, lang in work_items:
        if lang in semantic_languages:
            try:
                bundle = load_language(config.language_library_path, lang)
                parser = build_parser(bundle)
                tree = parser.parse(bytes(content, "utf-8", errors="ignore"))
                file_ctx = extract_file_context(bundle.language, tree, file_path, lang)
                file_contexts.append(file_ctx)
            except Exception as exc:
                LOGGER.debug("semantic_context_failed file=%s error=%s", file_path, exc)
    
    global_semantic_ctx = build_semantic_context(file_contexts)
    LOGGER.info(
        "semantic_context_built files=%d classes=%d fields=%d",
        len(file_contexts),
        len(global_semantic_ctx.symbol_table),
        sum(len(fc.fields) for fc in file_contexts),
    )

    # Resolve calls using semantic context where available
    resolved_count = 0
    call_dicts = []
    for row in call_rows:
        call_dict = {
            "caller_id": row.caller_id,
            "callee_id": row.callee_id,  # Start with original
            "file_path": row.file_path,
            "line": row.line,
            "source_ref": row.source_ref,
            "receiver": getattr(row, "receiver", ""),
            "callee_name": getattr(row, "callee_name", ""),
        }
        
        # Try semantic resolution first
        file_ctx = global_semantic_ctx.files.get(row.file_path)
        if file_ctx:
            from .semantic_resolver import resolve_call_type
            receiver = getattr(row, "receiver", "")
            callee_name = getattr(row, "callee_name", "")
            if receiver and callee_name:
                resolved_id = resolve_call_type(
                    receiver, callee_name, file_ctx, global_semantic_ctx
                )
                if resolved_id:
                    call_dict["callee_id"] = resolved_id
                    call_dict["resolved"] = True
                    resolved_count += 1
                    call_dicts.append(call_dict)
                    continue
        
        # Fallback to symbol lookup resolution
        call_dict["callee_id"] = _resolve_callee_id(row, symbol_lookup)
        call_dicts.append(call_dict)
    
    LOGGER.info(
        "call_resolution_complete total=%d semantic_resolved=%d",
        len(call_dicts),
        resolved_count,
    )
    LOGGER.info("parser_call_rows=%s", len(call_dicts))
    write_parquet(
        output_root,
        "calls",
        _with_metadata(call_dicts, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write calls=done")

    condition_dicts = [
        {
            "symbol_id": row.symbol_id,
            "predicate": row.predicate,
            "file_path": row.file_path,
            "line": row.line,
            "source_ref": row.source_ref,
        }
        for row in condition_rows
    ]
    LOGGER.info("parser_condition_rows=%s", len(condition_dicts))
    write_parquet(
        output_root,
        "conditions",
        _with_metadata(condition_dicts, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write conditions=done")

    constant_dicts = [
        {
            "name": row.name,
            "value": row.value,
            "file_path": row.file_path,
            "line": row.line,
            "source_ref": row.source_ref,
        }
        for row in constant_rows
    ]
    LOGGER.info("parser_constant_rows=%s", len(constant_dicts))
    write_parquet(
        output_root,
        "constants",
        _with_metadata(constant_dicts, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write constants=done")

    data_access_dicts = [
        {
            "symbol_id": row.symbol_id,
            "table_name": row.table_name,
            "op": row.op,
            "sql_text": row.sql_text,
            "file_path": row.file_path,
            "line": row.line,
            "source_ref": row.source_ref,
        }
        for row in data_access_rows
    ]
    LOGGER.info("parser_data_access_rows=%s", len(data_access_dicts))
    write_parquet(
        output_root,
        "data_access",
        _with_metadata(data_access_dicts, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write data_access=done")

    base_dir = None
    if files:
        try:
            base_dir = Path(os.path.commonpath(list(files.keys())))
        except Exception as exc:  # noqa: BLE001
            LOGGER.warning("parser_base_dir_failed error=%s", exc)
            base_dir = None
    if base_dir:
        LOGGER.info("parser_base_dir=%s", base_dir)
    graph_nodes, _ = _build_graph_nodes(
        rows,
        call_dicts,
        data_access_dicts,
        config.max_label_chars,
        base_dir,
    )
    graph_edges = _build_graph_edges(call_dicts, data_access_dicts)
    entry_exit_rows = _build_entry_exit_map(call_dicts, data_access_dicts, graph_edges)
    graph_meta_rows = _build_graph_metadata(
        graph_nodes,
        graph_edges,
    )
    LOGGER.info(
        "parser_graph built nodes=%s edges=%s",
        len(graph_nodes),
        len(graph_edges),
    )
    
    # Skip expensive entry graph computation if top_k is very small or graph is huge
    skip_entry_graph = (
        config.entry_graph_top_k is not None 
        and config.entry_graph_top_k <= 10
        or len(graph_nodes) > 200000
    )
    
    if skip_entry_graph:
        LOGGER.info(
            "parser_skip_entry_graph top_k=%s nodes=%s reason=%s",
            config.entry_graph_top_k,
            len(graph_nodes),
            "top_k_too_small" if config.entry_graph_top_k and config.entry_graph_top_k <= 10 else "graph_too_large"
        )
        entry_graph_candidates = []
        entry_graph_summary = {
            "exit_nodes": set(),
            "excluded": [],
            "eligible": [],
            "entry_candidates": [],
            "entry_groups": [],
            "edges": [],
        }
    else:
        LOGGER.info(
            "parser_entry_graph_start nodes=%s edges=%s top_k=%s threshold=%s",
            len(graph_nodes), len(graph_edges), config.entry_graph_top_k, config.entry_graph_depth_threshold
        )
        entry_graph_candidates, entry_graph_summary = _entry_graph_candidates(
            graph_nodes,
            graph_edges,
            config.entry_graph_max_depth,
            config.entry_graph_node_limit,
            config.entry_graph_depth_threshold,
            config.entry_graph_top_k,
        )
        LOGGER.info(
            "parser_entry_graph_done candidates=%s eligible=%s excluded=%s",
            len(entry_graph_candidates),
            len(entry_graph_summary.get("eligible", [])),
            len(entry_graph_summary.get("excluded", []))
        )
    graph_label_map = _graph_label_map(rows, graph_nodes)
    entry_nodes, entry_group_nodes, exit_nodes = _graph_label_sets(
        entry_graph_summary.get("entry_candidates", []),
        entry_graph_summary.get("entry_groups", []),
        entry_graph_summary.get("exit_nodes", set()),
    )
    existing_entry_state = _entry_graph_state_map(
        client,
        config.output_root,
        config.run_id,
        config.artifact_version,
        config.entry_graph_incremental,
    )
    processed_existing: set[str] = set(
        key for key, value in existing_entry_state.items() if value.get("status") == "processed"
    )
    entry_graph_rows: list[dict] = []
    entry_state_rows: list[dict] = []
    processed_keys: list[str] = []
    skipped_keys: list[str] = []
    pending_keys: list[str] = []
    excluded_keys: list[str] = []
    selected_keys = {item["entry_key"] for item in entry_graph_candidates}
    for item in entry_graph_summary.get("eligible", []):
        entry_key = str(item["entry_key"])
        if entry_key not in selected_keys:
            pending_keys.append(entry_key)
            entry_state_rows.append(
                {
                    "entry_key": entry_key,
                    "entry_type": item["entry_type"],
                    "status": "pending",
                    "reason": "top_k_limit",
                    "metrics": json.dumps(item.get("metrics", {}), ensure_ascii=True),
                    "source_ref": entry_key,
                }
            )
    for item in entry_graph_summary.get("excluded", []):
        entry_key = str(item["entry_key"])
        excluded_keys.append(entry_key)
        entry_state_rows.append(
            {
                "entry_key": entry_key,
                "entry_type": item["entry_type"],
                "status": "excluded",
                "reason": item.get("reason", "excluded"),
                "metrics": json.dumps(item.get("metrics", {}), ensure_ascii=True),
                "source_ref": entry_key,
            }
        )
    edges_summary = entry_graph_summary.get("edges", [])
    workers = _resolve_workers(config)
    LOGGER.info(
        "entry_graph_process start candidates=%s workers=%s", len(entry_graph_candidates), workers
    )
    worker_inputs = [
        (item, edges_summary, processed_existing, config.entry_graph_incremental)
        for item in entry_graph_candidates
    ]
    # Optimize chunksize for entry graph processing
    chunksize = max(1, len(worker_inputs) // (workers * 2)) if worker_inputs else 1
    results = process_map(_entry_graph_worker, worker_inputs, workers, chunksize=chunksize)
    for idx, result in enumerate(results, start=1):
        entry_row, state_row, status, entry_key = result
        if entry_row:
            entry_graph_rows.append(entry_row)
        entry_state_rows.append(state_row)
        if status == "processed" and entry_key:
            processed_keys.append(str(entry_key))
        elif status == "skipped" and entry_key:
            skipped_keys.append(str(entry_key))
        if idx % 1000 == 0 or idx == len(results):
            LOGGER.info(
                "entry_graph_progress processed=%s/%s last=%s status=%s",
                idx,
                len(results),
                entry_key,
                status,
            )
    summary_row = {
        "total_candidates": len(entry_graph_summary.get("eligible", [])),
        "processed_count": len(processed_keys),
        "skipped_count": len(skipped_keys),
        "pending_count": len(pending_keys),
        "excluded_count": len(excluded_keys),
        "processed_keys": json.dumps(processed_keys[:100], ensure_ascii=True),
        "pending_keys": json.dumps(pending_keys[:100], ensure_ascii=True),
        "skipped_keys": json.dumps(skipped_keys[:100], ensure_ascii=True),
        "excluded_keys": json.dumps(excluded_keys[:100], ensure_ascii=True),
        "source_ref": "entry_graph_processing_summary",
    }
    write_parquet(
        output_root,
        "code_graph_nodes",
        _with_metadata(graph_nodes, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "code_graph_edges",
        _with_metadata(graph_edges, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "entry_exit_map",
        _with_metadata(entry_exit_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "graph_metadata",
        _with_metadata(graph_meta_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    if config.entry_graph_render_dot or config.entry_graph_render_png or config.entry_graph_render_svg:
        render_root = config.entry_graph_render_dir / config.run_id / "step_2"
        full_dir = render_root / "full"
        entries_dir = render_root / "entries"
        if render_root.exists() and not config.entry_graph_incremental:
            shutil.rmtree(render_root)
        full_dir.mkdir(parents=True, exist_ok=True)
        entries_dir.mkdir(parents=True, exist_ok=True)
        if config.entry_graph_render_full:
            full_title = (
                f"entries={len(entry_nodes)} entry_groups={len(entry_graph_summary.get('entry_groups', []))} "
                f"exits={len(exit_nodes)}"
            )
            full_dot = _format_graph_dot(
                graph_nodes,
                graph_edges,
                entry_nodes,
                entry_group_nodes,
                exit_nodes,
                full_title,
                graph_label_map,
            )
            full_dot_path = full_dir / "code_graph.dot"
            if config.entry_graph_render_dot:
                _write_if_changed(full_dot_path, full_dot, config.entry_graph_incremental)
            if config.entry_graph_render_png:
                _render_graph(
                    full_dot_path,
                    full_dir / "code_graph.png",
                    config.entry_graph_incremental,
                    config.entry_graph_render_engine,
                    "png",
                )
            if config.entry_graph_render_svg:
                _render_graph(
                    full_dot_path,
                    full_dir / "code_graph.svg",
                    config.entry_graph_incremental,
                    config.entry_graph_render_engine,
                    "svg",
                )
        for idx, item in enumerate(entry_graph_candidates, start=1):
            entry_key = str(item["entry_key"])
            entry_type = str(item["entry_type"])
            entry_nodes_set = set(item.get("entry_nodes", []))
            reachable = item.get("reachable", set())
            capped_depth = int(item.get("metrics", {}).get("capped_depth", 0))
            entry_edges = _entry_graph_edges(
                entry_graph_summary.get("edges", []),
                reachable,
                entry_nodes_set,
                entry_type,
            )
            raw_label = graph_label_map.get(entry_key, entry_key)
            base_name = _entry_graph_basename(raw_label, entry_key, entry_type, idx)
            
            if config.entry_graph_render_by_depth and capped_depth > 0:
                # Build adjacency for this entry's subgraph
                adjacency: dict[str, list[str]] = defaultdict(list)
                for src, tgt in entry_edges:
                    adjacency[src].append(tgt)
                
                # Compute nodes at each depth level
                nodes_by_depth = _compute_nodes_by_depth(adjacency, entry_key, capped_depth + 1)
                
                # Find exit nodes in graph
                exit_nodes_in_graph = exit_nodes & reachable
                
                # Generate a separate .dot file for each cumulative depth
                for target_depth in range(1, capped_depth + 1):
                    # Cumulative: all nodes from depth 0 to target_depth
                    cumulative_nodes: set[str] = set()
                    for d in range(target_depth + 1):
                        cumulative_nodes |= nodes_by_depth.get(d, set())
                    
                    if len(cumulative_nodes) <= 1:  # Only entry node
                        continue
                    
                    # Find exits in this cumulative set
                    exits_in_scope = cumulative_nodes & exit_nodes_in_graph
                    
                    # Filter edges to only those within cumulative nodes
                    scoped_edges = [(s, t) for s, t in entry_edges if s in cumulative_nodes and t in cumulative_nodes]
                    
                    depth_title = f"entry={entry_key[:16]} up_to_depth={target_depth}/{capped_depth} nodes={len(cumulative_nodes)}"
                    depth_dot = _format_cumulative_depth_dot(
                        [node for node in graph_nodes if node.get("node_id") in cumulative_nodes],
                        scoped_edges,
                        entry_key,
                        exit_nodes_in_graph,
                        target_depth,
                        depth_title,
                        graph_label_map,
                        nodes_by_depth,
                    )
                    
                    depth_dir = entries_dir / f"depth_{capped_depth}"
                    depth_dir.mkdir(parents=True, exist_ok=True)
                    depth_dot_path = depth_dir / f"{base_name}_d{target_depth}.dot"
                    
                    if config.entry_graph_render_dot:
                        _write_if_changed(depth_dot_path, depth_dot, config.entry_graph_incremental)
                    if config.entry_graph_render_png:
                        _render_graph(
                            depth_dot_path,
                            depth_dir / f"{base_name}.png",
                            config.entry_graph_incremental,
                            config.entry_graph_render_engine,
                            "png",
                        )
                    if config.entry_graph_render_svg:
                        _render_graph(
                            depth_dot_path,
                            depth_dir / f"{base_name}.svg",
                            config.entry_graph_incremental,
                            config.entry_graph_render_engine,
                            "svg",
                        )
            else:
                # Original behavior: single graph per entry
                entry_title = f"{entry_type}={entry_key} depth={capped_depth}"
                entry_dot = _format_graph_dot(
                    [node for node in graph_nodes if node.get("node_id") in reachable],
                    [{"from_id": e[0], "to_id": e[1]} for e in entry_edges],
                    entry_nodes_set,
                    entry_nodes_set if entry_type == "entry_group" else set(),
                    exit_nodes & reachable,
                    entry_title,
                    graph_label_map,
                )
                output_dir = entries_dir
                entry_dot_path = output_dir / f"{base_name}.dot"
                if config.entry_graph_render_dot:
                    _write_if_changed(entry_dot_path, entry_dot, config.entry_graph_incremental)
                if config.entry_graph_render_png:
                    _render_graph(
                        entry_dot_path,
                        output_dir / f"{base_name}.png",
                        config.entry_graph_incremental,
                        config.entry_graph_render_engine,
                        "png",
                    )
                if config.entry_graph_render_svg:
                    _render_graph(
                        entry_dot_path,
                        output_dir / f"{base_name}.svg",
                        config.entry_graph_incremental,
                        config.entry_graph_render_engine,
                        "svg",
                    )
    write_parquet(
        output_root,
        "entry_graphs",
        _with_metadata(entry_graph_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write entry_graphs=done")
    write_parquet(
        output_root,
        "entry_graph_state",
        _with_metadata(entry_state_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write entry_graph_state=done")
    write_parquet(
        output_root,
        "entry_graph_processing_summary",
        _with_metadata([summary_row], config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    LOGGER.info("parser_write entry_graph_processing_summary=done")
    if run_llm:
        symbol_exts = _symbol_ext_map(rows)
        entry_graph_summaries, entry_graph_debug = _build_entry_graph_summaries(
            entry_graph_candidates,
            exit_nodes,
            graph_label_map,
            symbol_exts,
            graph_nodes,
            symbol_rows,
            config,
        )
        write_parquet(
            output_root,
            "entry_graph_summaries",
            _with_metadata(entry_graph_summaries, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
        LOGGER.info("parser_write entry_graph_summaries=done")
        if config.entry_graph_llm_merge_enabled:
            merged_rows = _merge_entry_graph_summaries(entry_graph_summaries, config)
            write_parquet(
                output_root,
                "entry_graph_summaries_merged",
                _with_metadata(merged_rows, config, created_at),
                partition_cols=["run_id", "artifact_version"],
            )
            LOGGER.info("parser_write entry_graph_summaries_merged=done")
        if config.entry_graph_llm_debug and entry_graph_debug:
            write_parquet(
                output_root,
                "entry_graph_llm_debug",
                _with_metadata(entry_graph_debug, config, created_at),
                partition_cols=["run_id", "artifact_version"],
            )
            LOGGER.info("parser_write entry_graph_llm_debug=done")

    LOGGER.info("parser_audit_rows=%s", len(audit_rows))
    write_parquet(
        output_root,
        "parse_audit",
        _with_metadata(audit_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    if missed_rows:
        write_parquet(
            output_root,
            "parse_missed",
            _with_metadata(missed_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
        LOGGER.info("parser_write parse_missed=%s", len(missed_rows))
    _log_audit_summary(audit_rows)
    
    # Generate and log coverage summary
    from migration_agents.coverage.summary import generate_parser_coverage, get_coverage_report
    if generate_parser_coverage(config.output_root):
        LOGGER.info("parser_coverage_summary_written=1")
    
    # Log deterministic summary
    LOGGER.info("=" * 60)
    LOGGER.info("PARSER SUMMARY")
    LOGGER.info("=" * 60)
    LOGGER.info("parser_files_total=%d", len(files))
    LOGGER.info("parser_files_parsed=%d", len([r for r in audit_rows if r.get("status") == "ok"]))
    LOGGER.info("parser_files_skipped=%d", len([r for r in audit_rows if r.get("status") == "skip"]))
    LOGGER.info("parser_files_failed=%d", len([r for r in audit_rows if r.get("status") not in ("ok", "skip")]))
    LOGGER.info("parser_symbols=%d", len(symbol_rows))
    LOGGER.info("parser_calls=%d", len(call_rows))
    LOGGER.info("parser_conditions=%d", len(condition_rows))
    LOGGER.info("parser_constants=%d", len(constant_rows))
    LOGGER.info("parser_data_access=%d", len(data_access_rows))
    LOGGER.info("parser_graph_nodes=%d", len(graph_nodes))
    LOGGER.info("parser_graph_edges=%d", len(graph_edges))
    LOGGER.info("parser_entry_graphs=%d", len(entry_graph_rows))
    LOGGER.info("=" * 60)
    
    outputs = {
        "symbols": len(symbol_rows),
        "calls": len(call_rows),
        "conditions": len(condition_rows),
        "constants": len(constant_rows),
        "data_access": len(data_access_rows),
        "code_graph_nodes": len(graph_nodes),
        "code_graph_edges": len(graph_edges),
        "entry_graphs": len(entry_graph_rows),
        "parse_audit": len(audit_rows),
    }
    notes = {
        "files_total": len(files),
        "work_items": len(work_items),
        "entry_graph_candidates": len(entry_graph_candidates),
        "entry_graph_processed": summary_row.get("processed_count"),
        "entry_graph_skipped": summary_row.get("skipped_count"),
        "entry_graph_pending": summary_row.get("pending_count"),
    }
    state = finalize_state(
        state,
        processed_count=len(work_items),
        skipped_count=max(0, len(files) - len(work_items)),
        outputs=outputs,
        notes=notes,
    )
    write_state("parser", state)
    LOGGER.info("parser_complete elapsed_sec=%.2f", time.monotonic() - start_time)


def _resolve_callee_id(row: CallRow, symbol_lookup: dict[str, str]) -> str:
    """Attempt to resolve callee_id to an actual symbol definition.
    
    Resolution order:
    1. Qualified name (Receiver.Method) if receiver looks like a type
    2. Method name only match
    3. Fallback to original hash-based ID
    """
    callee_name = getattr(row, "callee_name", "")
    receiver = getattr(row, "receiver", "")
    
    # Try qualified lookup first (static calls, known types)
    if receiver and receiver[0].isupper():
        qualified = f"{receiver}.{callee_name}"
        if qualified in symbol_lookup:
            return symbol_lookup[qualified]
    
    # Try direct name match
    if callee_name in symbol_lookup:
        return symbol_lookup[callee_name]
    
    # Fallback to original callee_id
    return row.callee_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Tree-sitter parser stage.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--run-llm",
        action="store_true",
        help="Also run the LLM summarization path after graph build.",
    )
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("parser")
    config = load_config(args.config)
    run(config, run_llm=bool(args.run_llm))


def _parse_roslyn(
    file_path: Path, roslyn_cmd: list[str], roslyn_timeout_sec: int
) -> RoslynResult:
    return run_roslyn(roslyn_cmd, file_path, roslyn_timeout_sec)


def _symbols_from_roslyn(result: RoslynResult, file_path: str) -> list[SymbolRow]:
    rows: list[SymbolRow] = []
    for row in result.symbols:
        symbol_id = row.get("symbol_id") or row.get("SymbolId", "")
        name = row.get("name") or row.get("Name", "")
        kind = row.get("kind") or row.get("Kind", "")
        signature = row.get("signature") or row.get("Signature", "")
        line = row.get("line") or row.get("Line", 0)
        fp = row.get("file_path") or row.get("FilePath", file_path)
        source_ref = row.get("source_ref") or row.get("SourceRef", fp or file_path)
        rows.append(
            SymbolRow(
                symbol_id=str(symbol_id),
                name=str(name),
                kind=str(kind),
                signature=str(signature),
                file_path=str(fp or file_path),
                line=int(line or 0),
                source_ref=str(source_ref),
            )
        )
    return rows


def _calls_from_roslyn(result: RoslynResult, file_path: str) -> list[CallRow]:
    rows: list[CallRow] = []
    for row in result.calls:
        caller_id = row.get("caller_id") or row.get("CallerId", "")
        callee_id = row.get("callee_id") or row.get("CalleeId", "")
        line = row.get("line") or row.get("Line", 0)
        fp = row.get("file_path") or row.get("FilePath", file_path)
        source_ref = row.get("source_ref") or row.get("SourceRef", fp or file_path)
        receiver = row.get("receiver") or row.get("Receiver", "")
        callee_name = row.get("callee_name") or row.get("CalleeName", "")
        rows.append(
            CallRow(
                caller_id=str(caller_id),
                callee_id=str(callee_id),
                file_path=str(fp or file_path),
                line=int(line or 0),
                source_ref=str(source_ref),
                receiver=str(receiver),
                callee_name=str(callee_name),
            )
        )
    return rows


def _conditions_from_roslyn(result: RoslynResult, file_path: str) -> list[ConditionRow]:
    rows: list[ConditionRow] = []
    for row in result.conditions:
        symbol_id = row.get("symbol_id") or row.get("SymbolId", "")
        predicate = row.get("predicate") or row.get("Predicate", "")
        line = row.get("line") or row.get("Line", 0)
        fp = row.get("file_path") or row.get("FilePath", file_path)
        source_ref = row.get("source_ref") or row.get("SourceRef", fp or file_path)
        rows.append(
            ConditionRow(
                symbol_id=str(symbol_id),
                predicate=str(predicate),
                file_path=str(fp or file_path),
                line=int(line or 0),
                source_ref=str(source_ref),
            )
        )
    return rows


def _constants_from_roslyn(result: RoslynResult, file_path: str) -> list[ConstantRow]:
    rows: list[ConstantRow] = []
    for row in result.constants:
        name = row.get("name") or row.get("Name", "")
        value = row.get("value") or row.get("Value", "")
        line = row.get("line") or row.get("Line", 0)
        fp = row.get("file_path") or row.get("FilePath", file_path)
        source_ref = row.get("source_ref") or row.get("SourceRef", fp or file_path)
        rows.append(
            ConstantRow(
                name=str(name),
                value=str(value),
                file_path=str(fp or file_path),
                line=int(line or 0),
                source_ref=str(source_ref),
            )
        )
    return rows


def _data_access_from_roslyn(result: RoslynResult, file_path: str) -> list[DataAccessRow]:
    rows: list[DataAccessRow] = []
    for row in result.data_access:
        symbol_id = row.get("symbol_id") or row.get("SymbolId", "")
        table_name = row.get("table_name") or row.get("TableName", "")
        op = row.get("op") or row.get("Op", "")
        sql_text = row.get("sql_text") or row.get("SqlText", "")
        line = row.get("line") or row.get("Line", 0)
        fp = row.get("file_path") or row.get("FilePath", file_path)
        source_ref = row.get("source_ref") or row.get("SourceRef", fp or file_path)
        rows.append(
            DataAccessRow(
                symbol_id=str(symbol_id),
                table_name=str(table_name),
                op=str(op),
                sql_text=str(sql_text),
                file_path=str(fp or file_path),
                line=int(line or 0),
                source_ref=str(source_ref),
            )
        )
    return rows


def _audit_row(file_path: str, language: str, method: str, status: str, reason: str = "") -> dict:
    return {
        "file_path": file_path,
        "language": language,
        "method": method,
        "status": status,
        "reason": reason,
        "source_ref": file_path,
    }


def _log_audit_summary(audit_rows: list[dict]) -> None:
    counts: dict[str, int] = {}
    for row in audit_rows:
        key = f"{row.get('language')}:{row.get('method')}:{row.get('status')}"
        counts[key] = counts.get(key, 0) + 1
    if counts:
        LOGGER.info("parse_audit_summary")
        for key, value in sorted(counts.items()):
            LOGGER.info("%s=%s", key, value)


def _ensure_query_coverage(config: ParserConfig) -> None:
    required_suffixes = ["symbols", "calls", "conditions", "constants", "data_access"]
    missing: list[str] = []
    languages = sorted(set(config.language_map.values()))
    for language_name in languages:
        if language_name == "text" or language_name in set(config.roslyn_languages):
            continue
        for suffix in required_suffixes:
            query_text = load_query(config.queries_dir, language_name, suffix)
            if not query_text and suffix != "symbols":
                # Allow empty but present files; treat missing file as coverage error.
                path = config.queries_dir / f"{language_name}.{suffix}.scm"
                if not path.exists():
                    missing.append(str(path))
            if suffix == "symbols":
                path = config.queries_dir / f"{language_name}.scm"
                if not path.exists():
                    missing.append(str(path))
    if missing:
        missing_list = "\n".join(sorted(set(missing)))
        raise RuntimeError(f"Missing required .scm query files:\n{missing_list}")


def _ensure_language_library(config: ParserConfig) -> None:
    if config.language_library_path.exists():
        return
    config.language_library_path.parent.mkdir(parents=True, exist_ok=True)
    if not (config.auto_build_languages_if_missing and config.tree_sitter_languages_config_path):
        raise FileNotFoundError(
            f"Missing language library: {config.language_library_path}"
        )
    LOGGER.info(
        "parser_build_languages start config=%s",
        config.tree_sitter_languages_config_path,
    )
    build_config = load_languages_config(config.tree_sitter_languages_config_path)
    build_languages(build_config)
    if not config.language_library_path.exists():
        raise FileNotFoundError(
            f"Language library not found after build: {config.language_library_path}"
        )


if __name__ == "__main__":
    main()
