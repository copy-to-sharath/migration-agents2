from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import urllib.request
from urllib.error import HTTPError, URLError

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_multiprocessing import resolve_workers
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.state import finalize_state, start_state, write_state

from .config import ApiMigrationConfig, load_config

LOGGER = logging.getLogger("migration_agents.api_migration")


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _with_metadata(rows: list[dict], config: ApiMigrationConfig, created_at: str) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _prune(row: dict) -> dict:
    return {k: v for k, v in row.items() if v not in (None, "", [], {})}


def _fetch_rows(client, table: str, run_id: str, artifact_version: int) -> list[dict]:
    sql = f"""
        select *
        from {table}
        where run_id = '{run_id}' and artifact_version = {artifact_version}
    """
    try:
        return client.query(sql)
    except Exception:  # noqa: BLE001
        LOGGER.info("api_migration_missing_table table=%s", table)
        return []


def _hash_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _call_llm(config: ApiMigrationConfig, prompt: str) -> str:
    if config.llm_cmd:
        result = subprocess.run(
            config.llm_cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=config.llm_timeout_sec,
            check=True,
        )
        return result.stdout.strip()
    provider = (config.llm_provider or "copilot").lower()
    if provider in ("copilot", "github"):
        # Use GitHub/Copilot LLM via models.inference.ai.azure.com
        api_key = os.environ.get("GITHUB_TOKEN")
        if not api_key:
            raise RuntimeError("GITHUB_TOKEN environment variable is required for Copilot LLM")
        base_url = config.llm_base_url if hasattr(config, "llm_base_url") and config.llm_base_url else "https://models.inference.ai.azure.com/chat/completions"
        model = config.llm_model or "gpt-4o-mini"
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt[:config.llm_max_input_chars]}],
            "temperature": 0.2,
        }).encode("utf-8")
        request = urllib.request.Request(
            base_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
                data = json.load(response)
        except HTTPError as exc:
            raise RuntimeError(f"Copilot LLM HTTP error {exc.code}: {exc.reason}") from exc
        except URLError as exc:
            raise RuntimeError(f"Copilot LLM connection error: {exc.reason}") from exc
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("Copilot LLM response missing choices")
        return str(choices[0].get("message", {}).get("content", "")).strip()
    # Fallback to Ollama-style endpoint
    payload = json.dumps(
        {
            "model": config.llm_model,
            "prompt": prompt[: config.llm_max_input_chars],
            "stream": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        config.llm_base_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"LLM HTTP error {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"LLM connection error: {exc.reason}") from exc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("LLM unexpected error") from exc
    return str(data.get("response") or data.get("output") or "").strip()


def _validate_openapi(contract_json: str) -> bool:
    try:
        data = json.loads(contract_json)
    except json.JSONDecodeError:
        return False
    return isinstance(data, dict) and "paths" in data and isinstance(data.get("paths"), dict)


def _llm_contract_prompt(
    endpoints: list[dict],
    summaries: dict[str, str],
    brd: list[dict] | None,
    bdd: list[dict] | None,
    ddd: list[dict] | None,
) -> str:
    items = []
    for ep in endpoints:
        entry_key = ep.get("entry_key", "")
        summary = summaries.get(entry_key, "")
        items.append(
            {
                "name": ep.get("name") or entry_key or "api",
                "entry_key": entry_key,
                "summary": summary,
            }
        )
    brd_text = brd or []
    bdd_text = bdd or []
    ddd_text = ddd or []
    return (
        "You are an API architect. Given endpoints, summaries, and BRD/BDD/DDD context, emit an OpenAPI 3.0 JSON with paths and basic 200 responses. "
        "Honor the business language from BRD, flows from BDD, and domain entities from DDD. Return only JSON.\n"
        f"Endpoints: {json.dumps(items, ensure_ascii=True)}\n"
        f"BRD: {json.dumps(brd_text, ensure_ascii=True)[:2000]}\n"
        f"BDD: {json.dumps(bdd_text, ensure_ascii=True)[:2000]}\n"
        f"DDD: {json.dumps(ddd_text, ensure_ascii=True)[:2000]}"
    )


def _contract_stub(api_name: str, summary: str, source_ref: str) -> dict:
    route = f"/{api_name.lower()}"
    contract = {
        "openapi": "3.0.3",
        "info": {"title": api_name, "version": "0.1.0"},
        "paths": {
            route: {
                "get": {
                    "summary": summary or f"Get {api_name}",
                    "responses": {"200": {"description": "Success"}},
                }
            }
        },
    }
    return {
        "api_contract_id": _hash_id(f"{api_name}:{source_ref}"),
        "api_name": api_name,
        "contract_json": json.dumps(contract, ensure_ascii=True),
        "source_ref": source_ref,
    }


def run(config: ApiMigrationConfig) -> None:
    created_at = _created_at()
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    workers = resolve_workers(config.workers)
    config = config.model_copy(update={"run_id": run_id, "workers": workers})
    output_root = config.output_root / config.run_id / "step_8"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("api_migration", config.run_id, config.artifact_version)
    client = get_mcp_client()

    endpoints = _fetch_rows(client, "endpoints", config.run_id, config.artifact_version)
    entry_summaries = _fetch_rows(
        client, "entry_graph_summaries_merged", config.run_id, config.artifact_version
    )
    if not entry_summaries:
        entry_summaries = _fetch_rows(
            client, "entry_graph_summaries", config.run_id, config.artifact_version
        )
    summary_map = {
        row.get("entry_key"): row.get("summary_en", row.get("summary_en_merged", ""))
        for row in entry_summaries
        if row.get("entry_key")
    }

    contracts: list[dict] = []
    tasks: list[dict] = []
    use_llm = bool(config.llm_model or config.llm_cmd)
    llm_contracts: list[dict] = []
    if use_llm and endpoints:
        prompt = _llm_contract_prompt(endpoints, summary_map)
        for attempt in range(max(1, config.llm_max_retries + 1)):
            try:
                llm_text = _call_llm(config, prompt)
                parsed = json.loads(llm_text)
                if isinstance(parsed, dict) and "paths" in parsed:
                    llm_contracts = [parsed]
                elif isinstance(parsed, list):
                    llm_contracts = [c for c in parsed if isinstance(c, dict) and "paths" in c]
                if all(_validate_openapi(json.dumps(c, ensure_ascii=True)) for c in llm_contracts):
                    break
                llm_contracts = []
            except Exception as exc:  # noqa: BLE001
                LOGGER.warning("api_migration_llm_failed attempt=%s err=%s", attempt + 1, exc)
                llm_contracts = []

    for endpoint in endpoints:
        api_name = endpoint.get("name") or endpoint.get("entry_key") or "api"
        entry_key = endpoint.get("entry_key", "")
        summary = summary_map.get(entry_key, "")
        if use_llm and llm_contracts:
            contract_json = json.dumps(llm_contracts.pop(0), ensure_ascii=True)
            contract = {
                "api_contract_id": _hash_id(f"{api_name}:{entry_key or api_name}"),
                "api_name": api_name,
                "contract_json": contract_json,
                "source_ref": entry_key or api_name,
                "generated_by": "llm",
            }
        else:
            contract = _contract_stub(api_name, summary, entry_key or api_name)
        contracts.append(_prune(contract))
        tasks.append(
            _prune(
                {
                    "task_id": _hash_id(f"{api_name}:{entry_key}"),
                    "api_contract_id": contract["api_contract_id"],
                    "api_name": api_name,
                    "status": "pending",
                    "source_ref": contract["source_ref"],
                }
            )
        )

    if config.max_contracts is not None:
        contracts = contracts[: max(0, config.max_contracts)]
        tasks = tasks[: len(contracts)]

    status_row = {
        "total_contracts": len(contracts),
        "pending_contracts": len(contracts),
        "source_ref": "api_migration",
    }

    if contracts:
        write_parquet(
            output_root,
            "api_contracts",
            _with_metadata(contracts, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if tasks:
        write_parquet(
            output_root,
            "migration_tasks",
            _with_metadata(tasks, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if contracts or tasks:
        write_parquet(
            output_root,
            "migration_status",
            _with_metadata([_prune(status_row)], config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )

    state = finalize_state(
        state,
        processed_count=len(contracts),
        outputs={
            "api_contracts": len(contracts),
            "migration_tasks": len(tasks),
            "migration_status": 1,
        },
        notes={"output_root": str(output_root)},
    )
    write_state("api_migration", state)
    LOGGER.info("api_migration_done contracts=%d", len(contracts))


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 8 API Migration pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("api_migration")
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
