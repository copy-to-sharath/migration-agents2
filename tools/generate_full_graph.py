#!/usr/bin/env python3
import duckdb
import networkx as nx
import os

con = duckdb.connect()
path = 'data/parquet/verify_run/run_20260120151424/stage_1'

print('Loading data...')

# Load symbols
symbols = con.execute(f"""
    SELECT SymbolId, Name, FilePath
    FROM read_parquet('{path}/symbols/**/*.parquet')
""").fetchdf()
symbol_info = {row['SymbolId']: (row['Name'], row['FilePath']) for _, row in symbols.iterrows()}

# Load calls
calls = con.execute(f"""
    SELECT CallerId, CalleeId, COALESCE(line, 0) as line
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE CallerId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
      AND CalleeId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
""").fetchdf()

# Build graph with edge line info
G = nx.DiGraph()
for _, row in calls.iterrows():
    caller_id, callee_id, line = row['CallerId'], row['CalleeId'], row['line']
    if G.has_edge(caller_id, callee_id):
        if line < G[caller_id][callee_id].get('line', float('inf')):
            G[caller_id][callee_id]['line'] = line
    else:
        G.add_edge(caller_id, callee_id, line=line)

print(f'Full graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges')

# Compute PageRank
print('Computing PageRank...')
try:
    pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=500, tol=1e-06)
    print(f'Computed PageRank for {len(pagerank_scores):,} nodes')
except nx.PowerIterationFailedConvergence:
    print('Warning: PageRank did not converge, using partial results')
    pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=1000, tol=1e-04)

# Generate DOT file
output_dir = 'generated/graphs'
os.makedirs(output_dir, exist_ok=True)
output_file = f'{output_dir}/full_call_graph.dot'

print(f'\nGenerating DOT file: {output_file}')

with open(output_file, 'w') as f:
    f.write('digraph CallGraph {\n')
    f.write('  rankdir=TB;\n')
    f.write('  node [shape=box, style=filled, fillcolor=lightblue];\n')
    f.write('  edge [color=gray];\n\n')
    
    # Legend
    f.write('  subgraph cluster_legend {\n')
    f.write('    label="Legend";\n')
    f.write('    style=dashed;\n')
    f.write('    legend_node [label="Code Node", shape=box, style=filled, fillcolor=lightblue];\n')
    f.write('  }\n\n')
    
    # Add nodes with labels
    for node_id in G.nodes():
        name, filepath = symbol_info.get(node_id, ('<unknown>', ''))
        # Shorten name and escape quotes
        short_name = name[:50].replace('"', '\\"')
        short_path = filepath.split('/')[-1] if '/' in filepath else filepath
        pr = pagerank_scores.get(node_id, 0.0)
        label = f'{short_name}\\n{short_path}\\nPR: {pr:.6f}'
        
        # Use short ID for node name
        node_name = node_id[:8]
        f.write(f'  "{node_name}" [label="{label}"];\n')
    
    f.write('\n')
    
    # Add edges with sequence numbers
    from collections import defaultdict
    edges_by_source = defaultdict(list)
    for caller_id, callee_id in G.edges():
        line = G[caller_id][callee_id].get('line', 0)
        edges_by_source[caller_id].append((callee_id, line))
    
    for caller_id, callees in edges_by_source.items():
        callees.sort(key=lambda x: x[1])
        caller_name = caller_id[:8]
        for seq, (callee_id, line) in enumerate(callees, start=1):
            callee_name = callee_id[:8]
            f.write(f'  "{caller_name}" -> "{callee_name}" [label="{seq}"];\n')
    
    f.write('}\n')

print(f'✓ DOT file created: {output_file}')
print(f'\nGenerating SVG (this may take a while for {G.number_of_nodes():,} nodes)...')

# Try to render with dot
import subprocess
svg_file = f'{output_dir}/full_call_graph.svg'
try:
    result = subprocess.run(
        ['dot', '-Tsvg', output_file, '-o', svg_file],
        capture_output=True,
        timeout=300  # 5 minutes max
    )
    if result.returncode == 0:
        print(f'✓ SVG created: {svg_file}')
        
        # Get file size
        size_mb = os.path.getsize(svg_file) / (1024 * 1024)
        print(f'  File size: {size_mb:.2f} MB')
    else:
        print(f'✗ Graphviz error: {result.stderr.decode()}')
except FileNotFoundError:
    print('✗ Graphviz not installed. Install with: brew install graphviz')
except subprocess.TimeoutExpired:
    print('✗ Rendering timed out (graph too large)')
except Exception as e:
    print(f'✗ Error: {e}')

print(f'\nFiles created:')
print(f'  DOT: {output_file}')
if os.path.exists(svg_file):
    print(f'  SVG: {svg_file}')
