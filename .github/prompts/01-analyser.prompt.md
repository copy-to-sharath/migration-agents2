---
name: 01-analyzer
description: Run the one-time analysis pipeline (ingest → parse → slice) to prepare legacy code for migration.
---

# 01-Analyzer Agent

## Standard Paths (Use These Defaults)

| Path | Purpose |
|------|---------|
| `config/ingestion.json` | Ingestion config (source path, exclusions) |
| `config/parser.json` | Parser config (tree-sitter settings) |
| `config/slice.json` | Slice config (slicing mode, depth) |
| `data/parquet/` | Lakehouse output (Parquet tables) |

## Getting Started

```
discover_tools agent='01-analyzer'
```

## Quick Start (Copy-Paste)

```bash
# Step 1: Ingest
analyzer step='ingest' config_path='config/ingestion.json' confirm=true

# Step 2: Parse  
analyzer step='parse' config_path='config/parser.json' confirm=true

# Step 3: Slice
analyzer step='slice' config_path='config/slice.json' confirm=true
```

## Pipeline Steps

| Step | Config | Outputs |
|------|--------|---------|
| **ingest** | `config/ingestion.json` | `source_index`, `source_chunks` |
| **parse** | `config/parser.json` | `symbols`, `calls`, `code_graph_*` |
| **slice** | `config/slice.json` | `slice_manifest`, `slice_context` |

## Key Config Settings

**ingestion.json:**
- `input_root`: Path to legacy source (e.g., `/path/to/legacy`)
- `output_root`: `data/parquet` (default)

**parser.json:**
- `output_root`: `data/parquet` (default)
- `language_library_path`: `tree-sitter/languages.so`

**slice.json:**
- `slicing_mode`: `entry_graph` (recommended) or `community`
- `max_source_refs_per_slice`: 200

## Verification

```
pipeline_status
list_endpoints
list_slices
```

## Handoff

Hand off to **02-builder** when `list_slices` shows available slices.
