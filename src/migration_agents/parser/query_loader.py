from __future__ import annotations

from pathlib import Path


def load_query(queries_dir: Path, language_name: str, suffix: str) -> str:
    if suffix == "symbols":
        path = queries_dir / f"{language_name}.scm"
    else:
        path = queries_dir / f"{language_name}.{suffix}.scm"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
