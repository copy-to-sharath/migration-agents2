# Configuration

All stages are configured via JSON files in `config/`.
Paths are resolved to absolute paths at load time.

## Centralized Constants

Default values are defined in `src/migration_agents/constants.py`:

```python
class DefaultPaths:
    PARQUET_ROOT = Path("data/parquet")
    GENERATED_ROOT = Path("generated")
    DUCKDB_DIR = Path("data/duckdb")
    CONFIG_DIR = Path("config")

class ConfigFiles:
    INGESTION = "config/ingestion.json"
    PARSER = "config/parser.json"
    SLICE = "config/slice.json"
    CODEGEN = "config/codegen.json"
    JUDGE = "config/judge.json"
    MCP = "config/mcp.json"
```

Import from `constants.py` instead of hardcoding paths:

```python
from migration_agents.constants import DEFAULT_PATHS, CONFIG_FILES
```

## Config Files

| File | Purpose |
|------|---------|
| `ingestion.json` | Source ingestion settings |
| `parser.json` | Tree-sitter parsing settings |
| `parser.windows.example.json` | Windows-specific paths |
| `slice.json` | Vertical slice extraction |
| `codegen.json` | Code generation config |
| `codegen.ddd-first.json` | DDD-first workflow example |
| `ddd_batch.json` | Batch DDD analysis |
| `judge.json` | Validation/rubric settings |
| `mcp.json` | MCP server config |

## Ingestion config (`config/ingestion.json`)

Fields (see `src/migration_agents/ingestion/config.py`):

- `run_id`: `"auto"` or a fixed id (e.g., `run_20250101120000`).
- `artifact_version`: integer >= 1.
- `input_root`: source directory to scan.
- `output_root`: Parquet output root (default `data/parquet`).
- `include_extensions`: file extensions or `"*"` for all.
- `exclude_extensions`: extensions to skip. Defaults exclude executables/libraries (`.exe`, `.dll`, `.so`, `.a`, `.lib`, `.o`, `.obj`, `.pdb`), archives (`.zip`, `.tar`, `.gz`, `.rar`, etc.), media, and static assets (`.js`, `.css`), plus other binaries. Add language-specific extensions here (e.g., `.php`, `.jsp`) to omit whole languages if needed.
- `exclude_dirs`: directories to skip by name. Defaults exclude VCS/IDE/cache/build folders (`.git`, `.github`, `.vs`, `.idea`, `.vscode`, `.venv`, `node_modules`, `bin`, `obj`, `dist`, `build`, `target`, `out`, `coverage`, `packages`, `vendor`, `CMakeFiles`).
- `max_lines_per_chunk`: line-based chunk size.
- `max_chars_per_chunk`: character-based chunk size.
- `checksum_algo`: currently `"sha256"`.
- `workers`: integer or `"auto"`.
- `incremental`: when true, skip unchanged files using MCP checksums.
- `build_context`: optional list of build metadata entries.
- `schema_snapshot_path`: optional schema file to include in intake.

## Parser config (`config/parser.json`)

Fields (see `src/migration_agents/parser/config.py`):

- `run_id`: `auto` (default) or must match ingestion.
- `artifact_version`: must match ingestion.
- `output_root`: Parquet output root.
- `language_library_path`: path to compiled tree-sitter library (`languages.so` on macOS/Linux, `languages.dll` on Windows).
- `language_map`: extension to language name mapping.
- `queries_dir`: directory for `.scm` queries (default `config/queries`).
- `workers`: integer or `"auto"`.
- `roslyn_languages`: languages handled by Roslyn when configured.
- `roslyn_cmd`: optional command that emits JSON to stdout.
- `roslyn_timeout_sec`: per-file timeout.
- `max_label_chars`: truncate labels for graph nodes.
- `entry_graph_max_depth`: maximum depth when scoring entry graphs.
- `entry_graph_node_limit`: cap on nodes used in depth-breadth scoring.
- `entry_graph_depth_threshold`: minimum capped depth to emit an entry graph.
- `entry_graph_top_k`: keep only top-K entry graphs (null = no limit).
- `entry_graph_incremental`: skip already processed entry graphs using state.
- `entry_graph_render_dot`: write DOT graphs for full graph + entry graphs.
- `entry_graph_render_png`: render PNG graphs using Graphviz `dot`.
- `entry_graph_render_svg`: render SVG graphs using Graphviz.
- `entry_graph_render_engine`: Graphviz engine to use (e.g., `sfdp`).
- `entry_graph_render_dir`: output directory for rendered graphs.
- `entry_graph_render_full`: render the full graph (disable to speed up runs).
- `llm_provider`/`llm_model`/`llm_base_url`: LLM configuration (HTTP/hosted providers such as Ollama/OpenAI/Gemini). Leave `llm_cmd` empty when using endpoints.
- `llm_timeout_sec`: LLM timeout seconds.
- `llm_max_input_chars`: maximum prompt size for entry graph summaries.
- `entry_graph_llm_batch_size`: number of entry graphs summarized per LLM call.
- `entry_graph_summary_fields`: dictionary of optional summary fields to request.
- `entry_graph_llm_strict`: fail the run if LLM summaries are missing.
- `entry_graph_llm_debug`: write `entry_graph_llm_debug` with raw prompt + error info.

## Vectorization config (`config/vectorization.example.json`)

Fields (see `src/migration_agents/vectorization/config.py`):

- `run_id`: `auto` (default) or must match ingestion/parser.
- `artifact_version`: must match ingestion/parser.
- `output_root`: Parquet output root.
- `workers`: integer or `\"auto\"`.
- `embedding_model`: embedding model name or endpoint.
- `embedding_batch_size`: batch size for embedding requests.
- `max_items`: optional cap on input rows for testing.
- `include_enriched_sources`: include slice/logic/domain tables in embeddings.
- `embedding_provider`: `local` (default) or `http`.
- `embedding_http_url`: URL for remote embedding service when `embedding_provider=http`.
- `embedding_http_timeout_sec`: request timeout for remote embeddings.
- `embedding_http_headers`: optional HTTP headers for remote embeddings.

## Slice extractor config (`config/slice.json`)

Fields (see `src/migration_agents/slice_extractor/config.py`):

- `run_id`: `auto` (default) or must match ingestion/parser.
- `artifact_version`: must match ingestion/parser.
- `output_root`: Parquet output root.
- `workers`: integer or `\"auto\"`.
- `max_source_refs_per_slice`: cap source references per slice.
- `max_excerpt_chars`: truncate excerpt length.

## Logic manifester config (`config/logic_manifester.json`)

Fields (see `src/migration_agents/logic_manifester/config.py`):

- `run_id`: `auto` (default) or must match upstream stages.
- `artifact_version`: must match upstream stages.
- `output_root`: Parquet output root.
- `workers`: integer or `\"auto\"`.
- `max_rule_text_chars`: truncate rule text length.
- `max_trace_refs_per_rule`: cap trace references per rule.

## Domain architect config (`config/domain_architect.json`)

Fields (see `src/migration_agents/domain_architect/config.py`):

- `run_id`: `auto` (default) or must match upstream stages.
- `artifact_version`: must match upstream stages.
- `output_root`: Parquet output root.
- `workers`: integer or `\"auto\"`.
- `max_name_chars`: truncate entity/value object names.
- `max_comment_chars`: truncate logic comments.
- `max_indicative_chars`: truncate indicative summaries.
- `context_cluster_bits`: number of high-order simhash bits to cluster contexts.
- `vector_cluster_bits`: number of high-order simhash bits for embedding clusters.
- `max_nodes_per_slice`: cap nodes used per slice when aggregating vectors.
- `llm_provider`: `ollama`, `openai`, or `gemini` to use hosted/HTTP providers. Leave `llm_cmd` empty when using endpoints.
- `llm_model`: model name for `llm_provider` providers (required for `ollama`, `openai`, `gemini`).
- `llm_base_url`: base URL for Ollama HTTP (default `http://localhost:11434`).
- `entry_graph_llm_merge_enabled`: when true, writes a merged LLM summary parquet for downstream BRD/DDD.
- `entry_graph_llm_merge_join`: separator used when combining per-entry summaries into merged fields.
- `entry_graph_llm_merge_max_chars`: cap for merged summary fields to avoid oversized rows.
- `entry_graph_llm_log_response`: log LLM response previews for debugging (truncated).
- `entry_graph_llm_store_response`: store per-entry LLM response JSON in `entry_graph_summaries`.
- `auto_ingest_if_missing`: run ingestion automatically if `intake_source_chunks` is missing.
- `ingestion_config_path`: config path used when `auto_ingest_if_missing` is enabled.
- `auto_build_languages_if_missing`: build `languages.so` automatically when missing.
- `tree_sitter_languages_config_path`: config for tree-sitter language build.
- `llm_timeout_sec`: timeout for LLM calls.
- `llm_max_input_chars`: truncate LLM prompt size.

## Judge config (`config/judge.json`)

Fields (see `src/migration_agents/judge/main.py`):

- `run_id`: `auto` (default) or must match upstream stages.
- `artifact_version`: must match upstream stages.
- `output_root`: Parquet output root.
- `check_citations`: validate citation completeness.
- `check_coverage`: validate rule coverage.
- `check_dead_code`: detect dead/unreachable code.

## Codegen config (`config/codegen.json`)

Fields (see `src/migration_agents/codegen/config.py`):

- `run_id`: `auto` (default) or must match upstream stages.
- `artifact_version`: must match upstream stages.
- `output_root`: Parquet output root.
- `generated_root`: folder for generated solutions.
- `solution_name`: name of the solution being generated.
- `api_namespace`: namespace for the API project.
- `test_namespace`: namespace for test projects.
- `target_framework`: target .NET framework (e.g., `dotnet8`).
- `generate_tests`: whether to generate test files.
- `use_clean_architecture`: use Clean Architecture patterns.
- `use_cqrs`: use CQRS pattern.
- `use_ddd`: use Domain-Driven Design patterns.
- `ddd_first`: run DDD analysis before code generation.
- `require_domain_verification`: require domain model verification.
- `require_gherkin_verification`: require Gherkin/BDD verification.
- `require_contract_verification`: require contract verification.

## DDD Batch config (`config/ddd_batch.json`)

Fields for batch DDD analysis:

- `job.solution_name`: name of the solution.
- `job.output_root`: Parquet output root.
- `job.generated_root`: folder for generated code.
- `batch.batch_size`: slices per batch.
- `batch.rate_limit_ms`: delay between batches.
- `batch.auto_checkpoint`: save progress after each batch.
- `slicing.min_depth` / `max_depth`: depth range for slices.
- `llm.provider`: LLM provider (`copilot`, `ollama`, etc.).

## MCP config (`config/mcp.json`)

Fields (see `src/migration_agents/mcp/config.py`):

- `parquet_root`: root folder with Parquet datasets.
- `duckdb_dir`: directory for run-specific DuckDB files (each run gets `{run_id}.duckdb`).
- `max_rows`: limit for `resources/read` results.

## State Management

Pipeline state is stored in Parquet files under `data/parquet/pipeline_state/`:

| File | Purpose |
|------|---------|
| `pipeline_step_state.parquet` | Overall pipeline step tracking |
| `ddd_job_state.parquet` | DDD job metadata |
| `ddd_slice_state.parquet` | Per-slice DDD analysis state |
| `codegen_state.parquet` | Code generation state |
| `validation_state.parquet` | Validation results |
| `approval_state.parquet` | Human approval state |

Legacy JSON state files are in `generated/state/<stage>.json`.

See [state-management.md](state-management.md) for details.
