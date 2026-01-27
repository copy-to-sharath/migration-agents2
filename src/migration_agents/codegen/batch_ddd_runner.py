"""Batch DDD Analysis Runner for Large-Scale Migrations.

This module provides batch processing for Copilot-driven DDD analysis,
with support for rate limiting, resumption, and progress tracking.

WORKFLOW:
  Phase 1: Batch Slice Analysis  → Analyze slices in batches with rate limiting
  Phase 2: Build Domain Model    → Synthesize unified domain model from all analyses
  Phase 3: SME Review Gate       → Validate and get SME approval
  Phase 4: Code Generation       → Generate Clean Architecture code

The workflow ensures:
- LLM rate limits are respected with configurable delays
- Progress is saved for resumption after interruption
- Large codebases (1000+ slices) are handled efficiently
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

LOGGER = logging.getLogger("migration_agents.codegen.batch_ddd_runner")

# Default batch configuration
DEFAULT_BATCH_SIZE = 50  # Slices per batch
DEFAULT_DELAY_BETWEEN_BATCHES = 5.0  # Seconds between batches
DEFAULT_DELAY_BETWEEN_SLICES = 0.5  # Seconds between individual slice analyses
MAX_RETRIES_PER_BATCH = 3
RETRY_DELAY_BASE = 10.0  # Base delay for exponential backoff


@dataclass
class DDDBatchProgress:
    """Progress tracking for batch DDD analysis."""
    total_slices: int = 0
    total_batches: int = 0
    completed_batches: int = 0
    analyzed_slices: int = 0
    failed_slices: list[str] = field(default_factory=list)
    skipped_slices: list[str] = field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    current_batch: int = 0
    last_saved_batch: int = 0
    
    # Aggregate tracking
    aggregates_found: int = 0
    events_found: int = 0
    value_objects_found: int = 0
    bounded_contexts: list[str] = field(default_factory=list)
    
    @property
    def elapsed_seconds(self) -> float:
        if not self.start_time:
            return 0.0
        end = self.end_time or datetime.now(timezone.utc)
        return (end - self.start_time).total_seconds()
    
    @property
    def slices_per_minute(self) -> float:
        if self.elapsed_seconds == 0:
            return 0.0
        return (self.analyzed_slices / self.elapsed_seconds) * 60
    
    @property
    def estimated_remaining_minutes(self) -> float:
        if self.slices_per_minute == 0:
            return 0.0
        remaining = self.total_slices - self.analyzed_slices
        return remaining / self.slices_per_minute
    
    @property
    def completion_percentage(self) -> float:
        if self.total_slices == 0:
            return 0.0
        return (self.analyzed_slices / self.total_slices) * 100
    
    def to_dict(self) -> dict:
        return {
            "total_slices": self.total_slices,
            "total_batches": self.total_batches,
            "completed_batches": self.completed_batches,
            "analyzed_slices": self.analyzed_slices,
            "failed_slices_count": len(self.failed_slices),
            "skipped_slices_count": len(self.skipped_slices),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "elapsed_seconds": self.elapsed_seconds,
            "slices_per_minute": round(self.slices_per_minute, 2),
            "estimated_remaining_minutes": round(self.estimated_remaining_minutes, 2),
            "completion_percentage": round(self.completion_percentage, 1),
            "current_batch": self.current_batch,
            "aggregates_found": self.aggregates_found,
            "events_found": self.events_found,
            "value_objects_found": self.value_objects_found,
            "bounded_contexts": self.bounded_contexts,
        }
    
    def save_checkpoint(self, checkpoint_path: Path) -> None:
        """Save progress checkpoint for resumption."""
        checkpoint = {
            **self.to_dict(),
            "failed_slices": self.failed_slices,
            "skipped_slices": self.skipped_slices,
            "checkpoint_time": datetime.now(timezone.utc).isoformat(),
        }
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_path.write_text(json.dumps(checkpoint, indent=2))
        self.last_saved_batch = self.current_batch
        LOGGER.info("Saved checkpoint at batch %d to %s", self.current_batch, checkpoint_path)
    
    @classmethod
    def load_checkpoint(cls, checkpoint_path: Path) -> Optional["DDDBatchProgress"]:
        """Load progress from checkpoint."""
        if not checkpoint_path.exists():
            return None
        try:
            data = json.loads(checkpoint_path.read_text())
            progress = cls(
                total_slices=data.get("total_slices", 0),
                total_batches=data.get("total_batches", 0),
                completed_batches=data.get("completed_batches", 0),
                analyzed_slices=data.get("analyzed_slices", 0),
                failed_slices=data.get("failed_slices", []),
                skipped_slices=data.get("skipped_slices", []),
                current_batch=data.get("current_batch", 0),
                aggregates_found=data.get("aggregates_found", 0),
                events_found=data.get("events_found", 0),
                value_objects_found=data.get("value_objects_found", 0),
                bounded_contexts=data.get("bounded_contexts", []),
            )
            if data.get("start_time"):
                progress.start_time = datetime.fromisoformat(data["start_time"])
            return progress
        except Exception as e:
            LOGGER.warning("Failed to load checkpoint: %s", e)
            return None


@dataclass
class BatchDDDConfig:
    """Configuration for batch DDD analysis."""
    solution_name: str
    parquet_root: Path
    output_root: Path
    run_id: str
    artifact_version: int = 1
    
    # Batch settings
    batch_size: int = DEFAULT_BATCH_SIZE
    delay_between_batches: float = DEFAULT_DELAY_BETWEEN_BATCHES
    delay_between_slices: float = DEFAULT_DELAY_BETWEEN_SLICES
    max_retries: int = MAX_RETRIES_PER_BATCH
    
    # Slice filtering
    min_depth: int = 0
    max_depth: int = 10
    slice_filter: Optional[str] = None
    
    # Resumption
    start_batch: int = 0
    max_batches: Optional[int] = None
    resume_from_checkpoint: bool = True
    
    # LLM settings
    llm_provider: str = "copilot"  # "copilot", "github", "openai", "gemini", "azure"
    llm_model: str = "gpt-4o-mini"  # Cost-effective for batch processing
    llm_base_url: Optional[str] = None  # Custom endpoint (e.g., Azure)
    llm_timeout_sec: int = 60
    llm_temperature: float = 0.2
    llm_max_tokens: int = 2000
    
    @property
    def checkpoint_path(self) -> Path:
        return self.output_root / self.solution_name / "ddd" / ".ddd_batch_checkpoint.json"
    
    @property
    def analyses_dir(self) -> Path:
        return self.output_root / self.solution_name / "ddd" / "slice_analyses"


@dataclass
class SliceAnalysis:
    """DDD analysis result for a single slice."""
    slice_id: str
    aggregate_name: str
    description: str = ""
    properties: list[dict] = field(default_factory=list)
    behaviors: list[str] = field(default_factory=list)
    domain_events: list[str] = field(default_factory=list)
    value_objects: list[dict] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)
    bounded_context_hint: str = ""
    source_summary: str = ""
    analyzed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> dict:
        return {
            "slice_id": self.slice_id,
            "aggregate_name": self.aggregate_name,
            "description": self.description,
            "properties": self.properties,
            "behaviors": self.behaviors,
            "domain_events": self.domain_events,
            "value_objects": self.value_objects,
            "invariants": self.invariants,
            "bounded_context_hint": self.bounded_context_hint,
            "source_summary": self.source_summary,
            "analyzed_at": self.analyzed_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SliceAnalysis":
        return cls(
            slice_id=data.get("slice_id", ""),
            aggregate_name=data.get("aggregate_name", ""),
            description=data.get("description", ""),
            properties=data.get("properties", []),
            behaviors=data.get("behaviors", []),
            domain_events=data.get("domain_events", []),
            value_objects=data.get("value_objects", []),
            invariants=data.get("invariants", []),
            bounded_context_hint=data.get("bounded_context_hint", ""),
            source_summary=data.get("source_summary", ""),
            analyzed_at=data.get("analyzed_at", ""),
        )


def get_all_slices_from_parquet(
    parquet_root: Path,
    run_id: str,
    min_depth: int = 0,
    max_depth: int = 10,
) -> list[dict]:
    """Get all slices directly from parquet files.
    
    This bypasses DuckDB views and reads directly from the parquet files
    to avoid view registration issues.
    """
    import duckdb
    
    # Direct parquet query for entry graphs with join to symbols
    # Use glob pattern string directly for DuckDB
    entry_graph_glob = str(parquet_root / run_id / "step_2" / "entry_graphs") + "/**/*.parquet"
    symbols_glob = str(parquet_root / run_id / "step_2" / "symbols") + "/**/*.parquet"
    
    # Join entry_graphs with symbols to get file_path and name
    sql = f"""
        SELECT 
            eg.entry_key as slice_id,
            eg.capped_depth as depth,
            s.file_path as root_file,
            s.name as root_name,
            s.kind as root_kind
        FROM read_parquet('{entry_graph_glob}') eg
        LEFT JOIN read_parquet('{symbols_glob}') s 
            ON eg.source_ref = s.symbol_id
        WHERE eg.capped_depth >= {min_depth}
          AND eg.capped_depth <= {max_depth}
          AND eg.capped_depth >= 1
        ORDER BY eg.capped_depth DESC, eg.entry_key
    """
    
    try:
        from migration_agents.mcp.duckdb_catalog import get_run_connection
        conn, _ = get_run_connection(parquet_root, run_id)
        result = conn.execute(sql).fetchdf()
        conn.close()
        return result.to_dict(orient="records")
    except Exception as e:
        LOGGER.error("Failed to query slices from parquet: %s", e)
        return []


def get_slice_context_from_parquet(
    parquet_root: Path,
    run_id: str,
    slice_id: str,
) -> dict:
    """Get detailed context for a slice from parquet files."""
    from migration_agents.mcp.duckdb_catalog import get_run_connection
    
    conn, _ = get_run_connection(parquet_root, run_id)
    context = {"slice_id": slice_id, "symbols": [], "calls": [], "source_refs": []}
    
    # Get slice context - use glob pattern string
    slice_context_glob = str(parquet_root / run_id / "step_3" / "slice_context") + "/**/*.parquet"
    try:
        sql = f"""
            SELECT * FROM read_parquet('{slice_context_glob}')
            WHERE slice_id = 'entry_{slice_id[:8]}'
            LIMIT 1
        """
        result = conn.execute(sql).fetchdf()
        if len(result) > 0:
            row = result.iloc[0].to_dict()
            context["summary"] = row.get("summary", "")
            context["risks"] = row.get("risks", "")
            context["source_ref"] = row.get("source_ref", "")
    except Exception as e:
        LOGGER.debug("No slice context found: %s", e)
    
    # Get entry graph info - use glob pattern string
    entry_graph_glob = str(parquet_root / run_id / "step_2" / "entry_graphs") + "/**/*.parquet"
    try:
        sql = f"""
            SELECT root_file, root_name, capped_depth
            FROM read_parquet('{entry_graph_glob}')
            WHERE entry_key = '{slice_id}'
            LIMIT 1
        """
        result = conn.execute(sql).fetchdf()
        if len(result) > 0:
            row = result.iloc[0].to_dict()
            context["root_file"] = row.get("root_file", "")
            context["root_name"] = row.get("root_name", "")
            context["depth"] = row.get("capped_depth", 0)
    except Exception as e:
        LOGGER.debug("No entry graph found: %s", e)
    
    # Get symbols in the entry graph - use glob pattern string
    symbols_glob = str(parquet_root / run_id / "step_2" / "symbols") + "/**/*.parquet"
    root_file = context.get("root_file", "")
    if root_file:
        try:
            sql = f"""
                SELECT name, kind, file_path, line_start
                FROM read_parquet('{symbols_glob}')
                WHERE file_path = '{root_file}'
                LIMIT 20
            """
            result = conn.execute(sql).fetchdf()
            context["symbols"] = result.to_dict(orient="records")
        except Exception:
            pass
    
    conn.close()
    return context


def build_ddd_analysis_prompt_for_slice(
    slice_id: str,
    context: dict,
) -> str:
    """Build a structured prompt for Copilot to analyze a slice for DDD concepts."""
    symbols_text = ""
    if context.get("symbols"):
        symbols_text = "\n".join([
            f"  - {s.get('name')} ({s.get('kind')}) at line {s.get('line_start', '?')}"
            for s in context["symbols"][:15]
        ])
    
    return f"""
## DDD SLICE ANALYSIS

Analyze this slice and extract Domain-Driven Design concepts.

### SLICE INFORMATION
- **Slice ID**: {slice_id}
- **Root File**: {context.get('root_file', 'Unknown')}
- **Root Name**: {context.get('root_name', 'Unknown')}
- **Depth**: {context.get('depth', 0)}

### SUMMARY
{context.get('summary', 'No summary available')}

### SOURCE REFERENCES
{context.get('source_ref', 'No source references')}

### SYMBOLS IN SCOPE
{symbols_text or 'No symbols found'}

### RISKS/CONSIDERATIONS
{context.get('risks', 'None identified')}

---

## ANALYSIS REQUIRED

Extract the following DDD concepts:

1. **AGGREGATE NAME**: The primary domain aggregate this slice represents
2. **DESCRIPTION**: What this aggregate/feature does
3. **PROPERTIES**: Key properties with types (e.g., [{{"name": "Id", "type": "Guid"}}])
4. **BEHAVIORS**: Domain operations/methods (e.g., ["PlaceOrder", "CancelOrder"])
5. **DOMAIN EVENTS**: Events raised by this aggregate (e.g., ["OrderPlaced", "OrderCancelled"])
6. **VALUE OBJECTS**: Embedded value objects (e.g., [{{"name": "Address", "properties": [...]}}])
7. **INVARIANTS**: Business rules that must always be true
8. **BOUNDED CONTEXT HINT**: Suggested bounded context (e.g., "Orders", "Catalog", "Customers")

Respond with a JSON object:
```json
{{
  "aggregate_name": "OrderAggregate",
  "description": "Manages customer orders and their lifecycle",
  "properties": [{{"name": "CustomerId", "type": "Guid"}}, {{"name": "TotalAmount", "type": "decimal"}}],
  "behaviors": ["PlaceOrder", "AddItem", "RemoveItem", "CalculateTotal"],
  "domain_events": ["OrderPlaced", "ItemAdded", "OrderCompleted"],
  "value_objects": [{{"name": "Money", "properties": [{{"name": "Amount", "type": "decimal"}}, {{"name": "Currency", "type": "string"}}]}}],
  "invariants": ["Order must have at least one item", "Total must be positive"],
  "bounded_context_hint": "Orders"
}}
```
"""


def _call_llm_openai(
    config: BatchDDDConfig,
    prompt: str,
) -> str:
    """Call OpenAI API with rate limiting and retry logic."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")
    
    base_url = config.llm_base_url or "https://api.openai.com/v1/chat/completions"
    
    payload = json.dumps({
        "model": config.llm_model,
        "messages": [
            {"role": "system", "content": "You are a Domain-Driven Design expert. Analyze code slices and extract DDD concepts. Always respond with valid JSON only, no markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        "temperature": config.llm_temperature,
        "max_tokens": config.llm_max_tokens,
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
        raise ValueError("OpenAI response missing choices")
    
    return str(choices[0].get("message", {}).get("content", "")).strip()


def _call_llm_gemini(
    config: BatchDDDConfig,
    prompt: str,
) -> str:
    """Call Gemini API with rate limiting and retry logic."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is required")
    
    model = config.llm_model or "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": config.llm_temperature,
            "maxOutputTokens": config.llm_max_tokens,
        },
    }).encode("utf-8")
    
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


def _call_llm_azure(
    config: BatchDDDConfig,
    prompt: str,
) -> str:
    """Call Azure OpenAI API with rate limiting and retry logic."""
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("AZURE_OPENAI_API_KEY environment variable is required")
    
    if not config.llm_base_url:
        raise RuntimeError("llm_base_url is required for Azure OpenAI")
    
    # Azure uses api-version query param
    base_url = config.llm_base_url
    if "api-version" not in base_url:
        base_url += "?api-version=2024-02-15-preview"
    
    payload = json.dumps({
        "messages": [
            {"role": "system", "content": "You are a Domain-Driven Design expert. Analyze code slices and extract DDD concepts. Always respond with valid JSON only, no markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        "temperature": config.llm_temperature,
        "max_tokens": config.llm_max_tokens,
    }).encode("utf-8")
    
    request = urllib.request.Request(
        base_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
        },
        method="POST",
    )
    
    with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
        data = json.load(response)
    
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("Azure OpenAI response missing choices")
    
    return str(choices[0].get("message", {}).get("content", "")).strip()


def _call_llm_github(
    config: BatchDDDConfig,
    prompt: str,
) -> str:
    """Call GitHub Models API (Copilot LLM) with rate limiting and retry logic.
    
    Uses the GitHub Models inference endpoint which is powered by the same
    models as GitHub Copilot. Requires a GitHub token with appropriate permissions.
    
    Environment variables:
        GITHUB_TOKEN: GitHub personal access token or Copilot token
    """
    api_key = os.environ.get("GITHUB_TOKEN")
    if not api_key:
        raise RuntimeError("GITHUB_TOKEN environment variable is required for GitHub/Copilot LLM")
    
    # GitHub Models API endpoint
    base_url = config.llm_base_url or "https://models.inference.ai.azure.com/chat/completions"
    model = config.llm_model or "gpt-4o-mini"
    
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a Domain-Driven Design expert. Analyze code slices and extract DDD concepts. Always respond with valid JSON only, no markdown formatting."},
            {"role": "user", "content": prompt}
        ],
        "temperature": config.llm_temperature,
        "max_tokens": config.llm_max_tokens,
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
        raise ValueError("GitHub Models response missing choices")
    
    return str(choices[0].get("message", {}).get("content", "")).strip()


def call_llm_with_retry(
    config: BatchDDDConfig,
    prompt: str,
    max_retries: int = 3,
) -> str:
    """Call LLM with exponential backoff retry on rate limit errors."""
    provider = config.llm_provider.lower()
    
    for attempt in range(max_retries):
        try:
            if provider == "openai":
                return _call_llm_openai(config, prompt)
            elif provider == "gemini":
                return _call_llm_gemini(config, prompt)
            elif provider == "azure":
                return _call_llm_azure(config, prompt)
            elif provider in ("github", "copilot"):
                return _call_llm_github(config, prompt)
            else:
                raise ValueError(f"Unknown LLM provider: {provider}")
                
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limit
                retry_after = int(e.headers.get("Retry-After", RETRY_DELAY_BASE * (2 ** attempt)))
                LOGGER.warning("Rate limited. Waiting %d seconds (attempt %d/%d)", 
                              retry_after, attempt + 1, max_retries)
                time.sleep(retry_after)
            elif e.code >= 500:  # Server error
                delay = RETRY_DELAY_BASE * (2 ** attempt)
                LOGGER.warning("Server error %d. Waiting %.1f seconds (attempt %d/%d)", 
                              e.code, delay, attempt + 1, max_retries)
                time.sleep(delay)
            else:
                raise
        except urllib.error.URLError as e:
            delay = RETRY_DELAY_BASE * (2 ** attempt)
            LOGGER.warning("Network error: %s. Waiting %.1f seconds (attempt %d/%d)", 
                          e.reason, delay, attempt + 1, max_retries)
            time.sleep(delay)
    
    raise RuntimeError(f"Failed after {max_retries} retries")


def _clean_llm_json(text: str) -> str:
    """Clean LLM response to extract JSON."""
    # Remove ANSI codes
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    
    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE)
    
    # Find JSON object
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]
    
    return text.strip()


def analyze_slice_with_llm(
    config: BatchDDDConfig,
    slice_item: dict,
) -> dict:
    """Analyze a single slice using LLM."""
    prompt = slice_item.get("prompt", "")
    slice_id = slice_item.get("slice_id", "")
    
    if not prompt:
        raise ValueError("No prompt provided for slice analysis")
    
    response = call_llm_with_retry(config, prompt, config.max_retries)
    
    # Parse JSON response
    cleaned = _clean_llm_json(response)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        LOGGER.warning("Failed to parse LLM JSON response for slice %s: %s", slice_id[:16], e)
        LOGGER.debug("Raw response: %s", response[:500])
        # Return minimal valid response
        result = {
            "aggregate_name": f"Aggregate_{slice_id[:8]}",
            "description": "Failed to parse LLM response",
            "properties": [],
            "behaviors": [],
            "domain_events": [],
            "value_objects": [],
            "invariants": [],
            "bounded_context_hint": "Default",
            "parse_error": str(e),
        }
    
    return result


def save_slice_analysis(
    config: BatchDDDConfig,
    analysis: SliceAnalysis,
) -> None:
    """Save a slice analysis to disk."""
    analyses_dir = config.analyses_dir
    analyses_dir.mkdir(parents=True, exist_ok=True)
    
    # Use first 16 chars of slice_id for filename
    filename = f"{analysis.slice_id[:16]}.json"
    filepath = analyses_dir / filename
    filepath.write_text(json.dumps(analysis.to_dict(), indent=2))


def load_existing_analyses(config: BatchDDDConfig) -> dict[str, SliceAnalysis]:
    """Load all existing slice analyses from disk."""
    analyses_dir = config.analyses_dir
    if not analyses_dir.exists():
        return {}
    
    analyses = {}
    for filepath in analyses_dir.glob("*.json"):
        try:
            data = json.loads(filepath.read_text())
            analysis = SliceAnalysis.from_dict(data)
            analyses[analysis.slice_id] = analysis
        except Exception as e:
            LOGGER.warning("Failed to load analysis from %s: %s", filepath, e)
    
    return analyses


def get_batch_ddd_status(config: BatchDDDConfig) -> dict:
    """Get the current status of batch DDD analysis."""
    # Load checkpoint if exists
    checkpoint = DDDBatchProgress.load_checkpoint(config.checkpoint_path)
    
    # Count existing analyses
    existing_analyses = load_existing_analyses(config)
    
    # Get total slices
    all_slices = get_all_slices_from_parquet(
        config.parquet_root,
        config.run_id,
        config.min_depth,
        config.max_depth,
    )
    
    status = {
        "solution_name": config.solution_name,
        "total_slices": len(all_slices),
        "analyzed_slices": len(existing_analyses),
        "remaining_slices": len(all_slices) - len(existing_analyses),
        "has_checkpoint": checkpoint is not None,
        "checkpoint_batch": checkpoint.current_batch if checkpoint else 0,
        "analyses_dir": str(config.analyses_dir),
    }
    
    if checkpoint:
        status["checkpoint"] = checkpoint.to_dict()
    
    # Aggregate bounded contexts from analyses
    bounded_contexts = set()
    for analysis in existing_analyses.values():
        if analysis.bounded_context_hint:
            bounded_contexts.add(analysis.bounded_context_hint)
    status["bounded_contexts_found"] = sorted(bounded_contexts)
    
    return status


def prepare_batch_for_copilot(
    config: BatchDDDConfig,
    batch_slices: list[dict],
    existing_analyses: dict[str, SliceAnalysis],
) -> list[dict]:
    """Prepare a batch of slices for Copilot analysis.
    
    Returns list of slice contexts with prompts, excluding already-analyzed slices.
    """
    batch_items = []
    
    for slice_info in batch_slices:
        slice_id = slice_info.get("slice_id", "")
        
        # Skip if already analyzed
        if slice_id in existing_analyses:
            continue
        
        # Get context
        context = get_slice_context_from_parquet(
            config.parquet_root,
            config.run_id,
            slice_id,
        )
        
        # Build prompt
        prompt = build_ddd_analysis_prompt_for_slice(slice_id, context)
        
        batch_items.append({
            "slice_id": slice_id,
            "depth": slice_info.get("depth", 0),
            "root_name": slice_info.get("root_name", ""),
            "context": context,
            "prompt": prompt,
        })
    
    return batch_items


def run_batch_ddd_analysis(
    config: BatchDDDConfig,
    analysis_callback: Callable[[str, dict], Optional[dict]] | None = None,
    progress_callback: Callable[[DDDBatchProgress], None] | None = None,
) -> dict:
    """
    Run batch DDD analysis on slices.
    
    This function prepares batches but does NOT call the LLM directly.
    Instead, it returns batch data for the MCP agent to process.
    
    For actual LLM-driven analysis, the MCP tool should:
    1. Call this to get batch info
    2. Iterate through slices, calling Copilot for each
    3. Call apply_batch_analysis with results
    
    Args:
        config: Batch configuration
        analysis_callback: Optional callback to process each slice (for testing)
        progress_callback: Optional callback for progress updates
        
    Returns:
        Dict with batch info or status
    """
    LOGGER.info("Starting batch DDD analysis for %s", config.solution_name)
    LOGGER.info("  Parquet root: %s", config.parquet_root)
    LOGGER.info("  Run ID: %s", config.run_id)
    LOGGER.info("  Batch size: %d", config.batch_size)
    
    # Get all slices
    all_slices = get_all_slices_from_parquet(
        config.parquet_root,
        config.run_id,
        config.min_depth,
        config.max_depth,
    )
    
    if not all_slices:
        return {
            "status": "no_slices",
            "message": "No slices found. Run analyzer with step='slice' first.",
        }
    
    # Load existing analyses
    existing_analyses = load_existing_analyses(config)
    LOGGER.info("Found %d existing analyses", len(existing_analyses))
    
    # Load or create progress
    progress = None
    if config.resume_from_checkpoint:
        progress = DDDBatchProgress.load_checkpoint(config.checkpoint_path)
    
    if not progress:
        progress = DDDBatchProgress(
            total_slices=len(all_slices),
            total_batches=(len(all_slices) + config.batch_size - 1) // config.batch_size,
            start_time=datetime.now(timezone.utc),
            analyzed_slices=len(existing_analyses),
        )
    
    # Calculate batches
    remaining_slices = [s for s in all_slices if s.get("slice_id") not in existing_analyses]
    total_remaining = len(remaining_slices)
    
    if total_remaining == 0:
        return {
            "status": "complete",
            "message": f"All {len(all_slices)} slices already analyzed",
            "total_slices": len(all_slices),
            "analyzed_slices": len(existing_analyses),
            "analyses_dir": str(config.analyses_dir),
            "next_step": f"Run ddd_build_domain_model solution_name='{config.solution_name}' to synthesize domain model",
        }
    
    # Determine batch range
    start_batch = config.start_batch
    if config.resume_from_checkpoint and progress.current_batch > start_batch:
        start_batch = progress.current_batch
    
    batches_needed = (total_remaining + config.batch_size - 1) // config.batch_size
    max_batches = config.max_batches or batches_needed
    end_batch = min(start_batch + max_batches, batches_needed)
    
    LOGGER.info("Processing batches %d to %d (%d slices remaining)", 
                start_batch, end_batch - 1, total_remaining)
    
    # Prepare first batch for agent to process
    # Use index 0 since remaining_slices is already filtered
    batch_start_idx = 0  # Always start from 0 in remaining slices
    batch_end_idx = min(config.batch_size, total_remaining)
    current_batch_slices = remaining_slices[batch_start_idx:batch_end_idx]
    
    batch_items = prepare_batch_for_copilot(
        config,
        current_batch_slices,
        existing_analyses,
    )
    
    return {
        "status": "batch_ready",
        "message": f"Prepared batch {start_batch + 1} of {batches_needed} ({len(batch_items)} slices)",
        "batch_number": start_batch + 1,
        "total_batches": batches_needed,
        "slices_in_batch": len(batch_items),
        "total_remaining": total_remaining,
        "total_slices": len(all_slices),
        "already_analyzed": len(existing_analyses),
        "batch_items": batch_items,  # List of {slice_id, prompt, context}
        "config": {
            "solution_name": config.solution_name,
            "delay_between_slices": config.delay_between_slices,
            "delay_between_batches": config.delay_between_batches,
        },
        "progress": progress.to_dict(),
        "instructions": """
For each slice in batch_items:
1. Read the 'prompt' field
2. Analyze and produce a JSON response with the DDD concepts
3. Call ddd_apply_batch_slice_analysis with the slice_id and your analysis

After all slices in this batch are analyzed:
- Call batch_ddd_analysis with start_batch incremented to get next batch
- Continue until status='complete'

Finally, call ddd_build_domain_model to synthesize the unified domain model.
""",
    }


def apply_batch_slice_analysis(
    config: BatchDDDConfig,
    slice_id: str,
    analysis_data: dict,
) -> dict:
    """Apply analysis for a single slice from batch processing."""
    analysis = SliceAnalysis(
        slice_id=slice_id,
        aggregate_name=analysis_data.get("aggregate_name", f"Aggregate_{slice_id[:8]}"),
        description=analysis_data.get("description", ""),
        properties=analysis_data.get("properties", []),
        behaviors=analysis_data.get("behaviors", []),
        domain_events=analysis_data.get("domain_events", []),
        value_objects=analysis_data.get("value_objects", []),
        invariants=analysis_data.get("invariants", []),
        bounded_context_hint=analysis_data.get("bounded_context_hint", ""),
        source_summary=analysis_data.get("source_summary", ""),
    )
    
    save_slice_analysis(config, analysis)
    
    return {
        "status": "saved",
        "slice_id": slice_id,
        "aggregate_name": analysis.aggregate_name,
        "bounded_context_hint": analysis.bounded_context_hint,
    }


def build_unified_domain_model(config: BatchDDDConfig) -> dict:
    """Build a unified domain model from all slice analyses."""
    from .ddd_builder import (
        DomainModel, DomainAggregate, DomainProperty, 
        DomainValueObject, DomainEvent, DDDAnalysisResult,
        BoundedContextCandidate, UbiquitousTerm,
    )
    
    analyses = load_existing_analyses(config)
    
    if not analyses:
        return {
            "status": "no_analyses",
            "message": "No slice analyses found. Run batch_ddd_analysis first.",
        }
    
    # Group analyses by bounded context hint
    contexts: dict[str, list[SliceAnalysis]] = {}
    for analysis in analyses.values():
        ctx = analysis.bounded_context_hint or "Default"
        contexts.setdefault(ctx, []).append(analysis)
    
    # Build aggregates
    aggregates: list[DomainAggregate] = []
    all_events: set[str] = set()
    all_vos: dict[str, DomainValueObject] = {}
    
    for ctx_name, ctx_analyses in contexts.items():
        for analysis in ctx_analyses:
            # Convert properties - handle both string and dict formats
            props = []
            for p in analysis.properties:
                if isinstance(p, str):
                    # Simple string property name
                    props.append(DomainProperty(name=p, type_name="string", is_required=True))
                else:
                    # Dict with name, type, etc.
                    props.append(DomainProperty(
                        name=p.get("name", ""),
                        type_name=p.get("type", "string"),
                        is_required=p.get("required", True),
                    ))
            
            # Convert value objects - handle both string and dict formats
            vos = []
            for vo in analysis.value_objects:
                if isinstance(vo, str):
                    # Simple string value object name
                    vos.append(DomainValueObject(name=vo, properties=[]))
                else:
                    # Dict with name, properties, etc.
                    vo_props = []
                    for p in vo.get("properties", []):
                        if isinstance(p, str):
                            vo_props.append(DomainProperty(name=p, type_name="string"))
                        else:
                            vo_props.append(DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string")))
                    vos.append(DomainValueObject(name=vo.get("name", ""), properties=vo_props))
            
            # Track shared value objects
            for vo in vos:
                if vo.name not in all_vos:
                    all_vos[vo.name] = vo
            
            # Convert events
            events = [
                DomainEvent(
                    name=e if isinstance(e, str) else e.get("name", ""),
                    aggregate=analysis.aggregate_name,
                )
                for e in analysis.domain_events
            ]
            all_events.update(e.name for e in events)
            
            aggregate = DomainAggregate(
                name=analysis.aggregate_name,
                description=analysis.description,
                properties=props,
                value_objects=vos,
                domain_events=events,
                behaviors=analysis.behaviors,
                invariants=analysis.invariants,
            )
            aggregates.append(aggregate)
    
    # Build bounded context candidates
    bounded_context_candidates = [
        BoundedContextCandidate(
            name=ctx_name,
            description=f"Bounded context for {ctx_name}",
            aggregates=[a.aggregate_name for a in ctx_analyses],
            endpoints=[a.slice_id for a in ctx_analyses],
            confidence_score=0.7,
        )
        for ctx_name, ctx_analyses in contexts.items()
    ]
    
    # Create domain model
    domain_model = DomainModel(
        name=config.solution_name,
        description=f"Domain model for {config.solution_name} generated from {len(analyses)} slice analyses",
        aggregates=aggregates,
        shared_value_objects=list(all_vos.values()),
    )
    
    # Create analysis result
    result = DDDAnalysisResult(
        solution_name=config.solution_name,
        analysis_timestamp=datetime.now(timezone.utc).isoformat(),
        aggregates=aggregates,
        bounded_context_candidates=bounded_context_candidates,
        shared_value_objects=list(all_vos.values()),
        recommended_context=list(contexts.keys())[0] if contexts else "Default",
    )
    
    # Save domain model
    output_dir = config.output_root / config.solution_name / "ddd" / "domain"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    domain_file = output_dir / f"{config.solution_name}_domain.json"
    domain_file.write_text(json.dumps({
        "name": domain_model.name,
        "description": domain_model.description,
        "aggregates": [
            {
                "name": a.name,
                "description": a.description,
                "properties": [{"name": p.name, "type": p.type_name} for p in a.properties],
                "behaviors": a.behaviors,
                "domain_events": [e.name for e in a.domain_events],
                "invariants": a.invariants,
            }
            for a in domain_model.aggregates
        ],
        "bounded_contexts": [ctx.name for ctx in bounded_context_candidates],
        "shared_value_objects": [vo.name for vo in domain_model.shared_value_objects],
    }, indent=2))
    
    # Generate markdown summary
    md_file = output_dir / f"{config.solution_name}_domain.md"
    md_content = f"""# Domain Model: {config.solution_name}

Generated from {len(analyses)} slice analyses at {datetime.now(timezone.utc).isoformat()}

## Bounded Contexts

{chr(10).join(f"- **{ctx.name}**: {len(ctx.aggregates)} aggregates" for ctx in bounded_context_candidates)}

## Aggregates ({len(aggregates)} total)

"""
    for agg in aggregates[:20]:  # Limit display
        md_content += f"""
### {agg.name}

{agg.description}

**Behaviors**: {', '.join(agg.behaviors[:5]) if agg.behaviors else 'None'}

**Domain Events**: {', '.join(e.name for e in agg.domain_events[:5]) if agg.domain_events else 'None'}

---
"""
    
    md_file.write_text(md_content)
    
    return {
        "status": "success",
        "message": f"Built domain model from {len(analyses)} analyses",
        "aggregates_count": len(aggregates),
        "bounded_contexts": [ctx.name for ctx in bounded_context_candidates],
        "domain_events_count": len(all_events),
        "value_objects_count": len(all_vos),
        "domain_file": str(domain_file),
        "markdown_file": str(md_file),
        "next_step": f"ddd_get_sme_review solution_name='{config.solution_name}'",
    }


# ============================================================================
# STATE MANAGER INTEGRATION 
# ============================================================================

def create_job_with_state_manager(config: BatchDDDConfig) -> dict:
    """Create a DDD job with Parquet-based state tracking."""
    from .ddd_state_manager import get_state_manager
    
    state_mgr = get_state_manager(config.parquet_root, config.run_id)
    
    # Count slices
    all_slices = get_all_slices_from_parquet(
        config.parquet_root, config.run_id, config.min_depth, config.max_depth
    )
    
    if not all_slices:
        return {"status": "error", "message": "No slices found"}
    
    # Check for existing job
    existing = state_mgr.get_resumable_job(config.solution_name)
    if existing:
        return {
            "status": "existing_job",
            "job_id": existing.job_id,
            "can_resume": True,
        }
    
    # Create new job
    job = state_mgr.create_job(
        solution_name=config.solution_name,
        total_slices=len(all_slices),
        batch_size=config.batch_size,
        min_depth=config.min_depth,
        max_depth=config.max_depth,
        llm_provider=config.llm_provider,
        llm_model=config.llm_model,
    )
    
    # Create batches
    total_batches = (len(all_slices) + config.batch_size - 1) // config.batch_size
    for batch_num in range(total_batches):
        batch_start = batch_num * config.batch_size
        batch_end = min(batch_start + config.batch_size, len(all_slices))
        batch_slices = all_slices[batch_start:batch_end]
        
        batch = state_mgr.create_batch(job.job_id, batch_num, len(batch_slices))
        state_mgr.register_slices(job.job_id, batch.batch_id, batch_slices)
    
    return {
        "status": "created",
        "job_id": job.job_id,
        "total_slices": len(all_slices),
        "total_batches": total_batches,
    }


def save_analysis_to_state_manager(
    config: BatchDDDConfig,
    slice_id: str,
    analysis: dict,
    llm_response_raw: str = "",
) -> dict:
    """Save slice analysis using state manager."""
    from .ddd_state_manager import get_state_manager
    
    state_mgr = get_state_manager(config.parquet_root, config.run_id)
    job = state_mgr.get_latest_job_for_solution(config.solution_name)
    
    if not job:
        return {"status": "error", "message": "No job found"}
    
    try:
        state_mgr.save_slice_analysis(slice_id, job.job_id, analysis, llm_response_raw)
        
        # Update job progress
        analyzed = len(state_mgr.get_analyzed_slices(job.job_id))
        state_mgr.update_job_progress(job.job_id, analyzed_slices=analyzed)
        
        return {
            "status": "saved",
            "slice_id": slice_id,
            "aggregate_name": analysis.get("aggregate_name", ""),
        }
    except Exception as e:
        state_mgr.mark_slice_failed(slice_id, str(e))
        return {"status": "error", "message": str(e)}


def get_progress_from_state_manager(config: BatchDDDConfig) -> dict:
    """Get progress using state manager."""
    from .ddd_state_manager import get_state_manager
    
    state_mgr = get_state_manager(config.parquet_root, config.run_id)
    job = state_mgr.get_latest_job_for_solution(config.solution_name)
    
    if not job:
        return {"status": "no_job", "message": "No job found"}
    
    return state_mgr.get_job_progress(job.job_id)


def synthesize_model_from_state_manager(config: BatchDDDConfig) -> dict:
    """Synthesize domain model using state manager."""
    from .ddd_state_manager import get_state_manager
    
    state_mgr = get_state_manager(config.parquet_root, config.run_id)
    job = state_mgr.get_latest_job_for_solution(config.solution_name)
    
    if not job:
        return {"status": "no_job", "message": "No job found"}
    
    return state_mgr.synthesize_domain_model(job.job_id)
