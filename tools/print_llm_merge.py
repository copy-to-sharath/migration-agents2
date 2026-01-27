from __future__ import annotations

import json
from pathlib import Path

import duckdb


def main() -> None:
    root = Path("data/parquet")
    latest_path = root / "LATEST_RUN"
    if not latest_path.exists():
        raise SystemExit("LATEST_RUN not found. Run ingestion/parser first.")
    run_id = latest_path.read_text(encoding="utf-8").strip()
    merged_dir = root / run_id / "stage_1" / "entry_graph_summaries_merged"
    files = [str(p) for p in merged_dir.rglob("*.parquet")]
    if not files:
        raise SystemExit("Merged summaries not found. Enable entry_graph_llm_merge_enabled and rerun.")
    con = duckdb.connect()
    row = con.execute(
        "select * from read_parquet(?::VARCHAR[]) limit 1",
        [files],
    ).fetchone()
    cols = [col[0] for col in con.execute("describe select * from read_parquet(?::VARCHAR[])", [files]).fetchall()]
    record = dict(zip(cols, row))
    print(json.dumps(record, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
