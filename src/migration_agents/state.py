from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from migration_agents.constants import DEFAULT_PATHS

STATE_DIR = DEFAULT_PATHS.STATE_DIR


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state(stage: str) -> dict[str, Any]:
    path = STATE_DIR / f"{stage}.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_state(stage: str, payload: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{stage}.json"
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def start_state(stage: str, run_id: str, artifact_version: int) -> dict[str, Any]:
    return {
        "stage": stage,
        "run_id": run_id,
        "artifact_version": artifact_version,
        "started_at": _timestamp(),
        "status": "running",
    }


def finalize_state(
    state: dict[str, Any],
    *,
    processed_count: int | None = None,
    skipped_count: int | None = None,
    error_count: int | None = None,
    outputs: dict[str, int] | None = None,
    notes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = dict(state)
    if processed_count is not None:
        state["processed_count"] = processed_count
    if skipped_count is not None:
        state["skipped_count"] = skipped_count
    if error_count is not None:
        state["error_count"] = error_count
    if outputs is not None:
        state["outputs"] = outputs
    if notes is not None:
        state["notes"] = notes
    state["finished_at"] = _timestamp()
    state["status"] = "finished"
    return state
