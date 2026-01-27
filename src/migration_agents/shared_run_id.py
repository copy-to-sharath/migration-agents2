from __future__ import annotations

from pathlib import Path


def resolve_run_id(output_root: Path) -> str:
    latest_file = output_root / "LATEST_RUN"
    if latest_file.exists():
        value = latest_file.read_text(encoding="utf-8").strip()
        if value:
            return value
    if not output_root.exists():
        raise RuntimeError("No runs found; output_root does not exist")
    candidates = [path.name for path in output_root.iterdir() if path.is_dir()]
    if not candidates:
        raise RuntimeError("No runs found under output_root")
    return sorted(candidates)[-1]
