"""
Pipeline State Manager - Parquet-based state management for all pipeline operations.

This module provides persistent state management for:
1. Pipeline Steps - track each step (ingest, parse, slice, ddd, codegen, validate)
2. Code Generation Jobs - track codegen phase progress
3. Validation Runs - track validation scores and fixes
4. Approval Workflows - persist approval decisions across sessions

State Tables:
- pipeline_step_state: Per-step progress tracking (ingest, parse, slice, ddd, etc.)
- codegen_job_state: Code generation job metadata and progress
- codegen_slice_state: Per-slice code generation status
- validation_run_state: Validation run results and scores
- validation_fix_state: Pending and applied validation fixes
- approval_state: Step approval decisions and history
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from enum import Enum

import pyarrow as pa
import pyarrow.parquet as pq

LOGGER = logging.getLogger("migration_agents.codegen.pipeline_state_manager")


# ============================================================================
# Enums
# ============================================================================

class PipelineStep(str, Enum):
    """Pipeline step names."""
    INGEST = "ingest"
    PARSE = "parse"
    SLICE = "slice"
    DDD_ANALYSIS = "ddd_analysis"
    DDD_MODEL = "ddd_model"
    CODEGEN_DOMAIN = "codegen_domain"
    CODEGEN_CONTRACT = "codegen_contract"
    CODEGEN_CODE = "codegen_code"
    VALIDATE = "validate"
    APPROVE = "approve"


class PipelineStepStatus(str, Enum):
    """Pipeline step status."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class CodegenPhase(str, Enum):
    """Code generation phase."""
    DOMAIN = "domain"
    CONTRACT = "contract"
    CODE = "code"
    ALL = "all"


class CodegenJobStatus(str, Enum):
    """Code generation job status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class CodegenSliceStatus(str, Enum):
    """Per-slice code generation status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    GENERATED = "generated"
    SKIPPED = "skipped"
    FAILED = "failed"


class ValidationStatus(str, Enum):
    """Validation run status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class FixStatus(str, Enum):
    """Validation fix status."""
    PENDING = "pending"
    APPLIED = "applied"
    REJECTED = "rejected"
    SKIPPED = "skipped"


class ApprovalStatus(str, Enum):
    """Step approval status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


# ============================================================================
# Parquet Schemas
# ============================================================================

CODEGEN_JOB_SCHEMA = pa.schema([
    pa.field("job_id", pa.string()),
    pa.field("solution_name", pa.string()),
    pa.field("run_id", pa.string()),
    pa.field("phase", pa.string()),
    pa.field("status", pa.string()),
    pa.field("total_slices", pa.int64()),
    pa.field("generated_slices", pa.int64()),
    pa.field("failed_slices", pa.int64()),
    pa.field("skipped_slices", pa.int64()),
    pa.field("current_batch", pa.int64()),
    pa.field("total_batches", pa.int64()),
    pa.field("batch_size", pa.int64()),
    pa.field("created_at", pa.string()),
    pa.field("updated_at", pa.string()),
    pa.field("started_at", pa.string()),
    pa.field("completed_at", pa.string()),
    pa.field("error_message", pa.string()),
    pa.field("config_json", pa.string()),
])

CODEGEN_SLICE_SCHEMA = pa.schema([
    pa.field("slice_id", pa.string()),
    pa.field("job_id", pa.string()),
    pa.field("status", pa.string()),
    pa.field("phase", pa.string()),
    pa.field("generated_files_json", pa.string()),
    pa.field("error_message", pa.string()),
    pa.field("started_at", pa.string()),
    pa.field("completed_at", pa.string()),
    pa.field("retry_count", pa.int64()),
])

VALIDATION_RUN_SCHEMA = pa.schema([
    pa.field("run_id", pa.string()),
    pa.field("project_path", pa.string()),
    pa.field("solution_name", pa.string()),
    pa.field("status", pa.string()),
    pa.field("overall_score", pa.float64()),
    pa.field("domain_score", pa.float64()),
    pa.field("application_score", pa.float64()),
    pa.field("api_score", pa.float64()),
    pa.field("infrastructure_score", pa.float64()),
    pa.field("total_issues", pa.int64()),
    pa.field("critical_issues", pa.int64()),
    pa.field("rubric_results_json", pa.string()),
    pa.field("created_at", pa.string()),
    pa.field("completed_at", pa.string()),
])

VALIDATION_FIX_SCHEMA = pa.schema([
    pa.field("fix_id", pa.string()),
    pa.field("validation_run_id", pa.string()),
    pa.field("status", pa.string()),
    pa.field("category", pa.string()),
    pa.field("severity", pa.string()),
    pa.field("file_path", pa.string()),
    pa.field("description", pa.string()),
    pa.field("suggested_fix", pa.string()),
    pa.field("applied_at", pa.string()),
    pa.field("applied_by", pa.string()),
])

APPROVAL_STATE_SCHEMA = pa.schema([
    pa.field("step_id", pa.string()),
    pa.field("solution_name", pa.string()),
    pa.field("step_name", pa.string()),
    pa.field("step_type", pa.string()),
    pa.field("status", pa.string()),
    pa.field("reviewer", pa.string()),
    pa.field("decision", pa.string()),
    pa.field("comments", pa.string()),
    pa.field("artifacts_json", pa.string()),
    pa.field("created_at", pa.string()),
    pa.field("reviewed_at", pa.string()),
])

PIPELINE_STEP_SCHEMA = pa.schema([
    pa.field("step_id", pa.string()),
    pa.field("run_id", pa.string()),
    pa.field("solution_name", pa.string()),
    pa.field("step_name", pa.string()),
    pa.field("status", pa.string()),
    pa.field("processed_count", pa.int64()),
    pa.field("skipped_count", pa.int64()),
    pa.field("error_count", pa.int64()),
    pa.field("total_count", pa.int64()),
    pa.field("outputs_json", pa.string()),
    pa.field("config_json", pa.string()),
    pa.field("error_message", pa.string()),
    pa.field("created_at", pa.string()),
    pa.field("started_at", pa.string()),
    pa.field("completed_at", pa.string()),
])


# ============================================================================
# Helper Functions
# ============================================================================

def _now_iso() -> str:
    """Return current UTC time as ISO string."""
    return datetime.now(timezone.utc).isoformat()


def _generate_id(prefix: str, name: str) -> str:
    """Generate a unique ID with timestamp."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{name}_{timestamp}"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class PipelineStepState:
    """Represents the state of a pipeline step (ingest, parse, slice, etc.)."""
    step_id: str
    run_id: str
    solution_name: str
    step_name: str
    status: PipelineStepStatus = PipelineStepStatus.NOT_STARTED
    processed_count: int = 0
    skipped_count: int = 0
    error_count: int = 0
    total_count: int = 0
    outputs_json: str = "{}"
    config_json: str = "{}"
    error_message: str = ""
    created_at: str = field(default_factory=_now_iso)
    started_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, PipelineStepStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "PipelineStepState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = PipelineStepStatus(d["status"])
        return cls(**d)


@dataclass
class CodegenJobState:
    """Represents the state of a code generation job."""
    job_id: str
    solution_name: str
    run_id: str
    phase: CodegenPhase = CodegenPhase.ALL
    status: CodegenJobStatus = CodegenJobStatus.PENDING
    total_slices: int = 0
    generated_slices: int = 0
    failed_slices: int = 0
    skipped_slices: int = 0
    current_batch: int = 0
    total_batches: int = 0
    batch_size: int = 500
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    started_at: str = ""
    completed_at: str = ""
    error_message: str = ""
    config_json: str = "{}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["phase"] = self.phase.value if isinstance(self.phase, CodegenPhase) else self.phase
        d["status"] = self.status.value if isinstance(self.status, CodegenJobStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "CodegenJobState":
        d = d.copy()
        if "phase" in d and isinstance(d["phase"], str):
            d["phase"] = CodegenPhase(d["phase"])
        if "status" in d and isinstance(d["status"], str):
            d["status"] = CodegenJobStatus(d["status"])
        return cls(**d)


@dataclass
class CodegenSliceState:
    """Represents the state of a single slice's code generation."""
    slice_id: str
    job_id: str
    status: CodegenSliceStatus = CodegenSliceStatus.PENDING
    phase: str = ""
    generated_files_json: str = "[]"
    error_message: str = ""
    started_at: str = ""
    completed_at: str = ""
    retry_count: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, CodegenSliceStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "CodegenSliceState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = CodegenSliceStatus(d["status"])
        return cls(**d)


@dataclass
class ValidationRunState:
    """Represents a validation run."""
    run_id: str
    project_path: str
    solution_name: str
    status: ValidationStatus = ValidationStatus.PENDING
    overall_score: float = 0.0
    domain_score: float = 0.0
    application_score: float = 0.0
    api_score: float = 0.0
    infrastructure_score: float = 0.0
    total_issues: int = 0
    critical_issues: int = 0
    rubric_results_json: str = "{}"
    created_at: str = field(default_factory=_now_iso)
    completed_at: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, ValidationStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ValidationRunState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = ValidationStatus(d["status"])
        return cls(**d)


@dataclass
class ValidationFixState:
    """Represents a validation fix."""
    fix_id: str
    validation_run_id: str
    status: FixStatus = FixStatus.PENDING
    category: str = ""
    severity: str = ""
    file_path: str = ""
    description: str = ""
    suggested_fix: str = ""
    applied_at: str = ""
    applied_by: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, FixStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ValidationFixState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = FixStatus(d["status"])
        return cls(**d)


@dataclass
class ApprovalState:
    """Represents an approval decision."""
    step_id: str
    solution_name: str
    step_name: str
    step_type: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewer: str = ""
    decision: str = ""
    comments: str = ""
    artifacts_json: str = "{}"
    created_at: str = field(default_factory=_now_iso)
    reviewed_at: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, ApprovalStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ApprovalState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = ApprovalStatus(d["status"])
        return cls(**d)


# ============================================================================
# Pipeline State Manager
# ============================================================================

class PipelineStateManager:
    """
    Manages persistent state for pipeline operations using Parquet files.
    
    Provides state tracking for:
    - Pipeline steps (ingest, parse, slice, ddd, codegen, validate)
    - Code generation jobs
    - Validation runs
    - Approval workflows
    """

    def __init__(self, parquet_root: Path, run_id: Optional[str] = None):
        self.parquet_root = Path(parquet_root)
        self.run_id = run_id
        self.state_dir = self.parquet_root / "pipeline_state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # State file paths
        self.pipeline_step_file = self.state_dir / "pipeline_step_state.parquet"
        self.codegen_job_file = self.state_dir / "codegen_job_state.parquet"
        self.codegen_slice_file = self.state_dir / "codegen_slice_state.parquet"
        self.validation_run_file = self.state_dir / "validation_run_state.parquet"
        self.validation_fix_file = self.state_dir / "validation_fix_state.parquet"
        self.approval_file = self.state_dir / "approval_state.parquet"

    # ========================================================================
    # Pipeline Step State (ingest, parse, slice, ddd, codegen, validate)
    # ========================================================================

    def start_pipeline_step(
        self,
        step_name: str,
        solution_name: str = "",
        total_count: int = 0,
        config: Optional[dict] = None,
    ) -> PipelineStepState:
        """Start tracking a pipeline step."""
        step = PipelineStepState(
            step_id=_generate_id("step", step_name),
            run_id=self.run_id or "",
            solution_name=solution_name,
            step_name=step_name,
            status=PipelineStepStatus.RUNNING,
            total_count=total_count,
            config_json=json.dumps(config or {}),
            started_at=_now_iso(),
        )
        self._save_pipeline_step(step)
        LOGGER.info(f"Started pipeline step {step.step_id} ({step_name})")
        return step

    def update_pipeline_step_progress(
        self,
        step_id: str,
        processed_count: Optional[int] = None,
        skipped_count: Optional[int] = None,
        error_count: Optional[int] = None,
        outputs: Optional[dict] = None,
    ) -> None:
        """Update progress counters for a pipeline step."""
        steps = self._load_pipeline_steps()
        for step in steps:
            if step.step_id == step_id:
                if processed_count is not None:
                    step.processed_count = processed_count
                if skipped_count is not None:
                    step.skipped_count = skipped_count
                if error_count is not None:
                    step.error_count = error_count
                if outputs is not None:
                    step.outputs_json = json.dumps(outputs)
                break
        self._save_all_pipeline_steps(steps)

    def complete_pipeline_step(
        self,
        step_id: str,
        processed_count: int = 0,
        skipped_count: int = 0,
        error_count: int = 0,
        outputs: Optional[dict] = None,
    ) -> None:
        """Mark a pipeline step as completed."""
        steps = self._load_pipeline_steps()
        for step in steps:
            if step.step_id == step_id:
                step.status = PipelineStepStatus.COMPLETED
                step.processed_count = processed_count
                step.skipped_count = skipped_count
                step.error_count = error_count
                if outputs:
                    step.outputs_json = json.dumps(outputs)
                step.completed_at = _now_iso()
                break
        self._save_all_pipeline_steps(steps)
        LOGGER.info(f"Completed pipeline step {step_id}")

    def fail_pipeline_step(self, step_id: str, error_message: str) -> None:
        """Mark a pipeline step as failed."""
        steps = self._load_pipeline_steps()
        for step in steps:
            if step.step_id == step_id:
                step.status = PipelineStepStatus.FAILED
                step.error_message = error_message
                step.completed_at = _now_iso()
                break
        self._save_all_pipeline_steps(steps)
        LOGGER.error(f"Failed pipeline step {step_id}: {error_message}")

    def get_pipeline_step(self, step_id: str) -> Optional[PipelineStepState]:
        """Get a pipeline step by ID."""
        steps = self._load_pipeline_steps()
        for step in steps:
            if step.step_id == step_id:
                return step
        return None

    def get_latest_pipeline_step(self, step_name: str, run_id: Optional[str] = None) -> Optional[PipelineStepState]:
        """Get the most recent step of a given type."""
        steps = self._load_pipeline_steps()
        matching = [s for s in steps if s.step_name == step_name]
        if run_id:
            matching = [s for s in matching if s.run_id == run_id]
        if not matching:
            return None
        return max(matching, key=lambda s: s.created_at)

    def get_pipeline_status(self, run_id: Optional[str] = None) -> dict[str, Any]:
        """Get overall pipeline status showing all steps."""
        steps = self._load_pipeline_steps()
        if run_id:
            steps = [s for s in steps if s.run_id == run_id]
        
        # Get latest status for each step type
        step_status = {}
        for step_name in [s.value for s in PipelineStep]:
            matching = [s for s in steps if s.step_name == step_name]
            if matching:
                latest = max(matching, key=lambda s: s.created_at)
                step_status[step_name] = {
                    "step_id": latest.step_id,
                    "status": latest.status.value if isinstance(latest.status, PipelineStepStatus) else latest.status,
                    "processed": latest.processed_count,
                    "errors": latest.error_count,
                    "started_at": latest.started_at,
                    "completed_at": latest.completed_at,
                }
            else:
                step_status[step_name] = {"status": "not_started"}
        
        return {
            "status": "ok",
            "run_id": run_id or self.run_id,
            "steps": step_status,
        }

    def get_resumable_step(self, step_name: str) -> Optional[PipelineStepState]:
        """Get a step that can be resumed (running or paused)."""
        steps = self._load_pipeline_steps()
        for step in sorted(steps, key=lambda s: s.created_at, reverse=True):
            if (step.step_name == step_name and 
                step.status in (PipelineStepStatus.RUNNING, PipelineStepStatus.PAUSED)):
                return step
        return None

    def _save_pipeline_step(self, step: PipelineStepState) -> None:
        """Save a single pipeline step."""
        steps = self._load_pipeline_steps()
        found = False
        for i, s in enumerate(steps):
            if s.step_id == step.step_id:
                steps[i] = step
                found = True
                break
        if not found:
            steps.append(step)
        self._save_all_pipeline_steps(steps)

    def _load_pipeline_steps(self) -> list[PipelineStepState]:
        """Load all pipeline steps from parquet."""
        if not self.pipeline_step_file.exists():
            return []
        try:
            table = pq.read_table(self.pipeline_step_file)
            return [PipelineStepState.from_dict(row) for row in table.to_pylist()]
        except Exception as e:
            LOGGER.warning(f"Failed to load pipeline steps: {e}")
            return []

    def _save_all_pipeline_steps(self, steps: list[PipelineStepState]) -> None:
        """Save all pipeline steps to parquet."""
        if not steps:
            return
        records = [s.to_dict() for s in steps]
        table = pa.Table.from_pylist(records, schema=PIPELINE_STEP_SCHEMA)
        pq.write_table(table, self.pipeline_step_file)

    # ========================================================================
    # Code Generation State
    # ========================================================================

    def create_codegen_job(
        self,
        solution_name: str,
        phase: CodegenPhase,
        total_slices: int,
        batch_size: int = 500,
        config: Optional[dict] = None,
    ) -> CodegenJobState:
        """Create a new code generation job."""
        job = CodegenJobState(
            job_id=_generate_id("codegen", solution_name),
            solution_name=solution_name,
            run_id=self.run_id or "",
            phase=phase,
            total_slices=total_slices,
            batch_size=batch_size,
            total_batches=(total_slices + batch_size - 1) // batch_size,
            config_json=json.dumps(config or {}),
        )
        self._save_codegen_job(job)
        LOGGER.info(f"Created codegen job {job.job_id} for {solution_name} ({phase.value} phase)")
        return job

    def get_codegen_job(self, job_id: str) -> Optional[CodegenJobState]:
        """Get a code generation job by ID."""
        jobs = self._load_codegen_jobs()
        for job in jobs:
            if job.job_id == job_id:
                return job
        return None

    def get_latest_codegen_job(self, solution_name: str) -> Optional[CodegenJobState]:
        """Get the most recent codegen job for a solution."""
        jobs = self._load_codegen_jobs()
        solution_jobs = [j for j in jobs if j.solution_name == solution_name]
        if not solution_jobs:
            return None
        return max(solution_jobs, key=lambda j: j.created_at)

    def get_resumable_codegen_job(self, solution_name: str, phase: CodegenPhase) -> Optional[CodegenJobState]:
        """Get a job that can be resumed (running or paused)."""
        jobs = self._load_codegen_jobs()
        for job in sorted(jobs, key=lambda j: j.created_at, reverse=True):
            if (job.solution_name == solution_name and 
                job.phase == phase and
                job.status in (CodegenJobStatus.RUNNING, CodegenJobStatus.PAUSED)):
                return job
        return None

    def update_codegen_job_status(self, job_id: str, status: CodegenJobStatus) -> None:
        """Update job status."""
        jobs = self._load_codegen_jobs()
        for job in jobs:
            if job.job_id == job_id:
                job.status = status
                job.updated_at = _now_iso()
                if status == CodegenJobStatus.RUNNING and not job.started_at:
                    job.started_at = _now_iso()
                elif status == CodegenJobStatus.COMPLETED:
                    job.completed_at = _now_iso()
                break
        self._save_all_codegen_jobs(jobs)

    def update_codegen_job_progress(
        self,
        job_id: str,
        generated_slices: Optional[int] = None,
        failed_slices: Optional[int] = None,
        current_batch: Optional[int] = None,
    ) -> None:
        """Update job progress counters."""
        jobs = self._load_codegen_jobs()
        for job in jobs:
            if job.job_id == job_id:
                if generated_slices is not None:
                    job.generated_slices = generated_slices
                if failed_slices is not None:
                    job.failed_slices = failed_slices
                if current_batch is not None:
                    job.current_batch = current_batch
                job.updated_at = _now_iso()
                break
        self._save_all_codegen_jobs(jobs)

    def register_codegen_slices(self, job_id: str, slice_ids: list[str]) -> None:
        """Register slices for code generation."""
        slices = self._load_codegen_slices()
        for slice_id in slice_ids:
            # Check if already registered
            existing = next((s for s in slices if s.slice_id == slice_id and s.job_id == job_id), None)
            if not existing:
                slices.append(CodegenSliceState(slice_id=slice_id, job_id=job_id))
        self._save_all_codegen_slices(slices)

    def save_codegen_slice_result(
        self,
        slice_id: str,
        job_id: str,
        status: CodegenSliceStatus,
        generated_files: Optional[list[str]] = None,
        error_message: str = "",
    ) -> None:
        """Save the result of code generation for a slice."""
        slices = self._load_codegen_slices()
        found = False
        for s in slices:
            if s.slice_id == slice_id and s.job_id == job_id:
                s.status = status
                s.generated_files_json = json.dumps(generated_files or [])
                s.error_message = error_message
                s.completed_at = _now_iso()
                found = True
                break
        
        if not found:
            slices.append(CodegenSliceState(
                slice_id=slice_id,
                job_id=job_id,
                status=status,
                generated_files_json=json.dumps(generated_files or []),
                error_message=error_message,
                completed_at=_now_iso(),
            ))
        
        self._save_all_codegen_slices(slices)

    def get_pending_codegen_slices(self, job_id: str, limit: int = 100) -> list[CodegenSliceState]:
        """Get pending slices for code generation."""
        slices = self._load_codegen_slices()
        pending = [s for s in slices if s.job_id == job_id and s.status == CodegenSliceStatus.PENDING]
        return pending[:limit]

    def get_codegen_job_progress(self, job_id: str) -> dict[str, Any]:
        """Get comprehensive progress for a codegen job."""
        job = self.get_codegen_job(job_id)
        if not job:
            return {"status": "error", "message": f"Job {job_id} not found"}
        
        slices = self._load_codegen_slices()
        job_slices = [s for s in slices if s.job_id == job_id]
        
        status_counts = {}
        for s in job_slices:
            status = s.status.value if isinstance(s.status, CodegenSliceStatus) else s.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "status": "ok",
            "job_id": job_id,
            "solution_name": job.solution_name,
            "phase": job.phase.value if isinstance(job.phase, CodegenPhase) else job.phase,
            "job_status": job.status.value if isinstance(job.status, CodegenJobStatus) else job.status,
            "progress": {
                "total_slices": job.total_slices,
                "generated": job.generated_slices,
                "failed": job.failed_slices,
                "pending": status_counts.get("pending", 0),
                "percentage": round(job.generated_slices / job.total_slices * 100, 2) if job.total_slices > 0 else 0,
            },
            "batches": {
                "current": job.current_batch,
                "total": job.total_batches,
            },
            "timestamps": {
                "created_at": job.created_at,
                "started_at": job.started_at,
                "updated_at": job.updated_at,
            },
        }

    def _save_codegen_job(self, job: CodegenJobState) -> None:
        """Save a single codegen job (append or update)."""
        jobs = self._load_codegen_jobs()
        found = False
        for i, j in enumerate(jobs):
            if j.job_id == job.job_id:
                jobs[i] = job
                found = True
                break
        if not found:
            jobs.append(job)
        self._save_all_codegen_jobs(jobs)

    def _load_codegen_jobs(self) -> list[CodegenJobState]:
        """Load all codegen jobs from parquet."""
        if not self.codegen_job_file.exists():
            return []
        try:
            table = pq.read_table(self.codegen_job_file)
            return [CodegenJobState.from_dict(row) for row in table.to_pylist()]
        except Exception as e:
            LOGGER.warning(f"Failed to load codegen jobs: {e}")
            return []

    def _save_all_codegen_jobs(self, jobs: list[CodegenJobState]) -> None:
        """Save all codegen jobs to parquet."""
        if not jobs:
            return
        records = [j.to_dict() for j in jobs]
        table = pa.Table.from_pylist(records, schema=CODEGEN_JOB_SCHEMA)
        pq.write_table(table, self.codegen_job_file)

    def _load_codegen_slices(self) -> list[CodegenSliceState]:
        """Load all codegen slices from parquet."""
        if not self.codegen_slice_file.exists():
            return []
        try:
            table = pq.read_table(self.codegen_slice_file)
            return [CodegenSliceState.from_dict(row) for row in table.to_pylist()]
        except Exception as e:
            LOGGER.warning(f"Failed to load codegen slices: {e}")
            return []

    def _save_all_codegen_slices(self, slices: list[CodegenSliceState]) -> None:
        """Save all codegen slices to parquet."""
        if not slices:
            return
        records = [s.to_dict() for s in slices]
        table = pa.Table.from_pylist(records, schema=CODEGEN_SLICE_SCHEMA)
        pq.write_table(table, self.codegen_slice_file)

    # ========================================================================
    # Validation State
    # ========================================================================

    def create_validation_run(
        self,
        project_path: str,
        solution_name: str,
    ) -> ValidationRunState:
        """Create a new validation run."""
        run = ValidationRunState(
            run_id=_generate_id("validation", solution_name),
            project_path=project_path,
            solution_name=solution_name,
        )
        self._save_validation_run(run)
        LOGGER.info(f"Created validation run {run.run_id} for {solution_name}")
        return run

    def get_validation_run(self, run_id: str) -> Optional[ValidationRunState]:
        """Get a validation run by ID."""
        runs = self._load_validation_runs()
        for run in runs:
            if run.run_id == run_id:
                return run
        return None

    def get_latest_validation_run(self, solution_name: str) -> Optional[ValidationRunState]:
        """Get the most recent validation run for a solution."""
        runs = self._load_validation_runs()
        solution_runs = [r for r in runs if r.solution_name == solution_name]
        if not solution_runs:
            return None
        return max(solution_runs, key=lambda r: r.created_at)

    def save_validation_results(
        self,
        run_id: str,
        scores: dict[str, float],
        rubric_results: dict[str, Any],
        total_issues: int = 0,
        critical_issues: int = 0,
    ) -> None:
        """Save validation results."""
        runs = self._load_validation_runs()
        for run in runs:
            if run.run_id == run_id:
                run.status = ValidationStatus.COMPLETED
                run.overall_score = scores.get("overall", 0.0)
                run.domain_score = scores.get("domain", 0.0)
                run.application_score = scores.get("application", 0.0)
                run.api_score = scores.get("api", 0.0)
                run.infrastructure_score = scores.get("infrastructure", 0.0)
                run.total_issues = total_issues
                run.critical_issues = critical_issues
                run.rubric_results_json = json.dumps(rubric_results)
                run.completed_at = _now_iso()
                break
        self._save_all_validation_runs(runs)

    def register_validation_fixes(self, run_id: str, fixes: list[dict[str, Any]]) -> list[ValidationFixState]:
        """Register validation fixes for a run."""
        all_fixes = self._load_validation_fixes()
        new_fixes = []
        for i, fix_data in enumerate(fixes):
            fix = ValidationFixState(
                fix_id=f"{run_id}_fix_{i:04d}",
                validation_run_id=run_id,
                category=fix_data.get("category", ""),
                severity=fix_data.get("severity", ""),
                file_path=fix_data.get("file_path", ""),
                description=fix_data.get("description", ""),
                suggested_fix=fix_data.get("suggested_fix", ""),
            )
            all_fixes.append(fix)
            new_fixes.append(fix)
        self._save_all_validation_fixes(all_fixes)
        return new_fixes

    def get_pending_fixes(self, run_id: str) -> list[ValidationFixState]:
        """Get pending fixes for a validation run."""
        fixes = self._load_validation_fixes()
        return [f for f in fixes if f.validation_run_id == run_id and f.status == FixStatus.PENDING]

    def apply_fix(self, fix_id: str, applied_by: str) -> Optional[ValidationFixState]:
        """Mark a fix as applied."""
        fixes = self._load_validation_fixes()
        for fix in fixes:
            if fix.fix_id == fix_id:
                fix.status = FixStatus.APPLIED
                fix.applied_at = _now_iso()
                fix.applied_by = applied_by
                self._save_all_validation_fixes(fixes)
                return fix
        return None

    def get_validation_history(self, solution_name: str, limit: int = 10) -> list[dict[str, Any]]:
        """Get validation history for a solution."""
        runs = self._load_validation_runs()
        solution_runs = sorted(
            [r for r in runs if r.solution_name == solution_name],
            key=lambda r: r.created_at,
            reverse=True
        )[:limit]
        
        return [
            {
                "run_id": r.run_id,
                "status": r.status.value if isinstance(r.status, ValidationStatus) else r.status,
                "overall_score": r.overall_score,
                "scores": {
                    "domain": r.domain_score,
                    "application": r.application_score,
                    "api": r.api_score,
                    "infrastructure": r.infrastructure_score,
                },
                "issues": {"total": r.total_issues, "critical": r.critical_issues},
                "created_at": r.created_at,
                "completed_at": r.completed_at,
            }
            for r in solution_runs
        ]

    def _save_validation_run(self, run: ValidationRunState) -> None:
        """Save a single validation run."""
        runs = self._load_validation_runs()
        found = False
        for i, r in enumerate(runs):
            if r.run_id == run.run_id:
                runs[i] = run
                found = True
                break
        if not found:
            runs.append(run)
        self._save_all_validation_runs(runs)

    def _load_validation_runs(self) -> list[ValidationRunState]:
        """Load all validation runs from parquet."""
        if not self.validation_run_file.exists():
            return []
        try:
            table = pq.read_table(self.validation_run_file)
            return [ValidationRunState.from_dict(row) for row in table.to_pylist()]
        except Exception as e:
            LOGGER.warning(f"Failed to load validation runs: {e}")
            return []

    def _save_all_validation_runs(self, runs: list[ValidationRunState]) -> None:
        """Save all validation runs to parquet."""
        if not runs:
            return
        records = [r.to_dict() for r in runs]
        table = pa.Table.from_pylist(records, schema=VALIDATION_RUN_SCHEMA)
        pq.write_table(table, self.validation_run_file)

    def _load_validation_fixes(self) -> list[ValidationFixState]:
        """Load all validation fixes from parquet."""
        if not self.validation_fix_file.exists():
            return []
        try:
            table = pq.read_table(self.validation_fix_file)
            return [ValidationFixState.from_dict(row) for row in table.to_pylist()]
        except Exception as e:
            LOGGER.warning(f"Failed to load validation fixes: {e}")
            return []

    def _save_all_validation_fixes(self, fixes: list[ValidationFixState]) -> None:
        """Save all validation fixes to parquet."""
        if not fixes:
            return
        records = [f.to_dict() for f in fixes]
        table = pa.Table.from_pylist(records, schema=VALIDATION_FIX_SCHEMA)
        pq.write_table(table, self.validation_fix_file)

    # ========================================================================
    # Approval State
    # ========================================================================

    def create_approval_step(
        self,
        solution_name: str,
        step_name: str,
        step_type: str,
        artifacts: Optional[dict[str, Any]] = None,
    ) -> ApprovalState:
        """Create a new approval step."""
        step = ApprovalState(
            step_id=_generate_id("approval", f"{solution_name}_{step_name}"),
            solution_name=solution_name,
            step_name=step_name,
            step_type=step_type,
            artifacts_json=json.dumps(artifacts or {}),
        )
        self._save_approval(step)
        LOGGER.info(f"Created approval step {step.step_id} for {solution_name}/{step_name}")
        return step

    def get_approval_step(self, step_id: str) -> Optional[ApprovalState]:
        """Get an approval step by ID."""
        approvals = self._load_approvals()
        for a in approvals:
            if a.step_id == step_id:
                return a
        return None

    def get_pending_approvals(self, solution_name: str) -> list[ApprovalState]:
        """Get all pending approvals for a solution."""
        approvals = self._load_approvals()
        return [a for a in approvals if a.solution_name == solution_name and a.status == ApprovalStatus.PENDING]

    def get_approval_by_step(self, solution_name: str, step_name: str) -> Optional[ApprovalState]:
        """Get approval state for a specific step."""
        approvals = self._load_approvals()
        for a in sorted(approvals, key=lambda x: x.created_at, reverse=True):
            if a.solution_name == solution_name and a.step_name == step_name:
                return a
        return None

    def submit_approval(
        self,
        step_id: str,
        decision: ApprovalStatus,
        reviewer: str,
        comments: str = "",
    ) -> Optional[ApprovalState]:
        """Submit an approval decision."""
        approvals = self._load_approvals()
        for a in approvals:
            if a.step_id == step_id:
                a.status = decision
                a.reviewer = reviewer
                a.decision = decision.value
                a.comments = comments
                a.reviewed_at = _now_iso()
                self._save_all_approvals(approvals)
                LOGGER.info(f"Approval {step_id} submitted: {decision.value} by {reviewer}")
                return a
        return None

    def get_approval_status(self, solution_name: str) -> dict[str, Any]:
        """Get approval status summary for a solution."""
        approvals = self._load_approvals()
        solution_approvals = [a for a in approvals if a.solution_name == solution_name]
        
        status_counts = {}
        for a in solution_approvals:
            status = a.status.value if isinstance(a.status, ApprovalStatus) else a.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        steps = []
        for a in sorted(solution_approvals, key=lambda x: x.created_at):
            steps.append({
                "step_id": a.step_id,
                "step_name": a.step_name,
                "step_type": a.step_type,
                "status": a.status.value if isinstance(a.status, ApprovalStatus) else a.status,
                "reviewer": a.reviewer,
                "reviewed_at": a.reviewed_at,
            })
        
        return {
            "status": "ok",
            "solution_name": solution_name,
            "total_steps": len(solution_approvals),
            "status_counts": status_counts,
            "steps": steps,
        }

    def _save_approval(self, approval: ApprovalState) -> None:
        """Save a single approval."""
        approvals = self._load_approvals()
        found = False
        for i, a in enumerate(approvals):
            if a.step_id == approval.step_id:
                approvals[i] = approval
                found = True
                break
        if not found:
            approvals.append(approval)
        self._save_all_approvals(approvals)

    def _load_approvals(self) -> list[ApprovalState]:
        """Load all approvals from parquet."""
        if not self.approval_file.exists():
            return []
        try:
            table = pq.read_table(self.approval_file)
            return [ApprovalState.from_dict(row) for row in table.to_pylist()]
        except Exception as e:
            LOGGER.warning(f"Failed to load approvals: {e}")
            return []

    def _save_all_approvals(self, approvals: list[ApprovalState]) -> None:
        """Save all approvals to parquet."""
        if not approvals:
            return
        records = [a.to_dict() for a in approvals]
        table = pa.Table.from_pylist(records, schema=APPROVAL_STATE_SCHEMA)
        pq.write_table(table, self.approval_file)


# ============================================================================
# Module-level Singleton
# ============================================================================

_pipeline_state_manager: Optional[PipelineStateManager] = None


def get_pipeline_state_manager(parquet_root: Path, run_id: Optional[str] = None) -> PipelineStateManager:
    """Get or create the pipeline state manager singleton."""
    global _pipeline_state_manager
    if _pipeline_state_manager is None:
        _pipeline_state_manager = PipelineStateManager(parquet_root, run_id)
    return _pipeline_state_manager


def reset_pipeline_state_manager() -> None:
    """Reset the singleton (for testing)."""
    global _pipeline_state_manager
    _pipeline_state_manager = None
