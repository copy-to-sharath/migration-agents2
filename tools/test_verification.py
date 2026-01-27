#!/usr/bin/env python3
import duckdb
import os

con = duckdb.connect()
path = 'data/parquet/verify_run'

# Find the run directory
runs = [d for d in os.listdir(path) if d.startswith('run_')]
if not runs:
    print('No runs found')
    exit(1)
    
latest = sorted(runs)[-1]
full_path = f'{path}/{latest}/stage_1'

print(f'Testing: {full_path}\n')

# Get counts
calls = con.execute(f"SELECT COUNT(*) FROM read_parquet('{full_path}/calls/**/*.parquet')").fetchone()[0]
symbols = con.execute(f"SELECT COUNT(*) FROM read_parquet('{full_path}/symbols/**/*.parquet')").fetchone()[0]
print(f'Calls: {calls:,}')
print(f'Symbols: {symbols:,}')

# JOIN test
matches = con.execute(f"""
    SELECT COUNT(*)
    FROM read_parquet('{full_path}/calls/**/*.parquet') c
    JOIN read_parquet('{full_path}/symbols/**/*.parquet') s
        ON c.CalleeId = s.SymbolId
""").fetchone()[0]

print(f'\nMatching calls: {matches:,}')
print(f'Match rate: {matches * 100.0 / calls:.2f}%')

if matches > 0:
    print('\n✓ SUCCESS! CalleeIds now match SymbolIds!')
    
    # Check for call chains (depth > 1)
    print('\nChecking for call chains...')
    chains = con.execute(f"""
        SELECT COUNT(*)
        FROM read_parquet('{full_path}/calls/**/*.parquet') c1
        JOIN read_parquet('{full_path}/symbols/**/*.parquet') s1
            ON c1.CalleeId = s1.SymbolId
        JOIN read_parquet('{full_path}/calls/**/*.parquet') c2
            ON s1.SymbolId = c2.CallerId
    """).fetchone()[0]
    
    print(f'Call chains (A→B→C): {chains:,}')
    if chains > 0:
        print('✓ Call chains exist! Can build depth ≥2 graphs')
    else:
        print('⚠ No chains found - still flat architecture')
else:
    print('\n✗ No matches found')
