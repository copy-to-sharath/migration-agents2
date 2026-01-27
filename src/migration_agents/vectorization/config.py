from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class VectorizationConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    workers: int | Literal["auto"] = "auto"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_batch_size: int = Field(default=32, ge=1, le=512)
    max_items: int | None = None
    include_enriched_sources: bool = True
    embedding_provider: Literal["local", "http"] = "local"
    embedding_http_url: str | None = None
    embedding_http_timeout_sec: int = Field(default=60, ge=5, le=600)
    embedding_http_headers: dict[str, str] | None = None

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


def load_config(path: Path) -> VectorizationConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, VectorizationConfig)
