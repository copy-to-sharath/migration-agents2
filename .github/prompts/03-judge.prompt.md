---
name: 03-judge
description: Validate build/test status, citation completeness, and logic alignment. Populate fix queue.
---

# 03-Judge Agent

## Standard Paths (Use These Defaults)

| Path | Purpose |
|------|---------|
| `config/judge.json` | Validation config |
| `generated/` | Generated code to validate |
| `generated/<solution>-modern/` | Standard project path pattern |
| `data/parquet/` | Lakehouse (Parquet tables) |

## Getting Started

```
discover_tools agent='03-judge'
discover_tools category='validation'
```

## Quick Start

```bash
# 1. Validate the generated project
validate_migration project_path='generated/nopcommerce-modern' output_format='detailed'

# 2. Check coverage
get_coverage_summary project_path='generated/nopcommerce-modern'

# 3. If issues found, create review with fixes
create_validation_review project_path='generated/nopcommerce-modern' auto_generate_fixes=true

# 4. List fixes for builder
list_validation_fixes project_path='generated/nopcommerce-modern'
```

## Validation Checks

| Check | Pass Criteria |
|-------|---------------|
| Build Status | No compilation errors |
| Test Status | All tests pass |
| Rule Coverage | All logic rules exercised |
| Citations | Every artifact has `source_ref` |
| Endpoint Coverage | All endpoints covered |
| Dead Code | No dead code dependencies |

## Output Formats

```bash
# Summary only (scores)
validate_migration project_path='generated/nopcommerce-modern' output_format='summary'

# Detailed with rubrics
validate_migration project_path='generated/nopcommerce-modern' output_format='detailed'

# Raw JSON
validate_migration project_path='generated/nopcommerce-modern' output_format='json'
```

## Validate Specific Stages

```bash
validate_migration project_path='generated/nopcommerce-modern' stages=['domain']
validate_migration project_path='generated/nopcommerce-modern' stages=['domain', 'api']
validate_migration project_path='generated/nopcommerce-modern' stages=['all']
```

## Fix Loop

```bash
# 1. List fixes
list_validation_fixes project_path='generated/nopcommerce-modern'

# 2. Builder applies fixes
# (handoff to 02-builder)
builder_fix fix_id='fix_001' confirm=true

# 3. Re-validate
validate_migration project_path='generated/nopcommerce-modern'
```

## Handoff

- **From 02-builder**: After code generation
- **To 02-builder** (on failure): With populated `fix_queue`
- **Complete** (on pass): Mark slice complete
