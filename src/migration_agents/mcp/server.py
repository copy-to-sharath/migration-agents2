from __future__ import annotations

from pathlib import Path
from typing import Any

from .agent_tools import AGENT_TOOLS, AgentToolHandler
from .config import MCPConfig, load_config
from .duckdb_catalog import (
    connect_for_run,
    register_parquet_views,
    should_refresh_views,
)
from .jsonrpc import JsonRpcRequest, run_stdio, write_error, write_result


class MCPServer:
    def __init__(self, config: MCPConfig) -> None:
        self.config = config
        # Connect to run-specific DuckDB file
        self.conn, self.run_id = connect_for_run(config.duckdb_dir, config.parquet_root)
        self.views = self._get_views()
        self.agent_handler = AgentToolHandler(self.conn, config)

    def _get_views(self) -> list[str]:
        """Get list of current view names."""
        try:
            result = self.conn.execute("SELECT name FROM (SHOW TABLES)").fetchall()
            return [row[0] for row in result]
        except Exception:
            return []

    def _ensure_views_fresh(self) -> None:
        """Switch to new run's database if run ID changed."""
        needs_switch, new_run_id = should_refresh_views(self.config.parquet_root, self.run_id)
        if needs_switch and new_run_id:
            # Close old connection and switch to new run's database
            self.conn.close()
            self.conn, self.run_id = connect_for_run(self.config.duckdb_dir, self.config.parquet_root)
            self.views = self._get_views()
            self.agent_handler = AgentToolHandler(self.conn, self.config)

    def handle(self, request: JsonRpcRequest) -> None:
        method = request.method
        params = request.params or {}
        if method == "initialize":
            write_result(
                request.id,
                {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "migration-agents-mcp", "version": "0.2.0"},
                    "capabilities": {"tools": {}, "resources": {}},
                },
            )
            return
        if method == "tools/list":
            # Combine duckdb_query with agent tools
            all_tools = [
                {
                    "name": "duckdb_query",
                    "description": "Execute a DuckDB SQL query over Parquet-backed views.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"sql": {"type": "string"}},
                        "required": ["sql"],
                    },
                }
            ] + AGENT_TOOLS
            write_result(request.id, {"tools": all_tools})
            return
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            # Ensure views are fresh before any tool call
            self._ensure_views_fresh()
            
            # Handle duckdb_query
            if name == "duckdb_query":
                sql = arguments.get("sql")
                if not isinstance(sql, str) or not sql.strip():
                    write_error(request.id, -32602, "Missing sql")
                    return
                try:
                    result = self._query(sql)
                except Exception as exc:
                    write_error(request.id, -32000, str(exc))
                    return
                # MCP spec requires content to be a list of content items
                import json as _json
                content_items = [{"type": "text", "text": _json.dumps(result, indent=2, default=str)}]
                write_result(request.id, {"content": content_items})
                return
            
            # Handle agent tools
            agent_tool_names = [t["name"] for t in AGENT_TOOLS]
            if name in agent_tool_names:
                try:
                    result = self.agent_handler.handle_tool(name, arguments)
                except Exception as exc:
                    write_error(request.id, -32000, str(exc))
                    return
                # MCP spec requires content to be a list of content items
                import json as _json
                content_items = [{"type": "text", "text": _json.dumps(result, indent=2, default=str)}]
                write_result(request.id, {"content": content_items})
                return
            
            write_error(request.id, -32601, "Unknown tool")
            return
        if method == "resources/list":
            # Refresh views before listing
            self._ensure_views_fresh()
            resources = [
                {
                    "uri": f"duckdb://{name}",
                    "name": name,
                    "mimeType": "application/x-duckdb-view",
                }
                for name in sorted(self.views)
            ]
            write_result(request.id, {"resources": resources})
            return
        if method == "resources/read":
            # Refresh views before reading
            self._ensure_views_fresh()
            uri = params.get("uri")
            if not isinstance(uri, str) or not uri.startswith("duckdb://"):
                write_error(request.id, -32602, "Invalid uri")
                return
            view_name = uri.replace("duckdb://", "")
            if view_name not in self.views:
                write_error(request.id, -32602, "Unknown view")
                return
            sql = f"select * from {view_name} limit {self.config.max_rows}"
            try:
                result = self._query(sql)
            except Exception as exc:
                write_error(request.id, -32000, str(exc))
                return
            write_result(request.id, {"contents": [{"uri": uri, "text": result}]})
            return
        write_error(request.id, -32601, "Unknown method")

    def _query(self, sql: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(sql).fetchdf()
        return rows.to_dict(orient="records")


def main() -> None:
    import argparse
    from migration_agents.constants import ensure_directories
    
    # Ensure all standard directories exist
    ensure_directories()

    parser = argparse.ArgumentParser(description="MCP DuckDB server (stdio JSON-RPC).")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    server = MCPServer(config)
    run_stdio(server.handle)


if __name__ == "__main__":
    main()
