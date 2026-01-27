# Migration Agents Documentation

This folder is the source of truth for how to run and extend the migration-agents pipeline.
If you are new, start with Quickstart and Configuration.

## Agent Architecture

The pipeline uses 3 agents with clear responsibilities:

| Agent | Role | Steps | Tools |
|-------|------|-------|-------|
| **01-analyzer** | One-time analysis | 1-3 | `analyzer` (steps: `ingest`, `parse`, `slice`) |
| **02-builder** | Per-slice generation | 4+ | `builder_generate`, `builder_fix`, `ddd_*`, `batch_ddd_*` |
| **03-judge** | Validation & fix loop | 5 | `judge_validate` |

```
01-analyzer (one-time) → handoff → 02-builder ↔ 03-judge (fix loop per slice)
```

### State Management

For large codebases (100+ slices), use Parquet-based state management:

```
ddd_create_job → batch_ddd_analysis → [analyze slices] → batch_ddd_build_model → batch_codegen
```

State survives chat restarts. Resume with:
```
ddd_get_job_progress solution_name='...'  # Check state
ddd_resume_job solution_name='...'        # Continue
```

See [state-management.md](state-management.md) for details.

### Tool Discovery

Use `discover_tools` to get all available tools, standard paths, and state management info:

```
discover_tools                    # All tools
discover_tools agent='01-analyzer'  # Filter by agent
```

## Config Files

All configs are in `config/`. Defaults are in `src/migration_agents/constants.py`.

| File | Purpose |
|------|---------|
| `ingestion.json` | Source ingestion |
| `parser.json` | Tree-sitter parsing |
| `slice.json` | Slice extraction |
| `codegen.json` | Code generation |
| `ddd_batch.json` | Batch DDD analysis |
| `judge.json` | Validation settings |
| `mcp.json` | MCP server config |

## Docs Map

- [quickstart.md](quickstart.md): Bootstrap environment and run pipeline
- [configuration.md](configuration.md): JSON config files reference
- [mcp.md](mcp.md): MCP server, agent tools, and VS Code integration
- [state-management.md](state-management.md): Parquet-based resumable batch processing
- [pipeline.md](pipeline.md): End-to-end pipeline stages
- [data-model.md](data-model.md): Parquet tables and versioning

### Stage Docs

- [ingestion.md](ingestion.md): Stage 0 intake
- [parser.md](parser.md): Stage 1/2 parser
- [slice-extractor.md](slice-extractor.md): Stage 3 slicing
- [domain-architect.md](domain-architect.md): Domain model synthesis
- [logic-manifester.md](logic-manifester.md): Business logic extraction

## Agent Files

Agent prompts are in `.github/agents/`:
- `01-analyzer.agent.md` - One-time analysis
- `02-builder.agent.md` - Per-slice code generation  
- `03-judge.agent.md` - Validation with fix loop

### Grounding Requirements

All agents must produce grounded responses based on actual data:

| Agent | Grounding Focus |
|-------|----------------|
| **01-analyzer** | Query `duckdb_query` before answering; cite actual counts and paths |
| **02-builder** | Every artifact needs `source_ref`; trace to legacy code |
| **03-judge** | Evidence-based validation; specific file:line for issues |

**Never produce:**
- Hallucinated code or counts
- Vague issues ("some tests failing")
- Properties not found in source

## Database Architecture

Each run gets its own DuckDB file to avoid view conflicts:

```
data/duckdb/
├── run_20260126120000.duckdb
├── run_20260126143000.duckdb
└── run_20260127091500.duckdb
```

Use `get_run_connection()` for all database access:

```python
from migration_agents.mcp.duckdb_catalog import get_run_connection

conn, run_id = get_run_connection(parquet_root, run_id)
try:
    result = conn.execute("SELECT * FROM symbols").fetchdf()
finally:
    conn.close()  # Always close!
```
