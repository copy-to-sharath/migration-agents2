from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime, timezone
from functools import partial
from pathlib import Path

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_multiprocessing import process_map, resolve_workers
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.state import finalize_state, start_state, write_state

from .config import KnowledgeBaseConfig, load_config

LOGGER = logging.getLogger("migration_agents.knowledge_base")


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _with_metadata(rows: list[dict], config: KnowledgeBaseConfig, created_at: str) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _fetch_rows(client, table: str, run_id: str, artifact_version: int) -> list[dict]:
    sql = f"""
        select *
        from {table}
        where run_id = '{run_id}' and artifact_version = {artifact_version}
    """
    try:
        return client.query(sql)
    except Exception:  # noqa: BLE001
        LOGGER.info("knowledge_base_missing_table table=%s", table)
        return []


def _build_short_term_row(row: dict) -> dict | None:
    summary_en = row.get("summary_en") or row.get("summary_en_merged") or ""
    summary_math = row.get("summary_math") or row.get("summary_math_merged") or ""
    text = f"{summary_en}\n{summary_math}".strip()
    if not text:
        return None
    return {
        "knowledge_id": row.get("entry_key") or row.get("merge_key") or "",
        "title": "Entry graph summary",
        "text": text,
        "source_ref": row.get("source_ref", "entry_graph_summaries"),
    }


def _build_episodic_row(row: dict) -> dict | None:
    logic_comment = row.get("logic_comment", "")
    indicative = row.get("indicative_result", "")
    text = f"{logic_comment}\n{indicative}".strip()
    if not text:
        return None
    return {
        "knowledge_id": row.get("rule_id", ""),
        "title": "Domain insight",
        "text": text,
        "source_ref": row.get("source_ref", "domain_insights"),
    }


def _build_long_term_row(row: dict) -> dict | None:
    name = row.get("name") or row.get("context_name") or row.get("aggregate_name") or ""
    invariants = row.get("invariants", "")
    text = f"{name}\n{invariants}".strip()
    if not text:
        return None
    return {
        "knowledge_id": row.get("entity_id") or row.get("vo_id") or row.get("aggregate_id") or "",
        "title": "Domain concept",
        "text": text,
        "source_ref": row.get("source_ref", "domain_entities"),
    }


def _load_seed(path: Path) -> tuple[list[dict], list[dict], list[dict]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload, [], []
    if not isinstance(payload, dict):
        raise ValueError("knowledge_input_path must be a list or dict")
    return (
        payload.get("short_term", []),
        payload.get("episodic", []),
        payload.get("long_term", []),
    )


def run(config: KnowledgeBaseConfig) -> None:
    created_at = _created_at()
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    workers = resolve_workers(config.workers)
    config = config.model_copy(update={"run_id": run_id, "workers": workers})
    output_root = config.output_root / config.run_id / "step_7"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("knowledge_base", config.run_id, config.artifact_version)
    LOGGER.info(
        "knowledge_base_start run_id=%s workers=%s",
        config.run_id,
        config.workers,
    )

    short_term: list[dict] = []
    episodic: list[dict] = []
    long_term: list[dict] = []

    if config.knowledge_input_path:
        short_term, episodic, long_term = _load_seed(config.knowledge_input_path)
    else:
        client = get_mcp_client()
        entry_rows = _fetch_rows(client, "entry_graph_summaries_merged", config.run_id, config.artifact_version)
        if not entry_rows:
            entry_rows = _fetch_rows(client, "entry_graph_summaries", config.run_id, config.artifact_version)
        insight_rows = _fetch_rows(client, "domain_insights", config.run_id, config.artifact_version)
        entity_rows = _fetch_rows(client, "domain_entities", config.run_id, config.artifact_version)
        vo_rows = _fetch_rows(client, "value_objects", config.run_id, config.artifact_version)
        aggregate_rows = _fetch_rows(client, "aggregates", config.run_id, config.artifact_version)
        context_rows = _fetch_rows(client, "context_map", config.run_id, config.artifact_version)

        short_term = [
            row for row in process_map(_build_short_term_row, entry_rows, workers) if row
        ]
        episodic = [
            row for row in process_map(_build_episodic_row, insight_rows, workers) if row
        ]
        long_term_inputs = entity_rows + vo_rows + aggregate_rows + context_rows
        long_term = [
            row for row in process_map(_build_long_term_row, long_term_inputs, workers) if row
        ]

    write_parquet(
        output_root,
        "knowledge_base_short_term",
        _with_metadata(short_term, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "knowledge_base_episodic",
        _with_metadata(episodic, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "knowledge_base_long_term",
        _with_metadata(long_term, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    state = finalize_state(
        state,
        processed_count=len(short_term) + len(episodic) + len(long_term),
        outputs={
            "knowledge_base_short_term": len(short_term),
            "knowledge_base_episodic": len(episodic),
            "knowledge_base_long_term": len(long_term),
        },
        notes={"output_root": str(output_root)},
    )
    write_state("knowledge_base", state)
    LOGGER.info(
        "knowledge_base_done short_term=%d episodic=%d long_term=%d",
        len(short_term),
        len(episodic),
        len(long_term),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 7 Knowledge Base pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("knowledge_base")
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
