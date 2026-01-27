#!/usr/bin/env python3
"""
Split entry graph keys into depth buckets for staged Domain Architect runs.

Reads entry graphs parquet for the latest run (or a provided run_id), inspects
metrics.max_depth, and writes per-bucket entry key lists under
generated/depth_buckets/<run_id>/.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Tuple

import duckdb


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bucket entry graph keys by max_depth for staged processing."
    )
    parser.add_argument(
        "--run-id",
        dest="run_id",
        help="Run id to use (default: contents of data/parquet/LATEST_RUN)",
    )
    parser.add_argument(
        "--buckets",
        nargs="+",
        type=int,
        default=[0, 3, 5, 8, 9999],
        help="Depth cut points (inclusive lower bounds; last value is upper bound). "
        "Example: 0 3 5 8 9999 -> [0-2], [3-4], [5-7], [8+]",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("generated/depth_buckets"),
        help="Output directory root for bucket files.",
    )
    parser.add_argument(
        "--parquet",
        type=Path,
        help="Override entry_graphs parquet path (otherwise derived from run_id).",
    )
    return parser.parse_args()


def load_run_id(run_id: str | None) -> str:
    if run_id:
        return run_id
    latest = Path("data/parquet/LATEST_RUN")
    if latest.exists():
        return latest.read_text().strip()
    raise SystemExit("Could not find run_id (data/parquet/LATEST_RUN missing).")


def bucket_labels(cuts: List[int]) -> List[Tuple[int, int, str]]:
    if len(cuts) < 2:
        raise ValueError("Provide at least two bucket cut points")
    buckets: List[Tuple[int, int, str]] = []
    for i in range(len(cuts) - 1):
        low, high = cuts[i], cuts[i + 1]
        label = f"depth_{low}_to_{high-1}" if high != cuts[-1] else f"depth_ge_{low}"
        buckets.append((low, high, label))
    return buckets


def read_entry_depths(parquet_path: Path) -> Iterable[Tuple[str, float]]:
    con = duckdb.connect()
    rows = con.execute(
        "select entry_key, metrics from read_parquet(?)", [str(parquet_path)]
    ).fetchall()
    for entry_key, metrics_raw in rows:
        if not entry_key or not metrics_raw:
            continue
        try:
            metrics = json.loads(metrics_raw)
            depth = float(metrics.get("max_depth", 0.0))
        except Exception:
            continue
        yield entry_key, depth


def main() -> None:
    args = parse_args()
    run_id = load_run_id(args.run_id)
    parquet_path = (
        args.parquet
        if args.parquet
        else Path(
            f"data/parquet/{run_id}/stage_1/entry_graphs/"
            f"run_id={run_id}/artifact_version=1/entry_graphs-0.parquet"
        )
    )
    if not parquet_path.exists():
        raise SystemExit(f"Parquet not found: {parquet_path}")

    cuts = args.buckets
    buckets = bucket_labels(cuts)

    entries_by_bucket: dict[str, list[str]] = {label: [] for _, _, label in buckets}
    for entry_key, depth in read_entry_depths(parquet_path):
        for low, high, label in buckets:
            if low <= depth < high:
                entries_by_bucket[label].append(entry_key)
                break

    out_root = args.output_dir / run_id
    out_root.mkdir(parents=True, exist_ok=True)
    for label, keys in entries_by_bucket.items():
        out_file = out_root / f"{label}.txt"
        out_file.write_text("\n".join(keys))
        print(f"{label}: {len(keys)} -> {out_file}")


if __name__ == "__main__":
    main()
