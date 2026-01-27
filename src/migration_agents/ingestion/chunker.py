from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .doc_extractor import extract_text

@dataclass(frozen=True)
class SourceChunk:
    file_path: Path
    line_start: int
    line_end: int
    content: str
    checksum: str
    source_ref: str


def chunk_file(
    file_path: Path,
    max_lines: int,
    max_chars: int,
    checksum: str,
) -> Iterable[SourceChunk]:
    text = extract_text(file_path)
    lines = text.splitlines()
    if not lines:
        return []
    chunks: list[SourceChunk] = []
    start = 1
    buffer: list[str] = []
    for idx, line in enumerate(lines, start=1):
        buffer.append(line)
        if len(buffer) >= max_lines or sum(len(s) for s in buffer) >= max_chars:
            end = idx
            content = "\n".join(buffer)
            source_ref = f"{file_path}:{start}-{end}"
            chunks.append(
                SourceChunk(
                    file_path=file_path,
                    line_start=start,
                    line_end=end,
                    content=content,
                    checksum=checksum,
                    source_ref=source_ref,
                )
            )
            buffer = []
            start = idx + 1
    if buffer:
        end = len(lines)
        content = "\n".join(buffer)
        source_ref = f"{file_path}:{start}-{end}"
        chunks.append(
            SourceChunk(
                file_path=file_path,
                line_start=start,
                line_end=end,
                content=content,
                checksum=checksum,
                source_ref=source_ref,
            )
        )
    return chunks
