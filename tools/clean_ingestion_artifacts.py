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
        description="Clean ingestion artifacts (intake_* tables for a run, or all)."
    )
    parser.add_argument(
        "--run-id",
        help="run_id suffix (e.g., 20260118142610). Cleans run_<id>/stage_0 under data/parquet.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Clean all ingestion artifacts (removes data/parquet/intake_* and stage_0). Requires --execute.",
    )
    parser.add_argument(
        "--flush-all",
        action="store_true",
        help="Flush ALL parquet files (removes entire data/parquet directory contents). Requires --execute.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete files. Without this flag, a dry-run is performed.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    parquet_root = root / "data" / "parquet"
    duckdb_root = root / "data" / "duckdb"
    graphs_root = root / "data" / "graphs"
    generated_root = root / "generated"

    targets: List[Path] = []

    if args.flush_all:
        # Flush ALL parquet data - complete reset for fresh ingestion
        # Include all run_* directories
        targets.extend(parquet_root.glob("run_*"))
        # Include all intake_* tables
        targets.extend(parquet_root.glob("intake_*"))
        # Include coverage_summary and entry_graphs
        targets.append(parquet_root / "coverage_summary")
        targets.append(parquet_root / "entry_graphs")
        # Include LATEST_RUN marker
        targets.append(parquet_root / "LATEST_RUN")
        # Also flush DuckDB files
        targets.extend(duckdb_root.glob("*.duckdb"))
        targets.extend(duckdb_root.glob("*.duckdb.wal"))
        # Flush generated graphs and state
        targets.extend(graphs_root.glob("*"))
        targets.append(generated_root / "graphs")
        targets.append(generated_root / "state")
        targets.append(generated_root / "depth_buckets")
    elif args.run_id:
        targets.append(parquet_root / f"run_{args.run_id}" / "stage_0")
        targets.extend(parquet_root.glob("intake_*"))
    elif args.all:
        targets.append(parquet_root / "intake_source_index")
        targets.append(parquet_root / "intake_source_chunks")
        targets.append(parquet_root / "intake_build_context")
        targets.append(parquet_root / "intake_schema_snapshot")
        targets.append(parquet_root / "intake_logs")
        targets.append(parquet_root / "intake_missing")
    else:
        parser.error("Specify --run-id, --all, or --flush-all.")

    removed = _remove_paths(targets, execute=args.execute)
    action = "Deleted" if args.execute else "Dry-run (would delete)"
    for path in removed:
        print(f"{action}: {path}")
    
    if args.flush_all and args.execute:
        print("\n✓ All parquet/duckdb/graph data flushed. Ready for fresh ingestion.")


if __name__ == "__main__":
    main()
