from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import duckdb
import networkx as nx

from migration_agents.parser.config import load_config
from migration_agents.parser.main import (
    _entry_graph_basename,
    _format_graph_dot,
    _graph_label_map,
    _safe_filename,
    _write_if_changed,
    _render_graph,
)


def _latest_run(root: Path) -> str:
    latest_path = root / "LATEST_RUN"
    if not latest_path.exists():
        raise SystemExit("LATEST_RUN not found; run ingestion/parser first.")
    return latest_path.read_text(encoding="utf-8").strip()


def _read_table(con: duckdb.DuckDBPyConnection, root: Path, table: str) -> list[dict]:
    files = [str(p) for p in (root / table).rglob("*.parquet")]
    if not files:
        raise SystemExit(f"Missing parquet table: {table}")
    rows = con.execute("select * from read_parquet(?::VARCHAR[])", [files]).fetchall()
    cols = [col[0] for col in con.execute("describe select * from read_parquet(?::VARCHAR[])", [files]).fetchall()]
    return [dict(zip(cols, row)) for row in rows]


def _compute_exit_nodes(graph_nodes: list[dict], graph_edges: list[dict]) -> set[str]:
    graph = nx.DiGraph()
    for node in graph_nodes:
        graph.add_node(node.get("node_id"))
    for edge in graph_edges:
        graph.add_edge(edge.get("from_id"), edge.get("to_id"))
    recursive = {node for node in graph.nodes if graph.has_edge(node, node)}
    for comp in nx.strongly_connected_components(graph):
        if len(comp) > 1:
            recursive |= comp
    out_degree = dict(graph.out_degree())
    return {
        node_id
        for node_id in graph.nodes
        if out_degree.get(node_id, 0) == 0 or node_id in recursive
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Render entry graphs from existing parquet.")
    parser.add_argument("--config", type=Path, default=Path("config/parser.example.json"))
    parser.add_argument("--run-id", type=str, default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    run_id = args.run_id or _latest_run(config.output_root)
    stage_root = config.output_root / run_id / "stage_1"
    con = duckdb.connect()

    graph_nodes = _read_table(con, stage_root, "code_graph_nodes")
    graph_edges = _read_table(con, stage_root, "code_graph_edges")
    symbols = _read_table(con, stage_root, "symbols")
    entry_graphs = _read_table(con, stage_root, "entry_graphs")

    graph_label_map = _graph_label_map(symbols, graph_nodes)
    exit_nodes = _compute_exit_nodes(graph_nodes, graph_edges)

    entry_nodes: set[str] = set()
    entry_group_nodes: set[str] = set()
    for row in entry_graphs:
        entry_key = str(row.get("entry_key", ""))
        entry_type = str(row.get("entry_type", "entry"))
        entry_node_ids = set(json.loads(row.get("entry_nodes") or "[]"))
        if entry_type == "entry":
            entry_nodes.add(entry_key)
        else:
            entry_group_nodes.update(entry_node_ids)

    render_root = config.entry_graph_render_dir / run_id / "stage_1"
    full_dir = render_root / "full"
    entries_dir = render_root / "entries"
    if render_root.exists():
        import shutil

        shutil.rmtree(render_root)
    full_dir.mkdir(parents=True, exist_ok=True)
    entries_dir.mkdir(parents=True, exist_ok=True)

    if args.full or config.entry_graph_render_full:
        full_title = f"entries={len(entry_nodes)} entry_groups={len(entry_group_nodes)} exits={len(exit_nodes)}"
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

    limit = args.limit if args.limit > 0 else len(entry_graphs)
    for idx, row in enumerate(entry_graphs[:limit], start=1):
        entry_key = str(row.get("entry_key", ""))
        entry_type = str(row.get("entry_type", "entry"))
        entry_nodes_set = set(json.loads(row.get("entry_nodes") or "[]"))
        reachable = set(json.loads(row.get("reachable_nodes") or "[]"))
        entry_edges = json.loads(row.get("reachable_edges") or "[]")
        entry_title = f"{entry_type}={entry_key}"
        raw_label = graph_label_map.get(entry_key, entry_key)
        base_name = _entry_graph_basename(raw_label, entry_key, entry_type, idx)
        entry_dot = _format_graph_dot(
            [node for node in graph_nodes if node.get("node_id") in reachable],
            [{"from_id": e[0], "to_id": e[1]} for e in entry_edges],
            entry_nodes_set,
            entry_nodes_set if entry_type == "entry_group" else set(),
            exit_nodes & reachable,
            entry_title,
            graph_label_map,
        )
        entry_dot_path = entries_dir / f"{_safe_filename(base_name)}.dot"
        if config.entry_graph_render_dot:
            _write_if_changed(entry_dot_path, entry_dot, config.entry_graph_incremental)
        if config.entry_graph_render_png:
            _render_graph(
                entry_dot_path,
                entries_dir / f"{_safe_filename(base_name)}.png",
                config.entry_graph_incremental,
                config.entry_graph_render_engine,
                "png",
            )
        if config.entry_graph_render_svg:
            _render_graph(
                entry_dot_path,
                entries_dir / f"{_safe_filename(base_name)}.svg",
                config.entry_graph_incremental,
                config.entry_graph_render_engine,
                "svg",
            )


if __name__ == "__main__":
    main()
