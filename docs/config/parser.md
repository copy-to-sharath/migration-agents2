# Parser Config

Local config for the parser stage. Use `config/parser.example.json` (or Windows variant).

## Parameters
- `language_library_path`: compiled tree-sitter library path.
- `language_map`: extension → language name.
- `queries_dir`: tree-sitter query folder.
- `entry_graph_*`: entry graph depth/limits/render options.
- `llm_*`: LLM configuration and debug options.
- `auto_ingest_if_missing`: run ingestion if `intake_source_chunks` is missing.
- `auto_build_languages_if_missing`: build `languages.so`/`languages.dll` if missing.
- `run_id`, `artifact_version`, `output_root`: use global defaults if not set.
