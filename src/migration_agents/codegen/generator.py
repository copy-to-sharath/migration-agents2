"""
Unified Solution Generator.

Generates a single Clean Architecture solution from multiple slices,
following SOLID principles, DDD, BDD, and CQRS patterns.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from .architecture import (
    CleanArchitectureSolution,
    ContractDefinition,
    Command,
    Query,
    DomainEntity,
    solution_file,
    domain_csproj,
    application_csproj,
    infrastructure_csproj,
    api_csproj,
    tests_csproj,
    entity_base_cs,
    aggregate_root_cs,
    value_object_cs,
    domain_event_cs,
    result_cs,
    command_interface_cs,
    query_interface_cs,
    dependency_injection_cs,
    program_cs,
    controller_base_cs,
    infrastructure_di_cs,
    feature_file_bdd,
    steps_file_bdd,
    web_factory_cs,
)
from .contracts import GeneratedContract

LOGGER = logging.getLogger("migration_agents.codegen.generator")


def _write_file(path: Path, content: str) -> None:
    """Write content to file, creating directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    LOGGER.debug("Written: %s", path)


def _generate_domain_entity_cs(namespace: str, entity: DomainEntity) -> str:
    """Generate a domain entity class."""
    # Filter out Id since it's inherited from base class
    props = []
    for name, type_, required in entity.properties:
        if name == "Id":
            continue  # Skip - inherited from Entity<TId>
        # Add default! for reference types to avoid nullable warnings
        suffix = " = default!;" if type_ == "string" else ""
        props.append(f"    public {type_} {name} {{ get; private set; }}{suffix}")
    
    base_class = "AggregateRoot<Guid>" if entity.is_aggregate_root else "Entity<Guid>"
    
    events = ""
    if entity.domain_events:
        events = "\n\n    // Domain Events\n" + "\n".join(
            f"    public void Raise{evt}() => AddDomainEvent(new {evt}());"
            for evt in entity.domain_events
        )
    
    return f"""using {namespace}.Domain.Common;

namespace {namespace}.Domain.Entities;

/// <summary>
/// {entity.name} aggregate{"" if not entity.is_aggregate_root else " root"}.
/// </summary>
public class {entity.name} : {base_class}
{{
{chr(10).join(props)}

    private {entity.name}() {{ }} // EF Core

    public static {entity.name} Create()
    {{
        return new {entity.name}
        {{
            Id = Guid.NewGuid(),
            CreatedAt = DateTime.UtcNow
        }};
    }}{events}
}}
"""


def _generate_command_cs(namespace: str, command: Command) -> str:
    """Generate a CQRS command class."""
    props = "\n".join(
        f"    public {type_} {name} {{ get; init; }}"
        for name, type_ in command.properties
    )
    
    return_type = "ICommand" if command.returns == "Unit" else f"ICommand<{command.returns}>"
    
    return f"""using {namespace}.Application.Common.Interfaces;
using {namespace}.Domain.Common;

namespace {namespace}.Application.{command.aggregate}.Commands;

/// <summary>
/// Command: {command.name}
/// </summary>
public record {command.name}(
{','.join(f'    {t} {n}' for n, t in command.properties)}
) : {return_type};
"""


def _generate_command_handler_cs(namespace: str, command: Command) -> str:
    """Generate a CQRS command handler."""
    if command.returns == "Unit":
        return_type = "Result"
        handler_interface = f"ICommandHandler<{command.name}>"
    else:
        return_type = f"Result<{command.returns}>"
        handler_interface = f"ICommandHandler<{command.name}, {command.returns}>"
    
    return f"""using {namespace}.Application.Common.Interfaces;
using {namespace}.Domain.Common;
using Microsoft.Extensions.Logging;

namespace {namespace}.Application.{command.aggregate}.Commands;

/// <summary>
/// Handler for {command.name}
/// </summary>
public class {command.name}Handler : {handler_interface}
{{
    private readonly ILogger<{command.name}Handler> _logger;

    public {command.name}Handler(ILogger<{command.name}Handler> logger)
    {{
        _logger = logger;
    }}

    public async Task<{return_type}> Handle({command.name} request, CancellationToken cancellationToken)
    {{
        _logger.LogInformation("Handling {command.name}");
        
        try
        {{
            // TODO: Implement business logic
            // 1. Validate request
            // 2. Load aggregate from repository
            // 3. Execute domain operation
            // 4. Persist changes
            // 5. Return result
            
            await Task.CompletedTask;
            return Result.Success();
        }}
        catch (Exception ex)
        {{
            _logger.LogError(ex, "Error handling {command.name}");
            return Result.Failure(ex.Message);
        }}
    }}
}}
"""


def _generate_command_validator_cs(namespace: str, command: Command) -> str:
    """Generate FluentValidation validator for command."""
    rules = []
    for name, type_ in command.properties:
        if type_ in ("int", "long", "Guid"):
            rules.append(f'        RuleFor(x => x.{name}).NotEmpty().WithMessage("{name} is required");')
        elif type_ == "string":
            rules.append(f'        RuleFor(x => x.{name}).NotEmpty().MaximumLength(500);')
        elif type_ == "decimal":
            rules.append(f'        RuleFor(x => x.{name}).GreaterThan(0).WithMessage("{name} must be positive");')
    
    return f"""using FluentValidation;

namespace {namespace}.Application.{command.aggregate}.Commands;

public class {command.name}Validator : AbstractValidator<{command.name}>
{{
    public {command.name}Validator()
    {{
{chr(10).join(rules)}
    }}
}}
"""


def _generate_query_cs(namespace: str, query: Query) -> str:
    """Generate a CQRS query class."""
    return f"""using {namespace}.Application.Common.Interfaces;
using {namespace}.Domain.Common;

namespace {namespace}.Application.Queries;

/// <summary>
/// Query: {query.name}
/// </summary>
public record {query.name}(
{','.join(f'    {t} {n}' for n, t in query.properties)}
) : IQuery<{query.returns}>;
"""


def _generate_query_handler_cs(namespace: str, query: Query) -> str:
    """Generate a CQRS query handler."""
    return f"""using {namespace}.Application.Common.Interfaces;
using {namespace}.Domain.Common;
using Microsoft.Extensions.Logging;

namespace {namespace}.Application.Queries;

/// <summary>
/// Handler for {query.name}
/// </summary>
public class {query.name}Handler : IQueryHandler<{query.name}, {query.returns}>
{{
    private readonly ILogger<{query.name}Handler> _logger;

    public {query.name}Handler(ILogger<{query.name}Handler> logger)
    {{
        _logger = logger;
    }}

    public async Task<Result<{query.returns}>> Handle({query.name} request, CancellationToken cancellationToken)
    {{
        _logger.LogInformation("Handling {query.name}");
        
        try
        {{
            // TODO: Implement query logic
            await Task.CompletedTask;
            return Result<{query.returns}>.Failure("Not implemented");
        }}
        catch (Exception ex)
        {{
            _logger.LogError(ex, "Error handling {query.name}");
            return Result<{query.returns}>.Failure(ex.Message);
        }}
    }}
}}
"""


def _generate_controller_cs(namespace: str, contract: ContractDefinition) -> str:
    """Generate an API controller from contract."""
    # Group endpoints by tag (domain)
    tags = set()
    for ep in contract.endpoints:
        tags.update(ep.tags)
    
    controllers = []
    for tag in tags:
        endpoints = [ep for ep in contract.endpoints if tag in ep.tags]
        
        methods = []
        for ep in endpoints:
            method_attr = f"Http{ep.method.capitalize()}"
            route = ep.path.replace(f"/api/{tag.lower()}", "").lstrip("/") or ""
            route_attr = f'("{route}")' if route else ""
            
            # Determine command/query name
            op_name = ep.operation_id
            
            if ep.method in ("POST", "PUT", "DELETE", "PATCH"):
                # Command
                methods.append(f"""
    /// <summary>
    /// {ep.summary}
    /// </summary>
    [{method_attr}{route_attr}]
    [ProducesResponseType(typeof(Result), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> {op_name}([FromBody] {op_name}Command command)
    {{
        var result = await Mediator.Send(command);
        return result.IsSuccess ? Ok(result) : BadRequest(result);
    }}""")
            else:
                # Query
                methods.append(f"""
    /// <summary>
    /// {ep.summary}
    /// </summary>
    [{method_attr}{route_attr}]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> {op_name}([FromQuery] {op_name}Query query)
    {{
        var result = await Mediator.Send(query);
        return result.IsSuccess ? Ok(result.Value) : NotFound();
    }}""")
        
        controller = f"""using MediatR;
using Microsoft.AspNetCore.Mvc;
using {namespace}.Application.{tag}.Commands;
using {namespace}.Domain.Common;

namespace {namespace}.Api.Controllers;

/// <summary>
/// {tag} API Controller
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class {tag}Controller : ApiControllerBase
{{{"".join(methods)}
}}
"""
        controllers.append((tag, controller))
    
    return controllers


def generate_clean_architecture_solution(
    solution_name: str,
    namespace: str,
    contracts: list[GeneratedContract],
    output_root: Path,
) -> list[dict[str, Any]]:
    """Generate a complete Clean Architecture solution."""
    LOGGER.info("Generating Clean Architecture solution: %s", solution_name)
    
    # Merge all contracts, commands, queries, entities
    all_commands: list[Command] = []
    all_queries: list[Query] = []
    all_entities: list[DomainEntity] = []
    all_endpoints = []
    all_schemas = {}
    
    for gc in contracts:
        all_commands.extend(gc.commands)
        all_queries.extend(gc.queries)
        all_entities.extend(gc.entities)
        all_endpoints.extend(gc.contract.endpoints)
        all_schemas.update(gc.contract.schemas)
    
    merged_contract = ContractDefinition(
        name=f"{solution_name}Api",
        version="1.0.0",
        description=f"API for {solution_name}",
        endpoints=all_endpoints,
        schemas=all_schemas
    )
    
    solution = CleanArchitectureSolution(
        name=solution_name,
        namespace=namespace,
        contract=merged_contract,
        entities=all_entities,
        commands=all_commands,
        queries=all_queries
    )
    
    # Output paths
    root = output_root / solution_name
    domain_root = root / "src" / f"{solution_name}.Domain"
    app_root = root / "src" / f"{solution_name}.Application"
    infra_root = root / "src" / f"{solution_name}.Infrastructure"
    api_root = root / "src" / f"{solution_name}.Api"
    tests_root = root / "tests" / f"{solution_name}.Tests"
    
    manifest: list[dict[str, Any]] = []
    
    # ========== Solution File ==========
    sln_path = root / f"{solution_name}.sln"
    _write_file(sln_path, solution_file(solution))
    manifest.append({"path": str(sln_path), "kind": "solution", "layer": "root"})
    
    # ========== Domain Layer ==========
    _write_file(domain_root / f"{solution_name}.Domain.csproj", domain_csproj(solution_name))
    _write_file(domain_root / "Common" / "Entity.cs", entity_base_cs(namespace))
    _write_file(domain_root / "Common" / "AggregateRoot.cs", aggregate_root_cs(namespace))
    _write_file(domain_root / "Common" / "ValueObject.cs", value_object_cs(namespace))
    _write_file(domain_root / "Common" / "IDomainEvent.cs", domain_event_cs(namespace))
    _write_file(domain_root / "Common" / "Result.cs", result_cs(namespace))
    
    manifest.append({"path": str(domain_root / f"{solution_name}.Domain.csproj"), "kind": "csproj", "layer": "domain"})
    
    # Generate entities
    for entity in all_entities:
        entity_path = domain_root / "Entities" / f"{entity.name}.cs"
        _write_file(entity_path, _generate_domain_entity_cs(namespace, entity))
        manifest.append({"path": str(entity_path), "kind": "entity", "layer": "domain", "name": entity.name})
    
    # ========== Application Layer (CQRS) ==========
    _write_file(app_root / f"{solution_name}.Application.csproj", application_csproj(solution_name))
    _write_file(app_root / "Common" / "Interfaces" / "ICommand.cs", command_interface_cs(namespace))
    _write_file(app_root / "Common" / "Interfaces" / "IQuery.cs", query_interface_cs(namespace))
    _write_file(app_root / "DependencyInjection.cs", dependency_injection_cs(namespace))
    
    manifest.append({"path": str(app_root / f"{solution_name}.Application.csproj"), "kind": "csproj", "layer": "application"})
    
    # Generate commands and handlers
    for cmd in all_commands:
        cmd_folder = app_root / cmd.aggregate / "Commands"
        _write_file(cmd_folder / f"{cmd.name}.cs", _generate_command_cs(namespace, cmd))
        _write_file(cmd_folder / f"{cmd.name}Handler.cs", _generate_command_handler_cs(namespace, cmd))
        _write_file(cmd_folder / f"{cmd.name}Validator.cs", _generate_command_validator_cs(namespace, cmd))
        manifest.append({"path": str(cmd_folder / f"{cmd.name}.cs"), "kind": "command", "layer": "application", "name": cmd.name})
        manifest.append({"path": str(cmd_folder / f"{cmd.name}Handler.cs"), "kind": "command_handler", "layer": "application", "name": cmd.name})
    
    # Generate queries and handlers
    for qry in all_queries:
        qry_folder = app_root / "Queries"
        _write_file(qry_folder / f"{qry.name}.cs", _generate_query_cs(namespace, qry))
        _write_file(qry_folder / f"{qry.name}Handler.cs", _generate_query_handler_cs(namespace, qry))
        manifest.append({"path": str(qry_folder / f"{qry.name}.cs"), "kind": "query", "layer": "application", "name": qry.name})
    
    # ========== Infrastructure Layer ==========
    _write_file(infra_root / f"{solution_name}.Infrastructure.csproj", infrastructure_csproj(solution_name))
    _write_file(infra_root / "DependencyInjection.cs", infrastructure_di_cs(namespace))
    _write_file(infra_root / "Persistence" / ".gitkeep", "")
    _write_file(infra_root / "Persistence" / "Repositories" / ".gitkeep", "")
    
    manifest.append({"path": str(infra_root / f"{solution_name}.Infrastructure.csproj"), "kind": "csproj", "layer": "infrastructure"})
    
    # ========== API Layer ==========
    _write_file(api_root / f"{solution_name}.Api.csproj", api_csproj(solution_name))
    _write_file(api_root / "Program.cs", program_cs(namespace, solution_name))
    _write_file(api_root / "Controllers" / "ApiControllerBase.cs", controller_base_cs(namespace))
    
    manifest.append({"path": str(api_root / f"{solution_name}.Api.csproj"), "kind": "csproj", "layer": "api"})
    manifest.append({"path": str(api_root / "Program.cs"), "kind": "program", "layer": "api"})
    
    # Generate controllers
    controllers = _generate_controller_cs(namespace, merged_contract)
    for tag, controller_code in controllers:
        controller_path = api_root / "Controllers" / f"{tag}Controller.cs"
        _write_file(controller_path, controller_code)
        manifest.append({"path": str(controller_path), "kind": "controller", "layer": "api", "name": tag})
    
    # Save OpenAPI spec
    openapi_path = api_root / "openapi.json"
    _write_file(openapi_path, json.dumps(merged_contract.to_openapi(), indent=2))
    manifest.append({"path": str(openapi_path), "kind": "openapi", "layer": "api"})
    
    # ========== Tests Layer (BDD) ==========
    _write_file(tests_root / f"{solution_name}.Tests.csproj", tests_csproj(solution_name))
    _write_file(tests_root / "CustomWebApplicationFactory.cs", web_factory_cs(namespace))
    
    manifest.append({"path": str(tests_root / f"{solution_name}.Tests.csproj"), "kind": "csproj", "layer": "tests"})
    
    # Generate BDD features for each command
    for cmd in all_commands:
        feature_name = cmd.name.replace("Command", "")
        scenarios = [(f"Execute {feature_name}", f"the {feature_name} operation is executed")]
        
        feature_path = tests_root / "Features" / f"{feature_name}.feature"
        _write_file(feature_path, feature_file_bdd(feature_name, scenarios))
        
        steps_path = tests_root / "Steps" / f"{feature_name}Steps.cs"
        _write_file(steps_path, steps_file_bdd(f"{namespace}.Tests", feature_name))
        
        manifest.append({"path": str(feature_path), "kind": "feature", "layer": "tests", "name": feature_name})
        manifest.append({"path": str(steps_path), "kind": "steps", "layer": "tests", "name": feature_name})
    
    LOGGER.info("Generated %d files for %s", len(manifest), solution_name)
    return manifest
