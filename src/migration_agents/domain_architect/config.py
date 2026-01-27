from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DomainArchitectConfig(BaseModel):
    entry_keys_path: Path | None = None
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    workers: int | Literal["auto"] = "auto"
    max_name_chars: int = Field(ge=10, le=200, default=80)
    max_comment_chars: int = Field(ge=50, le=1000, default=300)
    max_indicative_chars: int = Field(ge=50, le=1000, default=300)
    context_cluster_bits: int = Field(ge=1, le=16, default=8)
    vector_cluster_bits: int = Field(ge=1, le=16, default=6)
    max_nodes_per_slice: int = Field(ge=10, le=5000, default=500)
    llm_cmd: list[str] = Field(default_factory=list)
    llm_provider: str = Field(default="copilot")  # copilot, github, ollama, cmd
    llm_model: str = Field(default="gpt-4o-mini")
    llm_timeout_sec: int = Field(ge=1, le=600, default=120)
    llm_max_input_chars: int = Field(ge=200, le=20000, default=6000)
    llm_domain_insights_batch_size: int = Field(ge=1, le=50, default=1)
    llm_domain_insights_max_items: int | None = Field(default=None)
    llm_domain_insights_group_size: int | None = Field(default=10)
    llm_domain_insights_max_groups: int | None = Field(default=None)
    llm_workers: int = Field(ge=1, le=16, default=1)
    entry_filter: Literal["pagerank_non_sink", "in_degree_zero"] = Field(default="in_degree_zero")
    exit_filter: Literal["table_nodes", "out_degree_zero", "table_or_sink", "sink_or_recursive"] = Field(
        default="table_nodes"
    )
    pagerank_entry_top_k: int = Field(ge=1, le=100, default=10)
    entry_embedding_model: str = Field(default="all-MiniLM-L6-v2")
    entry_embedding_batch_size: int = Field(ge=1, le=256, default=32)
    enable_entry_embeddings: bool = Field(default=True)
    exclude_recursive_entries: bool = Field(default=True)
    node_type_weights: dict[str, float] = Field(default_factory=lambda: {
        "symbol": 1.0,
        "callsite": 0.6,
        "callee": 0.7,
        "sql_site": 1.2,
        "table": 1.1,
        "data_asset": 1.1,
    })
    llm_endpoint_flow_batch_size: int = Field(ge=1, le=50, default=1)
    llm_endpoint_flow_max_items: int | None = Field(default=None)
    llm_context_groups_max_items: int | None = Field(default=None)
    domain_insights_only: bool = Field(default=False)
    allow_heuristics: bool = Field(default=False)
    max_flow_summary_chars: int = Field(ge=80, le=2000, default=400)
    max_endpoint_paths: int = Field(ge=1, le=200, default=25)
    max_endpoint_path_nodes: int = Field(ge=2, le=100, default=20)
    max_endpoint_nodes: int = Field(ge=50, le=20000, default=5000)
    entry_graph_max_depth: int = Field(ge=1, le=200, default=50)
    entry_graph_node_limit: int = Field(ge=10, le=200000, default=200)
    entry_graph_depth_threshold: int = Field(ge=0, le=200, default=1)
    entry_graph_top_k: int | None = Field(default=5)
    entry_graph_incremental: bool = Field(default=False)
    context_cluster_bits: int = Field(ge=1, le=16, default=8)

    @field_validator("output_root", "entry_keys_path")
    @classmethod
    def _normalize_path(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        return value.expanduser().resolve()

    @field_validator("workers")
    @classmethod
    def _normalize_workers(cls, value: int | str) -> int | str:
        if isinstance(value, str) and value != "auto":
            raise ValueError("workers must be an integer or 'auto'")
        return value


def load_config(path: Path) -> DomainArchitectConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, DomainArchitectConfig)
