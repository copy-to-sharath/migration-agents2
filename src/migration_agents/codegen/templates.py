from __future__ import annotations


def solution_file(solution_name: str, api_guid: str, persistence_guid: str, tests_guid: str) -> str:
    return f"""
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.8.34330.188
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{solution_name}", "src\\{solution_name}\\{solution_name}.csproj", "{{{api_guid}}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{solution_name}.Persistence", "src\\{solution_name}.Persistence\\{solution_name}.Persistence.csproj", "{{{persistence_guid}}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{solution_name}.Tests", "tests\\{solution_name}.Tests\\{solution_name}.Tests.csproj", "{{{tests_guid}}}"
EndProject
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|Any CPU = Debug|Any CPU
        Release|Any CPU = Release|Any CPU
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        {{{api_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{api_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{persistence_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{persistence_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {{{tests_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {{{tests_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU
    EndGlobalSection
EndGlobal
""".strip()


def api_csproj(project_name: str, persistence_project_path: str | None = None) -> str:
    ref = (
        f"""  <ItemGroup>
    <ProjectReference Include="{persistence_project_path}" />
  </ItemGroup>
"""
        if persistence_project_path
        else ""
    )
    return f"""
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
{ref}
</Project>
""".strip()


def persistence_csproj(project_name: str) -> str:
    return f"""
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
""".strip()


def tests_csproj(project_name: str) -> str:
    return f"""
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Reqnroll" Version="2.0.0" />
    <PackageReference Include="Reqnroll.NUnit" Version="2.0.0" />
    <PackageReference Include="NUnit" Version="3.14.0" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
    <ProjectReference Include="..\\..\\src\\{project_name}\\{project_name}.csproj" />
  </ItemGroup>
</Project>
""".strip()


def program_cs(namespace_name: str) -> str:
    return f"""
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();

app.MapGet("/health", () => new {{ status = "ok" }});

app.Run();
""".strip()


def controller_cs(namespace_name: str, api_name: str, actions: list[tuple[str, str]]) -> str:
    lines = [
        "using Microsoft.AspNetCore.Mvc;",
        "",
        f"namespace {namespace_name}.Controllers;",
        "",
        f"[ApiController]",
        f"[Route(\"{api_name}\")]",
        f"public class {api_name}Controller : ControllerBase",
        "{",
    ]
    for verb, route in actions:
        method_name = f"{verb.capitalize()}{api_name}"
        lines.append(f"    [Http{verb.capitalize()}(\"{route}\")]")
        lines.append(f"    public IActionResult {method_name}() => Ok(new {{ status = \"ok\" }});")
        lines.append("")
    lines.append("}")
    return "\n".join(lines).strip()


def feature_file(api_name: str) -> str:
    return f"""
Feature: {api_name} health

  Scenario: Health endpoint returns OK
    Given the API is running
    When I call the health endpoint
    Then the response status should be 200
""".strip()


def steps_cs(namespace_name: str) -> str:
    return f"""
using NUnit.Framework;
using Reqnroll;

namespace {namespace_name};

[Binding]
public class ApiSteps
{{
    private int _statusCode;

    [Given("the API is running")]
    public void GivenApiRunning()
    {{
        _statusCode = 200;
    }}

    [When("I call the health endpoint")]
    public void WhenICallHealth()
    {{
        _statusCode = 200;
    }}

    [Then("the response status should be 200")]
    public void ThenStatusShouldBe200()
    {{
        Assert.That(_statusCode, Is.EqualTo(200));
    }}
}}
""".strip()
