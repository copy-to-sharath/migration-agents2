from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Set

import duckdb


def load_parallel_callers(con: duckdb.DuckDBPyConnection, conditions_glob: str) -> Set[str]:
    query = """
        select distinct entry_key
        from read_parquet(?)
        where value like 'parallel:%'
    """
    return {row[0] for row in con.execute(query, [conditions_glob]).fetchall()}


def load_edges(
    con: duckdb.DuckDBPyConnection,
    edges_glob: str,
    parallel_callers: Set[str],
    mode: str,
) -> list[tuple[str, str, str]]:
    query = """
        select
          caller,
          callee,
          coalesce(file_path, source_ref, '') as file_path
        from read_parquet(?)
    """
    rows = con.execute(query, [edges_glob]).fetchall()
    if mode == "parallel":
        return [(c, d, f) for c, d, f in rows if c in parallel_callers]
    if mode == "sequential":
        return [(c, d, f) for c, d, f in rows if c not in parallel_callers]
    return rows


def write_dot(edges: Iterable[tuple[str, str, str]], output: Path) -> None:
    nodes: Set[str] = set()
    lines = ["digraph callgraph {"]
    lines.append('  rankdir=LR;')
    for caller, callee, file_path in edges:
        nodes.add(caller)
        nodes.add(callee)
        label = file_path if file_path else ""
        attr = f' [label="{label}"]' if label else ""
        lines.append(f'  "{caller}" -> "{callee}"{attr};')
    for node in nodes:
        lines.append(f'  "{node}";')
    lines.append("}")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export call graph DOT from parser outputs, with optional parallel/sequential filtering."
    )
    parser.add_argument("--run-id", required=True, help="run_id suffix, e.g., 20260118142610")
    parser.add_argument(
        "--mode",
        choices=["all", "parallel", "sequential"],
        default="all",
        help="Select all edges, only callers tagged as parallel, or only sequential callers.",
    )
    parser.add_argument(
        "--parquet-root",
        default="data/parquet",
        help="Root directory containing run_<id>/stage_1 parquet outputs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("callgraph.dot"),
        help="Output DOT file path.",
    )
    args = parser.parse_args()

    parquet_root = Path(args.parquet_root).expanduser().resolve()
    run_stage = parquet_root / f"run_{args.run_id}" / "stage_1"
    edges_glob = str(run_stage / "code_graph_edges" / "*.parquet")
    conditions_glob = str(run_stage / "conditions" / "*.parquet")

    con = duckdb.connect(database=":memory:")
    parallel_callers: Set[str] = set()
    if args.mode in ("parallel", "sequential"):
        parallel_callers = load_parallel_callers(con, conditions_glob)

    edges = load_edges(con, edges_glob, parallel_callers, args.mode)
    write_dot(edges, args.output)
    print(f"Wrote DOT to {args.output} (mode={args.mode}, edges={len(edges)})")


if __name__ == "__main__":
    main()
