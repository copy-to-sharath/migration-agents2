#!/usr/bin/env bash
set -euo pipefail

# Optional shared MCP environment. Override MCP_DUCKDB_URL to point
# at an HTTP MCP endpoint if one is available.
export MCP_SERVER_CMD="${MCP_SERVER_CMD:-.venv/bin/python -m migration_agents.mcp.server --config config/mcp.json}"
export MCP_DUCKDB_URL="${MCP_DUCKDB_URL:-}"
