# MCP DuckDB Server

The MCP server exposes Parquet-backed DuckDB views via stdio JSON-RPC.
It registers a view per top-level directory in `parquet_root`.

## Per-Run Database Architecture

Each pipeline run gets its own DuckDB database file:

```
data/duckdb/
├── run_20260126120000.duckdb   # First run
├── run_20260126143000.duckdb   # Second run
└── run_20260127091500.duckdb   # Latest run
```

**Benefits:**
- Views are created once when the database is first accessed
- No stale view issues when switching between runs
- Clean separation between different pipeline executions
- Parallel runs don't conflict with each other

**Connection Management:**
- All code uses `get_run_connection()` from `duckdb_catalog.py`
- Connections are always closed in `finally` blocks
- Falls back to `:memory:` only when no run exists yet

```python
from migration_agents.mcp.duckdb_catalog import get_run_connection

conn, run_id = get_run_connection(parquet_root, run_id)
try:
    result = conn.execute("SELECT * FROM symbols").fetchdf()
finally:
    conn.close()  # Always close!
```

## Running the server

```bash
PYTHONPATH=src python -m migration_agents.mcp.server \
  --config config/mcp.json
```

Alternatively, run the included helper script:

```bash
scripts/run_mcp_server.sh
```

## Agent Tools

The MCP server provides agent-aligned tools for autonomous pipeline execution.
These tools are organized by agent responsibility:

### 01-analyzer (One-time setup, Steps 1-3)

| Tool | Step | Description |
|------|------|--------------|
| `analyzer` | `ingest` | Step 1: Ingest legacy source files into the lakehouse |
| `analyzer` | `parse` | Step 2: Parse source with tree-sitter, emit symbols/calls |
| `analyzer` | `slice` | Step 3: Build vertical slices by depth workflows |

**Parameters:**

| Parameter | Steps | Default | Description |
|-----------|-------|---------|-------------|
| `step` | all | *required* | `ingest`, `parse`, `slice` |
| `source_path` | ingest | — | Path to legacy source directory |
| `ingestion_mode` | ingest | `incremental` | `full` or `incremental` |
| `output_root` | ingest | `data/parquet` | Output directory for parquet files |
| `config_path` | parse, slice | `config/parser.json` | Path to config JSON file |
| `artifact_version` | ingest, parse | `1` | Artifact version number |
| `entry_graph_incremental` | parse | `true` | Skip already processed entry graphs |
| `entry_graph_render_svg` | parse | `false` | Render SVG graphs |
| `roslyn_cmd` | parse | `null` | Command for C#/VB.NET Roslyn analyzer |
| `roslyn_timeout_sec` | parse | `60` | Timeout for Roslyn analysis |
| `roslyn_parquet_root` | parse | `null` | Pre-computed Roslyn output path |
| `depth` | slice | `10` | Maximum call graph depth to traverse |
| `min_depth` | slice | `0` | Minimum depth to start processing |
| `slicing_mode` | slice | `auto` | `auto`, `entry_graph`, or `community` |
| `confirm` | all | `false` | Set to `true` to execute after preview |

**Roslyn Integration:**

For deep C#/VB.NET call resolution, configure Roslyn:

```
analyzer step='parse' roslyn_cmd=['dotnet', 'run', '--project', 'RoslynAnalyzer'] confirm=true
```

Or use pre-computed Roslyn output for faster incremental runs:

```
analyzer step='parse' roslyn_parquet_root='data/roslyn_output' confirm=true
```

**Usage:**
```
analyzer step='ingest' source_path='/path/to/source' ingestion_mode='full' confirm=true
analyzer step='parse' config_path='config/parser.json' confirm=true
analyzer step='slice' slicing_mode='entry_graph' confirm=true
```

### 02-builder (Per-slice code generation)

| Tool | Description |
|------|-------------|
| `builder_generate` | Generate logic rules, domain model, tests, and code |
| `builder_fix` | Apply a fix from the fix_queue after validation failures |

### DDD Progress & State Management (Parquet-based)

| Tool | Description |
|------|-------------|
| `ddd_create_job` | Create a DDD job with Parquet state tracking |
| `ddd_get_job_progress` | Get progress report with ETA (survives chat restart) |
| `ddd_list_pending_slices` | List slices still needing analysis |
| `ddd_resume_job` | Resume interrupted job from checkpoint |
| `ddd_get_context_summary` | Get bounded contexts discovered so far |

### Batch DDD Analysis (for 100+ slices)

| Tool | Description |
|------|-------------|
| `batch_ddd_analysis` | Prepare batch of slices for Copilot-driven analysis |
| `batch_ddd_apply_slice` | Store analysis for single slice from batch |
| `batch_ddd_status` | Check batch processing status |
| `batch_ddd_build_model` | Synthesize domain model from all analyses |
| `batch_codegen` | DDD-first code generation for entire codebase |

### 03-judge (Validation and fix loop)

| Tool | Description |
|------|-------------|
| `judge_validate` | Validate build/test status, citations, and logic alignment |

### Utility Tools

| Tool | Description |
|------|-------------|
| `pipeline_status` | Get status of all pipeline stages |
| `list_endpoints` | List discovered endpoints from parsed codebase |
| `list_slices` | List generated slices with status |
| `get_slice_context` | Get full context for a specific slice |
| `duckdb_query` | Execute custom SQL on the lakehouse |

## Workflow

```
01-analyzer (one-time) → handoff → 02-builder ↔ 03-judge (fix loop per slice)
```

1. **01-analyzer** runs steps 1-3 once to populate the lakehouse
2. **02-builder** creates DDD job with state tracking (`ddd_create_job`)
3. **02-builder** processes slices in batches (`batch_ddd_analysis` + `batch_ddd_apply_slice`)
4. Progress is tracked in Parquet - survives chat restart (`ddd_get_job_progress`)
5. **02-builder** synthesizes domain model (`batch_ddd_build_model`)
6. **02-builder** generates code (`batch_codegen`)
7. **03-judge** validates and populates `fix_queue` if issues found
8. **02-builder** applies fixes via `builder_fix`
9. Repeat 7-8 until validation passes

### Resumable Batch Processing

State is stored in Parquet files (`data/parquet/ddd_state/`):
- `job_state.parquet` - Overall job progress
- `batch_state.parquet` - Per-batch tracking
- `slice_analysis.parquet` - Individual slice results
- `domain_model.parquet` - Synthesized domain model

After chat restart:
```
ddd_get_job_progress solution_name='...'  # See current state
ddd_resume_job solution_name='...'        # Continue from checkpoint
ddd_list_pending_slices solution_name='...' # See remaining work
```

## VS Code Integration

Configure `.vscode/mcp.json` to auto-start the server:

```json
{
  "servers": {
    "migration-agents": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "migration_agents.mcp.server", "--config", "config/mcp.json"],
      "env": { "PYTHONPATH": "src" }
    }
  }
}
```

Auto-approve tools in `.vscode/settings.json`:

```json
{
  "chat.mcp.autoApprove": {
    "migration-agents": {
      "tools": [
        "duckdb_query",
        "analyzer",
        "builder_generate",
        "builder_fix",
        "judge_validate",
        "pipeline_status",
        "list_endpoints",
        "list_slices",
        "get_slice_context",
        "ddd_create_job",
        "ddd_get_job_progress",
        "ddd_list_pending_slices",
        "ddd_resume_job",
        "ddd_get_context_summary",
        "batch_ddd_analysis",
        "batch_ddd_apply_slice",
        "batch_ddd_status",
        "batch_ddd_build_model",
        "batch_codegen"
      ]
    }
  }
}
```

## Core Tooling

The server implements:

- `tools/list`: exposes all agent tools and `duckdb_query`
- `tools/call`: executes tool with arguments
- `resources/list`: lists Parquet-backed views
- `resources/read`: reads rows from a view (limited by `max_rows`)

## Client usage

Use one of these environment variables to enable MCP queries
from ingestion and parser stages:

- `MCP_SERVER_CMD`: command to run the stdio MCP server (split on spaces).
- `MCP_DUCKDB_URL`: URL for an HTTP MCP endpoint.

If neither is set, ingestion incremental mode and parser stage
will fail when they attempt to query intake tables.
