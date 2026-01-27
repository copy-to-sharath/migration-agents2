# Pipeline Overview

This pipeline migrates legacy systems by producing Parquet-backed artifacts
for each stage and using DuckDB as the read layer.

## Agent Architecture

The pipeline is orchestrated by 3 agents with clear handoffs:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  01-ANALYZER (One-time setup, Steps 1-3)                                │
│  ────────────────────────────────────────                              │
│  INGEST → PARSE → SLICE                                                │
│                                                                         │
│  Tool: analyzer step='ingest|parse|slice'                              │
│                                                                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HANDOFF (per slice by depth)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  02-BUILDER ↔ 03-JUDGE (Repeatable per slice)                           │
│  ─────────────────────────────────────────────                          │
│                                                                         │
│  builder_generate → judge_validate → builder_fix (if needed) → repeat  │
│                                                                         │
│  Process: depth_0 slices → depth_1 slices → ... → depth_N slices       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Files

- `.github/agents/01-analyzer.agent.md` - One-time analysis agent
- `.github/agents/02-builder.agent.md` - Per-slice code generation
- `.github/agents/03-judge.agent.md` - Validation with fix loop

## Global rules

- All artifacts are Parquet, queried via DuckDB.
- All tables are versioned with:
  `run_id`, `artifact_version`, `slice_id`, `created_at`, `supersedes_version`.
- No in-place updates; new versions append rows.
- Parquet outputs must include `source_ref` for traceability.
- Endpoint processing is per-slice and per-endpoint to avoid context bleed.

## Stages

0) Intake and normalization
- Build source index and chunked content.
- Tables: `intake_source_index`, `intake_source_chunks`,
  `intake_build_context`, `intake_schema_snapshot`.

1) Parser (build only)
- Extract symbols, calls, conditions, constants, data access; build call/data graphs and metadata.
- Tables: `symbols`, `calls`, `conditions`, `constants`, `data_access`, `parse_audit`,
 `code_graph_nodes`, `code_graph_edges`, `graph_metadata`, `entry_exit_map`,
 `entry_graphs`, `entry_graph_state`, `entry_graph_processing_summary`, `parse_missed`.
- Entry: `python -m migration_agents.parser.build --config config/parser.build.example.json`
- Incremental: set `entry_graph_incremental=true` in config to skip already processed entry graphs for the same `run_id`/`artifact_version`.

2) Parser LLM (separate run, optional)
- Load stage_1 graph parquet, filter depth >= `entry_graph_min_depth` with source, produce LLM summaries.
- Tables: `entry_graph_summaries`, `entry_graph_summaries_merged` (optional), `entry_graph_llm_debug`.
- Entry: `python -m migration_agents.parser.main --config config/parser.llm.example.json --run-llm`
- Incremental: re-use the same `run_id` to avoid reprocessing graphs; keep rendering disabled in the LLM config.
- Cleanup: use `tools/clean_parser_artifacts.py --run-id <run> --execute` to delete a prior parser run (dry-run by default).

2b) Parser render-only (optional)
- Render DOT/PNG/SVG from existing stage_1 parquet without re-parsing.
- Entry: `python -m migration_agents.parser.render --config config/parser.render.example.json`

3) Slice extractor (Implemented)
- Produce slice manifests and source references.
- Tables: `slice_manifest`, `slice_context`, `slice_source_refs`.

4) Logic manifester (Implemented)
- Convert slices to Logic Manifest rules and traceability.
- Tables: `logic_rules`, `logic_edges`, `trace_map`.

5) Domain architect (Implemented)
- Identify entities, value objects, aggregates, and context map, plus per-endpoint
  flows and LLM summaries.
- Tables: `domain_entities`, `value_objects`, `aggregates`, `context_map`,
  `domain_insights`, `endpoints`, `endpoint_flows`, `endpoint_coverage`,
  `dead_code`, `context_reasoning`, `context_groups`.

6) TDD engineer
- Generate tests and coverage mapping.
- Tables: `tests`, `test_cases`, `test_coverage`.

7) Implementer
- Generate code artifacts and API contracts.
- Tables: `code_artifacts`, `api_contracts`.

8) Build and test loop
- Build and test reports, fix queue.
- Tables: `build_reports`, `test_reports`, `fix_queue`.

9) Fixer and debugger
- Record fixes and diffs.
- Tables: `fix_log`, `code_changes`.

10) Judge
- Judge reports and rule coverage.
- Tables: `judge_reports`, `rule_coverage`.

## Related references

- `blueprint.md` contains the detailed rationale and enforcement rules.
- `.github/agents/01-analyzer.agent.md` - One-time analysis (Steps 1-3)
- `.github/agents/02-builder.agent.md` - Per-slice code generation
- `.github/agents/03-judge.agent.md` - Validation with fix loop
- `docs/mcp.md` - MCP server tools and VS Code integration
