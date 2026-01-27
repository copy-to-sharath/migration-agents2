#!/usr/bin/env bash
set -euo pipefail

# Helper to run the MCP DuckDB server from the repository root.
# Prefers a Python from a local virtualenv (.venv, venv, env, .env) if present.
# Pass any extra args to the Python command.

if [ -f "scripts/mcp_env.sh" ]; then
	source "scripts/mcp_env.sh"
fi

venv_dirs=(.venv venv env .env)
PYEXEC=""
for d in "${venv_dirs[@]}"; do
	if [ -x "${d}/bin/python" ]; then
		PYEXEC="${d}/bin/python"
		break
	fi
done

if [ -z "${PYEXEC}" ]; then
	if command -v python3 >/dev/null 2>&1; then
		PYEXEC=python3
	else
		PYEXEC=python
	fi
fi

export PYTHONPATH="${PYTHONPATH:-src}"
export MCP_SERVER_CMD="${PYEXEC} -m migration_agents.mcp.server --config config/mcp.json"
exec "${PYEXEC}" -m migration_agents.mcp.server --config config/mcp.json "$@"
