from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb

from migration_agents.constants import DEFAULT_PATHS
from migration_agents.ingestion.parquet_writer import write_parquet


@dataclass(frozen=True)
class CoverageRow:
    language: str
    symbols: int
    calls: int
    conditions: int
    data_access: int
    calls_per_symbol: float
    conditions_per_symbol: float
    data_access_per_symbol: float


def build_summary(parquet_root: Path) -> tuple[str, int, str, list[CoverageRow]]:
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    con, _ = get_run_connection(parquet_root)
    try:
        return _build_summary_impl(con, parquet_root)
    finally:
        con.close()


def _build_summary_impl(con, parquet_root: Path) -> tuple[str, int, str, list[CoverageRow]]:
    parse_audit_files = _table_files(parquet_root, "parse_audit")
    if not parse_audit_files:
        return "", 0, "", []
    con.execute(
        f"create or replace view parse_audit as select * from read_parquet({_sql_string_list(parse_audit_files)})"
    )
    latest = con.execute(
        """
        select run_id, artifact_version, created_at
        from parse_audit
        qualify row_number() over (order by created_at desc) = 1
        """
    ).fetchone()
    if latest is None:
        return "", 0, "", []
    run_id, artifact_version, created_at = latest

    def load(table: str) -> None:
        files = _table_files(parquet_root, table)
        if not files:
            con.execute(f"create or replace view {table} as select * from (select * where false)")
            return
        con.execute(
            f"create or replace view {table} as select * from read_parquet({_sql_string_list(files)})"
        )

    for table in ["symbols", "calls", "conditions", "data_access"]:
        load(table)

    df = con.execute(
        """
        with scoped as (
            select file_path, language
            from parse_audit
            where run_id = ? and artifact_version = ?
        ),
        symbols as (
            select s.file_path, count(*) as cnt
            from symbols s
            join scoped a on a.file_path = s.file_path
            group by s.file_path
        ),
        calls as (
            select s.file_path, count(*) as cnt
            from calls s
            join scoped a on a.file_path = s.file_path
            group by s.file_path
        ),
        conditions as (
            select s.file_path, count(*) as cnt
            from conditions s
            join scoped a on a.file_path = s.file_path
            group by s.file_path
        ),
        data_access as (
            select s.file_path, count(*) as cnt
            from data_access s
            join scoped a on a.file_path = s.file_path
            group by s.file_path
        )
        select
            a.language,
            coalesce(sum(sym.cnt), 0) as symbols,
            coalesce(sum(ca.cnt), 0) as calls,
            coalesce(sum(co.cnt), 0) as conditions,
            coalesce(sum(da.cnt), 0) as data_access
        from scoped a
        left join symbols sym on sym.file_path = a.file_path
        left join calls ca on ca.file_path = a.file_path
        left join conditions co on co.file_path = a.file_path
        left join data_access da on da.file_path = a.file_path
        group by a.language
        order by symbols desc
        """,
        [run_id, artifact_version],
    ).fetchall()

    rows: list[CoverageRow] = []
    for language, symbols, calls, conditions, data_access in df:
        symbols = int(symbols)
        calls = int(calls)
        conditions = int(conditions)
        data_access = int(data_access)
        denom = symbols if symbols > 0 else 1
        rows.append(
            CoverageRow(
                language=language,
                symbols=symbols,
                calls=calls,
                conditions=conditions,
                data_access=data_access,
                calls_per_symbol=calls / denom,
                conditions_per_symbol=conditions / denom,
                data_access_per_symbol=data_access / denom,
            )
        )
    created_at = created_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return run_id, int(artifact_version), created_at, rows


def _table_files(parquet_root: Path, table: str) -> list[str]:
    return sorted(str(path) for path in parquet_root.rglob(f"{table}/**/*.parquet"))


def _sql_string_list(paths: list[str]) -> str:
    escaped = [path.replace("'", "''") for path in paths]
    quoted = ", ".join(f"'{path}'" for path in escaped)
    return f"[{quoted}]"


def generate_coverage_summary(parquet_root: Path) -> bool:
    run_id, artifact_version, created_at, rows = build_summary(parquet_root)
    if not rows:
        return False
    existing = _existing_languages(parquet_root, run_id, artifact_version)
    if existing:
        rows = [row for row in rows if row.language not in existing]
    if not rows:
        return False
    output_rows = []
    for row in rows:
        record = asdict(row)
        record["run_id"] = run_id
        record["artifact_version"] = artifact_version
        record["slice_id"] = None
        record["created_at"] = created_at
        record["supersedes_version"] = None
        record["source_ref"] = "parse_audit"
        output_rows.append(record)
    write_parquet(
        parquet_root,
        "coverage_summary",
        output_rows,
        partition_cols=["run_id", "artifact_version"],
    )
    return True


def _existing_languages(parquet_root: Path, run_id: str, artifact_version: int) -> set[str]:
    files = sorted(str(path) for path in parquet_root.rglob("coverage_summary/**/*.parquet"))
    if not files:
        return set()
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    con, _ = get_run_connection(parquet_root, run_id)
    try:
        # Check if 'language' column exists (parser coverage format)
        rows = con.execute(
            """
            select distinct language
            from read_parquet(?::VARCHAR[])
            where run_id = ? and artifact_version = ? and language is not null
            """,
            [files, run_id, artifact_version],
        ).fetchall()
        return {row[0] for row in rows}
    except Exception:
        # Different schema (stage/metric format from ingestion/slice)
        return set()
    finally:
        con.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate coverage summary parquet.")
    parser.add_argument("--parquet-root", type=Path, default=DEFAULT_PATHS.PARQUET_ROOT)
    args = parser.parse_args()
    generate_coverage_summary(args.parquet_root)


if __name__ == "__main__":
    main()
