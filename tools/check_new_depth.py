#!/usr/bin/env python3
import duckdb
import networkx as nx
from collections import defaultdict

con = duckdb.connect()
path = 'data/parquet/run_20260120155302/stage_1'

print('Loading symbols and calls...')

# Load symbols
symbols = con.execute(f"SELECT symbol_id, name FROM read_parquet('{path}/symbols/**/*.parquet')").fetchdf()
symbol_names = dict(zip(symbols['symbol_id'], symbols['name']))
print(f'Loaded {len(symbol_names):,} symbols')

# Load calls (need to match column names)
calls = con.execute(f"""
    SELECT caller_id, callee_id
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE caller_id IN (SELECT symbol_id FROM read_parquet('{path}/symbols/**/*.parquet'))
      AND callee_id IN (SELECT symbol_id FROM read_parquet('{path}/symbols/**/*.parquet'))
""").fetchdf()
print(f'Loaded {len(calls):,} in-source calls')

# Build graph
G = nx.DiGraph()
G.add_edges_from(zip(calls['caller_id'], calls['callee_id']))
print(f'Graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges')

# Find entry points
entries = [n for n in G.nodes() if G.in_degree(n) == 0]
print(f'Entry points: {len(entries):,}')

# Compute depths
print('\nComputing depths...')
max_depth = 0
max_path = []
depth_dist = defaultdict(int)

for i, entry in enumerate(entries):
    if i % 100 == 0:
        print(f'  Processing entry {i}/{len(entries)}...', end='\r')
    
    lengths = nx.single_source_shortest_path_length(G, entry)
    for node, depth in lengths.items():
        depth_dist[depth] += 1
        if depth > max_depth:
            max_depth = depth
            max_path = nx.shortest_path(G, entry, node)

print(f'\nMaximum call depth: {max_depth}')
print(f'\nDepth distribution:')
for d in sorted(depth_dist.keys())[:15]:
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
