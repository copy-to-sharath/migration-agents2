from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MCPDuckDBClient:
    url: str

    def query(self, sql: str) -> list[dict[str, Any]]:
        payload = json.dumps({"sql": sql}).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.load(response)
        if isinstance(data, dict) and "rows" in data:
            return data["rows"]
        if isinstance(data, list):
            return data
        raise ValueError("Unexpected MCP response format")


@dataclass(frozen=True)
class MCPStdIOClient:
    command: list[str]

    def query(self, sql: str) -> list[dict[str, Any]]:
        request_id = 1
        with subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as proc:
            assert proc.stdin is not None
            assert proc.stdout is not None
            init = {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}}
            proc.stdin.write(json.dumps(init) + "\n")
            proc.stdin.flush()
            proc.stdout.readline()
            call = {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": "tools/call",
                "params": {"name": "duckdb_query", "arguments": {"sql": sql}},
            }
            proc.stdin.write(json.dumps(call) + "\n")
            proc.stdin.flush()
            response = json.loads(proc.stdout.readline())
            if "result" in response:
                return response["result"].get("content", [])
            raise ValueError(response.get("error", {}).get("message", "MCP error"))


@dataclass
class DirectDuckDBClient:
    """Direct DuckDB client for querying parquet files without MCP server.
    
    Supports both full and incremental modes:
    - Full mode: Uses latest run directory
    - Incremental mode: Use specific run_id if provided
    """
    parquet_root: str
    run_id: str | None = None  # If None, uses latest run
    _conn: Any = None
    _initialized: bool = False

    def _get_run_dir(self) -> Path:
        """Get the appropriate run directory based on mode."""
        from pathlib import Path
        parquet_root = Path(self.parquet_root)
        
        if self.run_id:
            # Incremental mode: use specific run
            run_dir = parquet_root / self.run_id
            if run_dir.exists():
                return run_dir
        
        # Full mode or fallback: use latest run
        run_dirs = sorted(parquet_root.glob("run_*"))
        if run_dirs:
            return run_dirs[-1]
        
        raise FileNotFoundError(f"No run directories found in {parquet_root}")

    def _initialize_views(self, conn: Any, run_dir: Path) -> None:
        """Register views for all known tables."""
        import glob
        
        # All known table patterns for steps 1-9
        table_patterns = [
            # Step 1: Ingestion
            ("intake_source_index", "step_1/intake_source_index/**/*.parquet"),
            ("intake_source_chunks", "step_1/intake_source_chunks/**/*.parquet"),
            # Step 2: Parser
            ("symbols", "step_2/symbols/**/*.parquet"),
            ("calls", "step_2/calls/**/*.parquet"),
            ("conditions", "step_2/conditions/**/*.parquet"),
            ("constants", "step_2/constants/**/*.parquet"),
            ("data_access", "step_2/data_access/**/*.parquet"),
            ("code_graph_nodes", "step_2/code_graph_nodes/**/*.parquet"),
            ("code_graph_edges", "step_2/code_graph_edges/**/*.parquet"),
            ("graph_metadata", "step_2/graph_metadata/**/*.parquet"),
            ("entry_graphs", "step_2/entry_graphs/**/*.parquet"),
            ("entry_exit_map", "step_2/entry_exit_map/**/*.parquet"),
            ("parse_audit", "step_2/parse_audit/**/*.parquet"),
            # Step 3: Slice Extractor
            ("slice_manifest", "step_3/slice_manifest/**/*.parquet"),
            ("slice_context", "step_3/slice_context/**/*.parquet"),
            ("slice_source_refs", "step_3/slice_source_refs/**/*.parquet"),
            # Step 4: Logic Manifester
            ("logic_rules", "step_4/logic_rules/**/*.parquet"),
            ("logic_edges", "step_4/logic_edges/**/*.parquet"),
            ("trace_map", "step_4/trace_map/**/*.parquet"),
            # Step 9: Codegen
            ("codegen_manifest", "step_9/codegen_manifest/**/*.parquet"),
            ("code_artifacts", "step_9/code_artifacts/**/*.parquet"),
        ]
        
        for table_name, pattern in table_patterns:
            full_pattern = str(run_dir / pattern)
            files = glob.glob(full_pattern, recursive=True)
            if files:
                try:
                    conn.execute(f"""
                        CREATE OR REPLACE VIEW {table_name} AS 
                        SELECT * FROM read_parquet('{full_pattern}', hive_partitioning=true)
                    """)
                except Exception:
                    pass  # Table might not exist yet

    def query(self, sql: str) -> list[dict[str, Any]]:
        from migration_agents.mcp.duckdb_catalog import get_run_connection
        
        try:
            run_dir = self._get_run_dir()
            run_id = run_dir.name if run_dir else None
            conn, _ = get_run_connection(self.parquet_root, run_id)
            try:
                self._initialize_views(conn, run_dir)
                result = conn.execute(sql).fetchdf()
                return result.to_dict(orient="records")
            finally:
                conn.close()
        except FileNotFoundError:
            return []


def get_mcp_client(
    run_id: str | None = None,
    parquet_root: str | None = None,
) -> MCPDuckDBClient | MCPStdIOClient | DirectDuckDBClient:
    """Get an MCP client for querying data.
    
    Args:
        run_id: Optional specific run_id for incremental mode
        parquet_root: Optional parquet root directory override
    
    Returns:
        An MCP client instance
    """
    command = os.environ.get("MCP_SERVER_CMD")
    if command:
        return MCPStdIOClient(command=command.split(" "))
    url = os.environ.get("MCP_DUCKDB_URL")
    if url:
        return MCPDuckDBClient(url=url)
    
    # Use DirectDuckDBClient for parquet-based queries
    root = parquet_root or os.environ.get("PARQUET_ROOT", "data/parquet")
    env_run_id = os.environ.get("RUN_ID")  # Allow run_id from env
    effective_run_id = run_id or env_run_id
    
    if os.path.exists(root):
        return DirectDuckDBClient(parquet_root=root, run_id=effective_run_id)
    raise RuntimeError("MCP_SERVER_CMD, MCP_DUCKDB_URL, or valid PARQUET_ROOT required for queries")
