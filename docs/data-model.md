# Data Model

All artifacts are Parquet datasets under `data/parquet/<table_name>`.
DuckDB views are registered per table name by the MCP server.

## Storage Layout

Artifacts are stored by run and stage:

```
data/parquet/<run_id>/stage_<n>/<table_name>/run_id=<...>/artifact_version=<...>/*.parquet
```

## DuckDB Database Layout

Each run gets its own DuckDB database:

```
data/duckdb/<run_id>.duckdb
```

Views are registered by table name when the database is first created.
Use `get_run_connection()` to get the correct database for a run.

## Versioning columns (required)

Every table must include these columns:

- `run_id`
- `artifact_version`
- `slice_id`
- `created_at`
- `supersedes_version`
- `source_ref`

## Current tables (implemented)

Stage 0 (Ingestion):
- `intake_source_index`
- `intake_source_chunks`
- `intake_build_context`
- `intake_schema_snapshot`

Stage 1 (Parser):
- `symbols`
- `calls`
- `conditions`
- `constants`
- `data_access`
- `code_graph_nodes`
- `code_graph_edges`
- `graph_metadata`
- `entry_exit_map`
- `entry_graphs`
- `entry_graph_state`
- `entry_graph_processing_summary`
- `entry_graph_summaries`
- `entry_graph_llm_debug`
- `parse_audit`
- `coverage_summary`

Stage 3 (Slice extractor):
- `slice_manifest`
- `slice_context`
- `slice_source_refs`

Stage 4 (Logic manifester):
- `logic_rules`
- `logic_edges`
- `trace_map`

Stage 5 (Domain architect):
- `domain_entities`
- `value_objects`
- `aggregates`
- `context_map`
- `domain_insights`
- `endpoints`
- `endpoint_flows`
- `endpoint_coverage`
- `dead_code`
- `context_reasoning`
- `context_groups`

Agent knowledge base:
- `knowledge_base_episodic`
- `knowledge_base_short_term`
- `knowledge_base_long_term`

## Planned tables (pipeline target)

Stage 2 (Graph enrichment - optional):
- `code_vectors`
- `graph_metadata`
- `vector_metadata`
- `slice_candidates`

Stage 6:
- `tests`, `test_cases`, `test_coverage`

Stage 7:
- `code_artifacts`, `api_contracts`

Stage 8:
- `build_reports`, `test_reports`, `fix_queue`

Stage 9:
- `fix_log`, `code_changes`

Stage 10:
- `judge_reports`, `rule_coverage`

## Governance tables (planned)

- `endpoints`, `dead_code`
- `knowledge_base_episodic`, `knowledge_base_short_term`, `knowledge_base_long_term`
- BDD and event storming tables (see `blueprint.md`)

For detailed table schemas and field definitions, see `blueprint.md`.
