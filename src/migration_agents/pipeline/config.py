from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, field_validator


class PipelineConfig(BaseModel):
    stages: list[str] = [
        "ingestion",
        "parser",
        "vectorization",
        "slice_extractor",
        "logic_manifester",
        "domain_architect",
        "knowledge_base",
        "api_migration",
        "codegen",
    ]
    ingestion_config: Path | None = None
    parser_config: Path | None = None
    vectorization_config: Path | None = None
    slice_extractor_config: Path | None = None
    logic_manifester_config: Path | None = None
    domain_architect_config: Path | None = None
    knowledge_base_config: Path | None = None
    api_migration_config: Path | None = None
    codegen_config: Path | None = None

    @field_validator(
        "ingestion_config",
        "parser_config",
        "vectorization_config",
        "slice_extractor_config",
        "logic_manifester_config",
        "domain_architect_config",
        "knowledge_base_config",
        "api_migration_config",
        "codegen_config",
    )
    @classmethod
    def _normalize_path(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        return value.expanduser().resolve()


def load_config(path: Path) -> PipelineConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Pipeline config must be a JSON object")
    return PipelineConfig(**data)
