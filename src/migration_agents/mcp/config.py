from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class MCPConfig(BaseModel):
    parquet_root: Path
    duckdb_dir: Path = Field(default=Path("data/duckdb"))
    max_rows: int = Field(ge=1, le=100000, default=2000)

    @field_validator("parquet_root", "duckdb_dir")
    @classmethod
    def _normalize_path(cls, value: Path) -> Path:
        return value.expanduser().resolve()


def load_config(path: Path) -> MCPConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return MCPConfig.model_validate(raw)
