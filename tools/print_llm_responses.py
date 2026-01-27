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
    summaries_dir = root / run_id / "stage_1" / "entry_graph_summaries"
    files = [str(p) for p in summaries_dir.rglob("*.parquet")]
    if not files:
        raise SystemExit("entry_graph_summaries not found. Rerun parser with LLM enabled.")
    con = duckdb.connect()
    cols = [
        col[0]
        for col in con.execute(
            "describe select * from read_parquet(?::VARCHAR[])", [files]
        ).fetchall()
    ]
    if "llm_response" not in cols:
        raise SystemExit(
            "llm_response column missing. Enable entry_graph_llm_store_response and rerun parser."
        )
    rows = con.execute(
        "select entry_key, llm_response from read_parquet(?::VARCHAR[]) "
        "where llm_response is not null",
        [files],
    ).fetchall()
    if not rows:
        raise SystemExit("No llm_response rows found. Enable entry_graph_llm_store_response.")
    for entry_key, response in rows:
        print(f"entry_key={entry_key}")
        try:
            payload = json.loads(response)
            print(json.dumps(payload, indent=2, ensure_ascii=True))
        except json.JSONDecodeError:
            print(response)
        print("---")


if __name__ == "__main__":
    main()
