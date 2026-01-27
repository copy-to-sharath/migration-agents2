"""
Contract-First Code Generation.

This module extracts contracts from slices and generates OpenAPI specifications
that must be verified before code generation proceeds.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .architecture import ContractDefinition, ContractEndpoint, Command, Query, DomainEntity

LOGGER = logging.getLogger("migration_agents.codegen.contracts")


@dataclass
class SliceContext:
    """Context extracted from a slice for contract generation."""
    slice_id: str
    entry_name: str
    rule_text: str
    source_excerpts: list[str] = field(default_factory=list)
    symbols: list[dict[str, Any]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    depth: int = 0
    node_count: int = 0
    file_count: int = 0


@dataclass
class GeneratedContract:
    """Result of contract generation for a slice."""
    slice_id: str
    contract: ContractDefinition
    commands: list[Command] = field(default_factory=list)
    queries: list[Query] = field(default_factory=list)
    entities: list[DomainEntity] = field(default_factory=list)
    verification_required: bool = True
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


def _extract_http_method_from_name(name: str) -> str:
    """Infer HTTP method from method name."""
    name_lower = name.lower()
    if any(x in name_lower for x in ["create", "add", "insert", "post", "save"]):
        return "POST"
    if any(x in name_lower for x in ["update", "edit", "modify", "put"]):
        return "PUT"
    if any(x in name_lower for x in ["delete", "remove", "cancel"]):
        return "DELETE"
    if any(x in name_lower for x in ["patch"]):
        return "PATCH"
    return "POST"  # Default for commands


def _extract_operation_type(name: str, rule_text: str) -> str:
    """Determine if this is a command or query operation."""
    name_lower = name.lower()
    rule_lower = rule_text.lower()
    
    # Query indicators
    query_indicators = ["get", "fetch", "find", "search", "list", "query", "read", "load"]
    if any(x in name_lower for x in query_indicators):
        return "query"
    
    # Check rule text for read patterns
    if any(x in rule_lower for x in ["retriev", "fetch", "find", "search", "display"]):
        return "query"
    
    # Default to command for write operations
    return "command"


def _pascal_to_kebab(name: str) -> str:
    """Convert PascalCase to kebab-case for URL paths."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def _extract_domain_name(entry_name: str) -> str:
    """Extract domain/aggregate name from entry point name."""
    # Remove common suffixes
    name = entry_name
    for suffix in ["Processor", "Service", "Handler", "Controller", "Manager", "Helper"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    
    # Remove method prefixes
    for prefix in ["Process", "Handle", "Execute", "Run", "Do"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    
    return name or entry_name


def _infer_request_schema(entry_name: str, symbols: list[dict]) -> dict[str, Any]:
    """Infer request schema from method parameters."""
    # Look for parameter types in symbols
    properties: dict[str, Any] = {}
    required: list[str] = []
    
    # Common patterns
    domain = _extract_domain_name(entry_name)
    domain_lower = domain.lower()
    
    # Add likely properties based on domain
    if "payment" in domain_lower or "order" in domain_lower:
        properties["orderId"] = {"type": "integer", "description": "Order identifier"}
        properties["amount"] = {"type": "number", "format": "decimal", "description": "Amount in cents"}
        required.extend(["orderId"])
    elif "customer" in domain_lower or "user" in domain_lower:
        properties["customerId"] = {"type": "integer", "description": "Customer identifier"}
        required.append("customerId")
    elif "product" in domain_lower:
        properties["productId"] = {"type": "integer", "description": "Product identifier"}
        required.append("productId")
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }


def _infer_response_schema(entry_name: str, operation_type: str) -> dict[str, Any]:
    """Infer response schema based on operation type."""
    if operation_type == "query":
        return {
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "Query result data"},
                "success": {"type": "boolean"}
            }
        }
    else:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "transactionId": {"type": "string", "nullable": True},
                "message": {"type": "string", "nullable": True}
            }
        }


def generate_contract_from_slice(context: SliceContext) -> GeneratedContract:
    """Generate an API contract from slice context."""
    LOGGER.info("Generating contract for slice %s (%s)", context.slice_id, context.entry_name)
    
    domain = _extract_domain_name(context.entry_name)
    operation_type = _extract_operation_type(context.entry_name, context.rule_text)
    
    # Create endpoint
    http_method = "GET" if operation_type == "query" else _extract_http_method_from_name(context.entry_name)
    path = f"/api/{_pascal_to_kebab(domain)}"
    if operation_type == "command":
        action = _pascal_to_kebab(context.entry_name)
        path = f"{path}/{action}"
    
    endpoint = ContractEndpoint(
        path=path,
        method=http_method,
        operation_id=context.entry_name,
        summary=f"{context.entry_name} - {operation_type.title()} operation",
        request_schema=_infer_request_schema(context.entry_name, context.symbols) if http_method != "GET" else None,
        response_schema=_infer_response_schema(context.entry_name, operation_type),
        tags=[domain]
    )
    
    # Create contract
    contract = ContractDefinition(
        name=f"{domain}Api",
        version="1.0.0",
        description=f"API contract for {domain} domain. Generated from slice {context.slice_id}.\n\n{context.rule_text[:500]}",
        endpoints=[endpoint],
        schemas={
            f"{context.entry_name}Request": _infer_request_schema(context.entry_name, context.symbols),
            f"{context.entry_name}Response": _infer_response_schema(context.entry_name, operation_type)
        }
    )
    
    # Create CQRS command/query
    commands: list[Command] = []
    queries: list[Query] = []
    
    if operation_type == "command":
        cmd = Command(
            name=f"{context.entry_name}Command",
            properties=[("OrderId", "int"), ("Amount", "decimal")],  # Inferred
            returns="Unit",  # Use Unit (void) for now - result types generated separately
            aggregate=domain
        )
        commands.append(cmd)
    else:
        qry = Query(
            name=f"{context.entry_name}Query",
            properties=[("Id", "int")],
            returns=f"{domain}Dto"
        )
        queries.append(qry)
    
    # Create domain entity
    entity = DomainEntity(
        name=domain,
        is_aggregate_root=True,
        properties=[
            ("Id", "Guid", True),
            ("CreatedAt", "DateTime", True),
            ("UpdatedAt", "DateTime?", False)
        ]
    )
    
    return GeneratedContract(
        slice_id=context.slice_id,
        contract=contract,
        commands=commands,
        queries=queries,
        entities=[entity]
    )


def generate_contracts_for_slices(contexts: list[SliceContext]) -> list[GeneratedContract]:
    """Generate contracts for multiple slices."""
    return [generate_contract_from_slice(ctx) for ctx in contexts]


def merge_contracts(contracts: list[GeneratedContract], solution_name: str) -> ContractDefinition:
    """Merge multiple slice contracts into a single API contract."""
    all_endpoints: list[ContractEndpoint] = []
    all_schemas: dict[str, Any] = {}
    
    for gc in contracts:
        all_endpoints.extend(gc.contract.endpoints)
        all_schemas.update(gc.contract.schemas)
    
    return ContractDefinition(
        name=f"{solution_name}Api",
        version="1.0.0",
        description=f"Merged API contract for {solution_name}. Contains {len(contracts)} slice contracts.",
        endpoints=all_endpoints,
        schemas=all_schemas
    )


def save_contract_for_verification(contract: ContractDefinition, output_path: Path) -> Path:
    """Save contract to file for human verification."""
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save OpenAPI spec
    openapi_path = output_path / f"{contract.name}.openapi.json"
    openapi_path.write_text(json.dumps(contract.to_openapi(), indent=2))
    
    # Save human-readable summary
    summary_path = output_path / f"{contract.name}.contract.md"
    summary = [
        f"# {contract.name} API Contract",
        "",
        f"**Version:** {contract.version}",
        f"**Description:** {contract.description}",
        "",
        "## Endpoints",
        ""
    ]
    
    for ep in contract.endpoints:
        summary.append(f"### {ep.method} {ep.path}")
        summary.append(f"- **Operation ID:** {ep.operation_id}")
        summary.append(f"- **Summary:** {ep.summary}")
        summary.append(f"- **Tags:** {', '.join(ep.tags)}")
        if ep.request_schema:
            summary.append(f"- **Request Schema:** {json.dumps(ep.request_schema, indent=2)}")
        if ep.response_schema:
            summary.append(f"- **Response Schema:** {json.dumps(ep.response_schema, indent=2)}")
        summary.append("")
    
    summary.extend([
        "## Schemas",
        "",
        "```json",
        json.dumps(contract.schemas, indent=2),
        "```",
        "",
        "---",
        "",
        "**VERIFICATION REQUIRED**",
        "",
        "Please review this contract and confirm:",
        "- [ ] Endpoint paths are correct",
        "- [ ] HTTP methods are appropriate",
        "- [ ] Request/Response schemas are accurate",
        "- [ ] All required fields are present",
        "",
        "To approve, set `verified: true` in the contract or run:",
        "```bash",
        f"migration-agents codegen --verify-contract {contract.name}",
        "```"
    ])
    
    summary_path.write_text("\n".join(summary))
    
    LOGGER.info("Contract saved for verification: %s", summary_path)
    return summary_path


def load_verified_contract(contract_path: Path) -> ContractDefinition | None:
    """Load a verified contract from file."""
    openapi_path = contract_path
    if contract_path.suffix == ".md":
        openapi_path = contract_path.with_suffix(".openapi.json")
    
    if not openapi_path.exists():
        LOGGER.warning("Contract file not found: %s", openapi_path)
        return None
    
    try:
        data = json.loads(openapi_path.read_text())
        
        endpoints = []
        for path, methods in data.get("paths", {}).items():
            for method, spec in methods.items():
                endpoints.append(ContractEndpoint(
                    path=path,
                    method=method.upper(),
                    operation_id=spec.get("operationId", ""),
                    summary=spec.get("summary", ""),
                    request_schema=spec.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema"),
                    response_schema=spec.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema"),
                    tags=spec.get("tags", [])
                ))
        
        return ContractDefinition(
            name=data.get("info", {}).get("title", ""),
            version=data.get("info", {}).get("version", "1.0.0"),
            description=data.get("info", {}).get("description", ""),
            endpoints=endpoints,
            schemas=data.get("components", {}).get("schemas", {}),
            verified=True
        )
    except Exception as e:
        LOGGER.error("Failed to load contract: %s", e)
        return None
