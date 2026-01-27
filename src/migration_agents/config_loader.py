from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from migration_agents.constants import DEFAULT_PARQUET_ROOT

T = TypeVar("T", bound=BaseModel)

# Default values for all configs
_DEFAULTS: dict[str, Any] = {
    "run_id": "auto",
    "artifact_version": 1,
    "output_root": DEFAULT_PARQUET_ROOT,
}


def load_with_global(path: Path, model_cls: type[T]) -> T:
    """Load config with defaults from constants."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    
    # Apply defaults for missing fields
    allowed = set(model_cls.model_fields.keys())
    merged: dict[str, Any] = {
        key: value for key, value in _DEFAULTS.items() if key in allowed
    }
    merged.update({key: value for key, value in raw.items() if key in allowed})
    return model_cls.model_validate(merged)
