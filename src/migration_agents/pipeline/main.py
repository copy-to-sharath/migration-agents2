from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

from migration_agents.logging_utils import setup_logging
from migration_agents.domain_architect.config import load_config as load_domain_config
from migration_agents.domain_architect.main import run as run_domain
from migration_agents.ingestion.config import load_config as load_ingestion_config
from migration_agents.ingestion.main import run as run_ingestion
from migration_agents.api_migration.config import load_config as load_api_config
from migration_agents.api_migration.main import run as run_api_migration
from migration_agents.codegen.config import load_config as load_codegen_config
from migration_agents.codegen.main import run as run_codegen
from migration_agents.knowledge_base.config import load_config as load_knowledge_config
from migration_agents.knowledge_base.main import run as run_knowledge
from migration_agents.logic_manifester.config import load_config as load_logic_config
from migration_agents.logic_manifester.main import run as run_logic
from migration_agents.parser.config import load_config as load_parser_config
from migration_agents.parser.main import run as run_parser
from migration_agents.slice_extractor.config import load_config as load_slice_config
from migration_agents.slice_extractor.main import run as run_slice
from migration_agents.vectorization.config import load_config as load_vector_config
from migration_agents.vectorization.main import run as run_vector
from migration_agents.state import load_state

from .config import PipelineConfig, load_config

LOGGER = logging.getLogger("migration_agents.pipeline")


def _run_stage(name: str, config_path: Path | None, require_previous: list[str], stage_states: dict) -> None:
    if not config_path:
        LOGGER.info("pipeline_skip stage=%s reason=no_config", name)
        return
    for prev in require_previous:
        prev_state = stage_states.get(prev) or load_state(prev)
        if not prev_state or prev_state.get("status") != "finished":
            raise RuntimeError(f"pipeline_stage_blocked stage={name} missing prerequisite state={prev}")
    LOGGER.info("pipeline_stage_start stage=%s config=%s", name, config_path)
    start = time.monotonic()
    if name == "ingestion":
        run_ingestion(load_ingestion_config(config_path))
    elif name == "parser":
        run_parser(load_parser_config(config_path))
    elif name == "vectorization":
        run_vector(load_vector_config(config_path))
    elif name == "slice_extractor":
        run_slice(load_slice_config(config_path))
    elif name == "logic_manifester":
        run_logic(load_logic_config(config_path))
    elif name == "domain_architect":
        run_domain(load_domain_config(config_path))
    elif name == "knowledge_base":
        run_knowledge(load_knowledge_config(config_path))
    elif name == "api_migration":
        run_api_migration(load_api_config(config_path))
    elif name == "codegen":
        run_codegen(load_codegen_config(config_path))
    else:
        raise ValueError(f"Unknown pipeline stage: {name}")
    duration = time.monotonic() - start
    stage_states[name] = load_state(name)
    LOGGER.info("pipeline_stage_done stage=%s seconds=%.2f", name, duration)


def run(config: PipelineConfig) -> None:
    stage_configs = {
        "ingestion": config.ingestion_config,
        "parser": config.parser_config,
        "vectorization": config.vectorization_config,
        "slice_extractor": config.slice_extractor_config,
        "logic_manifester": config.logic_manifester_config,
        "domain_architect": config.domain_architect_config,
        "knowledge_base": config.knowledge_base_config,
        "api_migration": config.api_migration_config,
        "codegen": config.codegen_config,
    }
    dependencies = {
        "parser": ["ingestion"],
        "vectorization": ["parser"],
        "slice_extractor": ["parser"],
        "logic_manifester": ["slice_extractor"],
        "domain_architect": ["logic_manifester", "parser"],
        "knowledge_base": ["domain_architect"],
        "api_migration": ["domain_architect"],
        "codegen": ["api_migration"],
    }
    stage_states: dict = {}
    for stage in config.stages:
        _run_stage(stage, stage_configs.get(stage), dependencies.get(stage, []), stage_states)


def main() -> None:
    from migration_agents.constants import ensure_directories
    
    # Ensure all standard directories exist
    ensure_directories()
    
    parser = argparse.ArgumentParser(description="Pipeline runner.")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    if not logging.getLogger().handlers:
        setup_logging("pipeline")
    config = load_config(args.config)
    run(config)


if __name__ == "__main__":
    main()
