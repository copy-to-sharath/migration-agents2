from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CodegenConfig(BaseModel):
    run_id: str = "auto"
    artifact_version: int = Field(ge=1)
    output_root: Path
    generated_root: Path = Path("generated")
    workers: int | Literal["auto"] = "auto"
    api_name: str | None = None
    api_namespace: str = "Generated.Api"
    test_namespace: str = "Generated.Api.Tests"
    max_apis: int | None = None
    max_slices: int | None = None
    """Maximum number of slices to process (None for all)."""
    slice_offset: int = 0
    """Offset for batch processing (skip first N slices)."""
    
    # Slice-based generation
    slice_id: str | None = None
    """Generate code for a specific slice (uses slice context instead of api_contracts)."""
    slice_ids: list[str] | None = None
    """Generate code for multiple slices into a single solution."""
    target_framework: Literal["dotnet8", "springboot3"] = "dotnet8"
    """Target framework for generated code."""
    generate_tests: bool = True
    """Whether to generate BDD test scaffolding."""
    
    # Clean Architecture + DDD + CQRS settings
    solution_name: str = "MigratedSolution"
    """Name of the generated solution (used when combining multiple slices)."""
    use_clean_architecture: bool = True
    """Generate code following Clean Architecture pattern."""
    use_cqrs: bool = True
    """Use CQRS pattern with MediatR for commands/queries."""
    use_ddd: bool = True
    """Use Domain-Driven Design patterns (Aggregates, Value Objects, Domain Events)."""
    
    # DDD-first generation flow
    ddd_first: bool = True
    """Build DDD domain model first, then generate Gherkin/BDD, then generate contract."""
    ddd_phase: Literal["domain", "gherkin", "contract", "all"] = "domain"
    """Phase to run: domain (build model only), gherkin (model + specs), contract (+ API), all (complete)."""
    require_domain_verification: bool = True
    """Require human verification of domain model before generating Gherkin."""
    require_gherkin_verification: bool = True
    """Require human verification of Gherkin/BDD before generating contract."""
    
    # Contract-first settings (legacy - use ddd_first instead)
    contract_first: bool = True
    """Generate and verify contracts before code generation."""
    require_contract_verification: bool = True
    """Require human verification of contracts before generating code."""
    contract_output_path: Path | None = None
    """Path to output generated contracts for verification."""
    
    # LLM settings
    llm_provider: Literal["copilot", "ollama", "cmd", "none"] = "copilot"
    """LLM provider for code generation. 'copilot' uses GitHub Copilot LLM, 'none' for manual Copilot-assisted generation."""
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = "http://localhost:11434/api/generate"
    llm_cmd: list[str] | None = None
    llm_timeout_sec: int = Field(default=60, ge=5, le=600)
    llm_max_input_chars: int = Field(default=6000, ge=512, le=20000)

    @field_validator("output_root", "generated_root", "contract_output_path")
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


def load_config(path: Path) -> CodegenConfig:
    from migration_agents.config_loader import load_with_global

    return load_with_global(path, CodegenConfig)
