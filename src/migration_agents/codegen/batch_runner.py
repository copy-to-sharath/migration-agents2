"""Batch code generation runner for large-scale migrations.

This module provides batch processing of codegen for large codebases,
with support for cleanup, progress tracking, and resumption.

WORKFLOW (DDD-First):
  Phase 1: DDD Analysis     → Analyze slices, build domain model, identify aggregates
  Phase 2: OpenAPI Contract → Generate OpenAPI spec from domain model  
  Phase 3: Code Generation  → Generate Clean Architecture code from contract

The workflow ensures:
- Domain model is complete before generating contracts
- OpenAPI contract is generated from DDD aggregates
- Code is forward-engineered from the contract (not reverse-engineered)
"""
from __future__ import annotations

import json
import logging
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Literal

from migration_agents.logging_utils import setup_logging
from migration_agents.ingestion.mcp_client import get_mcp_client
from migration_agents.shared_run_id import resolve_run_id

from .config import CodegenConfig, load_config
from .main import run_ddd_first

LOGGER = logging.getLogger("migration_agents.codegen.batch_runner")

# Valid phases for DDD-first workflow
DDDPhase = Literal["domain", "gherkin", "contract", "code", "all"]


@dataclass
class BatchProgress:
    """Progress tracking for batch processing."""
    total_slices: int = 0
    total_batches: int = 0
    completed_batches: int = 0
    completed_slices: int = 0
    failed_batches: list[int] = field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    total_files_generated: int = 0
    total_cs_files: int = 0
    total_feature_files: int = 0
    
    @property
    def elapsed_seconds(self) -> float:
        if not self.start_time:
            return 0.0
        end = self.end_time or datetime.now(timezone.utc)
        return (end - self.start_time).total_seconds()
    
    @property
    def slices_per_second(self) -> float:
        if self.elapsed_seconds == 0:
            return 0.0
        return self.completed_slices / self.elapsed_seconds
    
    @property
    def estimated_remaining_seconds(self) -> float:
        if self.slices_per_second == 0:
            return 0.0
        remaining = self.total_slices - self.completed_slices
        return remaining / self.slices_per_second
    
    def to_dict(self) -> dict:
        return {
            "total_slices": self.total_slices,
            "total_batches": self.total_batches,
            "completed_batches": self.completed_batches,
            "completed_slices": self.completed_slices,
            "failed_batches": self.failed_batches,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "elapsed_seconds": self.elapsed_seconds,
            "slices_per_second": self.slices_per_second,
            "estimated_remaining_seconds": self.estimated_remaining_seconds,
            "total_files_generated": self.total_files_generated,
            "total_cs_files": self.total_cs_files,
            "total_feature_files": self.total_feature_files,
        }


def _count_generated_files(output_dir: Path) -> tuple[int, int, int]:
    """Count generated files: (total, cs_files, feature_files)."""
    if not output_dir.exists():
        return 0, 0, 0
    
    total = 0
    cs_files = 0
    feature_files = 0
    
    for f in output_dir.rglob("*"):
        if f.is_file():
            total += 1
            if f.suffix == ".cs":
                cs_files += 1
            elif f.suffix == ".feature":
                feature_files += 1
    
    return total, cs_files, feature_files


def _check_ddd_status(ddd_output: Path, solution_name: str) -> dict:
    """Check the status of DDD artifacts.
    
    Returns:
        Dict with status of each DDD phase:
        - domain_complete: Domain model markdown exists
        - gherkin_complete: Feature files exist
        - contract_complete: OpenAPI JSON exists
        - aggregates_count: Number of aggregates detected
        - features_count: Number of feature files
    """
    status = {
        "domain_complete": False,
        "gherkin_complete": False,
        "contract_complete": False,
        "aggregates_count": 0,
        "features_count": 0,
        "domain_model_path": None,
        "contract_path": None,
    }
    
    # Check domain model
    domain_path = ddd_output / "domain" / f"{solution_name}_domain.md"
    if domain_path.exists():
        status["domain_complete"] = True
        status["domain_model_path"] = str(domain_path)
        # Count aggregates from the domain model
        try:
            content = domain_path.read_text()
            status["aggregates_count"] = content.count("## Aggregate:")
        except Exception:
            pass
    
    # Check Gherkin features
    features_dir = ddd_output / "features"
    if features_dir.exists():
        feature_files = list(features_dir.glob("*.feature"))
        status["features_count"] = len(feature_files)
        status["gherkin_complete"] = len(feature_files) > 0
    
    # Check OpenAPI contract
    contract_path = ddd_output / "contracts" / f"{solution_name}Api.openapi.json"
    if contract_path.exists():
        status["contract_complete"] = True
        status["contract_path"] = str(contract_path)
        # Validate contract has endpoints
        try:
            contract_data = json.loads(contract_path.read_text())
            paths = contract_data.get("paths", {})
            status["contract_endpoints"] = len(paths)
        except Exception:
            status["contract_endpoints"] = 0
    
    return status


def cleanup_generated(
    generated_root: Path,
    solution_name: str,
    confirm: bool = False,
) -> dict:
    """Clean up generated files for a solution.
    
    Args:
        generated_root: Root directory for generated output
        solution_name: Name of the solution to clean
        confirm: Must be True to actually delete files
        
    Returns:
        Dict with cleanup status and counts
    """
    solution_dir = generated_root / solution_name
    
    if not solution_dir.exists():
        return {
            "status": "not_found",
            "message": f"Solution directory not found: {solution_dir}",
            "deleted": False,
        }
    
    # Count files before cleanup
    total, cs_files, feature_files = _count_generated_files(solution_dir)
    
    if not confirm:
        return {
            "status": "preview",
            "message": f"Would delete {solution_dir} containing {total} files ({cs_files} .cs, {feature_files} .feature)",
            "path": str(solution_dir),
            "total_files": total,
            "cs_files": cs_files,
            "feature_files": feature_files,
            "deleted": False,
        }
    
    try:
        shutil.rmtree(solution_dir)
        LOGGER.info("Cleaned up %s (%d files)", solution_dir, total)
        return {
            "status": "success",
            "message": f"Deleted {solution_dir} ({total} files)",
            "path": str(solution_dir),
            "total_files": total,
            "cs_files": cs_files,
            "feature_files": feature_files,
            "deleted": True,
        }
    except Exception as e:
        LOGGER.error("Failed to clean up %s: %s", solution_dir, e)
        return {
            "status": "error",
            "message": f"Failed to delete {solution_dir}: {e}",
            "path": str(solution_dir),
            "deleted": False,
        }


def run_batch_codegen(
    config_path: Path,
    batch_size: int = 500,
    start_batch: int = 0,
    max_batches: int | None = None,
    cleanup_first: bool = False,
    phase: DDDPhase = "all",
    progress_callback: Callable[[BatchProgress], None] | None = None,
) -> dict:
    """Run batch code generation for a large codebase.
    
    DDD-First Workflow:
      1. phase="domain"   - Build domain model, aggregates, ubiquitous language
      2. phase="contract" - Generate OpenAPI contract from domain model
      3. phase="code"     - Generate Clean Architecture code from contract
      4. phase="all"      - Run all phases sequentially (default)
    
    For large codebases, recommend running phases separately:
      - Run phase="domain" first, review domain model
      - Run phase="contract" to generate OpenAPI
      - Run phase="code" to generate implementation
    
    Args:
        config_path: Path to codegen config JSON
        batch_size: Number of slices per batch
        start_batch: Batch number to start from (for resumption)
        max_batches: Maximum number of batches to run (None = all)
        cleanup_first: Whether to clean up existing generated files first
        phase: DDD workflow phase to execute
        progress_callback: Optional callback for progress updates
        
    Returns:
        Dict with batch processing results
    """
    if not logging.getLogger().handlers:
        setup_logging("batch_codegen")
    
    # Load config
    config = load_config(config_path)
    run_id = resolve_run_id(config.output_root) if config.run_id == "auto" else config.run_id
    
    LOGGER.info("Starting batch code generation")
    LOGGER.info("  Config: %s", config_path)
    LOGGER.info("  Run ID: %s", run_id)
    LOGGER.info("  Solution: %s", config.solution_name)
    LOGGER.info("  Batch size: %d", batch_size)
    LOGGER.info("  Phase: %s", phase)
    
    # Map phase parameter to config.ddd_phase
    ddd_phase_map = {
        "domain": "domain",
        "gherkin": "gherkin",
        "contract": "contract",
        "code": "all",  # "code" means generate code after DDD
        "all": "all",
    }
    effective_phase = ddd_phase_map.get(phase, "all")
    
    # Get MCP client to query slices
    client = get_mcp_client(run_id=run_id, parquet_root=str(config.output_root))
    
    # Get all entry graphs
    sql = f"""
        SELECT entry_key, capped_depth
        FROM entry_graphs
        WHERE run_id = '{run_id}' AND artifact_version = {config.artifact_version}
        AND capped_depth >= 1
        ORDER BY capped_depth DESC, entry_key
    """
    try:
        entry_graphs = client.query(sql)
    except Exception as e:
        LOGGER.error("Failed to query entry graphs: %s", e)
        return {"status": "error", "message": f"Failed to query slices: {e}"}
    
    all_slice_ids = [e.get("entry_key") for e in entry_graphs if e.get("entry_key")]
    total_slices = len(all_slice_ids)
    total_batches = (total_slices + batch_size - 1) // batch_size
    
    LOGGER.info("Total slices: %d", total_slices)
    LOGGER.info("Total batches: %d", total_batches)
    
    # Initialize progress
    progress = BatchProgress(
        total_slices=total_slices,
        total_batches=total_batches,
        start_time=datetime.now(timezone.utc),
    )
    
    # Cleanup if requested
    if cleanup_first:
        cleanup_result = cleanup_generated(config.generated_root, config.solution_name, confirm=True)
        if cleanup_result["status"] == "error":
            return {"status": "error", "message": cleanup_result["message"]}
        LOGGER.info("Cleanup complete: %s", cleanup_result["message"])
    
    # Check DDD status for phased execution
    ddd_output = config.generated_root / config.solution_name / "ddd"
    ddd_status = _check_ddd_status(ddd_output, config.solution_name)
    
    # For code generation phase, verify DDD is complete
    if phase == "code" and not ddd_status["domain_complete"]:
        return {
            "status": "error",
            "message": "Cannot generate code: DDD domain model not found. Run with phase='domain' first.",
            "ddd_status": ddd_status,
            "next_step": "Run batch_codegen with phase='domain' to build domain model first.",
        }
    
    if phase == "code" and not ddd_status["contract_complete"]:
        return {
            "status": "error", 
            "message": "Cannot generate code: OpenAPI contract not found. Run with phase='contract' first.",
            "ddd_status": ddd_status,
            "next_step": "Run batch_codegen with phase='contract' to generate OpenAPI contract.",
        }
    
    LOGGER.info("DDD Status: %s", ddd_status)
    
    # Determine batch range
    end_batch = total_batches
    if max_batches is not None:
        end_batch = min(start_batch + max_batches, total_batches)
    
    LOGGER.info("Processing batches %d to %d", start_batch, end_batch - 1)
    
    # Process batches
    for batch_num in range(start_batch, end_batch):
        batch_start_idx = batch_num * batch_size
        batch_end_idx = min(batch_start_idx + batch_size, total_slices)
        batch_slice_ids = all_slice_ids[batch_start_idx:batch_end_idx]
        
        LOGGER.info("=== Batch %d: Processing slices %d to %d ===", 
                   batch_num + 1, batch_start_idx, batch_end_idx)
        
        try:
            # Create config for this batch with the specified DDD phase
            batch_config = config.model_copy(update={
                "run_id": run_id,
                "slice_ids": batch_slice_ids,
                "slice_offset": batch_start_idx,
                "max_slices": batch_size,
                "ddd_phase": effective_phase,
            })
            
            # Run DDD-first generation for this batch
            result = run_ddd_first(batch_config)
            
            progress.completed_batches += 1
            progress.completed_slices += len(batch_slice_ids)
            
            LOGGER.info("Batch %d complete: phase=%s, slices=%d", 
                       batch_num + 1, result.get("phase"), len(batch_slice_ids))
            
        except Exception as e:
            LOGGER.error("Batch %d failed: %s", batch_num + 1, e)
            progress.failed_batches.append(batch_num)
        
        # Update file counts
        total, cs_files, feature_files = _count_generated_files(
            config.generated_root / config.solution_name
        )
        progress.total_files_generated = total
        progress.total_cs_files = cs_files
        progress.total_feature_files = feature_files
        
        # Call progress callback if provided
        if progress_callback:
            progress_callback(progress)
        
        # Log progress
        if progress.completed_batches % 5 == 0:
            LOGGER.info(
                "Progress: %d/%d batches (%.1f%%), %d slices, ETA: %.0fs",
                progress.completed_batches,
                progress.total_batches,
                100 * progress.completed_batches / progress.total_batches,
                progress.completed_slices,
                progress.estimated_remaining_seconds,
            )
    
    progress.end_time = datetime.now(timezone.utc)
    
    # Final counts
    total, cs_files, feature_files = _count_generated_files(
        config.generated_root / config.solution_name
    )
    progress.total_files_generated = total
    progress.total_cs_files = cs_files
    progress.total_feature_files = feature_files
    
    LOGGER.info("=== Batch processing complete ===")
    LOGGER.info("  Completed: %d/%d batches", progress.completed_batches, progress.total_batches)
    LOGGER.info("  Failed: %d batches", len(progress.failed_batches))
    LOGGER.info("  Total files: %d (%d .cs, %d .feature)", total, cs_files, feature_files)
    LOGGER.info("  Elapsed: %.1f seconds", progress.elapsed_seconds)
    
    # Get final DDD status
    final_ddd_status = _check_ddd_status(
        config.generated_root / config.solution_name / "ddd",
        config.solution_name
    )
    
    # Determine next step based on phase
    next_step = None
    if phase == "domain":
        next_step = "Review domain model, then run with phase='contract' to generate OpenAPI"
    elif phase == "contract":
        next_step = "Review OpenAPI contract, then run with phase='code' to generate implementation"
    elif phase == "code" or phase == "all":
        next_step = "Build and test the generated solution"
    
    return {
        "status": "success" if not progress.failed_batches else "partial",
        "phase": phase,
        "progress": progress.to_dict(),
        "solution_path": str(config.generated_root / config.solution_name),
        "failed_batches": progress.failed_batches,
        "ddd_status": final_ddd_status,
        "next_step": next_step,
    }


def main() -> None:
    """CLI entry point for batch runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch code generation runner (DDD-First)")
    parser.add_argument("--config", type=Path, required=True, help="Path to codegen config JSON")
    parser.add_argument("--batch-size", type=int, default=500, help="Slices per batch")
    parser.add_argument("--start-batch", type=int, default=0, help="Batch to start from")
    parser.add_argument("--max-batches", type=int, help="Maximum batches to run")
    parser.add_argument("--cleanup", action="store_true", help="Clean existing output first")
    parser.add_argument(
        "--phase", 
        type=str, 
        default="all",
        choices=["domain", "gherkin", "contract", "code", "all"],
        help="DDD workflow phase: domain=build domain model, contract=generate OpenAPI, code=generate implementation, all=run all phases"
    )
    
    args = parser.parse_args()
    
    result = run_batch_codegen(
        config_path=args.config,
        batch_size=args.batch_size,
        start_batch=args.start_batch,
        max_batches=args.max_batches,
        cleanup_first=args.cleanup,
        phase=args.phase,
    )
    
    import json
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
