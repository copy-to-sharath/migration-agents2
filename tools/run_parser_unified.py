import shutil
import logging
from pathlib import Path
from migration_agents.parser.config import load_config
from migration_agents.parser.main import run

# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Setup paths
    run_id = "run_20260120155302"
    parquet_root = Path("data/parquet")
    stage_1_path = parquet_root / run_id / "stage_1"
    stage_1_backup = parquet_root / run_id / "stage_1_backup"

    # Backup existing stage_1
    if stage_1_path.exists():
        print(f"Backing up {stage_1_path} to {stage_1_backup}")
        if stage_1_backup.exists():
            shutil.rmtree(stage_1_backup)
        shutil.move(stage_1_path, stage_1_backup)
    
    # Check if backup exists (if run repeatedly it might be already moved)
    # If stage_1 is missing and backup missing, we are in trouble, but we have filtered data.

    # Load base config
    config_path = Path("config/parser.example.json")
    config = load_config(config_path)

    # Override config
    config.run_id = run_id
    config.roslyn_parquet_root = Path("data/parquet/roslyn_only")
    config.roslyn_parquet_run_id = run_id
    config.queries_dir = Path("config/queries") # Ensure queries dir is set

    print("Starting unified parser run...")
    run(config)
    print("Done.")
