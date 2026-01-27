#!/usr/bin/env python3
import duckdb

con = duckdb.connect()
path = 'data/parquet/run_20260120155302/stage_1'

print('Checking ASPX/ASCX parsing results...\n')

# Get file counts - optimized query
files = con.execute(f"""
    SELECT DISTINCT file_path
    FROM read_parquet('{path}/symbols/run_id=*/artifact_version=*/*.parquet')
    WHERE file_path LIKE '%.aspx' OR file_path LIKE '%.ascx'
""").fetchall()

print(f'✓ ASPX/ASCX files with symbols: {len(files)}')

# Sample symbols only - skip expensive full counts
print('\nSkipping full table scans for speed...')

# Sample symbols
print('\nSample symbols from ASPX files:')
samples = con.execute(f"""
    SELECT name, file_path, line
    FROM read_parquet('{path}/symbols/run_id=*/artifact_version=*/*.parquet')
    WHERE file_path LIKE '%.aspx'
    LIMIT 10
""").fetchall()

for name, fp, line in samples:
    filename = fp.split('/')[-1]
    print(f'  Line {line}: {name} ({filename})')

