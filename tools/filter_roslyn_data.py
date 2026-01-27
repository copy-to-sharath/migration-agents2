import duckdb
import os
import shutil
from pathlib import Path

# Config
src_root = "data/parquet/run_20260120155302/stage_1"
dst_root = "data/parquet/roslyn_only/run_20260120155302/stage_1"
tables = ["symbols", "calls", "conditions", "constants", "data_access"]

# Clean dest
if os.path.exists(dst_root):
    shutil.rmtree(dst_root)
os.makedirs(dst_root, exist_ok=True)

con = duckdb.connect()

for table in tables:
    print(f"Processing {table}...")
    src_path = f"{src_root}/{table}/*/*/*.parquet"
    
    # Check if files exist
    try:
        count = con.execute(f"SELECT count(*) FROM read_parquet('{src_path}')").fetchone()[0]
        print(f"  Found {count} rows in source.")
    except Exception as e:
        print(f"  Skipping {table} (no files or error: {e})")
        continue

    # Create destination partition structure manually or let duckdb/hive do it? 
    # DuckDB's COPY handles partitioning if specified.
    # But for simplicity, we just dump to one file per table in the right folder structure if parser supports it.
    # The parser uses standard dataset reading, so structure matters.
    # Partition cols: run_id, artifact_version.
    
    # We will write to dst_root/{table}/run_id=.../artifact_version=.../part.parquet
    
    # Query to filter C# files (or exclude .aspx, .html, etc if easy, but including .cs is safer).
    # Also include .vb if any.
    
    query = f"""
        COPY (
            SELECT * FROM read_parquet('{src_path}')
            WHERE file_path LIKE '%.cs' OR file_path LIKE '%.vb'
        ) TO '{dst_root}/{table}' (FORMAT PARQUET, PARTITION_BY (run_id, artifact_version), OVERWRITE_OR_IGNORE 1)
    """
    
    con.execute(query)
    print(f"  Exported filtered {table}.")

print("Done.")
