from __future__ import annotations

import argparse
import logging
import os
import uuid
import json
import subprocess
import urllib.request
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
from pathlib import Path

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.ingestion.parquet_writer import write_parquet
from migration_agents.shared_multiprocessing import resolve_workers
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.state import finalize_state, start_state, write_state

from .config import CodegenConfig, load_config
from .contracts import (
    SliceContext,
    GeneratedContract,
    generate_contract_from_slice,
    save_contract_for_verification,
    merge_contracts,
)
from .generator import generate_clean_architecture_solution
from .ddd_builder import (
    SliceAnalysis,
    DDDGenerationResult,
    LLMConfig,
    analyze_slice_for_domain,
    analyze_slice_with_llm,
    build_domain_model_from_slices,
    build_domain_model_with_llm,
    generate_gherkin_from_domain_model,
    generate_contract_from_domain_model,
    generate_commands_from_aggregate,
    generate_queries_from_aggregate,
    run_ddd_first_generation,
)
from .templates import (
    api_csproj,
    feature_file,
    persistence_csproj,
    program_cs,
    solution_file,
    steps_cs,
    tests_csproj,
    controller_cs,
)

LOGGER = logging.getLogger("migration_agents.codegen")


def _created_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _with_metadata(rows: list[dict], config: CodegenConfig, created_at: str) -> list[dict]:
    for row in rows:
        row.setdefault("run_id", config.run_id)
        row.setdefault("artifact_version", config.artifact_version)
        row.setdefault("created_at", created_at)
        row.setdefault("supersedes_version", None)
    return rows


def _fetch_rows(client, table: str, run_id: str, artifact_version: int) -> list[dict]:
    sql = f"""
        select *
        from {table}
        where run_id = '{run_id}' and artifact_version = {artifact_version}
    """
    try:
        return client.query(sql)
    except Exception:  # noqa: BLE001
        LOGGER.info("codegen_missing_table table=%s", table)
        return []


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _call_llm(config: CodegenConfig, prompt: str) -> str:
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
        base_url = config.llm_base_url if hasattr(config, "llm_base_url") and config.llm_base_url else "https://models.inference.ai.azure.com/chat/completions"
        model = config.llm_model or "gpt-4o-mini"
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt[:config.llm_max_input_chars]}],
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
        try:
            with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
                data = json.load(response)
        except HTTPError as exc:
            raise RuntimeError(f"Copilot LLM HTTP error {exc.code}: {exc.reason}") from exc
        except URLError as exc:
            raise RuntimeError(f"Copilot LLM connection error: {exc.reason}") from exc
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("Copilot LLM response missing choices")
        return str(choices[0].get("message", {}).get("content", "")).strip()
    # Fallback to Ollama-style endpoint
    payload = json.dumps(
        {
            "model": config.llm_model,
            "prompt": prompt[: config.llm_max_input_chars],
            "stream": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        config.llm_base_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.llm_timeout_sec) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"LLM HTTP error {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"LLM connection error: {exc.reason}") from exc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("LLM unexpected error") from exc
    return str(data.get("response") or data.get("output") or "").strip()


def _controller_prompt(api_name: str, contract_json: str, namespace: str) -> str:
    return (
        "You are a C# API engineer. Generate a minimal ASP.NET Core controller class for .NET 8 "
        "matching this OpenAPI contract. Include [ApiController], [Route], and one method per operation. "
        "Return only C# code.\n\n"
        f"Namespace: {namespace}\n"
        f"API Name: {api_name}\n"
        f"OpenAPI JSON: {contract_json[:4000]}"
    )


def _actions_from_contract(contract_json: str) -> list[tuple[str, str]]:
    try:
        contract = json.loads(contract_json)
    except json.JSONDecodeError:
        return [("get", "health")]
    paths = contract.get("paths") or {}
    actions: list[tuple[str, str]] = []
    for route, verbs in paths.items():
        if not isinstance(verbs, dict):
            continue
        for verb in verbs.keys():
            actions.append((verb.lower(), route))
    return actions or [("get", "health")]


def _generate_solution(api_name: str, actions: list[tuple[str, str]], contract_json: str, config: CodegenConfig) -> list[dict]:
    solution_root = config.generated_root / api_name
    src_root = solution_root / "src" / api_name
    tests_root = solution_root / "tests" / f"{api_name}.Tests"
    persistence_root = solution_root / "src" / f"{api_name}.Persistence"
    api_guid = str(uuid.uuid4())
    persistence_guid = str(uuid.uuid4())
    tests_guid = str(uuid.uuid4())

    _write_file(
        solution_root / f"{api_name}.sln",
        solution_file(api_name, api_guid, persistence_guid, tests_guid),
    )
    _write_file(
        src_root / f"{api_name}.csproj",
        api_csproj(api_name, f"..\\{api_name}.Persistence\\{api_name}.Persistence.csproj"),
    )
    _write_file(persistence_root / f"{api_name}.Persistence.csproj", persistence_csproj(api_name))
    namespace_api = f"{config.api_namespace}.{api_name}"
    namespace_tests = f"{config.test_namespace}.{api_name}"
    _write_file(src_root / "Program.cs", program_cs(namespace_api))
    controller_code = None
    try:
        controller_code = _call_llm(config, _controller_prompt(api_name, contract_json, namespace_api))
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("codegen_llm_controller_failed api=%s err=%s", api_name, exc)
    if controller_code:
        _write_file(src_root / "Controllers" / f"{api_name}Controller.cs", controller_code)
    else:
        _write_file(src_root / "Controllers" / f"{api_name}Controller.cs", controller_cs(namespace_api, api_name, actions))
    _write_file(tests_root / f"{api_name}.Tests.csproj", tests_csproj(api_name))
    _write_file(tests_root / "Features" / "Health.feature", feature_file(api_name))
    _write_file(tests_root / "Steps" / "ApiSteps.cs", steps_cs(namespace_tests))

    return [
        {"api_name": api_name, "path": str(solution_root / f"{api_name}.sln"), "kind": "solution"},
        {"api_name": api_name, "path": str(src_root / f"{api_name}.csproj"), "kind": "api_csproj"},
        {"api_name": api_name, "path": str(persistence_root / f"{api_name}.Persistence.csproj"), "kind": "persistence_csproj"},
        {"api_name": api_name, "path": str(src_root / "Program.cs"), "kind": "program_cs"},
        {"api_name": api_name, "path": str(src_root / "Controllers" / f"{api_name}Controller.cs"), "kind": "controller"},
        {"api_name": api_name, "path": str(tests_root / f"{api_name}.Tests.csproj"), "kind": "tests_csproj"},
        {"api_name": api_name, "path": str(tests_root / "Features" / "Health.feature"), "kind": "gherkin"},
        {"api_name": api_name, "path": str(tests_root / "Steps" / "ApiSteps.cs"), "kind": "steps"},
    ]


def _slice_migration_prompt(slice_id: str, rule_text: str, source_excerpts: list[str], target_framework: str) -> str:
    """Build a prompt for migrating a slice to target framework."""
    excerpts_text = "\n\n".join(source_excerpts[:5])  # Limit to 5 excerpts
    
    framework_guidance = {
        "dotnet8": """
Target: .NET 8 with minimal APIs or controllers
- Use dependency injection instead of IoC.Resolve patterns
- Use HttpClient instead of custom HTTP helpers
- Use async/await patterns
- Use ILogger for logging
- Use records for DTOs where appropriate
""",
        "springboot3": """
Target: Spring Boot 3 with Java 21
- Use @RestController and @Service annotations
- Use RestTemplate or WebClient for HTTP calls
- Use CompletableFuture for async operations
- Use SLF4J for logging
- Use records for DTOs where appropriate
""",
    }
    
    return f"""You are a code migration expert. Migrate the following legacy .NET Framework code to {target_framework}.

## Slice Context
{rule_text}

## Legacy Source Code
{excerpts_text}

## Migration Guidelines
{framework_guidance.get(target_framework, framework_guidance["dotnet8"])}

## Output Requirements
1. Generate a clean, modern implementation
2. Preserve business logic exactly
3. Include XML documentation comments
4. Add appropriate error handling
5. Return only the migrated code, no explanations

Generate the migrated service class:"""


def _generate_slice_code(
    slice_id: str,
    rule_text: str, 
    source_excerpts: list[str],
    config: CodegenConfig,
) -> list[dict]:
    """Generate code for a slice migration."""
    # Determine service name from slice_id
    service_name = slice_id.replace("entry_", "").replace("_", "")[:20].title() + "Service"
    solution_root = config.generated_root / slice_id
    src_root = solution_root / "src" / service_name
    tests_root = solution_root / "tests" / f"{service_name}.Tests"
    
    # Generate using LLM
    prompt = _slice_migration_prompt(slice_id, rule_text, source_excerpts, config.target_framework)
    migrated_code = None
    try:
        migrated_code = _call_llm(config, prompt)
    except Exception as exc:
        LOGGER.warning("codegen_llm_slice_failed slice=%s err=%s", slice_id, exc)
    
    # Write files
    if config.target_framework == "dotnet8":
        namespace = f"{config.api_namespace}.{service_name}"
        _write_file(src_root / f"{service_name}.cs", migrated_code or f"// TODO: Migrate {slice_id}\n")
        _write_file(src_root / f"{service_name}.csproj", api_csproj(service_name, ""))
        _write_file(src_root / "Program.cs", program_cs(namespace))
        
        if config.generate_tests:
            _write_file(tests_root / f"{service_name}.Tests.csproj", tests_csproj(service_name))
            _write_file(tests_root / "Features" / f"{service_name}.feature", feature_file(service_name))
            _write_file(tests_root / "Steps" / f"{service_name}Steps.cs", steps_cs(f"{config.test_namespace}.{service_name}"))
    
    manifest = [
        {"slice_id": slice_id, "path": str(src_root / f"{service_name}.cs"), "kind": "service", "framework": config.target_framework},
        {"slice_id": slice_id, "path": str(src_root / f"{service_name}.csproj"), "kind": "csproj", "framework": config.target_framework},
    ]
    if config.generate_tests:
        manifest.extend([
            {"slice_id": slice_id, "path": str(tests_root / f"{service_name}.Tests.csproj"), "kind": "tests_csproj", "framework": config.target_framework},
            {"slice_id": slice_id, "path": str(tests_root / "Features" / f"{service_name}.feature"), "kind": "gherkin", "framework": config.target_framework},
        ])
    
    return manifest


def _fetch_slice_contexts(client, slice_ids: list[str], run_id: str, artifact_version: int) -> list[SliceContext]:
    """Fetch context for multiple slices."""
    contexts: list[SliceContext] = []
    
    # Fetch entry graphs
    entry_graphs = _fetch_rows(client, "entry_graphs", run_id, artifact_version)
    logic_rules = _fetch_rows(client, "logic_rules", run_id, artifact_version)
    slice_source_refs = _fetch_rows(client, "slice_source_refs", run_id, artifact_version)
    symbols = _fetch_rows(client, "symbols", run_id, artifact_version)
    code_graph_nodes = _fetch_rows(client, "code_graph_nodes", run_id, artifact_version)
    
    # Build symbol lookup by symbol_id for faster access
    symbol_lookup = {s.get("symbol_id"): s for s in symbols if s.get("symbol_id")}
    
    # Build node_id -> symbol_id lookup (entry_key is a node_id)
    node_to_symbol = {n.get("node_id"): n.get("symbol_id") for n in code_graph_nodes if n.get("symbol_id")}
    
    # Build node_id -> label lookup for fallback name extraction
    node_to_label = {n.get("node_id"): n.get("label") for n in code_graph_nodes if n.get("label")}
    
    # Build entry_key lookup: slice_id (entry_XXXXXXXX) -> full entry_key
    # slice_id format: "entry_" + first 8 chars of entry_key hash
    entry_key_lookup = {}
    for eg in entry_graphs:
        entry_key = eg.get("entry_key", "")
        if entry_key:
            short_id = "entry_" + entry_key[:8]
            entry_key_lookup[short_id] = entry_key
    
    for slice_id in slice_ids:
        # Find entry graph - slice_id is "entry_" + first 8 chars of entry_key
        full_entry_key = entry_key_lookup.get(slice_id)
        if full_entry_key:
            entry = next((e for e in entry_graphs if e.get("entry_key") == full_entry_key), None)
        else:
            # Fallback: try exact match
            entry = next((e for e in entry_graphs if e.get("entry_key") == slice_id), None)
        if not entry:
            LOGGER.warning("Slice not found: %s", slice_id)
            continue
        
        # Get symbol name: entry_key is a node_id, need to find symbol_id from nodes
        entry_key = full_entry_key or slice_id
        symbol = None
        # First try: look up via node_to_symbol mapping
        symbol_id = node_to_symbol.get(entry_key)
        if symbol_id:
            symbol = symbol_lookup.get(symbol_id)
        # Fallback: try direct symbol_id lookup
        if not symbol:
            symbol = symbol_lookup.get(entry_key)
        
        if symbol:
            entry_name = symbol.get("name", slice_id[:16])
            # Add signature info for better context
            signature = symbol.get("signature", "")
            kind = symbol.get("kind", "")
        else:
            # Try to derive name from node label (file path)
            label = node_to_label.get(entry_key, "")
            if label:
                # label format: 'path/to/file.ascx:linenum'
                parts = label.split(':')
                filepath = parts[0] if parts else label
                filename = os.path.basename(filepath)
                entry_name = os.path.splitext(filename)[0]  # Remove extension
            else:
                entry_name = entry.get("entry_name", slice_id[:16])
            signature = ""
            kind = ""
        
        # Find rule
        rule = next((r for r in logic_rules if r.get("slice_id") == slice_id), None)
        rule_text = rule.get("rule_text", "") if rule else ""
        
        # Get source excerpts
        excerpts = [
            ref.get("excerpt", "")
            for ref in slice_source_refs
            if ref.get("slice_id") == slice_id and ref.get("excerpt")
        ]
        
        # Get symbol info for better domain analysis
        slice_symbols = [
            {"name": s.get("name"), "kind": s.get("kind"), "signature": s.get("signature")}
            for s in symbols
            if s.get("slice_id") == slice_id or s.get("symbol_id") == slice_id
        ]
        
        contexts.append(SliceContext(
            slice_id=slice_id,
            entry_name=entry_name,
            rule_text=rule_text,
            source_excerpts=excerpts,
            depth=entry.get("capped_depth", 0),
            node_count=entry.get("node_count", 0),
            file_count=entry.get("file_count", 0),
            symbols=slice_symbols,
        ))
    
    return contexts


def _fetch_slice_analyses(
    client, 
    slice_ids: list[str], 
    run_id: str, 
    artifact_version: int,
    llm_config: LLMConfig | None = None,
    use_llm: bool = False,
) -> list[SliceAnalysis]:
    """Fetch slice data and create analyses for DDD-first generation."""
    contexts = _fetch_slice_contexts(client, slice_ids, run_id, artifact_version)
    
    analyses: list[SliceAnalysis] = []
    for ctx in contexts:
        if use_llm and llm_config and llm_config.provider != "none":
            LOGGER.info("Using LLM for slice analysis: %s", ctx.slice_id)
            analysis = analyze_slice_with_llm(
                slice_id=ctx.slice_id,
                entry_name=ctx.entry_name,
                rule_text=ctx.rule_text,
                source_excerpts=ctx.source_excerpts,
                symbols=ctx.symbols,
                llm_config=llm_config,
            )
        else:
            analysis = analyze_slice_for_domain(
                slice_id=ctx.slice_id,
                entry_name=ctx.entry_name,
                rule_text=ctx.rule_text,
                source_excerpts=ctx.source_excerpts,
                symbols=ctx.symbols,
            )
        analyses.append(analysis)
    
    return analyses


def _create_llm_config(config: CodegenConfig) -> LLMConfig:
    """Create LLMConfig from CodegenConfig."""
    return LLMConfig.from_codegen_config(config)


def run_ddd_first(config: CodegenConfig) -> dict:
    """
    Run DDD-first code generation using LLM.
    
    Phase 1: Build Domain Model from slices using LLM (requires verification)
    Phase 2: Generate Gherkin/BDD from domain model (requires verification)
    Phase 3: Generate Contract from domain model (requires verification)
    Phase 4: Generate implementation code
    """
    created_at = _created_at()
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    config = config.model_copy(update={"run_id": run_id, "workers": resolve_workers(config.workers)})
    
    client = get_mcp_client(run_id=run_id, parquet_root=str(config.output_root))
    
    # Create LLM config
    llm_config = _create_llm_config(config)
    use_llm = config.llm_provider != "none"
    
    if use_llm:
        LOGGER.info("Using LLM for DDD generation: provider=%s model=%s", 
                   llm_config.provider, llm_config.model)
    
    # Determine slice IDs to process
    slice_ids: list[str] = []
    if config.slice_ids:
        slice_ids = config.slice_ids
    elif config.slice_id:
        slice_ids = [config.slice_id]
    else:
        # Fetch all slices with min_capped_depth >= 1
        entry_graphs = _fetch_rows(client, "entry_graphs", run_id, config.artifact_version)
        all_slice_ids = [e.get("entry_key") for e in entry_graphs if e.get("capped_depth", 0) >= 1]
        # Apply offset and limit for batch processing
        offset = getattr(config, 'slice_offset', 0) or 0
        if offset > 0:
            all_slice_ids = all_slice_ids[offset:]
        if config.max_slices:
            slice_ids = all_slice_ids[:config.max_slices]
        else:
            slice_ids = all_slice_ids
    
    LOGGER.info("ddd_first_mode slices=%d offset=%d solution=%s use_llm=%s", 
                len(slice_ids), getattr(config, 'slice_offset', 0) or 0, config.solution_name, use_llm)
    
    # Build Domain Model (and optionally subsequent phases based on ddd_phase)
    LOGGER.info("Running DDD generation (phase=%s)...", config.ddd_phase)
    analyses = _fetch_slice_analyses(
        client, slice_ids, run_id, config.artifact_version,
        llm_config=llm_config, use_llm=use_llm
    )
    
    ddd_output = config.generated_root / config.solution_name / "ddd"
    ddd_result = run_ddd_first_generation(
        analyses=analyses,
        solution_name=config.solution_name,
        output_root=ddd_output,
        llm_config=llm_config,
        use_llm=use_llm,
        phase=config.ddd_phase,
    )
    
    result = {
        "phase": config.ddd_phase,
        "slice_count": len(slice_ids),
        "aggregate_count": len(ddd_result.domain_model.aggregates),
        "domain_model_path": str(ddd_result.domain_model_path),
        "gherkin_count": len(ddd_result.gherkin_features),
        "gherkin_paths": [str(p) for p in ddd_result.gherkin_paths],
        "contract_path": str(ddd_result.contract_path) if ddd_result.contract_path else None,
        "llm_used": use_llm,
        "command_count": len(ddd_result.commands),
        "query_count": len(ddd_result.queries),
    }
    
    # Provide next step guidance based on current phase
    if config.ddd_phase == "domain":
        result["next_step"] = f"Review domain model at {ddd_result.domain_model_path}, then run with ddd_phase='gherkin'"
        LOGGER.info("Domain model saved. Review and approve before proceeding.")
        LOGGER.info("Next step: Review domain model at %s and run with --phase gherkin", ddd_result.domain_model_path)
        return result
    
    if config.ddd_phase == "gherkin":
        result["next_step"] = f"Review Gherkin features at {ddd_output / 'features'}, then run with ddd_phase='contract'"
        LOGGER.info("Gherkin features saved. Review and approve before proceeding.")
        return result
    
    if config.ddd_phase == "contract":
        result["next_step"] = f"Review contract at {ddd_result.contract_path}, then run with ddd_phase='all'"
        LOGGER.info("Contract saved. Review and approve before proceeding.")
        return result
    
    # Phase is "all" - generate implementation code
    LOGGER.info("Generating implementation code...")
    
    # Convert DDD result to GeneratedContract for code generation
    contracts: list[GeneratedContract] = []
    for aggregate in ddd_result.domain_model.aggregates:
        gc = GeneratedContract(
            slice_id=f"ddd_{aggregate.name.lower()}",
            contract=ddd_result.contract,
            commands=[c for c in ddd_result.commands if c.aggregate == aggregate.name],
            queries=[q for q in ddd_result.queries if aggregate.name in q.name],
            entities=[aggregate.to_entity()],
        )
        contracts.append(gc)
    
    manifest = generate_clean_architecture_solution(
        solution_name=config.solution_name,
        namespace=config.api_namespace,
        contracts=contracts,
        output_root=config.generated_root,
    )
    
    result["phase"] = "code_generated"
    result["manifest_count"] = len(manifest)
    result["solution_path"] = str(config.generated_root / config.solution_name)
    
    return result


def run_contract_first(config: CodegenConfig) -> dict:
    """
    Run contract-first code generation.
    
    Phase 1: Generate contracts from slices (requires verification)
    Phase 2: Generate code from verified contracts
    """
    created_at = _created_at()
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    config = config.model_copy(update={"run_id": run_id, "workers": resolve_workers(config.workers)})
    
    client = get_mcp_client(run_id=run_id, parquet_root=str(config.output_root))
    
    # Determine slice IDs to process
    slice_ids: list[str] = []
    if config.slice_ids:
        slice_ids = config.slice_ids
    elif config.slice_id:
        slice_ids = [config.slice_id]
    else:
        # Fetch all slices with min_capped_depth >= 1
        entry_graphs = _fetch_rows(client, "entry_graphs", run_id, config.artifact_version)
        slice_ids = [e.get("entry_key") for e in entry_graphs if e.get("capped_depth", 0) >= 1]
        if config.max_slices:
            slice_ids = slice_ids[:config.max_slices]
    
    LOGGER.info("contract_first_mode slices=%d solution=%s", len(slice_ids), config.solution_name)
    
    # Fetch contexts
    contexts = _fetch_slice_contexts(client, slice_ids, run_id, config.artifact_version)
    
    # Generate contracts
    contracts: list[GeneratedContract] = []
    for ctx in contexts:
        contract = generate_contract_from_slice(ctx)
        contracts.append(contract)
    
    # Save contracts for verification
    contract_output = config.contract_output_path or (config.generated_root / "contracts")
    for gc in contracts:
        save_contract_for_verification(gc.contract, contract_output / gc.slice_id)
    
    # Save merged contract
    if len(contracts) > 1:
        merged = merge_contracts(contracts, config.solution_name)
        save_contract_for_verification(merged, contract_output)
    
    result = {
        "phase": "contracts_generated",
        "slice_count": len(slice_ids),
        "contract_count": len(contracts),
        "contract_output": str(contract_output),
        "requires_verification": config.require_contract_verification,
        "next_step": "Review contracts and run with --generate-code flag" if config.require_contract_verification else "Generating code...",
    }
    
    # If verification not required, proceed to code generation
    if not config.require_contract_verification:
        manifest = _generate_code_from_contracts(config, contracts)
        result["phase"] = "code_generated"
        result["manifest_count"] = len(manifest)
    
    return result


def _generate_code_from_contracts(config: CodegenConfig, contracts: list[GeneratedContract]) -> list[dict]:
    """Generate code from verified contracts using Clean Architecture."""
    if config.use_clean_architecture:
        return generate_clean_architecture_solution(
            solution_name=config.solution_name,
            namespace=config.api_namespace,
            contracts=contracts,
            output_root=config.generated_root,
        )
    else:
        # Fallback to simple generation
        manifest_rows = []
        for gc in contracts:
            manifest_rows.extend(
                _generate_slice_code(gc.slice_id, gc.contract.description, [], config)
            )
        return manifest_rows


def run(config: CodegenConfig) -> None:
    created_at = _created_at()
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    config = config.model_copy(update={"run_id": run_id, "workers": resolve_workers(config.workers)})
    output_root = config.output_root / config.run_id / "step_9"
    output_root.mkdir(parents=True, exist_ok=True)
    state = start_state("codegen", config.run_id, config.artifact_version)
    client = get_mcp_client(run_id=run_id, parquet_root=str(config.output_root))

    manifest_rows: list[dict] = []
    
    # DDD-first mode (preferred): Build DDD -> Generate Gherkin -> Generate Contract -> Generate Code
    if config.ddd_first and config.use_ddd and (config.slice_ids or config.slice_id or config.use_clean_architecture):
        LOGGER.info("codegen_ddd_first solution=%s", config.solution_name)
        result = run_ddd_first(config)
        LOGGER.info("codegen_ddd_first_result phase=%s", result.get("phase"))
        
        # If code was generated, get manifest
        if result.get("phase") == "code_generated":
            processed_count = result.get("slice_count", 0)
            manifest_rows = []  # Manifest is written by generator
            LOGGER.info("Solution generated at: %s", result.get("solution_path"))
        else:
            processed_count = result.get("aggregate_count", 0)
            LOGGER.info("Domain model saved to: %s", result.get("domain_model_path"))
            LOGGER.info("Gherkin features: %s", result.get("gherkin_paths"))
            LOGGER.info("Contract saved to: %s", result.get("contract_path"))
            LOGGER.info("Next step: %s", result.get("next_step"))
    
    # Contract-first mode (legacy): Generate Contract -> Verify -> Generate Code
    elif config.contract_first and (config.slice_ids or config.use_clean_architecture):
        LOGGER.info("codegen_contract_first solution=%s", config.solution_name)
        result = run_contract_first(config)
        LOGGER.info("codegen_contract_first_result phase=%s", result.get("phase"))
        
        # If code was generated, get manifest
        if result.get("phase") == "code_generated":
            processed_count = result.get("slice_count", 0)
            manifest_rows = []  # Manifest is written by generator
        else:
            processed_count = result.get("contract_count", 0)
            LOGGER.info("Contracts saved to: %s", result.get("contract_output"))
            LOGGER.info("Next step: %s", result.get("next_step"))
    
    # Single slice mode (legacy)
    elif config.slice_id:
        LOGGER.info("codegen_slice_mode slice=%s framework=%s", config.slice_id, config.target_framework)
        
        # Fetch slice context
        logic_rules = _fetch_rows(client, "logic_rules", config.run_id, config.artifact_version)
        slice_source_refs = _fetch_rows(client, "slice_source_refs", config.run_id, config.artifact_version)
        
        # Find rule for this slice
        rule = next((r for r in logic_rules if r.get("slice_id") == config.slice_id), None)
        if not rule:
            LOGGER.warning("codegen_no_rule slice=%s", config.slice_id)
            rule_text = f"Slice {config.slice_id}"
        else:
            rule_text = rule.get("rule_text", "")
        
        # Get source excerpts
        excerpts = [
            ref.get("excerpt", "")
            for ref in slice_source_refs
            if ref.get("slice_id") == config.slice_id and ref.get("excerpt")
        ]
        
        # Generate code
        manifest_rows = _generate_slice_code(config.slice_id, rule_text, excerpts, config)
        processed_count = 1
    else:
        # API contract-based code generation (original behavior)
        api_contracts = _fetch_rows(client, "api_contracts", config.run_id, config.artifact_version)
        if config.api_name:
            api_contracts = [row for row in api_contracts if row.get("api_name") == config.api_name]
        if config.max_apis is not None:
            api_contracts = api_contracts[: max(0, config.max_apis)]

        for contract in api_contracts:
            api_name = contract.get("api_name") or "GeneratedApi"
            actions = _actions_from_contract(contract.get("contract_json", ""))
            manifest_rows.extend(
                _generate_solution(api_name, actions, contract.get("contract_json", ""), config)
            )
        processed_count = len(api_contracts)

    if manifest_rows:
        write_parquet(
            output_root,
            "codegen_manifest",
            _with_metadata(manifest_rows, config, created_at),
            partition_cols=["run_id", "artifact_version"],
        )

    state = finalize_state(
        state,
        processed_count=processed_count,
        outputs={"codegen_manifest": len(manifest_rows)},
        notes={
            "output_root": str(output_root), 
            "slice_id": config.slice_id,
            "slice_ids": config.slice_ids,
            "framework": config.target_framework,
            "solution_name": config.solution_name,
            "contract_first": config.contract_first,
            "use_clean_architecture": config.use_clean_architecture,
            "use_cqrs": config.use_cqrs,
            "use_ddd": config.use_ddd,
        },
    )
    write_state("codegen", state)
    LOGGER.info("codegen_done processed=%d files=%d", processed_count, len(manifest_rows))


def main() -> None:
    from migration_agents.constants import ensure_directories
    ensure_directories()
    
    parser = argparse.ArgumentParser(description="Stage 9 Codegen pipeline.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--generate-code", action="store_true", help="Generate code from verified contracts")
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("codegen")
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
