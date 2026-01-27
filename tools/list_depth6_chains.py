#!/usr/bin/env python3
import duckdb
import networkx as nx

con = duckdb.connect()
path = 'data/parquet/verify_run/run_20260120151424/stage_1'

print('Finding all depth-6 call chains...\n')

# Load symbols
symbols = con.execute(f"""
    SELECT SymbolId, Name, FilePath
    FROM read_parquet('{path}/symbols/**/*.parquet')
""").fetchdf()
symbol_info = {row['SymbolId']: (row['Name'], row['FilePath']) for _, row in symbols.iterrows()}

# Load calls
calls = con.execute(f"""
    SELECT CallerId, CalleeId
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE CallerId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
      AND CalleeId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
""").fetchdf()

# Build graph
G = nx.DiGraph()
G.add_edges_from(zip(calls['CallerId'], calls['CalleeId']))

# Find entry points
entries = [n for n in G.nodes() if G.in_degree(n) == 0]

# Find all paths of depth 6
depth_6_paths = []
for entry in entries:
    lengths = nx.single_source_shortest_path_length(G, entry)
    for node, depth in lengths.items():
        if depth == 6:
            path = nx.shortest_path(G, entry, node)
            depth_6_paths.append(path)

print(f'Found {len(depth_6_paths)} call chains with depth 6\n')
print('='*80)

for i, path in enumerate(depth_6_paths, 1):
    print(f'\nChain {i}:')
    for j, node_id in enumerate(path):
        name, filepath = symbol_info.get(node_id, ('<unknown>', '<unknown>'))
        # Shorten file path
        short_path = filepath.split('/')[-1] if '/' in filepath else filepath
        indent = '  ' * j
        arrow = '→ ' if j > 0 else ''
        print(f'{indent}{arrow}{name}')
        print(f'{indent}   ({short_path})')
