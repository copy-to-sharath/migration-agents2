from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ApiMigrationConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    workers: int | Literal["auto"] = "auto"
    max_contracts: int | None = None
    llm_provider: Literal["copilot", "ollama", "cmd"] = "copilot"
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = "http://localhost:11434/api/generate"
    llm_cmd: list[str] | None = None
    llm_timeout_sec: int = Field(default=60, ge=5, le=600)
    llm_max_input_chars: int = Field(default=6000, ge=512, le=20000)
    llm_max_retries: int = Field(default=2, ge=0, le=5)

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


def load_config(path: Path) -> ApiMigrationConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, ApiMigrationConfig)
