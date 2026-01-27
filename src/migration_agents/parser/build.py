from __future__ import annotations

import argparse
from pathlib import Path

from migration_agents.parser.config import ParserConfig, load_config
from migration_agents.parser.main import run


def main() -> None:
    from migration_agents.constants import ensure_directories
    ensure_directories()
    
    parser = argparse.ArgumentParser(description="Parser build-only entrypoint (no LLM).")
    parser.add_argument("--config", type=Path, required=True, help="Parser build config JSON")
    args = parser.parse_args()

    cfg: ParserConfig = load_config(args.config)
    run(cfg, run_llm=False)


if __name__ == "__main__":
    main()
