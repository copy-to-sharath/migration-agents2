# Slice Extractor (Stage 3)

Stage 3 groups graph nodes into slices and emits the slice manifest,
context summary, and source references.

## Responsibilities

- Group nodes using entry graphs (preferred) or community detection.
- Emit `slice_manifest` with file paths, symbol ids, and table names.
- Emit `slice_context` with a summary, risks, and assumptions.
- Emit `slice_source_refs` with line-level excerpts.

## Slicing Modes

The slice extractor supports three slicing modes:

| Mode | Description |
|------|-------------|
| `auto` | Uses entry graphs if available, falls back to community detection |
| `entry_graph` | Forces entry graph-based slicing (1 slice per entry point) |
| `community` | Forces community detection-based slicing |

**Entry Graph Slicing** creates focused slices based on entry points and their 
reachable call graphs. Each entry (e.g., API endpoint, page handler) becomes 
a separate slice containing only the nodes reachable from that entry.

**Community Detection Slicing** groups nodes based on graph connectivity using 
Louvain community detection. This may result in larger, more interconnected slices.

## Inputs

Queried from MCP-backed DuckDB (or directly from Parquet):

- `code_graph_nodes`
- `graph_metadata`
- `entry_graphs` (for entry_graph slicing mode)
- `symbols`
- `data_access`
- `intake_source_chunks`

## Output tables

- `slice_manifest`
- `slice_context`
- `slice_source_refs`

All tables include versioning columns:
`run_id`, `artifact_version`, `slice_id`, `created_at`, `supersedes_version`.

## Configuration

```json
{
  "run_id": "auto",
  "artifact_version": 1,
  "output_root": "data/parquet",
  "slicing_mode": "auto",
  "max_source_refs_per_slice": 200,
  "max_excerpt_chars": 500
}
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `run_id` | `auto` | Run ID (auto uses latest) |
| `slicing_mode` | `auto` | Slicing strategy: `auto`, `entry_graph`, `community` |
| `max_source_refs_per_slice` | `200` | Maximum source refs per slice |
| `max_excerpt_chars` | `500` | Maximum characters per excerpt |

## Running

```bash
# Using MCP server
MCP_SERVER_CMD=".venv/bin/python -m migration_agents.mcp.server --config config/mcp.json" \
PYTHONPATH=src python -m migration_agents.slice_extractor.main --config config/slice.json

# Direct Parquet mode (no MCP server needed)
PARQUET_ROOT=data/parquet PYTHONPATH=src python -m migration_agents.slice_extractor.main \
  --config config/slice.json

# Incremental mode with specific run_id
RUN_ID=run_20260125203002 PARQUET_ROOT=data/parquet PYTHONPATH=src python -m migration_agents.slice_extractor.main \
  --config config/slice.json
```
