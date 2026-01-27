#!/usr/bin/env python3
"""
Build and export the complete call graph with ASPX edges.
"""
import os
import duckdb
import networkx as nx
import json
from pathlib import Path

con = duckdb.connect()
run_id = "run_20260120155302"
path = f'data/parquet/{run_id}/stage_1'

print('Building call graph...\n')

# Load all edges
print('1. Loading C# edges...')
cs_edges = con.execute(f"""
    SELECT DISTINCT 
        caller_id as from_id, 
        callee_id as to_id,
        file_path,
        line
    FROM read_parquet('{path}/calls/**/*.parquet')
""").fetchdf()
print(f"   Loaded {len(cs_edges)} C# edges")

print('2. Loading ASPX edges...')
aspx_edges = con.execute(f"""
    SELECT DISTINCT 
        from_id, 
        to_id,
        edge_type
    FROM read_parquet('{path}/aspx_edges/**/*.parquet')
""").fetchdf()
print(f"   Loaded {len(aspx_edges)} ASPX edges")

# Load symbols for node metadata
print('3. Loading symbols...')
symbols = con.execute(f"""
    SELECT 
        symbol_id,
        name,
        kind,
        file_path,
        line
    FROM read_parquet('{path}/symbols/**/*.parquet')
""").fetchdf()
print(f"   Loaded {len(symbols)} symbols")

# Build NetworkX graph
print('4. Building NetworkX graph...')
G = nx.DiGraph()

# Add C# edges and track file_path/line for nodes
for _, row in cs_edges.iterrows():
    G.add_edge(row['from_id'], row['to_id'], 
               edge_type='call',
               file_path=row['file_path'],
               line=row['line'])
    # Add file_path to both caller and callee if not already set
    if row['from_id'] not in G.nodes or 'file_path' not in G.nodes[row['from_id']]:
        G.add_node(row['from_id'], file_path=row['file_path'])
    if row['to_id'] not in G.nodes or 'file_path' not in G.nodes[row['to_id']]:
        G.add_node(row['to_id'], file_path=row['file_path'])

# Add ASPX edges
for _, row in aspx_edges.iterrows():
    G.add_edge(row['from_id'], row['to_id'],
               edge_type=row.get('edge_type', 'aspx_handler'))

# Add node attributes from symbols (handle duplicates by keeping first)
symbols_dedup = symbols.drop_duplicates(subset=['symbol_id'], keep='first')
symbol_dict = symbols_dedup.set_index('symbol_id').to_dict('index')
for node in G.nodes():
    if node in symbol_dict:
        G.nodes[node].update(symbol_dict[node])

print(f"   Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Calculate PageRank
print('\n5. Calculating PageRank...')
pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=100)
print(f"   Computed PageRank for {len(pagerank_scores)} nodes")

# Add PageRank to node attributes
for node, score in pagerank_scores.items():
    G.nodes[node]['pagerank'] = score

# Find top nodes by PageRank
top_pagerank = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:20]
print(f"   Top 5 nodes by PageRank:")
for i, (node_id, score) in enumerate(top_pagerank[:5]):
    node_data = G.nodes.get(node_id, {})
    name = node_data.get('name', node_data.get('file_path', node_id[:8]))
    if name and '/' in str(name):
        name = os.path.basename(name)
    print(f"      {i+1}. {name}: {score:.6f}")

# Find deepest paths
print('\n6. Finding deepest paths...')
# Find root nodes (no incoming edges)
root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
print(f"   Found {len(root_nodes)} root nodes")

# Find longest path from any root
max_depth = 0
deepest_path = []
deepest_root = None

for i, root in enumerate(root_nodes[:1000]):  # Limit to first 1000 roots for speed
    if i % 100 == 0:
        print(f"   Analyzing root {i}/1000...", end='\r')
    
    # DFS to find longest path from this root
    stack = [(root, [root])]
    while stack:
        node, path = stack.pop()
        if len(path) > max_depth:
            max_depth = len(path)
            deepest_path = path
            deepest_root = root
        
        if len(path) >= 20:  # Limit depth
            continue
            
        for neighbor in G.successors(node):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

print(f"\n   Deepest path: {max_depth} nodes")

# Export deepest path with details
print('\n7. Exporting deepest path...')
path_details = []
for i, node_id in enumerate(deepest_path):
    node_data = G.nodes.get(node_id, {})
    file_path = node_data.get('file_path', 'unknown')
    # Use file name as fallback if no name is present
    if 'name' in node_data:
        name = node_data['name']
    elif file_path != 'unknown':
        name = file_path.split('/')[-1]
    else:
        name = node_id[:8]
    kind = node_data.get('kind', 'unknown')
    line = node_data.get('line', 0)
    
    # Get edge info to next node
    edge_info = ""
    if i < len(deepest_path) - 1:
        next_node = deepest_path[i + 1]
        edge_data = G.edges.get((node_id, next_node), {})
        edge_type = edge_data.get('edge_type', 'call')
        edge_info = f" --[{edge_type}]--> "
    
    path_details.append({
        'depth': i,
        'node_id': node_id,
        'name': name,
        'kind': kind,
        'file': file_path.split('/')[-1],
        'line': line,
        'edge_to_next': edge_info
    })

print(f"\n{'='*80}")
print(f"DEEPEST PATH (depth={max_depth})")
print('='*80)
for item in path_details:
    print(f"[{item['depth']:2d}] {item['name']:40s} ({item['kind']:15s}) {item['file']}:{item['line']}")
    if item['edge_to_next']:
        print(f"     {item['edge_to_next']}")

# Export graph
print(f"\n{'='*80}")
print('7. Exporting graph...')

output_dir = Path('data/graphs')
output_dir.mkdir(exist_ok=True)

# Export as GraphML
graphml_path = output_dir / f'{run_id}_with_aspx.graphml'
nx.write_graphml(G, graphml_path)
print(f"   ✓ GraphML: {graphml_path}")

# Export as JSON
json_path = output_dir / f'{run_id}_with_aspx.json'
graph_json = nx.node_link_data(G)
with open(json_path, 'w') as f:
    json.dump(graph_json, f, indent=2)
print(f"   ✓ JSON: {json_path}")

# Export as DOT
dot_path = output_dir / f'{run_id}_with_aspx.dot'
try:
    # Create a copy with cleaned attributes for DOT export
    G_dot = G.copy()
    # Set labels for all nodes
    for node in G_dot.nodes():
        node_data = G_dot.nodes[node]
        if 'name' in node_data:
            # Has a name from symbols table
            G_dot.nodes[node]['label'] = node_data['name']
            del G_dot.nodes[node]['name']
        else:
            # Orphan node - use file name
            file_path = node_data.get('file_path', 'unknown')
            if file_path != 'unknown':
                G_dot.nodes[node]['label'] = file_path.split('/')[-1]
            else:
                G_dot.nodes[node]['label'] = node[:8]
    
    nx.drawing.nx_pydot.write_dot(G_dot, dot_path)
    print(f"   ✓ DOT: {dot_path}")
    
    # Also export deepest path as separate DOT
    path_subgraph = G_dot.subgraph(deepest_path)
    dot_path_subgraph = output_dir / f'{run_id}_deepest_path.dot'
    nx.drawing.nx_pydot.write_dot(path_subgraph, dot_path_subgraph)
    print(f"   ✓ DOT (deepest path): {dot_path_subgraph}")
    
except ImportError:
    print(f"   ⚠ DOT export requires pydot (pip install pydot)")
except Exception as e:
    print(f"   ⚠ DOT export failed: {e}")

# Export deepest path as JSON
path_json_path = output_dir / f'{run_id}_deepest_path.json'
with open(path_json_path, 'w') as f:
    json.dump(path_details, f, indent=2)
print(f"   ✓ Path JSON: {path_json_path}")

# Export PageRank data
pagerank_data = []
for node_id, score in top_pagerank[:100]:  # Top 100 nodes
    node_data = G.nodes.get(node_id, {})
    pagerank_data.append({
        'node_id': node_id,
        'pagerank': score,
        'name': node_data.get('name', ''),
        'file_path': node_data.get('file_path', ''),
        'kind': node_data.get('kind', ''),
        'line': node_data.get('line', 0),
        'in_degree': G.in_degree(node_id),
        'out_degree': G.out_degree(node_id)
    })

pagerank_json_path = output_dir / f'{run_id}_pagerank.json'
with open(pagerank_json_path, 'w') as f:
    json.dump(pagerank_data, f, indent=2)
print(f"   ✓ PageRank JSON: {pagerank_json_path}")

# Generate depth-based graphs
print('\n9. Generating depth-based graphs...')
depth_output_dir = Path('generated/graphs/by_depth')
depth_output_dir.mkdir(parents=True, exist_ok=True)

# Calculate depth for all nodes
node_depths = {}
for root in root_nodes:
    stack = [(root, 0)]
    visited = set()
    while stack:
        node, depth = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        
        # Update depth if this is deeper than previously recorded
        if node not in node_depths or depth < node_depths[node]:
            node_depths[node] = depth
        
        for neighbor in G.successors(node):
            if neighbor not in visited:
                stack.append((neighbor, depth + 1))

# Mark nodes with no computed depth (cycles or disconnected)
for node in G.nodes():
    if node not in node_depths:
        node_depths[node] = -1

# Group nodes by depth
from collections import defaultdict
depth_groups = defaultdict(list)
for node, depth in node_depths.items():
    depth_groups[depth].append(node)

print(f"   Found {len(depth_groups)} depth levels")

# Track which nodes have already been exported at earlier depths
exported_nodes = set()

# Export each depth level
for depth in sorted(depth_groups.keys()):
    # Skip depth 0 only
    if depth == 0:
        continue
        
    nodes_at_depth = depth_groups[depth]
    if depth == -1:
        depth_name = "cycles"
    else:
        depth_name = str(depth)
    
    # Create depth subdirectory
    depth_dir = depth_output_dir / f'depth_{depth_name}'
    depth_dir.mkdir(parents=True, exist_ok=True)
    
    # Find nodes at current depth that have BOTH entry and exit
    # AND have not been exported at earlier depths
    entry_exit_nodes = []
    for node in nodes_at_depth:
        if node in exported_nodes:
            continue  # Skip nodes already exported at earlier depths
        has_entry = G.in_degree(node) > 0
        has_exit = G.out_degree(node) > 0
        if has_entry and has_exit:
            entry_exit_nodes.append(node)
    
    if not entry_exit_nodes:
        print(f"   Depth {depth_name}: No nodes with both entry and exit")
        continue
    
    print(f"   Depth {depth_name}: {len(entry_exit_nodes)} nodes with entry and exit")
    
    # Generate separate graph for each entry-exit node
    for idx, entry_node in enumerate(entry_exit_nodes):
        # Mark this node as exported
        exported_nodes.add(entry_node)
        
        # Get node info for filename
        node_data = G.nodes.get(entry_node, {})
        entry_node_name = node_data.get('name', None)
        if not entry_node_name:
            entry_node_name = node_data.get('file_path', entry_node)
            # Use basename if it's a file path
            if entry_node_name and '/' in entry_node_name:
                entry_node_name = os.path.basename(entry_node_name)
        
        # Find all root nodes that can reach this entry_node
        def find_roots_for_node(target_node, target_depth):
            """Find all root nodes (depth 0) that can reach the target"""
            roots = set()
            
            def trace_to_roots(node, current_depth):
                if current_depth == 0:
                    roots.add(node)
                    return
                
                for predecessor in G.predecessors(node):
                    pred_depth = node_depths.get(predecessor, -1)
                    if pred_depth == current_depth - 1:
                        trace_to_roots(predecessor, current_depth - 1)
            
            trace_to_roots(target_node, target_depth)
            return roots
        
        # Get all roots that reach this node
        reaching_roots = find_roots_for_node(entry_node, depth)
        
        if not reaching_roots:
            continue
        
        # Generate a separate graph for each root path
        for root_idx, root_node in enumerate(reaching_roots):
            nodes_to_include = set()
            edges_to_include = []
            
            # Trace back from entry_node to this specific root
            def trace_back_to_specific_root(node, current_depth, target_root):
                """Trace back to a specific root node only"""
                if current_depth == 0:
                    if node == target_root:
                        return True
                    return False
                
                for predecessor in G.predecessors(node):
                    pred_depth = node_depths.get(predecessor, -1)
                    if pred_depth == current_depth - 1:
                        if trace_back_to_specific_root(predecessor, current_depth - 1, target_root):
                            nodes_to_include.add(predecessor)
                            nodes_to_include.add(node)
                            edges_to_include.append((predecessor, node))
                            return True
                return False
            
            # Start tracing from entry_node to this specific root
            nodes_to_include.add(entry_node)
            found_path = trace_back_to_specific_root(entry_node, depth, root_node)
            
            if not found_path or not edges_to_include:
                continue
            
            # Create subgraph
            subgraph = G.edge_subgraph(edges_to_include)
            
            # Create a copy with labels and visual attributes
            G_depth = subgraph.copy()
            for node in G_depth.nodes():
                node_data = G_depth.nodes[node]
                
                # Set label with PageRank
                pagerank = node_data.get('pagerank', 0.0)
                if 'name' in node_data:
                    label = node_data['name']
                    del G_depth.nodes[node]['name']
                else:
                    file_path = node_data.get('file_path', 'unknown')
                    if file_path != 'unknown':
                        label = file_path.split('/')[-1]
                    else:
                        label = node[:8]
                
                G_depth.nodes[node]['label'] = f"{label}\\nPR:{pagerank:.6f}"
                
                # Determine node type based on edges in the full graph
                has_entry = G.in_degree(node) > 0
                has_exit = G.out_degree(node) > 0
                
                # Set visual attributes based on entry/exit status
                if has_entry and has_exit:
                    # Both entry and exit
                    G_depth.nodes[node]['shape'] = 'box'
                    G_depth.nodes[node]['color'] = 'blue'
                    G_depth.nodes[node]['style'] = 'filled'
                    G_depth.nodes[node]['fillcolor'] = 'lightblue'
                elif has_entry and not has_exit:
                    # Exit point (leaf node)
                    G_depth.nodes[node]['shape'] = 'octagon'
                    G_depth.nodes[node]['color'] = 'red'
                    G_depth.nodes[node]['style'] = 'filled'
                    G_depth.nodes[node]['fillcolor'] = 'lightcoral'
                elif not has_entry and has_exit:
                    # Entry point (root node)
                    G_depth.nodes[node]['shape'] = 'hexagon'
                    G_depth.nodes[node]['color'] = 'green'
                    G_depth.nodes[node]['style'] = 'filled'
                    G_depth.nodes[node]['fillcolor'] = 'lightgreen'
                else:
                    # Isolated node
                    G_depth.nodes[node]['shape'] = 'circle'
                    G_depth.nodes[node]['color'] = 'gray'
            
            # Create safe filename from node name or hash (with root identifier)
            safe_name = entry_node_name[:50] if entry_node_name and entry_node_name != entry_node else entry_node[:8]
            safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in safe_name)
            
            # Add root identifier to filename
            root_name = G.nodes[root_node].get('file_path', root_node)
            if root_name:
                root_name = os.path.basename(root_name).replace('.', '_')[:30]
            else:
                root_name = root_node[:8]
            safe_root = "".join(c if c.isalnum() or c in "-_." else "_" for c in root_name)
            
            output_filename = f"{safe_name}_from_{safe_root}"
            
            # Add legend nodes to the graph
            G_depth.add_node('legend_entry', label='Entry Point', shape='hexagon', color='green', style='filled', fillcolor='lightgreen')
            G_depth.add_node('legend_exit', label='Exit Point', shape='octagon', color='red', style='filled', fillcolor='lightcoral')
            G_depth.add_node('legend_intermediate', label='Intermediate', shape='box', color='blue', style='filled', fillcolor='lightblue')
            G_depth.add_node('legend_isolated', label='Isolated', shape='circle', color='gray', style='filled', fillcolor='lightgray')
            
            # Export DOT
            dot_path = depth_dir / f'{output_filename}.dot'
            try:
                nx.drawing.nx_pydot.write_dot(G_depth, dot_path)
            except Exception as e:
                print(f"      ⚠ Export failed for {output_filename}: {e}")


# Basic statistics
print(f"\n{'='*80}")
print('GRAPH STATISTICS')
print('='*80)
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.6f}")
print(f"Strongly connected components: {nx.number_strongly_connected_components(G)}")
print(f"Weakly connected components: {nx.number_weakly_connected_components(G)}")
print(f"Root nodes (in-degree=0): {len(root_nodes)}")
print(f"Leaf nodes (out-degree=0): {len([n for n in G.nodes() if G.out_degree(n) == 0])}")
print(f"Max depth found: {max_depth}")
print('='*80)
