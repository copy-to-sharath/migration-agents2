"""Standard paths and constants for the migration pipeline.

This module centralizes all default paths and configuration to avoid hardcoding
throughout the codebase. Import from here instead of hardcoding paths.

Usage:
    from migration_agents.constants import DEFAULT_PATHS, CONFIG_FILES
"""
from pathlib import Path

# ============================================================================
# Standard Paths
# ============================================================================

class DefaultPaths:
    """Standard paths used throughout the pipeline."""
    
    # Lakehouse (Parquet data)
    PARQUET_ROOT = Path("data/parquet")
    PIPELINE_STATE = PARQUET_ROOT / "pipeline_state"
    ENTRY_GRAPHS_DIR = PARQUET_ROOT / "entry_graphs"
    
    # Generated output
    GENERATED_ROOT = Path("generated")
    
    # State files
    STATE_DIR = GENERATED_ROOT / "state"
    
    # Config directory
    CONFIG_DIR = Path("config")
    
    # DuckDB
    DUCKDB_DIR = Path("data/duckdb")


class ConfigFiles:
    """Standard config file paths."""
    
    # Analyzer configs
    INGESTION = "config/ingestion.json"
    PARSER = "config/parser.json"
    SLICE = "config/slice.json"
    
    # Builder configs
    CODEGEN = "config/codegen.json"
    DDD_BATCH = "config/ddd_batch.json"
    
    # Judge configs
    JUDGE = "config/judge.json"
    
    # MCP config
    MCP = "config/mcp.json"


class StateFiles:
    """Parquet state file names."""
    
    PIPELINE_STEPS = "pipeline_step_state.parquet"
    DDD_JOBS = "ddd_job_state.parquet"
    DDD_SLICES = "ddd_slice_state.parquet"
    CODEGEN = "codegen_state.parquet"
    VALIDATION = "validation_state.parquet"
    APPROVAL = "approval_state.parquet"


class PipelineSteps:
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
    
    ALL = [
        INGEST, PARSE, SLICE,
        DDD_ANALYSIS, DDD_MODEL,
        CODEGEN_DOMAIN, CODEGEN_CONTRACT, CODEGEN_CODE,
        VALIDATE, APPROVE,
    ]


class StepStatus:
    """Pipeline step statuses."""
    
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    
    ALL = [NOT_STARTED, RUNNING, PAUSED, COMPLETED, FAILED]


# Convenience aliases
DEFAULT_PATHS = DefaultPaths
CONFIG_FILES = ConfigFiles
STATE_FILES = StateFiles
PIPELINE_STEPS = PipelineSteps
STEP_STATUS = StepStatus

# Common defaults
DEFAULT_PARQUET_ROOT = str(DefaultPaths.PARQUET_ROOT)
DEFAULT_GENERATED_ROOT = str(DefaultPaths.GENERATED_ROOT)
DEFAULT_CONFIG_INGESTION = ConfigFiles.INGESTION
DEFAULT_CONFIG_PARSER = ConfigFiles.PARSER
DEFAULT_CONFIG_SLICE = ConfigFiles.SLICE
DEFAULT_CONFIG_CODEGEN = ConfigFiles.CODEGEN


# ============================================================================
# Directory Utilities
# ============================================================================

def ensure_directories() -> None:
    """Create all standard directories if they don't exist.
    
    Call this at pipeline startup to ensure the directory structure is ready.
    """
    directories = [
        DefaultPaths.PARQUET_ROOT,
        DefaultPaths.PIPELINE_STATE,
        DefaultPaths.GENERATED_ROOT,
        DefaultPaths.STATE_DIR,
        DefaultPaths.DUCKDB_DIR,
        DefaultPaths.CONFIG_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to create
        
    Returns:
        The same path (for chaining)
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(path: Path) -> Path:
    """Ensure the parent directory of a file path exists.
    
    Args:
        path: File path whose parent should exist
        
    Returns:
        The same path (for chaining)
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
