from __future__ import annotations

import argparse
import logging
import os
from functools import partial
from datetime import datetime, timezone
from pathlib import Path

from migration_agents.logging_utils import setup_logging
from migration_agents.shared_multiprocessing import process_map

from .chunker import chunk_file
from .config import IngestionConfig, load_config
from .file_scanner import (
    SourceFile,
    build_source_index,
    build_source_index_parallel,
)
from .incremental import fetch_existing_checksums, filter_changed_files
from .parquet_writer import dataclass_rows, write_parquet
from migration_agents.state import finalize_state, start_state, write_state

LOGGER = logging.getLogger("migration_agents.ingestion")


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _with_metadata(
    rows: list[dict],
    config: IngestionConfig,
    created_at: str,
) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("slice_id", None)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _write_build_context(
    output_root: Path,
    config: IngestionConfig,
    created_at: str,
) -> None:
    if not config.build_context:
        return
    rows = [
        {
            "tool": entry.get("tool"),
            "version": entry.get("version"),
            "flags": entry.get("flags"),
            "env_key": entry.get("env_key"),
            "env_value": entry.get("env_value"),
            "source_ref": entry.get("source_ref", "build_context"),
        }
        for entry in config.build_context
    ]
    write_parquet(
        output_root,
        "intake_build_context",
        _with_metadata(rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )


def _write_schema_snapshot(
    output_root: Path,
    config: IngestionConfig,
    created_at: str,
) -> None:
    if not config.schema_snapshot_path:
        return
    ddl = config.schema_snapshot_path.read_text(encoding="utf-8", errors="ignore")
    rows = [
        {
            "object_type": "ddl",
            "object_name": config.schema_snapshot_path.name,
            "ddl": ddl,
            "source": str(config.schema_snapshot_path),
            "source_ref": str(config.schema_snapshot_path),
        }
    ]
    write_parquet(
        output_root,
        "intake_schema_snapshot",
        _with_metadata(rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )


def _chunk_source_item(
    item: SourceFile,
    max_lines: int,
    max_chars: int,
) -> list[dict]:
    rows: list[dict] = []
    for chunk in chunk_file(
        item.file_path,
        max_lines,
        max_chars,
        item.checksum,
    ):
        rows.append(
            {
                "file_path": str(chunk.file_path),
                "line_start": chunk.line_start,
                "line_end": chunk.line_end,
                "content": chunk.content,
                "checksum": chunk.checksum,
                "source_ref": chunk.source_ref,
            }
        )
    return rows


def _filter_incremental(files: list[SourceFile]) -> list[SourceFile]:
    if not files:
        return []
    existing = fetch_existing_checksums()
    current = {item.file_path: item.checksum for item in files}
    changed = set(filter_changed_files([item.file_path for item in files], current, existing))
    return [item for item in files if item.file_path in changed]


def _resolve_run_id(config: IngestionConfig) -> str:
    if config.run_id != "auto":
        return config.run_id
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"run_{timestamp}"


def _resolve_workers(config: IngestionConfig) -> int:
    if config.workers != "auto":
        return int(config.workers)
    # Use all available CPUs for file scanning which is I/O bound but benefits from parallelization
    return max(1, os.cpu_count() or 2)


def run(config: IngestionConfig) -> None:
    created_at = _created_at()
    run_id = _resolve_run_id(config)
    workers = _resolve_workers(config)
    config = config.model_copy(update={"run_id": run_id, "workers": workers})
    config.output_root.mkdir(parents=True, exist_ok=True)
    (config.output_root / "LATEST_RUN").write_text(run_id, encoding="utf-8")
    output_root = config.output_root / config.run_id / "step_1"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("ingestion", config.run_id, config.artifact_version)
    if config.workers > 1:
        sources = build_source_index_parallel(
            config.input_root,
            config.include_extensions,
            config.exclude_extensions,
            config.exclude_dirs,
            config.checksum_algo,
            config.workers,
        )
    else:
        sources = build_source_index(
            config.input_root,
            config.include_extensions,
            config.exclude_extensions,
            config.exclude_dirs,
            config.checksum_algo,
        )

    print(f"ingestion_sources_found={len(sources)}")
    sources_found = len(sources)
    if sources and config.incremental:
        sources = _filter_incremental(sources)
        print(f"ingestion_sources_after_incremental={len(sources)}")
    sources_after_incremental = len(sources)

    index_rows = [
        {
            "file_path": str(item.file_path),
            "language": item.language,
            "loc": item.loc,
            "module": item.module,
            "checksum": item.checksum,
            "source_ref": item.source_ref,
        }
        for item in sources
    ]

    print(f"ingestion_index_rows={len(index_rows)}")
    write_parquet(
        output_root,
        "intake_source_index",
        _with_metadata(index_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )

    chunk_rows: list[dict] = []
    if sources:
        if config.workers > 1:
            chunker = partial(
                _chunk_source_item,
                max_lines=config.max_lines_per_chunk,
                max_chars=config.max_chars_per_chunk,
            )
            chunk_batches = process_map(chunker, sources, config.workers)
            for batch in chunk_batches:
                chunk_rows.extend(batch)
        else:
            for item in sources:
                chunk_rows.extend(
                    _chunk_source_item(
                        item,
                        config.max_lines_per_chunk,
                        config.max_chars_per_chunk,
                    )
                )

    print(f"ingestion_chunk_rows={len(chunk_rows)}")
    write_parquet(
        output_root,
        "intake_source_chunks",
        _with_metadata(chunk_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )

    _write_build_context(output_root, config, created_at)
    _write_schema_snapshot(output_root, config, created_at)

    outputs = {
        "intake_source_index": len(index_rows),
        "intake_source_chunks": len(chunk_rows),
    }
    notes = {
        "sources_found": sources_found,
        "sources_after_incremental": sources_after_incremental,
        "output_root": str(output_root),
    }
    state = finalize_state(
        state,
        processed_count=sources_after_incremental,
        skipped_count=max(0, sources_found - sources_after_incremental),
        outputs=outputs,
        notes=notes,
    )
    write_state("ingestion", state)

    # Generate coverage summary for ingestion stage
    try:
        from migration_agents.coverage import generate_ingestion_coverage
        if generate_ingestion_coverage(config.output_root):
            LOGGER.info("ingestion_coverage_summary_written=1")
    except Exception as exc:
        LOGGER.warning("ingestion_coverage_summary_failed error=%s", exc)

    # Log deterministic summary
    LOGGER.info("=" * 60)
    LOGGER.info("INGESTION SUMMARY")
    LOGGER.info("=" * 60)
    LOGGER.info("ingestion_sources_found=%d", sources_found)
    LOGGER.info("ingestion_sources_processed=%d", sources_after_incremental)
    LOGGER.info("ingestion_index_rows=%d", len(index_rows))
    LOGGER.info("ingestion_chunk_rows=%d", len(chunk_rows))
    LOGGER.info("=" * 60)


def main() -> None:
    from migration_agents.constants import ensure_directories
    
    # Ensure all standard directories exist
    ensure_directories()
    
    setup_logging("ingestion")
    parser = argparse.ArgumentParser(description="Ingest legacy sources into Parquet.")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to ingestion JSON config.",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
