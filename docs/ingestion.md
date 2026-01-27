# Ingestion (Stage 0)

The ingestion stage scans legacy sources and writes Parquet tables for
intake indexing and chunking.

## Responsibilities

- Detect language by file extension.
- Compute checksums per file for incremental runs.
- Chunk text files into line ranges.
- Extract text from PDF and DOCX for searchable intake.
- Record build context and schema snapshot if provided.

## Data flow

1) Scan files under `input_root` with include/exclude rules.
2) Compute per-file checksum and LOC.
3) Chunk content into `intake_source_chunks` with line ranges.
4) Write Parquet to `output_root` (partitioned by `run_id` and `artifact_version`).

## Output tables

- `intake_source_index`: file-level metadata and checksums.
- `intake_source_chunks`: chunked content with line ranges.
- `intake_build_context`: optional build metadata.
- `intake_schema_snapshot`: optional schema snapshot.

All tables include versioning columns:
`run_id`, `artifact_version`, `slice_id`, `created_at`, `supersedes_version`.

## Incremental behavior

When `incremental` is true, ingestion queries the MCP server for
`intake_source_index` checksums and only processes files whose checksum changed.
If you are running without MCP, set `incremental` to false.

## Default excludes (recommended)

Use `exclude_dirs` and `exclude_extensions` to skip compiler outputs, binaries,
and packaged artifacts.

Common directories to exclude:
- `.git`, `.github`, `.vs`, `.idea`, `.vscode`
- `.venv`, `venv`, `__pycache__`
- `bin`, `obj`, `dist`, `build`, `target`, `out`, `coverage`
- `node_modules`, `packages`, `vendor`, `CMakeFiles`

Common extensions to exclude:
- Executables/binaries: `.exe`, `.dll`, `.so`, `.dylib`, `.a`, `.lib`, `.o`, `.obj`, `.pdb`
- JVM/packaging: `.class`, `.jar`, `.war`, `.ear`
- Python packaging/cache: `.whl`, `.egg`, `.pyc`, `.pyo`, `.pyd`
- Installers/images: `.msi`, `.pkg`, `.dmg`, `.iso`, `.apk`, `.ipa`
- Archives/media: `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.mp4`, `.mp3`, `.avi`, `.mov`, `.wmv`, `.flv`, `.mkv`
