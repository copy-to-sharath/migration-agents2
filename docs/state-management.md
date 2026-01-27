# Pipeline State Management

Parquet-based state management enables resumable processing for all pipeline operations.
Progress survives chat restarts, crashes, and interruptions.

## Overview

The state management system persists progress to Parquet files for:

- **DDD Analysis**: Track slice-by-slice DDD analysis progress
- **Code Generation**: Resume batch code generation jobs
- **Validation**: Track validation runs, scores, and fix history
- **Approvals**: Persist approval workflow decisions

## State Managers

### DDD State Manager

For DDD analysis of large codebases (100+ slices).

**Location**: `data/parquet/ddd_state/`

| File | Purpose |
|------|---------|
| `job_state.parquet` | Overall job metadata and progress counters |
| `batch_state.parquet` | Per-batch tracking (pending, in-progress, completed) |
| `slice_analysis.parquet` | Individual slice DDD analysis results |
| `domain_model.parquet` | Synthesized domain model artifacts |

### Pipeline State Manager

For code generation, validation, and approval workflows.

**Location**: `data/parquet/pipeline_state/`

| File | Purpose |
|------|---------|
| `codegen_job_state.parquet` | Code generation job metadata and progress |
| `codegen_slice_state.parquet` | Per-slice code generation status |
| `validation_run_state.parquet` | Validation run results and scores |
| `validation_fix_state.parquet` | Pending and applied validation fixes |
| `approval_state.parquet` | Step approval decisions and history |

## MCP Tools

### DDD Analysis Tools

#### Creating a Job

```
ddd_create_job solution_name='NopCommerce' batch_size=50 min_depth=0 max_depth=10
```

Creates a new job with Parquet state tracking. Returns job_id and total slices.

#### Checking Progress

```
ddd_get_job_progress solution_name='NopCommerce'
```

Returns comprehensive progress report:
- Total/analyzed/pending slice counts
- Batch progress (pending, in-progress, completed)
- Elapsed time and ETA
- Whether job can be resumed

#### Listing Pending Work

```
ddd_list_pending_slices solution_name='NopCommerce' limit=50
```

Returns slices that still need analysis.

#### Resuming After Restart

```
ddd_resume_job solution_name='NopCommerce'
```

Finds the latest resumable job and continues from last checkpoint.
Returns the next batch of slices ready for analysis.

#### Viewing Bounded Contexts

```
ddd_get_context_summary solution_name='NopCommerce'
```

Returns summary of bounded contexts discovered so far, with aggregate counts.

### Code Generation Tools

#### Running Batch Codegen (with state tracking)

```
batch_codegen phase='all' confirm=true
```

Automatically creates/resumes codegen jobs with state tracking.

#### Checking Batch Status

```
get_batch_status solution_name='NopCommerce'
```

Returns file counts, DDD status, and job progress from state manager.

### Validation Tools

#### Running Validation

```
validate_migration project_path='generated/nopcommerce'
```

Creates validation run in state manager with scores and issues.

#### Getting Validation History

```
get_validation_history solution_name='NopCommerce' limit=10
```

Returns history of all validation runs with scores.

#### Managing Fixes

```
create_validation_review project_path='generated/nopcommerce'
apply_validation_fixes project_path='generated/nopcommerce' confirm=true
```

Fixes are tracked in state manager for audit history.

### Approval Workflow Tools

#### Getting Step for Approval

```
get_step_for_approval project_path='generated/nopcommerce' step_name='domain'
```

Returns step details and creates approval record in state.

#### Submitting Approval

```
submit_step_approval project_path='generated/nopcommerce' step_name='domain' decision='APPROVE' reviewer='John'
```

Persists approval decision to state manager.

#### Checking Status

```
get_approval_status project_path='generated/nopcommerce'
```

Returns all approval steps with status from state manager.

## DDD Analysis Workflow

### Initial Setup

```
# 1. Create job with state tracking
ddd_create_job solution_name='NopCommerce' batch_size=50

# 2. Start batch analysis
batch_ddd_analysis solution_name='NopCommerce'

# 3. For each slice in batch, analyze and store
batch_ddd_apply_slice solution_name='NopCommerce' slice_id='entry_xxx' analysis={...}

# 4. Continue with next batch
batch_ddd_analysis solution_name='NopCommerce' start_batch=1
```

### Resuming After Chat Restart

```
# 1. Check current state
ddd_get_job_progress solution_name='NopCommerce'

# Output shows:
# - status: "running" 
# - progress: {total: 4000, analyzed: 1500, pending: 2500}
# - can_resume: true

# 2. Resume the job
ddd_resume_job solution_name='NopCommerce'

# Output shows next batch ready to process

# 3. Continue processing
batch_ddd_analysis solution_name='NopCommerce'
```

### Completing the Job

```
# 1. Check all slices analyzed
ddd_get_job_progress solution_name='NopCommerce'

# 2. Build domain model (no LLM needed - synthesizes from Parquet)
batch_ddd_build_model solution_name='NopCommerce'

# 3. Generate code
batch_codegen phase='all' confirm=true
```

## Job States

| State | Description |
|-------|-------------|
| `pending` | Job created, not yet started |
| `running` | Actively processing slices |
| `paused` | Temporarily stopped (can resume) |
| `completed` | All slices analyzed successfully |
| `failed` | Stopped due to error |

Resumable states: `pending`, `running`, `paused`

## Slice States

| State | Description |
|-------|-------------|
| `pending` | Not yet analyzed |
| `in_progress` | Currently being analyzed |
| `analyzed` | Successfully analyzed |
| `skipped` | Skipped (e.g., duplicate, irrelevant) |
| `failed` | Analysis failed |

## Configuration

The batch configuration is in `config/ddd_batch.json`:

```json
{
  "job": {
    "solution_name": "nopcommerce",
    "output_root": "data/parquet"
  },
  "batch": {
    "batch_size": 50,
    "auto_checkpoint": true
  },
  "llm": {
    "provider": "copilot",
    "model": "gpt-4o-mini"
  },
  "resume": {
    "enabled": true,
    "skip_completed_slices": true
  }
}
```

## Data Model

### Job State Schema

| Field | Type | Description |
|-------|------|-------------|
| `job_id` | string | Unique job identifier |
| `solution_name` | string | Solution being analyzed |
| `status` | string | Job status (pending/running/completed/failed) |
| `total_slices` | int | Total slices in scope |
| `analyzed_slices` | int | Successfully analyzed |
| `failed_slices` | int | Failed analysis count |
| `total_batches` | int | Number of batches |
| `current_batch` | int | Current batch number |
| `llm_provider` | string | LLM provider (copilot/github/openai) |
| `created_at` | string | Job creation timestamp |
| `started_at` | string | Analysis start timestamp |

### Slice Analysis Schema

| Field | Type | Description |
|-------|------|-------------|
| `slice_id` | string | Slice identifier |
| `job_id` | string | Parent job |
| `status` | string | Analysis status |
| `aggregate_name` | string | Extracted aggregate name |
| `bounded_context` | string | Inferred bounded context |
| `properties_json` | string | JSON array of properties |
| `behaviors_json` | string | JSON array of behaviors |
| `domain_events_json` | string | JSON array of events |
| `analyzed_at` | string | Analysis timestamp |

## Pipeline State Data Models

### Codegen Job State

| Field | Type | Description |
|-------|------|-------------|
| `job_id` | string | Unique job identifier |
| `solution_name` | string | Solution being generated |
| `phase` | string | Phase (domain/contract/code/all) |
| `status` | string | Job status |
| `total_slices` | int | Total slices to process |
| `generated_slices` | int | Successfully generated |
| `failed_slices` | int | Failed count |
| `current_batch` | int | Current batch number |

### Validation Run State

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | string | Unique run identifier |
| `solution_name` | string | Solution validated |
| `overall_score` | float | Overall validation score |
| `domain_score` | float | Domain layer score |
| `application_score` | float | Application layer score |
| `api_score` | float | API layer score |
| `total_issues` | int | Total issues found |
| `critical_issues` | int | Critical issues count |

### Approval State

| Field | Type | Description |
|-------|------|-------------|
| `step_id` | string | Unique step identifier |
| `solution_name` | string | Solution being reviewed |
| `step_name` | string | Step name (domain, contract, etc.) |
| `status` | string | Approval status |
| `reviewer` | string | Reviewer name |
| `decision` | string | Decision made |
| `comments` | string | Review comments |
| `reviewed_at` | string | Review timestamp |

## Troubleshooting

### "No job found"
Create a new job first:
```
ddd_create_job solution_name='...'
```

### "Job not resumable"
The job is already completed or failed. Create a new job or clean the pipeline.

### "No slices found"
Run the analyzer first to generate slices:
```
analyzer step='slice' confirm=true
```

### Progress seems stuck
Check for failed slices:
```sql
SELECT slice_id, error_message 
FROM read_parquet('data/parquet/ddd_state/slice_analysis.parquet')
WHERE status = 'failed'
```

### Clear all state and start fresh
```
clean_pipeline confirm=true
ddd_create_job solution_name='...'
```
