from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

from migration_agents.constants import DEFAULT_PATHS


def main() -> None:
    parser = argparse.ArgumentParser(description="Print coverage summary from parquet.")
    parser.add_argument("--parquet-root", type=Path, default=DEFAULT_PATHS.PARQUET_ROOT)
    args = parser.parse_args()
    parquet_root = args.parquet_root
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    con, _ = get_run_connection(parquet_root)
    try:
        _run_coverage_report(con, parquet_root)
    finally:
        con.close()


def _run_coverage_report(con, parquet_root: Path) -> None:
    path = str(parquet_root / "coverage_summary" / "**" / "*.parquet")
    con.execute(f"create or replace view coverage_summary as select * from read_parquet('{path}')")
    latest = con.execute(
        """
        select run_id, artifact_version
        from coverage_summary
        qualify row_number() over (order by created_at desc) = 1
        """
    ).fetchone()
    if latest is None:
        print("coverage_summary_empty=1")
        return
    run_id, artifact_version = latest
    rows = con.execute(
        """
        select
            language,
            symbols,
            calls,
            conditions,
            data_access,
            round(calls_per_symbol, 4) as calls_per_symbol,
            round(conditions_per_symbol, 4) as conditions_per_symbol,
            round(data_access_per_symbol, 4) as data_access_per_symbol
        from coverage_summary
        where run_id = ? and artifact_version = ?
        order by symbols desc
        """,
        [run_id, artifact_version],
    ).fetchall()
    print(f"coverage_summary_run_id={run_id}")
    print(f"coverage_summary_artifact_version={artifact_version}")
    for row in rows:
        (
            language,
            symbols,
            calls,
            conditions,
            data_access,
            calls_per_symbol,
            conditions_per_symbol,
            data_access_per_symbol,
        ) = row
        print(
            "coverage_summary_row "
            f"language={language} "
            f"symbols={int(symbols)} "
            f"calls={int(calls)} "
            f"conditions={int(conditions)} "
            f"data_access={int(data_access)} "
            f"calls_per_symbol={calls_per_symbol} "
            f"conditions_per_symbol={conditions_per_symbol} "
            f"data_access_per_symbol={data_access_per_symbol}"
        )


if __name__ == "__main__":
    main()
