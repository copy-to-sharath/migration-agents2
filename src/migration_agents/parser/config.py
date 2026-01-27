from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from migration_agents.constants import DEFAULT_PATHS


class ParserConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    language_library_path: Path
    language_map: dict[str, str]
    queries_dir: Path
    workers: int | Literal["auto"] = "auto"
    roslyn_languages: list[str] = Field(default_factory=lambda: ["c_sharp", "vbnet"])
    roslyn_cmd: list[str] | None = None
    roslyn_timeout_sec: int = Field(ge=1, le=600000000, default=60)
    roslyn_parquet_root: Path | None = None
    roslyn_parquet_run_id: str | None = None
    max_label_chars: int = Field(ge=20, le=500, default=200)
    entry_graph_max_depth: int = Field(ge=1, default=200)
    entry_graph_node_limit: int = Field(ge=10, le=200000000, default=200000000)
    entry_graph_depth_threshold: int = Field(ge=0, le=2000000, default=2000000)
    entry_graph_top_k: int | None = Field(default=None)
    entry_graph_incremental: bool = Field(default=True)
    entry_graph_render_dot: bool = Field(default=True)
    entry_graph_render_png: bool = Field(default=False)
    entry_graph_render_dir: Path = DEFAULT_PATHS.ENTRY_GRAPHS_DIR
    entry_graph_render_svg: bool = Field(default=False)
    entry_graph_render_engine: str = Field(default="sfdp")
    entry_graph_render_full: bool = Field(default=True)
    entry_graph_render_by_depth: bool = Field(default=False)
    entry_graph_min_depth: int = Field(ge=0, le=200, default=2)
    llm_cmd: list[str] = Field(default_factory=list)
    llm_provider: str = Field(default="copilot")  # copilot, github, ollama, cmd
    llm_model: str = Field(default="gpt-4o-mini")
    llm_base_url: str = Field(default="http://localhost:11434")
    llm_timeout_sec: int = Field(ge=1, le=1800, default=120)
    llm_max_input_chars: int = Field(ge=1, le=2000000, default=8000)
    entry_graph_llm_batch_size: int = Field(ge=1, le=50, default=5)
    entry_graph_llm_strict: bool = Field(default=False)
    entry_graph_llm_debug: bool = Field(default=False)
    entry_graph_llm_log_response: bool = Field(default=False)
    entry_graph_llm_store_response: bool = Field(default=False)
    entry_graph_llm_merge_enabled: bool = Field(default=False)
    entry_graph_llm_merge_join: str = Field(default="\\n\\n")
    entry_graph_llm_merge_max_chars: int = Field(ge=1000, le=1000000, default=200000)
    auto_ingest_if_missing: bool = Field(default=False)
    ingestion_config_path: Path | None = None
    auto_build_languages_if_missing: bool = Field(default=False)
    tree_sitter_languages_config_path: Path | None = None
    entry_graph_summary_fields: dict[str, bool] = Field(default_factory=lambda: {
        "actor_hints": True,
        "business_rule_hint": True,
        "language_tags": True,
        "rank": True,
    })

    @field_validator(
        "output_root",
        "language_library_path",
        "queries_dir",
        "entry_graph_render_dir",
        "ingestion_config_path",
        "tree_sitter_languages_config_path",
    )
    @classmethod
    def _normalize_path(cls, value: Path | None) -> Path | None:
        if value is None:
            return value
        return value.expanduser().resolve()

    @field_validator("language_map")
    @classmethod
    def _normalize_language_map(cls, value: dict[str, str]) -> dict[str, str]:
        if not value:
            raise ValueError("language_map must not be empty")
        normalized: dict[str, str] = {}
        for ext, name in value.items():
            key = ext if ext.startswith(".") else f".{ext}"
            normalized[key] = name
        return normalized

    @field_validator("workers")
    @classmethod
    def _normalize_workers(cls, value: int | str) -> int | str:
        if isinstance(value, str) and value != "auto":
            raise ValueError("workers must be an integer or 'auto'")
        return value


def load_config(path: Path) -> ParserConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, ParserConfig)
