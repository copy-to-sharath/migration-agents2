#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONPATH=src
export MCP_SERVER_CMD="uv run python -m migration_agents.mcp.server --config config/mcp.json"

uv run python -m migration_agents.ingestion.main --config config/ingestion.json
uv run python -m migration_agents.parser.main --config config/parser.example.json
