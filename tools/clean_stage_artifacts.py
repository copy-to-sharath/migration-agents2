from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, List


STAGE_DIRS = {
    "ingestion": "stage_0",
    "parser": "stage_1",
    "vectorization": "stage_2",
    "slice_extractor": "stage_3",
    "logic_manifester": "stage_4",
    "domain_architect": "stage_5",
    "knowledge_base": "stage_6",
    "api_migration": "stage_8",
    "codegen": "stage_9",
}

EXTRA_TABLE_ROOTS = {
    "ingestion": ["intake_source_index", "intake_source_chunks", "intake_build_context", "intake_schema_snapshot", "intake_logs", "intake_missing"],
    "parser": ["entry_graphs", "coverage_summary"],
}


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
        description="Clean stage artifacts under data/parquet/run_<id>/stage_X and related roots."
    )
    parser.add_argument(
        "--stage",
        choices=list(STAGE_DIRS.keys()) + ["all"],
        required=True,
        help="Stage to clean or 'all' for every stage.",
    )
    parser.add_argument(
        "--run-id",
        help="run_id suffix (e.g., 20260118142610). Cleans run_<id>/stage_X. Required unless --stage=all.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete files. Without this flag, a dry-run is performed.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    parquet_root = root / "data" / "parquet"

    targets: List[Path] = []
    stages = STAGE_DIRS.keys() if args.stage == "all" else [args.stage]

    if args.stage != "all" and not args.run_id:
        parser.error("Specify --run-id when cleaning a single stage.")

    for stage in stages:
        stage_dir = STAGE_DIRS[stage]
        if args.run_id:
            targets.append(parquet_root / f"run_{args.run_id}" / stage_dir)
        if stage in EXTRA_TABLE_ROOTS:
            targets.extend(parquet_root / name for name in EXTRA_TABLE_ROOTS[stage])

    if not targets:
        parser.error("No targets selected; check flags.")

    removed = _remove_paths(targets, execute=args.execute)
    action = "Deleted" if args.execute else "Dry-run (would delete)"
    for path in removed:
        print(f"{action}: {path}")


if __name__ == "__main__":
    main()
