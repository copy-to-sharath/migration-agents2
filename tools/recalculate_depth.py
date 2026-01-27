#!/usr/bin/env python3
"""
Recalculate graph depth with ASPX edges included.
"""
import duckdb
from collections import defaultdict, deque

con = duckdb.connect()
run_id = "run_20260120155302"
path = f'data/parquet/{run_id}/stage_1'

print('Loading call graph edges...\n')

# Load original C# call edges
print('1. Loading C# call edges...')
cs_edges = con.execute(f"""
    SELECT DISTINCT caller_id as from_id, callee_id as to_id
    FROM read_parquet('{path}/calls/**/*.parquet')
""").fetchdf()
print(f"   Loaded {len(cs_edges)} C# edges")

# Load ASPX edges
print('2. Loading ASPX->C# edges...')
aspx_edges = con.execute(f"""
    SELECT DISTINCT from_id, to_id
    FROM read_parquet('{path}/aspx_edges/**/*.parquet')
""").fetchdf()
print(f"   Loaded {len(aspx_edges)} ASPX edges")

# Combine
print('3. Building combined adjacency list...')
adjacency = defaultdict(list)
for _, row in cs_edges.iterrows():
    adjacency[row['from_id']].append(row['to_id'])
for _, row in aspx_edges.iterrows():
    adjacency[row['from_id']].append(row['to_id'])

print(f"   Graph has {len(adjacency)} nodes")

# Load entry points - analyze from ALL potential entry points, not just ASPX
print('4. Loading entry points...')
# Get all nodes that have outbound edges but might be entry points
# Include: ASPX callers, and nodes with zero in-degree (potential root entries)
aspx_entry_nodes = set(aspx_edges['from_id'].unique())

# Calculate in-degrees to find root nodes
in_degrees = defaultdict(int)
for _, row in cs_edges.iterrows():
    in_degrees[row['to_id']] += 1
for _, row in aspx_edges.iterrows():
    in_degrees[row['to_id']] += 1

# Nodes that have outbound edges but no inbound edges (potential roots)
all_nodes_with_out_edges = set(cs_edges['from_id'].unique()) | set(aspx_edges['from_id'].unique())
root_nodes = {node for node in all_nodes_with_out_edges if in_degrees.get(node, 0) == 0}

# Combine ASPX entries with root nodes
entry_nodes = aspx_entry_nodes | root_nodes

print(f"   Found {len(aspx_entry_nodes)} ASPX entry nodes")
print(f"   Found {len(root_nodes)} root nodes (0 in-degree)")
print(f"   Total entry nodes to analyze: {len(entry_nodes)}")

# Create entry dataframe for analysis
entries_data = []
for node_id in entry_nodes:
    node_type = 'ASPX' if node_id in aspx_entry_nodes else 'ROOT'
    entries_data.append({'symbol_id': node_id, 'name': f'{node_type}_{node_id[:8]}'})

import pandas as pd
entries = pd.DataFrame(entries_data)

# Calculate depth for each entry using DFS with path tracking
print('5. Calculating depths (finding longest paths)...')
depths = {}
for idx, row in entries.iterrows():
    if idx % 100 == 0:
        print(f"   Processing entry {idx}/{len(entries)}...", end='\r')
    
    entry_id = row['symbol_id']
    max_depth = 0
    # Use DFS with path tracking to find longest path (not shortest)
    stack = [(entry_id, 0, {entry_id})]
    
    while stack:
        node, depth, path = stack.pop()
        max_depth = max(max_depth, depth)
        
        if depth >= 50:  # Prevent infinite depth
            continue
            
        for neighbor in adjacency.get(node, []):
            if neighbor not in path:  # Only check current path, not global visited
                stack.append((neighbor, depth + 1, path | {neighbor}))
    
    depths[entry_id] = max_depth

print(f"\n\n{'='*60}")
print("DEPTH ANALYSIS")
print('='*60)

# Summary statistics
depth_values = list(depths.values())
print(f"Total entries analyzed: {len(depth_values)}")
print(f"Max depth: {max(depth_values)}")
print(f"Min depth: {min(depth_values)}")
print(f"Average depth: {sum(depth_values)/len(depth_values):.2f}")

# Distribution
print("\nDepth Distribution:")
depth_counts = defaultdict(int)
for d in depth_values:
    depth_counts[d] += 1

for depth in sorted(depth_counts.keys()):
    count = depth_counts[depth]
    pct = (count / len(depth_values)) * 100
    bar = '█' * int(pct / 2)
    print(f"  Depth {depth:2d}: {count:4d} entries ({pct:5.1f}%) {bar}")

# Show some deep entries
print("\nDeepest entries:")
sorted_entries = sorted(depths.items(), key=lambda x: x[1], reverse=True)
for entry_id, depth in sorted_entries[:10]:
    entry_match = entries[entries['symbol_id'] == entry_id]
    if len(entry_match) > 0:
        entry_info = entry_match.iloc[0]
        print(f"  Depth {depth}: {entry_info['name']}")

print(f"\n{'='*60}")
