#!/usr/bin/env python3
import duckdb
import networkx as nx

con = duckdb.connect()
path = 'data/parquet/verify_run/run_20260120151424/stage_1'

print('Loading data...\n')

# Load symbols with PageRank if it exists
try:
    symbols = con.execute(f"""
        SELECT SymbolId, Name, FilePath, PageRank
        FROM read_parquet('{path}/symbols/**/*.parquet')
    """).fetchdf()
    has_pagerank = True
except:
    symbols = con.execute(f"""
        SELECT SymbolId, Name, FilePath
        FROM read_parquet('{path}/symbols/**/*.parquet')
    """).fetchdf()
    has_pagerank = False

symbol_info = {row['SymbolId']: row for _, row in symbols.iterrows()}

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

print(f'Found {len(depth_6_paths)} depth-6 chains\n')
print('='*80)

for i, path in enumerate(depth_6_paths, 1):
    print(f'\nChain {i}:')
    for j, node_id in enumerate(path):
        info = symbol_info.get(node_id)
        if info is not None:
            name = info['Name']
            filepath = info['FilePath']
            pagerank = info.get('PageRank', None) if has_pagerank else None
            
            short_path = filepath.split('/')[-1] if '/' in filepath else filepath
            indent = '  ' * j
            arrow = '→ ' if j > 0 else ''
            
            if pagerank is not None:
                print(f'{indent}{arrow}{name} (PageRank: {pagerank:.6f})')
            else:
                print(f'{indent}{arrow}{name} (PageRank: not computed)')
            print(f'{indent}   {short_path}')
        else:
            print(f'{indent}→ <unknown>')

if not has_pagerank:
    print('\n' + '='*80)
    print('PageRank not found in symbols. Computing now...\n')
    
    # Compute PageRank
    pagerank = nx.pagerank(G, max_iter=100)
    
    print('Top nodes by PageRank in depth-6 chains:')
    chain_nodes = set()
    for path in depth_6_paths:
        chain_nodes.update(path)
    
    chain_pageranks = [(node, pagerank.get(node, 0.0)) for node in chain_nodes]
    chain_pageranks.sort(key=lambda x: x[1], reverse=True)
    
    for node_id, pr in chain_pageranks[:10]:
        info = symbol_info.get(node_id)
        name = info['Name'] if info is not None else '<unknown>'
        print(f'  {name}: {pr:.6f}')
