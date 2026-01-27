#!/usr/bin/env python3
"""
Copilot-Driven DDD Batch Analysis.

This script prepares batches of slices for Copilot (in VS Code conversation)
to analyze directly. No external API needed.

Workflow:
1. Run with --prepare to get a batch of prompts
2. Copilot analyzes and returns JSON
3. Run with --apply to save Copilot's analysis
4. Repeat until all slices are done

Usage:
    # Prepare next batch (outputs prompts for Copilot)
    python scripts/copilot_ddd_batch.py --solution NopCommerce --prepare --batch-size 20

    # Apply Copilot's analysis (paste JSON response)
    python scripts/copilot_ddd_batch.py --solution NopCommerce --apply --input analyses.json

    # Check status
    python scripts/copilot_ddd_batch.py --solution NopCommerce --status
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from migration_agents.codegen.batch_ddd_runner import (
    BatchDDDConfig,
    get_all_slices_from_parquet,
    get_slice_context_from_parquet,
    build_ddd_analysis_prompt_for_slice,
    load_existing_analyses,
    apply_batch_slice_analysis,
    build_unified_domain_model,
    get_batch_ddd_status,
)
from migration_agents.shared_run_id import resolve_run_id


def get_config(solution_name: str) -> BatchDDDConfig:
    """Get batch config for solution."""
    from migration_agents.codegen.config import load_config
    
    config_path = Path("config/codegen.json")
    if config_path.exists():
        codegen_config = load_config(config_path)
        parquet_root = codegen_config.output_root
        output_root = codegen_config.generated_root
    else:
        parquet_root = Path("data/parquet")
        output_root = Path("generated")
    
    run_id = resolve_run_id(parquet_root)
    if not run_id:
        raise RuntimeError("No run_id found. Run analyzer first.")
    
    return BatchDDDConfig(
        solution_name=solution_name,
        parquet_root=parquet_root,
        output_root=output_root,
        run_id=run_id,
    )


def prepare_batch(solution_name: str, batch_size: int = 20, min_depth: int = 1) -> dict:
    """Prepare a batch of slices for Copilot to analyze."""
    config = get_config(solution_name)
    
    # Get all slices
    all_slices = get_all_slices_from_parquet(
        config.parquet_root, config.run_id, 
        min_depth=min_depth, max_depth=10
    )
    
    # Load existing analyses
    existing = load_existing_analyses(config)
    
    # Filter to unanalyzed slices
    remaining = [s for s in all_slices if s.get("slice_id") not in existing]
    
    if not remaining:
        return {
            "status": "complete",
            "message": f"All {len(all_slices)} slices already analyzed!",
            "next_step": "Run --build to create domain model",
        }
    
    # Take next batch
    batch = remaining[:batch_size]
    
    # Build prompts for each slice
    prompts = []
    for s in batch:
        slice_id = s["slice_id"]
        context = get_slice_context_from_parquet(config.parquet_root, config.run_id, slice_id)
        
        # Add slice info to context
        context["root_name"] = s.get("root_name") if s.get("root_name") == s.get("root_name") else ""
        context["root_file"] = s.get("root_file") if s.get("root_file") == s.get("root_file") else ""
        context["depth"] = s.get("depth", 1)
        
        prompts.append({
            "slice_id": slice_id,
            "root_name": context.get("root_name", ""),
            "root_file": str(context.get("root_file", ""))[-60:],
            "depth": int(context.get("depth", 1)),
            "symbols": context.get("symbols", [])[:10],
        })
    
    instructions = (
        "Analyze each slice and return a JSON array with DDD analysis. "
        "Include: slice_id, aggregate_name, description, bounded_context_hint, "
        "properties, behaviors, domain_events, invariants. "
        f"Then run: python scripts/copilot_ddd_batch.py --solution {solution_name} --apply"
    )
    
    return {
        "status": "batch_ready",
        "total_slices": len(all_slices),
        "analyzed": len(existing),
        "remaining": len(remaining),
        "batch_size": len(batch),
        "slices": prompts,
        "instructions": instructions,
    }


def apply_analyses(solution_name: str, analyses: list[dict]) -> dict:
    """Apply Copilot's analyses to the solution."""
    config = get_config(solution_name)
    
    saved = 0
    failed = 0
    
    for analysis in analyses:
        slice_id = analysis.get("slice_id", "")
        if not slice_id:
            failed += 1
            continue
        
        try:
            result = apply_batch_slice_analysis(config, slice_id, analysis)
            if result.get("status") == "saved":
                saved += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Error saving {slice_id[:16]}: {e}", file=sys.stderr)
            failed += 1
    
    return {
        "status": "applied",
        "saved": saved,
        "failed": failed,
        "next_step": f"Run --prepare to get next batch, or --status to check progress",
    }


def show_status(solution_name: str) -> dict:
    """Show current analysis status."""
    config = get_config(solution_name)
    return get_batch_ddd_status(config)


def build_model(solution_name: str) -> dict:
    """Build unified domain model from analyses."""
    config = get_config(solution_name)
    return build_unified_domain_model(config)


def main():
    parser = argparse.ArgumentParser(description="Copilot-Driven DDD Batch Analysis")
    parser.add_argument("--solution", "-s", required=True, help="Solution name")
    parser.add_argument("--prepare", action="store_true", help="Prepare next batch for Copilot")
    parser.add_argument("--apply", action="store_true", help="Apply Copilot's analysis")
    parser.add_argument("--status", action="store_true", help="Show analysis status")
    parser.add_argument("--build", action="store_true", help="Build domain model")
    parser.add_argument("--batch-size", "-b", type=int, default=20, help="Slices per batch")
    parser.add_argument("--min-depth", type=int, default=1, help="Minimum depth")
    parser.add_argument("--input", "-i", type=str, help="JSON file with analyses")
    
    args = parser.parse_args()
    
    if args.status:
        result = show_status(args.solution)
    elif args.prepare:
        result = prepare_batch(args.solution, args.batch_size, args.min_depth)
    elif args.apply:
        if args.input:
            data = json.loads(Path(args.input).read_text())
        else:
            print("Paste Copilot's JSON analysis (end with Ctrl+D):", file=sys.stderr)
            data = json.loads(sys.stdin.read())
        # Handle both formats: direct array or wrapped in {"analyses": [...]}
        if isinstance(data, list):
            analyses = data
        elif isinstance(data, dict) and "analyses" in data:
            analyses = data["analyses"]
        else:
            analyses = data
        result = apply_analyses(args.solution, analyses)
    elif args.build:
        result = build_model(args.solution)
    else:
        parser.print_help()
        return 1
    
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
