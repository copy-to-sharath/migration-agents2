"""
DuckDB Helper with Schema Hints for Migration Agents.

This module provides schema-aware DuckDB queries to prevent column name errors.
Always use these helpers instead of raw DuckDB queries.
"""

import duckdb
import json
from pathlib import Path
from typing import Any
from migration_agents.constants import DEFAULT_PARQUET_ROOT

# Schema definitions for all parquet tables
# Use these column names to avoid errors!
PARQUET_SCHEMAS = {
    "step_1": {
        "intake_source_chunks": [
            "file_path", "line_start", "line_end", "content", "checksum",
            "source_ref", "slice_id", "created_at", "supersedes_version", 
            "artifact_version", "run_id"
        ],
        "intake_source_index": [
            "file_path", "language", "loc", "module", "checksum",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
    },
    "step_2": {
        "calls": [
            "caller_id",  # symbol_id of the caller
            "callee_id",  # symbol_id of the callee (join with symbols.symbol_id)
            "file_path", "line", "source_ref", "slice_id", "created_at",
            "supersedes_version", "artifact_version", "run_id"
        ],
        "code_graph_edges": [
            "from_id", "to_id", "edge_type", "file_path", "line",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "code_graph_nodes": [
            "node_id", "node_type", "symbol_id", "table_name", "label",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "conditions": [
            "symbol_id", "predicate", "file_path", "line",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "constants": [
            "name", "value", "file_path", "line",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "data_access": [
            "symbol_id",
            "table_name",  # database table being accessed
            "op",          # operation: select, insert, update, delete
            "sql_text",    # SQL snippet
            "file_path", "line", "source_ref", "slice_id", "created_at",
            "supersedes_version", "artifact_version", "run_id"
        ],
        "entry_exit_map": [
            "entry_node_id", "exit_node_id", "effect_type",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "entry_graph_processing_summary": [
            "total_candidates", "processed_count", "skipped_count",
            "pending_count", "excluded_count", "processed_keys",
            "pending_keys", "skipped_keys", "excluded_keys",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "entry_graph_state": [
            "entry_key", "entry_type", "status", "reason", "metrics",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "entry_graphs": [
            "entry_key",           # same as symbol_id
            "entry_type",          # 'entry' or 'exit'
            "entry_nodes",         # JSON array
            "reachable_nodes",     # JSON array
            "reachable_edges",     # JSON array
            "metrics",             # JSON with max_depth, etc.
            "capped_depth",        # numeric depth (use this!)
            "normalized_depth",
            "log_scaled_depth",
            "depth_breadth",
            "reachable_nodes_count",
            "edge_count",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "graph_metadata": [
            "node_id", "degree", "pagerank", "community_id",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "parse_audit": [
            "file_path", "language", "method", "status", "reason",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "parse_missed": [
            "file_path", "language", "method", "status", "reason",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "symbols": [
            "symbol_id",   # unique identifier
            "name",        # symbol name (class, method, etc.)
            "kind",        # 'class', 'method', 'ctor', 'property_name', etc.
            "signature",   # full signature
            "file_path",   # source file path
            "line",        # line number
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
    },
    "step_3": {
        "slice_context": [
            "slice_id",
            "summary",      # text summary of the slice
            "risks",        # identified risks
            "assumptions",  # assumptions made
            "source_ref", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "slice_manifest": [
            "slice_id",
            "file_path",
            "symbol_id",
            "table_name",    # related database table
            "external_ref",
            "source_ref", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "slice_source_refs": [
            "slice_id",
            "file_path",
            "line",
            "excerpt",       # code excerpt
            "source_ref", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
    },
    "step_4": {
        "logic_edges": [
            "rule_id", "symbol_id", "file_path", "line", "evidence",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "logic_rules": [
            "rule_id",
            "slice_id",
            "rule_text",     # the business rule text
            "inputs",        # JSON array
            "outputs",       # JSON array
            "invariants",    # JSON array
            "source_ref", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
        "trace_map": [
            "rule_id", "file_path", "line", "rationale",
            "source_ref", "slice_id", "created_at", "supersedes_version",
            "artifact_version", "run_id"
        ],
    },
    "step_9": {
        "codegen_manifest": [
            "slice_id", "path", "kind", "framework",
            "created_at", "supersedes_version", "artifact_version", "run_id"
        ],
    },
}


def get_schema_hint(stage: str, table: str) -> str:
    """Get a schema hint string for a table."""
    if stage in PARQUET_SCHEMAS and table in PARQUET_SCHEMAS[stage]:
        cols = PARQUET_SCHEMAS[stage][table]
        return f"-- {table} columns: {', '.join(cols)}"
    return f"-- Unknown table: {stage}/{table}"


def get_table_path(base: str, stage: str, table: str) -> str:
    """Get the parquet path for a table."""
    return f"{base}/{stage}/{table}/**/*.parquet"


class DuckDBHelper:
    """Schema-aware DuckDB helper for migration agents."""
    
    def __init__(self, parquet_base: str, run_id: str | None = None):
        self.base = parquet_base
        self.run_id = run_id
        # Use run-specific database file
        from migration_agents.mcp.duckdb_catalog import get_run_connection
        parquet_root = Path(parquet_base).parent if run_id else Path(parquet_base)
        self.conn, _ = get_run_connection(parquet_root, run_id)
        self._register_views()
    
    def close(self) -> None:
        """Close the DuckDB connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self) -> "DuckDBHelper":
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def _register_views(self):
        """Register all parquet tables as views."""
        for stage, tables in PARQUET_SCHEMAS.items():
            stage_path = Path(self.base) / stage
            if stage_path.exists():
                for table in tables:
                    table_path = stage_path / table
                    if table_path.exists():
                        path = get_table_path(self.base, stage, table)
                        try:
                            self.conn.execute(
                                f"CREATE OR REPLACE VIEW {table} AS "
                                f"SELECT * FROM read_parquet('{path}')"
                            )
                        except Exception:
                            pass  # Table might not have data
    
    def query(self, sql: str) -> list[tuple]:
        """Execute a query and return results."""
        return self.conn.execute(sql).fetchall()
    
    def query_df(self, sql: str):
        """Execute a query and return a DataFrame."""
        return self.conn.execute(sql).df()
    
    # ============================================
    # Pre-built queries with correct column names
    # ============================================
    
    def get_all_symbols(self, kind: str | None = None) -> list[dict]:
        """Get all symbols, optionally filtered by kind."""
        sql = "SELECT symbol_id, name, kind, signature, file_path, line FROM symbols"
        if kind:
            sql += f" WHERE kind = '{kind}'"
        rows = self.query(sql)
        return [
            {"symbol_id": r[0], "name": r[1], "kind": r[2], 
             "signature": r[3], "file_path": r[4], "line": r[5]}
            for r in rows
        ]
    
    def get_aspx_pages(self) -> list[dict]:
        """Get all ASPX code-behind pages with their depth."""
        sql = """
            SELECT 
                s.symbol_id, s.name, s.kind, s.file_path, s.line,
                e.capped_depth, e.metrics
            FROM symbols s
            LEFT JOIN entry_graphs e ON s.symbol_id = e.entry_key
            WHERE s.file_path LIKE '%.aspx.cs'
            ORDER BY e.capped_depth, s.name
        """
        rows = self.query(sql)
        return [
            {"symbol_id": r[0], "name": r[1], "kind": r[2],
             "file_path": r[3], "line": r[4], "depth": r[5] or 0,
             "metrics": r[6]}
            for r in rows
        ]
    
    def get_data_access_patterns(self) -> list[dict]:
        """Get data access patterns (table operations)."""
        sql = """
            SELECT table_name, op, COUNT(*) as cnt
            FROM data_access
            WHERE table_name IS NOT NULL AND table_name != ''
            GROUP BY table_name, op
            ORDER BY cnt DESC
        """
        rows = self.query(sql)
        return [{"table": r[0], "operation": r[1], "count": r[2]} for r in rows]
    
    def get_call_patterns(self, limit: int = 50) -> list[dict]:
        """Get method call patterns."""
        sql = f"""
            SELECT s.name, s.kind, COUNT(*) as cnt
            FROM calls c
            JOIN symbols s ON c.callee_id = s.symbol_id
            GROUP BY s.name, s.kind
            ORDER BY cnt DESC
            LIMIT {limit}
        """
        rows = self.query(sql)
        return [{"name": r[0], "kind": r[1], "call_count": r[2]} for r in rows]
    
    def get_slices(self) -> list[dict]:
        """Get all slices from the manifest."""
        sql = """
            SELECT slice_id, file_path, symbol_id, table_name, external_ref
            FROM slice_manifest
        """
        rows = self.query(sql)
        return [
            {"slice_id": r[0], "file_path": r[1], "symbol_id": r[2],
             "table_name": r[3], "external_ref": r[4]}
            for r in rows
        ]
    
    def get_slice_contexts(self) -> list[dict]:
        """Get slice contexts with summaries."""
        sql = """
            SELECT slice_id, summary, risks, assumptions
            FROM slice_context
        """
        rows = self.query(sql)
        return [
            {"slice_id": r[0], "summary": r[1], "risks": r[2], "assumptions": r[3]}
            for r in rows
        ]
    
    def get_logic_rules(self) -> list[dict]:
        """Get extracted logic rules."""
        sql = """
            SELECT rule_id, slice_id, rule_text, inputs, outputs, invariants
            FROM logic_rules
        """
        rows = self.query(sql)
        return [
            {"rule_id": r[0], "slice_id": r[1], "rule_text": r[2],
             "inputs": r[3], "outputs": r[4], "invariants": r[5]}
            for r in rows
        ]
    
    def get_entry_graphs(self) -> list[dict]:
        """Get entry graphs with depth info."""
        sql = """
            SELECT entry_key, entry_type, capped_depth, normalized_depth,
                   reachable_nodes_count, edge_count, metrics
            FROM entry_graphs
        """
        rows = self.query(sql)
        return [
            {"entry_key": r[0], "entry_type": r[1], "depth": r[2],
             "normalized_depth": r[3], "node_count": r[4], "edge_count": r[5],
             "metrics": r[6]}
            for r in rows
        ]
    
    def get_depth_distribution(self) -> dict[int, int]:
        """Get distribution of endpoints by depth level."""
        sql = """
            SELECT CAST(capped_depth AS INTEGER) as depth, COUNT(*) as cnt
            FROM entry_graphs
            WHERE capped_depth IS NOT NULL
            GROUP BY CAST(capped_depth AS INTEGER)
            ORDER BY depth
        """
        rows = self.query(sql)
        return {r[0]: r[1] for r in rows}
    
    def get_conditions(self, limit: int = 100) -> list[dict]:
        """Get business conditions/predicates."""
        sql = f"""
            SELECT symbol_id, predicate, file_path, line
            FROM conditions
            LIMIT {limit}
        """
        rows = self.query(sql)
        return [
            {"symbol_id": r[0], "predicate": r[1], "file_path": r[2], "line": r[3]}
            for r in rows
        ]
    
    def get_constants(self) -> list[dict]:
        """Get defined constants."""
        sql = """
            SELECT name, value, file_path, line
            FROM constants
        """
        rows = self.query(sql)
        return [
            {"name": r[0], "value": r[1], "file_path": r[2], "line": r[3]}
            for r in rows
        ]


def get_latest_run(parquet_root: str = DEFAULT_PARQUET_ROOT) -> str | None:
    """Get the latest run directory."""
    latest_file = Path(parquet_root) / "LATEST_RUN"
    if latest_file.exists():
        return latest_file.read_text().strip()
    
    # Fall back to finding the most recent run_* directory
    runs = sorted(Path(parquet_root).glob("run_*"), reverse=True)
    if runs:
        return runs[0].name
    return None


def create_helper(parquet_root: str = DEFAULT_PARQUET_ROOT) -> DuckDBHelper | None:
    """Create a DuckDBHelper for the latest run."""
    latest = get_latest_run(parquet_root)
    if latest:
        base = f"{parquet_root}/{latest}"
        return DuckDBHelper(base, run_id=latest)
    return None
