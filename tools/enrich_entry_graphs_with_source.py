#!/usr/bin/env python3
"""
Enrich entry graphs with source snippets for entry and exit nodes.

Inputs (stage_1, run_id):
  - code_graph_nodes
  - code_graph_edges
  - symbols
  - entry_graphs

Outputs:
  - data/parquet/<run_id>/stage_1/entry_graphs_with_source/run_id=<run_id>/artifact_version=<artifact_version>/entry_graphs_with_source-0.parquet

Fields:
  entry_key, entry_node_id, entry_file_path, entry_line, entry_snippet,
  exit_nodes (json list of ids),
  exit_sources (json list of {node_id, file_path, line, snippet}),
  max_depth, reachable_nodes_count, run_id, artifact_version, created_at

No grouping/top-k filtering; uses existing entry_graphs parquet.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq


def load_run_id(run_id: str | None, output_root: Path) -> str:
    if run_id:
        return run_id
    latest = output_root / "LATEST_RUN"
    if latest.exists():
        return latest.read_text().strip()
    raise SystemExit("run_id not provided and data/parquet/LATEST_RUN not found")


def load_parquet(path: Path) -> Tuple[List[Dict], List[str]]:
    con = duckdb.connect()
    rows = con.execute(f"select * from read_parquet('{path}')").fetchall()
    cols = [c[0] for c in con.execute(f"describe select * from read_parquet('{path}')").fetchall()]
    def to_dict(row): return {k: v for k, v in zip(cols, row)}
    return [to_dict(r) for r in rows], cols


def adjacency(edges: Iterable[Dict]) -> Tuple[Dict[str, List[str]], Dict[str, int], Dict[str, int]]:
    adj: Dict[str, List[str]] = defaultdict(list)
    indeg: Dict[str, int] = defaultdict(int)
    outdeg: Dict[str, int] = defaultdict(int)
    for row in edges:
        u = str(row.get("from_id", "") or "")
        v = str(row.get("to_id", "") or "")
        if not u or not v:
            continue
        adj[u].append(v)
        indeg[v] += 1
        outdeg[u] += 1
    return adj, indeg, outdeg


def reachable_from(entry: str, adj: Dict[str, List[str]]) -> List[str]:
    seen = []
    visited = set()
    stack = [entry]
    while stack:
        cur = stack.pop()
        for nxt in adj.get(cur, []):
            if nxt not in visited:
                visited.add(nxt)
                seen.append(nxt)
                stack.append(nxt)
    return seen


def exit_nodes(reachables: List[str], outdeg: Dict[str, int]) -> List[str]:
    return [n for n in reachables if outdeg.get(n, 0) == 0]


def load_symbols_map(symbols: List[Dict]) -> Dict[str, Tuple[Path, int]]:
    out: Dict[str, Tuple[Path, int]] = {}
    for row in symbols:
        sym_id = row.get("symbol_id")
        file_path = row.get("file_path")
        line = row.get("line")
        if sym_id and file_path and isinstance(line, int):
            out[str(sym_id)] = (Path(file_path), int(line))
    return out


def node_symbol_map(nodes: List[Dict]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for row in nodes:
        nid = row.get("node_id")
        sym = row.get("symbol_id")
        if nid and sym:
            out[str(nid)] = str(sym)
    return out


def read_snippet(file_path: Path, line: int, context: int = 4) -> str:
    try:
        lines = file_path.read_text(errors="ignore").splitlines()
        start = max(0, line - 1 - context)
        end = min(len(lines), line + context)
        snippet = "\n".join(lines[start:end])
        return snippet
    except FileNotFoundError:
        return ""
    except Exception:
        return ""


def enrich(entries: List[Dict], adj, outdeg, node_to_sym, sym_to_src, context=4) -> List[Dict]:
    created_at = datetime.now(timezone.utc).isoformat()
    rows: List[Dict] = []
    for row in entries:
        entry_key = str(row.get("entry_key"))
        entry_nodes = json.loads(row.get("entry_nodes") or "[]")
        entry_node_id = entry_nodes[0] if entry_nodes else entry_key
        reachables = json.loads(row.get("reachable_nodes") or "[]")
        exits = exit_nodes(reachables, outdeg)
        entry_sym = node_to_sym.get(entry_node_id)
        entry_src = sym_to_src.get(entry_sym) if entry_sym else None
        entry_file = str(entry_src[0]) if entry_src else ""
        entry_line = entry_src[1] if entry_src else None
        entry_snippet = read_snippet(entry_src[0], entry_line, context) if entry_src else ""
        exit_sources = []
        for ex in exits:
            sym = node_to_sym.get(ex)
            src = sym_to_src.get(sym) if sym else None
            if not src:
                exit_sources.append({"node_id": ex, "file_path": "", "line": None, "snippet": ""})
            else:
                exit_sources.append(
                    {
                        "node_id": ex,
                        "file_path": str(src[0]),
                        "line": src[1],
                        "snippet": read_snippet(src[0], src[1], context),
                    }
                )
        rows.append(
            {
                "entry_key": entry_key,
                "entry_node_id": entry_node_id,
                "entry_file_path": entry_file,
                "entry_line": entry_line,
                "entry_snippet": entry_snippet,
                "exit_nodes": json.dumps(exits, ensure_ascii=True),
                "exit_sources": json.dumps(exit_sources, ensure_ascii=True),
                "max_depth": float(row.get("capped_depth") or row.get("normalized_depth") or 0.0),
                "reachable_nodes_count": len(reachables),
                "duplicate_of": row.get("duplicate_of"),
                "created_at": created_at,
            }
        )
    return rows


def write_parquet(rows: List[Dict], out_path: Path, run_id: str, artifact_version: int):
    for row in rows:
        row["run_id"] = run_id
        row["artifact_version"] = artifact_version
    table = pa.Table.from_pylist(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, out_path)
    print(f"Wrote {len(rows)} rows to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich entry graphs with source snippets for entry/exit nodes.")
    parser.add_argument("--run-id", dest="run_id", help="run_id (default: data/parquet/LATEST_RUN)")
    parser.add_argument("--artifact-version", type=int, default=1)
    parser.add_argument("--output-root", type=Path, default=Path("data/parquet"))
    parser.add_argument("--context", type=int, default=4, help="Lines of context around the line")
    args = parser.parse_args()

    run_id = load_run_id(args.run_id, args.output_root)
    base = args.output_root / run_id / "stage_1"
    def p(name): return base / name / f"run_id={run_id}" / f"artifact_version={args.artifact_version}" / f"{name}-0.parquet"
    nodes_path = p("code_graph_nodes")
    edges_path = p("code_graph_edges")
    symbols_path = p("symbols")
    entries_path = p("entry_graphs")
    out_path = base / "entry_graphs_with_source" / f"run_id={run_id}" / f"artifact_version={args.artifact_version}" / "entry_graphs_with_source-0.parquet"

    code_graph_nodes, _ = load_parquet(nodes_path)
    code_graph_edges, _ = load_parquet(edges_path)
    symbols, _ = load_parquet(symbols_path)
    entry_graphs, _ = load_parquet(entries_path)

    node_to_sym = node_symbol_map(code_graph_nodes)
    sym_to_src = load_symbols_map(symbols)
    adj, indeg, outdeg = adjacency(code_graph_edges)
    rows = enrich(entry_graphs, adj, outdeg, node_to_sym, sym_to_src, args.context)
    write_parquet(rows, out_path, run_id, args.artifact_version)


if __name__ == "__main__":
    main()
