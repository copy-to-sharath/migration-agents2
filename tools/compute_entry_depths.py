#!/usr/bin/env python3
"""
Compute entry depths for all entry nodes using DFS and write a parquet without grouping or filtering.
Inputs: stage_1 code_graph_nodes/code_graph_edges for a run_id.
Outputs: data/parquet/<run_id>/stage_1/entry_depths/run_id=<run_id>/artifact_version=<artifact_version>/entry_depths-0.parquet
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

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


def read_edges(nodes_path: Path, edges_path: Path) -> Tuple[List[Dict], List[Dict]]:
    if not nodes_path.exists():
        raise SystemExit(f"code_graph_nodes parquet missing: {nodes_path}")
    if not edges_path.exists():
        raise SystemExit(f"code_graph_edges parquet missing: {edges_path}")
    con = duckdb.connect()
    nodes = con.execute(f"select * from read_parquet('{nodes_path}')").fetchall()
    edges = con.execute(f"select * from read_parquet('{edges_path}')").fetchall()
    node_cols = [c[0] for c in con.execute(f"describe select * from read_parquet('{nodes_path}')").fetchall()]
    edge_cols = [c[0] for c in con.execute(f"describe select * from read_parquet('{edges_path}')").fetchall()]
    def to_dict(row, cols): return {k: v for k, v in zip(cols, row)}
    return [to_dict(r, node_cols) for r in nodes], [to_dict(r, edge_cols) for r in edges]


def adjacency(edges: Iterable[Dict]) -> Tuple[Dict[str, Set[str]], Dict[str, int], Dict[str, int]]:
    adj: Dict[str, Set[str]] = defaultdict(set)
    indeg: Dict[str, int] = defaultdict(int)
    outdeg: Dict[str, int] = defaultdict(int)
    for row in edges:
        u = str(row.get("from_id", "") or "")
        v = str(row.get("to_id", "") or "")
        if not u or not v:
            continue
        if v not in adj[u]:
            adj[u].add(v)
            indeg[v] += 1
            outdeg[u] += 1
    return adj, indeg, outdeg


def dfs_depth(node: str, adj: Dict[str, Set[str]], memo: Dict[str, int], stack: Set[str]) -> int:
    if node in memo:
        return memo[node]
    if node in stack:
        # cycle detected; do not extend depth through this edge
        return 0
    stack.add(node)
    depth = 0
    for nxt in adj.get(node, ()):
        depth = max(depth, 1 + dfs_depth(nxt, adj, memo, stack))
    stack.remove(node)
    memo[node] = depth
    return depth


def reachable_from(node: str, adj: Dict[str, Set[str]]) -> Set[str]:
    seen: Set[str] = set()
    stack = [node]
    while stack:
        cur = stack.pop()
        for nxt in adj.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def exit_nodes(adj: Dict[str, Set[str]], outdeg: Dict[str, int], reachable: Set[str]) -> List[str]:
    exits = []
    for n in reachable:
        if outdeg.get(n, 0) == 0:
            exits.append(n)
    return exits


def hash_set(values: Iterable[str]) -> str:
    import hashlib
    h = hashlib.sha256()
    for v in sorted(values):
        h.update(v.encode("utf-8"))
    return h.hexdigest()


def compute_entries(nodes: List[Dict], edges: List[Dict]) -> List[Dict]:
    adj, indeg, outdeg = adjacency(edges)
    node_ids = [str(n.get("node_id", "")) for n in nodes if n.get("node_id")]
    entries = [nid for nid in node_ids if indeg.get(nid, 0) == 0 and outdeg.get(nid, 0) > 0]
    memo_depth: Dict[str, int] = {}
    seen_hash: Dict[str, str] = {}
    rows: List[Dict] = []
    created_at = datetime.now(timezone.utc).isoformat()
    for entry in entries:
        max_depth = dfs_depth(entry, adj, memo_depth, set())
        reachable = reachable_from(entry, adj)
        exits = exit_nodes(adj, outdeg, reachable)
        r_hash = hash_set(reachable)
        duplicate_of = seen_hash.get(r_hash)
        if duplicate_of is None:
            seen_hash[r_hash] = entry
        row = {
            "entry_key": entry,
            "entry_type": "entry",
            "entry_node_id": entry,
            "max_depth": float(max_depth),
            "reachable_nodes": json.dumps(sorted(reachable), ensure_ascii=True),
            "reachable_nodes_count": len(reachable),
            "exit_nodes": json.dumps(sorted(exits), ensure_ascii=True),
            "duplicate_of": duplicate_of,
            "created_at": created_at,
        }
        rows.append(row)
    return rows


def write_parquet(rows: List[Dict], out_path: Path, run_id: str, artifact_version: int) -> None:
    for row in rows:
        row["run_id"] = run_id
        row["artifact_version"] = artifact_version
    table = pa.Table.from_pylist(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, out_path)
    print(f"Wrote {len(rows)} rows to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute entry depths for all entries (no grouping).")
    parser.add_argument("--run-id", dest="run_id", help="run_id (default: data/parquet/LATEST_RUN)")
    parser.add_argument("--artifact-version", type=int, default=1, help="artifact_version (default: 1)")
    parser.add_argument("--output-root", type=Path, default=Path("data/parquet"))
    args = parser.parse_args()

    run_id = load_run_id(args.run_id, args.output_root)
    base = args.output_root / run_id / "stage_1"
    nodes_path = base / "code_graph_nodes" / f"run_id={run_id}" / f"artifact_version={args.artifact_version}" / "code_graph_nodes-0.parquet"
    edges_path = base / "code_graph_edges" / f"run_id={run_id}" / f"artifact_version={args.artifact_version}" / "code_graph_edges-0.parquet"
    out_path = base / "entry_depths" / f"run_id={run_id}" / f"artifact_version={args.artifact_version}" / "entry_depths-0.parquet"

    nodes, edges = read_edges(nodes_path, edges_path)
    rows = compute_entries(nodes, edges)
    write_parquet(rows, out_path, run_id, args.artifact_version)


if __name__ == "__main__":
    main()
