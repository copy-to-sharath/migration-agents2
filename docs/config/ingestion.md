# Ingestion Config

Local config for the ingestion stage. Use `config/ingestion.json` as the primary source.

## Parameters
- `input_root`: path to the legacy code/documents.
- `include_extensions`: list of allowed extensions.
- `exclude_extensions`: list of excluded extensions.
- `exclude_dirs`: folders to skip.
- `incremental`: enable checksum-based incremental ingestion.
- `checksum_algo`: checksum algorithm (e.g., `sha256`).
- `workers`: `auto` or explicit worker count.
- `run_id`, `artifact_version`, `output_root`: use global defaults if not set.
