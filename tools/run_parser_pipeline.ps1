Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RootDir

$env:PYTHONPATH = "src"
$env:MCP_SERVER_CMD = "uv run python -m migration_agents.mcp.server --config config/mcp.json"

uv run python -m migration_agents.ingestion.main --config config/ingestion.json
uv run python -m migration_agents.parser.main --config config/parser.example.json
