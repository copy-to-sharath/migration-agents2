#!/usr/bin/env python3
"""
Batch DDD Analysis Script for Large Codebases.

This script processes slices in batches, calling the LLM for DDD analysis
and saving results. It supports:
- Rate limiting to avoid LLM throttling  
- Checkpointing for resumption
- Progress tracking

Usage:
    python scripts/run_batch_ddd_analysis.py --solution NopCommerce

For very large codebases, run with --max-batches to process incrementally:
    python scripts/run_batch_ddd_analysis.py --solution NopCommerce --max-batches 10

Environment Variables:
    OPENAI_API_KEY     Required for OpenAI provider
    GEMINI_API_KEY     Required for Gemini provider
    
Or create a .env file in project root with the keys.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Load .env file if it exists
def load_dotenv():
    """Load environment variables from .env file."""
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value and key not in os.environ:
                    os.environ[key] = value

load_dotenv()

from migration_agents.codegen.batch_ddd_runner import (
    BatchDDDConfig,
    run_batch_ddd_analysis,
    apply_batch_slice_analysis,
    get_batch_ddd_status,
    build_unified_domain_model,
    DDDBatchProgress,
    analyze_slice_with_llm,
)
from migration_agents.codegen.config import load_config
from migration_agents.shared_run_id import resolve_run_id
from migration_agents.logging_utils import setup_logging

LOGGER = logging.getLogger("batch_ddd_analysis")


def process_batch(
    config: BatchDDDConfig,
    batch_items: list[dict],
    delay_between_slices: float = 0.5,
) -> tuple[int, int]:
    """
    Process a batch of slices using LLM analysis.
    
    Args:
        config: Batch configuration (must have llm_provider set)
        batch_items: List of slice items with prompts
        delay_between_slices: Delay between processing each slice
        
    Returns:
        Tuple of (successful_count, failed_count)
    """
    successful = 0
    failed = 0
    
    for i, item in enumerate(batch_items):
        slice_id = item.get("slice_id", "")
        LOGGER.info("  [%d/%d] Analyzing slice %s...", i + 1, len(batch_items), slice_id[:16])
        
        try:
            # Use LLM-based analysis only - no heuristics
            analysis = analyze_slice_with_llm(config, item)
            
            # Save the analysis
            result = apply_batch_slice_analysis(config, slice_id, analysis)
            
            if result.get("status") == "saved":
                successful += 1
                LOGGER.info("    → Saved: %s (%s)", 
                           analysis.get("aggregate_name"), 
                           analysis.get("bounded_context_hint"))
            else:
                failed += 1
                LOGGER.warning("    → Failed to save: %s", result.get("message", "Unknown error"))
                
        except Exception as e:
            failed += 1
            LOGGER.error("    → Error: %s", e)
        
        # Rate limiting
        if delay_between_slices > 0 and i < len(batch_items) - 1:
            time.sleep(delay_between_slices)
    
    return successful, failed


def run_batch_processing(
    solution_name: str,
    batch_size: int = 50,
    max_batches: int | None = None,
    min_depth: int = 0,
    max_depth: int = 10,
    delay_between_slices: float = 0.5,
    delay_between_batches: float = 2.0,
    llm_provider: str = "copilot",
    llm_model: str = "gpt-4o",
    build_model_after: bool = True,
) -> dict:
    """
    Run the complete batch DDD analysis process using LLM.
    
    Args:
        solution_name: Name of the solution (e.g., 'NopCommerce')
        batch_size: Number of slices per batch
        max_batches: Maximum batches to process (None = all)
        min_depth: Minimum slice depth to include
        max_depth: Maximum slice depth to include
        delay_between_slices: Delay between each slice analysis
        delay_between_batches: Delay between batches
        llm_provider: LLM provider ('openai', 'gemini', 'azure', 'github', 'copilot')
        llm_model: LLM model name
        build_model_after: If True, build domain model after all slices analyzed
        
    Returns:
        Summary dict with results
    """
    setup_logging("batch_ddd")
    
    # Validate API key is available
    provider = llm_provider.lower()
    if provider == "openai" and not os.environ.get("OPENAI_API_KEY"):
        return {"status": "error", "message": "OPENAI_API_KEY environment variable required. Set it or use --api-key"}
    elif provider == "gemini" and not os.environ.get("GEMINI_API_KEY"):
        return {"status": "error", "message": "GEMINI_API_KEY environment variable required. Set it or use --api-key"}
    elif provider == "azure" and not os.environ.get("AZURE_OPENAI_API_KEY"):
        return {"status": "error", "message": "AZURE_OPENAI_API_KEY environment variable required. Set it or use --api-key"}
    elif provider in ("github", "copilot") and not os.environ.get("GITHUB_TOKEN"):
        return {"status": "error", "message": "GITHUB_TOKEN environment variable required. Set it or use --api-key"}
    
    # Load config
    config_path = Path("config/codegen.json")
    if config_path.exists():
        codegen_config = load_config(config_path)
        parquet_root = codegen_config.output_root
        output_root = codegen_config.generated_root
        artifact_version = codegen_config.artifact_version
    else:
        parquet_root = Path("data/parquet")
        output_root = Path("generated")
        artifact_version = 1
    
    run_id = resolve_run_id(parquet_root)
    if not run_id:
        return {"status": "error", "message": "No run_id found. Run analyzer first."}
    
    LOGGER.info("=" * 60)
    LOGGER.info("BATCH DDD ANALYSIS")
    LOGGER.info("=" * 60)
    LOGGER.info("Solution: %s", solution_name)
    LOGGER.info("Run ID: %s", run_id)
    LOGGER.info("Batch size: %d", batch_size)
    LOGGER.info("Depth range: %d-%d", min_depth, max_depth)
    LOGGER.info("LLM Provider: %s (model: %s)", llm_provider, llm_model)
    LOGGER.info("")
    
    # Create batch config
    batch_config = BatchDDDConfig(
        solution_name=solution_name,
        parquet_root=parquet_root,
        output_root=output_root,
        run_id=run_id,
        artifact_version=artifact_version,
        batch_size=batch_size,
        min_depth=min_depth,
        max_depth=max_depth,
        delay_between_slices=delay_between_slices,
        delay_between_batches=delay_between_batches,
        llm_provider=llm_provider,
        llm_model=llm_model,
    )
    
    # Get initial status
    status = get_batch_ddd_status(batch_config)
    LOGGER.info("Initial status: %d/%d slices analyzed", 
                status.get("analyzed_slices", 0), 
                status.get("total_slices", 0))
    
    total_successful = 0
    total_failed = 0
    batches_processed = 0
    start_time = datetime.now(timezone.utc)
    
    # Process batches
    current_batch = 0
    while True:
        # Check if we've hit max_batches limit
        if max_batches is not None and batches_processed >= max_batches:
            LOGGER.info("Reached max_batches limit (%d)", max_batches)
            break
        
        # Get next batch
        batch_config.start_batch = current_batch
        batch_config.max_batches = 1
        
        result = run_batch_ddd_analysis(batch_config)
        
        if result.get("status") == "complete":
            LOGGER.info("All slices have been analyzed!")
            break
        
        if result.get("status") != "batch_ready":
            LOGGER.error("Unexpected status: %s", result.get("status"))
            break
        
        batch_items = result.get("batch_items", [])
        if not batch_items:
            LOGGER.info("No more slices to process")
            break
        
        batch_num = result.get("batch_number", current_batch + 1)
        total_batches = result.get("total_batches", 1)
        
        LOGGER.info("")
        LOGGER.info("=" * 40)
        LOGGER.info("BATCH %d of %d (%d slices)", batch_num, total_batches, len(batch_items))
        LOGGER.info("=" * 40)
        
        # Process this batch with LLM
        successful, failed = process_batch(
            batch_config,
            batch_items,
            delay_between_slices=delay_between_slices,
        )
        
        total_successful += successful
        total_failed += failed
        batches_processed += 1
        current_batch += 1
        
        # Log progress
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        slices_per_min = (total_successful + total_failed) / elapsed * 60 if elapsed > 0 else 0
        LOGGER.info("Batch %d complete: %d success, %d failed (%.1f slices/min)", 
                   batch_num, successful, failed, slices_per_min)
        
        # Delay between batches
        if delay_between_batches > 0:
            LOGGER.info("Waiting %.1f seconds before next batch...", delay_between_batches)
            time.sleep(delay_between_batches)
    
    # Final status
    final_status = get_batch_ddd_status(batch_config)
    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    LOGGER.info("")
    LOGGER.info("=" * 60)
    LOGGER.info("BATCH PROCESSING COMPLETE")
    LOGGER.info("=" * 60)
    LOGGER.info("Batches processed: %d", batches_processed)
    LOGGER.info("Slices analyzed: %d success, %d failed", total_successful, total_failed)
    LOGGER.info("Total analyzed: %d/%d", final_status.get("analyzed_slices", 0), final_status.get("total_slices", 0))
    LOGGER.info("Bounded contexts: %s", final_status.get("bounded_contexts_found", []))
    LOGGER.info("Elapsed time: %.1f seconds", elapsed)
    
    # Build domain model if requested and all slices are done
    if build_model_after and final_status.get("remaining_slices", 1) == 0:
        LOGGER.info("")
        LOGGER.info("Building unified domain model...")
        model_result = build_unified_domain_model(batch_config)
        LOGGER.info("Domain model: %s", model_result.get("status"))
        if model_result.get("status") == "success":
            LOGGER.info("  Aggregates: %d", model_result.get("aggregates_count", 0))
            LOGGER.info("  Bounded contexts: %s", model_result.get("bounded_contexts", []))
            LOGGER.info("  Domain file: %s", model_result.get("domain_file", ""))
    
    return {
        "status": "success",
        "batches_processed": batches_processed,
        "slices_analyzed": total_successful,
        "slices_failed": total_failed,
        "elapsed_seconds": elapsed,
        "final_status": final_status,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Batch DDD Analysis for Large Codebases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use GitHub Copilot LLM (default - requires GITHUB_TOKEN)
  python scripts/run_batch_ddd_analysis.py --solution NopCommerce

  # Use OpenAI instead
  python scripts/run_batch_ddd_analysis.py --solution NopCommerce --provider openai --model gpt-4o-mini

  # Use Gemini
  python scripts/run_batch_ddd_analysis.py --solution NopCommerce --provider gemini --model gemini-1.5-flash

  # Process 10 batches of 20 slices each (for testing)
  python scripts/run_batch_ddd_analysis.py --solution NopCommerce --batch-size 20 --max-batches 10

  # Focus on high-depth slices (more complex)
  python scripts/run_batch_ddd_analysis.py --solution NopCommerce --min-depth 5

Environment Variables:
  GITHUB_TOKEN          Required for GitHub/Copilot provider (default)
  OPENAI_API_KEY        Required for OpenAI provider
  GEMINI_API_KEY        Required for Gemini provider
  AZURE_OPENAI_API_KEY  Required for Azure provider
        """
    )
    parser.add_argument("--solution", "-s", required=True, help="Solution name (e.g., 'NopCommerce')")
    parser.add_argument("--batch-size", "-b", type=int, default=50, help="Slices per batch (default: 50)")
    parser.add_argument("--max-batches", "-m", type=int, default=None, help="Max batches to process (default: all)")
    parser.add_argument("--min-depth", type=int, default=0, help="Minimum slice depth (default: 0)")
    parser.add_argument("--max-depth", type=int, default=10, help="Maximum slice depth (default: 10)")
    parser.add_argument("--delay-slices", type=float, default=0.5, help="Delay between slices in seconds (default: 0.5)")
    parser.add_argument("--delay-batches", type=float, default=2.0, help="Delay between batches in seconds (default: 2.0)")
    parser.add_argument("--provider", type=str, default="copilot", choices=["openai", "gemini", "azure", "github", "copilot"], help="LLM provider (default: copilot)")
    parser.add_argument("--model", type=str, default="gpt-4o", help="LLM model (default: gpt-4o)")
    parser.add_argument("--api-key", type=str, default=None, help="API key (alternative to environment variable)")
    parser.add_argument("--skip-model", action="store_true", help="Skip building domain model after analysis")
    
    args = parser.parse_args()
    
    # Set API key from argument if provided
    if args.api_key:
        if args.provider == "openai":
            os.environ["OPENAI_API_KEY"] = args.api_key
        elif args.provider == "gemini":
            os.environ["GEMINI_API_KEY"] = args.api_key
        elif args.provider == "azure":
            os.environ["AZURE_OPENAI_API_KEY"] = args.api_key
        elif args.provider in ("github", "copilot"):
            os.environ["GITHUB_TOKEN"] = args.api_key
    
    result = run_batch_processing(
        solution_name=args.solution,
        batch_size=args.batch_size,
        max_batches=args.max_batches,
        min_depth=args.min_depth,
        max_depth=args.max_depth,
        delay_between_slices=args.delay_slices,
        delay_between_batches=args.delay_batches,
        llm_provider=args.provider,
        llm_model=args.model,
        build_model_after=not args.skip_model,
    )
    
    print(json.dumps(result, indent=2, default=str))
    
    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
