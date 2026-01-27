from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .mcp_client import get_mcp_client


def fetch_existing_checksums() -> dict[str, str]:
    client = get_mcp_client()
    sql = """
        select file_path, checksum
        from intake_source_index
    """
    try:
        rows = client.query(sql)
    except Exception:
        return {}
    return {row["file_path"]: row["checksum"] for row in rows}


def filter_changed_files(
    file_paths: Iterable[Path],
    current_checksums: dict[Path, str],
    existing_checksums: dict[str, str],
) -> list[Path]:
    changed: list[Path] = []
    for path in file_paths:
        current = current_checksums[path]
        previous = existing_checksums.get(str(path))
        if previous != current:
            changed.append(path)
    return changed
