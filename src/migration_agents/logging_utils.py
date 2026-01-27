from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(stage: str) -> Path:
    """
    Configure logging to write to logs/<stage>_<timestamp>.log and stdout.
    """
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{stage}_{datetime.now():%Y%m%d%H%M%S}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return log_file
