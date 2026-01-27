# Quickstart

This project expects Python 3.13 and produces Parquet artifacts for each stage.

## Prereqs

- Python 3.13
- uv (recommended for dependency management)
- Git (for building tree-sitter grammars)
- C/C++ toolchain (cc/c++) for building tree-sitter language libraries

## 1) Install dependencies

```bash
uv sync
```

If you are not using uv, create a venv and install from pyproject.toml.

## 2) Build tree-sitter language library

The parser needs a compiled tree-sitter library. Build it once:

```bash
PYTHONPATH=src python -m migration_agents.parser.build_languages
```

The default output is `tree-sitter/languages.so`. On Windows, output is `tree-sitter/languages.dll`.

## 3) Run ingestion (Stage 0)

Update `config/ingestion.json` to point at your legacy source tree.

```bash
PYTHONPATH=src python -m migration_agents.ingestion.main \
  --config config/ingestion.json
```

This writes Parquet under `data/parquet/intake_*`.

## 4) Start the MCP server

```bash
PYTHONPATH=src python -m migration_agents.mcp.server \
  --config config/mcp.json
```

The MCP server:
- Creates a run-specific DuckDB database (`data/duckdb/{run_id}.duckdb`)
- Registers views over all Parquet tables for that run
- Auto-switches to new runs when `LATEST_RUN` changes

## 5) Run parser (Stage 1)

Update `config/parser.json` to point at your language library.
On Windows, use `config/parser.windows.example.json` as a reference.

```bash
PYTHONPATH=src python -m migration_agents.parser.build \
  --config config/parser.json
```

Coverage summary is generated under `data/parquet/coverage_summary`.

### Render graphs (optional)

Set these in `config/parser.json` to emit DOT/SVG:
- `entry_graph_render_dot: true`
- `entry_graph_render_svg: true`
- `entry_graph_render_full: true`

Outputs land under `data/parquet/entry_graphs/run_<id>/stage_1/`.

## 6) Run slice extractor (Stage 2)

```bash
PYTHONPATH=src python -m migration_agents.slice_extractor.main \
  --config config/slice.json
```

## 7) Use MCP Tools (Recommended)

For VS Code with GitHub Copilot, use the MCP tools directly:

```
# Discover available tools
discover_tools

# Run pipeline steps
analyzer step='ingest' config_path='config/ingestion.json' confirm=true
analyzer step='parse' config_path='config/parser.json' confirm=true
analyzer step='slice' config_path='config/slice.json' confirm=true

# Check pipeline status
pipeline_status
```

See [mcp.md](mcp.md) for full tool documentation.

### Roslyn support (C#/VB/.sln/.csproj/.vbproj)

Preferred flow: run Roslyn once to emit parquet, then point the parser at that parquet (no cross-process call during parsing).

1. Ingest (build intake parquet/index):
   ```bash
   PYTHONPATH=src python -m migration_agents.ingestion.main --config config/ingestion.json
   ```
2. Generate Roslyn parquet (reusing `input_root` from `config/ingestion.json`):
   ```bash
   INPUT_ROOT=$(python - <<'PY'
import json
cfg=json.load(open("config/ingestion.json"))
print(cfg.get("input_root",""))
PY
)
   dotnet run --project tools/roslyn-parser -- \
     --ingestion-config config/ingestion.json \
     --format parquet \
     --output data/parquet \
     "$INPUT_ROOT"
   # Run id: will reuse data/parquet/LATEST_RUN when present; else generates run_yyyyMMddHHmmss
   ```
   If you omit `--output`, the C# parser will default to the ingestion `output_root` (from `config/ingestion.json` when present) or `data/parquet`.
3. In `config/parser.json`, keep `roslyn_cmd: []`, set `roslyn_parquet_root` to the path above (default `data/parquet`), and optionally set `roslyn_parquet_run_id` (or leave `null` to use `LATEST_RUN`).
4. Run the parser as normal; it will load Roslyn symbols/calls/conditions/constants/data_access from the parquet and merge them into the same graphs/Parquet outputs.

Fallback: you can still set `roslyn_cmd` to `["dotnet","run","--project","tools/roslyn-parser","--"]` to shell out during parsing if you want the old behavior.

### Export a call graph DOT (optional)

```bash
PYTHONPATH=src python tools/export_call_graph.py \
  --run-id <run_suffix> --mode all|parallel|sequential \
  --output callgraph.dot
dot -Tsvg callgraph.dot -o callgraph.svg
```

### Generate depth-level graphs (optional)

Generate DOT graphs organized by call depth level (how deep the call chain goes):

```bash
uv run python tools/generate_depth_graphs.py
# Or specify a run:
uv run python tools/generate_depth_graphs.py --run-id run_20260122130739
```

Outputs to `generated/graphs/by_depth/depth_*.dot` with a summary file.

### Generate entry graphs by depth (optional)

Generate separate DOT files for each entry point, organized by depth level.
Each graph shows one entry point with all its reachable nodes and exit points.

```bash
uv run python tools/generate_entry_graphs_by_depth.py
# Or with options:
uv run python tools/generate_entry_graphs_by_depth.py --max-entries-per-depth 100
```

Options:
- `--max-entries-per-depth N`: Limit graphs per depth level (default: 10000)
- `--run-id`: Specify run ID (defaults to latest)

Outputs to `generated/graphs/entries_by_depth/depth_N/*.dot`:
- **Orange** = Entry node (in-degree 0)
- **Salmon** = Exit node(s) (out-degree 0 in subgraph)
- **Blue** = Intermediate node

Example output structure:
```
generated/graphs/entries_by_depth/
├── depth_1/    # Shallowest call chains
├── depth_2/
├── depth_3/
├── ...
├── depth_10/   # Deepest call chains
└── summary.txt
```

### Clean parser artifacts (optional)

To remove a prior parser run’s artifacts:

```bash
PYTHONPATH=src python tools/clean_parser_artifacts.py \
  --run-id <run_suffix> --target build --execute      # remove parse/graph artifacts

PYTHONPATH=src python tools/clean_parser_artifacts.py \
  --run-id <run_suffix> --target llm --execute        # remove entry-graph summaries only

PYTHONPATH=src python tools/clean_parser_artifacts.py \
  --run-id <run_suffix> --target all --execute        # remove both
```

Omit `--execute` for a dry-run preview.

### Clean ingestion artifacts (optional)

```bash
PYTHONPATH=src python tools/clean_ingestion_artifacts.py --run-id <run_suffix> --execute
# or everything: --all --execute
```

### Clean pipeline data (optional)

Use the MCP tool to clean all pipeline data:

```
clean_pipeline confirm=true
```

Or use the CLI:

```bash
PYTHONPATH=src python tools/clean_stage_artifacts.py \
  --stage all --execute
```

## Legacy Stages (Optional)

The following stages are available but typically not needed when using the MCP-based agent workflow:

### Domain Architect

```bash
PYTHONPATH=src python -m migration_agents.domain_architect.main \
  --config config/domain_architect.json
```

### Logic Manifester

```bash
PYTHONPATH=src python -m migration_agents.logic_manifester.main \
  --config config/logic_manifester.json
```

### Codegen

```bash
PYTHONPATH=src python -m migration_agents.codegen.main \
  --config config/codegen.json
```

## Query Data

You can query Parquet via the MCP server (DuckDB) or a local DuckDB shell.
See [mcp.md](mcp.md) for details.
