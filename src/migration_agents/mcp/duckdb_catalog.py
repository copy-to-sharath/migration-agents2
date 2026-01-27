"""DuckDB catalog management with per-run database files.

Each pipeline run gets its own DuckDB file, eliminating view refresh issues.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import duckdb

NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def get_latest_run_id(parquet_root: Path) -> Optional[str]:
    """Read the latest run ID from the LATEST_RUN file."""
    latest_run_file = parquet_root / "LATEST_RUN"
    if latest_run_file.exists():
        return latest_run_file.read_text(encoding="utf-8").strip()
    return None


def connect_duckdb(duckdb_path: Path) -> duckdb.DuckDBPyConnection:
    """Connect to DuckDB database, creating directory if needed."""
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(duckdb_path))


def connect_for_run(duckdb_dir: Path, parquet_root: Path) -> tuple[duckdb.DuckDBPyConnection, str | None]:
    """Connect to the DuckDB database for the latest run.
    
    Args:
        duckdb_dir: Directory for DuckDB files (each run gets its own file)
        parquet_root: Root directory containing parquet files and LATEST_RUN
    
    Returns:
        Tuple of (connection, run_id)
    """
    run_id = get_latest_run_id(parquet_root)
    
    if not run_id:
        # No run yet - use in-memory database
        return duckdb.connect(":memory:"), None
    
    # Create run-specific database file
    duckdb_dir = Path(duckdb_dir)
    duckdb_dir.mkdir(parents=True, exist_ok=True)
    db_path = duckdb_dir / f"{run_id}.duckdb"
    
    is_new_db = not db_path.exists()
    conn = connect_duckdb(db_path)
    
    if is_new_db:
        register_parquet_views(conn, parquet_root, run_id)
    
    return conn, run_id


def should_refresh_views(parquet_root: Path, current_run_id: Optional[str]) -> tuple[bool, Optional[str]]:
    """Check if we need to switch to a new run's database.
    
    Returns:
        Tuple of (needs_switch, new_run_id)
    """
    latest_run_id = get_latest_run_id(parquet_root)
    if latest_run_id != current_run_id:
        return True, latest_run_id
    return False, current_run_id


def register_parquet_views(
    conn: duckdb.DuckDBPyConnection, 
    parquet_root: Path, 
    run_id: Optional[str] = None
) -> list[str]:
    """Register DuckDB views for parquet files from a specific run.
    
    Args:
        conn: DuckDB connection
        parquet_root: Root directory for parquet files
        run_id: Specific run ID to register views for (uses latest if None)
    
    Returns:
        List of registered view names
    """
    views: list[str] = []
    if not parquet_root.exists():
        return views
    
    if run_id is None:
        run_id = get_latest_run_id(parquet_root)
    
    if not run_id:
        return views
    
    run_path = parquet_root / run_id
    if not run_path.exists():
        return views
    
    table_files: dict[str, list[str]] = {}
    for parquet_file in run_path.rglob("*.parquet"):
        name = _table_name_from_parquet(run_path, parquet_file)
        if name and NAME_RE.match(name):
            table_files.setdefault(name, []).append(str(parquet_file))
    
    for view_name, files in sorted(table_files.items()):
        if not files:
            continue
        sql_files = _sql_string_list(sorted(files))
        conn.execute(
            f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM read_parquet({sql_files})"
        )
        views.append(view_name)
    
    return views


def _table_name_from_parquet(run_root: Path, parquet_file: Path) -> str | None:
    """Extract table name from parquet file path."""
    try:
        relative = parquet_file.relative_to(run_root)
    except ValueError:
        return None
    
    parts = relative.parts
    for idx, part in enumerate(parts):
        if "=" in part:
            if idx == 0:
                return None
            return parts[idx - 1]
    
    if len(parts) >= 2:
        return parts[-2]
    return None


def _sql_string_list(paths: list[str]) -> str:
    """Convert list of paths to SQL array literal."""
    escaped = [path.replace("'", "''") for path in paths]
    quoted = ", ".join(f"'{path}'" for path in escaped)
    return f"[{quoted}]"


def get_run_connection(
    parquet_root: Path | str,
    run_id: str | None = None,
    duckdb_dir: Path | str | None = None,
) -> tuple[duckdb.DuckDBPyConnection, str | None]:
    """Get a DuckDB connection for a specific run.
    
    Each run_id gets its own DuckDB file to avoid view conflicts.
    This is the preferred way to get a DuckDB connection.
    
    Args:
        parquet_root: Root directory containing parquet files
        run_id: Specific run ID (uses latest if None)
        duckdb_dir: Directory for DuckDB files (default: data/duckdb)
    
    Returns:
        Tuple of (connection, run_id)
    
    Example:
        conn, run_id = get_run_connection(Path("data/parquet"))
        try:
            result = conn.execute("SELECT * FROM symbols LIMIT 10").fetchdf()
        finally:
            conn.close()
    """
    from migration_agents.constants import DEFAULT_PATHS
    
    parquet_root = Path(parquet_root)
    duckdb_dir = Path(duckdb_dir) if duckdb_dir else DEFAULT_PATHS.DUCKDB_DIR
    
    # Get run_id if not provided
    if run_id is None:
        run_id = get_latest_run_id(parquet_root)
    
    if not run_id:
        # No run yet - use in-memory database
        conn = duckdb.connect(":memory:")
        return conn, None
    
    # Use run-specific database file
    db_path = duckdb_dir / f"{run_id}.duckdb"
    is_new_db = not db_path.exists()
    
    conn = connect_duckdb(db_path)
    
    # Register views for new databases
    if is_new_db:
        register_parquet_views(conn, parquet_root, run_id)
    
    return conn, run_id

