from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class KnowledgeBaseConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    workers: int | Literal["auto"] = "auto"
    knowledge_input_path: Path | None = None

    @field_validator("output_root", "knowledge_input_path")
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


def load_config(path: Path) -> KnowledgeBaseConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, KnowledgeBaseConfig)
