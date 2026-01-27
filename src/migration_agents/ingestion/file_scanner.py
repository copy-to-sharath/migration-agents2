from __future__ import annotations

import hashlib
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Iterable
from migration_agents.shared_multiprocessing import process_map

from .doc_extractor import extract_text


@dataclass(frozen=True)
class SourceFile:
    file_path: Path
    language: str
    loc: int
    module: str
    checksum: str
    source_ref: str


def detect_language(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".cs": "csharp",
        ".sql": "sql",
        ".java": "java",
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".vb": "vbnet",
        ".cob": "cobol",
        ".md": "markdown",
        ".rst": "rst",
        ".adoc": "asciidoc",
        ".txt": "text",
        ".pdf": "pdf",
        ".docx": "docx",
    }
    return mapping.get(ext, "unknown")


def _hash_file(path: Path, algo: str) -> str:
    hasher = hashlib.new(algo)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def iter_source_files(
    input_root: Path,
    include_extensions: list[str],
    exclude_extensions: list[str],
    exclude_dirs: list[str],
) -> Iterable[Path]:
    exclude_set = {Path(name).name for name in exclude_dirs}
    for path in input_root.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if "*" not in include_extensions and suffix not in include_extensions:
            continue
        if suffix in exclude_extensions:
            continue
        if any(part in exclude_set for part in path.parts):
            continue
        yield path


def build_source_index(
    input_root: Path,
    include_extensions: list[str],
    exclude_extensions: list[str],
    exclude_dirs: list[str],
    checksum_algo: str,
) -> list[SourceFile]:
    file_paths = list(
        iter_source_files(input_root, include_extensions, exclude_extensions, exclude_dirs)
    )
    return [_scan_file(path, checksum_algo) for path in file_paths]


def build_source_index_parallel(
    input_root: Path,
    include_extensions: list[str],
    exclude_extensions: list[str],
    exclude_dirs: list[str],
    checksum_algo: str,
    workers: int,
) -> list[SourceFile]:
    file_paths = list(
        iter_source_files(input_root, include_extensions, exclude_extensions, exclude_dirs)
    )
    if not file_paths:
        return []
    scan = partial(_scan_file, checksum_algo=checksum_algo)
    return process_map(scan, file_paths, workers)


def _scan_file(path: Path, checksum_algo: str) -> SourceFile:
    text = extract_text(path)
    loc = text.count("\n") + 1 if text else 0
    return SourceFile(
        file_path=path,
        language=detect_language(path),
        loc=loc,
        module=path.parent.name,
        checksum=_hash_file(path, checksum_algo),
        source_ref=str(path),
    )
