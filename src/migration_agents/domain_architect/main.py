from __future__ import annotations

import argparse
import json
import hashlib
import logging
import os
import math
import re
import subprocess
import time
import urllib.request
import networkx as nx
from sentence_transformers import SentenceTransformer
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.shared_multiprocessing import process_map, resolve_workers
from migration_agents.state import finalize_state, start_state, write_state

from .config import DomainArchitectConfig, load_config

logger = logging.getLogger(__name__)

ENTRY_GRAPH_SUMMARY_LIMIT = 100

def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_workers(config: DomainArchitectConfig) -> int:
    if config.workers != "auto":
        return int(config.workers)
    return max(1, (os.cpu_count() or 2) - 1)


def _with_metadata(
    rows: list[dict],
    config: DomainArchitectConfig,
    created_at: str,
) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("slice_id", None)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _fetch_rows(client, table: str, run_id: str, artifact_version: int) -> list[dict]:
    sql = f"""
        select *
        from {table}
        where run_id = '{run_id}' and artifact_version = {artifact_version}
    """
    return client.query(sql)


def _fetch_rows_local(
    output_root: Path,
    run_id: str,
    stage: str,
    table: str,
) -> list[dict]:
    from migration_agents.mcp.duckdb_catalog import get_run_connection

    table_root = output_root / run_id / stage / table
    files = [str(path) for path in table_root.rglob("*.parquet")]
    if not files:
        return []
    con, _ = get_run_connection(output_root, run_id)
    try:
        rows = con.execute("select * from read_parquet(?::VARCHAR[])", [files]).fetchdf()
        return rows.to_dict(orient="records")
    finally:
        con.close()


def _fetch_rows_with_fallback(
    client,
    output_root: Path,
    run_id: str,
    artifact_version: int,
    stage: str,
    table: str,
) -> list[dict]:
    try:
        return _fetch_rows(client, table, run_id, artifact_version)
    except Exception:
        return _fetch_rows_local(output_root, run_id, stage, table)


def _hash_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _truncate(value: str, limit: int) -> str:
    cleaned = " ".join(value.split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3] + "..."


def _extract_nouns(text: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]+", text)
    return [token for token in tokens if token[0].isupper()]


_STOPWORDS = {
    "the",
    "and",
    "for",
    "from",
    "with",
    "when",
    "this",
    "that",
    "rule",
    "slice",
    "context",
    "data",
    "logic",
    "inputs",
    "outputs",
}


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9_]+", text)]


def _top_terms(texts: list[str], limit: int) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    for text in texts:
        for token in _tokenize(text):
            if token in _STOPWORDS:
                continue
            counts[token] += 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [item[0] for item in ranked[:limit]]


def _llm_prompt(
    cluster_key: str,
    summaries: list[str],
    tables: list[str],
    endpoint_counts: dict[str, int],
    flow_summaries: list[str],
    max_chars: int,
) -> str:
    summary_text = " ".join(summaries)
    summary_text = summary_text[:max_chars]
    endpoint_parts = [f"{key}:{value}" for key, value in sorted(endpoint_counts.items())]
    flow_text = " ".join(flow_summaries)
    flow_text = flow_text[:max_chars]
    prompt = f"""
You are a domain architect. Create a DDD context name and rationale.

Cluster: {cluster_key}
Summaries: {summary_text}
Tables: {", ".join(tables)}
Endpoints: {", ".join(endpoint_parts)}
Endpoint flows: {flow_text}

Return JSON with keys: name, rationale.
"""
    return prompt.strip()


def _endpoint_flow_batch_prompt(
    items: list[dict],
    max_flow_summary_chars: int,
) -> str:
    payload = json.dumps(items, ensure_ascii=True)
    prompt = f"""
You are a domain architect. Summarize each endpoint flow from entry to exit.

Return JSON array with objects:
- endpoint_id
- flow_summary (clean summary, mention entry, key steps, db access, <= {max_flow_summary_chars} chars)

Endpoints: {payload}
"""
    return prompt.strip()


def _endpoint_flow_prompt(
    item: dict,
    max_flow_summary_chars: int,
) -> str:
    payload = json.dumps(item, ensure_ascii=True)
    prompt = f"""
You are a domain architect. Summarize the endpoint flow from entry to exit.

Return JSON with keys:
- endpoint_id
- flow_summary (clean summary, mention entry, key steps, db access, <= {max_flow_summary_chars} chars)

Endpoint: {payload}
"""
    return prompt.strip()


def _pagerank_entry_prompt(item: dict, max_chars: int) -> str:
    payload = json.dumps(item, ensure_ascii=True)
    prompt = f"""
You are a domain architect. Explain the entry method and its exits in detail.

Return JSON with keys:
- entry_id
- explanation (<= {max_chars} chars, clear and detailed)

Entry: {payload}
"""
    return prompt.strip()

def _domain_insight_batch_prompt(
    items: list[dict],
    max_comment_chars: int,
    max_indicative_chars: int,
) -> str:
    payload = json.dumps(items, ensure_ascii=True)
    prompt = f"""
You are a domain architect. Generate domain insights from the rules provided.

Return JSON array with objects:
- rule_id
- logic_comment (one sentence, intent-focused, <= {max_comment_chars} chars)
- indicative_result (starts with "Indicative:", <= {max_indicative_chars} chars)
- confidence (float in [0, 1] based on clarity of rule and inputs)

Rules: {payload}
"""
    return prompt.strip()


def _domain_insight_prompt(
    rule: dict,
    slice_id: str,
    slice_summary: str,
    max_comment_chars: int,
    max_indicative_chars: int,
) -> str:
    rule_text = rule.get("rule_text", "")
    inputs = rule.get("inputs", "")
    outputs = rule.get("outputs", "")
    invariants = rule.get("invariants", "")
    prompt = f"""
You are a domain architect. Generate a domain insight from the rule data.

Slice: {slice_id}
Slice summary: {slice_summary}
Rule text: {rule_text}
Inputs: {inputs}
Outputs: {outputs}
Invariants: {invariants}

Return JSON only with:
- logic_comment: one sentence, intent-focused, <= {max_comment_chars} chars.
- indicative_result: starts with "Indicative:" and <= {max_indicative_chars} chars.
- confidence: float in [0, 1] based on clarity of the rule and inputs.
"""
    return prompt.strip()


def _llm_response_text(config: DomainArchitectConfig, prompt: str) -> str:
    if config.llm_cmd:
        result = subprocess.run(
            config.llm_cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=config.llm_timeout_sec,
            check=True,
        )
        return result.stdout.strip()
    provider = (config.llm_provider or "copilot").lower()
    if provider in ("copilot", "github"):
        # Use GitHub/Copilot LLM via models.inference.ai.azure.com
        api_key = os.environ.get("GITHUB_TOKEN")
        if not api_key:
            raise RuntimeError("GITHUB_TOKEN environment variable is required for Copilot LLM")
        base_url = config.llm_base_url if config.llm_base_url else "https://models.inference.ai.azure.com/chat/completions"
        model = config.llm_model or "gpt-4o-mini"
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }).encode("utf-8")
        request = urllib.request.Request(
            base_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("Copilot LLM response missing choices")
        return str(choices[0].get("message", {}).get("content", "")).strip()
    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI LLM calls")
        if not config.llm_model:
            raise RuntimeError("llm_model is required for OpenAI LLM calls")
        payload = json.dumps(
            {
                "model": config.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("OpenAI response missing choices")
        return str(choices[0].get("message", {}).get("content", "")).strip()
    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is required for Gemini LLM calls")
        if not config.llm_model:
            raise RuntimeError("llm_model is required for Gemini LLM calls")
        payload = json.dumps(
            {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2},
            }
        ).encode("utf-8")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{config.llm_model}:generateContent?key={api_key}"
        )
        request = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini response missing candidates")
        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            raise ValueError("Gemini response missing content parts")
        return str(parts[0].get("text", "")).strip()
    raise RuntimeError("llm_cmd or supported llm_provider is required for LLM calls")


def _call_llm_json(config: DomainArchitectConfig, prompt: str) -> object:
    text = _llm_response_text(config, prompt)
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    text = _clean_llm_text(text)
    try:
        payload = json.loads(text)
        if isinstance(payload, dict) and isinstance(payload.get("response"), str):
            response_text = payload["response"]
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return _extract_json_fragment(response_text)
        return payload
    except json.JSONDecodeError:
        pass
    return _extract_json_fragment(text)


def _extract_json_fragment(text: str) -> object:
    # Strip common fencing to improve odds of locating JSON
    fenced = text.strip()
    if fenced.startswith("```"):
        fenced = fenced.strip("`")
    text = fenced or text
    start_brace = text.find("{")
    end_brace = text.rfind("}")
    start_bracket = text.find("[")
    end_bracket = text.rfind("]")
    # Prefer array blocks when they appear earlier than the first object
    if start_bracket != -1 and end_bracket > start_bracket and (
        start_brace == -1 or start_bracket < start_brace
    ):
        return json.loads(text[start_bracket : end_bracket + 1])
    if start_brace != -1 and end_brace > start_brace:
        return json.loads(text[start_brace : end_brace + 1])
    # Last resort: wrap raw text so downstream can proceed
    cleaned = text.strip()
    if cleaned:
        return {"raw_text": cleaned}
    raise ValueError("LLM response is not JSON")


def _clean_llm_text(text: str) -> str:
    """
    Remove common “thinking” / analysis wrappers some models emit so we can parse JSON.
    Examples stripped: <think>...</think>, <analysis>...</analysis>, leading 'Thinking:' lines.
    """
    lowered = text.lower()
    for tag in ("think", "analysis"):
        start = lowered.find(f"<{tag}>")
        end = lowered.rfind(f"</{tag}>")
        if start != -1 and end != -1 and end > start:
            text = text[:start] + text[end + len(tag) + 3 :]
            lowered = text.lower()
    lines = []
    for line in text.splitlines():
        if line.strip().lower().startswith("thinking:"):
            continue
        lines.append(line)
    return "\n".join(lines)


def _call_llm(config: DomainArchitectConfig, prompt: str) -> dict:
    payload = _call_llm_json(config, prompt)
    if not isinstance(payload, dict):
        raise ValueError("LLM response JSON is not an object")
    return payload


def _call_llm_list(config: DomainArchitectConfig, prompt: str) -> list[dict]:
    payload = _call_llm_json(config, prompt)
    if isinstance(payload, dict):
        items = payload.get("items")
        if isinstance(items, list):
            payload = items
        elif _looks_like_item(payload):
            payload = [payload]
        else:
            # Be permissive: wrap a single object even if schema is slightly off
            payload = [payload]
    if not isinstance(payload, list):
        raise ValueError("LLM response JSON is not a list")
    rows: list[dict] = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("LLM response list contains non-object item")
        rows.append(item)
    return rows


def _looks_like_item(payload: dict) -> bool:
    return any(
        key in payload
        for key in (
            "endpoint_id",
            "flow_summary",
            "rule_id",
            "logic_comment",
            "indicative_result",
            "confidence",
            "name",
            "rationale",
        )
    )


def _parse_confidence(value: object, rule_id: str) -> float:
    if isinstance(value, (int, float)):
        confidence = float(value)
    elif isinstance(value, str):
        confidence = float(value.strip())
    else:
        raise ValueError(f"LLM confidence missing for rule {rule_id}")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"LLM confidence out of range for rule {rule_id}")
    return confidence


def _ensure_llm_available(config: DomainArchitectConfig, purpose: str) -> None:
    if config.llm_cmd:
        return
    provider = (config.llm_provider or "cmd").lower()
    if provider in {"openai", "gemini"}:
        return
    raise RuntimeError(f"LLM is required for {purpose}")


def _group_rules_by_slice(
    rules: list[dict],
    rule_cluster_map: dict[str, int],
) -> tuple[dict[str, list[dict]], dict[str, str]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    rule_slice_map: dict[str, str] = {}
    for row in rules:
        rule_id = row.get("rule_id")
        raw_slice_id = row.get("slice_id")
        cluster_id = rule_cluster_map.get(rule_id or "")
        if cluster_id:
            slice_id = f"slice_{cluster_id}"
        else:
            slice_id = raw_slice_id
        if rule_id and slice_id:
            rule_slice_map[rule_id] = slice_id
        if slice_id:
            grouped[slice_id].append(row)
    return grouped, rule_slice_map


def _slice_node_ids(
    slice_manifest: list[dict],
    code_graph_nodes: list[dict],
) -> dict[str, set[str]]:
    symbol_to_node: dict[str, str] = {}
    table_to_node: dict[str, str] = {}
    for node in code_graph_nodes:
        node_id = node.get("node_id")
        symbol_id = node.get("symbol_id")
        table_name = node.get("table_name")
        if node_id and symbol_id:
            symbol_to_node[symbol_id] = node_id
        if node_id and table_name:
            table_to_node[str(table_name).lower()] = node_id
    slices: dict[str, set[str]] = defaultdict(set)
    for row in slice_manifest:
        slice_id = row.get("slice_id")
        symbol_id = row.get("symbol_id")
        table_name = row.get("table_name")
        if not slice_id:
            continue
        if symbol_id and symbol_id in symbol_to_node:
            slices[slice_id].add(symbol_to_node[symbol_id])
        if table_name:
            key = str(table_name).lower()
            node_id = table_to_node.get(key)
            if node_id:
                slices[slice_id].add(node_id)
    return slices


def _derive_entities(
    slice_id: str,
    rules: list[dict],
    max_name_chars: int,
) -> list[dict]:
    names: list[str] = []
    for rule in rules:
        names.extend(_extract_nouns(rule.get("rule_text", "")))
        inputs = rule.get("inputs", "")
        for token in inputs.split(","):
            token = token.strip()
            if token:
                names.append(token)
    if not names:
        names = [slice_id.replace("slice_", "slice").title()]

    deduped: list[str] = []
    for name in names:
        normalized = name.strip()
        if not normalized:
            continue
        if normalized.lower() not in {item.lower() for item in deduped}:
            deduped.append(normalized)

    rows: list[dict] = []
    for name in deduped[:5]:
        entity_name = _truncate(name, max_name_chars)
        rows.append(
            {
                "entity_id": _hash_id(f"{slice_id}:{entity_name}"),
                "slice_id": slice_id,
                "name": entity_name,
                "invariants": "",
                "source_ref": "logic_rules",
            }
        )
    return rows


def _derive_value_objects(
    slice_id: str,
    rules: list[dict],
    max_name_chars: int,
) -> list[dict]:
    rows: list[dict] = []
    for rule in rules:
        inputs = [token.strip() for token in rule.get("inputs", "").split(",") if token]
        for token in inputs[:3]:
            name = _truncate(token, max_name_chars)
            rows.append(
                {
                    "vo_id": _hash_id(f"{slice_id}:{name}:vo"),
                    "slice_id": slice_id,
                    "name": name,
                    "invariants": "",
                    "source_ref": rule.get("source_ref", "logic_rules"),
                }
            )
    return rows


def _derive_aggregates(
    slice_id: str,
    entities: list[dict],
) -> list[dict]:
    if not entities:
        return []
    root = entities[0]
    return [
        {
            "aggregate_id": _hash_id(f"{slice_id}:{root['entity_id']}:agg"),
            "slice_id": slice_id,
            "name": f"{root['name']}Aggregate",
            "root_entity_id": root["entity_id"],
            "source_ref": root.get("source_ref", "logic_rules"),
        }
    ]


def _derive_context_map(slice_id: str, cluster_id: int | None) -> dict:
    if cluster_id is None:
        name = f"{slice_id}_context"
        context_id = _hash_id(f"{slice_id}:context")
    else:
        name = f"cluster_{cluster_id}_context"
        context_id = _hash_id(f"cluster:{cluster_id}")
    return {
        "context_id": context_id,
        "slice_id": slice_id,
        "name": name,
        "boundaries": "",
        "source_ref": "logic_rules",
    }


def _build_domain_rows_for_slice(
    item: tuple[str, list[dict], int | None, str, int],
) -> tuple[list[dict], list[dict], list[dict], dict]:
    slice_id, rules, cluster_id, context_name, max_name_chars = item
    entities = _derive_entities(slice_id, rules, max_name_chars)
    value_objects = _derive_value_objects(slice_id, rules, max_name_chars)
    aggregates = _derive_aggregates(slice_id, entities)
    context = _derive_context_map(slice_id, cluster_id)
    context["name"] = context_name
    return entities, value_objects, aggregates, context


def _simhash64(text: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9_]+", text.lower())
    if not tokens:
        return 0
    weights = [0] * 64
    for token in tokens:
        h = hashlib.md5(token.encode("utf-8")).digest()
        bits = int.from_bytes(h[:8], "big")
        for idx in range(64):
            bit = (bits >> idx) & 1
            weights[idx] += 1 if bit else -1
    value = 0
    for idx, weight in enumerate(weights):
        if weight >= 0:
            value |= 1 << idx
    return value


def _simhash_vector(vector: list[float]) -> int:
    if not vector:
        return 0
    weights = [0.0] * 64
    for idx, value in enumerate(vector):
        weights[idx % 64] += value
    value = 0
    for idx, weight in enumerate(weights):
        if weight >= 0:
            value |= 1 << idx
    return value


def _cluster_id(simhash: int, bits: int) -> int:
    if bits <= 0:
        return 0
    shift = 64 - bits
    return simhash >> shift if shift > 0 else simhash


def _context_cluster_map(
    slice_context: list[dict],
    bits: int,
) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for row in slice_context:
        slice_id = row.get("slice_id")
        summary = row.get("summary", "")
        if not slice_id:
            continue
        simhash = _simhash64(summary)
        mapping[slice_id] = _cluster_id(simhash, bits)
    return mapping


def _group_key(graph_id: int | None, vector_id: int | None) -> str:
    graph_part = graph_id if graph_id is not None else -1
    vector_part = vector_id if vector_id is not None else -1
    return f"g{graph_part}-v{vector_part}"


def _group_scores(
    summaries: list[str],
    tables: list[str],
    flow_summaries: list[str],
    graph_id: int | None,
    vector_id: int | None,
) -> tuple[float, float, float]:
    coverage_score = min(1.0, (len(summaries) + len(tables) + len(flow_summaries)) / 10.0)
    graph_score = 1.0 if graph_id is not None else 0.5
    vector_score = 1.0 if vector_id is not None else 0.5
    return graph_score, vector_score, coverage_score


def _combined_score(
    graph_score: float,
    vector_score: float,
    coverage_score: float,
    pagerank_score: float,
) -> float:
    base = coverage_score * (graph_score + vector_score) / 2.0
    return round(base * (0.5 + min(1.0, pagerank_score)), 4)


def _context_name_map(
    slice_context: list[dict],
    slice_manifest: list[dict],
    graph_clusters: dict[str, int],
    vector_clusters: dict[str, int],
    context_clusters: dict[str, int],
    max_name_chars: int,
) -> dict[str, str]:
    context_texts: dict[str, list[str]] = defaultdict(list)
    context_tables: dict[str, set[str]] = defaultdict(set)
    for row in slice_context:
        slice_id = row.get("slice_id")
        if not slice_id:
            continue
        graph_id = graph_clusters.get(slice_id)
        vector_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        context_key = _group_key(graph_id, vector_id)
        summary = row.get("summary", "")
        if summary:
            context_texts[context_key].append(summary)
    for row in slice_manifest:
        slice_id = row.get("slice_id")
        table_name = row.get("table_name")
        if not slice_id or not table_name:
            continue
        graph_id = graph_clusters.get(slice_id)
        vector_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        context_key = _group_key(graph_id, vector_id)
        context_tables[context_key].add(str(table_name))
    name_map: dict[str, str] = {}
    for key, texts in context_texts.items():
        terms = _top_terms(texts, 2)
        tables = sorted(context_tables.get(key, []))[:1]
        parts = [term for term in terms if term]
        if tables:
            parts.append(tables[0].lower())
        label = "_".join(parts) if parts else f"context_{key}"
        name_map[key] = _truncate(label, max_name_chars)
    return name_map


def _context_groups_llm(
    slice_context: list[dict],
    slice_manifest: list[dict],
    endpoints: list[dict],
    endpoint_flows: list[dict],
    graph_clusters: dict[str, int],
    vector_clusters: dict[str, int],
    context_clusters: dict[str, int],
    slice_pagerank: dict[str, float],
    config: DomainArchitectConfig,
) -> tuple[dict[str, str], list[dict]]:
    _ensure_llm_available(config, "LLM context grouping")
    summaries_by_cluster: dict[str, list[str]] = defaultdict(list)
    tables_by_cluster: dict[str, set[str]] = defaultdict(set)
    endpoint_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    flow_summaries_by_cluster: dict[str, list[str]] = defaultdict(list)
    graph_by_key: dict[str, int | None] = {}
    vector_by_key: dict[str, int | None] = {}
    pagerank_by_key: dict[str, list[float]] = defaultdict(list)
    for row in slice_context:
        slice_id = row.get("slice_id")
        summary = row.get("summary", "")
        if not slice_id:
            continue
        graph_id = graph_clusters.get(slice_id)
        vector_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        key = _group_key(graph_id, vector_id)
        graph_by_key.setdefault(key, graph_id)
        vector_by_key.setdefault(key, vector_id)
        if slice_id in slice_pagerank:
            pagerank_by_key[key].append(slice_pagerank[slice_id])
        if summary:
            summaries_by_cluster[key].append(summary)
    for row in slice_manifest:
        slice_id = row.get("slice_id")
        table_name = row.get("table_name")
        if not slice_id or not table_name:
            continue
        graph_id = graph_clusters.get(slice_id)
        vector_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        key = _group_key(graph_id, vector_id)
        graph_by_key.setdefault(key, graph_id)
        vector_by_key.setdefault(key, vector_id)
        if slice_id in slice_pagerank:
            pagerank_by_key[key].append(slice_pagerank[slice_id])
        tables_by_cluster[key].add(str(table_name))
    for row in endpoints:
        name = row.get("name", "")
        slice_id = row.get("name", "").split(":", 1)[-1]
        graph_id = graph_clusters.get(slice_id)
        vector_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        key = _group_key(graph_id, vector_id)
        graph_by_key.setdefault(key, graph_id)
        vector_by_key.setdefault(key, vector_id)
        if slice_id in slice_pagerank:
            pagerank_by_key[key].append(slice_pagerank[slice_id])
        kind = name.split(":", 1)[0] if ":" in name else "unknown"
        endpoint_counts[key][kind] += 1
    for row in endpoint_flows:
        slice_id = row.get("slice_id")
        flow_summary = row.get("flow_summary", "")
        if not slice_id or not flow_summary:
            continue
        graph_id = graph_clusters.get(slice_id)
        vector_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        key = _group_key(graph_id, vector_id)
        graph_by_key.setdefault(key, graph_id)
        vector_by_key.setdefault(key, vector_id)
        if slice_id in slice_pagerank:
            pagerank_by_key[key].append(slice_pagerank[slice_id])
        flow_summaries_by_cluster[key].append(flow_summary)
    name_map: dict[str, str] = {}
    group_rows: list[dict] = []
    heuristic_names = _context_name_map(
        slice_context,
        slice_manifest,
        graph_clusters,
        vector_clusters,
        context_clusters,
        config.max_name_chars,
    )
    all_keys = sorted(
        set(summaries_by_cluster) | set(tables_by_cluster) | set(flow_summaries_by_cluster)
    )
    llm_keys = all_keys
    fallback_keys: list[str] = []
    if config.llm_context_groups_max_items is not None:
        max_items = max(0, config.llm_context_groups_max_items)
        if len(all_keys) > max_items:
            llm_keys = all_keys[:max_items]
            fallback_keys = all_keys[max_items:]

    for key in llm_keys:
        summaries = summaries_by_cluster.get(key, [])[:10]
        tables = sorted(tables_by_cluster.get(key, []))[:10]
        flow_summaries = flow_summaries_by_cluster.get(key, [])[:10]
        prompt = _llm_prompt(
            key,
            summaries,
            tables,
            endpoint_counts.get(key, {}),
            flow_summaries,
            config.llm_max_input_chars,
        )
        graph_id = graph_by_key.get(key)
        vector_id = vector_by_key.get(key)
        graph_score, vector_score, coverage_score = _group_scores(
            summaries, tables, flow_summaries, graph_id, vector_id
        )
        pagerank_score = (
            sum(pagerank_by_key.get(key, [])) / len(pagerank_by_key.get(key, []))
            if pagerank_by_key.get(key)
            else 0.0
        )
        combined_score = _combined_score(
            graph_score, vector_score, coverage_score, pagerank_score
        )
        try:
            payload = _call_llm(config, prompt)
            name = _truncate(str(payload.get("name", f"context_{key}")), config.max_name_chars)
            rationale = _truncate(str(payload.get("rationale", "")), config.max_indicative_chars)
            source_ref = "llm"
        except Exception:
            if not config.allow_heuristics:
                raise
            name = heuristic_names.get(key, f"context_{key}")
            rationale = "Heuristic name derived from slice summaries and tables."
            source_ref = "heuristic"
        name_map[key] = name
        group_rows.append(
            {
                "context_id": _hash_id(f"context:{key}"),
                "context_key": key,
                "name": name,
                "rationale": rationale,
                "graph_score": graph_score,
                "vector_score": vector_score,
                "coverage_score": coverage_score,
                "pagerank_score": pagerank_score,
                "combined_score": combined_score,
                "source_ref": source_ref,
            }
        )
    for key in fallback_keys:
        if not config.allow_heuristics:
            raise ValueError("Heuristic context grouping disabled but fallback requested")
        name = heuristic_names.get(key, f"context_{key}")
        rationale = "Heuristic name derived from slice summaries and tables."
        summaries = summaries_by_cluster.get(key, [])[:10]
        tables = sorted(tables_by_cluster.get(key, []))[:10]
        flow_summaries = flow_summaries_by_cluster.get(key, [])[:10]
        graph_id = graph_by_key.get(key)
        vector_id = vector_by_key.get(key)
        graph_score, vector_score, coverage_score = _group_scores(
            summaries, tables, flow_summaries, graph_id, vector_id
        )
        pagerank_score = (
            sum(pagerank_by_key.get(key, [])) / len(pagerank_by_key.get(key, []))
            if pagerank_by_key.get(key)
            else 0.0
        )
        combined_score = _combined_score(
            graph_score, vector_score, coverage_score, pagerank_score
        )
        name_map[key] = name
        group_rows.append(
            {
                "context_id": _hash_id(f"context:{key}"),
                "context_key": key,
                "name": name,
                "rationale": rationale,
                "graph_score": graph_score,
                "vector_score": vector_score,
                "coverage_score": coverage_score,
                "pagerank_score": pagerank_score,
                "combined_score": combined_score,
                "source_ref": "heuristic",
            }
        )
    return name_map, group_rows


def _vector_cluster_map(
    slice_nodes: dict[str, set[str]],
    code_vectors: list[dict],
    bits: int,
    max_nodes_per_slice: int,
) -> dict[str, int]:
    node_vectors: dict[str, list[float]] = {}
    for row in code_vectors:
        node_id = row.get("node_id")
        vector = row.get("vector")
        if node_id and isinstance(vector, list):
            node_vectors[node_id] = [float(v) for v in vector]
    clusters: dict[str, int] = {}
    for slice_id, node_ids in slice_nodes.items():
        node_list = list(node_ids)
        if len(node_list) > max_nodes_per_slice:
            node_list = node_list[:max_nodes_per_slice]
        vectors = [node_vectors[nid] for nid in node_list if nid in node_vectors]
        if not vectors:
            continue
        dims = len(vectors[0])
        avg = [0.0] * dims
        for vec in vectors:
            for idx, value in enumerate(vec):
                avg[idx] += value
        avg = [value / len(vectors) for value in avg]
        simhash = _simhash_vector(avg)
        clusters[slice_id] = _cluster_id(simhash, bits)
    return clusters


def _endpoint_type(file_path: str, external_ref: str) -> str:
    _ = file_path
    _ = external_ref
    return "pagerank"


def _build_endpoints_with_entries(
    slice_manifest: list[dict],
    code_graph_nodes: list[dict],
    pagerank_entries: dict[str, str],
) -> list[dict]:
    rows: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    symbol_to_node: dict[str, str] = {}
    for node in code_graph_nodes:
        symbol_id = node.get("symbol_id")
        node_id = node.get("node_id")
        if symbol_id and node_id:
            symbol_to_node[symbol_id] = node_id
    for row in slice_manifest:
        slice_id = row.get("slice_id")
        file_path = row.get("file_path", "")
        external_ref = row.get("external_ref", "")
        symbol_id = row.get("symbol_id")
        if not slice_id:
            continue
        endpoint_type = _endpoint_type(file_path, external_ref)
        entry_node_id = symbol_to_node.get(symbol_id) if symbol_id else None
        if not entry_node_id:
            entry_node_id = pagerank_entries.get(slice_id)
        if endpoint_type == "unknown" and entry_node_id:
            endpoint_type = "pagerank"
        if not entry_node_id:
            continue
        key = (slice_id, endpoint_type, entry_node_id)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "endpoint_id": _hash_id(f"{slice_id}:{endpoint_type}:{entry_node_id}"),
                "slice_id": slice_id,
                "name": f"{endpoint_type}:{slice_id}",
                "entry_point": file_path,
                "route": "",
                "method": "",
                "symbol_id": symbol_id,
                "entry_node_id": entry_node_id,
                "source_ref": row.get("source_ref", file_path),
            }
        )
    return rows


def _build_dead_code(
    code_graph_nodes: list[dict],
    graph_metadata: list[dict],
    symbols: list[dict],
) -> list[dict]:
    node_degree: dict[str, int] = {}
    for row in graph_metadata:
        node_id = row.get("node_id")
        degree = row.get("degree")
        if node_id and isinstance(degree, int):
            node_degree[node_id] = degree
    symbol_lookup: dict[str, tuple[str, int]] = {}
    for row in symbols:
        symbol_id = row.get("symbol_id")
        file_path = row.get("file_path")
        line = row.get("line")
        if symbol_id and file_path and isinstance(line, int):
            symbol_lookup[symbol_id] = (file_path, line)
    rows: list[dict] = []
    for node in code_graph_nodes:
        if node.get("node_type") != "symbol":
            continue
        node_id = node.get("node_id")
        symbol_id = node.get("symbol_id")
        if not node_id or not symbol_id:
            continue
        if node_degree.get(node_id, 0) != 0:
            continue
        file_path, line = symbol_lookup.get(symbol_id, ("", 0))
        rows.append(
            {
                "symbol_id": symbol_id,
                "file_path": file_path,
                "line": line,
                "reason": "isolated_node",
                "source_ref": file_path or node.get("source_ref", ""),
            }
        )
    return rows


def _process_domain_insight_group(
    group_id: str,
    slice_id: str,
    batch: list[dict],
    group_score: float,
    config: DomainArchitectConfig,
) -> tuple[str, float, list[dict], Exception | None]:
    start = time.perf_counter()
    try:
        prompt = _domain_insight_batch_prompt(
            batch,
            config.max_comment_chars,
            config.max_indicative_chars,
        )
        use_single = len(batch) == 1 or len(prompt) > config.llm_max_input_chars
        rows_out: list[dict] = []
        if use_single:
            for item in batch:
                single_prompt = _domain_insight_prompt(
                    item,
                    item["slice_id"],
                    item.get("slice_summary", ""),
                    config.max_comment_chars,
                    config.max_indicative_chars,
                )
                payload = _call_llm(config, single_prompt)
                logic_comment = str(payload.get("logic_comment", "")).strip()
                indicative = str(payload.get("indicative_result", "")).strip()
                if not logic_comment or not indicative:
                    raise ValueError(f"LLM response missing text for rule {item['rule_id']}")
                confidence = _parse_confidence(payload.get("confidence"), item["rule_id"])
                rows_out.append(
                    {
                        "rule_id": item["rule_id"],
                        "slice_id": item["slice_id"],
                        "logic_comment": _truncate(logic_comment, config.max_comment_chars),
                        "indicative_result": _truncate(indicative, config.max_indicative_chars),
                        "confidence": confidence,
                        "llm_source": "llm",
                        "group_id": group_id,
                        "group_score": group_score,
                        "source_ref": item["source_ref"],
                    }
                )
        else:
            payload_items = _call_llm_list(config, prompt)
            payload_by_rule: dict[str, dict] = {}
            for entry in payload_items:
                rule_id = str(entry.get("rule_id", "")).strip()
                if not rule_id:
                    raise ValueError("LLM response missing rule_id for domain insight")
                payload_by_rule[rule_id] = entry
            for item in batch:
                rule_id = item["rule_id"]
                payload = payload_by_rule.get(rule_id)
                if not payload:
                    raise ValueError(f"LLM response missing domain insight for rule {rule_id}")
                logic_comment = str(payload.get("logic_comment", "")).strip()
                indicative = str(payload.get("indicative_result", "")).strip()
                if not logic_comment or not indicative:
                    raise ValueError(f"LLM response missing text for rule {rule_id}")
                confidence = _parse_confidence(payload.get("confidence"), rule_id)
                rows_out.append(
                    {
                        "rule_id": rule_id,
                        "slice_id": item["slice_id"],
                        "logic_comment": _truncate(logic_comment, config.max_comment_chars),
                        "indicative_result": _truncate(indicative, config.max_indicative_chars),
                        "confidence": confidence,
                        "llm_source": "llm",
                        "group_id": group_id,
                        "group_score": group_score,
                        "source_ref": item["source_ref"],
                    }
                )
        return group_id, time.perf_counter() - start, rows_out, None
    except Exception as exc:
        if not config.allow_heuristics:
            return group_id, time.perf_counter() - start, [], exc
        rows_out = []
        for item in batch:
            rule_text = str(item.get("rule_text", "")).strip()
            outputs = str(item.get("outputs", "")).strip()
            logic_comment = rule_text or "Derived rule from legacy logic."
            indicative = f"Indicative: {outputs}" if outputs else "Indicative: Outcome inferred."
            rows_out.append(
                {
                    "rule_id": item["rule_id"],
                    "slice_id": item["slice_id"],
                    "logic_comment": _truncate(logic_comment, config.max_comment_chars),
                    "indicative_result": _truncate(indicative, config.max_indicative_chars),
                    "confidence": 0.2,
                    "llm_source": "heuristic",
                    "group_id": group_id,
                    "group_score": group_score,
                    "source_ref": item["source_ref"],
                }
            )
        return group_id, time.perf_counter() - start, rows_out, None


def _build_domain_insights_llm(
    logic_rules: list[dict],
    rule_slice_map: dict[str, str],
    slice_summaries: dict[str, str],
    config: DomainArchitectConfig,
) -> list[dict]:
    _ensure_llm_available(config, "LLM domain insights")
    batch_size = max(1, config.llm_domain_insights_batch_size)
    rows: list[dict] = []
    items: list[dict] = []
    for rule in logic_rules:
        rule_id = rule.get("rule_id")
        slice_id = rule_slice_map.get(rule_id or "", rule.get("slice_id"))
        if not rule_id or not slice_id:
            continue
        items.append(
            {
                "rule_id": rule_id,
                "slice_id": slice_id,
                "slice_summary": slice_summaries.get(slice_id, ""),
                "rule_text": rule.get("rule_text", ""),
                "inputs": rule.get("inputs", ""),
                "outputs": rule.get("outputs", ""),
                "invariants": rule.get("invariants", ""),
                "source_ref": rule.get("source_ref", "logic_rules"),
            }
        )

    fallback_items: list[dict] = []
    if config.llm_domain_insights_max_items is not None:
        max_items = max(0, config.llm_domain_insights_max_items)
        if len(items) > max_items:
            fallback_items = items[max_items:]
            items = items[:max_items]

    groups_by_slice: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        groups_by_slice[item["slice_id"]].append(item)

    group_size = config.llm_domain_insights_group_size or batch_size
    group_budget = config.llm_domain_insights_max_groups
    groups_processed = 0
    group_timings: list[tuple[str, float]] = []
    estimated_total = 0
    for group_items in groups_by_slice.values():
        estimated_total += (len(group_items) + group_size - 1) // group_size
    if group_budget is not None:
        estimated_total = min(estimated_total, group_budget)
    overall_start = time.perf_counter()
    tasks: list[tuple[str, str, list[dict], float]] = []
    for slice_id, group_items in groups_by_slice.items():
        for offset in range(0, len(group_items), group_size):
            if group_budget is not None and len(tasks) >= group_budget:
                if config.allow_heuristics:
                    for item in group_items[offset:]:
                        fallback_items.append(item)
                    break
                raise ValueError("Heuristics disabled but group budget would drop items")
            batch = group_items[offset : offset + group_size]
            group_id = _hash_id(f"{slice_id}:{offset}")
            group_score = min(1.0, len(batch) / 10.0)
            tasks.append((group_id, slice_id, batch, group_score))
        if group_budget is not None and len(tasks) >= group_budget:
            break

    if config.llm_workers > 1 and len(tasks) > 1:
        with ProcessPoolExecutor(max_workers=config.llm_workers) as executor:
            future_map = {}
            for group_id, slice_id, batch, group_score in tasks:
                logger.info(
                    "domain_insights_group_start group_id=%s slice_id=%s size=%d progress=%d/%d",
                    group_id,
                    slice_id,
                    len(batch),
                    len(future_map) + 1,
                    estimated_total,
                )
                future = executor.submit(
                    _process_domain_insight_group,
                    group_id,
                    slice_id,
                    batch,
                    group_score,
                    config,
                )
                future_map[future] = (group_id, slice_id)
            for future in as_completed(future_map):
                group_id, elapsed, rows_out, error = future.result()
                if error is not None:
                    raise error
                rows.extend(rows_out)
                group_timings.append((group_id, elapsed))
                groups_processed += 1
                logger.info(
                    "domain_insights_group_done group_id=%s seconds=%.3f progress=%d/%d",
                    group_id,
                    elapsed,
                    groups_processed,
                    estimated_total,
                )
    else:
        for group_id, slice_id, batch, group_score in tasks:
            logger.info(
                "domain_insights_group_start group_id=%s slice_id=%s size=%d progress=%d/%d",
                group_id,
                slice_id,
                len(batch),
                groups_processed + 1,
                estimated_total,
            )
            group_id, elapsed, rows_out, error = _process_domain_insight_group(
                group_id, slice_id, batch, group_score, config
            )
            if error is not None:
                raise error
            rows.extend(rows_out)
            group_timings.append((group_id, elapsed))
            groups_processed += 1
            logger.info(
                "domain_insights_group_done group_id=%s seconds=%.3f progress=%d/%d",
                group_id,
                elapsed,
                groups_processed,
                estimated_total,
            )
    for item in fallback_items:
        if not config.allow_heuristics:
            raise ValueError("Heuristic fallback disabled but max_items produced leftovers")
        rule_text = str(item.get("rule_text", "")).strip()
        outputs = str(item.get("outputs", "")).strip()
        logic_comment = rule_text or "Derived rule from legacy logic."
        indicative = f"Indicative: {outputs}" if outputs else "Indicative: Outcome inferred."
        group_id = _hash_id(f"{item['slice_id']}:fallback")
        group_score = 0.1
        rows.append(
            {
                "rule_id": item["rule_id"],
                "slice_id": item["slice_id"],
                "logic_comment": _truncate(logic_comment, config.max_comment_chars),
                "indicative_result": _truncate(indicative, config.max_indicative_chars),
                "confidence": 0.2,
                "llm_source": "heuristic",
                "group_id": group_id,
                "group_score": group_score,
                "source_ref": item["source_ref"],
            }
        )
    overall_elapsed = time.perf_counter() - overall_start
    if group_timings:
        for gid, elapsed in group_timings:
            logger.info("domain_insights_group_timing group_id=%s seconds=%.3f", gid, elapsed)
        logger.info(
            "domain_insights_groups_total count=%d seconds=%.3f",
            len(group_timings),
            overall_elapsed,
        )
    return rows


def _node_maps(
    code_graph_nodes: list[dict],
) -> tuple[dict[str, dict], dict[str, str], dict[str, str]]:
    node_by_id: dict[str, dict] = {}
    label_by_id: dict[str, str] = {}
    table_by_id: dict[str, str] = {}
    for node in code_graph_nodes:
        node_id = node.get("node_id")
        if not node_id:
            continue
        node_by_id[node_id] = node
        label = node.get("label") or node.get("table_name") or node.get("symbol_id") or node_id
        label_by_id[node_id] = str(label)
        if node.get("node_type") == "table":
            table_name = node.get("table_name") or node.get("label") or node_id
            table_by_id[node_id] = str(table_name)
    return node_by_id, label_by_id, table_by_id


def _build_symbol_entry_map(
    symbols: list[dict],
    slice_manifest: list[dict],
    entry_by_slice: dict[str, str],
    code_graph_nodes: list[dict],
    recursive_nodes: set[str],
) -> list[dict]:
    node_by_id, label_by_id, _ = _node_maps(code_graph_nodes)
    symbol_to_slice: dict[str, str] = {}
    for row in slice_manifest:
        symbol_id = row.get("symbol_id")
        slice_id = row.get("slice_id")
        if symbol_id and slice_id and symbol_id not in symbol_to_slice:
            symbol_to_slice[symbol_id] = slice_id
    rows: list[dict] = []
    for row in symbols:
        symbol_id = row.get("symbol_id")
        if not symbol_id:
            continue
        slice_id = symbol_to_slice.get(symbol_id)
        if not slice_id:
            continue
        entry_node_id = entry_by_slice.get(slice_id)
        if not entry_node_id:
            continue
        file_path = row.get("file_path", "")
        path_obj = Path(file_path).expanduser().resolve()
        file_path = str(path_obj)
        file_name = path_obj.name
        file_ext = path_obj.suffix.lower()
        entry_label = label_by_id.get(entry_node_id) or node_by_id.get(entry_node_id, {}).get(
            "label", ""
        )
        rows.append(
            {
                "symbol_id": symbol_id,
                "slice_id": slice_id,
                "entry_point_id": entry_node_id,
                "entry_point_label": entry_label,
                "symbol_kind": row.get("kind", ""),
                "file_path": file_path,
                "file_name": file_name,
                "file_ext": file_ext,
                "is_recursive": symbol_id in recursive_nodes,
                "source_ref": row.get("source_ref", row.get("file_path", "")),
            }
        )
    return rows


def _graph_adjacency(code_graph_edges: list[dict]) -> dict[str, list[str]]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    for row in code_graph_edges:
        from_id = row.get("from_id")
        to_id = row.get("to_id")
        if from_id and to_id:
            adjacency[from_id].append(to_id)
    return adjacency


def _pagerank_by_node(
    code_graph_nodes: list[dict],
    code_graph_edges: list[dict],
    node_type_weights: dict[str, float],
) -> dict[str, float]:
    graph = nx.DiGraph()
    node_by_id, _, _ = _node_maps(code_graph_nodes)
    for node in code_graph_nodes:
        node_id = node.get("node_id")
        if node_id:
            graph.add_node(node_id)
    for row in code_graph_edges:
        from_id = row.get("from_id")
        to_id = row.get("to_id")
        if from_id and to_id:
            graph.add_edge(from_id, to_id)
    if graph.number_of_nodes() == 0:
        return {}
    personalization = {}
    for node in graph.nodes:
        node_type = node_by_id.get(node, {}).get("node_type", "symbol")
        personalization[node] = float(node_type_weights.get(node_type, 1.0))
    return nx.pagerank(graph, personalization=personalization)


def _recursive_nodes(code_graph_edges: list[dict]) -> set[str]:
    graph = nx.DiGraph()
    for row in code_graph_edges:
        from_id = row.get("from_id")
        to_id = row.get("to_id")
        if from_id and to_id:
            graph.add_edge(from_id, to_id)
    recursive: set[str] = set()
    for component in nx.strongly_connected_components(graph):
        if len(component) > 1:
            recursive.update(component)
    for node_id in graph.nodes:
        if graph.has_edge(node_id, node_id):
            recursive.add(node_id)
    return recursive


def _entry_graph_depth_metrics(
    adjacency: dict[str, list[str]],
    entry: str,
    max_depth: int,
    node_limit: int,
) -> tuple[dict[str, float], set[str]]:
    max_depth_seen = 0
    reachable: set[str] = set()
    stack: list[tuple[str, int, set[str]]] = [(entry, 0, {entry})]
    while stack:
        node, depth, path = stack.pop()
        reachable.add(node)
        if depth > max_depth_seen:
            max_depth_seen = depth
        if depth >= max_depth:
            continue
        for neighbor in adjacency.get(node, []):
            if neighbor in path:
                continue
            stack.append((neighbor, depth + 1, path | {neighbor}))
    capped_depth = min(max_depth_seen, max_depth)
    normalized = capped_depth / max_depth if max_depth else 0.0
    log_scaled = math.log1p(capped_depth) / math.log1p(max_depth) if max_depth else 0.0
    capped_nodes = min(len(reachable), node_limit)
    depth_breadth = (capped_depth * capped_nodes) / node_limit if node_limit else 0.0
    return {
        "max_depth": float(max_depth_seen),
        "capped_depth": float(capped_depth),
        "normalized": float(normalized),
        "log_scaled": float(log_scaled),
        "depth_breadth": float(depth_breadth),
        "reachable_nodes": float(len(reachable)),
    }, reachable


def _entry_graph_edges(
    edges: list[tuple[str, str]],
    reachable: set[str],
    entry_nodes: set[str],
    entry_type: str,
) -> list[tuple[str, str]]:
    if entry_type == "entry_group":
        return [
            (source, target)
            for source, target in edges
            if source in reachable
            and target in reachable
            and not (target in entry_nodes and source not in entry_nodes)
        ]
    return [
        (source, target)
        for source, target in edges
        if source in reachable and target in reachable and target not in entry_nodes
    ]


def _entry_graph_candidates(
    code_graph_nodes: list[dict],
    code_graph_edges: list[dict],
    config: DomainArchitectConfig,
) -> tuple[list[dict], dict[str, object]]:
    node_ids = [row.get("node_id") for row in code_graph_nodes if row.get("node_id")]
    edges = [
        (row.get("from_id"), row.get("to_id"))
        for row in code_graph_edges
        if row.get("from_id") and row.get("to_id")
    ]
    graph = nx.DiGraph()
    graph.add_nodes_from(node_ids)
    graph.add_edges_from(edges)
    adjacency = _graph_adjacency(code_graph_edges)
    in_degree: dict[str, int] = defaultdict(int)
    out_degree: dict[str, int] = defaultdict(int)
    for from_id, to_nodes in adjacency.items():
        out_degree[from_id] += len(to_nodes)
        for to_id in to_nodes:
            in_degree[to_id] += 1
    entry_candidates = [
        node_id
        for node_id in node_ids
        if in_degree.get(node_id, 0) == 0 and out_degree.get(node_id, 0) > 0
    ]
    entry_groups: list[dict[str, object]] = []
    entry_group_nodes: set[str] = set()
    sccs = list(nx.strongly_connected_components(graph))
    for comp in sccs:
        if len(comp) == 1:
            continue
        has_incoming = False
        for node in comp:
            for pred in graph.predecessors(node):
                if pred not in comp:
                    has_incoming = True
                    break
            if has_incoming:
                break
        if not has_incoming:
            group_nodes = sorted(comp)
            group_id = "scc_" + "_".join(group_nodes)
            entry_groups.append({"group_id": group_id, "nodes": group_nodes})
            entry_group_nodes.update(group_nodes)
    recursive = {node for node in graph.nodes if graph.has_edge(node, node)}
    for comp in sccs:
        if len(comp) > 1:
            recursive |= comp
    exit_nodes = {
        node_id for node_id in node_ids if out_degree.get(node_id, 0) == 0 or node_id in recursive
    }
    entry_cache: dict[str, tuple[dict[str, float], set[str]]] = {}
    candidates: list[dict] = []
    excluded: list[dict] = []
    for entry in entry_candidates:
        metrics, reachable = _entry_graph_depth_metrics(
            adjacency,
            entry,
            config.entry_graph_max_depth,
            config.entry_graph_node_limit,
        )
        entry_cache[entry] = (metrics, reachable)
        has_exit = bool(reachable & exit_nodes)
        if not has_exit:
            excluded.append(
                {
                    "entry_key": entry,
                    "entry_type": "entry",
                    "reason": "no_exit",
                    "metrics": metrics,
                    "entry_nodes": [entry],
                }
            )
            continue
        if metrics["capped_depth"] < config.entry_graph_depth_threshold:
            excluded.append(
                {
                    "entry_key": entry,
                    "entry_type": "entry",
                    "reason": "below_threshold",
                    "metrics": metrics,
                    "entry_nodes": [entry],
                }
            )
            continue
        candidates.append(
            {
                "entry_key": entry,
                "entry_type": "entry",
                "entry_nodes": [entry],
                "reachable": reachable,
                "metrics": metrics,
            }
        )
    for group in entry_groups:
        group_id = str(group.get("group_id", "group"))
        group_nodes = set(group.get("nodes", []))
        if not group_nodes:
            continue
        reachable = set(group_nodes)
        metrics_by_node: list[dict[str, float]] = []
        for entry in group_nodes:
            metrics, entry_reachable = entry_cache.get(entry) or _entry_graph_depth_metrics(
                adjacency,
                entry,
                config.entry_graph_max_depth,
                config.entry_graph_node_limit,
            )
            entry_cache[entry] = (metrics, entry_reachable)
            metrics_by_node.append(metrics)
            reachable |= entry_reachable
        has_exit = bool(reachable & exit_nodes)
        metrics = max(metrics_by_node, key=lambda item: item["max_depth"]) if metrics_by_node else {
            "max_depth": 0.0,
            "capped_depth": 0.0,
            "normalized": 0.0,
            "log_scaled": 0.0,
            "depth_breadth": 0.0,
            "reachable_nodes": float(len(reachable)),
        }
        if not has_exit:
            excluded.append(
                {
                    "entry_key": group_id,
                    "entry_type": "entry_group",
                    "reason": "no_exit",
                    "metrics": metrics,
                    "entry_nodes": sorted(group_nodes),
                }
            )
            continue
        if metrics["capped_depth"] < config.entry_graph_depth_threshold:
            excluded.append(
                {
                    "entry_key": group_id,
                    "entry_type": "entry_group",
                    "reason": "below_threshold",
                    "metrics": metrics,
                    "entry_nodes": sorted(group_nodes),
                }
            )
            continue
        candidates.append(
            {
                "entry_key": group_id,
                "entry_type": "entry_group",
                "entry_nodes": sorted(group_nodes),
                "reachable": reachable,
                "metrics": metrics,
            }
        )
    if config.entry_keys_path:
        allowed_keys = {
            line.strip()
            for line in config.entry_keys_path.read_text().splitlines()
            if line.strip()
        }
        candidates = [item for item in candidates if item["entry_key"] in allowed_keys]
    eligible = list(candidates)
    if config.entry_graph_top_k is not None:
        candidates = sorted(
            candidates,
            key=lambda item: (
                float(item["metrics"]["capped_depth"]),
                float(item["metrics"]["depth_breadth"]),
            ),
            reverse=True,
        )[: config.entry_graph_top_k]
    summary = {
        "exit_nodes": exit_nodes,
        "excluded": excluded,
        "eligible": eligible,
        "entry_candidates": entry_candidates,
        "entry_groups": entry_groups,
        "edges": edges,
    }
    return candidates, summary


def _slice_pagerank_scores(
    slice_nodes: dict[str, set[str]],
    pagerank_by_node: dict[str, float],
) -> dict[str, float]:
    scores: dict[str, float] = {}
    for slice_id, node_ids in slice_nodes.items():
        values = [pagerank_by_node.get(node_id, 0.0) for node_id in node_ids]
        scores[slice_id] = sum(values) / len(values) if values else 0.0
    return scores


def _pagerank_entry_by_slice(
    slice_nodes: dict[str, set[str]],
    pagerank_by_node: dict[str, float],
    in_degree: dict[str, int],
    out_degree: dict[str, int],
    entry_filter: str,
    recursive_nodes: set[str],
    exclude_recursive: bool,
    node_type_by_id: dict[str, str],
    node_type_weights: dict[str, float],
) -> dict[str, str]:
    entries: dict[str, str] = {}
    for slice_id, node_ids in slice_nodes.items():
        if not node_ids:
            continue
        candidates = list(node_ids)
        if entry_filter == "in_degree_zero":
            candidates = [
                node_id
                for node_id in candidates
                if in_degree.get(node_id, 0) == 0 and out_degree.get(node_id, 0) > 0
            ]
        else:
            candidates = [
                node_id for node_id in candidates if out_degree.get(node_id, 0) > 0
            ]
        if exclude_recursive:
            candidates = [node_id for node_id in candidates if node_id not in recursive_nodes]
        if not candidates:
            continue
        def entry_score(node_id: str) -> tuple[float, float]:
            pr = pagerank_by_node.get(node_id, 0.0)
            node_type = node_type_by_id.get(node_id, "symbol")
            weight = float(node_type_weights.get(node_type, 1.0))
            return (pr, weight)

        best = max(candidates, key=entry_score)
        entries[slice_id] = best
    return entries


def _reconstruct_path(
    parents: dict[str, str | None],
    entry_id: str,
    target_id: str,
) -> list[str]:
    path: list[str] = []
    current = target_id
    while current is not None:
        path.append(current)
        if current == entry_id:
            break
        current = parents.get(current)
    return list(reversed(path)) if path and path[-1] == entry_id else []


def _truncate_path_labels(
    labels: list[str],
    max_nodes: int,
) -> str:
    if len(labels) <= max_nodes:
        return " -> ".join(labels)
    head = labels[: max_nodes - 1]
    return " -> ".join(head + ["..."])


def _heuristic_flow_summary(item: dict, max_chars: int) -> str:
    entry = item.get("entry_point") or item.get("entry_label") or "entry"
    tables = item.get("exit_tables", [])
    steps = item.get("path_steps", [])
    parts = [f"Entry {entry}"]
    if steps:
        parts.append(f"path: {steps[0]}")
    if tables:
        parts.append(f"db: {', '.join(tables[:3])}")
    summary = "; ".join(parts)
    return _truncate(summary, max_chars)


def _build_endpoint_flows(
    endpoints: list[dict],
    code_graph_nodes: list[dict],
    code_graph_edges: list[dict],
    entry_exit_map: list[dict],
    pagerank_by_node: dict[str, float],
    recursive_nodes: set[str],
    config: DomainArchitectConfig,
) -> tuple[list[dict], dict[str, set[str]]]:
    _ensure_llm_available(config, "LLM endpoint flows")
    node_by_id, label_by_id, table_by_id = _node_maps(code_graph_nodes)
    adjacency = _graph_adjacency(code_graph_edges)
    in_degree: dict[str, int] = defaultdict(int)
    out_degree: dict[str, int] = defaultdict(int)
    for from_id, to_nodes in adjacency.items():
        out_degree[from_id] += len(to_nodes)
        for to_id in to_nodes:
            in_degree[to_id] += 1
    effect_by_pair: dict[tuple[str, str], str] = {}
    for row in entry_exit_map:
        entry_id = row.get("entry_node_id")
        exit_id = row.get("exit_node_id")
        effect = row.get("effect_type", "")
        if entry_id and exit_id:
            effect_by_pair[(entry_id, exit_id)] = effect

    total_nodes = max(1, len(node_by_id))
    flow_items: list[dict] = []
    coverage_by_endpoint: dict[str, set[str]] = {}
    for endpoint in endpoints:
        entry_node_id = endpoint.get("entry_node_id")
        if not entry_node_id:
            continue
        visited: set[str] = set()
        parents: dict[str, str | None] = {entry_node_id: None}
        queue = [entry_node_id]
        while queue and len(visited) < config.max_endpoint_nodes:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            for neighbor in adjacency.get(current, []):
                if neighbor not in parents:
                    parents[neighbor] = current
                if neighbor not in visited:
                    queue.append(neighbor)
        coverage_by_endpoint[endpoint["endpoint_id"]] = visited

        if config.exit_filter == "out_degree_zero":
            exit_nodes = [
                node_id
                for node_id in visited
                if out_degree.get(node_id, 0) == 0 and node_id in node_by_id
            ]
        elif config.exit_filter == "table_or_sink":
            exit_nodes = [
                node_id
                for node_id in visited
                if node_id in table_by_id or out_degree.get(node_id, 0) == 0
            ]
        elif config.exit_filter == "sink_or_recursive":
            exit_nodes = [
                node_id
                for node_id in visited
                if out_degree.get(node_id, 0) == 0 or node_id in recursive_nodes
            ]
        else:
            exit_nodes = [node_id for node_id in visited if node_id in table_by_id]
        def exit_score(node_id: str) -> tuple[float, float]:
            pr = pagerank_by_node.get(node_id, 0.0)
            node_type = node_by_id.get(node_id, {}).get("node_type", "symbol")
            weight = float(config.node_type_weights.get(node_type, 1.0))
            return (pr, weight)

        exit_nodes = sorted(exit_nodes, key=exit_score, reverse=True)
        exit_tables = [table_by_id[node_id] for node_id in exit_nodes if node_id in table_by_id]
        exit_types = ["db_exit" for _ in exit_tables]
        path_steps: list[str] = []
        path_lengths: list[int] = []
        path_pagerank_sums: list[float] = []
        path_weighted_pagerank_sums: list[float] = []
        for node_id in exit_nodes[: config.max_endpoint_paths]:
            path = _reconstruct_path(parents, entry_node_id, node_id)
            if not path:
                continue
            labels = [label_by_id.get(pid, pid) for pid in path]
            step = _truncate_path_labels(labels, config.max_endpoint_path_nodes)
            effect = effect_by_pair.get((entry_node_id, node_id), "")
            if effect:
                step = f"{step} ({effect})"
            path_steps.append(step)
            path_lengths.append(len(path))
            path_pagerank_sums.append(sum(pagerank_by_node.get(pid, 0.0) for pid in path))
            path_weighted_pagerank_sums.append(
                sum(
                    pagerank_by_node.get(pid, 0.0)
                    * float(config.node_type_weights.get(node_by_id.get(pid, {}).get("node_type", "symbol"), 1.0))
                    for pid in path
                )
            )
        max_depth = max(path_lengths) if path_lengths else 0
        max_cumulative_path_pagerank = max(path_pagerank_sums) if path_pagerank_sums else 0.0
        max_cumulative_weighted_pagerank = (
            max(path_weighted_pagerank_sums) if path_weighted_pagerank_sums else 0.0
        )
        cumulative_exit_pagerank = sum(pagerank_by_node.get(pid, 0.0) for pid in exit_nodes)
        cumulative_visited_pagerank = sum(
            pagerank_by_node.get(pid, 0.0) for pid in visited
        )
        cumulative_exit_weighted_pagerank = sum(
            pagerank_by_node.get(pid, 0.0)
            * float(config.node_type_weights.get(node_by_id.get(pid, {}).get("node_type", "symbol"), 1.0))
            for pid in exit_nodes
        )
        cumulative_visited_weighted_pagerank = sum(
            pagerank_by_node.get(pid, 0.0)
            * float(config.node_type_weights.get(node_by_id.get(pid, {}).get("node_type", "symbol"), 1.0))
            for pid in visited
        )
        entry_label = label_by_id.get(entry_node_id, entry_node_id)
        coverage_ratio = len(visited) / total_nodes
        flow_items.append(
            {
                "endpoint_id": endpoint["endpoint_id"],
                "endpoint_type": endpoint.get("name", "").split(":", 1)[0],
                "slice_id": endpoint.get("slice_id"),
                "entry_node_id": entry_node_id,
                "entry_label": entry_label,
                "entry_point": endpoint.get("entry_point", ""),
                "exit_tables": exit_tables[: config.max_endpoint_paths],
                "exit_types": exit_types[: config.max_endpoint_paths],
                "path_steps": path_steps,
                "path_lengths": path_lengths,
                "path_pagerank_sums": path_pagerank_sums,
                "path_weighted_pagerank_sums": path_weighted_pagerank_sums,
                "max_depth": max_depth,
                "max_cumulative_path_pagerank": max_cumulative_path_pagerank,
                "max_cumulative_weighted_pagerank": max_cumulative_weighted_pagerank,
                "cumulative_exit_pagerank": cumulative_exit_pagerank,
                "cumulative_visited_pagerank": cumulative_visited_pagerank,
                "cumulative_exit_weighted_pagerank": cumulative_exit_weighted_pagerank,
                "cumulative_visited_weighted_pagerank": cumulative_visited_weighted_pagerank,
                "reachable_nodes": len(visited),
                "total_nodes": total_nodes,
                "coverage_ratio": round(coverage_ratio, 4),
            }
        )

    fallback_flow_items: list[dict] = []
    if config.llm_endpoint_flow_max_items is not None:
        max_items = max(0, config.llm_endpoint_flow_max_items)
        if len(flow_items) > max_items:
            fallback_flow_items = flow_items[max_items:]
            flow_items = flow_items[:max_items]

    batch_size = max(1, config.llm_endpoint_flow_batch_size)
    flow_rows: list[dict] = []
    for start in range(0, len(flow_items), batch_size):
        batch = flow_items[start : start + batch_size]
        prompt = _endpoint_flow_batch_prompt(batch, config.max_flow_summary_chars)
        if len(prompt) > config.llm_max_input_chars and len(batch) > 1:
            for item in batch:
                single_prompt = _endpoint_flow_prompt(item, config.max_flow_summary_chars)
                payload = _call_llm(config, single_prompt)
                flow_summary = str(payload.get("flow_summary", "")).strip()
                if not flow_summary:
                    raise ValueError(
                        f"LLM response missing flow_summary for endpoint {item['endpoint_id']}"
                    )
                flow_rows.append(
                    {
                        "endpoint_id": item["endpoint_id"],
                        "slice_id": item.get("slice_id"),
                        "endpoint_type": item.get("endpoint_type"),
                        "entry_node_id": item.get("entry_node_id"),
                        "entry_label": _truncate(
                            item.get("entry_label", ""), config.max_name_chars
                        ),
                        "entry_point": item.get("entry_point", ""),
                        "exit_tables": json.dumps(
                            item.get("exit_tables", []), ensure_ascii=True
                        ),
                        "exit_types": json.dumps(
                            item.get("exit_types", []), ensure_ascii=True
                        ),
                        "path_steps": json.dumps(item.get("path_steps", []), ensure_ascii=True),
                        "path_lengths": json.dumps(item.get("path_lengths", []), ensure_ascii=True),
                        "path_pagerank_sums": json.dumps(
                            item.get("path_pagerank_sums", []), ensure_ascii=True
                        ),
                        "path_weighted_pagerank_sums": json.dumps(
                            item.get("path_weighted_pagerank_sums", []), ensure_ascii=True
                        ),
                        "max_depth": item.get("max_depth", 0),
                        "max_cumulative_path_pagerank": item.get(
                            "max_cumulative_path_pagerank", 0.0
                        ),
                        "max_cumulative_weighted_pagerank": item.get(
                            "max_cumulative_weighted_pagerank", 0.0
                        ),
                        "cumulative_exit_pagerank": item.get("cumulative_exit_pagerank", 0.0),
                        "cumulative_visited_pagerank": item.get(
                            "cumulative_visited_pagerank", 0.0
                        ),
                        "cumulative_exit_weighted_pagerank": item.get(
                            "cumulative_exit_weighted_pagerank", 0.0
                        ),
                        "cumulative_visited_weighted_pagerank": item.get(
                            "cumulative_visited_weighted_pagerank", 0.0
                        ),
                        "reachable_nodes": item.get("reachable_nodes", 0),
                        "total_nodes": item.get("total_nodes", 0),
                        "coverage_ratio": item.get("coverage_ratio", 0.0),
                        "flow_summary": _truncate(
                            flow_summary, config.max_flow_summary_chars
                        ),
                        "source_ref": item.get("entry_point", ""),
                    }
                )
            continue

        try:
            payload_items = _call_llm_list(config, prompt)
            payload_by_id: dict[str, dict] = {}
            for idx, entry in enumerate(payload_items):
                endpoint_id = str(entry.get("endpoint_id", "")).strip()
                if not endpoint_id and idx < len(batch):
                    # Fall back to positional mapping when the model omits endpoint_id
                    endpoint_id = batch[idx]["endpoint_id"]
                if not endpoint_id:
                    raise ValueError("LLM response missing endpoint_id for flow summary")
                payload_by_id[endpoint_id] = entry
            for item in batch:
                payload = payload_by_id.get(item["endpoint_id"])
                if not payload:
                    raise ValueError(
                        f"LLM response missing flow summary for endpoint {item['endpoint_id']}"
                    )
                flow_summary = str(payload.get("flow_summary", "")).strip()
                if not flow_summary:
                    flow_summary = f"Flow summary unavailable; endpoint {item['endpoint_id']}"
                flow_rows.append(
                    {
                        "endpoint_id": item["endpoint_id"],
                        "slice_id": item.get("slice_id"),
                        "endpoint_type": item.get("endpoint_type"),
                        "entry_node_id": item.get("entry_node_id"),
                        "entry_label": _truncate(
                            item.get("entry_label", ""), config.max_name_chars
                        ),
                        "entry_point": item.get("entry_point", ""),
                        "exit_tables": json.dumps(
                            item.get("exit_tables", []), ensure_ascii=True
                        ),
                        "exit_types": json.dumps(
                            item.get("exit_types", []), ensure_ascii=True
                        ),
                        "path_steps": json.dumps(
                            item.get("path_steps", []), ensure_ascii=True
                        ),
                        "path_lengths": json.dumps(
                            item.get("path_lengths", []), ensure_ascii=True
                        ),
                        "path_pagerank_sums": json.dumps(
                            item.get("path_pagerank_sums", []), ensure_ascii=True
                        ),
                        "path_weighted_pagerank_sums": json.dumps(
                            item.get("path_weighted_pagerank_sums", []), ensure_ascii=True
                        ),
                        "max_depth": item.get("max_depth", 0),
                        "max_cumulative_path_pagerank": item.get(
                            "max_cumulative_path_pagerank", 0.0
                        ),
                        "max_cumulative_weighted_pagerank": item.get(
                            "max_cumulative_weighted_pagerank", 0.0
                        ),
                        "cumulative_exit_pagerank": item.get("cumulative_exit_pagerank", 0.0),
                        "cumulative_visited_pagerank": item.get(
                            "cumulative_visited_pagerank", 0.0
                        ),
                        "cumulative_exit_weighted_pagerank": item.get(
                            "cumulative_exit_weighted_pagerank", 0.0
                        ),
                        "cumulative_visited_weighted_pagerank": item.get(
                            "cumulative_visited_weighted_pagerank", 0.0
                        ),
                        "reachable_nodes": item.get("reachable_nodes", 0),
                        "total_nodes": item.get("total_nodes", 0),
                        "coverage_ratio": item.get("coverage_ratio", 0.0),
                        "flow_summary": _truncate(
                            flow_summary, config.max_flow_summary_chars
                        ),
                        "source_ref": item.get("entry_point", ""),
                    }
                )
        except Exception:
            if not config.allow_heuristics:
                raise
            for item in batch:
                flow_summary = _heuristic_flow_summary(
                    item, config.max_flow_summary_chars
                )
                flow_rows.append(
                    {
                        "endpoint_id": item["endpoint_id"],
                        "slice_id": item.get("slice_id"),
                        "endpoint_type": item.get("endpoint_type"),
                        "entry_node_id": item.get("entry_node_id"),
                        "entry_label": _truncate(
                            item.get("entry_label", ""), config.max_name_chars
                        ),
                        "entry_point": item.get("entry_point", ""),
                        "exit_tables": json.dumps(
                            item.get("exit_tables", []), ensure_ascii=True
                        ),
                        "exit_types": json.dumps(
                            item.get("exit_types", []), ensure_ascii=True
                        ),
                        "path_steps": json.dumps(
                            item.get("path_steps", []), ensure_ascii=True
                        ),
                        "path_lengths": json.dumps(
                            item.get("path_lengths", []), ensure_ascii=True
                        ),
                        "path_pagerank_sums": json.dumps(
                            item.get("path_pagerank_sums", []), ensure_ascii=True
                        ),
                        "path_weighted_pagerank_sums": json.dumps(
                            item.get("path_weighted_pagerank_sums", []), ensure_ascii=True
                        ),
                        "max_depth": item.get("max_depth", 0),
                        "max_cumulative_path_pagerank": item.get(
                            "max_cumulative_path_pagerank", 0.0
                        ),
                        "max_cumulative_weighted_pagerank": item.get(
                            "max_cumulative_weighted_pagerank", 0.0
                        ),
                        "cumulative_exit_pagerank": item.get("cumulative_exit_pagerank", 0.0),
                        "cumulative_visited_pagerank": item.get(
                            "cumulative_visited_pagerank", 0.0
                        ),
                        "cumulative_exit_weighted_pagerank": item.get(
                            "cumulative_exit_weighted_pagerank", 0.0
                        ),
                        "cumulative_visited_weighted_pagerank": item.get(
                            "cumulative_visited_weighted_pagerank", 0.0
                        ),
                        "reachable_nodes": item.get("reachable_nodes", 0),
                        "total_nodes": item.get("total_nodes", 0),
                        "coverage_ratio": item.get("coverage_ratio", 0.0),
                        "flow_summary": flow_summary,
                        "source_ref": item.get("entry_point", ""),
                    }
                )
    if fallback_flow_items and not config.allow_heuristics:
        logger.warning(
            "allow_heuristics disabled but endpoint flow max items exceeded; using heuristic summaries"
        )
    for item in fallback_flow_items:
        flow_summary = _heuristic_flow_summary(item, config.max_flow_summary_chars)
        flow_rows.append(
            {
                "endpoint_id": item["endpoint_id"],
                "slice_id": item.get("slice_id"),
                "endpoint_type": item.get("endpoint_type"),
                "entry_node_id": item.get("entry_node_id"),
                "entry_label": _truncate(item.get("entry_label", ""), config.max_name_chars),
                "entry_point": item.get("entry_point", ""),
                "exit_tables": json.dumps(item.get("exit_tables", []), ensure_ascii=True),
                "exit_types": json.dumps(item.get("exit_types", []), ensure_ascii=True),
                "path_steps": json.dumps(item.get("path_steps", []), ensure_ascii=True),
                "path_lengths": json.dumps(item.get("path_lengths", []), ensure_ascii=True),
                "path_pagerank_sums": json.dumps(
                    item.get("path_pagerank_sums", []), ensure_ascii=True
                ),
                "path_weighted_pagerank_sums": json.dumps(
                    item.get("path_weighted_pagerank_sums", []), ensure_ascii=True
                ),
                "max_depth": item.get("max_depth", 0),
                "max_cumulative_path_pagerank": item.get("max_cumulative_path_pagerank", 0.0),
                "max_cumulative_weighted_pagerank": item.get(
                    "max_cumulative_weighted_pagerank", 0.0
                ),
                "cumulative_exit_pagerank": item.get("cumulative_exit_pagerank", 0.0),
                "cumulative_visited_pagerank": item.get("cumulative_visited_pagerank", 0.0),
                "cumulative_exit_weighted_pagerank": item.get(
                    "cumulative_exit_weighted_pagerank", 0.0
                ),
                "cumulative_visited_weighted_pagerank": item.get(
                    "cumulative_visited_weighted_pagerank", 0.0
                ),
                "reachable_nodes": item.get("reachable_nodes", 0),
                "total_nodes": item.get("total_nodes", 0),
                "coverage_ratio": item.get("coverage_ratio", 0.0),
                "flow_summary": flow_summary,
                "source_ref": item.get("entry_point", ""),
            }
        )
    return flow_rows, coverage_by_endpoint


def _build_entry_vectors(
    items: list[dict],
    model_name: str,
    batch_size: int,
) -> list[list[float]]:
    if not items:
        return []
    texts: list[str] = []
    for item in items:
        parts = [
            item.get("entry_label", ""),
            item.get("entry_point", ""),
            " ".join(item.get("exit_tables", [])),
            " ".join(item.get("path_steps", [])),
        ]
        texts.append(" ".join(part for part in parts if part))
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
    return [embeddings[idx].tolist() for idx in range(len(texts))]


def _build_pagerank_entry_insights(
    endpoints: list[dict],
    endpoint_flows: list[dict],
    pagerank_by_node: dict[str, float],
    config: DomainArchitectConfig,
) -> list[dict]:
    _ensure_llm_available(config, "LLM entry explanations")
    flow_by_endpoint = {row["endpoint_id"]: row for row in endpoint_flows}
    candidates: list[dict] = []
    for endpoint in endpoints:
        endpoint_id = endpoint.get("endpoint_id")
        entry_node_id = endpoint.get("entry_node_id")
        if not endpoint_id or not entry_node_id:
            continue
        flow = flow_by_endpoint.get(endpoint_id)
        if not flow:
            continue
        exit_tables = json.loads(flow.get("exit_tables", "[]"))
        if not exit_tables:
            continue
        candidates.append(
            {
                "endpoint_id": endpoint_id,
                "entry_node_id": entry_node_id,
                "entry_label": flow.get("entry_label", ""),
                "entry_point": flow.get("entry_point", ""),
                "exit_tables": exit_tables,
                "exit_types": json.loads(flow.get("exit_types", "[]")),
                "path_steps": json.loads(flow.get("path_steps", "[]")),
                "pagerank_score": pagerank_by_node.get(entry_node_id, 0.0),
                "slice_id": flow.get("slice_id"),
            }
        )
    top_k = sorted(
        candidates, key=lambda row: row.get("pagerank_score", 0.0), reverse=True
    )[: config.pagerank_entry_top_k]
    if not top_k:
        return []
    vectors: list[list[float]] = []
    if config.enable_entry_embeddings:
        vectors = _build_entry_vectors(
            top_k, config.entry_embedding_model, config.entry_embedding_batch_size
        )
    rows: list[dict] = []
    for idx, item in enumerate(top_k):
        prompt = _pagerank_entry_prompt(item, config.max_comment_chars)
        payload = _call_llm(config, prompt)
        explanation = str(payload.get("explanation", "")).strip()
        if not explanation:
            raise ValueError(f"LLM response missing explanation for entry {item['endpoint_id']}")
        rows.append(
            {
                "entry_id": _hash_id(item["entry_node_id"]),
                "endpoint_id": item["endpoint_id"],
                "entry_node_id": item["entry_node_id"],
                "entry_label": item.get("entry_label", ""),
                "entry_point": item.get("entry_point", ""),
                "pagerank_score": item.get("pagerank_score", 0.0),
                "exit_tables": json.dumps(item.get("exit_tables", []), ensure_ascii=True),
                "exit_types": json.dumps(item.get("exit_types", []), ensure_ascii=True),
                "path_steps": json.dumps(item.get("path_steps", []), ensure_ascii=True),
                "explanation": _truncate(explanation, config.max_comment_chars),
                "vector": vectors[idx] if vectors else [],
                "vector_dim": len(vectors[idx]) if vectors else 0,
                "source_ref": item.get("entry_point", ""),
            }
        )
    return rows


def _build_endpoint_coverage(
    coverage_by_endpoint: dict[str, set[str]],
    total_nodes: int,
) -> list[dict]:
    if total_nodes <= 0:
        total_nodes = 1
    covered: set[str] = set()
    for nodes in coverage_by_endpoint.values():
        covered |= nodes
    ratio = len(covered) / total_nodes
    return [
        {
            "coverage_id": _hash_id("endpoint_coverage"),
            "covered_nodes": len(covered),
            "total_nodes": total_nodes,
            "coverage_ratio": round(ratio, 4),
            "source_ref": "code_graph_nodes",
        }
    ]


def _build_context_reasoning(
    rule_slice_map: dict[str, str],
    vector_clusters: dict[str, int],
    graph_clusters: dict[str, int],
    slice_manifest: list[dict],
    slice_pagerank: dict[str, float],
    context_names: dict[str, str],
) -> list[dict]:
    table_by_slice: dict[str, set[str]] = defaultdict(set)
    for row in slice_manifest:
        slice_id = row.get("slice_id")
        table_name = row.get("table_name")
        if slice_id and table_name:
            table_by_slice[slice_id].add(str(table_name))
    rows: list[dict] = []
    for slice_id in set(rule_slice_map.values()):
        graph_cluster = graph_clusters.get(slice_id, 0)
        vector_cluster = vector_clusters.get(slice_id, 0)
        tables = sorted(table_by_slice.get(slice_id, []))[:5]
        graph_score, vector_score, coverage_score = _group_scores(
            [], tables, [], graph_cluster, vector_cluster
        )
        pagerank_score = slice_pagerank.get(slice_id, 0.0)
        combined_score = _combined_score(
            graph_score, vector_score, coverage_score, pagerank_score
        )
        rationale = (
            f"Clustered by graph community {graph_cluster} and vector cluster {vector_cluster}. "
            f"Shared tables: {', '.join(tables)}."
        ).strip()
        context_key = f"g{graph_cluster}-v{vector_cluster}"
        context_label = context_names.get(str(vector_cluster), "")
        rows.append(
            {
                "context_id": _hash_id(context_key),
                "slice_id": slice_id,
                "graph_cluster_id": graph_cluster,
                "vector_cluster_id": vector_cluster,
                "graph_score": graph_score,
                "vector_score": vector_score,
                "coverage_score": coverage_score,
                "pagerank_score": pagerank_score,
                "combined_score": combined_score,
                "rationale": f"{rationale} Name: {context_label}." if context_label else rationale,
                "source_ref": "graph_metadata",
            }
        )
    return rows


def _build_rule_cluster_map(
    logic_edges: list[dict],
    code_graph_nodes: list[dict],
    graph_metadata: list[dict],
) -> dict[str, int]:
    symbol_to_node: dict[str, str] = {}
    for node in code_graph_nodes:
        symbol_id = node.get("symbol_id")
        node_id = node.get("node_id")
        if symbol_id and node_id:
            symbol_to_node[symbol_id] = node_id
    node_to_cluster: dict[str, int] = {}
    for row in graph_metadata:
        node_id = row.get("node_id")
        community_id = row.get("community_id")
        if node_id and isinstance(community_id, int) and community_id > 0:
            node_to_cluster[node_id] = community_id
    counts: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for edge in logic_edges:
        rule_id = edge.get("rule_id")
        symbol_id = edge.get("symbol_id")
        if not rule_id or not symbol_id:
            continue
        node_id = symbol_to_node.get(symbol_id)
        cluster_id = node_to_cluster.get(node_id) if node_id else None
        if cluster_id:
            counts[rule_id][cluster_id] += 1
    result: dict[str, int] = {}
    for rule_id, cluster_counts in counts.items():
        result[rule_id] = max(cluster_counts.items(), key=lambda item: item[1])[0]
    return result


def _slice_summary_map(slice_context: list[dict]) -> dict[str, str]:
    summaries: dict[str, str] = {}
    for row in slice_context:
        slice_id = row.get("slice_id")
        summary = row.get("summary", "")
        risks = row.get("risks", "")
        assumptions = row.get("assumptions", "")
        if not slice_id:
            continue
        parts = [summary]
        if risks:
            parts.append(f"Risks: {risks}")
        if assumptions:
            parts.append(f"Assumptions: {assumptions}")
        summaries[slice_id] = " ".join(part for part in parts if part)
    return summaries


def _entry_graph_state_map(
    client,
    output_root: Path,
    run_id: str,
    artifact_version: int,
    config: DomainArchitectConfig,
) -> dict[str, dict]:
    if not config.entry_graph_incremental:
        return {}
    rows = _fetch_rows_with_fallback(
        client,
        output_root,
        run_id,
        artifact_version,
        "step_6",
        "entry_graph_state",
    )
    state_map: dict[str, dict] = {}
    for row in rows:
        entry_key = row.get("entry_key")
        if entry_key:
            state_map[str(entry_key)] = row
    return state_map


def run(config: DomainArchitectConfig) -> None:
    created_at = _created_at()
    _ = _resolve_workers(config)
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    config = config.model_copy(update={"run_id": run_id})
    output_root = config.output_root / config.run_id / "step_6"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("domain_architect", config.run_id, config.artifact_version)
    client = get_mcp_client()

    if config.domain_insights_only:
        group_size = config.llm_domain_insights_group_size or 1
        if config.llm_domain_insights_max_groups is not None:
            rule_limit = max(1, config.llm_domain_insights_max_groups * group_size)
        else:
            rule_limit = 1000
        logic_sql = f"""
            select *
            from logic_rules
            where run_id = '{config.run_id}' and artifact_version = {config.artifact_version}
            order by rule_id
            limit {rule_limit}
        """
        logic_rules = client.query(logic_sql)
        slice_ids = sorted({row.get("slice_id") for row in logic_rules if row.get("slice_id")})
        if slice_ids:
            slice_list = ", ".join(f"'{sid}'" for sid in slice_ids)
            slice_sql = f"""
                select *
                from slice_context
                where run_id = '{config.run_id}' and artifact_version = {config.artifact_version}
                  and slice_id in ({slice_list})
            """
            slice_context = client.query(slice_sql)
        else:
            slice_context = []
        rule_slice_map = {row.get("rule_id", ""): row.get("slice_id", "") for row in logic_rules}
        slice_summaries = _slice_summary_map(slice_context)
        insight_rows = _build_domain_insights_llm(
            logic_rules,
            rule_slice_map,
            slice_summaries,
            config,
        )
        write_parquet(
            output_root,
            "domain_insights",
            _with_metadata(insight_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
        state = finalize_state(
            state,
            processed_count=len(insight_rows),
            outputs={"domain_insights": len(insight_rows)},
            notes={"domain_insights_only": True, "output_root": str(output_root)},
        )
        write_state("domain_architect", state)
        return

    logic_rules = _fetch_rows(client, "logic_rules", config.run_id, config.artifact_version)
    logic_edges = _fetch_rows(client, "logic_edges", config.run_id, config.artifact_version)
    code_graph_nodes = _fetch_rows(client, "code_graph_nodes", config.run_id, config.artifact_version)
    graph_metadata = _fetch_rows(client, "graph_metadata", config.run_id, config.artifact_version)
    slice_context = _fetch_rows(client, "slice_context", config.run_id, config.artifact_version)
    slice_manifest = _fetch_rows(client, "slice_manifest", config.run_id, config.artifact_version)
    rule_cluster_map = _build_rule_cluster_map(logic_edges, code_graph_nodes, graph_metadata)
    rules_by_slice, rule_slice_map = _group_rules_by_slice(logic_rules, rule_cluster_map)
    context_clusters = _context_cluster_map(slice_context, config.context_cluster_bits)
    slice_nodes = _slice_node_ids(slice_manifest, code_graph_nodes)
    code_vectors: list[dict] = []
    vector_clusters: dict[str, int] = {}
    if not config.domain_insights_only:
        code_vectors = _fetch_rows_with_fallback(
            client,
            config.output_root,
            config.run_id,
            config.artifact_version,
            "step_5",
            "code_vectors",
        )
        vector_clusters = _vector_cluster_map(
            slice_nodes,
            code_vectors,
            config.vector_cluster_bits,
            config.max_nodes_per_slice,
        )
    # Handle both slice_XXX and entry_XXX formats
    graph_clusters = {}
    for idx, slice_id in enumerate(rules_by_slice):
        if slice_id.startswith("slice_"):
            try:
                graph_clusters[slice_id] = int(slice_id.replace("slice_", ""))
            except ValueError:
                graph_clusters[slice_id] = idx
        else:
            graph_clusters[slice_id] = idx
    slice_summaries = _slice_summary_map(slice_context)
    insight_rows = _build_domain_insights_llm(
        logic_rules,
        rule_slice_map,
        slice_summaries,
        config,
    )
    code_graph_edges = _fetch_rows(client, "code_graph_edges", config.run_id, config.artifact_version)
    entry_exit_map = _fetch_rows(client, "entry_exit_map", config.run_id, config.artifact_version)
    symbols = _fetch_rows(client, "symbols", config.run_id, config.artifact_version)
    node_by_id, _, _ = _node_maps(code_graph_nodes)
    node_type_by_id = {
        node_id: node.get("node_type", "symbol") for node_id, node in node_by_id.items()
    }
    pagerank_by_node = _pagerank_by_node(
        code_graph_nodes, code_graph_edges, config.node_type_weights
    )
    recursive_nodes = _recursive_nodes(code_graph_edges)
    slice_pagerank = _slice_pagerank_scores(slice_nodes, pagerank_by_node)
    adjacency = _graph_adjacency(code_graph_edges)
    in_degree: dict[str, int] = defaultdict(int)
    out_degree: dict[str, int] = defaultdict(int)
    for from_id, to_nodes in adjacency.items():
        out_degree[from_id] += len(to_nodes)
        for to_id in to_nodes:
            in_degree[to_id] += 1
    pagerank_entries = _pagerank_entry_by_slice(
        slice_nodes,
        pagerank_by_node,
        in_degree,
        out_degree,
        config.entry_filter,
        recursive_nodes,
        config.exclude_recursive_entries,
        node_type_by_id,
        config.node_type_weights,
    )
    symbols_entry_map = _build_symbol_entry_map(
        symbols, slice_manifest, pagerank_entries, code_graph_nodes, recursive_nodes
    )
    endpoints = _build_endpoints_with_entries(slice_manifest, code_graph_nodes, pagerank_entries)
    entry_graph_candidates, entry_graph_summary = _entry_graph_candidates(
        code_graph_nodes,
        code_graph_edges,
        config,
    )
    existing_entry_state = _entry_graph_state_map(
        client,
        config.output_root,
        config.run_id,
        config.artifact_version,
        config,
    )
    entry_graph_rows: list[dict] = []
    entry_state_rows: list[dict] = []
    processed_keys: list[str] = []
    skipped_keys: list[str] = []
    pending_keys: list[str] = []
    excluded_keys: list[str] = []
    selected_keys = {item["entry_key"] for item in entry_graph_candidates}
    for item in entry_graph_summary.get("eligible", []):
        entry_key = str(item["entry_key"])
        if entry_key not in selected_keys:
            pending_keys.append(entry_key)
            entry_state_rows.append(
                {
                    "entry_key": entry_key,
                    "entry_type": item["entry_type"],
                    "status": "pending",
                    "reason": "top_k_limit",
                    "metrics": json.dumps(item.get("metrics", {}), ensure_ascii=True),
                    "source_ref": entry_key,
                }
            )
    for item in entry_graph_summary.get("excluded", []):
        entry_key = str(item["entry_key"])
        excluded_keys.append(entry_key)
        entry_state_rows.append(
            {
                "entry_key": entry_key,
                "entry_type": item["entry_type"],
                "status": "excluded",
                "reason": item.get("reason", "excluded"),
                "metrics": json.dumps(item.get("metrics", {}), ensure_ascii=True),
                "source_ref": entry_key,
            }
        )
    for item in entry_graph_candidates:
        entry_key = str(item["entry_key"])
        entry_type = str(item["entry_type"])
        entry_nodes = set(item.get("entry_nodes", []))
        reachable = item.get("reachable", set())
        metrics = item.get("metrics", {})
        state = existing_entry_state.get(entry_key, {})
        if config.entry_graph_incremental and state.get("status") == "processed":
            skipped_keys.append(entry_key)
            entry_state_rows.append(
                {
                    "entry_key": entry_key,
                    "entry_type": entry_type,
                    "status": "skipped",
                    "reason": "already_processed",
                    "metrics": json.dumps(metrics, ensure_ascii=True),
                    "source_ref": entry_key,
                }
            )
            continue
        edges = _entry_graph_edges(
            entry_graph_summary.get("edges", []),
            reachable,
            entry_nodes,
            entry_type,
        )
        entry_graph_rows.append(
            {
                "entry_key": entry_key,
                "entry_type": entry_type,
                "entry_nodes": json.dumps(sorted(entry_nodes), ensure_ascii=True),
                "reachable_nodes": json.dumps(sorted(reachable), ensure_ascii=True),
                "reachable_edges": json.dumps(edges, ensure_ascii=True),
                "metrics": json.dumps(metrics, ensure_ascii=True),
                "capped_depth": metrics.get("capped_depth", 0.0),
                "normalized_depth": metrics.get("normalized", 0.0),
                "log_scaled_depth": metrics.get("log_scaled", 0.0),
                "depth_breadth": metrics.get("depth_breadth", 0.0),
                "reachable_nodes_count": metrics.get("reachable_nodes", 0.0),
                "edge_count": len(edges),
                "source_ref": entry_key,
            }
        )
        processed_keys.append(entry_key)
        entry_state_rows.append(
            {
                "entry_key": entry_key,
                "entry_type": entry_type,
                "status": "processed",
                "reason": "processed",
                "metrics": json.dumps(metrics, ensure_ascii=True),
                "source_ref": entry_key,
            }
        )
    summary_row = {
        "total_candidates": len(entry_graph_summary.get("eligible", [])),
        "processed_count": len(processed_keys),
        "skipped_count": len(skipped_keys),
        "pending_count": len(pending_keys),
        "excluded_count": len(excluded_keys),
        "processed_keys": json.dumps(processed_keys[:ENTRY_GRAPH_SUMMARY_LIMIT], ensure_ascii=True),
        "pending_keys": json.dumps(pending_keys[:ENTRY_GRAPH_SUMMARY_LIMIT], ensure_ascii=True),
        "skipped_keys": json.dumps(skipped_keys[:ENTRY_GRAPH_SUMMARY_LIMIT], ensure_ascii=True),
        "excluded_keys": json.dumps(excluded_keys[:ENTRY_GRAPH_SUMMARY_LIMIT], ensure_ascii=True),
        "source_ref": "entry_graph_processing_summary",
    }
    logger.info(
        "entry_graphs_summary total=%d processed=%d skipped=%d pending=%d excluded=%d",
        summary_row["total_candidates"],
        summary_row["processed_count"],
        summary_row["skipped_count"],
        summary_row["pending_count"],
        summary_row["excluded_count"],
    )
    selected_keys = set(processed_keys)
    if selected_keys:
        endpoints = [ep for ep in endpoints if ep.get("entry_node_id") in selected_keys]
    endpoint_flows, coverage_by_endpoint = _build_endpoint_flows(
        endpoints,
        code_graph_nodes,
        code_graph_edges,
        entry_exit_map,
        pagerank_by_node,
        recursive_nodes,
        config,
    )
    total_nodes = len(code_graph_nodes)
    endpoint_coverage = _build_endpoint_coverage(coverage_by_endpoint, total_nodes)
    context_names, context_groups = _context_groups_llm(
        slice_context,
        slice_manifest,
        endpoints,
        endpoint_flows,
        graph_clusters,
        vector_clusters,
        context_clusters,
        slice_pagerank,
        config,
    )
    pagerank_entry_insights = _build_pagerank_entry_insights(
        endpoints, endpoint_flows, pagerank_by_node, config
    )

    entity_rows: list[dict] = []
    vo_rows: list[dict] = []
    aggregate_rows: list[dict] = []
    context_rows: list[dict] = []

    slice_items: list[tuple[str, list[dict], int | None, str, int]] = []
    for slice_id, rules in rules_by_slice.items():
        cluster_id = vector_clusters.get(slice_id, context_clusters.get(slice_id))
        context_key = str(cluster_id) if cluster_id is not None else slice_id
        context_name = context_names.get(context_key, f"{slice_id}_context")
        slice_items.append((slice_id, rules, cluster_id, context_name, config.max_name_chars))

    workers = resolve_workers(config.workers)
    if workers > 1 and slice_items:
        results = process_map(_build_domain_rows_for_slice, slice_items, workers)
        for entities, value_objects, aggregates, context in results:
            entity_rows.extend(entities)
            vo_rows.extend(value_objects)
            aggregate_rows.extend(aggregates)
            context_rows.append(context)
    else:
        for slice_id, rules, cluster_id, context_name, max_name_chars in slice_items:
            entities = _derive_entities(slice_id, rules, max_name_chars)
            entity_rows.extend(entities)
            vo_rows.extend(_derive_value_objects(slice_id, rules, max_name_chars))
            aggregate_rows.extend(_derive_aggregates(slice_id, entities))
            context = _derive_context_map(slice_id, cluster_id)
            context["name"] = context_name
            context_rows.append(context)

    if entity_rows:
        write_parquet(
            output_root,
            "domain_entities",
            _with_metadata(entity_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if vo_rows:
        write_parquet(
            output_root,
            "value_objects",
            _with_metadata(vo_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if aggregate_rows:
        write_parquet(
            output_root,
            "aggregates",
            _with_metadata(aggregate_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if context_rows:
        write_parquet(
            output_root,
            "context_map",
            _with_metadata(context_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if insight_rows:
        write_parquet(
            output_root,
            "domain_insights",
            _with_metadata(insight_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if endpoints:
        write_parquet(
            output_root,
            "endpoints",
            _with_metadata(endpoints, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if endpoint_flows:
        write_parquet(
            output_root,
            "endpoint_flows",
            _with_metadata(endpoint_flows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if endpoint_coverage:
        write_parquet(
            output_root,
            "endpoint_coverage",
            _with_metadata(endpoint_coverage, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    if entry_graph_rows:
        write_parquet(
            output_root,
            "entry_graphs",
            _with_metadata(entry_graph_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )
    state = finalize_state(
        state,
        processed_count=len(entity_rows),
        outputs={
            "domain_entities": len(entity_rows),
            "value_objects": len(vo_rows),
            "aggregates": len(aggregate_rows),
            "context_map": len(context_rows),
            "domain_insights": len(insight_rows),
            "endpoints": len(endpoints),
            "endpoint_flows": len(endpoint_flows),
            "endpoint_coverage": len(endpoint_coverage),
            "entry_graphs": len(entry_graph_rows),
        },
        notes={"output_root": str(output_root)},
    )
    write_state("domain_architect", state)
    write_parquet(
        output_root,
        "entry_graph_state",
        _with_metadata(entry_state_rows, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "entry_graph_processing_summary",
        _with_metadata([summary_row], config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "dead_code",
        _with_metadata(_build_dead_code(code_graph_nodes, graph_metadata, symbols), config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "context_reasoning",
        _with_metadata(
            _build_context_reasoning(
                rule_slice_map,
                vector_clusters,
                graph_clusters,
                slice_manifest,
                slice_pagerank,
                context_names,
            ),
            config,
            created_at,
        ),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "context_groups",
        _with_metadata(context_groups, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "symbols_entry_map",
        _with_metadata(symbols_entry_map, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )
    write_parquet(
        output_root,
        "pagerank_entry_insights",
        _with_metadata(pagerank_entry_insights, config, created_at),
        partition_cols=["run_id", "artifact_version"],
    )


def main() -> None:
    if not logging.getLogger().handlers:
        setup_logging("domain_architect")
    parser = argparse.ArgumentParser(description="Stage 5 Domain Architect pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    logger.info(
        "domain_architect_start run_id=%s artifact_version=%s output_root=%s",
        config.run_id,
        config.artifact_version,
        config.output_root,
    )
    run(config)
    logger.info("domain_architect_done run_id=%s artifact_version=%s", config.run_id, config.artifact_version)


if __name__ == "__main__":
    main()
