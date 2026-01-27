#!/usr/bin/env python3
"""
Recalculate graph depth including ASPX edges.
"""
import duckdb
import networkx as nx
from collections import defaultdict

con = duckdb.connect()
run_id = "run_20260120155302"
path = f'data/parquet/{run_id}/stage_1'

print('Computing graph depth with ASPX edges...\n')

# Load all edges (original calls + ASPX links)
print('1. Loading original call edges...')
original_edges = con.execute(f"""
    SELECT DISTINCT caller_id as from_id, callee_id as to_id
    FROM read_parquet('{path}/calls/**/*.parquet')
""").fetchdf()
print(f"   Found {len(original_edges)} original call edges")

print('2. Loading ASPX event handler edges...')
aspx_edges = con.execute(f"""
    SELECT DISTINCT from_id, to_id
    FROM read_parquet('{path}/aspx_edges/**/*.parquet')
""").fetchdf()
print(f"   Found {len(aspx_edges)} ASPX edges")

# Combine edges
print('3. Combining edges...')
all_edges = original_edges.rename(columns={'caller_id': 'from_id', 'callee_id': 'to_id'}) if 'caller_id' in original_edges.columns else original_edges
combined_edges = duckdb.execute("""
    SELECT from_id, to_id FROM original_edges
    UNION
    SELECT from_id, to_id FROM aspx_edges
""").fetchdf()
print(f"   Total unique edges: {len(combined_edges)}")

# Load symbols for entry points
print('4. Loading entry points (Controller/Page methods)...')
entry_points = con.execute(f"""
    SELECT DISTINCT symbol_id, name, file_path
    FROM read_parquet('{path}/symbols/**/*.parquet')
    WHERE kind IN ('Method', 'method')
    AND (
        file_path LIKE '%Controller.cs'
        OR file_path LIKE '%.aspx.cs'
        OR file_path LIKE '%.ascx.cs'
    )
    AND (
        name LIKE 'Page_%'
        OR name LIKE 'btn%_Click'
        OR name LIKE '%_Click'
        OR signature LIKE '%ActionResult%'
        OR signature LIKE '%IActionResult%'
    )
""").fetchdf()
print(f"   Found {len(entry_points)} potential entry points")

# Build graph
print('5. Building directed graph...')
G = nx.DiGraph()
for _, row in combined_edges.iterrows():
    G.add_edge(row['from_id'], row['to_id'])
print(f"   Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Calculate depth from each entry point
print('6. Computing depths from entry points...')
depths = []
for _, entry in entry_points.iterrows():
    entry_id = entry['symbol_id']
    if entry_id not in G:
        continue
    
    # BFS to find max depth
    visited = {entry_id: 0}
    queue = [(entry_id, 0)]
    max_depth = 0
    
    while queue:
        node, depth = queue.pop(0)
        max_depth = max(max_depth, depth)
        
        if node in G:
            for neighbor in G.successors(node):
                if neighbor not in visited or visited[neighbor] < depth + 1:
                    visited[neighbor] = depth + 1
                    queue.append((neighbor, depth + 1))
    
    if max_depth > 0:
        depths.append({
            'entry_id': entry_id,
            'name': entry['name'],
            'file': entry['file_path'],
            'max_depth': max_depth,
            'reachable_nodes': len(visited)
        })

# Sort by depth
depths_sorted = sorted(depths, key=lambda x: x['max_depth'], reverse=True)

print(f"\n✓ Computed depths for {len(depths_sorted)} entry points")
print(f"\nTop 20 entry points by depth:")
print(f"{'Max Depth':<12} {'Reachable':<12} {'Entry Point':<40} {'File'}")
print("=" * 120)
for d in depths_sorted[:20]:
    file_short = d['file'].split('/')[-1]
    print(f"{d['max_depth']:<12} {d['reachable_nodes']:<12} {d['name']:<40} {file_short}")

overall_max = max((d['max_depth'] for d in depths_sorted), default=0)
print(f"\n📊 Overall maximum depth: {overall_max}")
