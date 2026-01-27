from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class IngestionConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    input_root: Path
    output_root: Path
    include_extensions: list[str]
    exclude_extensions: list[str] = Field(default_factory=list)
    exclude_dirs: list[str] = Field(default_factory=list)
    max_lines_per_chunk: int = Field(ge=1, le=5000)
    max_chars_per_chunk: int = Field(ge=100, le=200000)
    checksum_algo: Literal["sha256"] = "sha256"
    workers: int | Literal["auto"] = "auto"
    incremental: bool = True
    build_context: list[dict[str, str]] | None = None
    schema_snapshot_path: Path | None = None

    @field_validator("input_root", "output_root")
    @classmethod
    def _normalize_path(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        return value.expanduser().resolve()

    @field_validator("schema_snapshot_path")
    @classmethod
    def _normalize_optional_path(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        return value.expanduser().resolve()

    @field_validator("include_extensions")
    @classmethod
    def _normalize_extensions(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("include_extensions must not be empty")
        if "*" in value:
            return ["*"]
        return [ext if ext.startswith(".") else f".{ext}" for ext in value]

    @field_validator("exclude_extensions")
    @classmethod
    def _normalize_exclude_extensions(cls, value: list[str]) -> list[str]:
        return [ext if ext.startswith(".") else f".{ext}" for ext in value]

    @field_validator("workers")
    @classmethod
    def _normalize_workers(cls, value: int | str) -> int | str:
        if isinstance(value, str) and value != "auto":
            raise ValueError("workers must be an integer or 'auto'")
        return value


def load_config(path: Path) -> IngestionConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, IngestionConfig)
