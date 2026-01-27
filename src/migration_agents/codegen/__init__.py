"""
Code generation stage package.

Supports:
- DDD-First development (build domain model, then Gherkin, then contract, then code)
- Contract-First development (generate and verify contracts before code)
- Clean Architecture (Domain, Application, Infrastructure, API layers)
- SOLID principles (interface-based design, single responsibility)
- Domain-Driven Design (Aggregates, Value Objects, Domain Events)
- Behavior-Driven Development (Reqnroll/Gherkin tests)
- CQRS pattern (Commands/Queries with MediatR)

Generation Order (DDD-First):
1. Analyze slices → Build Domain Model (Aggregates, Value Objects, Events)
2. Generate Gherkin/BDD specifications from domain behaviors
3. Generate API Contract (OpenAPI) from domain model
4. Generate implementation code (Clean Architecture)
"""

from .config import CodegenConfig, load_config
from .main import run, run_contract_first, run_ddd_first
from .contracts import (
    SliceContext,
    GeneratedContract,
    generate_contract_from_slice,
    generate_contracts_for_slices,
    save_contract_for_verification,
    merge_contracts,
)
from .generator import generate_clean_architecture_solution
from .architecture import (
    ContractDefinition,
    ContractEndpoint,
    Command,
    Query,
    DomainEntity,
    CleanArchitectureSolution,
)
from .ddd_builder import (
    DomainModel,
    DomainAggregate,
    DomainProperty,
    DomainValueObject,
    DomainEvent,
    SliceAnalysis,
    DDDGenerationResult,
    GherkinFeature,
    GherkinScenario,
    LLMConfig,
    # Bounded Context & Ubiquitous Language
    UbiquitousTerm,
    BoundedContextCandidate,
    ContextMap,
    DDDAnalysisResult,
    # Rule-based analysis
    analyze_slice_for_domain,
    build_domain_model_from_slices,
    # Copilot/MCP-oriented functions (single slice)
    get_ddd_analysis_prompt,
    get_domain_model_prompt,
    apply_copilot_analysis,
    apply_copilot_domain_model,
    parse_ddd_analysis_response,
    parse_domain_model_response,
    # Comprehensive DDD analysis (all endpoints)
    get_full_ddd_analysis_prompt,
    get_sme_review_prompt,
    parse_full_ddd_analysis_response,
    parse_sme_review_response,
    # Gherkin and contract generation
    generate_gherkin_from_domain_model,
    generate_contract_from_domain_model,
    run_ddd_first_generation,
    # Legacy aliases
    analyze_slice_with_llm,
    build_domain_model_with_llm,
)

__all__ = [
    # Config
    "CodegenConfig",
    "load_config",
    # Main entry points
    "run",
    "run_ddd_first",
    "run_contract_first",
    # Contract-first types
    "SliceContext",
    "GeneratedContract",
    "generate_contract_from_slice",
    "generate_contracts_for_slices",
    "save_contract_for_verification",
    "merge_contracts",
    # Clean Architecture
    "generate_clean_architecture_solution",
    "ContractDefinition",
    "ContractEndpoint",
    "Command",
    "Query",
    "DomainEntity",
    "CleanArchitectureSolution",
    # DDD-First types
    "DomainModel",
    "DomainAggregate",
    "DomainProperty",
    "DomainValueObject",
    "DomainEvent",
    "SliceAnalysis",
    "DDDGenerationResult",
    "GherkinFeature",
    "GherkinScenario",
    "LLMConfig",
    # Bounded Context & Ubiquitous Language
    "UbiquitousTerm",
    "BoundedContextCandidate",
    "ContextMap",
    "DDDAnalysisResult",
    # Rule-based analysis
    "analyze_slice_for_domain",
    "build_domain_model_from_slices",
    # Copilot/MCP-oriented functions (single slice)
    "get_ddd_analysis_prompt",
    "get_domain_model_prompt",
    "apply_copilot_analysis",
    "apply_copilot_domain_model",
    "parse_ddd_analysis_response",
    "parse_domain_model_response",
    # Comprehensive DDD analysis (all endpoints)
    "get_full_ddd_analysis_prompt",
    "get_sme_review_prompt",
    "parse_full_ddd_analysis_response",
    "parse_sme_review_response",
    # Generation
    "generate_gherkin_from_domain_model",
    "generate_contract_from_domain_model",
    "run_ddd_first_generation",
    # Legacy aliases
    "analyze_slice_with_llm",
    "build_domain_model_with_llm",
]
