from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SliceExtractorConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    workers: int | Literal["auto"] = "auto"
    max_source_refs_per_slice: int = Field(ge=1, le=10000, default=200)
    max_excerpt_chars: int = Field(ge=20, le=5000, default=500)
    slicing_mode: Literal["auto", "entry_graph", "community"] = "auto"
    """Slicing strategy: 'auto' uses entry_graphs if available, else community.
    'entry_graph' forces entry-based slicing, 'community' forces community detection."""
    
    # Entry point filtering options
    entry_filter_top_level_only: bool = True
    """Only include top-level entry points (not called by other entries)."""
    entry_filter_min_depth: int = 2
    """Minimum call graph depth to qualify as a slice."""
    entry_filter_kinds: list[str] = Field(default_factory=lambda: ["method", "function", "http_endpoint"])
    """Symbol kinds to include as entry points (e.g., method, function, class)."""
    entry_filter_patterns: list[str] = Field(default_factory=lambda: [
        "Page_Load", "_Load", "Controller", "Handler", "Process", "Execute",
        "Main", "Run", "Start", "Init", "Button_Click", "_Click", "Service"
    ])
    """Name patterns that indicate top-level entry points."""

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


def load_config(path: Path) -> SliceExtractorConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, SliceExtractorConfig)
