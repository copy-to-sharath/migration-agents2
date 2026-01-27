from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, List


def _remove_paths(paths: Iterable[Path], execute: bool) -> List[Path]:
    removed: List[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if execute:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        removed.append(path)
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean parser-generated artifacts (entry graphs, depth buckets, logs)."
    )
    parser.add_argument(
        "--target",
        choices=["build", "llm", "all"],
        default="all",
        help="Choose which parser outputs to remove. 'build' deletes parse/graph artifacts; "
        "'llm' deletes LLM summary artifacts; 'all' deletes both.",
    )
    parser.add_argument(
        "--run-id",
        help="run_id suffix (e.g., 20260118142610). Cleans run_<id> under entry_graphs and depth_buckets.",
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Also remove parser entry-graph prompt/debug logs (entry_graph_*.txt).",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete files. Without this flag, a dry-run is performed.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    parquet_root = root / "data" / "parquet"
    entry_graphs_root = parquet_root / "entry_graphs"
    depth_buckets_root = root / "generated" / "depth_buckets"
    logs_root = root / "logs"

    build_tables = [
        "symbols",
        "calls",
        "conditions",
        "constants",
        "data_access",
        "parse_audit",
        "code_graph_nodes",
        "code_graph_edges",
        "graph_metadata",
        "entry_exit_map",
        "entry_graphs",
        "entry_graph_state",
        "entry_graph_processing_summary",
        "coverage_summary",
    ]
    llm_tables = [
        "entry_graph_summaries",
        "entry_graph_summaries_merged",
        "entry_graph_llm_debug",
    ]

    targets: List[Path] = []

    if args.run_id:
        stage_root = parquet_root / f"run_{args.run_id}" / "stage_1"
        if args.target in ("build", "all"):
            targets.extend(stage_root / name for name in build_tables)
            targets.append(entry_graphs_root / f"run_{args.run_id}")
            targets.append(depth_buckets_root / f"run_{args.run_id}")
        if args.target in ("llm", "all"):
            targets.extend(stage_root / name for name in llm_tables)
    else:
        parser.error("Specify --run-id to scope cleanup.")

    if args.logs:
        targets.extend(logs_root.glob("entry_graph_*.txt"))

    if not targets:
        parser.error("No targets selected; check flags.")

    removed = _remove_paths(targets, execute=args.execute)

    action = "Deleted" if args.execute else "Dry-run (would delete)"
    for path in removed:
        print(f"{action}: {path}")


if __name__ == "__main__":
    main()
