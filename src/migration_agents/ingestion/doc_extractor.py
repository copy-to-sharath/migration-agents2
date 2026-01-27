from __future__ import annotations

from pathlib import Path

from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix == ".docx":
        return _extract_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_pdf(path: Path) -> str:
    try:
        return extract_pdf_text(str(path))
    except Exception:
        return ""


def _extract_docx(path: Path) -> str:
    try:
        doc = Document(str(path))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    except Exception:
        return ""
