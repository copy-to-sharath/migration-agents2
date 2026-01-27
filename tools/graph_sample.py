from __future__ import annotations

import json
import logging
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import networkx as nx


EXCLUDED_ENTRY_NODES: set[str] = set()


@dataclass(frozen=True)
class GraphSampleConfig:
    max_depth_limit: int = 50
    node_count_limit: int = 200
    depth_score_threshold: int = 1
    entry_graph_top_k: int | None = 5
    print_graph_text: bool = False
    render_png: bool = False
    graphs_root: Path = Path("tools/graphs")
    log_level: str = "INFO"
    log_every: int = 1
    incremental: bool = False
    clean_output: bool = True


def _load_config(path: Path) -> GraphSampleConfig:
    if not path.exists():
        return GraphSampleConfig()
    raw = json.loads(path.read_text(encoding="utf-8"))
    return GraphSampleConfig(
        max_depth_limit=int(raw.get("max_depth_limit", 50)),
        node_count_limit=int(raw.get("node_count_limit", 200)),
        depth_score_threshold=int(raw.get("depth_score_threshold", 1)),
        entry_graph_top_k=raw.get("entry_graph_top_k", 5),
        print_graph_text=bool(raw.get("print_graph_text", False)),
        render_png=bool(raw.get("render_png", False)),
        graphs_root=Path(raw.get("graphs_root", "tools/graphs")),
        log_level=str(raw.get("log_level", "INFO")),
        log_every=int(raw.get("log_every", 1)),
        incremental=bool(raw.get("incremental", False)),
        clean_output=bool(raw.get("clean_output", True)),
    )


_RUNTIME_CONFIG = GraphSampleConfig()
LOGGER = logging.getLogger("graph_sample")


def _setup_logging(config: GraphSampleConfig) -> None:
    level = getattr(logging, config.log_level.upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")


def build_graph() -> tuple[nx.DiGraph, dict[str, str]]:
    start = perf_counter()
    nodes = [f"M{i}" for i in range(1, 31)]
    edges = []
    # Sequential chain M1->M2->...->M10
    for i in range(1, 10):
        edges.append((f"M{i}", f"M{i+1}"))
    # Parallel fan-out from M2
    edges.extend([("M2", "M11"), ("M2", "M12"), ("M2", "M13")])
    # Parallel fan-out from M5
    edges.extend([("M5", "M14"), ("M5", "M15")])
    # Join M11,M12 -> M16
    edges.extend([("M11", "M16"), ("M12", "M16")])
    # Second entry chain M21->M22->M23
    edges.extend([("M21", "M22"), ("M22", "M23")])
    # Second entry parallel
    edges.extend([("M21", "M24"), ("M21", "M25")])
    # Recursive M17->M17
    edges.append(("M17", "M17"))
    # Cycle M18->M19->M20->M18
    edges.extend([("M18", "M19"), ("M19", "M20"), ("M20", "M18")])
    # Extra cross edges
    edges.append(("M4", "M12"))
    edges.append(("M23", "M10"))

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    node_types: dict[str, str] = {node: "symbol" for node in nodes}
    node_types["M5"] = "sql_site"
    node_types["M16"] = "table"
    node_types["M20"] = "callee"
    LOGGER.info("build_graph nodes=%d edges=%d in %.3fs", len(nodes), len(edges), perf_counter() - start)
    return graph, node_types


def print_adjacency(graph: nx.DiGraph, node_types: dict[str, str]) -> None:
    print("adjacency_list")
    for node in sorted(graph.nodes):
        neighbors = sorted(graph.successors(node))
        node_type = node_types.get(node, "symbol")
        label = f"{node}({node_type})"
        if neighbors:
            print(f"{label}: {', '.join(neighbors)}")
        else:
            print(f"{label}:")


def print_dot(
    graph: nx.DiGraph,
    node_types: dict[str, str],
    summary: dict[str, object],
) -> None:
    print("\nDOT")
    print("digraph G {")
    print('  labelloc="t";')
    entry_nodes = set(summary.get("entry_candidates", []))
    entry_group_nodes = set(summary.get("entry_group_nodes", []))
    exit_nodes = set(summary.get("exit_nodes", []))
    group_count = len(summary.get("entry_groups", []))
    print(
        f'  label="entries={len(entry_nodes)} entry_groups={group_count} '
        f'exits={len(exit_nodes)}";'
    )
    for node in sorted(graph.nodes):
        node_type = node_types.get(node, "symbol")
        pr = graph.nodes[node].get("pagerank", 0.0)
        if node in entry_nodes:
            role = "entry"
        elif node in entry_group_nodes:
            role = "entry_group"
        elif node in exit_nodes:
            role = "exit"
        else:
            role = "node"
        print(
            f'  "{node}" [label="{node}\\n{role}\\n{node_type}\\n'
            f'pr={pr:.4f}"];'
        )
    for source, target in graph.edges:
        print(f'  "{source}" -> "{target}";')
    print("}")

def _format_dot(
    graph: nx.DiGraph,
    node_types: dict[str, str],
    summary: dict[str, object],
    nodes: list[str],
    edges: list[tuple[str, str]],
    title: str,
) -> str:
    lines = ["digraph G {"]
    lines.append('  labelloc="t";')
    lines.append(f'  label="{title}";')
    entry_nodes = set(summary.get("entry_candidates", []))
    entry_group_nodes = set(summary.get("entry_group_nodes", []))
    exit_nodes = set(summary.get("exit_nodes", []))
    for node in nodes:
        node_type = node_types.get(node, "symbol")
        pr = graph.nodes[node].get("pagerank", 0.0)
        if node in entry_nodes:
            role = "entry"
        elif node in entry_group_nodes:
            role = "entry_group"
        elif node in exit_nodes:
            role = "exit"
        else:
            role = "node"
        lines.append(
            f'  "{node}" [label="{node}\\n{role}\\n{node_type}\\n'
            f'pr={pr:.4f}"];'
        )
    for source, target in edges:
        lines.append(f'  "{source}" -> "{target}";')
    lines.append("}")
    return "\n".join(lines)


def write_dot(
    graph: nx.DiGraph,
    node_types: dict[str, str],
    summary: dict[str, object],
    path: Path,
) -> None:
    entry_nodes = set(summary.get("entry_candidates", []))
    exit_nodes = set(summary.get("exit_nodes", []))
    group_count = len(summary.get("entry_groups", []))
    title = (
        f"entries={len(entry_nodes)} entry_groups={group_count} "
        f"exits={len(exit_nodes)}"
    )
    content = _format_dot(
        graph,
        node_types,
        summary,
        sorted(graph.nodes),
        list(graph.edges),
        title,
    )
    path.write_text(content, encoding="utf-8")


CONFIG_PATH = Path("tools/graph_sample.json")


def _entry_depth_metrics(
    graph: nx.DiGraph,
    entry: str,
    config: GraphSampleConfig,
) -> tuple[dict[str, float], set[str]]:
    max_depth = 0
    reachable: set[str] = set()
    stack: list[tuple[str, int, set[str]]] = [(entry, 0, {entry})]
    while stack:
        node, depth, path = stack.pop()
        reachable.add(node)
        if depth > max_depth:
            max_depth = depth
        if depth >= config.max_depth_limit:
            continue
        for neighbor in graph.successors(node):
            if neighbor in path:
                continue
            stack.append((neighbor, depth + 1, path | {neighbor}))
    capped_depth = min(max_depth, config.max_depth_limit)
    normalized = capped_depth / config.max_depth_limit if config.max_depth_limit else 0.0
    log_scaled = (
        math.log1p(capped_depth) / math.log1p(config.max_depth_limit)
        if config.max_depth_limit
        else 0.0
    )
    capped_nodes = min(len(reachable), config.node_count_limit)
    depth_breadth = (
        (capped_depth * capped_nodes) / config.node_count_limit
        if config.node_count_limit
        else 0.0
    )
    return {
        "max_depth": float(max_depth),
        "capped_depth": float(capped_depth),
        "normalized": float(normalized),
        "log_scaled": float(log_scaled),
        "depth_breadth": float(depth_breadth),
        "reachable_nodes": float(len(reachable)),
    }, reachable


def _score_folder_name(metrics: dict[str, float]) -> str:
    return f"depth_score_{int(metrics['capped_depth'])}"


def _score_title(metrics: dict[str, float]) -> str:
    return (
        "depth_scores="
        f"capped:{metrics['capped_depth']:.0f},"
        f"norm:{metrics['normalized']:.2f},"
        f"log:{metrics['log_scaled']:.2f},"
        f"depth_breadth:{metrics['depth_breadth']:.2f}"
    )


def _full_graph_title(summary: dict[str, object]) -> str:
    entry_nodes = set(summary.get("entry_candidates", []))
    exit_nodes = set(summary.get("exit_nodes", []))
    group_count = len(summary.get("entry_groups", []))
    return f"entries={len(entry_nodes)} entry_groups={group_count} exits={len(exit_nodes)}"


def _write_if_changed(path: Path, content: str, incremental: bool) -> bool:
    if incremental and path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


def write_entry_subgraphs(
    graph: nx.DiGraph,
    node_types: dict[str, str],
    summary: dict[str, object],
    output_dir: Path,
    config: GraphSampleConfig,
) -> list[Path]:
    entry_nodes = list(summary.get("entry_candidates", []))
    entry_groups = list(summary.get("entry_groups", []))
    exit_nodes = set(summary.get("exit_nodes", []))
    candidates: list[dict[str, object]] = []
    entry_cache: dict[str, tuple[dict[str, float], set[str]]] = {}
    written: list[Path] = []
    for entry in entry_nodes:
        metrics, reachable = _entry_depth_metrics(graph, entry, config)
        entry_cache[entry] = (metrics, reachable)
        if not reachable & exit_nodes:
            continue
        nodes = sorted(reachable)
        edges = [
            (source, target)
            for source, target in graph.edges
            if source in reachable and target in reachable and target != entry
        ]
        if metrics["capped_depth"] < config.depth_score_threshold:
            continue
        title = f"entry_subgraph={entry} {_score_title(metrics)}"
        content = _format_dot(graph, node_types, summary, nodes, edges, title)
        candidates.append(
            {
                "kind": "entry",
                "name": entry,
                "metrics": metrics,
                "content": content,
            }
        )
    for group in entry_groups:
        group_id = str(group.get("group_id", "group"))
        nodes_in_group = set(group.get("nodes", []))
        if not nodes_in_group:
            continue
        reachable = set(nodes_in_group)
        metrics_by_node: list[dict[str, float]] = []
        for entry in nodes_in_group:
            metrics, entry_reachable = entry_cache.get(entry) or _entry_depth_metrics(
                graph, entry, config
            )
            entry_cache[entry] = (metrics, entry_reachable)
            metrics_by_node.append(metrics)
            reachable |= entry_reachable
        if not reachable & exit_nodes:
            continue
        nodes = sorted(reachable)
        edges = [
            (source, target)
            for source, target in graph.edges
            if source in reachable
            and target in reachable
            and not (target in nodes_in_group and source not in nodes_in_group)
        ]
        metrics = max(metrics_by_node, key=lambda item: item["max_depth"])
        if metrics["capped_depth"] < config.depth_score_threshold:
            continue
        title = f"entry_group={group_id} {_score_title(metrics)}"
        content = _format_dot(graph, node_types, summary, nodes, edges, title)
        candidates.append(
            {
                "kind": "entry_group",
                "name": group_id,
                "metrics": metrics,
                "content": content,
            }
        )
    if config.entry_graph_top_k is not None:
        candidates = sorted(
            candidates,
            key=lambda item: (
                float(item["metrics"]["capped_depth"]),
                float(item["metrics"]["depth_breadth"]),
            ),
            reverse=True,
        )[: config.entry_graph_top_k]
    for item in candidates:
        metrics = item["metrics"]
        depth_dir = output_dir / _score_folder_name(metrics)
        depth_dir.mkdir(parents=True, exist_ok=True)
        if item["kind"] == "entry_group":
            filename = f"graph_sample.entry_group.{item['name']}.dot"
        else:
            filename = f"graph_sample.entry.{item['name']}.dot"
        dot_path = depth_dir / filename
        if _write_if_changed(dot_path, item["content"], config.incremental):
            LOGGER.info("wrote_dot=%s", dot_path)
        written.append(dot_path)
    return written


def render_png(dot_path: Path, png_path: Path) -> None:
    if not _RUNTIME_CONFIG.render_png:
        return
    if _RUNTIME_CONFIG.incremental and png_path.exists():
        return
    dot = shutil.which("dot")
    if not dot:
        print(f"dot_not_found: install graphviz to render {png_path}")
        return
    subprocess.run([dot, "-Tpng", str(dot_path), "-o", str(png_path)], check=True)
    LOGGER.info("rendered_png=%s", png_path)


def print_pagerank_entry_exit(
    graph: nx.DiGraph,
) -> dict[str, object]:
    start = perf_counter()
    pr = nx.pagerank(graph)
    for node, value in pr.items():
        graph.nodes[node]["pagerank"] = value
    in_deg = dict(graph.in_degree())
    out_deg = dict(graph.out_degree())
    entry_candidates = [
        node
        for node in graph.nodes
        if in_deg.get(node, 0) == 0
        and out_deg.get(node, 0) > 0
        and node not in EXCLUDED_ENTRY_NODES
    ]
    entry_groups: list[dict[str, object]] = []
    entry_group_nodes: set[str] = set()
    sccs = list(nx.strongly_connected_components(graph))
    for comp in sccs:
        if len(comp) == 1:
            continue
        has_incoming = False
        for node in comp:
            for pred in graph.predecessors(node):
                if pred not in comp:
                    has_incoming = True
                    break
            if has_incoming:
                break
        if not has_incoming:
            group_nodes = sorted(node for node in comp if node not in EXCLUDED_ENTRY_NODES)
            if group_nodes:
                group_id = "scc_" + "_".join(group_nodes)
                entry_groups.append({"group_id": group_id, "nodes": group_nodes})
                entry_group_nodes.update(group_nodes)
    entry_candidates = sorted(set(entry_candidates))
    recursive = {node for node in graph.nodes if graph.has_edge(node, node)}
    for comp in sccs:
        if len(comp) > 1:
            recursive |= comp
    exits = [
        node for node in graph.nodes if out_deg.get(node, 0) == 0 or node in recursive
    ]
    exits = sorted(exits, key=lambda node: pr.get(node, 0.0), reverse=True)
    LOGGER.info(
        "pagerank top5=%s",
        sorted(pr.items(), key=lambda kv: kv[1], reverse=True)[:5],
    )
    LOGGER.info("pagerank_sum=%.6f", sum(pr.values()))
    LOGGER.info("entry_candidates=%s", sorted(entry_candidates))
    LOGGER.info("excluded_entry_candidates=%s", sorted(EXCLUDED_ENTRY_NODES))
    LOGGER.info("exits_top5=%s", exits[:5])
    LOGGER.info("pagerank_elapsed=%.3fs", perf_counter() - start)
    return {
        "entry_candidates": sorted(entry_candidates),
        "entry_groups": entry_groups,
        "entry_group_nodes": sorted(entry_group_nodes),
        "exit_nodes": exits,
    }


def main() -> None:
    global _RUNTIME_CONFIG
    _RUNTIME_CONFIG = _load_config(CONFIG_PATH)
    _setup_logging(_RUNTIME_CONFIG)
    graph, node_types = build_graph()
    if _RUNTIME_CONFIG.print_graph_text:
        print_adjacency(graph, node_types)
    summary = print_pagerank_entry_exit(graph)
    if _RUNTIME_CONFIG.print_graph_text:
        print_dot(graph, node_types, summary)
    graphs_root = _RUNTIME_CONFIG.graphs_root
    if _RUNTIME_CONFIG.clean_output and graphs_root.exists():
        shutil.rmtree(graphs_root)
    full_dir = graphs_root / "full"
    full_dir.mkdir(parents=True, exist_ok=True)
    dot_path = full_dir / "graph_sample.dot"
    png_path = full_dir / "graph_sample.png"
    full_content = _format_dot(
        graph,
        node_types,
        summary,
        sorted(graph.nodes),
        list(graph.edges),
        _full_graph_title(summary),
    )
    if _write_if_changed(dot_path, full_content, _RUNTIME_CONFIG.incremental):
        LOGGER.info("wrote_dot=%s", dot_path)
    render_png(dot_path, png_path)
    start_entries = perf_counter()
    entry_dots = write_entry_subgraphs(
        graph, node_types, summary, graphs_root / "entries", _RUNTIME_CONFIG
    )
    for entry_dot in entry_dots:
        render_png(entry_dot, entry_dot.with_suffix(".png"))
    LOGGER.info(
        "entry_graphs_written=%d in %.3fs",
        len(entry_dots),
        perf_counter() - start_entries,
    )


if __name__ == "__main__":
    main()
