"""Agent-aligned MCP tools for autonomous pipeline operations.

These tools map to the 3-agent pipeline and enable Copilot to
autonomously invoke them based on user intent.

Agents:
- 01-analyzer: One-time analysis (Ingest → Parse → Slice)
- 02-builder: Per-slice code generation (Logic → Domain → TDD → Code)
- 03-judge: Validation + fix loop (Validate → Fix Queue → Re-validate)

Pipeline Flow:
  [01-analyzer] ──► [02-builder] ◄──► [03-judge]
       │                  │              │
   One-time          Per-slice      Fix loop

BATCH CODE GENERATION (for large codebases):
When dealing with 100+ slices, use the batch_codegen tool instead of
individual builder_generate calls. The typical workflow is:

  1. get_batch_status(solution_name="X")     # Check current state
  2. cleanup_generated(solution_name="X")    # Clean if regenerating
  3. batch_codegen(batch_size=500, confirm=true)  # Generate all slices

The batch_codegen tool automatically:
- Processes slices in batches (default 500)
- Tracks progress and ETA
- Can resume from a specific batch if interrupted
- Reports total files generated
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from migration_agents.state import load_state
from migration_agents.constants import (
    DEFAULT_PATHS,
    CONFIG_FILES,
    STATE_FILES,
    PIPELINE_STEPS,
    STEP_STATUS,
    DEFAULT_PARQUET_ROOT,
    DEFAULT_GENERATED_ROOT,
    DEFAULT_CONFIG_INGESTION,
    DEFAULT_CONFIG_PARSER,
    DEFAULT_CONFIG_SLICE,
    DEFAULT_CONFIG_CODEGEN,
)

LOGGER = logging.getLogger("migration_agents.mcp.agent_tools")


def _load_config(config_path: str) -> dict:
    """Load a JSON config file, return empty dict if not found."""
    try:
        path = Path(config_path)
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return {}


def _merge_config(config: dict, overrides: dict) -> dict:
    """Merge overrides into config, returning merged result."""
    merged = config.copy()
    merged.update(overrides)
    return merged


# Tool definitions for MCP tools/list
AGENT_TOOLS = [
    # === 01-ANALYZER: One-time Analysis (unified tool) ===
    {
        "name": "analyzer",
        "description": "[01-analyzer] One-time analysis pipeline with 3 steps: ingest → parse → slice. Use 'step' parameter to specify which step to run.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "step": {
                    "type": "string",
                    "enum": ["ingest", "parse", "slice"],
                    "description": "Analysis step to run: 'ingest' (step 1), 'parse' (step 2), 'slice' (step 3)",
                },
                # Ingest parameters
                "source_path": {
                    "type": "string",
                    "description": "[ingest] Path to legacy source directory",
                },
                "ingestion_mode": {
                    "type": "string",
                    "enum": ["full", "incremental"],
                    "description": "[ingest] 'full' flushes all data and re-ingests; 'incremental' only processes changed files (default: incremental)",
                },
                "output_root": {
                    "type": "string",
                    "description": "[ingest] Output directory for parquet files (default: data/parquet)",
                },
                "exclude_dirs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "[ingest] Directories to exclude (e.g., ['.git', 'node_modules'])",
                },
                "exclude_extensions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "[ingest] File extensions to exclude (e.g., ['.png', '.exe'])",
                },
                # Parse parameters
                "config_path": {
                    "type": "string",
                    "description": "[parse/slice] Path to config JSON file",
                },
                "artifact_version": {
                    "type": "integer",
                    "description": "[ingest/parse] Artifact version number (default: 1)",
                },
                "entry_graph_incremental": {
                    "type": "boolean",
                    "description": "[parse] Skip already processed entry graphs (default: true)",
                },
                "entry_graph_render_svg": {
                    "type": "boolean",
                    "description": "[parse] Render SVG graphs (default: false)",
                },
                # Roslyn parameters for C#/VB.NET semantic analysis
                "roslyn_cmd": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "[parse] Command to run Roslyn analyzer for C#/VB.NET (e.g., ['dotnet', 'run', '--project', 'RoslynAnalyzer']). Enables deep call resolution.",
                },
                "roslyn_timeout_sec": {
                    "type": "integer",
                    "description": "[parse] Timeout for Roslyn analysis in seconds (default: 60)",
                },
                "roslyn_parquet_root": {
                    "type": "string",
                    "description": "[parse] Path to pre-computed Roslyn parquet output for faster incremental runs",
                },
                # Slice parameters
                "endpoint": {
                    "type": "string",
                    "description": "[slice] Specific endpoint to focus on (optional)",
                },
                "depth": {
                    "type": "integer",
                    "description": "[slice] Maximum call graph depth to traverse (default: 10)",
                },
                "min_depth": {
                    "type": "integer",
                    "description": "[slice] Minimum depth to start processing (default: 0)",
                },
                "slicing_mode": {
                    "type": "string",
                    "enum": ["auto", "entry_graph", "community"],
                    "description": "[slice] Slicing strategy: 'auto' uses entry_graphs if available, 'entry_graph' forces entry-based, 'community' forces community detection (default: auto)",
                },
                # Common
                "confirm": {
                    "type": "boolean",
                    "description": "Set to true to execute after previewing config. Omit or false to preview only.",
                },
            },
            "required": ["step"],
        },
    },
    # === 02-BUILDER: Per-slice Code Generation ===
    {
        "name": "builder_generate",
        "description": "[02-builder] Generate logic rules, domain model, tests, and implementation code from a slice.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slice_id": {
                    "type": "string",
                    "description": "Slice identifier to generate code for",
                },
                "target_framework": {
                    "type": "string",
                    "description": "Target framework (e.g., 'dotnet8', 'springboot3')",
                },
                "generate_tests": {
                    "type": "boolean",
                    "description": "Whether to generate TDD test cases (default: true)",
                },
                "is_retry": {
                    "type": "boolean",
                    "description": "Set true if regenerating after a fix was applied",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Human approval to proceed with generation",
                },
            },
            "required": ["slice_id"],
        },
    },
    {
        "name": "builder_fix",
        "description": "[02-builder] Apply a fix from the judge's fix_queue. REQUIRES HUMAN APPROVAL.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "fix_id": {
                    "type": "string",
                    "description": "Fix identifier from fix_queue",
                },
                "auto_revalidate": {
                    "type": "boolean",
                    "description": "Whether to re-run judge after fix (default: true)",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Human approval to apply the fix (required)",
                },
            },
            "required": ["fix_id"],
        },
    },
    # === 03-JUDGE: Validation + Fix Loop ===
    {
        "name": "judge_validate",
        "description": "[03-judge] Validate build/test status, citation completeness, and logic alignment. Populates fix_queue for failures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slice_id": {
                    "type": "string",
                    "description": "Slice identifier to validate",
                },
                "check_coverage": {
                    "type": "boolean",
                    "description": "Whether to check rule coverage (default: true)",
                },
                "check_citations": {
                    "type": "boolean",
                    "description": "Whether to check citation completeness (default: true)",
                },
                "iteration": {
                    "type": "integer",
                    "description": "Current validation iteration (for tracking re-validations)",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Human approval for re-validation (2nd+ iteration)",
                },
            },
            "required": ["slice_id"],
        },
    },
    # === Utility Tools ===
    {
        "name": "discover_tools",
        "description": "Discover all available MCP tools with their descriptions, parameters, and which agent they belong to. Use this at the start of a session to understand available capabilities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "enum": ["01-analyzer", "02-builder", "03-judge", "utility", "all"],
                    "description": "Filter tools by agent. 'all' returns everything (default).",
                },
                "category": {
                    "type": "string",
                    "enum": ["analysis", "ddd", "codegen", "validation", "approval", "batch", "all"],
                    "description": "Filter tools by category. 'all' returns everything (default).",
                },
            },
            "required": [],
        },
    },
    {
        "name": "clean_pipeline",
        "description": "Clean all pipeline data and start fresh. Removes parquet files, DuckDB database, generated code, and logs. REQUIRES confirm=true.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to execute the clean operation",
                },
            },
            "required": ["confirm"],
        },
    },
    {
        "name": "pipeline_status",
        "description": "Get the current status of all pipeline stages and agents.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "refresh_views",
        "description": "Refresh DuckDB views to pick up new parquet files from the latest run. Use after running analyzer steps to ensure queries use fresh data.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_parse_coverage",
        "description": "[01-analyzer] Get parse coverage report showing what was parsed vs skipped vs uncovered (0 symbols) vs partial coverage (<10%). Shows files that need query improvements. Use after running the parser to see quality metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "show_skipped": {
                    "type": "boolean",
                    "description": "Include details on skipped files (default: true)",
                },
                "show_uncovered": {
                    "type": "boolean",
                    "description": "Include files parsed but with 0 symbols extracted (default: true)",
                },
                "show_partial": {
                    "type": "boolean",
                    "description": "Include files with <10% symbol coverage that need improvement (default: true)",
                },
                "show_warnings": {
                    "type": "boolean",
                    "description": "Include warnings and improvement suggestions (default: true)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "list_endpoints",
        "description": "List all discovered endpoints from the parsed codebase.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "string",
                    "description": "Optional filter pattern for endpoint names",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of endpoints to return (default: 100)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "list_slices",
        "description": "List all generated slices with their status and metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by status: 'pending', 'complete', 'failed'",
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_slice_context",
        "description": "Get the full context for a specific slice including source references, symbols, and call chains.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slice_id": {
                    "type": "string",
                    "description": "Slice identifier to get context for",
                },
            },
            "required": ["slice_id"],
        },
    },
    # === DDD-FIRST TOOLS: Domain-Driven Design Generation ===
    {
        "name": "ddd_get_analysis_prompt",
        "description": "[DDD] Get the prompt for analyzing a slice to extract DDD concepts (aggregate, behaviors, events, etc). Copilot should analyze the prompt context and return a JSON response.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slice_id": {
                    "type": "string",
                    "description": "Slice identifier to analyze",
                },
            },
            "required": ["slice_id"],
        },
    },
    {
        "name": "ddd_apply_analysis",
        "description": "[DDD] Apply Copilot's DDD analysis response to a slice. Pass the JSON response from analyzing the DDD prompt.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slice_id": {
                    "type": "string",
                    "description": "Slice identifier that was analyzed",
                },
                "analysis": {
                    "type": "object",
                    "description": "Copilot's DDD analysis response with aggregate_name, properties, behaviors, domain_events, value_objects, invariants",
                },
            },
            "required": ["slice_id", "analysis"],
        },
    },
    {
        "name": "ddd_get_domain_model_prompt",
        "description": "[DDD] Get the prompt for building a unified domain model from slice analyses. Call after analyzing all slices.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution/domain model",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_apply_domain_model",
        "description": "[DDD] Apply Copilot's domain model response. Pass the JSON response from the domain model prompt.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution/domain model",
                },
                "domain_model": {
                    "type": "object",
                    "description": "Copilot's domain model response with aggregates and shared_value_objects",
                },
            },
            "required": ["solution_name", "domain_model"],
        },
    },
    {
        "name": "ddd_generate_gherkin",
        "description": "[DDD] Generate Gherkin/BDD specifications from the domain model. Run after applying the domain model.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution/domain model",
                },
                "output_path": {
                    "type": "string",
                    "description": "Output directory for Gherkin files (default: generated/)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_generate_contract",
        "description": "[DDD] Generate API contract (OpenAPI) from the domain model. Run after applying the domain model.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution/domain model",
                },
                "output_path": {
                    "type": "string",
                    "description": "Output directory for contract files (default: generated/)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_run_full_pipeline",
        "description": "[DDD] Run the complete DDD-first generation pipeline using rule-based analysis (no Copilot prompts). For Copilot-driven analysis, use the individual ddd_* tools.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution",
                },
                "output_path": {
                    "type": "string",
                    "description": "Output directory for all generated files",
                },
                "slice_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of slice IDs to process (default: all slices)",
                },
            },
            "required": ["solution_name"],
        },
    },
    # === COMPREHENSIVE DDD ANALYSIS (Analyzes ALL endpoints) ===
    {
        "name": "ddd_analyze_all_endpoints",
        "description": "[DDD] Get prompt for comprehensive DDD analysis of ALL recognized endpoints across all depth levels. This analyzes the entire system before drawing conclusions about bounded contexts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution being analyzed",
                },
                "min_depth": {
                    "type": "integer",
                    "description": "Minimum depth level to include (default: 0)",
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth level to include (default: 10)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_apply_full_analysis",
        "description": "[DDD] Apply Copilot's comprehensive DDD analysis including ubiquitous language, bounded context candidates, aggregates, and domain events. Must include SME review before proceeding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution",
                },
                "analysis": {
                    "type": "object",
                    "description": "Copilot's full DDD analysis with ubiquitous_language, bounded_context_candidates, recommended_context, aggregates, domain_events, etc.",
                },
            },
            "required": ["solution_name", "analysis"],
        },
    },
    {
        "name": "ddd_get_sme_review",
        "description": "[DDD] Get the DDD analysis document for Subject Matter Expert (SME) review. Returns a formatted review document with all DDD artifacts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution to get review document for",
                },
                "output_path": {
                    "type": "string",
                    "description": "Optional path to write the review document (default: generated/ddd_review/)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_submit_sme_review",
        "description": "[DDD] Submit SME review feedback for the DDD analysis. This gates proceeding to code generation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution being reviewed",
                },
                "review_status": {
                    "type": "string",
                    "enum": ["APPROVE", "NEEDS_REVISION", "REJECT"],
                    "description": "SME review decision",
                },
                "reviewer_name": {
                    "type": "string",
                    "description": "Name of the SME reviewer",
                },
                "feedback": {
                    "type": "object",
                    "description": "Detailed SME feedback with comments, corrections, and action items",
                },
            },
            "required": ["solution_name", "review_status", "reviewer_name"],
        },
    },
    {
        "name": "ddd_list_bounded_contexts",
        "description": "[DDD] List all bounded context candidates with their confidence scores and reasoning.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_get_ubiquitous_language",
        "description": "[DDD] Get the ubiquitous language glossary for the domain.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_validate_coverage",
        "description": "[DDD-Judge] Validate that the DDD analysis covers all endpoints. Run this BEFORE SME review to verify completeness.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution to validate",
                },
            },
            "required": ["solution_name"],
        },
    },
    # === VALIDATION TOOLS: Deterministic Validation & Versioning ===
    {
        "name": "validate_migration",
        "description": "[validation] Run deterministic validation against rubrics for a migration project. Returns scores per layer (domain, application, api, infrastructure) and overall assessment with detailed rubric breakdown.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project (e.g., 'generated/nopcommerce-modern')",
                },
                "stages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Which stages to validate: 'domain', 'application', 'api', 'infrastructure', 'all' (default: all)",
                },
                "output_format": {
                    "type": "string",
                    "enum": ["summary", "detailed", "json"],
                    "description": "Output format: summary (scores only), detailed (with rubrics), json (raw data)",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "get_validation_report",
        "description": "[validation] Get the latest validation report for a project, including scores, issues, and recommendations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "report_id": {
                    "type": "string",
                    "description": "Specific report ID (optional, defaults to latest)",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "get_coverage_summary",
        "description": "[validation] Get bounded context coverage summary showing expected vs generated endpoints per context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "create_validation_review",
        "description": "[validation] Create a review file with fixes to address validation issues. SME can then modify and apply.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "reviewer": {
                    "type": "string",
                    "description": "Name of the reviewer",
                },
                "auto_generate_fixes": {
                    "type": "boolean",
                    "description": "Auto-generate fix suggestions from validation issues (default: true)",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "list_validation_fixes",
        "description": "[validation] List all pending fixes from the latest review file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "priority": {
                    "type": "string",
                    "enum": ["all", "critical", "high", "medium", "low"],
                    "description": "Filter by priority (default: all)",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "apply_validation_fixes",
        "description": "[validation] Apply pending fixes from a review. REQUIRES confirm=true for actual application.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "fix_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific fix IDs to apply (optional, defaults to all pending)",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to actually apply fixes (false = dry run)",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "get_validation_history",
        "description": "[validation] Get validation run history from state manager, showing all validation runs with scores and issues.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution to get validation history for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of runs to return (default: 10)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "get_version_history",
        "description": "[validation] Get version history showing all changes, fixes applied, and score progression.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum entries to return (default: 20)",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "compare_versions",
        "description": "[validation] Compare two versions showing what changed between them.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "from_version": {
                    "type": "string",
                    "description": "Starting version (e.g., '1.0.0')",
                },
                "to_version": {
                    "type": "string",
                    "description": "Ending version (e.g., '1.0.3')",
                },
            },
            "required": ["project_path", "from_version", "to_version"],
        },
    },
    # === APPROVAL WORKFLOW TOOLS: Human-in-the-loop approval ===
    {
        "name": "get_step_for_approval",
        "description": "[approval] Get a pipeline step with its rules/criteria for human approval. Shows all rules, thresholds, and current scores. Human must APPROVE, REJECT, or SKIP.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "step_id": {
                    "type": "string",
                    "enum": ["step_1_analysis", "step_2_domain", "step_3_application", "step_4_infrastructure", "step_5_api", "step_6_testing", "step_7_validation"],
                    "description": "Step ID to get for approval",
                },
            },
            "required": ["project_path", "step_id"],
        },
    },
    {
        "name": "submit_step_approval",
        "description": "[approval] Submit human approval decision for a pipeline step. REQUIRES explicit decision: APPROVE, REJECT (with reason), or SKIP (with justification).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
                "step_id": {
                    "type": "string",
                    "description": "Step ID to approve",
                },
                "decision": {
                    "type": "string",
                    "enum": ["APPROVE", "REJECT", "SKIP"],
                    "description": "Approval decision: APPROVE to proceed, REJECT to block, SKIP to bypass",
                },
                "approver": {
                    "type": "string",
                    "description": "Name/role of the approver (e.g., 'SME', 'Tech Lead')",
                },
                "reason": {
                    "type": "string",
                    "description": "Required for REJECT/SKIP: Reason for rejection or justification for skip",
                },
            },
            "required": ["project_path", "step_id", "decision"],
        },
    },
    {
        "name": "get_approval_status",
        "description": "[approval] Get the current approval status of all pipeline steps. Shows which steps are approved, pending, rejected, or skipped.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the generated migration project",
                },
            },
            "required": ["project_path"],
        },
    },
    # === LLM-POWERED DDD ANALYSIS ===
    {
        "name": "ddd_analyze_with_copilot",
        "description": "[DDD-Copilot] Prepare DDD analysis for Copilot LLM. Returns a structured prompt that Copilot will automatically process. The analysis includes domain model, bounded contexts, and ubiquitous language.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution being analyzed",
                },
                "max_endpoints": {
                    "type": "integer",
                    "description": "Maximum number of endpoints to analyze (default: 50)",
                },
                "min_depth": {
                    "type": "integer",
                    "description": "Minimum depth level to include (default: 0)",
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth level to include (default: 3)",
                },
            },
            "required": ["solution_name"],
        },
    },
    # === BATCH CODE GENERATION ===
    # DDD-First Workflow: domain → contract → code
    # Use these tools when user wants to generate code for a large codebase (100+ slices)
    # Recommended workflow:
    #   1. batch_codegen(phase="domain") - Build domain model from slices
    #   2. Review domain model at generated/{solution}/ddd/domain/
    #   3. batch_codegen(phase="contract") - Generate OpenAPI from domain
    #   4. batch_codegen(phase="code") - Generate Clean Architecture code
    {
        "name": "batch_codegen",
        "description": "[codegen] ESSENTIAL for large-scale migrations. DDD-First workflow: phase='domain' builds domain model → phase='contract' generates OpenAPI → phase='code' generates implementation. Use phase='all' to run entire pipeline. For 100+ slices, always use batch_codegen instead of builder_generate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "config_path": {
                    "type": "string",
                    "description": "Path to codegen config JSON file (default: config/codegen.json)",
                },
                "phase": {
                    "type": "string",
                    "enum": ["domain", "gherkin", "contract", "code", "all"],
                    "description": "DDD workflow phase: 'domain'=build domain model, 'contract'=generate OpenAPI, 'code'=generate implementation, 'all'=run complete pipeline (default: all)",
                },
                "batch_size": {
                    "type": "integer",
                    "description": "Number of slices to process per batch (default: 500)",
                },
                "start_batch": {
                    "type": "integer",
                    "description": "Batch number to start from, for resumption (default: 0)",
                },
                "max_batches": {
                    "type": "integer",
                    "description": "Maximum number of batches to process (optional, default: all)",
                },
                "cleanup_first": {
                    "type": "boolean",
                    "description": "Delete existing generated files before starting (default: false)",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to actually run (preview mode if false)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "cleanup_generated",
        "description": "[codegen] Delete all generated files for a solution. Use this BEFORE batch_codegen when user wants a fresh regeneration, or to fix issues with previous generation. Always call with confirm=false first to preview what will be deleted.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution to clean up (e.g., 'NopCommerce')",
                },
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to actually delete files (preview mode if false)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "get_batch_status",
        "description": "[codegen] Check generation progress and results. Shows total files, .cs files, .feature files, and directory structure. Use this to: 1) Monitor ongoing batch_codegen progress, 2) Verify generation completed successfully, 3) Check what was generated before cleanup.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution to check",
                },
            },
            "required": ["solution_name"],
        },
    },
    # === BATCH DDD ANALYSIS (Copilot-driven with rate limiting) ===
    # For large codebases with 100+ slices, use batch_ddd_analysis instead of
    # individual ddd_get_analysis_prompt calls. This handles:
    # - Rate limiting to avoid LLM throttling
    # - Progress checkpointing for resumption
    # - Automatic batching of slices
    {
        "name": "batch_ddd_analysis",
        "description": "[DDD-Batch] ESSENTIAL for large codebases. Prepares batches of slices for Copilot-driven DDD analysis with rate limiting. Returns prompts for the current batch. After analyzing each slice, call batch_ddd_apply_slice with the results. Use this instead of ddd_analyze_all_endpoints when you have 100+ slices.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution being analyzed (e.g., 'NopCommerce')",
                },
                "batch_size": {
                    "type": "integer",
                    "description": "Number of slices per batch (default: 50, recommended: 20-100)",
                },
                "start_batch": {
                    "type": "integer",
                    "description": "Batch number to start from, for resumption (default: 0)",
                },
                "max_batches": {
                    "type": "integer",
                    "description": "Maximum batches to process in this call (optional)",
                },
                "min_depth": {
                    "type": "integer",
                    "description": "Minimum slice depth to include (default: 0)",
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum slice depth to include (default: 10)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "batch_ddd_apply_slice",
        "description": "[DDD-Batch] Apply DDD analysis for a single slice from batch processing. Call this after analyzing each slice prompt from batch_ddd_analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution being analyzed",
                },
                "slice_id": {
                    "type": "string",
                    "description": "Slice ID that was analyzed",
                },
                "analysis": {
                    "type": "object",
                    "description": "DDD analysis JSON with aggregate_name, behaviors, domain_events, etc.",
                },
            },
            "required": ["solution_name", "slice_id", "analysis"],
        },
    },
    {
        "name": "batch_ddd_status",
        "description": "[DDD-Batch] Get the current status of batch DDD analysis. Shows how many slices have been analyzed, remaining count, and bounded contexts discovered.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution to check",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "batch_ddd_build_model",
        "description": "[DDD-Batch] Build unified domain model from all analyzed slices. Call this AFTER all slices have been analyzed via batch_ddd_analysis. Synthesizes aggregates, bounded contexts, and ubiquitous language.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name for the solution",
                },
            },
            "required": ["solution_name"],
        },
    },
    # === DDD Progress Tracking (Parquet-based state management) ===
    {
        "name": "ddd_get_job_progress",
        "description": "[DDD-Progress] Get comprehensive progress report for a DDD analysis job. Shows slice counts, batch progress, ETA, and resume capability. Use this to check progress after chat restart.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution (e.g., 'nopcommerce')",
                },
                "job_id": {
                    "type": "string",
                    "description": "Specific job ID (optional, defaults to latest)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_list_pending_slices",
        "description": "[DDD-Progress] List slices that still need analysis. Use this to see what work remains after resuming.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of slices to return (default: 50)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_resume_job",
        "description": "[DDD-Progress] Resume a paused or interrupted DDD analysis job. Automatically picks up from last checkpoint.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution to resume",
                },
                "batch_size": {
                    "type": "integer",
                    "description": "Slices per batch (default: use previous job setting)",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_get_context_summary",
        "description": "[DDD-Progress] Get summary of bounded contexts discovered so far. Use to check progress of domain model building.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution",
                },
            },
            "required": ["solution_name"],
        },
    },
    {
        "name": "ddd_create_job",
        "description": "[DDD-Progress] Create a new DDD analysis job with Parquet-based state tracking. Use this to start fresh analysis with resumable state.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "solution_name": {
                    "type": "string",
                    "description": "Name of the solution",
                },
                "batch_size": {
                    "type": "integer",
                    "description": "Slices per batch (default: 50)",
                },
                "min_depth": {
                    "type": "integer",
                    "description": "Minimum slice depth (default: 0)",
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum slice depth (default: 10)",
                },
            },
            "required": ["solution_name"],
        },
    },
]


class AgentToolHandler:
    """Handler for 3-agent MCP tools."""

    def __init__(self, conn, config) -> None:
        from migration_agents.constants import ensure_directories
        ensure_directories()  # Ensure all standard directories exist
        
        self.conn = conn
        self.config = config

    def _get_symbol_name_for_slice(self, slice_id: str) -> str:
        """Look up the proper method/class name for a slice from the symbols table.
        
        The slice_id is derived from a symbol_id hash. We can find the corresponding
        symbol by joining entry_graphs with symbols using source_ref = symbol_id.
        Falls back to the slice_id if no symbol is found.
        """
        # The slice_id is typically "entry_XXXX" where XXXX is the first 8 chars of the entry_key
        # We need to find the full entry_key and then look up the symbol
        entry_key_prefix = slice_id.replace("entry_", "")
        
        sql = f"""
            SELECT s.name, s.kind, s.file_path
            FROM entry_graphs eg
            JOIN symbols s ON eg.source_ref = s.symbol_id
            WHERE eg.entry_key LIKE '{entry_key_prefix}%'
            AND s.kind IN ('method', 'class', 'function')
            ORDER BY eg.reachable_nodes_count DESC
            LIMIT 1
        """
        try:
            result = self.conn.execute(sql).fetchall()
            if result and result[0][0]:
                return result[0][0]  # Return the symbol name
        except Exception:
            pass
        
        return slice_id  # Fallback to slice_id if lookup fails

    def handle_tool(self, name: str, arguments: dict) -> dict[str, Any]:
        """Route tool call to appropriate handler."""
        handlers = {
            # Discovery
            "discover_tools": self._discover_tools,
            # 01-analyzer (unified tool with step parameter)
            "analyzer": self._analyzer,
            # 02-builder tools
            "builder_generate": self._builder_generate,
            "builder_fix": self._builder_fix,
            # 03-judge tools
            "judge_validate": self._judge_validate,
            # Utility tools
            "clean_pipeline": self._clean_pipeline,
            "pipeline_status": self._pipeline_status,
            "refresh_views": self._refresh_views,
            "get_parse_coverage": self._get_parse_coverage,
            "list_endpoints": self._list_endpoints,
            "list_slices": self._list_slices,
            "get_slice_context": self._get_slice_context,
            # DDD-first tools (single slice)
            "ddd_get_analysis_prompt": self._ddd_get_analysis_prompt,
            "ddd_apply_analysis": self._ddd_apply_analysis,
            "ddd_get_domain_model_prompt": self._ddd_get_domain_model_prompt,
            "ddd_apply_domain_model": self._ddd_apply_domain_model,
            "ddd_generate_gherkin": self._ddd_generate_gherkin,
            "ddd_generate_contract": self._ddd_generate_contract,
            "ddd_run_full_pipeline": self._ddd_run_full_pipeline,
            # Comprehensive DDD analysis (all endpoints)
            "ddd_analyze_all_endpoints": self._ddd_analyze_all_endpoints,
            "ddd_apply_full_analysis": self._ddd_apply_full_analysis,
            "ddd_get_sme_review": self._ddd_get_sme_review,
            "ddd_submit_sme_review": self._ddd_submit_sme_review,
            "ddd_list_bounded_contexts": self._ddd_list_bounded_contexts,
            "ddd_get_ubiquitous_language": self._ddd_get_ubiquitous_language,
            "ddd_validate_coverage": self._ddd_validate_coverage,
            # Validation tools
            "validate_migration": self._validate_migration,
            "get_validation_report": self._get_validation_report,
            "get_coverage_summary": self._get_coverage_summary,
            "create_validation_review": self._create_validation_review,
            "list_validation_fixes": self._list_validation_fixes,
            "apply_validation_fixes": self._apply_validation_fixes,
            "get_validation_history": self._get_validation_history,
            "get_version_history": self._get_version_history,
            "compare_versions": self._compare_versions,
            # Approval workflow tools
            "get_step_for_approval": self._get_step_for_approval,
            "submit_step_approval": self._submit_step_approval,
            "get_approval_status": self._get_approval_status,
            # LLM-powered DDD tools
            "ddd_analyze_with_copilot": self._ddd_analyze_with_copilot,
            # Batch code generation tools
            "batch_codegen": self._batch_codegen,
            "cleanup_generated": self._cleanup_generated,
            "get_batch_status": self._get_batch_status,
            # Batch DDD analysis tools (for large codebases)
            "batch_ddd_analysis": self._batch_ddd_analysis,
            "batch_ddd_apply_slice": self._batch_ddd_apply_slice,
            "batch_ddd_status": self._batch_ddd_status,
            "batch_ddd_build_model": self._batch_ddd_build_model,
            # DDD Progress tracking (Parquet-based state management)
            "ddd_get_job_progress": self._ddd_get_job_progress,
            "ddd_list_pending_slices": self._ddd_list_pending_slices,
            "ddd_resume_job": self._ddd_resume_job,
            "ddd_get_context_summary": self._ddd_get_context_summary,
            "ddd_create_job": self._ddd_create_job,
        }
        handler = handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown agent tool: {name}")
        return handler(arguments)

    # === DISCOVERY ===

    def _discover_tools(self, args: dict) -> dict[str, Any]:
        """Discover all available MCP tools with metadata."""
        agent_filter = args.get("agent", "all")
        category_filter = args.get("category", "all")

        # Tool metadata: maps tool name to agent and category
        tool_metadata = {
            # 01-analyzer tools
            "analyzer": {"agent": "01-analyzer", "category": "analysis"},
            # 02-builder tools
            "builder_generate": {"agent": "02-builder", "category": "codegen"},
            "builder_fix": {"agent": "02-builder", "category": "codegen"},
            # 03-judge tools
            "judge_validate": {"agent": "03-judge", "category": "validation"},
            # Utility tools
            "discover_tools": {"agent": "utility", "category": "utility"},
            "clean_pipeline": {"agent": "utility", "category": "utility"},
            "pipeline_status": {"agent": "utility", "category": "utility"},
            "refresh_views": {"agent": "utility", "category": "utility"},
            "get_parse_coverage": {"agent": "01-analyzer", "category": "analysis"},
            "list_endpoints": {"agent": "utility", "category": "utility"},
            "list_slices": {"agent": "utility", "category": "utility"},
            "get_slice_context": {"agent": "utility", "category": "utility"},
            # DDD tools
            "ddd_get_analysis_prompt": {"agent": "02-builder", "category": "ddd"},
            "ddd_apply_analysis": {"agent": "02-builder", "category": "ddd"},
            "ddd_get_domain_model_prompt": {"agent": "02-builder", "category": "ddd"},
            "ddd_apply_domain_model": {"agent": "02-builder", "category": "ddd"},
            "ddd_generate_gherkin": {"agent": "02-builder", "category": "ddd"},
            "ddd_generate_contract": {"agent": "02-builder", "category": "ddd"},
            "ddd_run_full_pipeline": {"agent": "02-builder", "category": "ddd"},
            "ddd_analyze_all_endpoints": {"agent": "02-builder", "category": "ddd"},
            "ddd_apply_full_analysis": {"agent": "02-builder", "category": "ddd"},
            "ddd_get_sme_review": {"agent": "02-builder", "category": "ddd"},
            "ddd_submit_sme_review": {"agent": "02-builder", "category": "ddd"},
            "ddd_list_bounded_contexts": {"agent": "02-builder", "category": "ddd"},
            "ddd_get_ubiquitous_language": {"agent": "02-builder", "category": "ddd"},
            "ddd_validate_coverage": {"agent": "02-builder", "category": "ddd"},
            "ddd_analyze_with_copilot": {"agent": "02-builder", "category": "ddd"},
            # Batch DDD tools
            "batch_ddd_analysis": {"agent": "02-builder", "category": "batch"},
            "batch_ddd_apply_slice": {"agent": "02-builder", "category": "batch"},
            "batch_ddd_status": {"agent": "02-builder", "category": "batch"},
            "batch_ddd_build_model": {"agent": "02-builder", "category": "batch"},
            "ddd_get_job_progress": {"agent": "02-builder", "category": "batch"},
            "ddd_list_pending_slices": {"agent": "02-builder", "category": "batch"},
            "ddd_resume_job": {"agent": "02-builder", "category": "batch"},
            "ddd_get_context_summary": {"agent": "02-builder", "category": "batch"},
            "ddd_create_job": {"agent": "02-builder", "category": "batch"},
            # Batch codegen tools
            "batch_codegen": {"agent": "02-builder", "category": "batch"},
            "cleanup_generated": {"agent": "02-builder", "category": "batch"},
            "get_batch_status": {"agent": "02-builder", "category": "batch"},
            # Validation tools
            "validate_migration": {"agent": "03-judge", "category": "validation"},
            "get_validation_report": {"agent": "03-judge", "category": "validation"},
            "get_coverage_summary": {"agent": "03-judge", "category": "validation"},
            "create_validation_review": {"agent": "03-judge", "category": "validation"},
            "list_validation_fixes": {"agent": "03-judge", "category": "validation"},
            "apply_validation_fixes": {"agent": "03-judge", "category": "validation"},
            "get_validation_history": {"agent": "03-judge", "category": "validation"},
            "get_version_history": {"agent": "03-judge", "category": "validation"},
            "compare_versions": {"agent": "03-judge", "category": "validation"},
            # Approval tools (shared)
            "get_step_for_approval": {"agent": "utility", "category": "approval"},
            "submit_step_approval": {"agent": "utility", "category": "approval"},
            "get_approval_status": {"agent": "utility", "category": "approval"},
        }

        # Filter and enrich tools
        result_tools = []
        for tool in AGENT_TOOLS:
            name = tool["name"]
            meta = tool_metadata.get(name, {"agent": "unknown", "category": "unknown"})

            # Apply filters
            if agent_filter != "all" and meta["agent"] != agent_filter:
                continue
            if category_filter != "all" and meta["category"] != category_filter:
                continue

            # Extract parameter info
            schema = tool.get("inputSchema", {})
            properties = schema.get("properties", {})
            required = schema.get("required", [])

            params = []
            for param_name, param_def in properties.items():
                params.append({
                    "name": param_name,
                    "type": param_def.get("type", "any"),
                    "description": param_def.get("description", ""),
                    "required": param_name in required,
                    "enum": param_def.get("enum"),
                })

            result_tools.append({
                "name": name,
                "agent": meta["agent"],
                "category": meta["category"],
                "description": tool.get("description", ""),
                "parameters": params,
            })

        # Group by agent for better presentation
        by_agent = {}
        for t in result_tools:
            agent = t["agent"]
            if agent not in by_agent:
                by_agent[agent] = []
            by_agent[agent].append(t)

        # Standard paths - so LLM doesn't need to figure these out
        standard_paths = {
            "01-analyzer": {
                "configs": {
                    "ingest": CONFIG_FILES.INGESTION,
                    "parse": CONFIG_FILES.PARSER,
                    "slice": CONFIG_FILES.SLICE,
                },
                "output": DEFAULT_PARQUET_ROOT,
            },
            "02-builder": {
                "configs": {
                    "codegen": CONFIG_FILES.CODEGEN,
                    "ddd_batch": CONFIG_FILES.DDD_BATCH,
                },
                "output": DEFAULT_GENERATED_ROOT,
            },
            "03-judge": {
                "configs": {
                    "judge": CONFIG_FILES.JUDGE,
                },
                "project_path_pattern": f"{DEFAULT_GENERATED_ROOT}/<solution>-modern/",
            },
            "shared": {
                "lakehouse": DEFAULT_PARQUET_ROOT,
                "generated": DEFAULT_GENERATED_ROOT,
            },
        }

        # Quick start commands
        quick_start = {
            "01-analyzer": [
                f"analyzer step='ingest' config_path='{CONFIG_FILES.INGESTION}' confirm=true",
                f"analyzer step='parse' config_path='{CONFIG_FILES.PARSER}' confirm=true",
                f"analyzer step='slice' config_path='{CONFIG_FILES.SLICE}' confirm=true",
            ],
            "02-builder": [
                "ddd_create_job solution_name='<solution>' batch_size=50",
                "batch_ddd_analysis solution_name='<solution>'",
                "ddd_get_job_progress solution_name='<solution>'",
                f"batch_codegen config_path='{CONFIG_FILES.CODEGEN}' phase='all' confirm=true",
            ],
            "03-judge": [
                f"validate_migration project_path='{DEFAULT_GENERATED_ROOT}/<solution>-modern' output_format='detailed'",
                f"get_coverage_summary project_path='{DEFAULT_GENERATED_ROOT}/<solution>-modern'",
            ],
        }

        # State management - Parquet-based, survives chat restarts
        state_management = {
            "state_location": str(DEFAULT_PATHS.PIPELINE_STATE) + "/",
            "state_files": {
                "pipeline_steps": STATE_FILES.PIPELINE_STEPS,
                "ddd_jobs": STATE_FILES.DDD_JOBS,
                "ddd_slices": STATE_FILES.DDD_SLICES,
                "codegen": STATE_FILES.CODEGEN,
                "validation": STATE_FILES.VALIDATION,
                "approval": STATE_FILES.APPROVAL,
            },
            "pipeline_steps": PIPELINE_STEPS.ALL,
            "step_statuses": STEP_STATUS.ALL,
            "check_state_tools": {
                "pipeline": "pipeline_status",
                "ddd_progress": "ddd_get_job_progress solution_name='<solution>'",
                "pending_slices": "ddd_list_pending_slices solution_name='<solution>'",
                "batch_status": "get_batch_status solution_name='<solution>'",
                "approval_status": f"get_approval_status project_path='{DEFAULT_GENERATED_ROOT}/<solution>-modern'",
            },
            "resume_tools": {
                "ddd_job": "ddd_resume_job solution_name='<solution>'",
                "batch_codegen": "batch_codegen start_batch=N confirm=true",
            },
            "note": "All state is Parquet-based. Check state after chat restart to resume.",
        }

        return {
            "total_tools": len(result_tools),
            "filters_applied": {"agent": agent_filter, "category": category_filter},
            "standard_paths": standard_paths,
            "quick_start": quick_start,
            "state_management": state_management,
            "tools_by_agent": by_agent,
            "tools": result_tools,
            "workflow_hint": "Start with analyzer (ingest→parse→slice), then DDD analysis, then codegen, finally validation",
        }

    # === 01-ANALYZER: Unified analysis tool (Stages 0-3) ===

    def _analyzer(self, args: dict) -> dict[str, Any]:
        """[01-analyzer] Unified analysis tool - routes to appropriate step handler."""
        step = args.get("step")
        if not step:
            # Show available steps if none specified
            return {
                "status": "step_required",
                "message": "Please specify which analysis step to run",
                "available_steps": [
                    {"step": "ingest", "name": "Step 1: Ingest", "description": "Ingest legacy source files into the lakehouse"},
                    {"step": "parse", "name": "Step 2: Parse", "description": "Parse source files to extract symbols, calls, data access"},
                    {"step": "slice", "name": "Step 3: Slice", "description": "Build vertical feature slices by depth workflows"},
                ],
                "followups": [
                    {"label": "📥 Run Ingest (Step 1)", "prompt": "Run analyzer with step='ingest' source_path='<path>'"},
                    {"label": "⚙️ Run Parse (Step 2)", "prompt": "Run analyzer with step='parse'"},
                    {"label": "🔪 Run Slice (Step 3)", "prompt": "Run analyzer with step='slice'"},
                ],
                "quick_actions": {
                    "ingest": "analyzer step='ingest' source_path='<path>'",
                    "parse": "analyzer step='parse' confirm=true",
                    "slice": "analyzer step='slice' confirm=true",
                },
            }
        
        step_handlers = {
            "ingest": self._analyzer_ingest,
            "parse": self._analyzer_parse,
            "slice": self._analyzer_slice,
        }
        
        handler = step_handlers.get(step)
        if not handler:
            return {
                "status": "invalid_step",
                "message": f"Unknown step: {step}",
                "valid_steps": ["ingest", "parse", "slice"],
            }
        
        return handler(args)

    def _analyzer_ingest(self, args: dict) -> dict[str, Any]:
        """[01-analyzer] Stage 0: Ingest legacy source files into the lakehouse."""
        source_path = args.get("source_path")
        config_path = args.get("config_path", "config/ingestion.json")
        confirm = args.get("confirm", False)
        
        # Determine ingestion mode (full vs incremental)
        ingestion_mode = args.get("ingestion_mode", "incremental")
        flush_all = args.get("flush_all", False)
        
        # Handle deprecated flush_all parameter
        if flush_all:
            ingestion_mode = "full"
        
        # Handle deprecated incremental parameter
        if args.get("incremental") is True:
            ingestion_mode = "incremental"
        
        # Load config file and build overrides
        config = _load_config(config_path)
        overrides = {}
        if source_path:
            overrides["input_root"] = source_path
        if args.get("output_root"):
            overrides["output_root"] = args["output_root"]
        if args.get("artifact_version") is not None:
            overrides["artifact_version"] = args["artifact_version"]
        # Set incremental based on mode
        overrides["incremental"] = (ingestion_mode == "incremental")
        if args.get("exclude_dirs"):
            overrides["exclude_dirs"] = args["exclude_dirs"]
        if args.get("exclude_extensions"):
            overrides["exclude_extensions"] = args["exclude_extensions"]

        # Merge config with overrides for preview
        merged = _merge_config(config, overrides)
        
        # Key settings to show in preview
        preview = {
            "input_root": merged.get("input_root", source_path),
            "output_root": merged.get("output_root", DEFAULT_PARQUET_ROOT),
            "artifact_version": merged.get("artifact_version", 1),
            "ingestion_mode": ingestion_mode,
            "flush_all": ingestion_mode == "full",
            "exclude_dirs": merged.get("exclude_dirs", [])[:5],  # Show first 5
            "exclude_extensions": merged.get("exclude_extensions", [])[:5],  # Show first 5
            "max_lines_per_chunk": merged.get("max_lines_per_chunk", 200),
            "workers": merged.get("workers", "auto"),
        }

        # Check ingestion state
        state = load_state("ingestion")
        if state and state.get("status") == "finished":
            # Get summary of ingested artifacts
            sql = """
                SELECT 
                    (SELECT COUNT(*) FROM source_index) as files_count,
                    (SELECT COUNT(*) FROM source_chunks) as chunks_count
            """
            try:
                result = self.conn.execute(sql).fetchdf().to_dict(orient="records")[0]
            except Exception:
                result = {}

            return {
                "stage": "0-ingestion",
                "status": "ingestion_complete",
                "source_path": source_path,
                "artifacts": result,
                "next_step": "Run analyzer step='parse' to extract symbols and calls",
            }

        # Build command with flush step if full mode
        flush_command = None
        if ingestion_mode == "full":
            flush_command = "python tools/clean_ingestion_artifacts.py --flush-all --execute"
        
        override_args = ""
        if overrides:
            override_args = f" --overrides '{json.dumps(overrides)}'"
        ingest_command = f"python -m migration_agents.ingestion.main --config {config_path}{override_args}"
        
        # Combined command for full mode
        if ingestion_mode == "full":
            command = f"{flush_command} && {ingest_command}"
        else:
            command = ingest_command

        # Pipeline overview - 3 agents, 6 steps with fix loop
        pipeline_steps = {
            "01-analyzer (one-time)": [
                {"step": 1, "name": "Ingest", "tool": "analyzer step=ingest", "status": "⏳ current"},
                {"step": 2, "name": "Parse", "tool": "analyzer step=parse", "status": "⬜ pending"},
                {"step": 3, "name": "Slice", "tool": "analyzer step=slice", "status": "⬜ pending → handoff"},
            ],
            "02-builder ↔ 03-judge (per-slice fix loop)": [
                {"step": "5a", "name": "Generate", "tool": "builder_generate", "status": "⬜ pending", "approval": "🔐 human approval on retry"},
                {"step": "5b", "name": "Validate", "tool": "judge_validate", "status": "⬜ pending", "approval": "🔐 human approval on re-validation"},
                {"step": "5c", "name": "Fix", "tool": "builder_fix", "status": "⬜ if issues found", "approval": "🔐 ALWAYS requires human approval"},
                {"step": "5d", "name": "Re-validate", "tool": "judge_validate", "status": "⬜ loop until ✅"},
            ],
        }
        fix_loop_note = "Fix loop: builder_generate → judge_validate → (if issues) → 🔐 builder_fix (human approval) → judge_validate → repeat until ✅"

        # All available parameters for this tool with current values
        all_input_params = {
            "source_path": {
                "value": source_path,
                "type": "string",
                "required": True,
                "description": "Path to legacy source directory to ingest",
            },
            "config_path": {
                "value": config_path,
                "type": "string", 
                "required": False,
                "default": CONFIG_FILES.INGESTION,
                "description": "Path to ingestion configuration file",
            },
            "output_root": {
                "value": merged.get("output_root", DEFAULT_PARQUET_ROOT),
                "type": "string",
                "required": False,
                "default": DEFAULT_PARQUET_ROOT,
                "description": "Output directory for parquet files",
            },
            "artifact_version": {
                "value": merged.get("artifact_version", 1),
                "type": "integer",
                "required": False,
                "default": 1,
                "description": "Artifact version number for this ingestion run",
            },
            "ingestion_mode": {
                "value": ingestion_mode,
                "type": "string",
                "enum": ["full", "incremental"],
                "required": False,
                "default": "incremental",
                "description": "'full' = flush all data and re-ingest; 'incremental' = only changed files",
            },
            "exclude_dirs": {
                "value": merged.get("exclude_dirs", []),
                "count": len(merged.get("exclude_dirs", [])),
                "type": "array",
                "required": False,
                "description": "Directories to exclude from ingestion",
            },
            "exclude_extensions": {
                "value": merged.get("exclude_extensions", []),
                "count": len(merged.get("exclude_extensions", [])),
                "type": "array",
                "required": False,
                "description": "File extensions to exclude from ingestion",
            },
            "max_lines_per_chunk": {
                "value": merged.get("max_lines_per_chunk", 200),
                "type": "integer",
                "required": False,
                "default": 200,
                "description": "Maximum lines per source chunk",
            },
            "workers": {
                "value": merged.get("workers", "auto"),
                "type": "string|integer",
                "required": False,
                "default": "auto",
                "description": "Number of parallel workers",
            },
            "confirm": {
                "value": confirm,
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "Set to true to execute after reviewing parameters",
            },
        }

        # If not confirmed, show preview and ask for confirmation
        if not confirm:
            mode_description = (
                "🔄 FULL MODE: Will flush all existing parquet/duckdb data before ingestion"
                if ingestion_mode == "full"
                else "📈 INCREMENTAL MODE: Will only process new/changed files"
            )
            
            # Build confirmation prompt
            confirm_prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 REVIEW ALL INPUT PARAMETERS BEFORE CONFIRMING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Source Path:        {source_path}
📂 Output Root:        {merged.get("output_root", DEFAULT_PARQUET_ROOT)}
📄 Config File:        {config_path}
🔢 Artifact Version:   {merged.get("artifact_version", 1)}
🔄 Ingestion Mode:     {ingestion_mode.upper()}
📊 Max Lines/Chunk:    {merged.get("max_lines_per_chunk", 200)}
⚡ Workers:            {merged.get("workers", "auto")}
🚫 Excluded Dirs:      {len(merged.get("exclude_dirs", []))} directories
🚫 Excluded Exts:      {len(merged.get("exclude_extensions", []))} extensions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            # Build clickable followup options
            followups = [
                {
                    "id": "confirm_execute",
                    "label": "✅ Confirm & Execute",
                    "prompt": f"Run analyzer step='ingest' with source_path='{source_path}', ingestion_mode='{ingestion_mode}', confirm=true",
                },
                {
                    "id": "switch_to_full",
                    "label": "🔄 Switch to Full Mode",
                    "prompt": f"Run analyzer step='ingest' with source_path='{source_path}', ingestion_mode='full'",
                    "hidden": ingestion_mode == "full",
                },
                {
                    "id": "switch_to_incremental", 
                    "label": "📈 Switch to Incremental Mode",
                    "prompt": f"Run analyzer step='ingest' with source_path='{source_path}', ingestion_mode='incremental'",
                    "hidden": ingestion_mode == "incremental",
                },
                {
                    "id": "change_source",
                    "label": "📁 Change Source Path",
                    "prompt": "Run analyzer step='ingest' with source_path='<enter new path>'",
                },
                {
                    "id": "cancel",
                    "label": "❌ Cancel",
                    "prompt": "Cancel the ingestion",
                },
            ]
            # Filter out hidden options
            visible_followups = [f for f in followups if not f.get("hidden", False)]
            
            result = {
                "stage": "0-ingestion",
                "status": "awaiting_confirmation",
                "message": "⚙️ STEP 1 of 3 (01-analyzer): Ingest Legacy Source",
                "ingestion_mode": mode_description,
                "confirmation_prompt": confirm_prompt,
                "all_parameters": all_input_params,
                "followups": visible_followups,
                "quick_actions": {
                    "confirm": f"analyzer step='ingest' source_path='{source_path}' ingestion_mode='{ingestion_mode}' confirm=true",
                    "full_mode": f"analyzer step='ingest' source_path='{source_path}' ingestion_mode='full'",
                    "incremental_mode": f"analyzer step='ingest' source_path='{source_path}' ingestion_mode='incremental'",
                },
                "pipeline_overview": pipeline_steps,
                "fix_loop": fix_loop_note,
                "current_step": "1 of 3 in 01-analyzer",
                "effective_config": preview,
                "overrides_applied": overrides if overrides else "none",
                "config_file": config_path,
                "command": command,
                "action_required": "👆 Select an option above or type your choice",
            }
            if ingestion_mode == "full" and flush_command:
                result["flush_command"] = flush_command
                result["warning"] = "⚠️ FULL MODE will DELETE all existing parquet/duckdb data!"
            return result

        # Confirmed - return execution instruction with all confirmed parameters
        mode_msg = "(FULL - flushing all data first)" if ingestion_mode == "full" else "(INCREMENTAL)"
        
        # Start pipeline step tracking
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(merged.get("output_root", DEFAULT_PARQUET_ROOT))
        run_id = resolve_run_id(parquet_root) or f"run_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        pipeline_step = state_mgr.start_pipeline_step(
            step_name="ingest",
            solution_name=Path(source_path).name if source_path else "",
            config={"source_path": source_path, "mode": ingestion_mode},
        )
        
        confirmed_params_summary = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ CONFIRMED PARAMETERS - READY TO EXECUTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Source Path:        {source_path}
📂 Output Root:        {merged.get("output_root", DEFAULT_PARQUET_ROOT)}
📄 Config File:        {config_path}
🔢 Artifact Version:   {merged.get("artifact_version", 1)}
🔄 Ingestion Mode:     {ingestion_mode.upper()}
📊 Max Lines/Chunk:    {merged.get("max_lines_per_chunk", 200)}
⚡ Workers:            {merged.get("workers", "auto")}
🚫 Excluded Dirs:      {len(merged.get("exclude_dirs", []))} directories
🚫 Excluded Exts:      {len(merged.get("exclude_extensions", []))} extensions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        result = {
            "stage": "0-ingestion",
            "status": "ready_to_execute",
            "step_id": pipeline_step.step_id,
            "message": f"✅ STEP 1 of 3 (01-analyzer): Configuration confirmed {mode_msg}. Execute the command below:",
            "confirmed_parameters": confirmed_params_summary,
            "all_parameters": all_input_params,
            "ingestion_mode": ingestion_mode,
            "current_step": "1 of 3 in 01-analyzer",
            "effective_config": preview,
            "command": command,
            "instruction": f"Run: {command}",
            "next_step": "After completion, run analyzer step='parse' (step 2 of 3)",
            "post_execution": "After command completes, views are automatically refreshed on next query.",
        }
        if ingestion_mode == "full" and flush_command:
            result["flush_command"] = flush_command
            result["steps"] = [
                f"1. Flush existing data: {flush_command}",
                f"2. Run ingestion: {ingest_command}",
            ]
        return result

    def _analyzer_parse(self, args: dict) -> dict[str, Any]:
        """[01-analyzer] Stage 2: Parse source files and emit lakehouse tables.
        
        Supports Roslyn integration for C#/VB.NET semantic analysis:
        - roslyn_cmd: Command to run Roslyn analyzer
        - roslyn_timeout_sec: Timeout for Roslyn execution
        - roslyn_parquet_root: Pre-computed Roslyn output for incremental runs
        """
        config_path = args.get("config_path", "config/parser.json")
        confirm = args.get("confirm", False)

        # Load config and build overrides
        config = _load_config(config_path)
        overrides = {}
        if args.get("artifact_version") is not None:
            overrides["artifact_version"] = args["artifact_version"]
        if args.get("entry_graph_incremental") is not None:
            overrides["entry_graph_incremental"] = args["entry_graph_incremental"]
        if args.get("entry_graph_render_svg") is not None:
            overrides["entry_graph_render_svg"] = args["entry_graph_render_svg"]
        
        # Roslyn overrides for C#/VB.NET semantic analysis
        if args.get("roslyn_cmd") is not None:
            overrides["roslyn_cmd"] = args["roslyn_cmd"]
        if args.get("roslyn_timeout_sec") is not None:
            overrides["roslyn_timeout_sec"] = args["roslyn_timeout_sec"]
        if args.get("roslyn_parquet_root") is not None:
            overrides["roslyn_parquet_root"] = args["roslyn_parquet_root"]

        # Merge for preview
        merged = _merge_config(config, overrides)
        roslyn_configured = merged.get("roslyn_cmd") is not None or merged.get("roslyn_parquet_root") is not None
        preview = {
            "artifact_version": merged.get("artifact_version", 1),
            "entry_graph_incremental": merged.get("entry_graph_incremental", True),
            "entry_graph_render_svg": merged.get("entry_graph_render_svg", False),
            "entry_graph_render_dot": merged.get("entry_graph_render_dot", False),
            "parquet_root": merged.get("parquet_root", DEFAULT_PARQUET_ROOT),
            "roslyn_enabled": roslyn_configured,
            "roslyn_cmd": merged.get("roslyn_cmd"),
            "roslyn_timeout_sec": merged.get("roslyn_timeout_sec", 60),
        }

        # Check if ingestion is done first
        ingestion_state = load_state("ingestion")
        if not ingestion_state or ingestion_state.get("status") != "finished":
            return {
                "stage": "2-parser",
                "status": "blocked",
                "reason": "Ingestion not complete. Run analyzer step='ingest' first.",
            }

        # Check parser state
        state = load_state("parser")
        if state and state.get("status") == "finished":
            # Get summary of parsed artifacts
            sql = """
                SELECT 
                    (SELECT COUNT(*) FROM symbols) as symbols_count,
                    (SELECT COUNT(*) FROM calls) as calls_count,
                    (SELECT COUNT(*) FROM data_access) as data_access_count,
                    (SELECT COUNT(*) FROM conditions) as conditions_count,
                    (SELECT COUNT(*) FROM constants) as constants_count
            """
            try:
                result = self.conn.execute(sql).fetchdf().to_dict(orient="records")[0]
            except Exception:
                result = {}

            return {
                "stage": "2-parser",
                "status": "parser_complete",
                "config_path": config_path,
                "artifacts": result,
                "next_step": "Run analyzer step='slice' to create vertical slices",
            }

        # Build command
        override_args = ""
        if overrides:
            override_args = f" --overrides '{json.dumps(overrides)}'"
        command = f"python -m migration_agents.parser.main --config {config_path}{override_args}"

        # Pipeline overview - 3 agents, 6 steps with fix loop
        pipeline_steps = {
            "01-analyzer (one-time)": [
                {"step": 1, "name": "Ingest", "tool": "analyzer step=ingest", "status": "✅ complete"},
                {"step": 2, "name": "Parse", "tool": "analyzer step=parse", "status": "⏳ current"},
                {"step": 3, "name": "Slice", "tool": "analyzer step=slice", "status": "⬜ pending → handoff"},
            ],
            "02-builder ↔ 03-judge (per-slice fix loop)": [
                {"step": "5a", "name": "Generate", "tool": "builder_generate", "status": "⬜ pending", "approval": "🔐 human approval on retry"},
                {"step": "5b", "name": "Validate", "tool": "judge_validate", "status": "⬜ pending", "approval": "🔐 human approval on re-validation"},
                {"step": "5c", "name": "Fix", "tool": "builder_fix", "status": "⬜ if issues found", "approval": "🔐 ALWAYS requires human approval"},
                {"step": "5d", "name": "Re-validate", "tool": "judge_validate", "status": "⬜ loop until ✅"},
            ],
        }
        fix_loop_note = "Fix loop: builder_generate → judge_validate → (if issues) → 🔐 builder_fix (human approval) → judge_validate → repeat until ✅"

        # All available parameters including Roslyn
        available_params = {
            "config_path": {"type": "string", "required": False, "default": "config/parser.json", "current": config_path},
            "artifact_version": {"type": "integer", "required": False, "default": 1, "current": merged.get("artifact_version", 1)},
            "entry_graph_incremental": {"type": "boolean", "required": False, "default": True, "current": merged.get("entry_graph_incremental", True)},
            "entry_graph_render_svg": {"type": "boolean", "required": False, "default": False, "current": merged.get("entry_graph_render_svg", False)},
            "roslyn_cmd": {"type": "array", "required": False, "default": None, "current": merged.get("roslyn_cmd"), "description": "Command for C#/VB.NET semantic analysis"},
            "roslyn_timeout_sec": {"type": "integer", "required": False, "default": 60, "current": merged.get("roslyn_timeout_sec", 60)},
            "roslyn_parquet_root": {"type": "string", "required": False, "default": None, "current": merged.get("roslyn_parquet_root"), "description": "Pre-computed Roslyn output"},
            "confirm": {"type": "boolean", "required": False, "default": False, "description": "Set true to execute"},
        }

        # Roslyn status message
        roslyn_status = "✅ Enabled" if roslyn_configured else "❌ Disabled (call resolution limited)"
        roslyn_hint = "" if roslyn_configured else "\n⚠️  Enable Roslyn for deep C#/VB.NET call resolution: roslyn_cmd=['dotnet', 'run', '--project', 'path/to/RoslynAnalyzer']"

        # If not confirmed, show preview
        if not confirm:
            confirm_prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 PARSER CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Config File:           {config_path}
🔢 Artifact Version:      {merged.get("artifact_version", 1)}
📈 Incremental:           {merged.get("entry_graph_incremental", True)}
🖼️ Render SVG:            {merged.get("entry_graph_render_svg", False)}
📂 Parquet Root:          {merged.get("parquet_root", DEFAULT_PARQUET_ROOT)}

🔬 ROSLYN (C#/VB.NET):    {roslyn_status}
   Command:               {merged.get("roslyn_cmd") or "Not configured"}
   Timeout:               {merged.get("roslyn_timeout_sec", 60)}s
{roslyn_hint}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            followups = [
                {"label": "✅ Confirm & Execute", "prompt": "Run analyzer step='parse' with confirm=true"},
                {"label": "🖼️ Enable SVG Rendering", "prompt": "Run analyzer step='parse' with entry_graph_render_svg=true"},
                {"label": "🔬 Enable Roslyn", "prompt": "Run analyzer step='parse' with roslyn_cmd=['dotnet', 'run', '--project', 'RoslynAnalyzer'] confirm=true"},
                {"label": "❌ Cancel", "prompt": "Cancel the parse operation"},
            ]
            return {
                "stage": "2-parser",
                "status": "awaiting_confirmation",
                "message": "⚙️ STEP 2 of 3 (01-analyzer): Parse Legacy Source",
                "confirmation_prompt": confirm_prompt,
                "followups": followups,
                "quick_actions": {
                    "confirm": "analyzer step='parse' confirm=true",
                    "with_svg": "analyzer step='parse' entry_graph_render_svg=true confirm=true",
                },
                "pipeline_overview": pipeline_steps,
                "fix_loop": fix_loop_note,
                "current_step": "2 of 3 in 01-analyzer",
                "available_parameters": available_params,
                "effective_config": preview,
                "overrides_applied": overrides if overrides else "none",
                "config_file": config_path,
                "command": command,
                "action_required": "👆 Select an option above or confirm to proceed",
            }

        # Start pipeline step tracking
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(merged.get("parquet_root", DEFAULT_PARQUET_ROOT))
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        pipeline_step = state_mgr.start_pipeline_step(
            step_name="parse",
            config={"config_path": config_path, "roslyn_enabled": roslyn_configured},
        )
        
        return {
            "stage": "2-parser",
            "status": "ready_to_execute",
            "step_id": pipeline_step.step_id,
            "message": "✅ STEP 2 of 3 (01-analyzer): Configuration confirmed. Execute the command below:",
            "current_step": "2 of 3 in 01-analyzer",
            "effective_config": preview,
            "command": command,
            "instruction": f"Run: {command}",
            "next_step": "After completion, run analyzer step='slice' (step 3 of 3, then handoff)",
        }

    def _analyzer_slice(self, args: dict) -> dict[str, Any]:
        """[01-analyzer] Step 3: Build vertical slices by depth workflows."""
        config_path = args.get("config_path", "config/slice.json")
        endpoint = args.get("endpoint")  # Optional - if omitted, processes all by depth
        depth = args.get("depth", 10)
        min_depth = args.get("min_depth", 0)
        slicing_mode = args.get("slicing_mode", "auto")
        confirm = args.get("confirm", False)

        # Load config and build overrides
        config = _load_config(config_path)
        overrides = {}
        if endpoint:
            overrides["endpoint"] = endpoint
        if args.get("depth") is not None:
            overrides["max_depth"] = depth
        if args.get("min_depth") is not None:
            overrides["min_depth"] = min_depth
        if args.get("slicing_mode") is not None:
            overrides["slicing_mode"] = slicing_mode

        # Merge for preview
        merged = _merge_config(config, overrides)
        preview = {
            "endpoint": endpoint or "all endpoints",
            "max_depth": merged.get("max_depth", depth),
            "min_depth": merged.get("min_depth", min_depth),
            "parquet_root": merged.get("parquet_root", DEFAULT_PARQUET_ROOT),
            "slicing_mode": merged.get("slicing_mode", slicing_mode),
        }

        # Check if parser is done first
        parser_state = load_state("parser")
        if not parser_state or parser_state.get("status") != "finished":
            return {
                "stage": "3-slice",
                "status": "blocked",
                "reason": "Parser not complete. Run analyzer step='parse' first.",
            }

        # Check slice_extractor state
        slice_state = load_state("slice_extractor")
        if slice_state and slice_state.get("status") == "finished":
            # Get summary of all slices
            sql = """
                SELECT COUNT(*) as slice_count, 
                       COUNT(DISTINCT endpoint) as endpoint_count
                FROM slice_manifest
            """
            try:
                summary = self.conn.execute(sql).fetchdf().to_dict(orient="records")[0]
            except Exception:
                summary = {}

            return {
                "stage": "3-slice",
                "status": "slicing_complete",
                "slices_generated": summary.get("slice_count", 0),
                "endpoints_covered": summary.get("endpoint_count", 0),
                "next_step": "Handoff to 02-builder: Run builder_generate for each slice, or list_slices to see available slices",
            }

        # If specific endpoint requested, check for that slice
        if endpoint:
            sql = f"""
                SELECT slice_id, endpoint, status, created_at
                FROM slice_manifest
                WHERE endpoint = '{endpoint}'
                ORDER BY created_at DESC
                LIMIT 1
            """
            try:
                result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
            except Exception:
                result = []

            if result:
                slice_info = result[0]
                return {
                    "stage": "3-slice",
                    "status": "slice_exists",
                    "slice_id": slice_info.get("slice_id"),
                    "endpoint": endpoint,
                    "next_step": f"Handoff to 02-builder: Run builder_generate with slice_id={slice_info.get('slice_id')}",
                }

        # Build command
        override_args = ""
        if overrides:
            override_args = f" --overrides '{json.dumps(overrides)}'"
        command = f"python -m migration_agents.slice_extractor.main --config {config_path}{override_args}"

        # Pipeline overview - 3 agents, 6 steps with fix loop
        pipeline_steps = {
            "01-analyzer (one-time)": [
                {"step": 1, "name": "Ingest", "tool": "analyzer step=ingest", "status": "✅ complete"},
                {"step": 2, "name": "Parse", "tool": "analyzer step=parse", "status": "✅ complete"},
                {"step": 3, "name": "Slice", "tool": "analyzer step=slice", "status": "⏳ current → handoff"},
            ],
            "02-builder ↔ 03-judge (per-slice fix loop)": [
                {"step": "5a", "name": "Generate", "tool": "builder_generate", "status": "⬜ pending", "approval": "🔐 human approval on retry"},
                {"step": "5b", "name": "Validate", "tool": "judge_validate", "status": "⬜ pending", "approval": "🔐 human approval on re-validation"},
                {"step": "5c", "name": "Fix", "tool": "builder_fix", "status": "⬜ if issues found", "approval": "🔐 ALWAYS requires human approval"},
                {"step": "5d", "name": "Re-validate", "tool": "judge_validate", "status": "⬜ loop until ✅"},
            ],
        }
        fix_loop_note = "Fix loop: builder_generate → judge_validate → (if issues) → 🔐 builder_fix (human approval) → judge_validate → repeat until ✅"

        # All available parameters
        available_params = {
            "config_path": {"type": "string", "required": False, "default": "config/slice.json", "current": config_path},
            "endpoint": {"type": "string", "required": False, "default": "all", "current": endpoint or "all endpoints"},
            "depth": {"type": "integer", "required": False, "default": 10, "current": depth},
            "min_depth": {"type": "integer", "required": False, "default": 0, "current": min_depth},
            "confirm": {"type": "boolean", "required": False, "default": False, "description": "Set true to execute"},
        }

        # If not confirmed, show preview
        if not confirm:
            confirm_prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 SLICE CONFIGURATION - FINAL STEP BEFORE HANDOFF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Config File:           {config_path}
🎯 Endpoint:              {endpoint or "all endpoints"}
📊 Max Depth:             {merged.get("max_depth", depth)}
📉 Min Depth:             {merged.get("min_depth", min_depth)}
📂 Parquet Root:          {merged.get("parquet_root", DEFAULT_PARQUET_ROOT)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ After this step: HANDOFF to 02-builder ↔ 03-judge fix loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            followups = [
                {"label": "✅ Confirm & Execute All", "prompt": "Run analyzer step='slice' with confirm=true"},
                {"label": "🎯 Slice Specific Endpoint", "prompt": "Run analyzer step='slice' with endpoint='<endpoint_name>' confirm=true"},
                {"label": "📋 List Endpoints First", "prompt": "Run list_endpoints to see available endpoints"},
                {"label": "❌ Cancel", "prompt": "Cancel the slice operation"},
            ]
            return {
                "stage": "3-slice",
                "status": "awaiting_confirmation",
                "message": "⚙️ STEP 3 of 3 (01-analyzer): Build Vertical Slices - FINAL STEP before handoff!",
                "confirmation_prompt": confirm_prompt,
                "followups": followups,
                "quick_actions": {
                    "confirm_all": "analyzer step='slice' confirm=true",
                    "list_endpoints": "list_endpoints",
                },
                "pipeline_overview": pipeline_steps,
                "fix_loop": fix_loop_note,
                "current_step": "3 of 3 in 01-analyzer (last one-time step)",
                "available_parameters": available_params,
                "effective_config": preview,
                "overrides_applied": overrides if overrides else "none",
                "config_file": config_path,
                "command": command,
                "action_required": "👆 Select an option above or confirm to proceed",
                "handoff_note": "After this step, HANDOFF to 02-builder ↔ 03-judge fix loop for per-slice processing",
            }

        # Start pipeline step tracking
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(merged.get("parquet_root", DEFAULT_PARQUET_ROOT))
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        pipeline_step = state_mgr.start_pipeline_step(
            step_name="slice",
            config={"config_path": config_path, "endpoint": endpoint, "depth": depth, "slicing_mode": slicing_mode},
        )
        
        return {
            "stage": "3-slice",
            "status": "ready_to_execute",
            "step_id": pipeline_step.step_id,
            "message": "✅ STEP 3 of 3 (01-analyzer): Configuration confirmed. Execute the command below:",
            "current_step": "3 of 3 in 01-analyzer",
            "effective_config": preview,
            "command": command,
            "instruction": f"Run: {command}",
            "next_step": "HANDOFF: After completion, invoke @02-builder with builder_generate for each slice",
            "fix_loop": fix_loop_note,
        }

    # === 02-BUILDER: Per-slice code generation ===

    def _builder_generate(self, args: dict) -> dict[str, Any]:
        """[02-builder] Generate code artifacts from a slice."""
        slice_id = args.get("slice_id")
        target_framework = args.get("target_framework", "dotnet8")
        generate_tests = args.get("generate_tests", True)
        confirm = args.get("confirm", False)
        is_retry = args.get("is_retry", False)  # True if this is after a fix

        # If no slice_id, suggest batch_codegen for large-scale operations
        if not slice_id:
            # Count total slices
            try:
                count_sql = """
                    SELECT COUNT(*) as cnt FROM entry_graphs WHERE capped_depth >= 1
                """
                result = self.conn.execute(count_sql).fetchone()
                total_slices = result[0] if result else 0
            except Exception:
                total_slices = 0
            
            if total_slices > 100:
                return {
                    "status": "suggest_batch",
                    "message": f"Found {total_slices} slices. For large-scale code generation, use batch_codegen instead.",
                    "total_slices": total_slices,
                    "recommendation": "batch_codegen",
                    "suggested_command": "batch_codegen(batch_size=500, cleanup_first=true, confirm=true)",
                    "alternative": "Provide a specific slice_id to generate just one slice",
                }
            return {
                "status": "error",
                "message": "slice_id is required. Use list_slices to find available slices.",
            }

        # Check for existing artifacts
        sql = f"""
            SELECT artifact_type, COUNT(*) as count
            FROM code_artifacts
            WHERE slice_id = '{slice_id}'
            GROUP BY artifact_type
        """
        try:
            result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            result = []

        # Check if there were previous validation failures
        fix_sql = f"""
            SELECT COUNT(*) as fix_count 
            FROM fix_queue 
            WHERE slice_id = '{slice_id}'
        """
        try:
            fix_history = self.conn.execute(fix_sql).fetchdf().to_dict(orient="records")[0]
            has_fix_history = fix_history.get("fix_count", 0) > 0
        except Exception:
            has_fix_history = False

        if result:
            return {
                "stage": "5a-builder-generate",
                "status": "artifacts_exist",
                "slice_id": slice_id,
                "artifacts": result,
                "next_step": f"Handoff to 03-judge: Run judge_validate with slice_id={slice_id}",
            }

        # Build preview
        preview = {
            "slice_id": slice_id,
            "target_framework": target_framework,
            "generate_tests": generate_tests,
            "is_retry": is_retry,
            "has_previous_fixes": has_fix_history,
        }

        available_params = {
            "slice_id": {"type": "string", "required": True, "current": slice_id},
            "target_framework": {"type": "string", "required": False, "default": "dotnet8", "current": target_framework},
            "generate_tests": {"type": "boolean", "required": False, "default": True, "current": generate_tests},
            "is_retry": {"type": "boolean", "required": False, "default": False, "description": "Set true if regenerating after fix"},
            "confirm": {"type": "boolean", "required": False, "default": False, "description": "Human approval to proceed"},
        }

        command = f"python -m migration_agents.codegen.main --config config/codegen.json --slice {slice_id}"

        # Human-in-the-loop: require confirmation, especially for retries
        if not confirm:
            message = "⚙️ GENERATE CODE: First-time generation for this slice"
            if is_retry or has_fix_history:
                message = "🔄 RETRY GENERATION: Re-generating after fix - HUMAN APPROVAL REQUIRED"
            
            confirm_prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 CODE GENERATION - {"RETRY" if is_retry or has_fix_history else "NEW"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 Slice ID:              {slice_id}
🎯 Target Framework:      {target_framework}
🧪 Generate Tests:        {generate_tests}
🔄 Is Retry:              {is_retry or has_fix_history}
📜 Has Fix History:       {has_fix_history}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            followups = [
                {"label": "✅ Confirm & Generate", "prompt": f"Run builder_generate with slice_id='{slice_id}' confirm=true"},
                {"label": "🎯 Change Framework", "prompt": f"Run builder_generate with slice_id='{slice_id}' target_framework='springboot3'"},
                {"label": "⏭️ Skip This Slice", "prompt": "Skip this slice and list_slices status='pending'"},
                {"label": "📋 View Slice Context", "prompt": f"Run get_slice_context with slice_id='{slice_id}'"},
                {"label": "❌ Cancel", "prompt": "Cancel code generation"},
            ]
            return {
                "stage": "5a-builder-generate",
                "status": "awaiting_human_approval",
                "message": message,
                "confirmation_prompt": confirm_prompt,
                "followups": followups,
                "quick_actions": {
                    "confirm": f"builder_generate slice_id='{slice_id}' confirm=true",
                    "dotnet8": f"builder_generate slice_id='{slice_id}' target_framework='dotnet8' confirm=true",
                    "springboot3": f"builder_generate slice_id='{slice_id}' target_framework='springboot3' confirm=true",
                    "skip": "list_slices status='pending'",
                },
                "human_action_required": True,
                "is_retry": is_retry or has_fix_history,
                "available_parameters": available_params,
                "effective_config": preview,
                "command": command,
                "action_required": "👆 Select an option above to proceed",
            }

        return {
            "stage": "5a-builder-generate",
            "status": "ready_to_execute",
            "message": "✅ Human approved. Execute the command below:",
            "effective_config": preview,
            "command": command,
            "instruction": f"Run: {command}",
            "next_step": f"After completion, run judge_validate with slice_id={slice_id}",
        }

    # === 03-JUDGE: Validation and fix loop ===

    def _judge_validate(self, args: dict) -> dict[str, Any]:
        """[03-judge] Validate a slice's artifacts and populate fix_queue."""
        slice_id = args["slice_id"]
        check_coverage = args.get("check_coverage", True)
        check_citations = args.get("check_citations", True)
        confirm = args.get("confirm", False)
        iteration = args.get("iteration", 1)  # Which validation iteration

        # Query for existing judge reports
        sql = f"""
            SELECT report_id, status, findings, created_at
            FROM judge_reports
            WHERE slice_id = '{slice_id}'
            ORDER BY created_at DESC
            LIMIT 1
        """
        try:
            result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            result = []

        # Count how many judge runs have happened for this slice
        count_sql = f"""
            SELECT COUNT(*) as run_count
            FROM judge_reports
            WHERE slice_id = '{slice_id}'
        """
        try:
            run_count = self.conn.execute(count_sql).fetchdf().to_dict(orient="records")[0].get("run_count", 0)
        except Exception:
            run_count = 0

        is_revalidation = run_count > 0 or iteration > 1

        if result:
            report = result[0]
            # Check fix queue
            fix_sql = f"""
                SELECT fix_id, issue_type, status
                FROM fix_queue
                WHERE slice_id = '{slice_id}' AND status = 'pending'
            """
            try:
                fixes = self.conn.execute(fix_sql).fetchdf().to_dict(orient="records")
            except Exception:
                fixes = []

            if fixes:
                # There are pending fixes - show what needs to be fixed and ask for human approval
                first_fix_id = fixes[0]['fix_id']
                followups = [
                    {"label": "🔧 Apply First Fix", "prompt": f"Run builder_fix with fix_id='{first_fix_id}' confirm=true"},
                    {"label": "📋 View All Fixes", "prompt": f"Show all {len(fixes)} pending fixes for slice {slice_id}"},
                    {"label": "⏭️ Skip This Slice", "prompt": f"Skip slice {slice_id} and list_slices status='pending'"},
                    {"label": "✅ Accept Despite Issues", "prompt": f"Override and accept slice {slice_id} despite issues"},
                ]
                return {
                    "stage": "5b-judge-validate",
                    "status": "issues_found",
                    "slice_id": slice_id,
                    "iteration": iteration,
                    "report_id": report.get("report_id"),
                    "findings": report.get("findings"),
                    "pending_fixes": fixes,
                    "pending_fix_count": len(fixes),
                    "human_action_required": True,
                    "message": f"🔍 VALIDATION FOUND {len(fixes)} ISSUE(S) - Human decision required",
                    "followups": followups,
                    "quick_actions": {
                        "apply_fix": f"builder_fix fix_id='{first_fix_id}' confirm=true",
                        "skip": "list_slices status='pending'",
                    },
                    "action_required": "👆 Select an option above to proceed",
                }
            else:
                followups = [
                    {"label": "📋 List Pending Slices", "prompt": "Run list_slices with status='pending'"},
                    {"label": "📊 View Pipeline Status", "prompt": "Run pipeline_status"},
                    {"label": "🎉 View Completed Slices", "prompt": "Run list_slices with status='complete'"},
                ]
                return {
                    "stage": "5b-judge-validate",
                    "status": "passed",
                    "slice_id": slice_id,
                    "iteration": iteration,
                    "report_id": report.get("report_id"),
                    "findings": report.get("findings"),
                    "message": "✅ All validations passed!",
                    "next_step": "Migration complete for this slice. Move to next slice with list_slices(status='pending')",
                    "followups": followups,
                    "quick_actions": {
                        "next_slice": "list_slices status='pending'",
                        "view_status": "pipeline_status",
                    },
                }

        # No existing report - need to run validation
        preview = {
            "slice_id": slice_id,
            "check_coverage": check_coverage,
            "check_citations": check_citations,
            "iteration": iteration,
            "is_revalidation": is_revalidation,
        }

        available_params = {
            "slice_id": {"type": "string", "required": True, "current": slice_id},
            "check_coverage": {"type": "boolean", "required": False, "default": True, "current": check_coverage},
            "check_citations": {"type": "boolean", "required": False, "default": True, "current": check_citations},
            "iteration": {"type": "integer", "required": False, "default": 1, "description": "Current validation iteration"},
            "confirm": {"type": "boolean", "required": False, "default": False, "description": "Human approval to proceed"},
        }

        command = f"python -m migration_agents.judge.main --config config/judge.json --slice {slice_id}"

        # Require confirmation for revalidation (2nd+ iteration)
        if is_revalidation and not confirm:
            confirm_prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 RE-VALIDATION - Iteration {iteration}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 Slice ID:              {slice_id}
✅ Check Coverage:        {check_coverage}
📚 Check Citations:       {check_citations}
🔢 Iteration:             {iteration}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            followups = [
                {"label": "✅ Confirm & Re-validate", "prompt": f"Run judge_validate with slice_id='{slice_id}' iteration={iteration} confirm=true"},
                {"label": "⏭️ Skip This Slice", "prompt": "Skip this slice and list_slices status='pending'"},
                {"label": "❌ Cancel", "prompt": "Cancel re-validation"},
            ]
            return {
                "stage": "5b-judge-validate",
                "status": "awaiting_human_approval",
                "message": f"🔄 RE-VALIDATION (iteration {iteration}): After fix applied - HUMAN APPROVAL REQUIRED",
                "confirmation_prompt": confirm_prompt,
                "followups": followups,
                "quick_actions": {
                    "confirm": f"judge_validate slice_id='{slice_id}' iteration={iteration} confirm=true",
                    "skip": "list_slices status='pending'",
                },
                "human_action_required": True,
                "iteration": iteration,
                "is_revalidation": is_revalidation,
                "available_parameters": available_params,
                "effective_config": preview,
                "command": command,
                "action_required": "👆 Select an option above to proceed",
            }

        # If confirm=true or first validation, run inline
        if confirm or not is_revalidation:
            from migration_agents.judge.main import validate_slice, write_judge_reports
            from migration_agents.shared_run_id import resolve_run_id
            
            parquet_root = Path(self.config.parquet_root)
            run_id = resolve_run_id(parquet_root)
            artifact_version = 1
            
            report = validate_slice(
                parquet_root=parquet_root,
                slice_id=slice_id,
                run_id=run_id,
                artifact_version=artifact_version,
                check_citations=check_citations,
                check_coverage=check_coverage,
            )
            
            # Write the report
            write_judge_reports([report], parquet_root, run_id, artifact_version)
            
            # Note: Views are per-run database now, no refresh needed for same run
            
            followups = [
                {"label": "📋 List Pending Slices", "prompt": "Run list_slices with status='pending'"},
                {"label": "📊 View Pipeline Status", "prompt": "Run pipeline_status"},
            ]
            
            return {
                "stage": "5b-judge-validate",
                "status": report.status,
                "slice_id": slice_id,
                "iteration": iteration,
                "report_id": report.report_id,
                "citation_coverage": report.citation_coverage,
                "rule_coverage": report.rule_coverage,
                "dead_code_deps": report.dead_code_deps,
                "error_count": report.error_count,
                "warning_count": report.warning_count,
                "findings_count": len(report.findings),
                "message": f"✅ Validation {report.status.upper()}" if report.status == "passed" else f"⚠️ Validation {report.status.upper()}",
                "next_step": "Move to next slice with list_slices(status='pending')" if report.status == "passed" else "Review findings and apply fixes",
                "followups": followups,
            }

        return {
            "stage": "5b-judge-validate",
            "status": "ready_to_execute",
            "message": "✅ Ready to validate. Execute the command below:",
            "iteration": iteration,
            "effective_config": preview,
            "command": command,
            "instruction": f"Run: {command}",
        }

    def _pipeline_status(self, args: dict) -> dict[str, Any]:
        """Get status of all pipeline stages with stage numbers."""
        stages = [
            ("1", "ingestion"),
            ("2", "parser"),
            ("2", "vectorization"),
            ("3", "slice_extractor"),
            ("4", "logic_manifester"),
            ("4", "domain_architect"),
            ("4", "knowledge_base"),
            ("4", "api_migration"),
            ("4", "codegen"),
        ]
        status = {}
        for stage_num, stage in stages:
            state = load_state(stage)
            status[f"{stage_num}-{stage}"] = {
                "status": state.get("status") if state else "not_started",
                "run_id": state.get("run_id") if state else None,
            }
        return {"pipeline_status": status}

    def _refresh_views(self, args: dict) -> dict[str, Any]:
        """Refresh DuckDB views - reconnects to the latest run's database."""
        from .duckdb_catalog import get_latest_run_id, connect_for_run
        
        parquet_root = self.config.parquet_root
        run_id_before = get_latest_run_id(parquet_root)
        
        # With per-run databases, "refresh" means reconnecting to latest run
        # This is handled by the server's _ensure_views_fresh()
        # Here we just report current state
        run_id_after = get_latest_run_id(parquet_root)
        
        # Get current view count
        try:
            result = self.conn.execute("SELECT name FROM (SHOW TABLES)").fetchall()
            views = [row[0] for row in result]
        except Exception:
            views = []
        
        return {
            "status": "checked",
            "run_id": run_id_after,
            "views_count": len(views),
            "views": views,
            "changed": run_id_before != run_id_after,
            "message": f"Refreshed {len(views)} views for run {run_id_after}",
        }

    def _get_parse_coverage(self, args: dict) -> dict[str, Any]:
        """Get parse coverage report with warnings and improvement suggestions."""
        show_skipped = args.get("show_skipped", True)
        show_warnings = args.get("show_warnings", True)
        show_uncovered = args.get("show_uncovered", True)
        show_partial = args.get("show_partial", True)
        
        result: dict[str, Any] = {
            "status": "ok",
            "summary": {},
            "by_language": [],
            "skipped_files": [],
            "uncovered_files": [],  # Files parsed but 0 symbols extracted
            "partial_coverage_files": [],  # Files with low symbol coverage
            "warnings": [],
            "suggestions": [],
        }
        
        # Get parse audit summary
        try:
            audit_sql = """
                SELECT 
                    language,
                    status,
                    COUNT(*) as file_count
                FROM parse_audit
                GROUP BY language, status
                ORDER BY file_count DESC
            """
            audit_rows = self.conn.execute(audit_sql).fetchall()
        except Exception as e:
            return {"status": "error", "error": f"Failed to query parse_audit: {e}"}
        
        # Build language coverage stats
        lang_stats: dict[str, dict] = {}
        total_files = 0
        total_ok = 0
        total_error = 0
        total_skip = 0
        
        for lang, status, count in audit_rows:
            if lang not in lang_stats:
                lang_stats[lang] = {"language": lang, "ok": 0, "error": 0, "skip": 0, "uncovered": 0}
            lang_stats[lang][status] = count
            total_files += count
            if status == "ok":
                total_ok += count
            elif status == "error":
                total_error += count
            elif status == "skip":
                total_skip += count
        
        # Get files with 0 symbols (parsed but not covered)
        total_uncovered = 0
        try:
            uncovered_sql = """
                WITH parsed_files AS (
                    SELECT DISTINCT file_path, language
                    FROM parse_audit
                    WHERE status = 'ok'
                ),
                files_with_symbols AS (
                    SELECT DISTINCT file_path
                    FROM symbols
                )
                SELECT 
                    p.language,
                    COUNT(*) as uncovered_count
                FROM parsed_files p
                LEFT JOIN files_with_symbols s ON p.file_path = s.file_path
                WHERE s.file_path IS NULL
                GROUP BY p.language
            """
            uncovered_rows = self.conn.execute(uncovered_sql).fetchall()
            for lang, count in uncovered_rows:
                if lang in lang_stats:
                    lang_stats[lang]["uncovered"] = count
                    total_uncovered += count
        except Exception:
            pass
        
        result["summary"] = {
            "total_files": total_files,
            "parsed_ok": total_ok,
            "parse_errors": total_error,
            "skipped": total_skip,
            "uncovered": total_uncovered,
            "parse_rate": f"{(total_ok / total_files * 100) if total_files > 0 else 0:.1f}%",
            "coverage_rate": f"{((total_ok - total_uncovered) / total_files * 100) if total_files > 0 else 0:.1f}%",
        }
        
        # Get symbols and calls per language
        try:
            symbols_sql = """
                SELECT 
                    CASE 
                        WHEN file_path LIKE '%.cs' THEN 'c_sharp'
                        WHEN file_path LIKE '%.html' OR file_path LIKE '%.aspx' OR file_path LIKE '%.ascx' THEN 'html'
                        WHEN file_path LIKE '%.js' THEN 'javascript'
                        WHEN file_path LIKE '%.css' THEN 'css'
                        WHEN file_path LIKE '%.xml' OR file_path LIKE '%.config' THEN 'xml'
                        ELSE 'other'
                    END as lang,
                    kind,
                    COUNT(*) as count
                FROM symbols
                GROUP BY lang, kind
            """
            symbol_rows = self.conn.execute(symbols_sql).fetchall()
            
            for lang, kind, count in symbol_rows:
                if lang in lang_stats:
                    if "symbols" not in lang_stats[lang]:
                        lang_stats[lang]["symbols"] = 0
                    lang_stats[lang]["symbols"] += count
                    if kind in ("class", "interface", "struct"):
                        if "classes" not in lang_stats[lang]:
                            lang_stats[lang]["classes"] = 0
                        lang_stats[lang]["classes"] += count
                    elif kind in ("method", "function"):
                        if "methods" not in lang_stats[lang]:
                            lang_stats[lang]["methods"] = 0
                        lang_stats[lang]["methods"] += count
        except Exception:
            pass
        
        # Get calls per language
        try:
            calls_sql = """
                SELECT 
                    CASE 
                        WHEN file_path LIKE '%.cs' THEN 'c_sharp'
                        WHEN file_path LIKE '%.html' OR file_path LIKE '%.aspx' THEN 'html'
                        WHEN file_path LIKE '%.js' THEN 'javascript'
                        WHEN file_path LIKE '%.css' THEN 'css'
                        ELSE 'other'
                    END as lang,
                    COUNT(*) as call_count
                FROM calls
                GROUP BY lang
            """
            call_rows = self.conn.execute(calls_sql).fetchall()
            for lang, count in call_rows:
                if lang in lang_stats:
                    lang_stats[lang]["calls"] = count
        except Exception:
            pass
        
        result["by_language"] = list(lang_stats.values())
        
        # Get skipped files if requested
        if show_skipped:
            try:
                skipped_sql = """
                    SELECT file_path, language
                    FROM parse_audit
                    WHERE status = 'skip' OR language = 'text'
                    LIMIT 50
                """
                skipped_rows = self.conn.execute(skipped_sql).fetchall()
                result["skipped_files"] = [
                    {"file_path": row[0], "detected_as": row[1]}
                    for row in skipped_rows
                ]
            except Exception:
                pass
        
        # Get uncovered files (parsed but 0 symbols)
        if show_uncovered:
            try:
                uncovered_files_sql = """
                    WITH parsed_files AS (
                        SELECT DISTINCT file_path, language
                        FROM parse_audit
                        WHERE status = 'ok'
                    ),
                    files_with_symbols AS (
                        SELECT DISTINCT file_path
                        FROM symbols
                    )
                    SELECT 
                        p.file_path,
                        p.language
                    FROM parsed_files p
                    LEFT JOIN files_with_symbols s ON p.file_path = s.file_path
                    WHERE s.file_path IS NULL
                    ORDER BY p.language, p.file_path
                    LIMIT 100
                """
                uncovered_files_rows = self.conn.execute(uncovered_files_sql).fetchall()
                result["uncovered_files"] = [
                    {"file_path": row[0], "language": row[1], "reason": "0 symbols extracted"}
                    for row in uncovered_files_rows
                ]
            except Exception:
                pass
        
        # Get partial coverage files (parsed with some symbols but low coverage)
        if show_partial:
            try:
                partial_sql = """
                    WITH file_stats AS (
                        SELECT 
                            file_path,
                            COUNT(*) as symbol_count,
                            COUNT(CASE WHEN kind = 'method' THEN 1 END) as methods,
                            COUNT(CASE WHEN kind = 'class' THEN 1 END) as classes,
                            COUNT(CASE WHEN kind IN ('property', 'field') THEN 1 END) as members,
                            COUNT(DISTINCT line) as lines_with_symbols
                        FROM symbols
                        GROUP BY file_path
                    ),
                    file_size AS (
                        SELECT 
                            file_path,
                            MAX(line_end) as total_lines
                        FROM intake_source_chunks
                        GROUP BY file_path
                    )
                    SELECT 
                        s.file_path,
                        s.symbol_count,
                        s.methods,
                        s.classes,
                        s.members,
                        s.lines_with_symbols,
                        f.total_lines,
                        ROUND(s.lines_with_symbols * 100.0 / NULLIF(f.total_lines, 0), 1) as coverage_pct,
                        ROUND(s.symbol_count * 100.0 / NULLIF(f.total_lines, 0), 1) as symbol_density
                    FROM file_stats s
                    JOIN file_size f ON s.file_path = f.file_path
                    WHERE s.symbol_count > 0 
                      AND f.total_lines > 50
                      AND (s.lines_with_symbols * 100.0 / NULLIF(f.total_lines, 0)) < 5
                    ORDER BY f.total_lines DESC, coverage_pct ASC
                    LIMIT 50
                """
                partial_rows = self.conn.execute(partial_sql).fetchall()
                result["partial_coverage_files"] = [
                    {
                        "file_path": row[0],
                        "symbols": row[1],
                        "methods": row[2],
                        "classes": row[3],
                        "properties_fields": row[4],
                        "lines_covered": row[5],
                        "total_lines": row[6],
                        "coverage_pct": row[7],
                        "symbol_density": row[8],
                        "issue": "missing properties/fields" if row[4] == 0 and row[2] > 5 else f"Only {row[7]}% coverage"
                    }
                    for row in partial_rows
                ]
            except Exception:
                pass
        
        # Generate warnings and suggestions
        if show_warnings:
            warnings = []
            suggestions = []
            
            # Check for high error rates
            if total_error > 0:
                warnings.append(
                    f"⚠️ {total_error} files failed to parse. Check parse_audit for error details."
                )
            
            # Check for partial coverage issues
            partial_count = len(result.get("partial_coverage_files", []))
            if partial_count > 0:
                warnings.append(
                    f"🟡 {partial_count} files have <10% symbol coverage. Query patterns may be incomplete."
                )
            
            # Check for high uncovered rate
            if total_uncovered > 0:
                warnings.append(
                    f"🔴 {total_uncovered} files parsed but 0 symbols extracted (uncovered)."
                )
            
            # Check for valuable files being skipped
            for lang, stats in lang_stats.items():
                if lang == "text":
                    suggestions.append(
                        f"💡 {stats.get('ok', 0) + stats.get('skip', 0)} files detected as 'text'. "
                        f"Consider adding language mappings in config/parser.json"
                    )
                
                # Check for high uncovered rate per language
                uncovered = stats.get("uncovered", 0)
                ok_count = stats.get("ok", 0)
                if uncovered > 0 and ok_count > 0:
                    pct = (uncovered / ok_count) * 100
                    if pct >= 50:
                        warnings.append(
                            f"🔴 {lang}: {uncovered}/{ok_count} files ({pct:.0f}%) have 0 symbols. "
                            f"Query file may be missing patterns: config/queries/{lang}.scm"
                        )
                    elif pct >= 20:
                        suggestions.append(
                            f"⚠️ {lang}: {uncovered}/{ok_count} files ({pct:.0f}%) have 0 symbols. "
                            f"Consider improving: config/queries/{lang}.scm"
                        )
                
                # Check for languages with no symbols extracted at all
                if stats.get("ok", 0) > 0 and stats.get("symbols", 0) == 0:
                    warnings.append(
                        f"⚡ {lang}: {stats.get('ok', 0)} files parsed but 0 symbols extracted. "
                        f"Check query file: config/queries/{lang}.scm"
                    )
                
                # Check for low call resolution
                if stats.get("calls", 0) > 100 and stats.get("classes", 0) == 0:
                    suggestions.append(
                        f"💡 {lang}: High call count ({stats.get('calls', 0)}) but no class types. "
                        f"Add class/type queries to improve call resolution."
                    )
            
            result["warnings"] = warnings
            result["suggestions"] = suggestions
        
        return result

    def _clean_pipeline(self, args: dict) -> dict[str, Any]:
        """Clean all pipeline data and start fresh."""
        import shutil
        
        confirm = args.get("confirm", False)
        
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "⚠️ This will DELETE all pipeline data. Set confirm=true to proceed.",
                "will_delete": [
                    "data/parquet/* (all parquet files)",
                    "data/duckdb/* (database files)",
                    "generated/* (all generated code)",
                    "logs/* (all log files)",
                ],
                "followups": [
                    {"label": "✅ Confirm Clean", "prompt": "Run clean_pipeline with confirm=true"},
                    {"label": "❌ Cancel", "prompt": "Cancel the clean operation"},
                ],
            }
        
        # Get base path from config
        base_path = Path(self.config.parquet_root).parent.parent
        
        cleaned = []
        errors = []
        
        # Clean parquet
        parquet_dir = base_path / "data" / "parquet"
        if parquet_dir.exists():
            for item in parquet_dir.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    cleaned.append(f"data/parquet/{item.name}")
                except Exception as e:
                    errors.append(f"data/parquet/{item.name}: {e}")
        
        # Clean duckdb
        duckdb_dir = base_path / "data" / "duckdb"
        if duckdb_dir.exists():
            for item in duckdb_dir.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    cleaned.append(f"data/duckdb/{item.name}")
                except Exception as e:
                    errors.append(f"data/duckdb/{item.name}: {e}")
        
        # Clean generated
        generated_dir = base_path / "generated"
        if generated_dir.exists():
            for item in generated_dir.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    cleaned.append(f"generated/{item.name}")
                except Exception as e:
                    errors.append(f"generated/{item.name}: {e}")
        
        # Clean logs
        logs_dir = base_path / "logs"
        if logs_dir.exists():
            for item in logs_dir.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    cleaned.append(f"logs/{item.name}")
                except Exception as e:
                    errors.append(f"logs/{item.name}: {e}")
        
        return {
            "status": "cleaned" if not errors else "partial",
            "message": f"🧹 Cleaned {len(cleaned)} items" + (f" with {len(errors)} errors" if errors else ""),
            "cleaned": cleaned,
            "errors": errors if errors else None,
            "next_step": "Ready to start fresh. Run analyzer step='ingest' to begin.",
            "followups": [
                {"label": "📥 Start Ingest", "prompt": "Run analyzer step='ingest' source_path='/path/to/source'"},
                {"label": "📊 Check Status", "prompt": "Run pipeline_status"},
            ],
        }

    def _list_endpoints(self, args: dict) -> dict[str, Any]:
        """List discovered endpoints."""
        filter_pattern = args.get("filter", "%")
        limit = args.get("limit", 100)

        sql = f"""
            SELECT endpoint_id, endpoint, method, file_path, line_start
            FROM endpoints
            WHERE endpoint LIKE '%{filter_pattern}%'
            ORDER BY endpoint
            LIMIT {limit}
        """
        try:
            result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            result = []

        return {"endpoints": result, "count": len(result)}

    def _list_slices(self, args: dict) -> dict[str, Any]:
        """List generated slices with proper domain names resolved from symbols table."""
        status_filter = args.get("status")

        # First, get total count from entry_graphs for batch recommendation
        try:
            count_sql = "SELECT COUNT(*) as cnt FROM entry_graphs WHERE capped_depth >= 1"
            total_result = self.conn.execute(count_sql).fetchone()
            total_slices = total_result[0] if total_result else 0
        except Exception:
            total_slices = 0

        # Handle both old schema (with status/endpoint) and new schema (without)
        try:
            # Try new schema first - join with entry_graphs and symbols to get proper names
            sql = """
                SELECT DISTINCT 
                    sm.slice_id, 
                    sm.created_at,
                    s.name as symbol_name,
                    s.kind as symbol_kind,
                    s.file_path
                FROM slice_manifest sm
                LEFT JOIN entry_graphs eg ON sm.slice_id = CONCAT('entry_', LEFT(eg.entry_key, 8))
                LEFT JOIN symbols s ON eg.source_ref = s.symbol_id
                WHERE s.kind IN ('method', 'class', 'function') OR s.kind IS NULL
                ORDER BY sm.created_at DESC 
                LIMIT 100
            """
            result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
            # Add status='pending' for compatibility with pipeline
            for row in result:
                row["status"] = "pending"
                # Use the proper symbol name if available, otherwise fallback to slice_id
                row["endpoint"] = row.get("symbol_name") or row["slice_id"]
                row["domain_name"] = row.get("symbol_name") or row["slice_id"]
        except Exception:
            try:
                # Fallback to simple query
                sql = "SELECT DISTINCT slice_id, created_at FROM slice_manifest ORDER BY created_at DESC LIMIT 100"
                result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
                for row in result:
                    row["status"] = "pending"
                    # Try to resolve the symbol name
                    row["endpoint"] = self._get_symbol_name_for_slice(row["slice_id"])
                    row["domain_name"] = row["endpoint"]
            except Exception:
                try:
                    # Fallback to old schema
                    sql = "SELECT slice_id, endpoint, status, created_at FROM slice_manifest"
                    if status_filter:
                        sql += f" WHERE status = '{status_filter}'"
                    sql += " ORDER BY created_at DESC LIMIT 100"
                    result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
                except Exception:
                    result = []

        response = {"slices": result, "count": len(result), "total_slices": total_slices}
        
        # Add batch recommendation for large codebases
        if total_slices > 100:
            response["batch_recommendation"] = {
                "message": f"Large codebase detected: {total_slices} slices. Use batch_codegen for efficient processing.",
                "command": "batch_codegen(batch_size=500, cleanup_first=true, confirm=true)",
                "estimated_batches": (total_slices + 499) // 500,
            }
        
        return response

    def _get_slice_context(self, args: dict) -> dict[str, Any]:
        """Get full context for a slice."""
        slice_id = args["slice_id"]

        context = {}

        # Get slice manifest
        sql = f"SELECT * FROM slice_manifest WHERE slice_id = '{slice_id}'"
        try:
            context["manifest"] = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            context["manifest"] = []

        # Get source refs
        sql = f"SELECT * FROM slice_source_refs WHERE slice_id = '{slice_id}' LIMIT 500"
        try:
            context["source_refs"] = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            context["source_refs"] = []

        # Get slice context
        sql = f"SELECT * FROM slice_context WHERE slice_id = '{slice_id}'"
        try:
            context["context"] = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            context["context"] = []

        return context

    def _builder_fix(self, args: dict) -> dict[str, Any]:
        """[02-builder] Apply a fix from the fix queue (with human approval)."""
        fix_id = args["fix_id"]
        auto_revalidate = args.get("auto_revalidate", True)
        confirm = args.get("confirm", False)

        # Get fix details
        sql = f"SELECT * FROM fix_queue WHERE fix_id = '{fix_id}'"
        try:
            result = self.conn.execute(sql).fetchdf().to_dict(orient="records")
        except Exception:
            result = []

        if not result:
            return {"status": "fix_not_found", "fix_id": fix_id}

        fix = result[0]
        slice_id = fix.get("slice_id")

        # Get slice info for context
        slice_sql = f"SELECT endpoint FROM slice_manifest WHERE slice_id = '{slice_id}'"
        try:
            slice_info = self.conn.execute(slice_sql).fetchdf().to_dict(orient="records")
            endpoint = slice_info[0].get("endpoint") if slice_info else "unknown"
        except Exception:
            endpoint = "unknown"

        preview = {
            "fix_id": fix_id,
            "slice_id": slice_id,
            "endpoint": endpoint,
            "issue_type": fix.get("issue_type"),
            "fix_instruction": fix.get("fix_instruction"),
            "auto_revalidate": auto_revalidate,
        }

        available_params = {
            "fix_id": {"type": "string", "required": True, "current": fix_id},
            "auto_revalidate": {"type": "boolean", "required": False, "default": True, "current": auto_revalidate, "description": "Re-run judge_validate after fix"},
            "confirm": {"type": "boolean", "required": False, "default": False, "description": "Human approval to apply fix"},
        }

        # Human-in-the-loop: always require approval for fixes
        if not confirm:
            confirm_prompt = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 FIX DETAILS - HUMAN APPROVAL REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 Fix ID:                {fix_id}
🎯 Slice ID:              {slice_id}
📍 Endpoint:              {endpoint}
⚠️ Issue Type:            {fix.get("issue_type")}
📝 Fix Instruction:       {fix.get("fix_instruction")}
🔄 Auto Re-validate:      {auto_revalidate}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            followups = [
                {"label": "✅ Apply Fix", "prompt": f"Run builder_fix with fix_id='{fix_id}' confirm=true"},
                {"label": "⏭️ Skip This Fix", "prompt": f"Skip fix {fix_id} and continue"},
                {"label": "🚫 Reject & Manual Review", "prompt": f"Reject fix and mark slice {slice_id} for manual review"},
                {"label": "📋 View Slice Context", "prompt": f"Run get_slice_context with slice_id='{slice_id}'"},
            ]
            return {
                "stage": "5c-builder-fix",
                "status": "awaiting_human_approval",
                "message": "🔧 FIX REQUIRED - HUMAN APPROVAL NEEDED",
                "confirmation_prompt": confirm_prompt,
                "followups": followups,
                "quick_actions": {
                    "apply": f"builder_fix fix_id='{fix_id}' confirm=true",
                    "skip": "list_slices status='pending'",
                },
                "human_action_required": True,
                "available_parameters": available_params,
                "fix_details": preview,
                "action_required": "👆 Select an option above to proceed",
            }

        command = f"python -m migration_agents.builder.fix --fix-id {fix_id}"
        
        return {
            "stage": "5c-builder-fix",
            "status": "ready_to_execute",
            "message": "✅ Human approved fix. Execute the command below:",
            "fix_details": preview,
            "command": command,
            "instruction": f"Run: {command}",
            "next_step": f"After fix applied, run judge_validate with slice_id='{slice_id}' to re-validate" if auto_revalidate else "Fix applied. Manually verify or proceed.",
        }

    # =========================================================================
    # DDD-FIRST TOOLS: Domain-Driven Design Generation with Copilot
    # =========================================================================

    def _ddd_get_analysis_prompt(self, args: dict) -> dict[str, Any]:
        """[DDD] Get prompt for analyzing a slice to extract DDD concepts."""
        from migration_agents.codegen.ddd_builder import (
            get_ddd_analysis_prompt,
            SliceAnalysis,
        )
        
        slice_id = args["slice_id"]
        
        # Get slice context from database
        context = self._get_slice_context({"slice_id": slice_id})
        
        if not context.get("manifest"):
            return {
                "status": "slice_not_found",
                "slice_id": slice_id,
                "message": f"Slice '{slice_id}' not found. Use list_slices to see available slices.",
            }
        
        manifest = context["manifest"][0] if context["manifest"] else {}
        entry_name = manifest.get("endpoint", slice_id)
        
        # Get rule text from slice context
        slice_ctx = context.get("context", [])
        rule_text = ""
        if slice_ctx:
            rule_text = slice_ctx[0].get("rule_text", "") or slice_ctx[0].get("description", "")
        
        # Get source excerpts
        source_refs = context.get("source_refs", [])
        source_excerpts = []
        for ref in source_refs[:5]:  # Limit to 5 excerpts
            if ref.get("source_code"):
                source_excerpts.append(ref["source_code"])
            elif ref.get("file_path"):
                # Just include file path reference
                source_excerpts.append(f"// From: {ref['file_path']}:{ref.get('line_start', '?')}")
        
        # Generate the prompt
        prompt = get_ddd_analysis_prompt(entry_name, rule_text, source_excerpts)
        
        # Store context for later apply
        self._ddd_pending_slices = getattr(self, "_ddd_pending_slices", {})
        self._ddd_pending_slices[slice_id] = {
            "entry_name": entry_name,
            "rule_text": rule_text,
            "source_excerpts": source_excerpts,
        }
        
        return {
            "status": "prompt_ready",
            "slice_id": slice_id,
            "entry_name": entry_name,
            "prompt": prompt,
            "instructions": """
Analyze the prompt above and respond with a JSON object containing:
- aggregate_name: The main entity/aggregate root
- aggregate_description: Brief description
- properties: Array of {name, type, required, description}
- behaviors: Array of method/action names
- domain_events: Array of event names (past tense)
- value_objects: Array of {name, properties, description}
- invariants: Array of business rule statements

After analyzing, call ddd_apply_analysis with slice_id and your analysis JSON.
""",
            "next_step": f"After analyzing, call ddd_apply_analysis with slice_id='{slice_id}' and analysis=<your JSON response>",
        }

    def _ddd_apply_analysis(self, args: dict) -> dict[str, Any]:
        """[DDD] Apply Copilot's DDD analysis to a slice with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.ddd_builder import (
            apply_copilot_analysis,
            SliceAnalysis,
        )
        from migration_agents.codegen.config import load_config
        from migration_agents.shared_run_id import resolve_run_id
        
        slice_id = args["slice_id"]
        analysis_data = args.get("analysis", {})
        
        # Get stored context from prompt step
        pending = getattr(self, "_ddd_pending_slices", {})
        slice_ctx = pending.get(slice_id, {})
        
        if not slice_ctx:
            # Try to get from database
            context = self._get_slice_context({"slice_id": slice_id})
            manifest = context.get("manifest", [{}])[0]
            slice_ctx = {
                "entry_name": manifest.get("endpoint", slice_id),
                "rule_text": "",
                "source_excerpts": [],
            }
        
        # Apply the analysis
        analysis = apply_copilot_analysis(
            slice_id=slice_id,
            entry_name=slice_ctx.get("entry_name", slice_id),
            rule_text=slice_ctx.get("rule_text", ""),
            source_excerpts=slice_ctx.get("source_excerpts", []),
            copilot_response=analysis_data,
        )
        
        # Store the analysis for domain model building (in memory)
        self._ddd_slice_analyses = getattr(self, "_ddd_slice_analyses", {})
        self._ddd_slice_analyses[slice_id] = analysis
        
        # Also persist to state manager for resumability
        try:
            config_path = Path("config/codegen.json")
            if config_path.exists():
                codegen_config = load_config(config_path)
                parquet_root = codegen_config.output_root
            else:
                parquet_root = Path(DEFAULT_PARQUET_ROOT)
            
            run_id = resolve_run_id(parquet_root)
            if run_id:
                from migration_agents.codegen.ddd_state_manager import get_state_manager
                state_mgr = get_state_manager(parquet_root, run_id)
                
                # Get or create job for this solution
                solution_name = getattr(self, "_ddd_pending_solution", "default")
                job = state_mgr.get_latest_job_for_solution(solution_name)
                
                if job:
                    # Save to state manager
                    state_data = {
                        "aggregate_name": analysis.inferred_aggregate,
                        "bounded_context_hint": "",
                        "description": "",
                        "properties": [{"name": p.name, "type": p.type_hint} for p in analysis.inferred_properties],
                        "behaviors": analysis.inferred_behaviors,
                        "domain_events": analysis.inferred_events,
                        "value_objects": [{"name": vo.name} for vo in analysis.inferred_value_objects],
                        "invariants": analysis.inferred_invariants,
                    }
                    try:
                        state_mgr.save_slice_analysis(slice_id, job.job_id, state_data)
                    except ValueError:
                        pass  # Slice not registered - that's ok for non-batch workflow
        except Exception:
            pass  # State manager not available, continue with in-memory only
        
        return {
            "status": "analysis_applied",
            "slice_id": slice_id,
            "aggregate": analysis.inferred_aggregate,
            "properties": [p.name for p in analysis.inferred_properties],
            "behaviors": analysis.inferred_behaviors,
            "events": analysis.inferred_events,
            "invariants": analysis.inferred_invariants,
            "value_objects": [vo.name for vo in analysis.inferred_value_objects],
            "analyses_collected": len(self._ddd_slice_analyses),
            "next_steps": [
                "Analyze more slices with ddd_get_analysis_prompt",
                "Or build domain model with ddd_get_domain_model_prompt",
            ],
        }

    def _ddd_get_domain_model_prompt(self, args: dict) -> dict[str, Any]:
        """[DDD] Get prompt for building unified domain model from slice analyses."""
        from migration_agents.codegen.ddd_builder import (
            get_domain_model_prompt,
            SliceAnalysis,
        )
        
        solution_name = args["solution_name"]
        
        # Get collected analyses
        analyses = list(getattr(self, "_ddd_slice_analyses", {}).values())
        
        if not analyses:
            return {
                "status": "no_analyses",
                "message": "No slice analyses found. First analyze slices using ddd_get_analysis_prompt and ddd_apply_analysis.",
                "next_step": "Use ddd_get_analysis_prompt with a slice_id to start analyzing slices.",
            }
        
        # Generate the prompt
        prompt = get_domain_model_prompt(solution_name, analyses)
        
        # Store solution name for apply
        self._ddd_pending_solution = solution_name
        
        return {
            "status": "prompt_ready",
            "solution_name": solution_name,
            "slice_count": len(analyses),
            "aggregates_discovered": list(set(a.inferred_aggregate for a in analyses)),
            "prompt": prompt,
            "instructions": """
Analyze the slice analyses above and respond with a unified domain model JSON:
- name: Solution name
- description: Brief description
- aggregates: Array of aggregates with name, description, properties, behaviors, domain_events, value_objects, invariants
- shared_value_objects: Array of value objects used across aggregates

After analyzing, call ddd_apply_domain_model with solution_name and your domain_model JSON.
""",
            "next_step": f"After analyzing, call ddd_apply_domain_model with solution_name='{solution_name}' and domain_model=<your JSON response>",
        }

    def _ddd_apply_domain_model(self, args: dict) -> dict[str, Any]:
        """[DDD] Apply Copilot's domain model response."""
        from migration_agents.codegen.ddd_builder import (
            apply_copilot_domain_model,
            DomainModel,
        )
        
        solution_name = args["solution_name"]
        domain_model_data = args.get("domain_model", {})
        
        # Get collected analyses
        analyses = list(getattr(self, "_ddd_slice_analyses", {}).values())
        
        # Apply the domain model
        domain_model = apply_copilot_domain_model(
            analyses=analyses,
            model_name=solution_name,
            copilot_response=domain_model_data,
        )
        
        # Store the domain model for generation
        self._ddd_domain_model = domain_model
        
        return {
            "status": "domain_model_applied",
            "solution_name": solution_name,
            "aggregates": [agg.name for agg in domain_model.aggregates],
            "aggregate_count": len(domain_model.aggregates),
            "total_behaviors": sum(len(agg.behaviors) for agg in domain_model.aggregates),
            "total_events": sum(len(agg.domain_events) for agg in domain_model.aggregates),
            "shared_value_objects": [vo.name for vo in domain_model.shared_value_objects],
            "next_steps": [
                f"Generate Gherkin: ddd_generate_gherkin solution_name='{solution_name}'",
                f"Generate Contract: ddd_generate_contract solution_name='{solution_name}'",
            ],
        }

    def _ddd_generate_gherkin(self, args: dict) -> dict[str, Any]:
        """[DDD] Generate Gherkin/BDD specifications from domain model."""
        from migration_agents.codegen.ddd_builder import generate_gherkin_from_domain_model
        from pathlib import Path
        
        solution_name = args["solution_name"]
        output_path = args.get("output_path", "generated")
        
        # Get the domain model
        domain_model = getattr(self, "_ddd_domain_model", None)
        
        if not domain_model:
            return {
                "status": "no_domain_model",
                "message": "No domain model found. First build a domain model using ddd_get_domain_model_prompt and ddd_apply_domain_model.",
            }
        
        # Generate Gherkin
        features = generate_gherkin_from_domain_model(domain_model)
        
        # Write files
        output_dir = Path(output_path) / "features"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        written_files = []
        for feature in features:
            filename = f"{feature.name.replace(' ', '_')}.feature"
            filepath = output_dir / filename
            filepath.write_text(feature.render(), encoding="utf-8")
            written_files.append(str(filepath))
        
        return {
            "status": "gherkin_generated",
            "solution_name": solution_name,
            "feature_count": len(features),
            "files": written_files,
            "output_directory": str(output_dir),
            "next_step": f"Generate contract: ddd_generate_contract solution_name='{solution_name}'",
        }

    def _ddd_generate_contract(self, args: dict) -> dict[str, Any]:
        """[DDD] Generate API contract from domain model."""
        from migration_agents.codegen.ddd_builder import generate_contract_from_domain_model
        from pathlib import Path
        import json
        
        solution_name = args["solution_name"]
        output_path = args.get("output_path", "generated")
        
        # Get the domain model
        domain_model = getattr(self, "_ddd_domain_model", None)
        
        if not domain_model:
            return {
                "status": "no_domain_model",
                "message": "No domain model found. First build a domain model using ddd_get_domain_model_prompt and ddd_apply_domain_model.",
            }
        
        # Generate contract
        contract = generate_contract_from_domain_model(domain_model)
        
        # Write files
        output_dir = Path(output_path) / "contracts"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # OpenAPI JSON
        openapi_path = output_dir / f"{contract.name}.openapi.json"
        openapi_path.write_text(json.dumps(contract.to_openapi(), indent=2), encoding="utf-8")
        
        # Markdown summary
        md_path = output_dir / f"{contract.name}.contract.md"
        md_lines = [
            f"# {contract.name} API Contract",
            "",
            f"**Version:** {contract.version}",
            f"**Description:** {contract.description}",
            "",
            "## Endpoints",
            "",
        ]
        for ep in contract.endpoints:
            md_lines.append(f"### {ep.method} `{ep.path}`")
            md_lines.append(f"- **Operation:** `{ep.operation_id}`")
            md_lines.append(f"- **Summary:** {ep.summary}")
            md_lines.append("")
        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        
        return {
            "status": "contract_generated",
            "solution_name": solution_name,
            "endpoint_count": len(contract.endpoints),
            "files": [str(openapi_path), str(md_path)],
            "output_directory": str(output_dir),
            "next_step": "Review generated contract and proceed to code generation with builder_generate",
        }

    def _ddd_run_full_pipeline(self, args: dict) -> dict[str, Any]:
        """[DDD] Run complete DDD-first pipeline with rule-based analysis."""
        from migration_agents.codegen.ddd_builder import (
            analyze_slice_for_domain,
            build_domain_model_from_slices,
            generate_gherkin_from_domain_model,
            generate_contract_from_domain_model,
            SliceAnalysis,
        )
        from pathlib import Path
        import json
        
        solution_name = args["solution_name"]
        output_path = args.get("output_path", "generated")
        slice_ids = args.get("slice_ids")
        
        # Get slices from database
        if slice_ids:
            slices = []
            for sid in slice_ids:
                ctx = self._get_slice_context({"slice_id": sid})
                if ctx.get("manifest"):
                    slices.append(ctx)
        else:
            # Get all pending slices
            slices_result = self._list_slices({"status": "pending"})
            slices = []
            for s in slices_result.get("slices", [])[:20]:  # Limit to 20
                ctx = self._get_slice_context({"slice_id": s["slice_id"]})
                if ctx.get("manifest"):
                    slices.append(ctx)
        
        if not slices:
            return {
                "status": "no_slices",
                "message": "No slices found to process. Run analyzer first.",
            }
        
        # Analyze each slice with rule-based analysis
        analyses = []
        for ctx in slices:
            manifest = ctx["manifest"][0] if ctx.get("manifest") else {}
            slice_id = manifest.get("slice_id", "unknown")
            
            # Try to get the proper domain name from the symbols table
            # This resolves hash-based slice IDs to actual method/class names
            entry_name = manifest.get("endpoint")
            if not entry_name or entry_name == slice_id:
                entry_name = self._get_symbol_name_for_slice(slice_id)
            
            slice_ctx_list = ctx.get("context", [])
            rule_text = slice_ctx_list[0].get("rule_text", "") if slice_ctx_list else ""
            
            analysis = analyze_slice_for_domain(
                slice_id=slice_id,
                entry_name=entry_name,
                rule_text=rule_text,
            )
            analyses.append(analysis)
        
        # Build domain model
        domain_model = build_domain_model_from_slices(analyses, solution_name)
        
        # Generate Gherkin
        features = generate_gherkin_from_domain_model(domain_model)
        output_dir = Path(output_path)
        gherkin_dir = output_dir / "features"
        gherkin_dir.mkdir(parents=True, exist_ok=True)
        
        gherkin_files = []
        for feature in features:
            filename = f"{feature.name.replace(' ', '_')}.feature"
            filepath = gherkin_dir / filename
            filepath.write_text(feature.render(), encoding="utf-8")
            gherkin_files.append(str(filepath))
        
        # Generate contract
        contract = generate_contract_from_domain_model(domain_model)
        contract_dir = output_dir / "contracts"
        contract_dir.mkdir(parents=True, exist_ok=True)
        
        openapi_path = contract_dir / f"{contract.name}.openapi.json"
        openapi_path.write_text(json.dumps(contract.to_openapi(), indent=2), encoding="utf-8")
        
        # Store for subsequent operations
        self._ddd_domain_model = domain_model
        self._ddd_slice_analyses = {a.slice_id: a for a in analyses}
        
        return {
            "status": "pipeline_complete",
            "solution_name": solution_name,
            "slices_analyzed": len(analyses),
            "aggregates": [agg.name for agg in domain_model.aggregates],
            "gherkin_features": len(features),
            "gherkin_files": gherkin_files,
            "contract_endpoints": len(contract.endpoints),
            "contract_file": str(openapi_path),
            "output_directory": str(output_dir),
            "next_step": "Review generated artifacts and proceed to code generation with builder_generate",
        }

    # =========================================================================
    # COMPREHENSIVE DDD ANALYSIS (All Endpoints + SME Review)
    # =========================================================================

    def _ddd_analyze_all_endpoints(self, args: dict) -> dict[str, Any]:
        """[DDD] Get prompt for comprehensive analysis of ALL endpoints."""
        from migration_agents.codegen.ddd_builder import get_full_ddd_analysis_prompt
        from pathlib import Path
        
        solution_name = args["solution_name"]
        min_depth = args.get("min_depth", 0)
        max_depth = args.get("max_depth", 10)
        
        # Get ALL endpoints from database across all depth levels
        # Note: endpoints view already has depth from entry_graphs join
        sql = f"""
            SELECT DISTINCT 
                e.endpoint_id,
                e.endpoint as name,
                e.method,
                e.file_path,
                e.line_start,
                COALESCE(e.depth, 0) as depth
            FROM endpoints e
            WHERE COALESCE(e.depth, 0) >= {min_depth}
              AND COALESCE(e.depth, 0) <= {max_depth}
            ORDER BY depth, name
        """
        try:
            endpoints_df = self.conn.execute(sql).fetchdf()
            endpoints = endpoints_df.to_dict(orient="records")
        except Exception as ex:
            LOGGER.warning("Failed to fetch endpoints: %s", ex)
            endpoints = []
        
        if not endpoints:
            return {
                "status": "no_endpoints",
                "message": "No endpoints found. Run analyzer with step='parse' first.",
            }
        
        # Get depth levels present
        depth_levels = sorted(set(ep.get("depth", 0) for ep in endpoints))
        
        # Build source analysis summary by fetching symbols
        source_analysis_parts = []
        for ep in endpoints[:50]:  # Limit to first 50 for prompt size
            ep_id = ep.get("endpoint_id")
            sym_sql = f"SELECT name, kind FROM symbols WHERE file_path = '{ep.get('file_path', '')}' LIMIT 10"
            try:
                symbols = self.conn.execute(sym_sql).fetchdf().to_dict(orient="records")
                sym_names = [s["name"] for s in symbols]
                source_analysis_parts.append(f"### {ep.get('name')} (Depth {ep.get('depth')})\nSymbols: {', '.join(sym_names[:5])}")
            except Exception:
                source_analysis_parts.append(f"### {ep.get('name')} (Depth {ep.get('depth')})")
        
        source_analysis = "\n\n".join(source_analysis_parts)
        
        # Generate comprehensive prompt
        prompt = get_full_ddd_analysis_prompt(
            solution_name=solution_name,
            endpoints=[{"name": ep.get("name"), "depth": ep.get("depth"), "description": f"From {ep.get('file_path')}"} for ep in endpoints],
            depth_levels=depth_levels,
            source_analysis=source_analysis,
        )
        
        # Store for later apply
        self._ddd_pending_full_analysis = {
            "solution_name": solution_name,
            "endpoints": endpoints,
            "depth_levels": depth_levels,
        }
        
        return {
            "status": "prompt_ready",
            "solution_name": solution_name,
            "endpoint_count": len(endpoints),
            "depth_levels": depth_levels,
            "prompt": prompt,
            "instructions": """
Analyze ALL endpoints listed above before drawing conclusions. You MUST:

1. Extract UBIQUITOUS LANGUAGE - all domain terms with definitions
2. Identify AT LEAST 2-3 BOUNDED CONTEXT CANDIDATES with confidence scores
3. RECOMMEND the best bounded context structure with reasoning
4. Extract AGGREGATE ROOTS with behaviors, events, and invariants
5. Identify VALUE OBJECTS and DOMAIN EVENTS

This analysis will be reviewed by a Subject Matter Expert (SME).

After analyzing, call ddd_apply_full_analysis with your complete JSON response.
""",
            "next_step": f"After comprehensive analysis, call ddd_apply_full_analysis with solution_name='{solution_name}' and analysis=<your JSON response>",
        }

    def _ddd_apply_full_analysis(self, args: dict) -> dict[str, Any]:
        """[DDD] Apply comprehensive DDD analysis from Copilot with state tracking."""
        from migration_agents.codegen.ddd_builder import (
            parse_full_ddd_analysis_response,
            DDDAnalysisResult,
        )
        from datetime import datetime
        from pathlib import Path
        
        solution_name = args["solution_name"]
        analysis_data = args.get("analysis", {})
        
        # Get stored context
        pending = getattr(self, "_ddd_pending_full_analysis", {})
        
        # Parse the full analysis
        result = parse_full_ddd_analysis_response(analysis_data)
        
        if not result:
            return {
                "status": "parse_error",
                "message": "Failed to parse DDD analysis response. Ensure JSON format is correct.",
            }
        
        # Update with solution info
        result.solution_name = solution_name
        result.analysis_timestamp = datetime.now().isoformat()
        result.endpoints_analyzed = [ep.get("name", "") for ep in pending.get("endpoints", [])]
        result.endpoint_count = len(result.endpoints_analyzed)
        result.depth_levels_analyzed = pending.get("depth_levels", [])
        
        # Store the result in memory
        self._ddd_full_analysis = result
        
        # Also persist to state manager for resumability
        try:
            from migration_agents.codegen.config import load_config
            from migration_agents.shared_run_id import resolve_run_id
            from migration_agents.codegen.ddd_state_manager import get_state_manager, JobStatus
            
            config_path = Path("config/codegen.json")
            if config_path.exists():
                codegen_config = load_config(config_path)
                parquet_root = codegen_config.output_root
            else:
                parquet_root = Path(DEFAULT_PARQUET_ROOT)
            
            run_id = resolve_run_id(parquet_root)
            if run_id:
                state_mgr = get_state_manager(parquet_root, run_id)
                job = state_mgr.get_latest_job_for_solution(solution_name)
                
                if job:
                    # Save each aggregate as a slice analysis
                    for agg in result.aggregates:
                        state_data = {
                            "aggregate_name": agg.name,
                            "bounded_context_hint": result.recommended_context or "",
                            "description": agg.description,
                            "properties": [{"name": p.name, "type": p.type_hint} for p in agg.properties],
                            "behaviors": agg.behaviors,
                            "domain_events": [e.name for e in agg.domain_events],
                            "value_objects": [{"name": vo.name} for vo in agg.value_objects],
                            "invariants": agg.invariants,
                        }
                        # Create a synthetic slice_id for aggregates
                        slice_id = f"agg_{agg.name.lower().replace(' ', '_')}"
                        try:
                            state_mgr.save_slice_analysis(slice_id, job.job_id, state_data)
                        except ValueError:
                            pass  # Slice not registered
                    
                    # Update job progress
                    state_mgr.update_job_progress(
                        job.job_id, 
                        analyzed_slices=len(result.aggregates)
                    )
        except Exception:
            pass  # State manager not available
        
        # Write review document
        output_dir = Path("generated") / "ddd_review"
        output_dir.mkdir(parents=True, exist_ok=True)
        review_path = output_dir / f"{solution_name}_ddd_review.md"
        review_path.write_text(result.to_review_document(), encoding="utf-8")
        
        return {
            "status": "analysis_applied",
            "solution_name": solution_name,
            "sme_review_required": True,
            "review_status": result.sme_review_status,
            "summary": {
                "endpoints_analyzed": result.endpoint_count,
                "depth_levels": result.depth_levels_analyzed,
                "ubiquitous_terms": len(result.ubiquitous_language),
                "bounded_context_candidates": len(result.bounded_context_candidates),
                "recommended_context": result.recommended_context,
                "aggregates": [agg.name for agg in result.aggregates],
                "domain_events": len(result.domain_events),
                "value_objects": len(result.shared_value_objects),
            },
            "review_document": str(review_path),
            "bounded_context_options": [
                {
                    "name": ctx.name,
                    "confidence": f"{ctx.confidence_score:.0%}",
                    "is_recommended": ctx.name == result.recommended_context,
                }
                for ctx in result.bounded_context_candidates
            ],
            "next_steps": [
                f"1. Validate coverage: ddd_validate_coverage solution_name='{solution_name}'",
                f"2. Review document at: {review_path}",
                "3. Get SME review: ddd_get_sme_review",
                "4. Submit SME feedback: ddd_submit_sme_review",
                "5. After SME approval: ddd_generate_gherkin and ddd_generate_contract",
            ],
            "action_required": "⚠️ RUN ddd_validate_coverage BEFORE SME REVIEW",
        }

    def _ddd_get_sme_review(self, args: dict) -> dict[str, Any]:
        """[DDD] Get the DDD analysis document for SME review."""
        from pathlib import Path
        
        solution_name = args["solution_name"]
        output_path = args.get("output_path", "generated/ddd_review")
        skip_validation = args.get("skip_validation", False)
        
        # Get stored analysis
        result = getattr(self, "_ddd_full_analysis", None)
        
        if not result or result.solution_name != solution_name:
            return {
                "status": "no_analysis",
                "message": f"No DDD analysis found for '{solution_name}'. Run ddd_analyze_all_endpoints first.",
            }
        
        # Run validation first (judge gate)
        if not skip_validation:
            validation = self._ddd_validate_coverage({"solution_name": solution_name})
            if not validation.get("coverage_ok", False):
                return {
                    "status": "validation_failed",
                    "message": "❌ Coverage validation failed. Address issues before SME review.",
                    "validation_result": validation,
                    "next_step": f"Fix issues and re-run ddd_validate_coverage solution_name='{solution_name}'",
                }
        
        # Generate review document
        review_doc = result.to_review_document()
        
        # Write to file
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        review_path = output_dir / f"{solution_name}_ddd_review.md"
        review_path.write_text(review_doc, encoding="utf-8")
        
        return {
            "status": "review_ready",
            "solution_name": solution_name,
            "review_status": result.sme_review_status,
            "validation": "✅ PASSED" if not skip_validation else "⏭️ SKIPPED",
            "review_document_path": str(review_path),
            "review_document": review_doc,
            "summary": {
                "ubiquitous_terms": len(result.ubiquitous_language),
                "bounded_context_candidates": len(result.bounded_context_candidates),
                "recommended_context": result.recommended_context,
                "aggregates": len(result.aggregates),
                "requires_approval": result.sme_review_required,
            },
            "instructions": """
Please review the DDD analysis document above with a Subject Matter Expert.

The SME should verify:
1. Ubiquitous Language - Are terms correctly defined?
2. Bounded Contexts - Is the recommended structure appropriate?
3. Aggregates - Are boundaries and invariants correct?
4. Domain Events - Are all significant events captured?

After review, submit feedback using ddd_submit_sme_review with:
- review_status: APPROVE, NEEDS_REVISION, or REJECT
- reviewer_name: Name of the SME
- feedback: Detailed comments
""",
            "next_step": f"After SME review, call ddd_submit_sme_review with solution_name='{solution_name}' and review decision",
        }

    def _ddd_submit_sme_review(self, args: dict) -> dict[str, Any]:
        """[DDD] Submit SME review feedback for the DDD analysis."""
        from datetime import datetime
        from pathlib import Path
        
        solution_name = args["solution_name"]
        review_status = args["review_status"].upper()
        reviewer_name = args["reviewer_name"]
        feedback = args.get("feedback", {})
        
        # Get stored analysis
        result = getattr(self, "_ddd_full_analysis", None)
        
        if not result or result.solution_name != solution_name:
            return {
                "status": "no_analysis",
                "message": f"No DDD analysis found for '{solution_name}'. Run ddd_analyze_all_endpoints first.",
            }
        
        # Update review status
        result.sme_review_status = review_status.lower()
        result.sme_reviewed_by = reviewer_name
        result.sme_reviewed_at = datetime.now().isoformat()
        
        # Add comments from feedback
        if isinstance(feedback, dict):
            if feedback.get("action_items"):
                result.sme_comments.extend(feedback["action_items"])
            if feedback.get("reviewer_notes"):
                result.sme_comments.append(feedback["reviewer_notes"])
        
        # Write updated review document
        output_dir = Path("generated") / "ddd_review"
        output_dir.mkdir(parents=True, exist_ok=True)
        review_path = output_dir / f"{solution_name}_ddd_review.md"
        review_path.write_text(result.to_review_document(), encoding="utf-8")
        
        # Determine next steps based on status
        if review_status == "APPROVE":
            # Convert to domain model for code generation
            from migration_agents.codegen.ddd_builder import DomainModel
            
            domain_model = DomainModel(
                name=solution_name,
                description=result.recommendation_reasoning,
                aggregates=result.aggregates,
                shared_value_objects=result.shared_value_objects,
            )
            self._ddd_domain_model = domain_model
            
            next_steps = [
                "✅ SME APPROVED - Ready for code generation",
                f"Generate Gherkin: ddd_generate_gherkin solution_name='{solution_name}'",
                f"Generate Contract: ddd_generate_contract solution_name='{solution_name}'",
            ]
            action = "Proceed to code generation"
        elif review_status == "NEEDS_REVISION":
            next_steps = [
                "⚠️ REVISION REQUIRED",
                f"Re-analyze: ddd_analyze_all_endpoints solution_name='{solution_name}'",
                "Address the feedback items and re-submit for review",
            ]
            action = "Address feedback and re-analyze"
        else:  # REJECT
            next_steps = [
                "❌ REJECTED - Major issues identified",
                "Review the feedback carefully",
                "Consider re-analyzing with different approach",
                f"Re-analyze: ddd_analyze_all_endpoints solution_name='{solution_name}'",
            ]
            action = "Review feedback and restart analysis"
        
        return {
            "status": "review_submitted",
            "solution_name": solution_name,
            "review_status": review_status,
            "reviewed_by": reviewer_name,
            "reviewed_at": result.sme_reviewed_at,
            "feedback_summary": {
                "action_items": feedback.get("action_items", []),
                "overall_assessment": feedback.get("overall_assessment", ""),
            },
            "review_document": str(review_path),
            "next_steps": next_steps,
            "action_required": action,
            "can_proceed_to_codegen": review_status == "APPROVE",
        }

    def _ddd_list_bounded_contexts(self, args: dict) -> dict[str, Any]:
        """[DDD] List all bounded context candidates with scores."""
        solution_name = args["solution_name"]
        
        # Get stored analysis
        result = getattr(self, "_ddd_full_analysis", None)
        
        if not result or result.solution_name != solution_name:
            return {
                "status": "no_analysis",
                "message": f"No DDD analysis found for '{solution_name}'. Run ddd_analyze_all_endpoints first.",
            }
        
        contexts = []
        for ctx in result.bounded_context_candidates:
            contexts.append({
                "name": ctx.name,
                "description": ctx.description,
                "confidence_score": f"{ctx.confidence_score:.0%}",
                "is_recommended": ctx.name == result.recommended_context,
                "aggregates": ctx.aggregates,
                "responsibilities": ctx.responsibilities,
                "endpoints": ctx.endpoints,  # Complete list - no truncation
                "integration_points": ctx.integration_points,  # Include integration points
                "reasoning": ctx.reasoning,
            })
        
        # Sort by confidence
        contexts.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        return {
            "status": "success",
            "solution_name": solution_name,
            "total_candidates": len(contexts),
            "recommended": result.recommended_context,
            "recommendation_reasoning": result.recommendation_reasoning,
            "bounded_contexts": contexts,
        }

    def _ddd_get_ubiquitous_language(self, args: dict) -> dict[str, Any]:
        """[DDD] Get the ubiquitous language glossary."""
        solution_name = args["solution_name"]
        
        # Get stored analysis
        result = getattr(self, "_ddd_full_analysis", None)
        
        if not result or result.solution_name != solution_name:
            return {
                "status": "no_analysis",
                "message": f"No DDD analysis found for '{solution_name}'. Run ddd_analyze_all_endpoints first.",
            }
        
        glossary = []
        for term in result.ubiquitous_language:
            glossary.append({
                "term": term.term,
                "definition": term.definition,
                "aliases": term.aliases,
                "examples": term.examples,
                "related_terms": term.related_terms,
            })
        
        # Sort alphabetically
        glossary.sort(key=lambda x: x["term"].lower())
        
        return {
            "status": "success",
            "solution_name": solution_name,
            "total_terms": len(glossary),
            "ubiquitous_language": glossary,
        }

    def _ddd_validate_coverage(self, args: dict) -> dict[str, Any]:
        """[DDD-Judge] Validate DDD analysis coverage before SME review."""
        from pathlib import Path
        import json
        
        solution_name = args["solution_name"]
        
        # Get stored analysis
        result = getattr(self, "_ddd_full_analysis", None)
        ddd_file = Path("generated/ddd_analysis_result.json")
        
        # Try loading from file if not in memory
        if not result and ddd_file.exists():
            with open(ddd_file) as f:
                ddd_data = json.load(f)
            ddd_analyzed = ddd_data.get("total_endpoints_analyzed", 0)
            ddd_depths = ddd_data.get("depth_levels_covered", [])
            bounded_contexts = ddd_data.get("bounded_context_candidates", [])
        elif result:
            ddd_analyzed = result.endpoint_count
            ddd_depths = result.depth_levels_analyzed
            bounded_contexts = result.bounded_context_candidates
        else:
            return {
                "status": "no_analysis",
                "message": f"No DDD analysis found for '{solution_name}'. Run ddd_analyze_all_endpoints first.",
            }
        
        # Get source counts from parquet
        findings = []
        issues = []
        
        # Find latest run
        parquet_dir = Path(DEFAULT_PARQUET_ROOT)
        runs = sorted([d for d in parquet_dir.iterdir() if d.is_dir() and d.name.startswith("run_")])
        if not runs:
            return {
                "status": "no_parquet",
                "message": "No parquet data found. Run analyzer first.",
            }
        
        run_dir = runs[-1]
        
        # Find source index
        source_index = None
        for f in run_dir.rglob("intake_source_index*.parquet"):
            source_index = f
            break
        
        source_counts = {}
        if source_index:
            # Count ASPX pages
            aspx_query = f'''
                SELECT COUNT(*) FROM "{source_index}"
                WHERE file_path LIKE '%.aspx'
                AND file_path NOT LIKE '%.cs'
                AND file_path NOT LIKE '%Zone.Identifier%'
            '''
            aspx_pages = self.conn.execute(aspx_query).fetchone()[0]
            source_counts["aspx_pages"] = aspx_pages
            
            # Count code-behind files
            codebehind_query = f'''
                SELECT COUNT(*) FROM "{source_index}"
                WHERE file_path LIKE '%.aspx.cs'
                AND file_path NOT LIKE '%Zone.Identifier%'
            '''
            codebehind = self.conn.execute(codebehind_query).fetchone()[0]
            source_counts["aspx_codebehind"] = codebehind
            
            # Count all CS files
            cs_query = f'''
                SELECT COUNT(*) FROM "{source_index}"
                WHERE file_path LIKE '%.cs'
                AND file_path NOT LIKE '%Zone.Identifier%'
            '''
            cs_files = self.conn.execute(cs_query).fetchone()[0]
            source_counts["cs_files"] = cs_files
        
        # Find entry graphs
        entry_graphs = None
        for f in run_dir.rglob("entry_graphs*.parquet"):
            entry_graphs = f
            break
        
        if entry_graphs:
            total_entries = self.conn.execute(f'SELECT COUNT(*) FROM "{entry_graphs}"').fetchone()[0]
            source_counts["entry_graphs"] = total_entries
        
        # Validation checks
        coverage_ok = True
        
        # Check 1: ASPX endpoint coverage
        if source_counts.get("aspx_pages", 0) > 0:
            if ddd_analyzed >= source_counts["aspx_pages"]:
                findings.append({
                    "check": "aspx_coverage",
                    "status": "✅ PASS",
                    "message": f"All {source_counts['aspx_pages']} ASPX pages covered by {ddd_analyzed} analyzed endpoints",
                })
            else:
                coverage_ok = False
                issues.append({
                    "check": "aspx_coverage",
                    "status": "❌ FAIL",
                    "message": f"Only {ddd_analyzed} endpoints analyzed, but {source_counts['aspx_pages']} ASPX pages exist",
                    "gap": source_counts["aspx_pages"] - ddd_analyzed,
                })
        
        # Check 2: Bounded contexts have endpoints
        bc_with_endpoints = 0
        bc_endpoint_total = 0
        for bc in bounded_contexts:
            if isinstance(bc, dict):
                eps = bc.get("endpoints", [])
            else:
                eps = bc.endpoints if hasattr(bc, "endpoints") else []
            if eps:
                bc_with_endpoints += 1
                bc_endpoint_total += len(eps)
        
        if bc_with_endpoints == len(bounded_contexts):
            findings.append({
                "check": "bounded_context_endpoints",
                "status": "✅ PASS",
                "message": f"All {len(bounded_contexts)} bounded contexts have assigned endpoints ({bc_endpoint_total} total)",
            })
        else:
            issues.append({
                "check": "bounded_context_endpoints",
                "status": "⚠️ WARN",
                "message": f"Only {bc_with_endpoints}/{len(bounded_contexts)} bounded contexts have endpoints",
            })
        
        # Check 3: Depth levels coverage
        expected_depths = list(range(10))  # 0-9
        missing_depths = [d for d in expected_depths if d not in ddd_depths]
        if not missing_depths:
            findings.append({
                "check": "depth_coverage",
                "status": "✅ PASS",
                "message": f"All depth levels covered: {ddd_depths}",
            })
        else:
            issues.append({
                "check": "depth_coverage",
                "status": "⚠️ WARN",
                "message": f"Missing depth levels: {missing_depths}",
            })
        
        # Check 4: Review document completeness (no truncation markers)
        review_file = Path("generated/ddd_sme_review.md")
        if review_file.exists():
            content = review_file.read_text()
            if "... and" in content or "+ more" in content.lower():
                coverage_ok = False
                issues.append({
                    "check": "document_completeness",
                    "status": "❌ FAIL",
                    "message": "Review document contains truncation markers ('... and X more')",
                    "action": "Regenerate the DDD analysis to include complete listings",
                })
            else:
                findings.append({
                    "check": "document_completeness",
                    "status": "✅ PASS",
                    "message": "Review document has no truncation markers",
                })
        
        # Determine overall status
        if coverage_ok and not issues:
            overall_status = "✅ VALIDATED"
            message = "DDD analysis coverage is complete. Ready for SME review."
            next_step = f"ddd_get_sme_review solution_name='{solution_name}'"
        elif coverage_ok:
            overall_status = "⚠️ WARNINGS"
            message = "Coverage validated with warnings. Review issues before proceeding."
            next_step = f"ddd_get_sme_review solution_name='{solution_name}'"
        else:
            overall_status = "❌ FAILED"
            message = "Coverage validation failed. Address issues before SME review."
            next_step = f"ddd_analyze_all_endpoints solution_name='{solution_name}'"
        
        return {
            "stage": "judge-ddd-validate",
            "status": overall_status,
            "message": message,
            "solution_name": solution_name,
            "source_counts": source_counts,
            "ddd_analysis": {
                "endpoints_analyzed": ddd_analyzed,
                "depth_levels": ddd_depths,
                "bounded_contexts": len(bounded_contexts),
            },
            "findings": findings,
            "issues": issues,
            "coverage_ok": coverage_ok,
            "next_step": next_step,
        }

    # === VALIDATION TOOLS: Deterministic Validation & Versioning ===

    def _validate_migration(self, args: dict) -> dict[str, Any]:
        """[validation] Run deterministic validation against rubrics with state tracking."""
        import sys
        project_path = args.get("project_path", "")
        stages = args.get("stages", ["all"])
        output_format = args.get("output_format", "summary")
        
        # Resolve path
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        if not validation_dir.exists():
            return {
                "status": "error",
                "message": f"Validation directory not found: {validation_dir}. Run validator.py first.",
            }
        
        # Initialize pipeline state manager
        from migration_agents.codegen.pipeline_state_manager import (
            get_pipeline_state_manager, ValidationStatus
        )
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(self.config.parquet_root)
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        # Create validation run
        solution_name = project_path.name
        validation_run = state_mgr.create_validation_run(str(project_path), solution_name)
        
        # Add validation dir to path and import
        sys.path.insert(0, str(validation_dir))
        try:
            from validator import MigrationValidator, LayerScore
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import validator: {e}"}
        
        validator = MigrationValidator(str(project_path))
        
        results = []
        if "all" in stages or "domain" in stages:
            results.append(("Domain", validator.validate_domain_layer()))
        if "all" in stages or "application" in stages:
            results.append(("Application", validator.validate_application_layer()))
        if "all" in stages or "api" in stages:
            results.append(("API", validator.validate_api_layer()))
        
        # Calculate overall (LayerScore has score and max_score)
        total_score = sum(v.score for _, v in results)
        max_score = sum(v.max_score for _, v in results)
        overall = round((total_score / max_score) * 100, 2) if max_score > 0 else 0
        
        # Save results to state manager
        scores = {
            "overall": overall,
            "domain": next((v.percentage for n, v in results if n == "Domain"), 0.0),
            "application": next((v.percentage for n, v in results if n == "Application"), 0.0),
            "api": next((v.percentage for n, v in results if n == "API"), 0.0),
            "infrastructure": 0.0,
        }
        rubric_results = {name: v.rubrics for name, v in results}
        total_issues = sum(len([r for r in v.rubrics if r.get("score", 0) < r.get("max", 1) * 0.7]) for _, v in results)
        critical_issues = sum(len([r for r in v.rubrics if r.get("score", 0) == 0]) for _, v in results)
        
        state_mgr.save_validation_results(
            validation_run.run_id,
            scores,
            rubric_results,
            total_issues,
            critical_issues,
        )
        
        if output_format == "json":
            return {
                "status": "success",
                "validation_run_id": validation_run.run_id,
                "overall_score": overall,
                "validations": [{
                    "stage": name,
                    "score": v.percentage,
                    "status": "PASSED" if v.percentage >= 70 else "NEEDS_WORK",
                    "rubrics": v.rubrics
                } for name, v in results]
            }
        
        # Build summary
        summary_lines = [f"**Overall Score: {overall}%**\n"]
        for name, v in results:
            status = "✅" if v.percentage >= 70 else "⚠️"
            summary_lines.append(f"- {status} **{name}**: {v.percentage:.1f}%")
            if output_format == "detailed":
                for r in v.rubrics:
                    r_status = "✓" if r.get("score", 0) >= r.get("max", 1) * 0.7 else "⚠"
                    summary_lines.append(f"  - {r_status} {r.get('id')}: {r.get('score', 0)}/{r.get('max', 0)}")
        
        return {
            "status": "success",
            "validation_run_id": validation_run.run_id,
            "overall_score": overall,
            "summary": "\n".join(summary_lines),
            "passing": overall >= 70,
        }

    def _get_validation_report(self, args: dict) -> dict[str, Any]:
        """[validation] Get latest validation report."""
        project_path = args.get("project_path", "")
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        reports = list(validation_dir.glob("validation_report_*.json"))
        
        if not reports:
            return {"status": "error", "message": "No validation reports found"}
        
        latest = max(reports, key=lambda p: p.stat().st_mtime)
        with open(latest) as f:
            report = json.load(f)
        
        return {
            "status": "success",
            "report_file": str(latest.name),
            "overall_score": report.get("overall_score"),
            "timestamp": report.get("timestamp"),
            "validations_count": len(report.get("validations", [])),
        }

    def _get_coverage_summary(self, args: dict) -> dict[str, Any]:
        """[validation] Get bounded context coverage."""
        import sys
        project_path = args.get("project_path", "")
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from validator import MigrationValidator
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import validator: {e}"}
        
        validator = MigrationValidator(str(project_path))
        coverage = validator.generate_coverage_summary()
        
        return {
            "status": "success",
            "coverage": [{
                "context": c.bounded_context,
                "expected": c.expected_endpoints,
                "generated": c.generated_endpoints,
                "percentage": c.coverage_percentage
            } for c in coverage]
        }

    def _create_validation_review(self, args: dict) -> dict[str, Any]:
        """[validation] Create a review file with fixes and track in state."""
        import sys
        project_path = args.get("project_path", "")
        reviewer = args.get("reviewer", "SME")
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from fix_workflow import create_sample_review
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import fix_workflow: {e}"}
        
        review_path = create_sample_review(str(project_path))
        
        # Register fixes in state manager
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(self.config.parquet_root)
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        solution_name = project_path.name
        latest_validation = state_mgr.get_latest_validation_run(solution_name)
        
        # Parse review file to get fixes
        if latest_validation and Path(review_path).exists():
            with open(review_path) as f:
                review_data = json.load(f)
            fixes = review_data.get("fixes", [])
            state_mgr.register_validation_fixes(latest_validation.run_id, fixes)
        
        return {
            "status": "success",
            "message": "Review file created",
            "review_file": str(review_path),
            "validation_run_id": latest_validation.run_id if latest_validation else None,
            "next_step": "Edit the review file to add/modify fixes, then run apply_validation_fixes",
        }

    def _list_validation_fixes(self, args: dict) -> dict[str, Any]:
        """[validation] List pending fixes."""
        import sys
        project_path = args.get("project_path", "")
        priority_filter = args.get("priority", "all")
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from fix_workflow import FixWorkflowManager
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import fix_workflow: {e}"}
        
        manager = FixWorkflowManager(str(project_path))
        fixes = manager.list_pending_fixes()
        
        if priority_filter != "all":
            fixes = [f for f in fixes if f.priority == priority_filter]
        
        return {
            "status": "success",
            "pending_fixes": len(fixes),
            "fixes": [{
                "id": f.id,
                "type": f.fix_type,
                "target": f.target,
                "action": f.action,
                "priority": f.priority
            } for f in fixes]
        }

    def _apply_validation_fixes(self, args: dict) -> dict[str, Any]:
        """[validation] Apply fixes with state tracking."""
        import sys
        project_path = args.get("project_path", "")
        confirm = args.get("confirm", False)
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from fix_workflow import FixWorkflowManager
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import fix_workflow: {e}"}
        
        manager = FixWorkflowManager(str(project_path))
        
        # Find latest review
        reviews = list(validation_dir.glob("review_*.json"))
        if not reviews:
            return {"status": "error", "message": "No review files found"}
        
        latest_review = str(max(reviews, key=lambda p: p.stat().st_mtime))
        results = manager.run_fix_workflow(latest_review, dry_run=not confirm)
        
        # Update fix states in state manager
        if confirm and results["applied"]:
            from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
            from migration_agents.shared_run_id import resolve_run_id
            
            parquet_root = Path(self.config.parquet_root)
            run_id = resolve_run_id(parquet_root)
            state_mgr = get_pipeline_state_manager(parquet_root, run_id)
            
            for fix_info in results["applied"]:
                fix_id = fix_info.get("id", "")
                if fix_id:
                    state_mgr.apply_fix(fix_id, "MCP")
        
        return {
            "status": "success",
            "mode": "applied" if confirm else "dry_run",
            "applied": len(results["applied"]),
            "failed": len(results["failed"]),
            "skipped": len(results["skipped"]),
            "message": "Fixes applied" if confirm else "Dry run - set confirm=true to apply",
        }

    def _get_validation_history(self, args: dict) -> dict[str, Any]:
        """[validation] Get validation run history from state manager."""
        solution_name = args.get("solution_name", "")
        limit = args.get("limit", 10)
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(self.config.parquet_root)
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        history = state_mgr.get_validation_history(solution_name, limit)
        
        return {
            "status": "success",
            "solution_name": solution_name,
            "runs": history,
            "total_runs": len(history),
        }

    def _get_version_history(self, args: dict) -> dict[str, Any]:
        """[validation] Get version history."""
        project_path = args.get("project_path", "")
        limit = args.get("limit", 20)
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        history_path = project_path / "validation" / "version_history.json"
        
        if not history_path.exists():
            return {"status": "error", "message": "No version history found"}
        
        with open(history_path) as f:
            history = json.load(f)
        
        entries = history[-limit:]
        
        return {
            "status": "success",
            "total_entries": len(history),
            "entries": entries
        }

    def _compare_versions(self, args: dict) -> dict[str, Any]:
        """[validation] Compare two versions."""
        import sys
        project_path = args.get("project_path", "")
        from_version = args.get("from_version", "")
        to_version = args.get("to_version", "")
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from fix_workflow import FixWorkflowManager
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import fix_workflow: {e}"}
        
        manager = FixWorkflowManager(str(project_path))
        diff = manager.get_version_diff(from_version, to_version)
        
        return {
            "status": "success",
            "from_version": from_version,
            "to_version": to_version,
            "changes": diff.get("changes", [])
        }

    # =========================================================================
    # APPROVAL WORKFLOW HANDLERS
    # =========================================================================

    def _get_step_for_approval(self, args: dict) -> dict[str, Any]:
        """[approval] Get step details with rules for human approval with state tracking."""
        import sys
        project_path = args.get("project_path", "")
        step_name = args.get("step_name", "")
        
        if not step_name:
            return {"status": "error", "message": "step_name is required"}
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        # Initialize pipeline state manager
        from migration_agents.codegen.pipeline_state_manager import (
            get_pipeline_state_manager, ApprovalStatus
        )
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(self.config.parquet_root)
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        solution_name = project_path.name
        
        # Check if approval already exists in state
        existing_approval = state_mgr.get_approval_by_step(solution_name, step_name)
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from approval_workflow import ApprovalWorkflow
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import approval_workflow: {e}"}
        
        workflow = ApprovalWorkflow(str(project_path))
        step_data = workflow.get_step_for_approval(step_name)
        
        if "error" in step_data:
            return {"status": "error", "message": step_data["error"]}
        
        # Create approval step in state if not exists
        if not existing_approval:
            existing_approval = state_mgr.create_approval_step(
                solution_name=solution_name,
                step_name=step_name,
                step_type=step_data.get("step_type", "validation"),
                artifacts=step_data.get("artifacts", {}),
            )
        
        # Format for human display
        rules_display = []
        for rule in step_data.get("rules", []):
            rules_display.append({
                "id": rule["id"],
                "name": rule["name"],
                "description": rule["description"],
                "weight": rule["weight"],
                "threshold": rule["threshold"],
                "current_score": rule.get("current_score", "N/A")
            })
        
        return {
            "status": "success",
            "step_id": existing_approval.step_id,
            "step": step_data["step"],
            "description": step_data["description"],
            "current_status": existing_approval.status.value if hasattr(existing_approval.status, 'value') else existing_approval.status,
            "rules_count": len(rules_display),
            "rules": rules_display,
            "artifacts_to_review": step_data.get("artifacts", []),
            "message": f"Step '{step_name}' ready for approval. Review {len(rules_display)} rules and artifacts before approving."
        }

    def _submit_step_approval(self, args: dict) -> dict[str, Any]:
        """[approval] Submit approval decision for a step with state tracking."""
        import sys
        project_path = args.get("project_path", "")
        step_name = args.get("step_name", "")
        decision = args.get("decision", "")
        reviewer = args.get("reviewer", "human")
        comments = args.get("comments", "")
        
        if not step_name:
            return {"status": "error", "message": "step_name is required"}
        if not decision:
            return {"status": "error", "message": "decision is required (APPROVE/REJECT/SKIP)"}
        if decision.upper() not in ["APPROVE", "REJECT", "SKIP"]:
            return {"status": "error", "message": "decision must be APPROVE, REJECT, or SKIP"}
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        # Initialize pipeline state manager
        from migration_agents.codegen.pipeline_state_manager import (
            get_pipeline_state_manager, ApprovalStatus
        )
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(self.config.parquet_root)
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        solution_name = project_path.name
        
        # Map decision to ApprovalStatus
        status_map = {
            "APPROVE": ApprovalStatus.APPROVED,
            "REJECT": ApprovalStatus.REJECTED,
            "SKIP": ApprovalStatus.NEEDS_REVISION,
        }
        approval_status = status_map.get(decision.upper(), ApprovalStatus.PENDING)
        
        # Get or create approval step
        existing_approval = state_mgr.get_approval_by_step(solution_name, step_name)
        if existing_approval:
            state_mgr.submit_approval(
                existing_approval.step_id,
                approval_status,
                reviewer,
                comments,
            )
        
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from approval_workflow import ApprovalWorkflow
        except ImportError as e:
            return {"status": "error", "message": f"Cannot import approval_workflow: {e}"}
        
        workflow = ApprovalWorkflow(str(project_path))
        result = workflow.submit_approval(
            step_id=step_name,
            decision=decision.upper(),
            approver=reviewer,
            reason=comments if comments else None
        )
        
        if "error" in result:
            return {"status": "error", "message": result["error"]}
        
        # Get next step if approved
        next_step = result.get("next_step")
        
        response = {
            "status": "success",
            "step": step_name,
            "step_id": existing_approval.step_id if existing_approval else None,
            "decision": decision.upper(),
            "reviewer": reviewer,
            "timestamp": result.get("timestamp", ""),
            "message": f"Step '{step_name}' {decision.upper()}D successfully."
        }
        
        if next_step:
            response["next_step"] = next_step
            response["message"] += f" Next step: '{next_step}'"
        elif decision.upper() == "APPROVE":
            response["message"] += " All steps complete!"
        
        return response

    def _get_approval_status(self, args: dict) -> dict[str, Any]:
        """[approval] Get approval status for all steps with state tracking."""
        import sys
        project_path = args.get("project_path", "")
        
        base_path = Path(self.config.parquet_root).parent.parent
        if not Path(project_path).is_absolute():
            project_path = base_path / project_path
        else:
            project_path = Path(project_path)
        
        # Get status from pipeline state manager first
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        parquet_root = Path(self.config.parquet_root)
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        solution_name = project_path.name
        state_status = state_mgr.get_approval_status(solution_name)
        
        # Also get from approval workflow for additional details
        validation_dir = project_path / "validation"
        sys.path.insert(0, str(validation_dir))
        
        try:
            from approval_workflow import ApprovalWorkflow
            workflow = ApprovalWorkflow(str(project_path))
            summary = workflow.get_workflow_summary()
            
            # Format step status
            steps_display = []
            for step in summary.get("steps", []):
                steps_display.append({
                    "order": step["order"],
                    "name": step["name"],
                    "status": step["status"],
                    "reviewer": step.get("reviewer", "-"),
                    "timestamp": step.get("approved_at", "-"),
                    "rules_count": step["rules_count"]
                })
            
            return {
                "status": "success",
                "total_steps": summary["total_steps"],
                "approved": summary["approved"],
                "pending": summary["pending"],
                "rejected": summary["rejected"],
                "skipped": summary["skipped"],
                "current_step": summary.get("current_step"),
                "steps": steps_display,
                "state_tracking": state_status.get("steps", []),
                "message": f"Workflow: {summary['approved']}/{summary['total_steps']} steps approved"
            }
        except ImportError:
            # Fall back to state manager only
            return {
                "status": "success",
                **state_status,
                "message": f"Approval status from state manager for {solution_name}",
            }

    # === COPILOT-POWERED DDD ANALYSIS ===

    def _ddd_analyze_with_copilot(self, args: dict) -> dict[str, Any]:
        """[DDD-Copilot] Prepare DDD analysis for Copilot LLM processing.
        
        This tool gathers endpoint data and returns a structured analysis request
        that Copilot will automatically process and apply.
        """
        import json

        solution_name = args.get("solution_name", "")
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}

        max_endpoints = args.get("max_endpoints", 50)
        min_depth = args.get("min_depth", 0)
        max_depth = args.get("max_depth", 3)

        # Get endpoints data with proper domain names
        try:
            entries = self.db.execute("""
                SELECT 
                    e.entry_key,
                    e.source_ref,
                    e.depth,
                    s.symbol_id,
                    s.name as symbol_name,
                    s.kind as symbol_kind,
                    s.file_path,
                    s.signature
                FROM entry_graphs e
                LEFT JOIN symbols s ON e.source_ref = s.symbol_id
                WHERE e.depth >= ? AND e.depth <= ?
                ORDER BY e.depth, s.name
                LIMIT ?
            """, [min_depth, max_depth, max_endpoints]).fetchall()
        except Exception as e:
            return {"status": "error", "message": f"Failed to query endpoints: {e}"}

        if not entries:
            return {"status": "error", "message": "No endpoints found. Run analyzer first (step: ingest → parse → slice)."}

        # Format endpoints for analysis
        endpoints_by_depth = {}
        for entry in entries:
            depth = entry[2]
            if depth not in endpoints_by_depth:
                endpoints_by_depth[depth] = []
            endpoints_by_depth[depth].append({
                "entry_key": entry[0],
                "name": entry[4] or entry[1] or "Unknown",
                "kind": entry[5] or "method",
                "file": entry[6] or "",
                "signature": entry[7] or "",
            })

        # Build the analysis context for Copilot
        analysis_context = {
            "solution_name": solution_name,
            "total_endpoints": len(entries),
            "depth_range": {"min": min_depth, "max": max_depth},
            "endpoints_by_depth": endpoints_by_depth,
        }

        # Return a structured response that tells Copilot what to do
        return {
            "status": "success",
            "action": "analyze_with_copilot",
            "solution_name": solution_name,
            "endpoints_count": len(entries),
            "context": analysis_context,
            "copilot_instructions": f"""
## DDD Analysis Request for {solution_name}

I have gathered {len(entries)} endpoints from the legacy codebase. Please analyze them and generate a comprehensive DDD domain model.

### Endpoints by Depth Level:
""" + "\n".join([
                f"\n**Depth {depth}** ({len(eps)} endpoints):\n" + "\n".join([
                    f"- `{ep['name']}` ({ep['kind']}) - {ep['file']}"
                    for ep in eps[:15]  # Limit display per depth
                ]) + (f"\n- ... and {len(eps) - 15} more" if len(eps) > 15 else "")
                for depth, eps in sorted(endpoints_by_depth.items())
            ]) + f"""

### Required Analysis Output:
Please provide a JSON object with this structure:
```json
{{
  "ubiquitous_language": [
    {{"term": "Order", "definition": "A customer's request to purchase products", "examples": ["PlaceOrder", "CancelOrder"]}}
  ],
  "bounded_context_candidates": [
    {{
      "name": "OrderManagement",
      "description": "Handles order lifecycle",
      "core_concepts": ["Order", "OrderItem", "OrderStatus"],
      "key_aggregates": ["Order"],
      "confidence": 0.9
    }}
  ],
  "recommended_context": "OrderManagement",
  "aggregates": [
    {{
      "name": "Order",
      "root_entity": "Order",
      "properties": [{{"name": "Id", "type": "Guid", "required": true}}],
      "behaviors": [{{"name": "PlaceOrder", "description": "Creates a new order", "parameters": ["customerId", "items"]}}],
      "domain_events": [{{"name": "OrderPlaced", "trigger": "When order is successfully created"}}],
      "invariants": ["Order must have at least one item"]
    }}
  ],
  "domain_events": [
    {{"name": "OrderPlaced", "aggregate": "Order", "properties": ["orderId", "customerId", "totalAmount"]}}
  ]
}}
```

After you generate the analysis, I will automatically apply it using `ddd_apply_full_analysis`.
""",
            "next_step": "Copilot will analyze this and generate the domain model. The result will be applied via ddd_apply_full_analysis.",
        }

    # === BATCH CODE GENERATION TOOLS ===

    def _batch_codegen(self, args: dict) -> dict[str, Any]:
        """[codegen] Run batch code generation with DDD-first workflow."""
        from pathlib import Path
        from migration_agents.codegen.batch_runner import run_batch_codegen, cleanup_generated, _check_ddd_status
        from migration_agents.codegen.config import load_config
        
        config_path = args.get("config_path", "config/codegen.json")
        phase = args.get("phase", "all")
        batch_size = args.get("batch_size", 500)
        start_batch = args.get("start_batch", 0)
        max_batches = args.get("max_batches")
        cleanup_first = args.get("cleanup_first", False)
        confirm = args.get("confirm", False)
        
        config_path = Path(config_path)
        if not config_path.exists():
            return {
                "status": "error",
                "message": f"Config file not found: {config_path}",
            }
        
        # Preview mode if not confirmed
        if not confirm:
            config = load_config(config_path)
            from migration_agents.shared_run_id import resolve_run_id
            run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
            
            # Get slice count
            try:
                sql = f"""
                    SELECT COUNT(*) as cnt
                    FROM entry_graphs
                    WHERE run_id = '{run_id}' AND artifact_version = {config.artifact_version}
                    AND capped_depth >= 1
                """
                result = self.conn.execute(sql).fetchone()
                total_slices = result[0] if result else 0
            except Exception:
                total_slices = 0
            
            total_batches = (total_slices + batch_size - 1) // batch_size if total_slices > 0 else 0
            
            # Check DDD status
            ddd_output = config.generated_root / config.solution_name / "ddd"
            ddd_status = _check_ddd_status(ddd_output, config.solution_name)
            
            # Determine recommended workflow based on phase and current status
            workflow_guidance = None
            if phase == "code" and not ddd_status["domain_complete"]:
                workflow_guidance = "⚠️ Domain model not found. Run with phase='domain' first."
            elif phase == "code" and not ddd_status["contract_complete"]:
                workflow_guidance = "⚠️ OpenAPI contract not found. Run with phase='contract' first."
            elif phase == "all":
                workflow_guidance = "Will run complete DDD workflow: domain → contract → code"
            
            return {
                "status": "preview",
                "message": "Batch codegen preview (DDD-First). Set confirm=true to run.",
                "config_path": str(config_path),
                "solution_name": config.solution_name,
                "phase": phase,
                "workflow_guidance": workflow_guidance,
                "ddd_status": ddd_status,
                "total_slices": total_slices,
                "batch_size": batch_size,
                "total_batches": total_batches,
                "start_batch": start_batch,
                "max_batches": max_batches or total_batches,
                "cleanup_first": cleanup_first,
                "estimated_batches_to_run": min(max_batches, total_batches - start_batch) if max_batches else total_batches - start_batch,
                "ddd_workflow": {
                    "phase_1": "domain - Build domain model, aggregates, ubiquitous language",
                    "phase_2": "contract - Generate OpenAPI spec from domain model",
                    "phase_3": "code - Generate Clean Architecture implementation",
                },
            }
        
        # Run batch codegen with phase and state tracking
        from migration_agents.codegen.pipeline_state_manager import (
            get_pipeline_state_manager, CodegenPhase, CodegenJobStatus
        )
        from migration_agents.shared_run_id import resolve_run_id
        
        config = load_config(config_path)
        parquet_root = config.output_root
        run_id = resolve_run_id(parquet_root) if config.run_id == "auto" else config.run_id
        
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        # Check for resumable job
        phase_enum = CodegenPhase(phase) if phase in [p.value for p in CodegenPhase] else CodegenPhase.ALL
        existing_job = state_mgr.get_resumable_codegen_job(config.solution_name, phase_enum)
        
        if existing_job:
            # Resume existing job
            state_mgr.update_codegen_job_status(existing_job.job_id, CodegenJobStatus.RUNNING)
            start_batch = existing_job.current_batch
        else:
            # Get slice count for new job
            try:
                sql = f"""
                    SELECT COUNT(*) as cnt
                    FROM entry_graphs
                    WHERE run_id = '{run_id}' AND artifact_version = {config.artifact_version}
                    AND capped_depth >= 1
                """
                result = self.conn.execute(sql).fetchone()
                total_slices = result[0] if result else 0
            except Exception:
                total_slices = 0
            
            # Create new job
            existing_job = state_mgr.create_codegen_job(
                solution_name=config.solution_name,
                phase=phase_enum,
                total_slices=total_slices,
                batch_size=batch_size,
                config={"config_path": str(config_path)},
            )
            state_mgr.update_codegen_job_status(existing_job.job_id, CodegenJobStatus.RUNNING)
        
        result = run_batch_codegen(
            config_path=config_path,
            batch_size=batch_size,
            start_batch=start_batch,
            max_batches=max_batches,
            cleanup_first=cleanup_first,
            phase=phase,
        )
        
        # Update job status based on result
        if result.get("status") == "success":
            state_mgr.update_codegen_job_status(existing_job.job_id, CodegenJobStatus.COMPLETED)
        elif result.get("status") == "error":
            state_mgr.update_codegen_job_status(existing_job.job_id, CodegenJobStatus.FAILED)
        
        result["job_id"] = existing_job.job_id
        return result

    def _cleanup_generated(self, args: dict) -> dict[str, Any]:
        """[codegen] Clean up generated solution files."""
        from pathlib import Path
        from migration_agents.codegen.batch_runner import cleanup_generated
        from migration_agents.codegen.config import load_config
        
        solution_name = args.get("solution_name")
        confirm = args.get("confirm", False)
        
        if not solution_name:
            return {
                "status": "error",
                "message": "solution_name is required",
            }
        
        # Load config to get generated_root
        config_path = Path("config/codegen.json")
        if config_path.exists():
            config = load_config(config_path)
            generated_root = config.generated_root
        else:
            generated_root = Path("generated")
        
        return cleanup_generated(generated_root, solution_name, confirm=confirm)

    def _get_batch_status(self, args: dict) -> dict[str, Any]:
        """[codegen] Get status of generated files for a solution with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.config import load_config
        
        solution_name = args.get("solution_name")
        
        if not solution_name:
            return {
                "status": "error",
                "message": "solution_name is required",
            }
        
        # Load config to get generated_root
        config_path = Path("config/codegen.json")
        if config_path.exists():
            config = load_config(config_path)
            generated_root = config.generated_root
            parquet_root = config.output_root
        else:
            generated_root = Path("generated")
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        # Get job state from pipeline state manager
        from migration_agents.codegen.pipeline_state_manager import get_pipeline_state_manager
        from migration_agents.shared_run_id import resolve_run_id
        
        run_id = resolve_run_id(parquet_root)
        state_mgr = get_pipeline_state_manager(parquet_root, run_id)
        
        latest_job = state_mgr.get_latest_codegen_job(solution_name)
        job_progress = None
        if latest_job:
            job_progress = state_mgr.get_codegen_job_progress(latest_job.job_id)
        
        solution_dir = generated_root / solution_name
        
        if not solution_dir.exists():
            return {
                "status": "not_found",
                "message": f"Solution directory not found: {solution_dir}",
                "path": str(solution_dir),
                "job_state": job_progress,
            }
        
        # Count files by type
        file_counts = {}
        total_files = 0
        total_size = 0
        
        for f in solution_dir.rglob("*"):
            if f.is_file():
                total_files += 1
                total_size += f.stat().st_size
                ext = f.suffix.lower() or "(no extension)"
                file_counts[ext] = file_counts.get(ext, 0) + 1
        
        # Get directory structure (top level)
        top_dirs = [d.name for d in solution_dir.iterdir() if d.is_dir()]
        
        # Check DDD status
        from migration_agents.codegen.batch_runner import _check_ddd_status
        ddd_status = _check_ddd_status(solution_dir / "ddd", solution_name)
        
        # Determine next recommended action
        next_action = None
        if not ddd_status["domain_complete"]:
            next_action = "Run batch_codegen(phase='domain') to build domain model"
        elif not ddd_status["contract_complete"]:
            next_action = "Run batch_codegen(phase='contract') to generate OpenAPI"
        elif file_counts.get(".cs", 0) == 0:
            next_action = "Run batch_codegen(phase='code') to generate implementation"
        else:
            next_action = "Build and test the solution with 'dotnet build'"
        
        return {
            "status": "success",
            "solution_name": solution_name,
            "path": str(solution_dir),
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_counts_by_extension": dict(sorted(file_counts.items(), key=lambda x: -x[1])),
            "top_directories": top_dirs,
            "cs_files": file_counts.get(".cs", 0),
            "feature_files": file_counts.get(".feature", 0),
            "csproj_files": file_counts.get(".csproj", 0),
            "ddd_status": ddd_status,
            "job_state": job_progress,
            "next_action": next_action,
        }

    # =========================================================================
    # BATCH DDD ANALYSIS (for large codebases with 100+ slices)
    # =========================================================================

    def _batch_ddd_analysis(self, args: dict) -> dict[str, Any]:
        """[DDD-Batch] Prepare batches of slices for Copilot-driven DDD analysis with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.batch_ddd_runner import get_all_slices_from_parquet
        from migration_agents.codegen.ddd_state_manager import get_state_manager, JobStatus
        from migration_agents.codegen.config import load_config
        from migration_agents.shared_run_id import resolve_run_id
        
        solution_name = args.get("solution_name")
        if not solution_name:
            return {
                "status": "error",
                "message": "solution_name is required",
            }
        
        batch_size = args.get("batch_size", 50)
        min_depth = args.get("min_depth", 0)
        max_depth = args.get("max_depth", 10)
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        # Get run_id
        run_id = resolve_run_id(parquet_root)
        if not run_id:
            return {
                "status": "error",
                "message": "No run_id found. Run analyzer first.",
            }
        
        # Initialize state manager
        state_mgr = get_state_manager(parquet_root, run_id)
        
        # Check for existing resumable job
        existing_job = state_mgr.get_resumable_job(solution_name)
        if existing_job:
            # Resume existing job
            state_mgr.update_job_status(existing_job.job_id, JobStatus.RUNNING)
            pending = state_mgr.get_pending_slices(existing_job.job_id, limit=batch_size)
            progress = state_mgr.get_job_progress(existing_job.job_id)
            
            return {
                "status": "resumed",
                "message": f"Resumed job {existing_job.job_id} with {len(pending)} pending slices",
                "job_id": existing_job.job_id,
                "progress": progress["progress"],
                "batch_items": [
                    {"slice_id": s.slice_id, "depth": s.depth, "root_name": s.root_name}
                    for s in pending
                ],
                "instructions": "For each slice, analyze and call batch_ddd_apply_slice with results.",
            }
        
        # Get all slices from parquet
        all_slices = get_all_slices_from_parquet(
            parquet_root, run_id, min_depth, max_depth
        )
        
        if not all_slices:
            return {"status": "error", "message": "No slices found. Run analyzer first."}
        
        # Create new job with state tracking
        job = state_mgr.create_job(
            solution_name=solution_name,
            total_slices=len(all_slices),
            batch_size=batch_size,
            min_depth=min_depth,
            max_depth=max_depth,
            llm_provider="copilot",
            llm_model="gpt-4o-mini",
        )
        
        # Create batches and register slices
        total_batches = (len(all_slices) + batch_size - 1) // batch_size
        for batch_num in range(total_batches):
            batch_start = batch_num * batch_size
            batch_end = min(batch_start + batch_size, len(all_slices))
            batch_slices = all_slices[batch_start:batch_end]
            
            batch = state_mgr.create_batch(job.job_id, batch_num, len(batch_slices))
            state_mgr.register_slices(job.job_id, batch.batch_id, batch_slices)
        
        # Start job
        state_mgr.update_job_status(job.job_id, JobStatus.RUNNING)
        
        # Get first batch of pending slices
        pending = state_mgr.get_pending_slices(job.job_id, limit=batch_size)
        
        return {
            "status": "created",
            "message": f"Created job {job.job_id} with {len(all_slices)} slices in {total_batches} batches",
            "job_id": job.job_id,
            "total_slices": len(all_slices),
            "total_batches": total_batches,
            "batch_size": batch_size,
            "batch_items": [
                {"slice_id": s.slice_id, "depth": s.depth, "root_name": s.root_name}
                for s in pending
            ],
            "instructions": "For each slice, analyze and call batch_ddd_apply_slice with results.",
        }

    def _batch_ddd_apply_slice(self, args: dict) -> dict[str, Any]:
        """[DDD-Batch] Apply DDD analysis for a single slice with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager
        from migration_agents.codegen.config import load_config
        from migration_agents.shared_run_id import resolve_run_id
        
        solution_name = args.get("solution_name")
        slice_id = args.get("slice_id")
        analysis = args.get("analysis", {})
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        if not slice_id:
            return {"status": "error", "message": "slice_id is required"}
        if not analysis:
            return {"status": "error", "message": "analysis object is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        run_id = resolve_run_id(parquet_root)
        if not run_id:
            return {"status": "error", "message": "No run_id found"}
        
        # Save to state manager
        state_mgr = get_state_manager(parquet_root, run_id)
        job = state_mgr.get_latest_job_for_solution(solution_name)
        
        if not job:
            return {
                "status": "error", 
                "message": f"No job found for solution '{solution_name}'. Run batch_ddd_analysis first."
            }
        
        try:
            state_mgr.save_slice_analysis(slice_id, job.job_id, analysis)
            # Update job progress
            analyzed_count = len(state_mgr.get_analyzed_slices(job.job_id))
            state_mgr.update_job_progress(job.job_id, analyzed_slices=analyzed_count)
        except ValueError as e:
            return {"status": "error", "message": f"Failed to save analysis: {e}"}
        
        # Get updated progress
        progress = state_mgr.get_job_progress(job.job_id)
        
        return {
            "status": "ok",
            "message": f"Saved analysis for slice {slice_id}",
            "slice_id": slice_id,
            "job_id": job.job_id,
            "progress": progress["progress"],
        }

    def _batch_ddd_status(self, args: dict) -> dict[str, Any]:
        """[DDD-Batch] Get current status of batch DDD analysis with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager
        from migration_agents.codegen.config import load_config
        from migration_agents.shared_run_id import resolve_run_id
        
        solution_name = args.get("solution_name")
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        run_id = resolve_run_id(parquet_root)
        if not run_id:
            return {"status": "error", "message": "No run_id found"}
        
        # Get status from state manager
        state_mgr = get_state_manager(parquet_root, run_id)
        job = state_mgr.get_latest_job_for_solution(solution_name)
        
        if not job:
            return {
                "status": "error",
                "message": f"No job found for solution '{solution_name}'. Run batch_ddd_analysis first."
            }
        
        progress = state_mgr.get_job_progress(job.job_id)
        context_summary = state_mgr.get_bounded_context_summary(job.job_id)
        
        return {
            "status": "ok",
            **progress,
            "bounded_contexts": context_summary.get("bounded_contexts", []),
        }

    def _batch_ddd_build_model(self, args: dict) -> dict[str, Any]:
        """[DDD-Batch] Build unified domain model from analyzed slices with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager, JobStatus
        from migration_agents.codegen.config import load_config
        from migration_agents.shared_run_id import resolve_run_id
        
        solution_name = args.get("solution_name")
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        run_id = resolve_run_id(parquet_root)
        if not run_id:
            return {"status": "error", "message": "No run_id found"}
        
        # Get job from state manager
        state_mgr = get_state_manager(parquet_root, run_id)
        job = state_mgr.get_latest_job_for_solution(solution_name)
        
        if not job:
            return {
                "status": "error",
                "message": f"No job found for solution '{solution_name}'. Run batch_ddd_analysis first."
            }
        
        # Synthesize from state manager (no LLM needed)
        model_summary = state_mgr.synthesize_domain_model(job.job_id)
        
        # Mark job as completed
        state_mgr.update_job_status(job.job_id, JobStatus.COMPLETED)
        
        model_summary["job_id"] = job.job_id
        return model_summary

    # === DDD Progress Tracking (Parquet-based State Management) ===

    def _ddd_get_job_progress(self, args: dict) -> dict[str, Any]:
        """[DDD-Progress] Get comprehensive progress report for a DDD analysis job."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager
        from migration_agents.codegen.config import load_config
        
        solution_name = args.get("solution_name")
        job_id = args.get("job_id")
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        state_mgr = get_state_manager(parquet_root)
        
        # Get job (by ID or latest for solution)
        if job_id:
            job = state_mgr.get_job(job_id)
        else:
            job = state_mgr.get_latest_job_for_solution(solution_name)
        
        if not job:
            return {
                "status": "no_job",
                "message": f"No DDD job found for solution '{solution_name}'",
                "hint": "Use ddd_create_job to create a new job, or batch_ddd_analysis to start processing",
            }
        
        progress = state_mgr.get_job_progress(job.job_id)
        return {
            "status": "ok",
            **progress,
        }

    def _ddd_list_pending_slices(self, args: dict) -> dict[str, Any]:
        """[DDD-Progress] List slices that still need analysis."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager
        from migration_agents.codegen.config import load_config
        
        solution_name = args.get("solution_name")
        limit = args.get("limit", 50)
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        state_mgr = get_state_manager(parquet_root)
        job = state_mgr.get_latest_job_for_solution(solution_name)
        
        if not job:
            return {
                "status": "no_job",
                "message": f"No DDD job found for solution '{solution_name}'",
            }
        
        pending = state_mgr.get_pending_slices(job.job_id, limit=limit)
        
        return {
            "status": "ok",
            "job_id": job.job_id,
            "pending_count": len(pending),
            "limit": limit,
            "slices": [
                {
                    "slice_id": s.slice_id,
                    "depth": s.depth,
                    "root_name": s.root_name,
                }
                for s in pending
            ],
        }

    def _ddd_resume_job(self, args: dict) -> dict[str, Any]:
        """[DDD-Progress] Resume a paused or interrupted DDD analysis job."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager, JobStatus
        from migration_agents.codegen.config import load_config
        
        solution_name = args.get("solution_name")
        batch_size = args.get("batch_size")
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        state_mgr = get_state_manager(parquet_root)
        job = state_mgr.get_resumable_job(solution_name)
        
        if not job:
            # Check if there's a completed job
            latest = state_mgr.get_latest_job_for_solution(solution_name)
            if latest:
                return {
                    "status": "job_not_resumable",
                    "message": f"Latest job '{latest.job_id}' has status '{latest.status.value}' and cannot be resumed",
                    "hint": "Use ddd_create_job to start a new job",
                }
            return {
                "status": "no_job",
                "message": f"No resumable job found for solution '{solution_name}'",
                "hint": "Use ddd_create_job or batch_ddd_analysis to start",
            }
        
        # Get next batch to process
        next_batch = state_mgr.get_next_pending_batch(job.job_id)
        pending_slices = state_mgr.get_pending_slices(job.job_id, limit=batch_size or job.batch_size)
        
        # Update job to running
        state_mgr.update_job_status(job.job_id, JobStatus.RUNNING)
        
        return {
            "status": "resumed",
            "job_id": job.job_id,
            "solution_name": job.solution_name,
            "progress": {
                "total_slices": job.total_slices,
                "analyzed_slices": job.analyzed_slices,
                "remaining": job.total_slices - job.analyzed_slices - job.skipped_slices,
            },
            "next_batch": next_batch.batch_id if next_batch else None,
            "pending_slice_count": len(pending_slices),
            "message": f"Resumed job {job.job_id}. {len(pending_slices)} slices ready to analyze.",
        }

    def _ddd_get_context_summary(self, args: dict) -> dict[str, Any]:
        """[DDD-Progress] Get summary of bounded contexts discovered so far."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager
        from migration_agents.codegen.config import load_config
        
        solution_name = args.get("solution_name")
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        state_mgr = get_state_manager(parquet_root)
        job = state_mgr.get_latest_job_for_solution(solution_name)
        
        if not job:
            return {
                "status": "no_job",
                "message": f"No DDD job found for solution '{solution_name}'",
            }
        
        summary = state_mgr.get_bounded_context_summary(job.job_id)
        
        return {
            "status": "ok",
            **summary,
        }

    def _ddd_create_job(self, args: dict) -> dict[str, Any]:
        """[DDD-Progress] Create a new DDD analysis job with state tracking."""
        from pathlib import Path
        from migration_agents.codegen.ddd_state_manager import get_state_manager
        from migration_agents.codegen.config import load_config
        from migration_agents.shared_run_id import resolve_run_id
        
        solution_name = args.get("solution_name")
        batch_size = args.get("batch_size", 50)
        min_depth = args.get("min_depth", 0)
        max_depth = args.get("max_depth", 10)
        
        if not solution_name:
            return {"status": "error", "message": "solution_name is required"}
        
        # Load config
        config_path = Path("config/codegen.json")
        if config_path.exists():
            codegen_config = load_config(config_path)
            parquet_root = codegen_config.output_root
        else:
            parquet_root = Path(DEFAULT_PARQUET_ROOT)
        
        run_id = resolve_run_id(parquet_root)
        if not run_id:
            return {"status": "error", "message": "No run_id found. Run analyzer first."}
        
        # Count total slices from parquet using run-specific database
        from migration_agents.mcp.duckdb_catalog import get_run_connection
        conn, _ = get_run_connection(parquet_root, run_id)
        try:
            manifest_path = Path(parquet_root) / run_id / "slice_manifest.parquet"
            if not manifest_path.exists():
                return {"status": "error", "message": f"slice_manifest.parquet not found at {manifest_path}"}
            
            count_result = conn.execute(f"""
                SELECT COUNT(DISTINCT slice_id) 
                FROM read_parquet('{manifest_path}')
                WHERE depth >= {min_depth} AND depth <= {max_depth}
            """).fetchone()
            total_slices = count_result[0] if count_result else 0
            
            if total_slices == 0:
                return {"status": "error", "message": "No slices found matching depth criteria"}
        finally:
            conn.close()
        
        state_mgr = get_state_manager(parquet_root, run_id)
        
        # Check for existing resumable job
        existing = state_mgr.get_resumable_job(solution_name)
        if existing:
            return {
                "status": "existing_job",
                "message": f"Resumable job already exists: {existing.job_id}",
                "job_id": existing.job_id,
                "progress": {
                    "total": existing.total_slices,
                    "analyzed": existing.analyzed_slices,
                    "remaining": existing.total_slices - existing.analyzed_slices - existing.skipped_slices,
                },
                "hint": "Use ddd_resume_job to continue, or clean_pipeline to start fresh",
            }
        
        # Create new job
        job = state_mgr.create_job(
            solution_name=solution_name,
            total_slices=total_slices,
            batch_size=batch_size,
            min_depth=min_depth,
            max_depth=max_depth,
            llm_provider="copilot",
            llm_model="gpt-4o-mini",
        )
        
        return {
            "status": "created",
            "job_id": job.job_id,
            "solution_name": solution_name,
            "total_slices": total_slices,
            "total_batches": job.total_batches,
            "batch_size": batch_size,
            "depth_range": f"{min_depth}-{max_depth}",
            "message": f"Created job {job.job_id} to analyze {total_slices} slices in {job.total_batches} batches",
        }