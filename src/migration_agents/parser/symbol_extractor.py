from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable

from tree_sitter import Language, Node, Query, QueryCursor


@dataclass(frozen=True)
class SymbolRow:
    symbol_id: str
    name: str
    kind: str
    signature: str
    file_path: str
    line: int
    source_ref: str


def extract_symbols(
    language: Language,
    tree,
    query_text: str,
    file_path: str,
    source_ref: str,
) -> Iterable[SymbolRow]:
    if not query_text:
        return []
    query = Query(language, query_text)
    cursor = QueryCursor(query)
    captures = cursor.captures(tree.root_node)
    rows: list[SymbolRow] = []
    for capture_name, nodes in captures.items():
        if capture_name != "name":
            continue
        for node in nodes:
            name = _node_text(node)
            if not name:
                continue
            line = node.start_point[0] + 1
            symbol_id = _hash_symbol(file_path, name, line)
            rows.append(
                SymbolRow(
                    symbol_id=symbol_id,
                    name=name,
                    kind=node.type,
                    signature="",
                    file_path=file_path,
                    line=line,
                    source_ref=source_ref,
                )
            )
    return rows


def _node_text(node: Node) -> str:
    try:
        return node.text.decode("utf-8", errors="ignore")
    except AttributeError:
        return ""


def _hash_symbol(file_path: str, name: str, line: int) -> str:
    raw = f"{file_path}:{line}:{name}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
