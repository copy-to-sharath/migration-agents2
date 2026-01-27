#!/usr/bin/env python3
"""
Check if nodes appear in multiple depth_groups (they shouldn't!)
"""
import duckdb
import networkx as nx
from collections import defaultdict

con = duckdb.connect()
run_id = "run_20260120155302"
path = f'data/parquet/{run_id}/stage_1'

print('Loading graph data...')

# Load edges
cs_edges = con.execute(f"""
    SELECT DISTINCT 
        caller_id as from_id, 
        callee_id as to_id,
        caller_file_path as caller_file,
        callee_file_path as callee_file
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE caller_id IS NOT NULL AND callee_id IS NOT NULL
""").fetchall()

aspx_edges = con.execute(f"""
    SELECT DISTINCT 
        aspx_file_id as from_id,
        codebehind_symbol_id as to_id,
        aspx_file_path as caller_file,
        codebehind_file_path as callee_file
    FROM read_parquet('{path}/aspx_edges/**/*.parquet')
    WHERE aspx_file_id IS NOT NULL AND codebehind_symbol_id IS NOT NULL
""").fetchall()

print(f'Loaded {len(cs_edges)} C# edges, {len(aspx_edges)} ASPX edges')

# Build graph
G = nx.DiGraph()
for from_id, to_id, from_file, to_file in cs_edges + aspx_edges:
    G.add_edge(from_id, to_id)
    if from_file:
        G.nodes[from_id]['file_path'] = from_file
    if to_file:
        G.nodes[to_id]['file_path'] = to_file

print(f'Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges')

# Calculate depths
root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
print(f'Found {len(root_nodes)} root nodes')

node_depths = {}
for root in root_nodes:
    stack = [(root, 0)]
    visited = set()
    while stack:
        node, depth = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        
        # Update depth if this is shorter than previously recorded
        if node not in node_depths or depth < node_depths[node]:
            node_depths[node] = depth
        
        for neighbor in G.successors(node):
            if neighbor not in visited:
                stack.append((neighbor, depth + 1))

# Mark nodes with no depth
for node in G.nodes():
    if node not in node_depths:
        node_depths[node] = -1

# Group by depth
depth_groups = defaultdict(list)
for node, depth in node_depths.items():
    depth_groups[depth].append(node)

print(f'\nDepth distribution:')
for depth in sorted(depth_groups.keys()):
    print(f'  Depth {depth}: {len(depth_groups[depth])} nodes')

# Check if any node appears in multiple groups (should be impossible!)
node_depth_count = defaultdict(int)
for depth, nodes in depth_groups.items():
    for node in nodes:
        node_depth_count[node] += 1

duplicates = {node: count for node, count in node_depth_count.items() if count > 1}
if duplicates:
    print(f'\n❌ ERROR: {len(duplicates)} nodes appear in multiple depth groups!')
    for node, count in list(duplicates.items())[:10]:
        print(f'  {node}: appears {count} times')
else:
    print('\n✓ Each node appears in exactly one depth group')

# Now check specific problematic nodes
problem_nodes = ['Reference.cs', 'BindData', 'Settings.Designer.cs']
print(f'\nChecking specific nodes that appear in multiple depth DIRECTORIES:')
for pnode_name in problem_nodes:
    # Find nodes with this basename in file_path
    matching_nodes = []
    for node in G.nodes():
        fp = G.nodes[node].get('file_path', '')
        if fp and fp.endswith(pnode_name):
            matching_nodes.append((node, node_depths.get(node, -999)))
    
    if matching_nodes:
        print(f'\n  "{pnode_name}":')
        for node_id, depth in matching_nodes[:5]:
            print(f'    Node {node_id[:16]}: depth={depth}, file={G.nodes[node_id].get("file_path", "?")}')
