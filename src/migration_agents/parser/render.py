from __future__ import annotations

import argparse
import glob
import json
import logging
import shutil
from pathlib import Path

import duckdb

from migration_agents.logging_utils import setup_logging
from migration_agents.parser.config import ParserConfig, load_config
from migration_agents.parser.main import (
    _entry_graph_basename,
    _format_graph_dot,
    _graph_label_map,
    _render_graph,
    _write_if_changed,
)
from migration_agents.shared_run_id import resolve_run_id

LOGGER = logging.getLogger("migration_agents.parser.render")


def _read_parquet_rows(base_dir: Path) -> list[dict]:
    paths = glob.glob(str(base_dir / "**" / "*.parquet"), recursive=True)
    if not paths:
        return []
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    # Extract run_id from path if possible
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
        return con.execute("select * from read_parquet($1)", [paths]).fetchdf().to_dict(orient="records")
    finally:
        con.close()


def _load_stage1_tables(output_root: Path, run_id: str):
    base = output_root / run_id / "step_2"
    nodes = _read_parquet_rows(base / "code_graph_nodes")
    edges = _read_parquet_rows(base / "code_graph_edges")
    symbols = _read_parquet_rows(base / "symbols")
    entry_graphs = _read_parquet_rows(base / "entry_graphs")
    return nodes, edges, symbols, entry_graphs


def _compute_exit_nodes(edges: list[dict], node_ids: set[str]) -> set[str]:
    out_degree = {nid: 0 for nid in node_ids}
    for row in edges:
        src = row.get("from_id")
        tgt = row.get("to_id")
        if src in out_degree:
            out_degree[src] += 1
        if tgt not in out_degree:
            out_degree[tgt] = 0
    return {nid for nid, deg in out_degree.items() if deg == 0}


def _render_full_graph(
    render_dir: Path,
    graph_nodes: list[dict],
    graph_edges: list[dict],
    entry_nodes: set[str],
    exit_nodes: set[str],
    graph_label_map: dict[str, str],
    render_dot: bool,
    render_png: bool,
    render_svg: bool,
    render_engine: str,
    incremental: bool,
):
    title = f"entries={len(entry_nodes)} exits={len(exit_nodes)}"
    dot = _format_graph_dot(
        graph_nodes,
        graph_edges,
        entry_nodes,
        set(),
        exit_nodes,
        title,
        graph_label_map,
    )
    dot_path = render_dir / "full" / "code_graph.dot"
    if render_dot:
        _write_if_changed(dot_path, dot, incremental)
    if render_png:
        _render_graph(dot_path, render_dir / "full" / "code_graph.png", incremental, render_engine, "png")
    if render_svg:
        _render_graph(dot_path, render_dir / "full" / "code_graph.svg", incremental, render_engine, "svg")


def _render_entry_graphs(
    render_dir: Path,
    graph_nodes: list[dict],
    graph_edges: list[dict],
    entry_graphs: list[dict],
    graph_label_map: dict[str, str],
    exit_nodes: set[str],
    render_dot: bool,
    render_png: bool,
    render_svg: bool,
    render_engine: str,
    incremental: bool,
):
    for idx, row in enumerate(entry_graphs, start=1):
        entry_key = str(row.get("entry_key"))
        entry_type = str(row.get("entry_type"))
        entry_nodes_set = set(json.loads(row.get("entry_nodes", "[]")))
        reachable = set(json.loads(row.get("reachable_nodes", "[]")))
        reachable_edges = [(a, b) for a, b in json.loads(row.get("reachable_edges", "[]"))]
        entry_title = f"{entry_type}={entry_key} depth={row.get('capped_depth', 0)}"
        raw_label = graph_label_map.get(entry_key, entry_key)
        base_name = _entry_graph_basename(raw_label, entry_key, entry_type, idx)
        nodes_subset = [n for n in graph_nodes if n.get("node_id") in reachable]
        edges_subset = [{"from_id": a, "to_id": b} for a, b in reachable_edges if a in reachable and b in reachable]
        dot = _format_graph_dot(
            nodes_subset,
            edges_subset,
            entry_nodes_set,
            entry_nodes_set if entry_type == "entry_group" else set(),
            exit_nodes & reachable,
            entry_title,
            graph_label_map,
        )
        dot_path = render_dir / "entries" / f"{base_name}.dot"
        if render_dot:
            _write_if_changed(dot_path, dot, incremental)
        if render_png:
            _render_graph(dot_path, render_dir / "entries" / f"{base_name}.png", incremental, render_engine, "png")
        if render_svg:
            _render_graph(dot_path, render_dir / "entries" / f"{base_name}.svg", incremental, render_engine, "svg")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render-only entry graph DOT/PNG/SVG from existing Parquet.")
    parser.add_argument("--config", type=Path, required=True, help="Parser render config JSON")
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("parser_render")
    config: ParserConfig = load_config(args.config)
    run_id = config.run_id if config.run_id != "auto" else resolve_run_id(config.output_root)

    render_root = config.entry_graph_render_dir / run_id / "step_2"
    if render_root.exists() and not config.entry_graph_incremental:
        shutil.rmtree(render_root)
    (render_root / "full").mkdir(parents=True, exist_ok=True)
    (render_root / "entries").mkdir(parents=True, exist_ok=True)

    nodes, edges, symbols, entry_graphs = _load_stage1_tables(config.output_root, run_id)
    if not nodes or not edges:
        raise RuntimeError("Missing step_2 tables (nodes/edges); run parser build first.")

    # Entry graphs are optional subsets - parent graph has all data
    if not entry_graphs:
        LOGGER.warning("No entry graphs found; skipping entry graph rendering (parent graph has all data)")
    
    graph_label_map = _graph_label_map(symbols, nodes)
    node_ids = {n.get("node_id") for n in nodes if n.get("node_id")}
    exit_nodes = _compute_exit_nodes(edges, node_ids)
    entry_nodes_union: set[str] = set()
    for row in entry_graphs:
        entry_nodes_union.update(json.loads(row.get("entry_nodes", "[]")))

    if config.entry_graph_render_full:
        _render_full_graph(
            render_root,
            nodes,
            edges,
            entry_nodes_union,
            exit_nodes,
            graph_label_map,
            config.entry_graph_render_dot,
            config.entry_graph_render_png,
            config.entry_graph_render_svg,
            config.entry_graph_render_engine,
            config.entry_graph_incremental,
        )

    if entry_graphs:
        _render_entry_graphs(
            render_root,
            nodes,
            edges,
            entry_graphs,
            graph_label_map,
            exit_nodes,
            config.entry_graph_render_dot,
            config.entry_graph_render_png,
            config.entry_graph_render_svg,
            config.entry_graph_render_engine,
            config.entry_graph_incremental,
        )
    LOGGER.info("parser_render_complete run_id=%s entries=%s", run_id, len(entry_graphs))


if __name__ == "__main__":
    main()
