"""
DDD State Manager - Parquet-based state management for DDD analysis pipeline.

This module provides persistent state management using Parquet files to enable:
1. Resumable batch processing - pick up exactly where left off
2. Progress tracking - query progress via MCP or CLI
3. Checkpointing - automatic saves after each slice analysis
4. No data loss - survives chat restarts, crashes, or interruptions

State Tables:
- ddd_job_state: Overall job/run metadata and progress
- ddd_batch_state: Per-batch progress tracking
- ddd_slice_analysis: Individual slice analysis results
- ddd_domain_model: Synthesized domain model artifacts
"""

from __future__ import annotations

import hashlib
import logging
import os
from migration_agents.constants import DEFAULT_PARQUET_ROOT
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Literal
from enum import Enum

import pyarrow as pa
import pyarrow.parquet as pq

LOGGER = logging.getLogger("migration_agents.codegen.ddd_state_manager")


class JobStatus(str, Enum):
    """Overall job status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class SliceStatus(str, Enum):
    """Individual slice analysis status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    ANALYZED = "analyzed"
    SKIPPED = "skipped"
    FAILED = "failed"


class BatchStatus(str, Enum):
    """Batch processing status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# Parquet Schemas
JOB_STATE_SCHEMA = pa.schema([
    pa.field("job_id", pa.string()),
    pa.field("solution_name", pa.string()),
    pa.field("run_id", pa.string()),
    pa.field("status", pa.string()),
    pa.field("total_slices", pa.int64()),
    pa.field("analyzed_slices", pa.int64()),
    pa.field("failed_slices", pa.int64()),
    pa.field("skipped_slices", pa.int64()),
    pa.field("total_batches", pa.int64()),
    pa.field("completed_batches", pa.int64()),
    pa.field("current_batch", pa.int64()),
    pa.field("batch_size", pa.int64()),
    pa.field("min_depth", pa.int64()),
    pa.field("max_depth", pa.int64()),
    pa.field("llm_provider", pa.string()),
    pa.field("llm_model", pa.string()),
    pa.field("created_at", pa.string()),
    pa.field("updated_at", pa.string()),
    pa.field("started_at", pa.string()),
    pa.field("completed_at", pa.string()),
    pa.field("error_message", pa.string()),
    pa.field("config_json", pa.string()),
])

BATCH_STATE_SCHEMA = pa.schema([
    pa.field("batch_id", pa.string()),
    pa.field("job_id", pa.string()),
    pa.field("batch_number", pa.int64()),
    pa.field("status", pa.string()),
    pa.field("slice_count", pa.int64()),
    pa.field("analyzed_count", pa.int64()),
    pa.field("failed_count", pa.int64()),
    pa.field("started_at", pa.string()),
    pa.field("completed_at", pa.string()),
    pa.field("error_message", pa.string()),
])

SLICE_ANALYSIS_SCHEMA = pa.schema([
    pa.field("slice_id", pa.string()),
    pa.field("job_id", pa.string()),
    pa.field("batch_id", pa.string()),
    pa.field("status", pa.string()),
    pa.field("depth", pa.float64()),
    pa.field("root_name", pa.string()),
    pa.field("aggregate_name", pa.string()),
    pa.field("bounded_context", pa.string()),
    pa.field("description", pa.string()),
    pa.field("properties_json", pa.string()),
    pa.field("behaviors_json", pa.string()),
    pa.field("domain_events_json", pa.string()),
    pa.field("value_objects_json", pa.string()),
    pa.field("invariants_json", pa.string()),
    pa.field("source_summary", pa.string()),
    pa.field("llm_response_raw", pa.string()),
    pa.field("analyzed_at", pa.string()),
    pa.field("error_message", pa.string()),
    pa.field("retry_count", pa.int64()),
])

DOMAIN_MODEL_SCHEMA = pa.schema([
    pa.field("job_id", pa.string()),
    pa.field("solution_name", pa.string()),
    pa.field("bounded_context", pa.string()),
    pa.field("aggregate_name", pa.string()),
    pa.field("aggregate_json", pa.string()),
    pa.field("domain_events_json", pa.string()),
    pa.field("value_objects_json", pa.string()),
    pa.field("invariants_json", pa.string()),
    pa.field("slice_ids_json", pa.string()),
    pa.field("created_at", pa.string()),
])


def _now_iso() -> str:
    """Return current UTC time as ISO string."""
    return datetime.now(timezone.utc).isoformat()


def _generate_job_id(solution_name: str) -> str:
    """Generate a unique job ID."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"ddd_{solution_name}_{timestamp}"


def _generate_batch_id(job_id: str, batch_number: int) -> str:
    """Generate a batch ID."""
    return f"{job_id}_batch_{batch_number:04d}"


@dataclass
class DDDJobState:
    """Represents the overall state of a DDD analysis job."""
    job_id: str
    solution_name: str
    run_id: str
    status: JobStatus = JobStatus.PENDING
    total_slices: int = 0
    analyzed_slices: int = 0
    failed_slices: int = 0
    skipped_slices: int = 0
    total_batches: int = 0
    completed_batches: int = 0
    current_batch: int = 0
    batch_size: int = 50
    min_depth: int = 0
    max_depth: int = 10
    llm_provider: str = "copilot"
    llm_model: str = "gpt-4o-mini"
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    started_at: str = ""
    completed_at: str = ""
    error_message: str = ""
    config_json: str = "{}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, JobStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "DDDJobState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = JobStatus(d["status"])
        return cls(**d)


@dataclass
class DDDBatchState:
    """Represents the state of a single batch."""
    batch_id: str
    job_id: str
    batch_number: int
    status: BatchStatus = BatchStatus.PENDING
    slice_count: int = 0
    analyzed_count: int = 0
    failed_count: int = 0
    started_at: str = ""
    completed_at: str = ""
    error_message: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, BatchStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "DDDBatchState":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = BatchStatus(d["status"])
        return cls(**d)


@dataclass
class DDDSliceAnalysis:
    """Represents the analysis result for a single slice."""
    slice_id: str
    job_id: str
    batch_id: str
    status: SliceStatus = SliceStatus.PENDING
    depth: float = 0.0
    root_name: str = ""
    aggregate_name: str = ""
    bounded_context: str = ""
    description: str = ""
    properties_json: str = "[]"
    behaviors_json: str = "[]"
    domain_events_json: str = "[]"
    value_objects_json: str = "[]"
    invariants_json: str = "[]"
    source_summary: str = ""
    llm_response_raw: str = ""
    analyzed_at: str = ""
    error_message: str = ""
    retry_count: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, SliceStatus) else self.status
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "DDDSliceAnalysis":
        d = d.copy()
        if "status" in d and isinstance(d["status"], str):
            d["status"] = SliceStatus(d["status"])
        return cls(**d)


class DDDStateManager:
    """
    Manages DDD analysis state using Parquet files.
    
    Provides:
    - Job creation and tracking
    - Batch progress management
    - Slice analysis storage
    - Resume capability
    - Progress queries
    """

    def __init__(self, output_root: Path, run_id: str = "latest"):
        self.output_root = Path(output_root)
        self.run_id = run_id
        self.state_dir = self.output_root / "ddd_state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.job_state_path = self.state_dir / "job_state.parquet"
        self.batch_state_path = self.state_dir / "batch_state.parquet"
        self.slice_analysis_path = self.state_dir / "slice_analysis.parquet"
        self.domain_model_path = self.state_dir / "domain_model.parquet"

    # =========================================================================
    # JOB STATE MANAGEMENT
    # =========================================================================

    def create_job(
        self,
        solution_name: str,
        total_slices: int,
        batch_size: int = 50,
        min_depth: int = 0,
        max_depth: int = 10,
        llm_provider: str = "copilot",
        llm_model: str = "gpt-4o-mini",
        config: dict | None = None,
    ) -> DDDJobState:
        """Create a new DDD analysis job."""
        import json
        
        job_id = _generate_job_id(solution_name)
        total_batches = (total_slices + batch_size - 1) // batch_size
        
        job = DDDJobState(
            job_id=job_id,
            solution_name=solution_name,
            run_id=self.run_id,
            status=JobStatus.PENDING,
            total_slices=total_slices,
            total_batches=total_batches,
            batch_size=batch_size,
            min_depth=min_depth,
            max_depth=max_depth,
            llm_provider=llm_provider,
            llm_model=llm_model,
            config_json=json.dumps(config or {}),
        )
        
        self._save_job_state(job)
        LOGGER.info("Created DDD job: %s with %d slices in %d batches", 
                   job_id, total_slices, total_batches)
        return job

    def get_job(self, job_id: str | None = None) -> DDDJobState | None:
        """Get job state by ID or latest job."""
        if not self.job_state_path.exists():
            return None
        
        table = pq.read_table(self.job_state_path)
        df = table.to_pandas()
        
        if df.empty:
            return None
        
        if job_id:
            row = df[df["job_id"] == job_id]
            if row.empty:
                return None
            return DDDJobState.from_dict(row.iloc[0].to_dict())
        else:
            # Return latest job
            df = df.sort_values("created_at", ascending=False)
            return DDDJobState.from_dict(df.iloc[0].to_dict())

    def get_latest_job_for_solution(self, solution_name: str) -> DDDJobState | None:
        """Get the latest job for a solution."""
        if not self.job_state_path.exists():
            return None
        
        table = pq.read_table(self.job_state_path)
        df = table.to_pandas()
        
        df = df[df["solution_name"] == solution_name]
        if df.empty:
            return None
        
        df = df.sort_values("created_at", ascending=False)
        return DDDJobState.from_dict(df.iloc[0].to_dict())

    def get_resumable_job(self, solution_name: str) -> DDDJobState | None:
        """Get a job that can be resumed (not completed or failed)."""
        job = self.get_latest_job_for_solution(solution_name)
        if job and job.status in (JobStatus.PENDING, JobStatus.RUNNING, JobStatus.PAUSED):
            return job
        return None

    def update_job_status(self, job_id: str, status: JobStatus, error_message: str = "") -> None:
        """Update job status."""
        job = self.get_job(job_id)
        if not job:
            raise ValueError(f"Job not found: {job_id}")
        
        job.status = status
        job.updated_at = _now_iso()
        job.error_message = error_message
        
        if status == JobStatus.RUNNING and not job.started_at:
            job.started_at = _now_iso()
        elif status in (JobStatus.COMPLETED, JobStatus.FAILED):
            job.completed_at = _now_iso()
        
        self._save_job_state(job, update=True)

    def update_job_progress(
        self,
        job_id: str,
        analyzed_slices: int | None = None,
        failed_slices: int | None = None,
        skipped_slices: int | None = None,
        completed_batches: int | None = None,
        current_batch: int | None = None,
    ) -> None:
        """Update job progress counters."""
        job = self.get_job(job_id)
        if not job:
            raise ValueError(f"Job not found: {job_id}")
        
        if analyzed_slices is not None:
            job.analyzed_slices = analyzed_slices
        if failed_slices is not None:
            job.failed_slices = failed_slices
        if skipped_slices is not None:
            job.skipped_slices = skipped_slices
        if completed_batches is not None:
            job.completed_batches = completed_batches
        if current_batch is not None:
            job.current_batch = current_batch
        
        job.updated_at = _now_iso()
        self._save_job_state(job, update=True)

    def _save_job_state(self, job: DDDJobState, update: bool = False) -> None:
        """Save job state to Parquet."""
        import pandas as pd
        
        new_row = pd.DataFrame([job.to_dict()])
        
        if update and self.job_state_path.exists():
            # Read existing, remove old entry, add new
            existing = pq.read_table(self.job_state_path).to_pandas()
            existing = existing[existing["job_id"] != job.job_id]
            df = pd.concat([existing, new_row], ignore_index=True)
        else:
            if self.job_state_path.exists():
                existing = pq.read_table(self.job_state_path).to_pandas()
                df = pd.concat([existing, new_row], ignore_index=True)
            else:
                df = new_row
        
        table = pa.Table.from_pandas(df, schema=JOB_STATE_SCHEMA, preserve_index=False)
        pq.write_table(table, self.job_state_path)

    # =========================================================================
    # BATCH STATE MANAGEMENT
    # =========================================================================

    def create_batch(self, job_id: str, batch_number: int, slice_count: int) -> DDDBatchState:
        """Create a new batch."""
        batch = DDDBatchState(
            batch_id=_generate_batch_id(job_id, batch_number),
            job_id=job_id,
            batch_number=batch_number,
            slice_count=slice_count,
        )
        self._save_batch_state(batch)
        return batch

    def get_batch(self, batch_id: str) -> DDDBatchState | None:
        """Get batch by ID."""
        if not self.batch_state_path.exists():
            return None
        
        table = pq.read_table(self.batch_state_path)
        df = table.to_pandas()
        
        row = df[df["batch_id"] == batch_id]
        if row.empty:
            return None
        return DDDBatchState.from_dict(row.iloc[0].to_dict())

    def get_batches_for_job(self, job_id: str) -> list[DDDBatchState]:
        """Get all batches for a job."""
        if not self.batch_state_path.exists():
            return []
        
        table = pq.read_table(self.batch_state_path)
        df = table.to_pandas()
        
        df = df[df["job_id"] == job_id].sort_values("batch_number")
        return [DDDBatchState.from_dict(row.to_dict()) for _, row in df.iterrows()]

    def get_next_pending_batch(self, job_id: str) -> DDDBatchState | None:
        """Get the next batch that needs processing."""
        batches = self.get_batches_for_job(job_id)
        for batch in batches:
            if batch.status in (BatchStatus.PENDING, BatchStatus.IN_PROGRESS):
                return batch
        return None

    def update_batch_status(
        self,
        batch_id: str,
        status: BatchStatus,
        analyzed_count: int | None = None,
        failed_count: int | None = None,
        error_message: str = "",
    ) -> None:
        """Update batch status."""
        batch = self.get_batch(batch_id)
        if not batch:
            raise ValueError(f"Batch not found: {batch_id}")
        
        batch.status = status
        if analyzed_count is not None:
            batch.analyzed_count = analyzed_count
        if failed_count is not None:
            batch.failed_count = failed_count
        batch.error_message = error_message
        
        if status == BatchStatus.IN_PROGRESS and not batch.started_at:
            batch.started_at = _now_iso()
        elif status in (BatchStatus.COMPLETED, BatchStatus.FAILED):
            batch.completed_at = _now_iso()
        
        self._save_batch_state(batch, update=True)

    def _save_batch_state(self, batch: DDDBatchState, update: bool = False) -> None:
        """Save batch state to Parquet."""
        import pandas as pd
        
        new_row = pd.DataFrame([batch.to_dict()])
        
        if update and self.batch_state_path.exists():
            existing = pq.read_table(self.batch_state_path).to_pandas()
            existing = existing[existing["batch_id"] != batch.batch_id]
            df = pd.concat([existing, new_row], ignore_index=True)
        else:
            if self.batch_state_path.exists():
                existing = pq.read_table(self.batch_state_path).to_pandas()
                df = pd.concat([existing, new_row], ignore_index=True)
            else:
                df = new_row
        
        table = pa.Table.from_pandas(df, schema=BATCH_STATE_SCHEMA, preserve_index=False)
        pq.write_table(table, self.batch_state_path)

    # =========================================================================
    # SLICE ANALYSIS MANAGEMENT
    # =========================================================================

    def register_slices(
        self,
        job_id: str,
        batch_id: str,
        slices: list[dict],
    ) -> None:
        """Register slices for analysis (creates pending entries)."""
        import pandas as pd
        
        records = []
        for slice_info in slices:
            records.append(DDDSliceAnalysis(
                slice_id=slice_info["slice_id"],
                job_id=job_id,
                batch_id=batch_id,
                depth=slice_info.get("depth", 0.0),
                root_name=slice_info.get("root_name", ""),
                source_summary=slice_info.get("summary", ""),
            ).to_dict())
        
        new_df = pd.DataFrame(records)
        
        if self.slice_analysis_path.exists():
            existing = pq.read_table(self.slice_analysis_path).to_pandas()
            # Don't duplicate existing slices
            existing_ids = set(existing["slice_id"].tolist())
            new_df = new_df[~new_df["slice_id"].isin(existing_ids)]
            df = pd.concat([existing, new_df], ignore_index=True)
        else:
            df = new_df
        
        table = pa.Table.from_pandas(df, schema=SLICE_ANALYSIS_SCHEMA, preserve_index=False)
        pq.write_table(table, self.slice_analysis_path)

    def get_slice_analysis(self, slice_id: str) -> DDDSliceAnalysis | None:
        """Get analysis for a specific slice."""
        if not self.slice_analysis_path.exists():
            return None
        
        table = pq.read_table(self.slice_analysis_path)
        df = table.to_pandas()
        
        row = df[df["slice_id"] == slice_id]
        if row.empty:
            return None
        return DDDSliceAnalysis.from_dict(row.iloc[0].to_dict())

    def get_pending_slices(self, job_id: str, batch_id: str | None = None, limit: int = 50) -> list[DDDSliceAnalysis]:
        """Get pending slices for analysis."""
        if not self.slice_analysis_path.exists():
            return []
        
        table = pq.read_table(self.slice_analysis_path)
        df = table.to_pandas()
        
        df = df[df["job_id"] == job_id]
        df = df[df["status"] == SliceStatus.PENDING.value]
        
        if batch_id:
            df = df[df["batch_id"] == batch_id]
        
        df = df.head(limit)
        return [DDDSliceAnalysis.from_dict(row.to_dict()) for _, row in df.iterrows()]

    def get_analyzed_slices(self, job_id: str) -> list[DDDSliceAnalysis]:
        """Get all analyzed slices for a job."""
        if not self.slice_analysis_path.exists():
            return []
        
        table = pq.read_table(self.slice_analysis_path)
        df = table.to_pandas()
        
        df = df[df["job_id"] == job_id]
        df = df[df["status"] == SliceStatus.ANALYZED.value]
        
        return [DDDSliceAnalysis.from_dict(row.to_dict()) for _, row in df.iterrows()]

    def save_slice_analysis(
        self,
        slice_id: str,
        job_id: str,
        analysis: dict,
        llm_response_raw: str = "",
    ) -> None:
        """Save analysis result for a slice."""
        import json
        import pandas as pd
        
        existing_slice = self.get_slice_analysis(slice_id)
        if not existing_slice:
            raise ValueError(f"Slice not registered: {slice_id}")
        
        # Update with analysis results
        existing_slice.status = SliceStatus.ANALYZED
        existing_slice.aggregate_name = analysis.get("aggregate_name", "")
        existing_slice.bounded_context = analysis.get("bounded_context_hint", "")
        existing_slice.description = analysis.get("description", "")
        existing_slice.properties_json = json.dumps(analysis.get("properties", []))
        existing_slice.behaviors_json = json.dumps(analysis.get("behaviors", []))
        existing_slice.domain_events_json = json.dumps(analysis.get("domain_events", []))
        existing_slice.value_objects_json = json.dumps(analysis.get("value_objects", []))
        existing_slice.invariants_json = json.dumps(analysis.get("invariants", []))
        existing_slice.llm_response_raw = llm_response_raw
        existing_slice.analyzed_at = _now_iso()
        
        self._update_slice_analysis(existing_slice)

    def mark_slice_failed(self, slice_id: str, error_message: str) -> None:
        """Mark a slice as failed."""
        existing = self.get_slice_analysis(slice_id)
        if not existing:
            return
        
        existing.status = SliceStatus.FAILED
        existing.error_message = error_message
        existing.retry_count += 1
        self._update_slice_analysis(existing)

    def mark_slice_skipped(self, slice_id: str, reason: str = "") -> None:
        """Mark a slice as skipped."""
        existing = self.get_slice_analysis(slice_id)
        if not existing:
            return
        
        existing.status = SliceStatus.SKIPPED
        existing.error_message = reason
        self._update_slice_analysis(existing)

    def _update_slice_analysis(self, analysis: DDDSliceAnalysis) -> None:
        """Update a slice analysis record."""
        import pandas as pd
        
        if not self.slice_analysis_path.exists():
            return
        
        existing = pq.read_table(self.slice_analysis_path).to_pandas()
        existing = existing[existing["slice_id"] != analysis.slice_id]
        
        new_row = pd.DataFrame([analysis.to_dict()])
        df = pd.concat([existing, new_row], ignore_index=True)
        
        table = pa.Table.from_pandas(df, schema=SLICE_ANALYSIS_SCHEMA, preserve_index=False)
        pq.write_table(table, self.slice_analysis_path)

    # =========================================================================
    # PROGRESS QUERIES
    # =========================================================================

    def get_job_progress(self, job_id: str) -> dict:
        """Get comprehensive progress report for a job."""
        job = self.get_job(job_id)
        if not job:
            return {"error": f"Job not found: {job_id}"}
        
        # Get slice counts by status
        slice_counts = self._count_slices_by_status(job_id)
        
        # Get batch progress
        batches = self.get_batches_for_job(job_id)
        batch_summary = {
            "total": len(batches),
            "pending": sum(1 for b in batches if b.status == BatchStatus.PENDING),
            "in_progress": sum(1 for b in batches if b.status == BatchStatus.IN_PROGRESS),
            "completed": sum(1 for b in batches if b.status == BatchStatus.COMPLETED),
            "failed": sum(1 for b in batches if b.status == BatchStatus.FAILED),
        }
        
        # Calculate percentages
        total = slice_counts.get("total", 0)
        analyzed = slice_counts.get("analyzed", 0)
        percentage = (analyzed / total * 100) if total > 0 else 0
        
        # Estimate remaining time
        elapsed = 0
        eta_minutes = 0
        if job.started_at:
            start = datetime.fromisoformat(job.started_at.replace("Z", "+00:00"))
            elapsed = (datetime.now(timezone.utc) - start).total_seconds()
            if analyzed > 0:
                rate = analyzed / elapsed  # slices per second
                remaining = total - analyzed
                eta_minutes = (remaining / rate / 60) if rate > 0 else 0
        
        return {
            "job_id": job.job_id,
            "solution_name": job.solution_name,
            "status": job.status.value,
            "progress": {
                "total_slices": total,
                "analyzed": analyzed,
                "failed": slice_counts.get("failed", 0),
                "skipped": slice_counts.get("skipped", 0),
                "pending": slice_counts.get("pending", 0),
                "in_progress": slice_counts.get("in_progress", 0),
                "percentage": round(percentage, 2),
            },
            "batches": batch_summary,
            "timing": {
                "started_at": job.started_at,
                "elapsed_seconds": round(elapsed, 1),
                "eta_minutes": round(eta_minutes, 1),
            },
            "config": {
                "batch_size": job.batch_size,
                "llm_provider": job.llm_provider,
                "llm_model": job.llm_model,
            },
            "can_resume": job.status in (JobStatus.PENDING, JobStatus.RUNNING, JobStatus.PAUSED),
        }

    def _count_slices_by_status(self, job_id: str) -> dict:
        """Count slices by status for a job."""
        if not self.slice_analysis_path.exists():
            return {"total": 0}
        
        table = pq.read_table(self.slice_analysis_path)
        df = table.to_pandas()
        
        df = df[df["job_id"] == job_id]
        
        counts = df["status"].value_counts().to_dict()
        counts["total"] = len(df)
        return counts

    def get_bounded_context_summary(self, job_id: str) -> dict:
        """Get summary of bounded contexts discovered."""
        analyzed = self.get_analyzed_slices(job_id)
        
        contexts = {}
        for slice_analysis in analyzed:
            ctx = slice_analysis.bounded_context or "Unknown"
            if ctx not in contexts:
                contexts[ctx] = {
                    "name": ctx,
                    "aggregates": set(),
                    "slice_count": 0,
                }
            contexts[ctx]["aggregates"].add(slice_analysis.aggregate_name)
            contexts[ctx]["slice_count"] += 1
        
        # Convert sets to counts
        result = []
        for ctx, data in sorted(contexts.items(), key=lambda x: -x[1]["slice_count"]):
            result.append({
                "bounded_context": data["name"],
                "aggregate_count": len(data["aggregates"]),
                "aggregates": sorted(data["aggregates"]),
                "slice_count": data["slice_count"],
            })
        
        return {
            "job_id": job_id,
            "total_contexts": len(result),
            "bounded_contexts": result,
        }

    # =========================================================================
    # DOMAIN MODEL SYNTHESIS
    # =========================================================================

    def synthesize_domain_model(self, job_id: str) -> dict:
        """Synthesize the domain model from analyzed slices (no LLM needed)."""
        import json
        import pandas as pd
        
        analyzed = self.get_analyzed_slices(job_id)
        job = self.get_job(job_id)
        
        if not job:
            return {"error": "Job not found"}
        
        # Group by bounded context
        contexts = {}
        for slice_analysis in analyzed:
            ctx = slice_analysis.bounded_context or "Unknown"
            if ctx not in contexts:
                contexts[ctx] = {
                    "name": ctx,
                    "aggregates": {},
                    "domain_events": set(),
                    "value_objects": {},
                    "invariants": set(),
                }
            
            bc = contexts[ctx]
            
            # Add aggregate
            agg_name = slice_analysis.aggregate_name
            if agg_name and agg_name not in bc["aggregates"]:
                bc["aggregates"][agg_name] = {
                    "name": agg_name,
                    "description": slice_analysis.description,
                    "properties": json.loads(slice_analysis.properties_json or "[]"),
                    "behaviors": json.loads(slice_analysis.behaviors_json or "[]"),
                    "slice_ids": [slice_analysis.slice_id],
                }
            elif agg_name:
                bc["aggregates"][agg_name]["slice_ids"].append(slice_analysis.slice_id)
            
            # Collect domain events
            for event in json.loads(slice_analysis.domain_events_json or "[]"):
                bc["domain_events"].add(event)
            
            # Collect value objects
            for vo in json.loads(slice_analysis.value_objects_json or "[]"):
                if isinstance(vo, dict) and vo.get("name"):
                    bc["value_objects"][vo["name"]] = vo
            
            # Collect invariants
            for inv in json.loads(slice_analysis.invariants_json or "[]"):
                bc["invariants"].add(inv)
        
        # Save to domain model parquet
        records = []
        for ctx_name, ctx_data in contexts.items():
            for agg_name, agg_data in ctx_data["aggregates"].items():
                records.append({
                    "job_id": job_id,
                    "solution_name": job.solution_name,
                    "bounded_context": ctx_name,
                    "aggregate_name": agg_name,
                    "aggregate_json": json.dumps(agg_data),
                    "domain_events_json": json.dumps(sorted(ctx_data["domain_events"])),
                    "value_objects_json": json.dumps(list(ctx_data["value_objects"].values())),
                    "invariants_json": json.dumps(list(ctx_data["invariants"])),
                    "slice_ids_json": json.dumps(agg_data["slice_ids"]),
                    "created_at": _now_iso(),
                })
        
        if records:
            df = pd.DataFrame(records)
            table = pa.Table.from_pandas(df, schema=DOMAIN_MODEL_SCHEMA, preserve_index=False)
            pq.write_table(table, self.domain_model_path)
        
        # Return summary
        return {
            "job_id": job_id,
            "solution_name": job.solution_name,
            "total_bounded_contexts": len(contexts),
            "total_aggregates": sum(len(c["aggregates"]) for c in contexts.values()),
            "total_domain_events": sum(len(c["domain_events"]) for c in contexts.values()),
            "bounded_contexts": [
                {
                    "name": ctx,
                    "aggregates": len(data["aggregates"]),
                    "events": len(data["domain_events"]),
                }
                for ctx, data in sorted(contexts.items(), key=lambda x: -len(x[1]["aggregates"]))
            ],
        }

    def load_domain_model(self, job_id: str) -> list[dict]:
        """Load the synthesized domain model."""
        import json
        
        if not self.domain_model_path.exists():
            return []
        
        table = pq.read_table(self.domain_model_path)
        df = table.to_pandas()
        
        df = df[df["job_id"] == job_id]
        
        results = []
        for _, row in df.iterrows():
            results.append({
                "bounded_context": row["bounded_context"],
                "aggregate_name": row["aggregate_name"],
                "aggregate": json.loads(row["aggregate_json"]),
                "domain_events": json.loads(row["domain_events_json"]),
                "value_objects": json.loads(row["value_objects_json"]),
                "invariants": json.loads(row["invariants_json"]),
            })
        
        return results


def get_state_manager(output_root: str | Path = DEFAULT_PARQUET_ROOT, run_id: str = "latest") -> DDDStateManager:
    """Factory function to get a state manager instance."""
    return DDDStateManager(Path(output_root), run_id)
