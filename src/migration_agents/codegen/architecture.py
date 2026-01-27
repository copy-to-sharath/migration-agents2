"""
Clean Architecture + DDD + CQRS code generation patterns.

This module provides templates and structure for generating code following:
- Clean Architecture (Domain, Application, Infrastructure, API layers)
- SOLID principles
- Domain-Driven Design (Aggregates, Value Objects, Domain Events)
- Behavior-Driven Development (Reqnroll/Gherkin)
- CQRS pattern (Commands/Queries with MediatR)
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Layer(Enum):
    DOMAIN = "Domain"
    APPLICATION = "Application"
    INFRASTRUCTURE = "Infrastructure"
    API = "Api"
    TESTS = "Tests"


@dataclass
class ContractEndpoint:
    """Represents an API endpoint contract."""
    path: str
    method: str  # GET, POST, PUT, DELETE, PATCH
    operation_id: str
    summary: str
    request_schema: dict[str, Any] | None = None
    response_schema: dict[str, Any] | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class ContractDefinition:
    """OpenAPI contract definition for verification."""
    name: str
    version: str
    description: str
    endpoints: list[ContractEndpoint] = field(default_factory=list)
    schemas: dict[str, Any] = field(default_factory=dict)
    verified: bool = False
    verification_notes: str = ""
    
    def to_openapi(self) -> dict[str, Any]:
        """Generate OpenAPI 3.0 specification."""
        paths: dict[str, Any] = {}
        for ep in self.endpoints:
            if ep.path not in paths:
                paths[ep.path] = {}
            paths[ep.path][ep.method.lower()] = {
                "operationId": ep.operation_id,
                "summary": ep.summary,
                "tags": ep.tags,
                "responses": {
                    "200": {
                        "description": "Success",
                        "content": {
                            "application/json": {
                                "schema": ep.response_schema or {"type": "object"}
                            }
                        }
                    }
                }
            }
            if ep.request_schema:
                paths[ep.path][ep.method.lower()]["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": ep.request_schema
                        }
                    }
                }
        
        return {
            "openapi": "3.0.3",
            "info": {
                "title": self.name,
                "version": self.version,
                "description": self.description,
            },
            "paths": paths,
            "components": {
                "schemas": self.schemas
            }
        }


@dataclass 
class DomainEntity:
    """Represents a DDD Entity or Aggregate Root."""
    name: str
    is_aggregate_root: bool = False
    properties: list[tuple[str, str, bool]] = field(default_factory=list)  # (name, type, required)
    value_objects: list[str] = field(default_factory=list)
    domain_events: list[str] = field(default_factory=list)


@dataclass
class Command:
    """CQRS Command definition."""
    name: str
    properties: list[tuple[str, str]] = field(default_factory=list)  # (name, type)
    returns: str = "Unit"
    aggregate: str = ""


@dataclass
class Query:
    """CQRS Query definition."""
    name: str
    properties: list[tuple[str, str]] = field(default_factory=list)  # (name, type)
    returns: str = ""


@dataclass
class CleanArchitectureSolution:
    """Complete Clean Architecture solution structure."""
    name: str
    namespace: str
    contract: ContractDefinition
    entities: list[DomainEntity] = field(default_factory=list)
    commands: list[Command] = field(default_factory=list)
    queries: list[Query] = field(default_factory=list)
    
    # GUIDs for solution file
    domain_guid: str = field(default_factory=lambda: str(uuid.uuid4()))
    application_guid: str = field(default_factory=lambda: str(uuid.uuid4()))
    infrastructure_guid: str = field(default_factory=lambda: str(uuid.uuid4()))
    api_guid: str = field(default_factory=lambda: str(uuid.uuid4()))
    tests_guid: str = field(default_factory=lambda: str(uuid.uuid4()))


# ========== TEMPLATE GENERATORS ==========

def solution_file(sol: CleanArchitectureSolution) -> str:
    """Generate Visual Studio solution file."""
    return f"""
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.8.34330.188
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{sol.name}.Domain", "src\\{sol.name}.Domain\\{sol.name}.Domain.csproj", "{{{sol.domain_guid}}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{sol.name}.Application", "src\\{sol.name}.Application\\{sol.name}.Application.csproj", "{{{sol.application_guid}}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{sol.name}.Infrastructure", "src\\{sol.name}.Infrastructure\\{sol.name}.Infrastructure.csproj", "{{{sol.infrastructure_guid}}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{sol.name}.Api", "src\\{sol.name}.Api\\{sol.name}.Api.csproj", "{{{sol.api_guid}}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{sol.name}.Tests", "tests\\{sol.name}.Tests\\{sol.name}.Tests.csproj", "{{{sol.tests_guid}}}"
EndProject
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|Any CPU = Debug|Any CPU
        Release|Any CPU = Release|Any CPU
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        {{{sol.domain_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{sol.domain_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{sol.domain_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {{{sol.domain_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU
        {{{sol.application_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{sol.application_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{sol.application_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {{{sol.application_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU
        {{{sol.infrastructure_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{sol.infrastructure_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{sol.infrastructure_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {{{sol.infrastructure_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU
        {{{sol.api_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{sol.api_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{sol.api_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {{{sol.api_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU
        {{{sol.tests_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{sol.tests_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{sol.tests_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {{{sol.tests_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU
    EndGlobalSection
EndGlobal
""".strip()


def domain_csproj(name: str) -> str:
    """Generate Domain layer project file."""
    return f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{name}.Domain</RootNamespace>
  </PropertyGroup>
</Project>"""


def application_csproj(name: str) -> str:
    """Generate Application layer project file with MediatR for CQRS."""
    return f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{name}.Application</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="MediatR" Version="12.2.0" />
    <PackageReference Include="FluentValidation" Version="11.9.0" />
    <PackageReference Include="FluentValidation.DependencyInjectionExtensions" Version="11.9.0" />
    <PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="8.0.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\\{name}.Domain\\{name}.Domain.csproj" />
  </ItemGroup>
</Project>"""


def infrastructure_csproj(name: str) -> str:
    """Generate Infrastructure layer project file."""
    return f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{name}.Infrastructure</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.1" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.1" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\\{name}.Application\\{name}.Application.csproj" />
  </ItemGroup>
</Project>"""


def api_csproj(name: str) -> str:
    """Generate API layer project file."""
    return f"""<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{name}.Api</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="8.0.1" />
    <PackageReference Include="MediatR" Version="12.2.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\\{name}.Application\\{name}.Application.csproj" />
    <ProjectReference Include="..\\{name}.Infrastructure\\{name}.Infrastructure.csproj" />
  </ItemGroup>
</Project>"""


def tests_csproj(name: str) -> str:
    """Generate Tests project file with BDD support."""
    return f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
    <RootNamespace>{name}.Tests</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.9.0" />
    <PackageReference Include="NUnit" Version="3.14.0" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Reqnroll" Version="2.0.0" />
    <PackageReference Include="Reqnroll.NUnit" Version="2.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.1" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\\..\\src\\{name}.Api\\{name}.Api.csproj" />
  </ItemGroup>
</Project>"""


# ========== DOMAIN LAYER TEMPLATES ==========

def entity_base_cs(namespace: str) -> str:
    """Generate base Entity class."""
    return f"""namespace {namespace}.Domain.Common;

/// <summary>
/// Base class for all domain entities.
/// </summary>
public abstract class Entity<TId> : IEquatable<Entity<TId>> where TId : notnull
{{
    public TId Id {{ get; protected set; }} = default!;
    public DateTime CreatedAt {{ get; protected set; }}
    public DateTime? UpdatedAt {{ get; protected set; }}
    
    private readonly List<IDomainEvent> _domainEvents = new();
    public IReadOnlyCollection<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    protected void AddDomainEvent(IDomainEvent domainEvent)
    {{
        _domainEvents.Add(domainEvent);
    }}

    public void ClearDomainEvents()
    {{
        _domainEvents.Clear();
    }}

    public bool Equals(Entity<TId>? other)
    {{
        if (other is null) return false;
        if (ReferenceEquals(this, other)) return true;
        return EqualityComparer<TId>.Default.Equals(Id, other.Id);
    }}

    public override bool Equals(object? obj) => Equals(obj as Entity<TId>);
    public override int GetHashCode() => EqualityComparer<TId>.Default.GetHashCode(Id);
    public static bool operator ==(Entity<TId>? left, Entity<TId>? right) => Equals(left, right);
    public static bool operator !=(Entity<TId>? left, Entity<TId>? right) => !Equals(left, right);
}}
"""


def aggregate_root_cs(namespace: str) -> str:
    """Generate AggregateRoot base class."""
    return f"""namespace {namespace}.Domain.Common;

/// <summary>
/// Base class for aggregate roots in DDD.
/// </summary>
public abstract class AggregateRoot<TId> : Entity<TId> where TId : notnull
{{
    public int Version {{ get; protected set; }}
    
    protected void IncrementVersion()
    {{
        Version++;
    }}
}}
"""


def value_object_cs(namespace: str) -> str:
    """Generate ValueObject base class."""
    return f"""namespace {namespace}.Domain.Common;

/// <summary>
/// Base class for value objects in DDD.
/// </summary>
public abstract class ValueObject : IEquatable<ValueObject>
{{
    protected abstract IEnumerable<object?> GetEqualityComponents();

    public bool Equals(ValueObject? other)
    {{
        if (other is null) return false;
        if (GetType() != other.GetType()) return false;
        return GetEqualityComponents().SequenceEqual(other.GetEqualityComponents());
    }}

    public override bool Equals(object? obj) => Equals(obj as ValueObject);
    
    public override int GetHashCode()
    {{
        return GetEqualityComponents()
            .Aggregate(1, (current, obj) => 
                HashCode.Combine(current, obj?.GetHashCode() ?? 0));
    }}

    public static bool operator ==(ValueObject? left, ValueObject? right) => Equals(left, right);
    public static bool operator !=(ValueObject? left, ValueObject? right) => !Equals(left, right);
}}
"""


def domain_event_cs(namespace: str) -> str:
    """Generate IDomainEvent interface."""
    return f"""namespace {namespace}.Domain.Common;

/// <summary>
/// Marker interface for domain events.
/// </summary>
public interface IDomainEvent
{{
    DateTime OccurredAt {{ get; }}
}}

/// <summary>
/// Base class for domain events.
/// </summary>
public abstract record DomainEventBase : IDomainEvent
{{
    public DateTime OccurredAt {{ get; }} = DateTime.UtcNow;
}}
"""


def result_cs(namespace: str) -> str:
    """Generate Result type for error handling."""
    return f"""namespace {namespace}.Domain.Common;

/// <summary>
/// Result type for operations that can fail.
/// </summary>
public class Result<T>
{{
    public bool IsSuccess {{ get; }}
    public T? Value {{ get; }}
    public string Error {{ get; }}

    private Result(bool isSuccess, T? value, string error)
    {{
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }}

    public static Result<T> Success(T value) => new(true, value, string.Empty);
    public static Result<T> Failure(string error) => new(false, default, error);
    
    public TResult Match<TResult>(Func<T, TResult> onSuccess, Func<string, TResult> onFailure)
        => IsSuccess ? onSuccess(Value!) : onFailure(Error);
}}

public class Result
{{
    public bool IsSuccess {{ get; }}
    public string Error {{ get; }}

    private Result(bool isSuccess, string error)
    {{
        IsSuccess = isSuccess;
        Error = error;
    }}

    public static Result Success() => new(true, string.Empty);
    public static Result Failure(string error) => new(false, error);
}}
"""


# ========== APPLICATION LAYER TEMPLATES (CQRS) ==========

def command_interface_cs(namespace: str) -> str:
    """Generate ICommand interfaces for CQRS."""
    return f"""using MediatR;
using {namespace}.Domain.Common;

namespace {namespace}.Application.Common.Interfaces;

/// <summary>
/// Marker interface for commands (write operations).
/// </summary>
public interface ICommand : IRequest<Result>
{{
}}

/// <summary>
/// Marker interface for commands that return a value.
/// </summary>
public interface ICommand<TResponse> : IRequest<Result<TResponse>>
{{
}}

/// <summary>
/// Marker interface for command handlers.
/// </summary>
public interface ICommandHandler<TCommand> : IRequestHandler<TCommand, Result>
    where TCommand : ICommand
{{
}}

/// <summary>
/// Marker interface for command handlers that return a value.
/// </summary>
public interface ICommandHandler<TCommand, TResponse> : IRequestHandler<TCommand, Result<TResponse>>
    where TCommand : ICommand<TResponse>
{{
}}
"""


def query_interface_cs(namespace: str) -> str:
    """Generate IQuery interfaces for CQRS."""
    return f"""using MediatR;
using {namespace}.Domain.Common;

namespace {namespace}.Application.Common.Interfaces;

/// <summary>
/// Marker interface for queries (read operations).
/// </summary>
public interface IQuery<TResponse> : IRequest<Result<TResponse>>
{{
}}

/// <summary>
/// Marker interface for query handlers.
/// </summary>
public interface IQueryHandler<TQuery, TResponse> : IRequestHandler<TQuery, Result<TResponse>>
    where TQuery : IQuery<TResponse>
{{
}}
"""

def repository_interface_cs(namespace: str, entity_name: str) -> str:
    """Generate repository interface."""
    return f"""namespace {namespace}.Application.Common.Interfaces;

/// <summary>
/// Repository interface for {entity_name} aggregate.
/// </summary>
public interface I{entity_name}Repository
{{
    Task<{entity_name}?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<{entity_name}>> GetAllAsync(CancellationToken cancellationToken = default);
    Task AddAsync({entity_name} entity, CancellationToken cancellationToken = default);
    Task UpdateAsync({entity_name} entity, CancellationToken cancellationToken = default);
    Task DeleteAsync({entity_name} entity, CancellationToken cancellationToken = default);
}}
"""


def dependency_injection_cs(namespace: str) -> str:
    """Generate DependencyInjection extension for Application layer."""
    return f"""using FluentValidation;
using Microsoft.Extensions.DependencyInjection;
using System.Reflection;

namespace {namespace}.Application;

public static class DependencyInjection
{{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {{
        services.AddMediatR(cfg => 
            cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));
        
        services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());
        
        return services;
    }}
}}
"""


# ========== API LAYER TEMPLATES ==========

def program_cs(namespace: str, solution_name: str) -> str:
    """Generate Program.cs with Clean Architecture DI setup."""
    return f"""using {namespace}.Application;
using {namespace}.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{{
    c.SwaggerDoc("v1", new() {{ Title = "{solution_name} API", Version = "v1" }});
}});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{{
    app.UseSwagger();
    app.UseSwaggerUI();
}}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.MapGet("/health", () => Results.Ok(new {{ status = "healthy", timestamp = DateTime.UtcNow }}))
   .WithName("HealthCheck")
   .WithOpenApi();

app.Run();

// Make Program class visible for integration tests
public partial class Program {{ }}
"""


def controller_base_cs(namespace: str) -> str:
    """Generate ApiControllerBase with MediatR."""
    return f"""using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace {namespace}.Api.Controllers;

/// <summary>
/// Base controller with MediatR support for CQRS.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public abstract class ApiControllerBase : ControllerBase
{{
    private ISender? _mediator;
    protected ISender Mediator => _mediator ??= HttpContext.RequestServices.GetRequiredService<ISender>();
}}
"""


def infrastructure_di_cs(namespace: str) -> str:
    """Generate DependencyInjection extension for Infrastructure layer."""
    return f"""using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace {namespace}.Infrastructure;

public static class DependencyInjection
{{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, 
        IConfiguration configuration)
    {{
        // TODO: Register DbContext
        // services.AddDbContext<ApplicationDbContext>(options =>
        //     options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));
        
        // TODO: Register repositories
        // services.AddScoped<IOrderRepository, OrderRepository>();
        
        return services;
    }}
}}
"""


# ========== BDD TEST TEMPLATES ==========

def feature_file_bdd(feature_name: str, scenarios: list[tuple[str, str]]) -> str:
    """Generate Gherkin feature file."""
    scenario_texts = []
    for scenario_name, description in scenarios:
        scenario_texts.append(f"""
  @{feature_name.lower()}
  Scenario: {scenario_name}
    Given the system is initialized
    When {description}
    Then the operation should succeed""")
    
    return f"""Feature: {feature_name}
    As a user
    I want to {feature_name.lower()}
    So that I can achieve my business goals
{"".join(scenario_texts)}
"""


def steps_file_bdd(namespace: str, feature_name: str) -> str:
    """Generate BDD step definitions."""
    return f"""using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using Reqnroll;
using System.Net;
using System.Net.Http.Json;

namespace {namespace}.Tests.Steps;

[Binding]
public class {feature_name}Steps
{{
    private readonly HttpClient _client;
    private HttpResponseMessage? _response;

    public {feature_name}Steps(WebApplicationFactory<Program> factory)
    {{
        _client = factory.CreateClient();
    }}

    [Given("the system is initialized")]
    public void GivenTheSystemIsInitialized()
    {{
        // Setup test preconditions
    }}

    [When("(.*)")]
    public async Task WhenActionIsPerformed(string action)
    {{
        // Perform the action based on description
        _response = await _client.GetAsync("/health");
    }}

    [Then("the operation should succeed")]
    public void ThenTheOperationShouldSucceed()
    {{
        _response.Should().NotBeNull();
        _response!.StatusCode.Should().Be(HttpStatusCode.OK);
    }}
}}
"""


def web_factory_cs(namespace: str) -> str:
    """Generate custom WebApplicationFactory for integration tests."""
    return f"""using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;

namespace {namespace}.Tests;

public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {{
        builder.ConfigureServices(services =>
        {{
            // Override services for testing
            // Example: Replace real database with in-memory
        }});
        
        builder.UseEnvironment("Testing");
    }}
}}
"""
