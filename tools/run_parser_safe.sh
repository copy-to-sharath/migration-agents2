#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TOP_K="${TOP_K:-10}"
LLM_TIMEOUT_SEC="${LLM_TIMEOUT_SEC:-600}"

TMP_CONFIG="$(mktemp -t parser.example.XXXXXX)"
TMP_CONFIG="${TMP_CONFIG}.json"
uv run python - <<PY
import json
from pathlib import Path

src = Path("config/parser.example.json")
data = json.loads(src.read_text(encoding="utf-8"))
data["entry_graph_top_k"] = int("${TOP_K}")
data["llm_timeout_sec"] = int("${LLM_TIMEOUT_SEC}")
Path("${TMP_CONFIG}").write_text(json.dumps(data, indent=2), encoding="utf-8")
PY

export PYTHONPATH=src
export MCP_SERVER_CMD="uv run python -m migration_agents.mcp.server --config config/mcp.json"

uv run python -m migration_agents.parser.main --config "${TMP_CONFIG}"
