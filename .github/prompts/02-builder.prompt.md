---
name: 02-builder
description: Generate domain model via DDD-first workflow, then generate code artifacts per slice.
---

# 02-Builder Agent

## Standard Paths (Use These Defaults)

| Path | Purpose |
|------|---------|
| `config/codegen.json` | Code generation config |
| `config/ddd_batch.json` | DDD batch processing config |
| `data/parquet/` | Lakehouse (Parquet tables) |
| `generated/` | Output directory for generated code |

## Getting Started

```
discover_tools agent='02-builder'
discover_tools agent='02-builder' category='ddd'
discover_tools agent='02-builder' category='batch'
```

## Quick Start - Batch DDD (Recommended)

```bash
# 1. Create job with state tracking
ddd_create_job solution_name='NopCommerce' batch_size=50

# 2. Get batch of slices to analyze
batch_ddd_analysis solution_name='NopCommerce'

# 3. For each slice, apply analysis
batch_ddd_apply_slice solution_name='NopCommerce' slice_id='entry_xxx' analysis={...}

# 4. Check progress (survives restart)
ddd_get_job_progress solution_name='NopCommerce'

# 5. Build domain model
batch_ddd_build_model solution_name='NopCommerce'

# 6. Validate and review
ddd_validate_coverage solution_name='NopCommerce'
ddd_get_sme_review solution_name='NopCommerce'
ddd_submit_sme_review solution_name='NopCommerce' review_status='APPROVE'

# 7. Generate code
batch_codegen config_path='config/codegen.json' phase='all' confirm=true
```

## Resume After Restart

```bash
ddd_get_job_progress solution_name='NopCommerce'
ddd_resume_job solution_name='NopCommerce'
ddd_list_pending_slices solution_name='NopCommerce'
```

## Key Config Settings

**codegen.json:**
- `solution_name`: `NopCommerce` (project name)
- `generated_root`: `generated` (output directory)
- `target_framework`: `dotnet8`
- `ddd_first`: `true`
- `ddd_phase`: `all` (or `domain`, `gherkin`, `contract`)

## DDD Analysis Output Format

```json
{
  "aggregate_name": "PaymentGateway",
  "properties": [{"name": "gatewayId", "type": "PaymentGatewayId", "is_identifier": true}],
  "behaviors": [{"name": "ProcessPayment", "description": "Process a payment"}],
  "domain_events": [{"name": "PaymentProcessed", "triggered_by": "ProcessPayment"}],
  "value_objects": [{"name": "PaymentProvider", "properties": ["name", "apiEndpoint"]}]
}
```

## Handoff

- **From 01-analyzer**: `list_slices` shows available slices
- **To 03-judge**: After code generation for validation
