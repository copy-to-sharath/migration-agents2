#!/usr/bin/env python3
import duckdb
import os
import networkx as nx
from collections import defaultdict

con = duckdb.connect()
path = 'data/parquet/verify_run'

# Find the run directory
runs = [d for d in os.listdir(path) if d.startswith('run_')]
latest = sorted(runs)[-1]
full_path = f'{path}/{latest}/stage_1'

print(f'Analyzing: {full_path}\n')

# Load data efficiently
print('Loading symbols...')
symbols = con.execute(f"""
    SELECT SymbolId, Name
    FROM read_parquet('{full_path}/symbols/**/*.parquet')
""").fetchdf()
symbol_names = dict(zip(symbols['SymbolId'], symbols['Name']))
print(f'Loaded {len(symbol_names):,} symbols')

print('Loading calls...')
calls = con.execute(f"""
    SELECT CallerId, CalleeId
    FROM read_parquet('{full_path}/calls/**/*.parquet')
    WHERE CallerId IN (SELECT SymbolId FROM read_parquet('{full_path}/symbols/**/*.parquet'))
      AND CalleeId IN (SELECT SymbolId FROM read_parquet('{full_path}/symbols/**/*.parquet'))
""").fetchdf()
print(f'Loaded {len(calls):,} in-source calls')

# Build graph
print('Building graph...')
G = nx.DiGraph()
G.add_edges_from(zip(calls['CallerId'], calls['CalleeId']))
print(f'Graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges')

# Find entry points (no incoming edges)
entries = [n for n in G.nodes() if G.in_degree(n) == 0]
print(f'Entry points: {len(entries):,}')

# Compute longest paths from each entry
print('\nComputing depths...')
max_depth = 0
max_path = []
depth_dist = defaultdict(int)

for i, entry in enumerate(entries):
    if i % 100 == 0:
        print(f'  Processing entry {i}/{len(entries)}...', end='\r')
    
    # BFS to find longest path from this entry
    lengths = nx.single_source_shortest_path_length(G, entry)
    for node, depth in lengths.items():
        depth_dist[depth] += 1
        if depth > max_depth:
            max_depth = depth
            # Get one path of this length
            max_path = nx.shortest_path(G, entry, node)

print(f'\nMaximum call depth: {max_depth}')
print(f'\nDepth distribution:')
for d in sorted(depth_dist.keys())[:10]:
    print(f'  Depth {d}: {depth_dist[d]:,} nodes')

if max_path:
    print(f'\nExample longest path (depth {max_depth}):')
    path_names = [symbol_names.get(nid, f'<{nid[:8]}>')[:50] for nid in max_path]
    if len(path_names) > 10:
        print('  ' + ' → '.join(path_names[:3]))
        print('  ...')
        print('  ' + ' → '.join(path_names[-3:]))
    else:
        print('  ' + ' → '.join(path_names))
