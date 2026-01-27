Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RootDir

$TopK = if ($env:TOP_K) { [int]$env:TOP_K } else { 10 }
$TimeoutSec = if ($env:LLM_TIMEOUT_SEC) { [int]$env:LLM_TIMEOUT_SEC } else { 600 }

$TempConfig = [System.IO.Path]::ChangeExtension([System.IO.Path]::GetTempFileName(), ".json")
python - <<PY
import json
from pathlib import Path

data = json.loads(Path("config/parser.example.json").read_text(encoding="utf-8"))
data["entry_graph_top_k"] = $TopK
data["llm_timeout_sec"] = $TimeoutSec
Path(r"$TempConfig").write_text(json.dumps(data, indent=2), encoding="utf-8")
PY

$env:PYTHONPATH = "src"
$env:MCP_SERVER_CMD = "uv run python -m migration_agents.mcp.server --config config/mcp.json"

uv run python -m migration_agents.parser.main --config $TempConfig
