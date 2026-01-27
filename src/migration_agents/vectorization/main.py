from __future__ import annotations

import argparse
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from functools import partial
import urllib.request
from urllib.error import HTTPError, URLError

from sentence_transformers import SentenceTransformer

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_multiprocessing import process_map, resolve_workers
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.state import finalize_state, start_state, write_state

from .config import VectorizationConfig, load_config

LOGGER = logging.getLogger("migration_agents.vectorization")


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _with_metadata(rows: list[dict], config: VectorizationConfig, created_at: str) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _fetch_rows(client, table: str, run_id: str, artifact_version: int) -> list[dict]:
    sql = f"""
        select *
        from {table}
        where run_id = '{run_id}' and artifact_version = {artifact_version}
    """
    try:
        return client.query(sql)
    except Exception:  # noqa: BLE001
        LOGGER.info("vectorization_missing_table table=%s", table)
        return []


def _build_input_row(row: dict, record_type: str) -> dict | None:
    if record_type == "symbol":
        name = row.get("name") or row.get("signature") or row.get("symbol_id")
        symbol_type = row.get("symbol_type", "")
        file_path = row.get("file_path", "")
        text = f"symbol {name} {symbol_type} {file_path}".strip()
        record_id = row.get("symbol_id", "")
    elif record_type == "call":
        caller = row.get("caller_id", "")
        callee = row.get("callee_id", "")
        text = f"call {caller} -> {callee}".strip()
        record_id = _hash_text(f"{caller}:{callee}:{row.get('source_ref', '')}")
    elif record_type == "condition":
        predicate = row.get("predicate", "")
        text = f"condition {predicate}".strip()
        record_id = row.get("symbol_id", "")
    elif record_type == "constant":
        name = row.get("name", "")
        value = row.get("value", "")
        text = f"constant {name} = {value}".strip()
        record_id = _hash_text(f"{name}:{row.get('source_ref', '')}")
    elif record_type == "data_access":
        op = row.get("op", "")
        table = row.get("table_name", "")
        sql_text = row.get("sql_text", "")
        text = f"data_access {op} {table} {sql_text}".strip()
        record_id = row.get("symbol_id", "")
    elif record_type == "entry_graph":
        summary_en = row.get("summary_en") or row.get("summary_en_merged") or ""
        summary_math = row.get("summary_math") or row.get("summary_math_merged") or ""
        text = f"{summary_en}\n{summary_math}".strip()
        record_id = row.get("entry_key") or row.get("merge_key") or ""
    elif record_type == "slice_context":
        summary = row.get("summary", "")
        risks = row.get("risks", "")
        assumptions = row.get("assumptions", "")
        text = f"{summary}\n{risks}\n{assumptions}".strip()
        record_id = row.get("slice_id", "")
    elif record_type == "slice_source_ref":
        excerpt = row.get("excerpt", "")
        file_path = row.get("file_path", "")
        line = row.get("line", "")
        text = f"source_ref {file_path}:{line}\n{excerpt}".strip()
        record_id = _hash_text(f"{file_path}:{line}:{row.get('source_ref', '')}")
    elif record_type == "logic_rule":
        rule_text = row.get("rule_text", "")
        inputs = row.get("inputs", "")
        outputs = row.get("outputs", "")
        invariants = row.get("invariants", "")
        text = f"{rule_text}\ninputs: {inputs}\noutputs: {outputs}\ninvariants: {invariants}".strip()
        record_id = row.get("rule_id", "")
    elif record_type == "logic_edge":
        rule_id = row.get("rule_id", "")
        symbol_id = row.get("symbol_id", "")
        evidence = row.get("evidence", "")
        text = f"logic_edge {rule_id} -> {symbol_id} {evidence}".strip()
        record_id = _hash_text(f"{rule_id}:{symbol_id}:{row.get('source_ref', '')}")
    elif record_type == "domain_insight":
        logic_comment = row.get("logic_comment", "")
        indicative = row.get("indicative_result", "")
        text = f"{logic_comment}\n{indicative}".strip()
        record_id = row.get("rule_id", "")
    elif record_type == "graph_node":
        label = row.get("label", "")
        node_type = row.get("node_type", "")
        source_ref = row.get("source_ref", "")
        text = f"node {node_type} {label} {source_ref}".strip()
        record_id = row.get("node_id", "")
    else:
        return None

    if not text:
        return None
    return {
        "record_type": record_type,
        "record_id": record_id or _hash_text(text),
        "text": text,
        "source_ref": row.get("source_ref", record_id or "vectorization"),
    }


def _build_input_row_worker(row: dict, record_type: str) -> dict | None:
    return _build_input_row(row, record_type)


def _prepare_inputs(config: VectorizationConfig, run_id: str) -> list[dict]:
    client = get_mcp_client()
    inputs: list[dict] = []

    table_map = [
        ("symbols", "symbol"),
        ("calls", "call"),
        ("conditions", "condition"),
        ("constants", "constant"),
        ("data_access", "data_access"),
        ("entry_graph_summaries_merged", "entry_graph"),
        ("entry_graph_summaries", "entry_graph"),
        ("code_graph_nodes", "graph_node"),
    ]
    if config.include_enriched_sources:
        table_map.extend(
            [
                ("slice_context", "slice_context"),
                ("slice_source_refs", "slice_source_ref"),
                ("logic_rules", "logic_rule"),
                ("logic_edges", "logic_edge"),
                ("domain_insights", "domain_insight"),
            ]
        )
    for table, record_type in table_map:
        rows = _fetch_rows(client, table, run_id, config.artifact_version)
        if not rows:
            continue
        worker = partial(_build_input_row_worker, record_type=record_type)
        processed = process_map(worker, rows, resolve_workers(config.workers))
        inputs.extend([row for row in processed if row])

    if config.max_items is not None:
        inputs = inputs[: max(0, config.max_items)]
    return inputs


def _encode_local(model_name: str, texts: list[str], batch_size: int) -> tuple[list[list[float]], int]:
    model = SentenceTransformer(model_name)
    vectors = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    dim = int(vectors.shape[1]) if len(vectors.shape) > 1 else 0
    return [vec.tolist() for vec in vectors], dim


def _encode_http(
    url: str,
    texts: list[str],
    batch_size: int,
    timeout_sec: int,
    headers: dict[str, str] | None,
) -> tuple[list[list[float]], int]:
    if not url:
        raise ValueError("embedding_http_url is required for http provider")
    payload_headers = {"Content-Type": "application/json"}
    if headers:
        payload_headers.update(headers)
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        payload = {"model": "default", "texts": batch}
        request = urllib.request.Request(
            url,
            data=json.dumps(payload, ensure_ascii=True).encode("utf-8"),
            headers=payload_headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_sec) as response:
                data = json.load(response)
        except HTTPError as exc:
            raise RuntimeError(f"HTTP embedding error {exc.code}: {exc.reason}") from exc
        except URLError as exc:
            raise RuntimeError(f"HTTP embedding connection error: {exc.reason}") from exc
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("HTTP embedding unexpected error") from exc

        if isinstance(data, dict):
            if "embeddings" in data:
                batch_embeddings = data["embeddings"]
            elif "data" in data and isinstance(data["data"], list):
                batch_embeddings = [item.get("embedding") for item in data["data"] if "embedding" in item]
            else:
                raise ValueError("Unexpected embedding response dict format")
        elif isinstance(data, list):
            batch_embeddings = data
        else:
            raise ValueError("Unexpected embedding response format")

        if not isinstance(batch_embeddings, list):
            raise ValueError("Embedding response must be a list")
        embeddings.extend(batch_embeddings)
    dim = len(embeddings[0]) if embeddings else 0
    return embeddings, dim


def run(config: VectorizationConfig) -> None:
    created_at = _created_at()
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    workers = resolve_workers(config.workers)
    config = config.model_copy(update={"run_id": run_id, "workers": workers})
    output_root = config.output_root / config.run_id / "step_5"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("vectorization", config.run_id, config.artifact_version)
    LOGGER.info(
        "vectorization_start run_id=%s model=%s batch_size=%s workers=%s",
        config.run_id,
        config.embedding_model,
        config.embedding_batch_size,
        config.workers,
    )

    inputs = _prepare_inputs(config, config.run_id)
    if not inputs:
        LOGGER.info("vectorization_no_inputs run_id=%s", config.run_id)
        state = finalize_state(
            state,
            processed_count=0,
            outputs={"vector_embeddings": 0, "vector_metadata": 0},
            notes={"output_root": str(output_root)},
        )
        write_state("vectorization", state)
        return
    texts = [item["text"] for item in inputs]
    if config.embedding_provider == "http":
        if not config.embedding_http_url:
            raise ValueError("embedding_http_url is required when embedding_provider='http'")
        vectors, dim = _encode_http(
            config.embedding_http_url or "",
            texts,
            config.embedding_batch_size,
            config.embedding_http_timeout_sec,
            config.embedding_http_headers,
        )
    else:
        vectors, dim = _encode_local(
            config.embedding_model,
            texts,
            config.embedding_batch_size,
        )

    embedding_rows: list[dict] = []
    for item, vector in zip(inputs, vectors, strict=False):
        text_hash = _hash_text(item["text"])
        embedding_rows.append(
            {
                "record_type": item["record_type"],
                "record_id": item["record_id"],
                "embedding": vector,
                "embedding_dim": dim,
                "text_hash": text_hash,
                "source_ref": item["source_ref"],
            }
        )

    meta_rows = [
        {
            "model": config.embedding_model,
            "embedding_dim": dim,
            "item_count": len(embedding_rows),
            "source_ref": "vector_metadata",
        }
    ]
    write_parquet(
        output_root,
        "vector_embeddings",
        _with_metadata(embedding_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "vector_metadata",
        _with_metadata(meta_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    state = finalize_state(
        state,
        processed_count=len(embedding_rows),
        outputs={"vector_embeddings": len(embedding_rows), "vector_metadata": len(meta_rows)},
        notes={
            "input_records": len(inputs),
            "embedding_dim": dim,
            "include_enriched_sources": config.include_enriched_sources,
            "embedding_provider": config.embedding_provider,
            "output_root": str(output_root),
        },
    )
    write_state("vectorization", state)
    LOGGER.info("vectorization_done embeddings=%s", len(embedding_rows))


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 2 Vectorization pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("vectorization")
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
