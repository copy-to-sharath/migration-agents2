#!/usr/bin/env python3
import duckdb

con = duckdb.connect()
path = 'data/parquet/verify_run/run_20260120151424/stage_1'

print('Call breakdown:\n')

total = con.execute(f"SELECT COUNT(*) FROM read_parquet('{path}/calls/**/*.parquet')").fetchone()[0]
print(f'Total calls: {total:,}')

in_source_callee = con.execute(f"""
    SELECT COUNT(*) 
    FROM read_parquet('{path}/calls/**/*.parquet') c
    JOIN read_parquet('{path}/symbols/**/*.parquet') s ON c.CalleeId = s.SymbolId
""").fetchone()[0]
print(f'Calls with in-source callee: {in_source_callee:,}')

both_in_source = con.execute(f"""
    SELECT COUNT(*) 
    FROM read_parquet('{path}/calls/**/*.parquet') c
    JOIN read_parquet('{path}/symbols/**/*.parquet') s1 ON c.CallerId = s1.SymbolId
    JOIN read_parquet('{path}/symbols/**/*.parquet') s2 ON c.CalleeId = s2.SymbolId
""").fetchone()[0]
print(f'Calls where BOTH are in-source: {both_in_source:,}')

print(f'\n{"="*60}')
print(f'Only {both_in_source:,} calls can form chains')
print(f'(both caller and callee must be tracked symbols)')
print(f'{"="*60}')
print(f'\nThis explains why max depth is only 6:')
print(f'- {total - in_source_callee:,} calls go to external libraries (dead ends)')
print(f'- {in_source_callee - both_in_source:,} calls FROM external code (no caller to chain from)')
print(f'- Only {both_in_source:,} ({both_in_source*100//total}%) can participate in depth calculations')
