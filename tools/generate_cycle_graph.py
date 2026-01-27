#!/usr/bin/env python3
import duckdb
import networkx as nx
import os

con = duckdb.connect()
path = 'data/parquet/verify_run/run_20260120151424/stage_1'

# Load symbols and calls
symbols = con.execute(f"SELECT SymbolId, Name, FilePath FROM read_parquet('{path}/symbols/**/*.parquet')").fetchdf()
calls = con.execute(f"""
    SELECT CallerId, CalleeId
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE CallerId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
      AND CalleeId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
""").fetchdf()

symbol_info = {row['SymbolId']: (row['Name'], row['FilePath']) for _, row in symbols.iterrows()}

G = nx.DiGraph()
G.add_edges_from(zip(calls['CallerId'], calls['CalleeId']))

# Compute PageRank
print('Computing PageRank...')
try:
    pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=500, tol=1e-06)
    print(f'Computed PageRank for {len(pagerank_scores):,} nodes')
except nx.PowerIterationFailedConvergence:
    print('Warning: PageRank did not converge, using partial results')
    pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=1000, tol=1e-04)

# Find unreachable (cycle) nodes
entries = [n for n in G.nodes() if G.in_degree(n) == 0]
reachable = set()
for entry in entries:
    reachable.update(nx.descendants(G, entry))
    reachable.add(entry)

unreachable = set(G.nodes()) - reachable
print(f'Found {len(unreachable)} unreachable nodes (cycles)')

# Create graph for cycles
output_dir = 'generated/graphs/by_depth'
os.makedirs(output_dir, exist_ok=True)
dot_file = f'{output_dir}/depth_cycles.dot'
svg_file = f'{output_dir}/depth_cycles.svg'

with open(dot_file, 'w') as f:
    f.write('digraph CallGraph_Cycles {\n')
    f.write('  rankdir=LR;\n')
    f.write('  label="Self-Referencing Cycles (Unreachable)";\n')
    f.write('  labelloc=t;\n')
    f.write('  fontsize=20;\n\n')
    
    # Legend
    f.write('  subgraph cluster_legend {\n')
    f.write('    label="Legend";\n')
    f.write('    style=dashed;\n')
    f.write('    legend_cycle [label="Cycle Node", shape=box, style=filled, fillcolor=lightcoral];\n')
    f.write('  }\n\n')
    
    for node_id in unreachable:
        name, filepath = symbol_info.get(node_id, ('<unknown>', ''))
        short_name = name[:50].replace('"', '\\"')
        short_path = filepath.split('/')[-1] if '/' in filepath else filepath
        pr = pagerank_scores.get(node_id, 0.0)
        label = f'{short_name}\\n{short_path}\\nPR: {pr:.6f}'
        node_name = node_id[:8]
        
        # Red for cycles
        f.write(f'  "{node_name}" [label="{label}", shape=box, style=filled, fillcolor=lightcoral];\n')
    
    f.write('\n')
    
    # Add self-referencing edges
    for node_id in unreachable:
        node_name = node_id[:8]
        # Check if it has a self-loop
        if G.has_edge(node_id, node_id):
            f.write(f'  "{node_name}" -> "{node_name}" [color=red, penwidth=2];\n')
    
    f.write('}\n')

import subprocess
result = subprocess.run(['dot', '-Tsvg', dot_file, '-o', svg_file], capture_output=True)
if result.returncode == 0:
    size_kb = os.path.getsize(svg_file) / 1024
    print(f'✓ Created: {svg_file} ({size_kb:.1f} KB)')
else:
    print(f'✗ Error: {result.stderr.decode()}')
