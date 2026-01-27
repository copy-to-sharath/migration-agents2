from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class LogicManifesterConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    workers: int | Literal["auto"] = "auto"
    max_rule_text_chars: int = Field(ge=50, le=5000, default=800)
    max_trace_refs_per_rule: int = Field(ge=1, le=10000, default=200)

    @field_validator("output_root")
    @classmethod
    def _normalize_path(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        return value.expanduser().resolve()

    @field_validator("workers")
    @classmethod
    def _normalize_workers(cls, value: int | str) -> int | str:
        if isinstance(value, str) and value != "auto":
            raise ValueError("workers must be an integer or 'auto'")
        return value


def load_config(path: Path) -> LogicManifesterConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, LogicManifesterConfig)
