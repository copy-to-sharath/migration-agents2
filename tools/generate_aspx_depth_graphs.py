#!/usr/bin/env python3
import duckdb
import networkx as nx
import os
import subprocess
from collections import defaultdict

con = duckdb.connect()
path = 'data/parquet/run_20260120155302/stage_1'

print('Loading data...')

# Load symbols
symbols = con.execute(f"""
    SELECT symbol_id, name, file_path
    FROM read_parquet('{path}/symbols/**/*.parquet')
""").fetchdf()
symbol_info = {row['symbol_id']: (row['name'], row['file_path']) for _, row in symbols.iterrows()}

# Load calls
calls = con.execute(f"""
    SELECT caller_id, callee_id, COALESCE(line, 0) as line
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE caller_id IN (SELECT symbol_id FROM read_parquet('{path}/symbols/**/*.parquet'))
      AND callee_id IN (SELECT symbol_id FROM read_parquet('{path}/symbols/**/*.parquet'))
""").fetchdf()

# Build graph with edge line info
G = nx.DiGraph()
for _, row in calls.iterrows():
    caller_id, callee_id, line = row['caller_id'], row['callee_id'], row['line']
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

# Find entry points and compute depths
print('\nComputing depths from entry points...')
entries = [n for n in G.nodes() if G.in_degree(n) == 0]
print(f'Entry points: {len(entries):,}')

# Compute depth for each node
node_depths = {}
for entry in entries:
    lengths = nx.single_source_shortest_path_length(G, entry)
    for node, depth in lengths.items():
        if node not in node_depths or depth < node_depths[node]:
            node_depths[node] = depth

# Find unreachable nodes (cycles)
all_reachable = set(node_depths.keys())
unreachable = set(G.nodes()) - all_reachable
if unreachable:
    for node in unreachable:
        node_depths[node] = -1

# Group nodes by depth
depth_groups = defaultdict(list)
for node, depth in node_depths.items():
    depth_groups[depth].append(node)

print('\nDepth distribution:')
for depth in sorted(depth_groups.keys()):
    print(f'  Depth {depth}: {len(depth_groups[depth]):,} nodes')

# Create graphs for each depth level
output_dir = 'generated/graphs/aspx_depth'
os.makedirs(output_dir, exist_ok=True)

print(f'\nGenerating graphs for each depth level...')

for depth in sorted(depth_groups.keys()):
    if depth == -1:
        continue  # Skip cycles for now
        
    nodes_at_depth = set(depth_groups[depth])
    
    # Create subgraph with edges from this depth
    subgraph_edges = []
    for caller, callee in G.edges():
        caller_depth = node_depths.get(caller)
        if caller_depth == depth:
            subgraph_edges.append((caller, callee))
    
    if not subgraph_edges:
        print(f'  Depth {depth}: {len(nodes_at_depth):,} nodes, 0 edges (skipping)')
        continue
    
    subgraph = nx.DiGraph(subgraph_edges)
    
    # Generate DOT file
    dot_file = f'{output_dir}/depth_{depth}.dot'
    svg_file = f'{output_dir}/depth_{depth}.svg'
    
    with open(dot_file, 'w') as f:
        f.write(f'digraph CallGraph_Depth_{depth} {{\n')
        f.write('  rankdir=TB;\n')
        f.write('  label="Call Graph - Depth ' + str(depth) + ' (with ASPX/ASCX)";\n')
        f.write('  labelloc=t;\n')
        f.write('  fontsize=20;\n\n')
        
        # Legend
        f.write('  subgraph cluster_legend {\n')
        f.write('    label="Legend";\n')
        f.write('    style=dashed;\n')
        f.write('    legend_current [label="Current Depth", shape=box, style=filled, fillcolor=lightblue];\n')
        f.write('    legend_next [label="Next Depth (Callee)", shape=box, style=filled, fillcolor=lightgreen];\n')
        f.write('  }\n\n')
        
        # Style nodes
        for node_id in subgraph.nodes():
            name, filepath = symbol_info.get(node_id, ('<unknown>', ''))
            short_name = name[:50].replace('"', '\\"')
            short_path = filepath.split('/')[-1] if '/' in filepath else filepath
            pr = pagerank_scores.get(node_id, 0.0)
            label = f'{short_name}\\n{short_path}\\nPR: {pr:.6f}'
            node_name = node_id[:8]
            
            node_depth = node_depths.get(node_id, -1)
            if node_depth == depth:
                # Current depth - blue
                f.write(f'  "{node_name}" [label="{label}", shape=box, style=filled, fillcolor=lightblue];\n')
            else:
                # Next depth - green
                f.write(f'  "{node_name}" [label="{label}", shape=box, style=filled, fillcolor=lightgreen];\n')
        
        f.write('\n')
        
        # Add edges with sequence numbers
        from collections import defaultdict
        edges_by_source = defaultdict(list)
        for caller_id, callee_id in subgraph.edges():
            line = subgraph[caller_id][callee_id].get('line', 0)
            edges_by_source[caller_id].append((callee_id, line))
        
        for caller_id, callees in edges_by_source.items():
            callees.sort(key=lambda x: x[1])
            caller_name = caller_id[:8]
            for seq, (callee_id, line) in enumerate(callees, start=1):
                callee_name = callee_id[:8]
                f.write(f'  "{caller_name}" -> "{callee_name}" [label="{seq}"];\n')
        
        f.write('}\n')
    
    # Render SVG
    try:
        result = subprocess.run(
            ['dot', '-Tsvg', dot_file, '-o', svg_file],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            size_kb = os.path.getsize(svg_file) / 1024
            print(f'  Depth {depth}: {len(nodes_at_depth):,} nodes (blue), {len(subgraph.edges()):,} edges → {svg_file} ({size_kb:.1f} KB)')
        else:
            print(f'  Depth {depth}: ✗ Graphviz error')
    except Exception as e:
        print(f'  Depth {depth}: ✗ Error: {e}')

print(f'\n✓ All graphs saved to: {output_dir}/')
print(f'\nBlue nodes = at this depth level')
print(f'Green nodes = called from this depth (next level)')
