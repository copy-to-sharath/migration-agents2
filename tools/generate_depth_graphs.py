#!/usr/bin/env python3
"""
Generate DOT graphs by depth level.

Each depth level shows entry nodes (no predecessors at that depth) and
exit nodes (no successors at that or deeper depth).
"""
import argparse
import duckdb
import networkx as nx
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate call graphs by depth level')
    parser.add_argument('--run-id', type=str, help='Run ID to use (e.g., run_20260122130739). Defaults to latest.')
    parser.add_argument('--output-dir', type=str, default='generated/graphs/by_depth', help='Output directory for graphs')
    return parser.parse_args()


def get_run_id(run_id: str | None, parquet_root: Path) -> str:
    if run_id:
        return run_id
    latest_run_file = parquet_root / 'LATEST_RUN'
    if latest_run_file.exists():
        return latest_run_file.read_text().strip()
    run_dirs = sorted([d for d in parquet_root.iterdir() if d.name.startswith('run_')])
    if not run_dirs:
        print('Error: No run directories found in data/parquet/', file=sys.stderr)
        sys.exit(1)
    return run_dirs[-1].name


def find_entries_exits_at_depth(
    G: nx.DiGraph,
    node_depths: Dict[str, int],
    depth: int
) -> Tuple[Set[str], Set[str]]:
    """
    Find entry and exit nodes for a specific depth level.
    
    Entry: nodes at this depth with no incoming edges from same depth
    Exit: nodes at this depth with no outgoing edges to same or deeper depth
    """
    nodes_at_depth = {n for n, d in node_depths.items() if d == depth}
    
    entries = set()
    exits = set()
    
    for node in nodes_at_depth:
        # Check if entry: no predecessors at same depth
        preds_at_depth = [p for p in G.predecessors(node) if node_depths.get(p) == depth]
        if not preds_at_depth:
            entries.add(node)
        
        # Check if exit: no successors at same or deeper depth
        succs_deeper = [s for s in G.successors(node) if node_depths.get(s, -999) >= depth]
        if not succs_deeper:
            exits.add(node)
    
    return entries, exits


def main():
    args = parse_args()
    con = duckdb.connect()

    # Determine run_id
    parquet_root = Path('data/parquet')
    run_id = get_run_id(args.run_id, parquet_root)
    path = f'data/parquet/{run_id}/stage_1'
    print(f'Using run: {run_id}')

    print('Loading data...')

    # Load nodes from code_graph_nodes (complete graph)
    nodes = con.execute(f"""
        SELECT node_id, label, node_type, source_ref
        FROM read_parquet('{path}/code_graph_nodes/**/*.parquet')
    """).fetchdf()
    node_info = {row['node_id']: (row['label'], row['node_type'], row['source_ref']) for _, row in nodes.iterrows()}
    print(f'Loaded {len(nodes):,} nodes')

    # Load edges from code_graph_edges (complete graph)
    edges = con.execute(f"""
        SELECT from_id, to_id, COALESCE(line, 0) as line
        FROM read_parquet('{path}/code_graph_edges/**/*.parquet')
    """).fetchdf()
    print(f'Loaded {len(edges):,} edges')

    # Build graph with edge line info
    G = nx.DiGraph()
    for _, row in edges.iterrows():
        from_id, to_id, line = row['from_id'], row['to_id'], row['line']
        if G.has_edge(from_id, to_id):
            if line < G[from_id][to_id].get('line', float('inf')):
                G[from_id][to_id]['line'] = line
        else:
            G.add_edge(from_id, to_id, line=line)

    print(f'Full graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges')

    # Find entry points
    entries = [n for n in G.nodes() if G.in_degree(n) == 0]
    print(f'Entry points: {len(entries):,}')

    # Compute PageRank
    print('Computing PageRank...')
    try:
        pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=500, tol=1e-06)
        print(f'Computed PageRank for {len(pagerank_scores):,} nodes')
    except nx.PowerIterationFailedConvergence:
        print('Warning: PageRank did not converge, using partial results')
        pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=1000, tol=1e-04)

    # Compute depths from entries
    print('\nComputing depths from entry points...')
    node_depths = {}
    for entry in entries:
        lengths = nx.single_source_shortest_path_length(G, entry)
        for node, depth in lengths.items():
            if node not in node_depths or depth < node_depths[node]:
                node_depths[node] = depth

    # Find unreachable nodes (cycles, self-references)
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
        entries_at_depth, exits_at_depth = find_entries_exits_at_depth(G, node_depths, depth)
        print(f'  Depth {depth}: {len(depth_groups[depth]):,} nodes, {len(entries_at_depth)} entries, {len(exits_at_depth)} exits')

    # Create output directory
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    print(f'\nGenerating graphs for each depth level to {output_dir}...')

    for depth in sorted(depth_groups.keys()):
        nodes_at_depth = set(depth_groups[depth])
        
        # Find entries and exits at this depth
        entries_at_depth, exits_at_depth = find_entries_exits_at_depth(G, node_depths, depth)
        
        # Create subgraph with edges between nodes at this depth or to next depth
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
        
        with open(dot_file, 'w') as f:
            f.write(f'digraph CallGraph_Depth_{depth} {{\n')
            # Compact graph settings for single-page view
            f.write('  rankdir=LR;\n')  # Left-to-right
            f.write('  splines=curved;\n')
            f.write('  nodesep=0.3;\n')
            f.write('  ranksep=0.4;\n')
            f.write('  margin=0.2;\n')
            f.write('  fontname="Helvetica";\n')
            f.write('  fontsize=14;\n')
            f.write('  bgcolor="white";\n')
            title = f'Depth {depth} | Entries: {len(entries_at_depth)} | Exits: {len(exits_at_depth)}'
            f.write(f'  label="{title}";\n')
            f.write('  labelloc=t;\n\n')
            
            # Compact node and edge styles
            f.write('  node [fontname="Helvetica", fontsize=8, shape=box, style="filled,rounded", penwidth=1, margin="0.08,0.04", height=0.25];\n')
            f.write('  edge [fontname="Helvetica", fontsize=7, color="#888888", penwidth=1, arrowsize=0.5];\n\n')
            
            # Compact inline legend
            f.write('  subgraph cluster_legend {\n')
            f.write('    label="";\n')
            f.write('    style=invis;\n')
            f.write('    rank=min;\n')
            f.write('    legend_entry [label="Entry", fillcolor="#ff9500", fontcolor="white", fontsize=7, height=0.18];\n')
            f.write('    legend_exit [label="Exit", fillcolor="#ff6b6b", fontcolor="white", fontsize=7, height=0.18];\n')
            f.write('    legend_both [label="Both", fillcolor="#ffd93d", fontsize=7, height=0.18];\n')
            f.write('    legend_current [label="Current", fillcolor="#74b9ff", fontsize=7, height=0.18];\n')
            f.write('    legend_next [label="Next", fillcolor="#00b894", fontcolor="white", fontsize=7, height=0.18];\n')
            f.write('  }\n\n')
            
            # Style nodes by entry/exit/depth status
            for node_id in subgraph.nodes():
                info = node_info.get(node_id, (node_id[:20], 'unknown', ''))
                label_text = info[0] if info[0] else node_id[:20]
                node_type = info[1] if info[1] else 'unknown'
                source_ref = info[2] if info[2] else ''
                
                # Compact label - truncate hash IDs, keep readable names
                if len(label_text) == 64 and label_text.isalnum():
                    short_label = f'#{node_id[:6]}'
                else:
                    short_label = label_text[:30].replace('"', '\\"').replace('\n', ' ')
                    if len(label_text) > 30:
                        short_label += '..'
                
                short_ref = source_ref.split('/')[-1].split(':')[0][:20] if source_ref else ''
                pr = pagerank_scores.get(node_id, 0.0)
                
                # Compact label format - only show PR if significant
                if short_ref:
                    display_label = f'{short_label}\\n{short_ref}'
                else:
                    display_label = short_label
                if pr >= 0.01:
                    display_label += f' [{pr:.2f}]'
                
                node_name = node_id[:8]
                node_depth = node_depths.get(node_id, -1)
                
                # Determine color and font color based on entry/exit/depth
                if node_id in entries_at_depth and node_id in exits_at_depth:
                    fillcolor = '#ffd93d'
                    fontcolor = 'black'
                elif node_id in entries_at_depth:
                    fillcolor = '#ff9500'
                    fontcolor = 'white'
                elif node_id in exits_at_depth:
                    fillcolor = '#ff6b6b'
                    fontcolor = 'white'
                elif node_depth == depth:
                    fillcolor = '#74b9ff'
                    fontcolor = 'black'
                else:
                    fillcolor = '#00b894'
                    fontcolor = 'white'
                
                f.write(f'  "{node_name}" [label="{display_label}", fillcolor="{fillcolor}", fontcolor="{fontcolor}"];\n')
            
            f.write('\n')
            
            # Add edges with sequence numbers
            edges_by_source = defaultdict(list)
            for caller_id, callee_id in subgraph.edges():
                line = G[caller_id][callee_id].get('line', 0) if G.has_edge(caller_id, callee_id) else 0
                edges_by_source[caller_id].append((callee_id, line))
            
            for caller_id, callees in edges_by_source.items():
                callees.sort(key=lambda x: x[1])
                caller_name = caller_id[:8]
                for seq, (callee_id, line) in enumerate(callees, start=1):
                    callee_name = callee_id[:8]
                    f.write(f'  "{caller_name}" -> "{callee_name}";\n')
            
            f.write('}\n')
        
        print(f'  Depth {depth}: {len(nodes_at_depth):,} nodes, {len(entries_at_depth)} entries, {len(exits_at_depth)} exits → {dot_file}')

    # Write summary
    summary_file = f'{output_dir}/summary.txt'
    with open(summary_file, 'w') as f:
        f.write(f'Run ID: {run_id}\n')
        f.write(f'Total nodes: {G.number_of_nodes():,}\n')
        f.write(f'Total edges: {G.number_of_edges():,}\n')
        f.write(f'Entry points: {len(entries):,}\n\n')
        f.write('Depth distribution:\n')
        for depth in sorted(depth_groups.keys()):
            entries_at_depth, exits_at_depth = find_entries_exits_at_depth(G, node_depths, depth)
            f.write(f'  Depth {depth}: {len(depth_groups[depth]):,} nodes, {len(entries_at_depth)} entries, {len(exits_at_depth)} exits\n')

    print(f'\n✓ All DOT files saved to: {output_dir}/')
    print(f'✓ Summary saved to: {summary_file}')
    print('\nColor legend:')
    print('  Orange = Entry node (no predecessors at this depth)')
    print('  Salmon = Exit node (no successors at this or deeper depth)')
    print('  Yellow = Both entry and exit')
    print('  Blue = Regular node at current depth')
    print('  Green = Node at next depth (callee)')


if __name__ == '__main__':
    main()
