"""
DDD-First Builder Module.

This module implements the DDD-first code generation strategy:
1. Build Domain Model (Entities, Aggregates, Value Objects, Domain Events) using Copilot
2. Generate BDD/Gherkin specifications from domain behavior
3. Generate API Contract (OpenAPI) from domain model
4. Generate implementation code

This approach ensures the domain model drives the API design, not vice versa.

Integration with VS Code Copilot via MCP:
- MCP tools expose DDD workflow actions
- Copilot analyzes legacy code and provides domain model insights
- Prompts are structured for Copilot to understand and respond in JSON
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .architecture import (
    ContractDefinition,
    ContractEndpoint,
    Command,
    Query,
    DomainEntity,
)

LOGGER = logging.getLogger("migration_agents.codegen.ddd_builder")


# ============================================================================
# PHASE 1: DOMAIN MODEL BUILDING
# ============================================================================

@dataclass
class DomainProperty:
    """A property on a domain entity or value object."""
    name: str
    type_name: str
    is_required: bool = True
    is_value_object: bool = False
    description: str = ""


@dataclass
class DomainValueObject:
    """A DDD Value Object definition."""
    name: str
    properties: list[DomainProperty] = field(default_factory=list)
    description: str = ""


@dataclass
class DomainEvent:
    """A domain event that can be raised by aggregates."""
    name: str
    aggregate: str
    properties: list[DomainProperty] = field(default_factory=list)
    description: str = ""


@dataclass
class DomainAggregate:
    """A DDD Aggregate Root with its entities, value objects, and events."""
    name: str
    description: str = ""
    properties: list[DomainProperty] = field(default_factory=list)
    value_objects: list[DomainValueObject] = field(default_factory=list)
    domain_events: list[DomainEvent] = field(default_factory=list)
    behaviors: list[str] = field(default_factory=list)  # Method names/behaviors
    invariants: list[str] = field(default_factory=list)  # Business rules
    
    def to_entity(self) -> DomainEntity:
        """Convert to DomainEntity for code generation."""
        return DomainEntity(
            name=self.name,
            is_aggregate_root=True,
            properties=[
                (p.name, p.type_name, p.is_required)
                for p in self.properties
                if p.name != "Id"  # Skip Id, it's inherited
            ],
            value_objects=[vo.name for vo in self.value_objects],
            domain_events=[e.name for e in self.domain_events]
        )


@dataclass
class DomainModel:
    """Complete domain model containing all aggregates and shared components."""
    name: str
    description: str = ""
    aggregates: list[DomainAggregate] = field(default_factory=list)
    shared_value_objects: list[DomainValueObject] = field(default_factory=list)
    shared_events: list[DomainEvent] = field(default_factory=list)
    
    @property
    def all_value_objects(self) -> list[DomainValueObject]:
        """Get all value objects from aggregates and shared."""
        vos = list(self.shared_value_objects)
        for agg in self.aggregates:
            vos.extend(agg.value_objects)
        return vos
    
    @property
    def all_events(self) -> list[DomainEvent]:
        """Get all domain events."""
        events = list(self.shared_events)
        for agg in self.aggregates:
            events.extend(agg.domain_events)
        return events


# ============================================================================
# BOUNDED CONTEXT & UBIQUITOUS LANGUAGE
# ============================================================================

@dataclass
class UbiquitousTerm:
    """A term in the Ubiquitous Language of the domain."""
    term: str
    definition: str
    aliases: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    related_terms: list[str] = field(default_factory=list)
    source_references: list[str] = field(default_factory=list)  # Where this term appears


@dataclass
class BoundedContextCandidate:
    """A candidate bounded context identified during analysis."""
    name: str
    description: str
    aggregates: list[str] = field(default_factory=list)  # Aggregate names in this context
    responsibilities: list[str] = field(default_factory=list)
    endpoints: list[str] = field(default_factory=list)  # Entry points belonging to this context
    ubiquitous_terms: list[str] = field(default_factory=list)  # Terms specific to this context
    integration_points: list[str] = field(default_factory=list)  # How it communicates with other contexts
    confidence_score: float = 0.0  # 0.0 to 1.0
    reasoning: str = ""  # Why this is a good bounded context


@dataclass
class ContextMap:
    """Relationships between bounded contexts."""
    upstream_context: str
    downstream_context: str
    relationship_type: str  # Customer-Supplier, Conformist, Anti-Corruption Layer, etc.
    description: str = ""


@dataclass
class DDDAnalysisResult:
    """Complete DDD analysis result including all endpoints and bounded context recommendations."""
    solution_name: str
    analysis_timestamp: str = ""
    
    # All endpoints analyzed
    endpoints_analyzed: list[str] = field(default_factory=list)
    endpoint_count: int = 0
    depth_levels_analyzed: list[int] = field(default_factory=list)
    
    # Ubiquitous Language
    ubiquitous_language: list[UbiquitousTerm] = field(default_factory=list)
    
    # Bounded Context Candidates (multiple options)
    bounded_context_candidates: list[BoundedContextCandidate] = field(default_factory=list)
    recommended_context: str = ""  # Name of recommended bounded context structure
    recommendation_reasoning: str = ""
    
    # Context Map
    context_map: list[ContextMap] = field(default_factory=list)
    
    # Domain Model (aggregates, events, value objects)
    aggregates: list[DomainAggregate] = field(default_factory=list)
    shared_value_objects: list[DomainValueObject] = field(default_factory=list)
    domain_events: list[DomainEvent] = field(default_factory=list)
    
    # SME Review
    sme_review_required: bool = True
    sme_review_status: str = "pending"  # pending, approved, rejected, needs_revision
    sme_comments: list[str] = field(default_factory=list)
    sme_reviewed_by: str = ""
    sme_reviewed_at: str = ""
    
    def to_review_document(self) -> str:
        """Generate a markdown document for SME review.
        
        IMPORTANT: This method outputs ALL items without truncation.
        No "... and X more" placeholders are used. Every endpoint,
        property, event, and invariant is listed completely.
        """
        lines = [
            f"# DDD Analysis Review: {self.solution_name}",
            "",
            f"**Analysis Date:** {self.analysis_timestamp}",
            f"**Status:** {self.sme_review_status.upper()}",
            f"**Endpoints Analyzed:** {self.endpoint_count}",
            f"**Depth Levels:** {self.depth_levels_analyzed}",
            "",
            "---",
            "",
            "## 1. Ubiquitous Language",
            "",
            "The following terms form the domain vocabulary. Please verify definitions:",
            "",
        ]
        
        for term in self.ubiquitous_language:
            lines.append(f"### {term.term}")
            lines.append(f"**Definition:** {term.definition}")
            if term.aliases:
                lines.append(f"**Aliases:** {', '.join(term.aliases)}")
            if term.examples:
                lines.append(f"**Examples:** {', '.join(term.examples)}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## 2. Bounded Context Candidates",
            "",
            "Multiple bounded context structures were identified. Please review and select:",
            "",
        ])
        
        for i, ctx in enumerate(self.bounded_context_candidates, 1):
            recommended = " ⭐ RECOMMENDED" if ctx.name == self.recommended_context else ""
            lines.append(f"### Option {i}: {ctx.name}{recommended}")
            lines.append(f"**Confidence Score:** {ctx.confidence_score:.0%}")
            lines.append(f"**Description:** {ctx.description}")
            lines.append(f"**Reasoning:** {ctx.reasoning}")
            lines.append(f"**Aggregates:** {', '.join(ctx.aggregates)}")
            lines.append("")
            lines.append("**Responsibilities:**")
            for resp in ctx.responsibilities:
                lines.append(f"  - {resp}")
            lines.append("")
            # Include ALL endpoints - no truncation
            if ctx.endpoints:
                lines.append("**Key Endpoints:**")
                for ep in ctx.endpoints:  # Complete list, no truncation
                    lines.append(f"  - {ep}")
                lines.append("")
            # Include ALL integration points
            if ctx.integration_points:
                lines.append("**Integration Points:**")
                for ip in ctx.integration_points:  # Complete list, no truncation
                    lines.append(f"  - {ip}")
            lines.append("")
        
        if self.recommendation_reasoning:
            lines.extend([
                "### Recommendation Rationale",
                "",
                self.recommendation_reasoning,
                "",
            ])
        
        lines.extend([
            "---",
            "",
            "## 3. Aggregate Roots",
            "",
        ])
        
        for agg in self.aggregates:
            lines.append(f"### {agg.name}")
            lines.append(f"**Description:** {agg.description}")
            lines.append("")
            lines.append("**Properties:**")
            # Include ALL properties with descriptions - no truncation
            for prop in agg.properties:
                req = " (required)" if prop.is_required else ""
                desc = f" - {prop.description}" if prop.description else ""
                lines.append(f"  - `{prop.name}`: {prop.type_name}{req}{desc}")
            lines.append("")
            lines.append("**Behaviors:**")
            # Include ALL behaviors - no truncation
            for beh in agg.behaviors:
                lines.append(f"  - {beh}")
            lines.append("")
            lines.append("**Domain Events Raised:**")
            # Include ALL domain events - no truncation
            for evt in agg.domain_events:
                evt_desc = f": {evt.description}" if evt.description else ""
                lines.append(f"  - {evt.name}{evt_desc}")
            lines.append("")
            lines.append("**Invariants (Business Rules):**")
            # Include ALL invariants - no truncation
            for inv in agg.invariants:
                lines.append(f"  - ⚠️ {inv}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## 4. Domain Events",
            "",
        ])
        
        # Group domain events by aggregate
        events_by_aggregate: dict[str, list] = {}
        for evt in self.domain_events:
            agg = evt.aggregate or "Shared"
            if agg not in events_by_aggregate:
                events_by_aggregate[agg] = []
            events_by_aggregate[agg].append(evt)
        
        for agg_name, events in sorted(events_by_aggregate.items()):
            lines.append(f"### {agg_name} Events")
            for evt in events:
                lines.append(f"- **{evt.name}**: {evt.description}")
                # Include ALL event properties - no truncation
                if evt.properties:
                    for prop in evt.properties:
                        lines.append(f"  - `{prop.name}`: {prop.type_name}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## 5. Shared Value Objects",
            "",
        ])
        
        for vo in self.shared_value_objects:
            lines.append(f"### {vo.name}")
            lines.append(f"**Description:** {vo.description}")
            lines.append("**Properties:**")
            # Include ALL value object properties - no truncation
            for prop in vo.properties:
                desc = f" - {prop.description}" if prop.description else ""
                lines.append(f"  - `{prop.name}`: {prop.type_name}{desc}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## SME Review Section",
            "",
            "Please provide your feedback below:",
            "",
            "### Approval",
            "- [ ] Approved - Domain model is accurate",
            "- [ ] Needs Revision - See comments below",
            "- [ ] Rejected - Major issues identified",
            "",
            "### Comments",
            "",
            "_(Add your comments here)_",
            "",
            "### Reviewer",
            "- **Name:** _______________",
            "- **Date:** _______________",
            "",
        ])
        
        return "\n".join(lines)


@dataclass
class SliceAnalysis:
    """Analysis result from a slice for domain model extraction."""
    slice_id: str
    entry_name: str
    rule_text: str
    source_excerpts: list[str] = field(default_factory=list)
    symbols: list[dict[str, Any]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    
    # Extracted domain concepts
    inferred_aggregate: str = ""
    inferred_behaviors: list[str] = field(default_factory=list)
    inferred_properties: list[DomainProperty] = field(default_factory=list)
    inferred_events: list[str] = field(default_factory=list)
    inferred_invariants: list[str] = field(default_factory=list)
    inferred_value_objects: list[DomainValueObject] = field(default_factory=list)


@dataclass
class LLMConfig:
    """Configuration for Copilot-based domain analysis via MCP.
    
    This config is used when DDD analysis is performed through VS Code
    Copilot. The prompts are exposed via MCP tools, and Copilot provides
    the domain model analysis.
    """
    provider: str = "copilot"  # copilot, rule-based
    model: str = "gpt-4"  # Used for reference/logging only
    timeout_sec: int = 300  # Timeout for Copilot interactions
    max_input_chars: int = 16000  # Copilot can handle larger contexts
    
    @classmethod
    def from_codegen_config(cls, config) -> "LLMConfig":
        """Create LLMConfig from CodegenConfig."""
        return cls(
            provider=getattr(config, "llm_provider", "copilot"),
            model=getattr(config, "llm_model", "gpt-4"),
            timeout_sec=getattr(config, "llm_timeout_sec", 300),
            max_input_chars=getattr(config, "llm_max_input_chars", 16000),
        )


# ============================================================================
# COPILOT/MCP INTEGRATION
# ============================================================================

def get_ddd_analysis_prompt(entry_name: str, rule_text: str, source_excerpts: list[str]) -> str:
    """
    Get the prompt for Copilot to analyze a slice for DDD concepts.
    
    This prompt is used via MCP - Copilot receives this prompt, analyzes
    the legacy code, and returns a structured JSON response.
    """
    excerpts_text = "\n\n---\n\n".join(source_excerpts[:5]) if source_excerpts else "(No source excerpts available)"
    
    return DDD_ANALYSIS_PROMPT.format(
        entry_name=entry_name,
        rule_text=rule_text or "(No business rules documented)",
        source_excerpts=excerpts_text,
    )


def get_domain_model_prompt(solution_name: str, analyses: list[SliceAnalysis]) -> str:
    """
    Get the prompt for Copilot to build a unified domain model.
    
    This prompt is used via MCP - Copilot consolidates slice analyses
    into a comprehensive domain model.
    """
    analyses_text = "\n\n".join([
        f"### Slice: {a.slice_id}\n"
        f"- Entry: {a.entry_name}\n"
        f"- Aggregate: {a.inferred_aggregate}\n"
        f"- Properties: {[p.name for p in a.inferred_properties]}\n"
        f"- Behaviors: {a.inferred_behaviors}\n"
        f"- Events: {a.inferred_events}\n"
        f"- Invariants: {a.inferred_invariants}"
        for a in analyses
    ])
    
    return DDD_DOMAIN_MODEL_PROMPT.format(
        solution_name=solution_name,
        slice_analyses=analyses_text,
    )


def parse_ddd_analysis_response(response: dict[str, Any]) -> dict[str, Any]:
    """Parse and validate DDD analysis response from Copilot."""
    # Handle both direct dict and JSON string
    if isinstance(response, str):
        try:
            response = _parse_json_from_llm(response)
        except Exception:
            return {}
    
    required_keys = ["aggregate_name"]
    for key in required_keys:
        if key not in response:
            LOGGER.warning("Missing required key in DDD response: %s", key)
            return {}
    
    return response


def parse_domain_model_response(response: dict[str, Any]) -> dict[str, Any]:
    """Parse and validate domain model response from Copilot."""
    if isinstance(response, str):
        try:
            response = _parse_json_from_llm(response)
        except Exception:
            return {}
    
    if "aggregates" not in response:
        LOGGER.warning("Missing 'aggregates' in domain model response")
        return {}
    
    return response


def _parse_json_from_llm(response: str) -> dict[str, Any]:
    """Extract and parse JSON from LLM response."""
    # Try to find JSON in the response
    # Look for ```json blocks first
    json_match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find raw JSON object
    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Last resort: try parsing the whole response
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        LOGGER.warning("Failed to parse LLM response as JSON: %s", response[:200])
        return {}


# ============================================================================
# DDD ANALYSIS PROMPTS (Used by Copilot via MCP)
# ============================================================================

DDD_ANALYSIS_PROMPT = """You are a Domain-Driven Design (DDD) expert. Analyze the following legacy code and business rules to extract a domain model.

## Entry Point
{entry_name}

## Business Rules
{rule_text}

## Source Code Excerpts
{source_excerpts}

## Instructions
Extract the following DDD concepts from the code and rules:

1. **Aggregate Root**: The main entity that owns the transaction/operation
2. **Properties**: Data fields on the aggregate (name, type, required, description)
3. **Behaviors**: Methods/operations the aggregate can perform (verb form)
4. **Domain Events**: Events raised when state changes (past tense, e.g., "OrderPlaced")
5. **Value Objects**: Immutable objects representing concepts (e.g., Money, Address)
6. **Invariants**: Business rules that must always be true

Return your analysis as JSON in this exact format:
```json
{{
    "aggregate_name": "Order",
    "aggregate_description": "Represents a customer order in the system",
    "properties": [
        {{"name": "Amount", "type": "decimal", "required": true, "description": "Order total amount"}},
        {{"name": "Status", "type": "string", "required": true, "description": "Current order status"}}
    ],
    "behaviors": ["Place", "Confirm", "Cancel", "Ship"],
    "domain_events": ["OrderPlaced", "OrderConfirmed", "OrderCancelled", "OrderShipped"],
    "value_objects": [
        {{"name": "Money", "properties": [{{"name": "Amount", "type": "decimal"}}, {{"name": "Currency", "type": "string"}}]}}
    ],
    "invariants": [
        "Order amount must be greater than zero",
        "Cannot cancel a shipped order"
    ]
}}
```

Analyze the code and provide your DDD analysis:"""


DDD_DOMAIN_MODEL_PROMPT = """You are a Domain-Driven Design (DDD) expert. Build a comprehensive domain model from the following slice analyses.

## Solution Name
{solution_name}

## Slice Analyses
{slice_analyses}

## Instructions
Consolidate the slice analyses into a unified domain model. Look for:
1. Common aggregates across slices (merge them)
2. Shared value objects
3. Relationships between aggregates
4. Missing behaviors or events

Return the unified domain model as JSON:
```json
{{
    "name": "{solution_name}",
    "description": "Domain model for {solution_name}",
    "aggregates": [
        {{
            "name": "Payment",
            "description": "Aggregate for payment processing",
            "properties": [...],
            "behaviors": [...],
            "domain_events": [...],
            "value_objects": [...],
            "invariants": [...]
        }}
    ],
    "shared_value_objects": [
        {{"name": "Money", "properties": [...], "description": "..."}}
    ]
}}
```

Provide the unified domain model:"""


# ============================================================================
# COMPREHENSIVE DDD ANALYSIS PROMPTS (Multi-Endpoint Analysis)
# ============================================================================

DDD_FULL_ANALYSIS_PROMPT = """You are a Domain-Driven Design (DDD) expert performing a comprehensive analysis of a legacy system for migration to a modern architecture.

## Solution Name
{solution_name}

## All Endpoints Analyzed
{endpoints_summary}

## Depth Levels Covered
{depth_levels}

## Complete Source Analysis
{source_analysis}

## Instructions

You MUST analyze ALL {endpoint_count} endpoints before forming conclusions. Look for patterns across the entire system.

Provide a comprehensive DDD analysis including:

### 1. UBIQUITOUS LANGUAGE
Extract ALL domain terms used consistently across the codebase. For each term provide:
- Clear definition
- Aliases (different names for same concept)
- Usage examples
- Related terms

### 2. BOUNDED CONTEXT CANDIDATES
Identify AT LEAST 2-3 different ways the system could be divided into bounded contexts. For each option:
- Name and description
- Which aggregates belong
- Responsibilities
- Integration points with other contexts
- Confidence score (0.0 to 1.0)
- Reasoning for this grouping

### 3. RECOMMENDED BOUNDED CONTEXT STRUCTURE
Select the BEST bounded context structure and explain WHY with specific reasoning.

### 4. AGGREGATE ROOTS
For each aggregate root identified:
- Name and description
- Properties with types
- Behaviors (commands it handles)
- Domain events it raises
- Invariants (business rules that must always be true)

### 5. VALUE OBJECTS
Immutable objects that represent domain concepts.

### 6. DOMAIN EVENTS
All events raised across the system.

### 7. CONTEXT MAP
How bounded contexts interact (Customer-Supplier, Conformist, Anti-Corruption Layer, etc.)

Return your analysis as JSON:
```json
{{
    "ubiquitous_language": [
        {{
            "term": "Payment",
            "definition": "A financial transaction representing money movement",
            "aliases": ["Transaction", "Txn"],
            "examples": ["Authorization payment", "Capture payment"],
            "related_terms": ["Amount", "Merchant", "Customer"]
        }}
    ],
    "bounded_context_candidates": [
        {{
            "name": "Payment Processing",
            "description": "Handles all payment lifecycle operations",
            "aggregates": ["Payment", "Authorization"],
            "responsibilities": ["Process payments", "Handle refunds"],
            "endpoints": ["CapturePayment", "AuthorizePayment", "RefundPayment"],
            "ubiquitous_terms": ["Payment", "Authorization", "Capture"],
            "integration_points": ["Merchant Context via events", "Customer Context via shared ID"],
            "confidence_score": 0.85,
            "reasoning": "Payment operations are cohesive and can be isolated"
        }},
        {{
            "name": "Alternative: Transaction Context",
            "description": "Broader context including all financial transactions",
            "aggregates": ["Transaction", "Account"],
            "responsibilities": ["All financial operations"],
            "endpoints": [...],
            "confidence_score": 0.65,
            "reasoning": "More general but less focused"
        }}
    ],
    "recommended_context": "Payment Processing",
    "recommendation_reasoning": "Payment Processing provides better cohesion because...",
    "context_map": [
        {{
            "upstream_context": "Payment Processing",
            "downstream_context": "Reporting",
            "relationship_type": "Customer-Supplier",
            "description": "Payment events are consumed by Reporting"
        }}
    ],
    "aggregates": [
        {{
            "name": "Payment",
            "description": "Aggregate root for payment transactions",
            "properties": [
                {{"name": "Amount", "type": "decimal", "required": true, "description": "Payment amount"}}
            ],
            "behaviors": ["Authorize", "Capture", "Refund", "Void"],
            "domain_events": ["PaymentAuthorized", "PaymentCaptured", "PaymentRefunded"],
            "value_objects": [{{"name": "Money", "properties": [...]}}],
            "invariants": ["Amount must be positive", "Cannot refund more than captured"]
        }}
    ],
    "shared_value_objects": [
        {{
            "name": "Money",
            "properties": [{{"name": "Amount", "type": "decimal"}}, {{"name": "Currency", "type": "string"}}],
            "description": "Represents a monetary value with currency"
        }}
    ],
    "domain_events": [
        {{
            "name": "PaymentCaptured",
            "aggregate": "Payment",
            "properties": [{{"name": "PaymentId", "type": "Guid"}}, {{"name": "Amount", "type": "decimal"}}],
            "description": "Raised when a payment is successfully captured"
        }}
    ]
}}
```

IMPORTANT: This analysis will be reviewed by a Subject Matter Expert (SME). Be thorough and provide clear reasoning for all recommendations."""


DDD_SME_REVIEW_PROMPT = """You are a Subject Matter Expert (SME) reviewing a Domain-Driven Design analysis.

## DDD Analysis to Review
{ddd_analysis}

## Review Instructions

Please review the DDD analysis above and provide feedback on:

1. **Ubiquitous Language Accuracy**
   - Are terms correctly defined?
   - Are there missing domain terms?
   - Are aliases correct?

2. **Bounded Context Appropriateness**
   - Are the suggested bounded contexts correctly scoped?
   - Are responsibilities properly assigned?
   - Are there better alternatives?

3. **Aggregate Design**
   - Are aggregate boundaries correct?
   - Are invariants accurately captured?
   - Are behaviors complete?

4. **Domain Events**
   - Are all significant state changes captured as events?
   - Are event names following past-tense convention?

5. **Overall Assessment**
   - APPROVE: Analysis is accurate and complete
   - NEEDS_REVISION: Minor issues to address
   - REJECT: Major issues require re-analysis

Provide your review as JSON:
```json
{{
    "review_status": "APPROVE|NEEDS_REVISION|REJECT",
    "overall_assessment": "Summary of your review",
    "ubiquitous_language_feedback": {{
        "accurate": true,
        "missing_terms": ["term1", "term2"],
        "corrections": [{{"term": "X", "correction": "Should be Y"}}]
    }},
    "bounded_context_feedback": {{
        "recommended_structure_approved": true,
        "suggested_changes": ["Change X to Y"],
        "alternative_recommendation": null
    }},
    "aggregate_feedback": [
        {{
            "aggregate": "Payment",
            "feedback": "Looks good",
            "missing_behaviors": [],
            "incorrect_invariants": []
        }}
    ],
    "domain_event_feedback": {{
        "complete": true,
        "missing_events": [],
        "naming_issues": []
    }},
    "action_items": [
        "Action 1",
        "Action 2"
    ],
    "reviewer_notes": "Additional notes..."
}}
```"""


def get_full_ddd_analysis_prompt(
    solution_name: str,
    endpoints: list[dict[str, Any]],
    depth_levels: list[int],
    source_analysis: str,
) -> str:
    """
    Get the prompt for comprehensive DDD analysis of ALL endpoints.
    
    This prompt analyzes the entire system before drawing conclusions
    about bounded contexts and domain model structure.
    """
    endpoints_summary = "\n".join([
        f"- **{ep.get('name', 'Unknown')}** (Depth {ep.get('depth', '?')}): {ep.get('description', 'No description')}"
        for ep in endpoints
    ])
    
    depth_str = ", ".join(str(d) for d in sorted(set(depth_levels)))
    
    return DDD_FULL_ANALYSIS_PROMPT.format(
        solution_name=solution_name,
        endpoints_summary=endpoints_summary,
        depth_levels=depth_str,
        endpoint_count=len(endpoints),
        source_analysis=source_analysis,
    )


def get_sme_review_prompt(ddd_analysis: DDDAnalysisResult) -> str:
    """Get the prompt for SME review of DDD analysis."""
    return DDD_SME_REVIEW_PROMPT.format(
        ddd_analysis=ddd_analysis.to_review_document()
    )


def parse_full_ddd_analysis_response(response: dict[str, Any]) -> DDDAnalysisResult | None:
    """Parse the comprehensive DDD analysis response from Copilot."""
    if isinstance(response, str):
        try:
            response = _parse_json_from_llm(response)
        except Exception:
            return None
    
    if not response:
        return None
    
    result = DDDAnalysisResult(
        solution_name="",
        analysis_timestamp=datetime.now().isoformat(),
    )
    
    # Parse ubiquitous language
    for term_data in response.get("ubiquitous_language", []):
        result.ubiquitous_language.append(UbiquitousTerm(
            term=term_data.get("term", ""),
            definition=term_data.get("definition", ""),
            aliases=term_data.get("aliases", []),
            examples=term_data.get("examples", []),
            related_terms=term_data.get("related_terms", []),
        ))
    
    # Parse bounded context candidates
    for ctx_data in response.get("bounded_context_candidates", []):
        result.bounded_context_candidates.append(BoundedContextCandidate(
            name=ctx_data.get("name", ""),
            description=ctx_data.get("description", ""),
            aggregates=ctx_data.get("aggregates", []),
            responsibilities=ctx_data.get("responsibilities", []),
            endpoints=ctx_data.get("endpoints", []),
            ubiquitous_terms=ctx_data.get("ubiquitous_terms", []),
            integration_points=ctx_data.get("integration_points", []),
            confidence_score=ctx_data.get("confidence_score", 0.0),
            reasoning=ctx_data.get("reasoning", ""),
        ))
    
    result.recommended_context = response.get("recommended_context", "")
    result.recommendation_reasoning = response.get("recommendation_reasoning", "")
    
    # Parse context map
    for cm_data in response.get("context_map", []):
        result.context_map.append(ContextMap(
            upstream_context=cm_data.get("upstream_context", ""),
            downstream_context=cm_data.get("downstream_context", ""),
            relationship_type=cm_data.get("relationship_type", ""),
            description=cm_data.get("description", ""),
        ))
    
    # Parse aggregates
    for agg_data in response.get("aggregates", []):
        properties = [
            DomainProperty(
                name=p.get("name", ""),
                type_name=p.get("type", "string"),
                is_required=p.get("required", True),
                description=p.get("description", ""),
            )
            for p in agg_data.get("properties", [])
        ]
        
        value_objects = [
            DomainValueObject(
                name=vo.get("name", ""),
                properties=[
                    DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string"))
                    for p in vo.get("properties", [])
                ],
            )
            for vo in agg_data.get("value_objects", [])
        ]
        
        domain_events = [
            DomainEvent(
                name=e if isinstance(e, str) else e.get("name", ""),
                aggregate=agg_data.get("name", ""),
            )
            for e in agg_data.get("domain_events", [])
        ]
        
        result.aggregates.append(DomainAggregate(
            name=agg_data.get("name", ""),
            description=agg_data.get("description", ""),
            properties=properties,
            value_objects=value_objects,
            domain_events=domain_events,
            behaviors=agg_data.get("behaviors", []),
            invariants=agg_data.get("invariants", []),
        ))
    
    # Parse shared value objects
    for vo_data in response.get("shared_value_objects", []):
        result.shared_value_objects.append(DomainValueObject(
            name=vo_data.get("name", ""),
            properties=[
                DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string"))
                for p in vo_data.get("properties", [])
            ],
            description=vo_data.get("description", ""),
        ))
    
    # Parse domain events
    for evt_data in response.get("domain_events", []):
        result.domain_events.append(DomainEvent(
            name=evt_data.get("name", ""),
            aggregate=evt_data.get("aggregate", ""),
            properties=[
                DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string"))
                for p in evt_data.get("properties", [])
            ],
            description=evt_data.get("description", ""),
        ))
    
    return result


def parse_sme_review_response(response: dict[str, Any]) -> dict[str, Any]:
    """Parse SME review response."""
    if isinstance(response, str):
        try:
            response = _parse_json_from_llm(response)
        except Exception:
            return {"review_status": "ERROR", "error": "Failed to parse response"}
    
    return response


# ============================================================================
# COPILOT-BASED DOMAIN ANALYSIS (Via MCP)
# ============================================================================

def apply_copilot_analysis(
    slice_id: str,
    entry_name: str,
    rule_text: str,
    source_excerpts: list[str] | None = None,
    symbols: list[dict] | None = None,
    copilot_response: dict[str, Any] | None = None,
) -> SliceAnalysis:
    """
    Apply Copilot's DDD analysis response to create a SliceAnalysis.
    
    This is called after Copilot responds to the DDD analysis prompt.
    If no copilot_response is provided, falls back to rule-based analysis.
    
    Args:
        slice_id: Unique identifier for the slice
        entry_name: Entry point name (e.g., "CapturePayment")
        rule_text: Business rules from BRD
        source_excerpts: Source code snippets
        symbols: Symbol information from parsing
        copilot_response: JSON response from Copilot (parsed)
    
    Returns:
        SliceAnalysis with extracted domain concepts
    """
    LOGGER.info("Applying Copilot DDD analysis for slice %s", slice_id)
    
    analysis = SliceAnalysis(
        slice_id=slice_id,
        entry_name=entry_name,
        rule_text=rule_text,
        source_excerpts=source_excerpts or [],
        symbols=symbols or [],
    )
    
    if not copilot_response:
        LOGGER.info("No Copilot response provided, using rule-based analysis")
        return analyze_slice_for_domain(slice_id, entry_name, rule_text, source_excerpts, symbols)
    
    # Parse response if it's a string
    ddd_data = parse_ddd_analysis_response(copilot_response)
    
    if not ddd_data:
        LOGGER.warning("Failed to parse Copilot response, falling back to rule-based")
        return analyze_slice_for_domain(slice_id, entry_name, rule_text, source_excerpts, symbols)
    
    # Extract aggregate
    analysis.inferred_aggregate = ddd_data.get("aggregate_name", entry_name)
    
    # Extract properties
    for prop in ddd_data.get("properties", []):
        analysis.inferred_properties.append(DomainProperty(
            name=prop.get("name", ""),
            type_name=prop.get("type", "string"),
            is_required=prop.get("required", True),
            description=prop.get("description", ""),
        ))
    
    # Extract behaviors
    analysis.inferred_behaviors = ddd_data.get("behaviors", [])
    
    # Extract events
    analysis.inferred_events = ddd_data.get("domain_events", [])
    
    # Extract invariants
    analysis.inferred_invariants = ddd_data.get("invariants", [])
    
    # Extract value objects
    for vo in ddd_data.get("value_objects", []):
        vo_props = [
            DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string"))
            for p in vo.get("properties", [])
        ]
        analysis.inferred_value_objects.append(DomainValueObject(
            name=vo.get("name", ""),
            properties=vo_props,
            description=vo.get("description", ""),
        ))
    
    LOGGER.info("Copilot extracted aggregate=%s, behaviors=%d, events=%d",
               analysis.inferred_aggregate,
               len(analysis.inferred_behaviors),
               len(analysis.inferred_events))
    
    return analysis


def apply_copilot_domain_model(
    analyses: list[SliceAnalysis],
    model_name: str,
    copilot_response: dict[str, Any] | None = None,
) -> DomainModel:
    """
    Apply Copilot's domain model response to create a DomainModel.
    
    This is called after Copilot responds to the domain model prompt.
    If no copilot_response is provided, falls back to rule-based building.
    
    Args:
        analyses: Slice analyses to consolidate
        model_name: Name for the domain model
        copilot_response: JSON response from Copilot (parsed)
    
    Returns:
        DomainModel consolidated from analyses
    """
    LOGGER.info("Applying Copilot domain model for %s", model_name)
    
    if not copilot_response:
        LOGGER.info("No Copilot response provided, using rule-based building")
        return build_domain_model_from_slices(analyses, model_name)
    
    # Parse response if it's a string
    model_data = parse_domain_model_response(copilot_response)
    
    if not model_data:
        LOGGER.warning("Failed to parse Copilot domain model, falling back to rule-based")
        return build_domain_model_from_slices(analyses, model_name)
    
    aggregates: list[DomainAggregate] = []
    
    for agg_data in model_data.get("aggregates", []):
        properties = [
            DomainProperty(
                name=p.get("name", ""),
                type_name=p.get("type", "string"),
                is_required=p.get("required", True),
                description=p.get("description", ""),
            )
            for p in agg_data.get("properties", [])
        ]
        
        value_objects = [
            DomainValueObject(
                name=vo.get("name", ""),
                properties=[
                    DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string"))
                    for p in vo.get("properties", [])
                ],
                description=vo.get("description", ""),
            )
            for vo in agg_data.get("value_objects", [])
        ]
        
        domain_events = [
            DomainEvent(
                name=e if isinstance(e, str) else e.get("name", ""),
                aggregate=agg_data.get("name", ""),
                description="",
            )
            for e in agg_data.get("domain_events", [])
        ]
        
        aggregates.append(DomainAggregate(
            name=agg_data.get("name", ""),
            description=agg_data.get("description", ""),
            properties=properties,
            value_objects=value_objects,
            domain_events=domain_events,
            behaviors=agg_data.get("behaviors", []),
            invariants=agg_data.get("invariants", []),
        ))
    
    shared_vos = [
        DomainValueObject(
            name=vo.get("name", ""),
            properties=[
                DomainProperty(name=p.get("name", ""), type_name=p.get("type", "string"))
                for p in vo.get("properties", [])
            ],
            description=vo.get("description", ""),
        )
        for vo in model_data.get("shared_value_objects", [])
    ]
    
    return DomainModel(
        name=model_data.get("name", model_name),
        description=model_data.get("description", ""),
        aggregates=aggregates,
        shared_value_objects=shared_vos,
    )


# Legacy function aliases for backward compatibility
def analyze_slice_with_llm(
    slice_id: str,
    entry_name: str,
    rule_text: str,
    source_excerpts: list[str] | None = None,
    symbols: list[dict] | None = None,
    llm_config: LLMConfig | None = None,
) -> SliceAnalysis:
    """Legacy alias - use rule-based analysis (Copilot is used via MCP)."""
    LOGGER.info("analyze_slice_with_llm called - using rule-based (use MCP for Copilot)")
    return analyze_slice_for_domain(slice_id, entry_name, rule_text, source_excerpts, symbols)


def build_domain_model_with_llm(
    analyses: list[SliceAnalysis],
    model_name: str,
    llm_config: LLMConfig | None = None,
) -> DomainModel:
    """Legacy alias - use rule-based building (Copilot is used via MCP)."""
    LOGGER.info("build_domain_model_with_llm called - using rule-based (use MCP for Copilot)")
    return build_domain_model_from_slices(analyses, model_name)


# ============================================================================
# RULE-BASED FALLBACK (Original Implementation)
# ============================================================================

def _extract_aggregate_name(entry_name: str, rule_text: str) -> str:
    """Extract the primary aggregate name from entry point and rules."""
    name = entry_name
    
    # Remove action prefixes FIRST (before suffixes)
    for prefix in ["Process", "Handle", "Execute", "Run", "Do", "Get", 
                   "Create", "Update", "Delete", "Find", "Search", "Capture",
                   "Authorize", "Cancel", "Complete", "Submit", "Validate"]:
        if name.startswith(prefix) and len(name) > len(prefix):
            name = name[len(prefix):]
            break
    
    # Remove common suffixes
    for suffix in ["Processor", "Service", "Handler", "Controller", "Manager", 
                   "Helper", "Command", "Query", "Request", "Response"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    
    return name or "Entity"


def _infer_properties_from_rule(rule_text: str, aggregate_name: str) -> list[DomainProperty]:
    """Infer domain properties from business rule text."""
    properties: list[DomainProperty] = []
    rule_lower = rule_text.lower()
    aggregate_lower = aggregate_name.lower()
    
    # Common patterns in payment/order domains
    if "payment" in aggregate_lower or "order" in aggregate_lower or "amount" in rule_lower:
        properties.extend([
            DomainProperty(name="Amount", type_name="decimal", is_required=True, 
                          description="Transaction amount"),
            DomainProperty(name="Currency", type_name="string", is_required=False,
                          description="Currency code (e.g., USD)"),
            DomainProperty(name="Status", type_name="string", is_required=True,
                          description="Current status"),
        ])
    
    if "capture" in rule_lower or "authorize" in rule_lower:
        properties.append(
            DomainProperty(name="AuthorizationCode", type_name="string", is_required=False,
                          description="Authorization code from payment provider")
        )
    
    if "customer" in rule_lower or "user" in rule_lower:
        properties.append(
            DomainProperty(name="CustomerId", type_name="Guid", is_required=True,
                          description="Customer identifier")
        )
    
    if "merchant" in rule_lower or "vendor" in rule_lower:
        properties.append(
            DomainProperty(name="MerchantId", type_name="Guid", is_required=True,
                          description="Merchant identifier")
        )
    
    return properties


def _infer_behaviors_from_entry(entry_name: str, rule_text: str) -> list[str]:
    """Infer aggregate behaviors from entry point name and rules."""
    behaviors: list[str] = []
    
    # Extract main action from entry name
    action = entry_name
    for prefix in ["Process", "Handle", "Execute", "Run", "Do"]:
        if action.startswith(prefix):
            action = action[len(prefix):]
            break
    
    if action:
        behaviors.append(action)
    
    # Look for additional actions in rule text
    action_patterns = [
        r"(validate|verify|check)\s+\w+",
        r"(create|update|delete|cancel|complete|process)\s+\w+",
        r"(send|receive|notify|publish)\s+\w+",
    ]
    
    for pattern in action_patterns:
        matches = re.findall(pattern, rule_text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            behavior = match.title().replace(" ", "")
            if behavior and behavior not in behaviors:
                behaviors.append(behavior)
    
    return behaviors[:5]  # Limit to 5 behaviors


def _infer_events_from_behaviors(aggregate_name: str, behaviors: list[str]) -> list[str]:
    """Infer domain events from aggregate behaviors."""
    events: list[str] = []
    
    past_tense_map = {
        "Create": "Created",
        "Update": "Updated",
        "Delete": "Deleted",
        "Cancel": "Cancelled",
        "Complete": "Completed",
        "Process": "Processed",
        "Capture": "Captured",
        "Authorize": "Authorized",
        "Refund": "Refunded",
        "Validate": "Validated",
        "Submit": "Submitted",
        "Approve": "Approved",
        "Reject": "Rejected",
        "Send": "Sent",
    }
    
    for behavior in behaviors:
        # Skip if behavior is the same as aggregate (avoid PaymentPaymented)
        if behavior.lower() == aggregate_name.lower():
            continue
        
        # Try to map to past tense
        past = past_tense_map.get(behavior)
        if not past:
            # Default: add 'ed' or 'd'
            if behavior.endswith("e"):
                past = behavior + "d"
            else:
                past = behavior + "ed"
        
        events.append(f"{aggregate_name}{past}")
    
    return events


def _infer_invariants_from_rule(rule_text: str) -> list[str]:
    """Extract business invariants from rule text."""
    invariants: list[str] = []
    
    # Look for constraint patterns
    constraint_patterns = [
        r"must\s+(be|have|not|always|never)\s+[^.]+",
        r"cannot\s+[^.]+",
        r"should\s+(not\s+)?[^.]+", 
        r"only\s+(if|when)\s+[^.]+",
        r"requires?\s+[^.]+",
    ]
    
    for pattern in constraint_patterns:
        matches = re.findall(pattern, rule_text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = " ".join(m for m in match if m)
            invariant = match.strip().capitalize()
            if invariant and len(invariant) > 10:  # Skip very short matches
                invariants.append(invariant)
    
    return invariants[:5]  # Limit to 5 invariants


def analyze_slice_for_domain(
    slice_id: str,
    entry_name: str,
    rule_text: str,
    source_excerpts: list[str] = None,
    symbols: list[dict] = None
) -> SliceAnalysis:
    """Analyze a slice to extract domain model concepts."""
    LOGGER.info("Analyzing slice %s for domain concepts", slice_id)
    
    analysis = SliceAnalysis(
        slice_id=slice_id,
        entry_name=entry_name,
        rule_text=rule_text,
        source_excerpts=source_excerpts or [],
        symbols=symbols or [],
    )
    
    # Extract aggregate name
    analysis.inferred_aggregate = _extract_aggregate_name(entry_name, rule_text)
    
    # Infer properties
    analysis.inferred_properties = _infer_properties_from_rule(rule_text, analysis.inferred_aggregate)
    
    # Infer behaviors
    analysis.inferred_behaviors = _infer_behaviors_from_entry(entry_name, rule_text)
    
    # Infer domain events
    analysis.inferred_events = _infer_events_from_behaviors(
        analysis.inferred_aggregate, 
        analysis.inferred_behaviors
    )
    
    # Extract invariants
    analysis.inferred_invariants = _infer_invariants_from_rule(rule_text)
    
    return analysis


def build_domain_model_from_slices(
    analyses: list[SliceAnalysis],
    model_name: str
) -> DomainModel:
    """Build a complete domain model from multiple slice analyses."""
    LOGGER.info("Building domain model '%s' from %d slices", model_name, len(analyses))
    
    aggregates: dict[str, DomainAggregate] = {}
    
    for analysis in analyses:
        agg_name = analysis.inferred_aggregate
        
        if agg_name not in aggregates:
            aggregates[agg_name] = DomainAggregate(
                name=agg_name,
                description=f"Aggregate root for {agg_name} domain",
                properties=[],
                value_objects=[],
                domain_events=[],
                behaviors=[],
                invariants=[],
            )
        
        agg = aggregates[agg_name]
        
        # Merge properties (dedupe by name)
        existing_prop_names = {p.name for p in agg.properties}
        for prop in analysis.inferred_properties:
            if prop.name not in existing_prop_names:
                agg.properties.append(prop)
                existing_prop_names.add(prop.name)
        
        # Merge behaviors
        for behavior in analysis.inferred_behaviors:
            if behavior not in agg.behaviors:
                agg.behaviors.append(behavior)
        
        # Create domain events
        for event_name in analysis.inferred_events:
            if not any(e.name == event_name for e in agg.domain_events):
                agg.domain_events.append(DomainEvent(
                    name=event_name,
                    aggregate=agg_name,
                    description=f"Raised when {agg_name} is modified"
                ))
        
        # Merge invariants
        for inv in analysis.inferred_invariants:
            if inv not in agg.invariants:
                agg.invariants.append(inv)
    
    return DomainModel(
        name=model_name,
        description=f"Domain model containing {len(aggregates)} aggregate(s)",
        aggregates=list(aggregates.values()),
    )


# ============================================================================
# PHASE 2: BDD/GHERKIN GENERATION FROM DOMAIN
# ============================================================================

@dataclass
class GherkinScenario:
    """A Gherkin scenario for BDD testing."""
    name: str
    description: str = ""
    given: list[str] = field(default_factory=list)
    when: list[str] = field(default_factory=list)
    then: list[str] = field(default_factory=list)
    examples: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class GherkinFeature:
    """A Gherkin feature file definition."""
    name: str
    description: str = ""
    background: list[str] = field(default_factory=list)
    scenarios: list[GherkinScenario] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    
    def render(self) -> str:
        """Render the feature to Gherkin text."""
        lines = []
        
        # Tags
        if self.tags:
            lines.append(" ".join(f"@{tag}" for tag in self.tags))
        
        # Feature header
        lines.append(f"Feature: {self.name}")
        if self.description:
            for desc_line in self.description.split("\n"):
                lines.append(f"  {desc_line}")
        lines.append("")
        
        # Background
        if self.background:
            lines.append("  Background:")
            for step in self.background:
                lines.append(f"    {step}")
            lines.append("")
        
        # Scenarios
        for scenario in self.scenarios:
            lines.append(f"  Scenario: {scenario.name}")
            
            for step in scenario.given:
                lines.append(f"    Given {step}")
            for step in scenario.when:
                lines.append(f"    When {step}")
            for step in scenario.then:
                lines.append(f"    Then {step}")
            
            # Scenario Outline with Examples
            if scenario.examples:
                lines.append("    Examples:")
                # Header
                headers = list(scenario.examples[0].keys())
                lines.append("      | " + " | ".join(headers) + " |")
                for example in scenario.examples:
                    values = [str(example.get(h, "")) for h in headers]
                    lines.append("      | " + " | ".join(values) + " |")
            
            lines.append("")
        
        return "\n".join(lines)


def _behavior_to_past_tense(behavior: str) -> str:
    """Convert a behavior name to past tense for Gherkin assertions."""
    past_tense_map = {
        "Create": "created",
        "Update": "updated",
        "Delete": "deleted",
        "Cancel": "cancelled",
        "Complete": "completed",
        "Process": "processed",
        "Capture": "captured",
        "Authorize": "authorized",
        "Refund": "refunded",
        "Validate": "validated",
        "Submit": "submitted",
        "Approve": "approved",
        "Reject": "rejected",
        "Send": "sent",
        "CapturePayment": "captured",
        "AuthorizePayment": "authorized",
        "RefundPayment": "refunded",
    }
    return past_tense_map.get(behavior, behavior.lower() + "ed")


def _behavior_to_action(behavior: str) -> str:
    """Convert a behavior name to action verb for Gherkin When steps."""
    action_map = {
        "CapturePayment": "capture payment for",
        "AuthorizePayment": "authorize payment for",
        "RefundPayment": "refund",
        "Create": "create",
        "Update": "update",
        "Delete": "delete",
        "Cancel": "cancel",
        "Complete": "complete",
        "Process": "process",
        "Capture": "capture",
        "Authorize": "authorize",
        "Refund": "refund",
        "Validate": "validate",
        "Submit": "submit",
        "Approve": "approve",
        "Reject": "reject",
        "Send": "send",
    }
    return action_map.get(behavior, behavior.lower())


def generate_gherkin_from_aggregate(aggregate: DomainAggregate) -> GherkinFeature:
    """Generate Gherkin feature from a domain aggregate."""
    LOGGER.info("Generating Gherkin for aggregate: %s", aggregate.name)
    
    scenarios: list[GherkinScenario] = []
    
    # Generate scenario for each behavior
    for behavior in aggregate.behaviors:
        action = _behavior_to_action(behavior)
        past_tense = _behavior_to_past_tense(behavior)
        event_name = f"{aggregate.name}{past_tense.title().replace(' ', '')}"
        
        scenario = GherkinScenario(
            name=f"{behavior} {aggregate.name} successfully",
            given=[
                f"a valid {aggregate.name} exists",
                f"the {aggregate.name} is in a valid state",
            ],
            when=[
                f"I {action} the {aggregate.name}",
            ],
            then=[
                f"the {aggregate.name} should be {past_tense}",
                f"a {event_name} event should be raised",
            ]
        )
        scenarios.append(scenario)
    
    # Generate invariant validation scenarios
    for i, invariant in enumerate(aggregate.invariants[:3]):  # Limit to 3
        scenario = GherkinScenario(
            name=f"Validate invariant: {invariant[:50]}",
            given=[
                f"a {aggregate.name} with invalid state",
            ],
            when=[
                f"I attempt to modify the {aggregate.name}",
            ],
            then=[
                f"the operation should fail",
                f"an error should indicate: {invariant[:100]}",
            ]
        )
        scenarios.append(scenario)
    
    return GherkinFeature(
        name=f"{aggregate.name} Domain Behavior",
        description=aggregate.description + "\n\nThis feature verifies the domain behavior of " + aggregate.name,
        background=[
            "the system is initialized",
            f"a {aggregate.name} repository is available",
        ],
        scenarios=scenarios,
        tags=[aggregate.name.lower(), "domain", "bdd"]
    )


def generate_gherkin_from_domain_model(domain_model: DomainModel) -> list[GherkinFeature]:
    """Generate all Gherkin features from a domain model."""
    features: list[GherkinFeature] = []
    
    for aggregate in domain_model.aggregates:
        feature = generate_gherkin_from_aggregate(aggregate)
        features.append(feature)
    
    return features


# ============================================================================
# PHASE 3: CONTRACT GENERATION FROM DOMAIN
# ============================================================================

def generate_contract_from_domain_model(
    domain_model: DomainModel,
    api_version: str = "1.0.0"
) -> ContractDefinition:
    """Generate API contract from the domain model."""
    LOGGER.info("Generating contract from domain model: %s", domain_model.name)
    
    endpoints: list[ContractEndpoint] = []
    schemas: dict[str, Any] = {}
    
    for aggregate in domain_model.aggregates:
        agg_kebab = _pascal_to_kebab(aggregate.name)
        base_path = f"/api/{agg_kebab}"
        
        # Generate CRUD + behavior endpoints
        # GET collection
        endpoints.append(ContractEndpoint(
            path=base_path,
            method="GET",
            operation_id=f"get{aggregate.name}List",
            summary=f"Get list of {aggregate.name} items",
            response_schema=_build_list_response_schema(aggregate),
            tags=[aggregate.name]
        ))
        
        # GET single
        endpoints.append(ContractEndpoint(
            path=f"{base_path}/{{id}}",
            method="GET",
            operation_id=f"get{aggregate.name}ById",
            summary=f"Get {aggregate.name} by ID",
            response_schema=_build_entity_schema(aggregate),
            tags=[aggregate.name]
        ))
        
        # POST create
        endpoints.append(ContractEndpoint(
            path=base_path,
            method="POST",
            operation_id=f"create{aggregate.name}",
            summary=f"Create new {aggregate.name}",
            request_schema=_build_create_request_schema(aggregate),
            response_schema=_build_entity_schema(aggregate),
            tags=[aggregate.name]
        ))
        
        # Behavior endpoints
        for behavior in aggregate.behaviors:
            if behavior.lower() in ["create", "update", "delete", "get"]:
                continue  # Skip CRUD - already covered
            
            behavior_kebab = _pascal_to_kebab(behavior)
            endpoints.append(ContractEndpoint(
                path=f"{base_path}/{{id}}/{behavior_kebab}",
                method="POST",
                operation_id=f"{behavior.lower()}{aggregate.name}",
                summary=f"{behavior} {aggregate.name}",
                request_schema=_build_behavior_request_schema(aggregate, behavior),
                response_schema=_build_behavior_response_schema(aggregate, behavior),
                tags=[aggregate.name]
            ))
        
        # Add schemas
        schemas[aggregate.name] = _build_entity_schema(aggregate)
        schemas[f"Create{aggregate.name}Request"] = _build_create_request_schema(aggregate)
    
    return ContractDefinition(
        name=f"{domain_model.name}Api",
        version=api_version,
        description=f"API for {domain_model.name}. " + domain_model.description,
        endpoints=endpoints,
        schemas=schemas
    )


def _pascal_to_kebab(name: str) -> str:
    """Convert PascalCase to kebab-case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def _build_entity_schema(aggregate: DomainAggregate) -> dict[str, Any]:
    """Build JSON schema for an entity."""
    properties = {
        "id": {"type": "string", "format": "uuid"}
    }
    required = ["id"]
    
    for prop in aggregate.properties:
        json_type = _dotnet_to_json_type(prop.type_name)
        properties[_camel_case(prop.name)] = {
            "type": json_type,
            "description": prop.description
        }
        if prop.is_required:
            required.append(_camel_case(prop.name))
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }


def _build_list_response_schema(aggregate: DomainAggregate) -> dict[str, Any]:
    """Build JSON schema for list response."""
    return {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {"$ref": f"#/components/schemas/{aggregate.name}"}
            },
            "total": {"type": "integer"},
            "page": {"type": "integer"},
            "pageSize": {"type": "integer"}
        }
    }


def _build_create_request_schema(aggregate: DomainAggregate) -> dict[str, Any]:
    """Build JSON schema for create request."""
    properties = {}
    required = []
    
    for prop in aggregate.properties:
        if prop.name.lower() in ["id", "createdat", "updatedat"]:
            continue  # Skip auto-generated fields
        
        json_type = _dotnet_to_json_type(prop.type_name)
        properties[_camel_case(prop.name)] = {
            "type": json_type,
            "description": prop.description
        }
        if prop.is_required:
            required.append(_camel_case(prop.name))
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }


def _build_behavior_request_schema(aggregate: DomainAggregate, behavior: str) -> dict[str, Any]:
    """Build JSON schema for behavior request."""
    return {
        "type": "object",
        "properties": {
            "id": {"type": "string", "format": "uuid", "description": f"{aggregate.name} ID"},
            "reason": {"type": "string", "description": f"Reason for {behavior}"},
        },
        "required": ["id"]
    }


def _build_behavior_response_schema(aggregate: DomainAggregate, behavior: str) -> dict[str, Any]:
    """Build JSON schema for behavior response."""
    return {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "message": {"type": "string"},
            f"{_camel_case(aggregate.name)}Id": {"type": "string", "format": "uuid"},
            "timestamp": {"type": "string", "format": "date-time"}
        }
    }


def _dotnet_to_json_type(dotnet_type: str) -> str:
    """Convert .NET type to JSON Schema type."""
    type_map = {
        "string": "string",
        "int": "integer",
        "long": "integer",
        "decimal": "number",
        "double": "number",
        "float": "number",
        "bool": "boolean",
        "boolean": "boolean",
        "Guid": "string",
        "DateTime": "string",
        "DateTimeOffset": "string",
    }
    # Handle nullable types
    base_type = dotnet_type.rstrip("?")
    return type_map.get(base_type, "string")


def _camel_case(name: str) -> str:
    """Convert PascalCase to camelCase."""
    if not name:
        return name
    return name[0].lower() + name[1:]


# ============================================================================
# PHASE 4: CQRS COMMANDS/QUERIES FROM DOMAIN
# ============================================================================

def generate_commands_from_aggregate(aggregate: DomainAggregate) -> list[Command]:
    """Generate CQRS commands from aggregate behaviors."""
    commands: list[Command] = []
    
    for behavior in aggregate.behaviors:
        # Skip query-like behaviors
        if behavior.lower().startswith(("get", "find", "search", "list")):
            continue
        
        cmd = Command(
            name=f"{behavior}{aggregate.name}Command",
            properties=[
                (f"{aggregate.name}Id", "Guid"),
            ] + [
                (prop.name, prop.type_name)
                for prop in aggregate.properties[:3]  # Limit properties
                if prop.name.lower() not in ["id", "createdat", "updatedat"]
            ],
            returns="Unit",
            aggregate=aggregate.name
        )
        commands.append(cmd)
    
    return commands


def generate_queries_from_aggregate(aggregate: DomainAggregate) -> list[Query]:
    """Generate CQRS queries from aggregate."""
    queries: list[Query] = []
    
    # Get by ID query
    queries.append(Query(
        name=f"Get{aggregate.name}ByIdQuery",
        properties=[("Id", "Guid")],
        returns=f"{aggregate.name}Dto"
    ))
    
    # List query
    queries.append(Query(
        name=f"Get{aggregate.name}ListQuery",
        properties=[("Page", "int"), ("PageSize", "int")],
        returns=f"PagedResult<{aggregate.name}Dto>"
    ))
    
    return queries


# ============================================================================
# ORCHESTRATION
# ============================================================================

@dataclass
class DDDGenerationResult:
    """Result of DDD-first generation."""
    domain_model: DomainModel
    gherkin_features: list[GherkinFeature]
    contract: ContractDefinition
    commands: list[Command]
    queries: list[Query]
    entities: list[DomainEntity]
    
    # Paths where files were written
    domain_model_path: Path | None = None
    gherkin_paths: list[Path] = field(default_factory=list)
    contract_path: Path | None = None


def run_ddd_first_generation(
    analyses: list[SliceAnalysis],
    solution_name: str,
    output_root: Path,
    llm_config: LLMConfig | None = None,
    use_llm: bool = True,
    phase: str = "domain",
) -> DDDGenerationResult:
    """
    Run DDD-first generation pipeline with phase control.
    
    Phases (cumulative, each includes prior phases):
    - "domain": Build domain model only (Phase 1)
    - "gherkin": Build domain model + generate Gherkin (Phases 1-2)  
    - "contract": Build domain model + Gherkin + contract (Phases 1-3)
    - "all": Complete pipeline including CQRS (Phases 1-4)
    
    1. Build domain model from slice analyses (using LLM if configured)
    2. Generate Gherkin/BDD from domain model
    3. Generate API contract from domain model
    4. Prepare CQRS commands/queries for implementation
    
    Args:
        analyses: Pre-analyzed slices (can be empty if use_llm=True and raw data provided)
        solution_name: Name of the solution
        output_root: Output directory for generated artifacts
        llm_config: LLM configuration (if None, uses defaults)
        use_llm: Whether to use LLM for domain model generation
        phase: Which phase to run up to: "domain", "gherkin", "contract", or "all"
    """
    LOGGER.info("Starting DDD-first generation for %s (use_llm=%s, phase=%s)", solution_name, use_llm, phase)
    
    # Initialize result containers
    gherkin_features: list[GherkinFeature] = []
    contract: ContractDefinition | None = None
    commands: list[Command] = []
    queries: list[Query] = []
    entities: list[DomainEntity] = []
    
    # Phase 1: Build Domain Model (always run)
    LOGGER.info("Phase 1: Building domain model...")
    if use_llm and llm_config and llm_config.provider != "none":
        domain_model = build_domain_model_with_llm(analyses, solution_name, llm_config)
    else:
        domain_model = build_domain_model_from_slices(analyses, solution_name)
    
    # Write domain model immediately
    domain_output = output_root / "domain"
    domain_output.mkdir(parents=True, exist_ok=True)
    domain_model_path = _write_domain_model(domain_model, domain_output)
    
    # Empty contract placeholder for early phases
    empty_contract = ContractDefinition(
        name=f"{solution_name}Api",
        version="1.0.0",
        description=f"API contract for {solution_name} (pending domain review)"
    )
    
    # Stop here if phase is "domain"
    if phase == "domain":
        LOGGER.info("Phase 1 complete. Domain model written to: %s", domain_model_path)
        LOGGER.info("Next: Review domain model, then run with --phase gherkin")
        return DDDGenerationResult(
            domain_model=domain_model,
            gherkin_features=[],
            contract=empty_contract,
            commands=[],
            queries=[],
            entities=[],
            domain_model_path=domain_model_path,
        )
    
    # Phase 2: Generate Gherkin/BDD
    LOGGER.info("Phase 2: Generating Gherkin/BDD specifications...")
    gherkin_features = generate_gherkin_from_domain_model(domain_model)
    
    # Write Gherkin features
    gherkin_output = output_root / "features"
    gherkin_output.mkdir(parents=True, exist_ok=True)
    gherkin_paths: list[Path] = []
    for feature in gherkin_features:
        feature_path = gherkin_output / f"{feature.name.replace(' ', '_')}.feature"
        feature_path.write_text(feature.render(), encoding="utf-8")
        gherkin_paths.append(feature_path)
    
    # Stop here if phase is "gherkin"
    if phase == "gherkin":
        LOGGER.info("Phase 2 complete. Gherkin features: %d files", len(gherkin_paths))
        LOGGER.info("Next: Review Gherkin specs, then run with --phase contract")
        return DDDGenerationResult(
            domain_model=domain_model,
            gherkin_features=gherkin_features,
            contract=ContractDefinition(name=f"{solution_name}Api", version="1.0.0", description="Pending contract generation"),
            commands=[],
            queries=[],
            entities=[],
            domain_model_path=domain_model_path,
            gherkin_paths=gherkin_paths,
        )
    
    # Phase 3: Generate Contract
    LOGGER.info("Phase 3: Generating API contract...")
    contract = generate_contract_from_domain_model(domain_model)
    
    # Write contract
    contract_output = output_root / "contracts"
    contract_output.mkdir(parents=True, exist_ok=True)
    contract_path = _write_contract(contract, contract_output)
    
    # Stop here if phase is "contract"
    if phase == "contract":
        LOGGER.info("Phase 3 complete. Contract written to: %s", contract_path)
        LOGGER.info("Next: Review contract, then run with --phase all")
        return DDDGenerationResult(
            domain_model=domain_model,
            gherkin_features=gherkin_features,
            contract=contract,
            commands=[],
            queries=[],
            entities=[],
            domain_model_path=domain_model_path,
            gherkin_paths=gherkin_paths,
            contract_path=contract_path,
        )
    
    # Phase 4: Generate CQRS Commands/Queries (phase == "all")
    LOGGER.info("Phase 4: Generating CQRS commands and queries...")
    
    for aggregate in domain_model.aggregates:
        commands.extend(generate_commands_from_aggregate(aggregate))
        queries.extend(generate_queries_from_aggregate(aggregate))
        entities.append(aggregate.to_entity())
    
    # Build final result - files already written in earlier phases
    result = DDDGenerationResult(
        domain_model=domain_model,
        gherkin_features=gherkin_features,
        contract=contract,
        commands=commands,
        queries=queries,
        entities=entities,
        domain_model_path=domain_model_path,
        gherkin_paths=gherkin_paths,
        contract_path=contract_path,
    )
    
    LOGGER.info("DDD-first generation complete:")
    LOGGER.info("  - Domain model: %s", result.domain_model_path)
    LOGGER.info("  - Gherkin features: %d files", len(result.gherkin_paths))
    LOGGER.info("  - Contract: %s", result.contract_path)
    LOGGER.info("  - Commands: %d", len(commands))
    LOGGER.info("  - Queries: %d", len(queries))
    
    return result


def _write_domain_model(domain_model: DomainModel, output_dir: Path) -> Path:
    """Write domain model documentation."""
    path = output_dir / f"{domain_model.name}_domain.md"
    
    lines = [
        f"# {domain_model.name} Domain Model",
        "",
        domain_model.description,
        "",
        "## Aggregates",
        ""
    ]
    
    for agg in domain_model.aggregates:
        lines.append(f"### {agg.name}")
        lines.append("")
        lines.append(f"**Description:** {agg.description}")
        lines.append("")
        
        if agg.properties:
            lines.append("**Properties:**")
            for prop in agg.properties:
                req = " (required)" if prop.is_required else ""
                lines.append(f"- `{prop.name}`: {prop.type_name}{req} - {prop.description}")
            lines.append("")
        
        if agg.behaviors:
            lines.append("**Behaviors:**")
            for behavior in agg.behaviors:
                lines.append(f"- {behavior}")
            lines.append("")
        
        if agg.domain_events:
            lines.append("**Domain Events:**")
            for event in agg.domain_events:
                lines.append(f"- {event.name}")
            lines.append("")
        
        if agg.invariants:
            lines.append("**Invariants:**")
            for inv in agg.invariants:
                lines.append(f"- {inv}")
            lines.append("")
    
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _write_contract(contract: ContractDefinition, output_dir: Path) -> Path:
    """Write contract files."""
    import json
    
    # Write OpenAPI JSON
    openapi_path = output_dir / f"{contract.name}.openapi.json"
    openapi_path.write_text(json.dumps(contract.to_openapi(), indent=2), encoding="utf-8")
    
    # Write human-readable summary
    summary_path = output_dir / f"{contract.name}.contract.md"
    lines = [
        f"# {contract.name} API Contract",
        "",
        f"**Version:** {contract.version}",
        f"**Description:** {contract.description}",
        "",
        "## Endpoints",
        ""
    ]
    
    for ep in contract.endpoints:
        lines.append(f"### {ep.method} `{ep.path}`")
        lines.append(f"**Operation ID:** `{ep.operation_id}`")
        lines.append(f"**Summary:** {ep.summary}")
        lines.append("")
    
    lines.extend([
        "---",
        "",
        "**VERIFICATION REQUIRED**",
        "",
        "Please review this contract before proceeding to code generation.",
    ])
    
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    
    return openapi_path
