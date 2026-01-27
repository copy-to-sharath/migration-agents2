from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable

from tree_sitter import Language, Query, QueryCursor

SQL_KEYWORDS = ("select", "insert", "update", "delete", "merge")


@dataclass(frozen=True)
class CallRow:
    caller_id: str
    callee_id: str
    file_path: str
    line: int
    source_ref: str
    receiver: str = ""  # Receiver expression for type inference
    callee_name: str = ""  # Raw callee name for symbol matching


@dataclass(frozen=True)
class ConditionRow:
    symbol_id: str
    predicate: str
    file_path: str
    line: int
    source_ref: str


@dataclass(frozen=True)
class ConstantRow:
    name: str
    value: str
    file_path: str
    line: int
    source_ref: str


@dataclass(frozen=True)
class DataAccessRow:
    symbol_id: str
    table_name: str
    op: str
    sql_text: str
    file_path: str
    line: int
    source_ref: str


def extract_calls(
    language: Language,
    tree,
    query_text: str,
    file_path: str,
) -> Iterable[CallRow]:
    if not query_text:
        return []
    query = Query(language, query_text)
    cursor = QueryCursor(query)
    rows: list[CallRow] = []
    captures = cursor.captures(tree.root_node)
    
    callee_nodes = captures.get("callee", [])
    receiver_nodes = captures.get("receiver", [])
    
    # Build receiver lookup by line for matching
    receiver_by_line: dict[int, str] = {}
    for node in receiver_nodes:
        line = node.start_point[0] + 1
        receiver_by_line[line] = _node_text(node)
    
    for node in callee_nodes:
        callee = _node_text(node)
        if not callee:
            continue
        line = node.start_point[0] + 1
        receiver = receiver_by_line.get(line, "")
        
        # Build qualified callee_id when receiver is available (likely class name)
        if receiver and receiver[0].isupper():
            # Receiver looks like a type name (PascalCase) - use qualified ID
            qualified = f"{receiver}.{callee}"
            callee_id = _hash_id(qualified, 0, "callee")
        else:
            # Fallback to name-only hash
            callee_id = _hash_id(callee, 0, "callee")
        
        rows.append(
            CallRow(
                caller_id=_hash_id(file_path, line, "call"),
                callee_id=callee_id,
                file_path=file_path,
                line=line,
                source_ref=f"{file_path}:{line}",
                receiver=receiver,
                callee_name=callee,
            )
        )
    return rows


def extract_conditions(
    language: Language,
    tree,
    query_text: str,
    file_path: str,
) -> Iterable[ConditionRow]:
    if not query_text:
        return []
    query = Query(language, query_text)
    cursor = QueryCursor(query)
    rows: list[ConditionRow] = []
    captures = cursor.captures(tree.root_node)
    nodes = captures.get("condition", [])
    for node in nodes:
        predicate = _node_text(node)
        if not predicate:
            continue
        line = node.start_point[0] + 1
        rows.append(
            ConditionRow(
                symbol_id=_hash_id(file_path, line, "cond"),
                predicate=predicate,
                file_path=file_path,
                line=line,
                source_ref=f"{file_path}:{line}",
            )
        )
    return rows


def extract_constants(
    language: Language,
    tree,
    query_text: str,
    file_path: str,
) -> Iterable[ConstantRow]:
    if not query_text:
        return []
    query = Query(language, query_text)
    cursor = QueryCursor(query)
    rows: list[ConstantRow] = []
    captures = cursor.captures(tree.root_node)
    nodes = captures.get("const", [])
    for node in nodes:
        value = _node_text(node)
        if not value:
            continue
        line = node.start_point[0] + 1
        rows.append(
            ConstantRow(
                name="",
                value=value,
                file_path=file_path,
                line=line,
                source_ref=f"{file_path}:{line}",
            )
        )
    return rows


def extract_data_access(
    language: Language,
    tree,
    query_text: str,
    file_path: str,
) -> Iterable[DataAccessRow]:
    if not query_text:
        return []
    query = Query(language, query_text)
    cursor = QueryCursor(query)
    rows: list[DataAccessRow] = []
    captures = cursor.captures(tree.root_node)
    nodes = captures.get("sql", [])
    for node in nodes:
        raw = _node_text(node)
        sql_text = _strip_quotes(raw)
        if not _looks_like_sql(sql_text):
            continue
        op = _sql_op(sql_text)
        line = node.start_point[0] + 1
        rows.append(
            DataAccessRow(
                symbol_id=_hash_id(file_path, line, "sql"),
                table_name="",
                op=op,
                sql_text=sql_text,
                file_path=file_path,
                line=line,
                source_ref=f"{file_path}:{line}",
            )
        )
    return rows


def _node_text(node) -> str:
    return node.text.decode("utf-8", errors="ignore")


def _strip_quotes(value: str) -> str:
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    return value


def _looks_like_sql(value: str) -> bool:
    lower = value.strip().lower()
    return any(lower.startswith(keyword) for keyword in SQL_KEYWORDS)


def _sql_op(value: str) -> str:
    lower = value.strip().lower()
    for keyword in SQL_KEYWORDS:
        if lower.startswith(keyword):
            return keyword
    return ""


def _hash_id(text: str, line: int, kind: str) -> str:
    raw = f"{text}:{line}:{kind}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
