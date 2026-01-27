#!/usr/bin/env python3
"""
Generate separate DOT graphs for each entry point, organized by depth level.

Requirements:
- Each graph has ONE entry and may have multiple exits (all shown)
- Depth 1 and above are included
- No node appears in multiple graphs (no duplicates)
- Deeper levels are processed first, so shallower levels don't contain subset data

Outputs to: generated/graphs/entries_by_depth/depth_N/entry_HASH.dot
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set, List, Tuple

import duckdb
import networkx as nx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate entry graphs by depth level (deepest first, no duplicates)'
    )
    parser.add_argument(
        '--run-id',
        type=str,
        help='Run ID to use. Defaults to latest.'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='generated/graphs/entries_by_depth',
        help='Output directory for graphs'
    )
    parser.add_argument(
        '--parquet-root',
        type=Path,
        default=Path('data/parquet'),
        help='Root directory for parquet files'
    )
    parser.add_argument(
        '--max-entries-per-depth',
        type=int,
        default=10000,
        help='Maximum entries to render per depth level (default: 10000)'
    )
    parser.add_argument(
        '--min-depth',
        type=int,
        default=2,
        help='Minimum depth to include (default: 2, skips shallow graphs)'
    )
    return parser.parse_args()


def load_run_id(run_id: str | None, parquet_root: Path) -> str:
    if run_id:
        return run_id
    latest_run_file = parquet_root / 'LATEST_RUN'
    if latest_run_file.exists():
        return latest_run_file.read_text().strip()
    run_dirs = sorted([d for d in parquet_root.iterdir() if d.name.startswith('run_')])
    if not run_dirs:
        print('Error: No run directories found', file=sys.stderr)
        sys.exit(1)
    return run_dirs[-1].name


def compute_reachable(G: nx.DiGraph, entry: str) -> Set[str]:
    """Compute all nodes reachable from entry."""
    reachable = set()
    stack = [entry]
    while stack:
        node = stack.pop()
        if node in reachable:
            continue
        reachable.add(node)
        for neighbor in G.successors(node):
            if neighbor not in reachable:
                stack.append(neighbor)
    return reachable


def compute_max_depth(G: nx.DiGraph, entry: str, max_limit: int = 100) -> int:
    """Compute max depth from entry using BFS."""
    max_depth = 0
    visited = {entry: 0}
    queue = [(entry, 0)]
    while queue:
        node, depth = queue.pop(0)
        if depth > max_depth:
            max_depth = depth
        if depth >= max_limit:
            continue
        for neighbor in G.successors(node):
            if neighbor not in visited:
                visited[neighbor] = depth + 1
                queue.append((neighbor, depth + 1))
    return max_depth


def find_all_exits(G: nx.DiGraph, reachable: Set[str]) -> List[str]:
    """Find all exit nodes in the subgraph (nodes with no successors in reachable set)."""
    exits = []
    for node in reachable:
        successors_in_subgraph = [s for s in G.successors(node) if s in reachable]
        if not successors_in_subgraph:
            exits.append(node)
    return exits


def escape_label(text: str, max_len: int = 35) -> str:
    """Escape text for DOT labels - compact version."""
    if text is None:
        return ''
    text = str(text).replace('"', '\\"').replace('\n', ' ').replace('\\', '/')
    # Truncate long labels
    if len(text) > max_len:
        return text[:max_len-2] + '..'
    return text


def generate_entry_dot(
    G: nx.DiGraph,
    entry: str,
    exits: List[str],
    reachable: Set[str],
    node_info: Dict[str, tuple],
    pagerank_scores: Dict[str, float],
    max_depth: int,
    output_path: str
) -> None:
    """Generate DOT file for a single entry's subgraph - clean and simple."""
    edges_in_subgraph = []
    for node in reachable:
        for succ in G.successors(node):
            if succ in reachable:
                line = G[node][succ].get('line', 0)
                edges_in_subgraph.append((node, succ, line))
    
    exits_set = set(exits)
    node_index = {node_id: i for i, node_id in enumerate(reachable)}
    
    def resolve_label(node_id: str) -> str:
        """Resolve a readable label for a node. For callee nodes, try to find context."""
        info = node_info.get(node_id, ('', 'unknown', ''))
        raw_label = info[0] if info[0] else ''
        node_type = info[1] if info[1] else 'unknown'
        source_ref = info[2] if info[2] else ''
        
        # Get filename from source_ref
        if source_ref:
            parts = str(source_ref).replace('\\', '/').split('/')
            filename = parts[-1].split(':')[0] if parts else ''
        else:
            filename = ''
        
        # Check if label is a hash (64 hex chars)
        is_hash = len(raw_label) == 64 and raw_label.isalnum()
        
        if not is_hash and raw_label:
            # Good label - use it with filename
            method_name = escape_label(raw_label)
            if filename:
                return f'{method_name}\\n{filename}'
            return method_name
        
        # Label is a hash - try to resolve via successors (what this node calls)
        if node_type == 'callee':
            # First try successors
            successors = list(G.successors(node_id))
            for succ in successors:
                succ_info = node_info.get(succ, ('', '', ''))
                succ_label = succ_info[0] if succ_info[0] else ''
                if succ_label and not (len(succ_label) == 64 and succ_label.isalnum()):
                    if filename:
                        return f'-> {escape_label(succ_label)}\\n{filename}'
                    return f'-> {escape_label(succ_label)}'
            
            # No successors - try predecessors to show context
            predecessors = list(G.predecessors(node_id))
            for pred in predecessors:
                pred_info = node_info.get(pred, ('', '', ''))
                pred_label = pred_info[0] if pred_info[0] else ''
                if pred_label and not (len(pred_label) == 64 and pred_label.isalnum()):
                    if filename:
                        return f'{escape_label(pred_label)} (call)\\n{filename}'
                    return f'{escape_label(pred_label)} (call)'
        
        # Fallback to filename
        if filename:
            return filename
        return f'node_{node_index[node_id]}'
    
    with open(output_path, 'w') as f:
        entry_label = escape_label(node_info.get(entry, (entry[:20], '', ''))[0])
        f.write(f'digraph Entry_{entry[:8]} {{\n')
        # Graph settings for compact single-page view
        f.write('  rankdir=LR;\n')  # Left-to-right for horizontal flow
        f.write('  splines=curved;\n')  # Curved edges for readability
        f.write('  nodesep=0.3;\n')  # Tighter vertical spacing
        f.write('  ranksep=0.5;\n')  # Tighter horizontal spacing
        f.write('  margin=0.2;\n')  # Smaller margins
        f.write('  fontname="Helvetica";\n')
        f.write('  fontsize=12;\n')
        f.write('  bgcolor="white";\n')
        f.write(f'  label="Entry: {entry_label} | Depth: {max_depth} | Nodes: {len(reachable)} | Exits: {len(exits)}";\n')
        f.write('  labelloc=t;\n\n')
        
        # Default node and edge styles - compact
        f.write('  node [fontname="Helvetica", fontsize=8, shape=box, style="filled,rounded", penwidth=1, margin="0.1,0.05", height=0.3];\n')
        f.write('  edge [fontname="Helvetica", fontsize=7, color="#888888", penwidth=1, arrowsize=0.6];\n\n')
        
        # Compact inline legend
        f.write('  subgraph cluster_legend {\n')
        f.write('    label="";\n')
        f.write('    style=invis;\n')  # Invisible border
        f.write('    rank=min;\n')
        f.write('    legend_entry [label="Entry", fillcolor="#ff9500", fontcolor="white", fontsize=7, height=0.2];\n')
        f.write('    legend_exit [label="Exit", fillcolor="#ff6b6b", fontcolor="white", fontsize=7, height=0.2];\n')
        f.write('    legend_node [label="Node", fillcolor="#74b9ff", fontsize=7, height=0.2];\n')
        f.write('    legend_entry -> legend_exit -> legend_node [style=invis];\n')
        f.write('  }\n\n')
        
        for node_id in reachable:
            label_text = resolve_label(node_id)
            pr = pagerank_scores.get(node_id, 0.0)
            
            # Compact label - only show PR if very significant
            if pr >= 0.01:
                label_with_pr = f'{label_text}\\n[{pr:.2f}]'
            else:
                label_with_pr = label_text
            
            node_name = f'n{node_index[node_id]}'
            
            # Modern colors with proper font colors
            if node_id == entry:
                fillcolor = '#ff9500'
                fontcolor = 'white'
            elif node_id in exits_set:
                fillcolor = '#ff6b6b'
                fontcolor = 'white'
            else:
                fillcolor = '#74b9ff'
                fontcolor = 'black'
            
            f.write(f'  "{node_name}" [label="{label_with_pr}", fillcolor="{fillcolor}", fontcolor="{fontcolor}"];\n')
        
        f.write('\n')
        
        # Edges with sequence numbers
        from collections import defaultdict
        edges_by_source = defaultdict(list)
        for from_id, to_id, line in edges_in_subgraph:
            edges_by_source[from_id].append((to_id, line))
        
        for from_id, callees in edges_by_source.items():
            callees.sort(key=lambda x: x[1])
            for seq, (to_id, line) in enumerate(callees, start=1):
                f.write(f'  "n{node_index[from_id]}" -> "n{node_index[to_id]}";\n')
        
        f.write('}\n')


def main() -> None:
    args = parse_args()
    
    con = duckdb.connect()
    run_id = load_run_id(args.run_id, args.parquet_root)
    path = f'{args.parquet_root}/{run_id}/stage_1'
    
    print(f'Using run: {run_id}')
    print('Loading data...')
    
    # Load nodes
    nodes = con.execute(f"""
        SELECT node_id, label, node_type, source_ref
        FROM read_parquet('{path}/code_graph_nodes/**/*.parquet')
    """).fetchdf()
    node_info = {row['node_id']: (row['label'], row['node_type'], row['source_ref']) 
                 for _, row in nodes.iterrows()}
    print(f'Loaded {len(nodes):,} nodes')
    
    # Load edges
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
    
    # Compute PageRank
    print('Computing PageRank...')
    try:
        pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=500, tol=1e-06)
        print(f'Computed PageRank for {len(pagerank_scores):,} nodes')
    except nx.PowerIterationFailedConvergence:
        print('Warning: PageRank did not converge, using partial results')
        pagerank_scores = nx.pagerank(G, alpha=0.85, max_iter=1000, tol=1e-04)
    
    # Find entry points (in-degree = 0, out-degree > 0)
    entries = [n for n in G.nodes() if G.in_degree(n) == 0 and G.out_degree(n) > 0]
    print(f'Entry points: {len(entries):,}')
    
    # Compute depth for each entry
    print('\nComputing entry depths...')
    # Each item: (entry, depth, reachable_nodes, exits)
    all_entries: List[Tuple[str, int, Set[str], List[str]]] = []
    
    single_exit_count = 0
    multi_exit_count = 0
    
    for i, entry in enumerate(entries):
        if i % 500 == 0:
            print(f'  Processing {i}/{len(entries)}...')
        
        reachable = compute_reachable(G, entry)
        exits = find_all_exits(G, reachable)
        
        if len(exits) == 0:
            continue
        
        max_depth = compute_max_depth(G, entry)
        if max_depth < args.min_depth:
            continue
        
        if len(exits) == 1:
            single_exit_count += 1
        else:
            multi_exit_count += 1
        
        all_entries.append((entry, max_depth, reachable, exits))
    
    print(f'\nEntry analysis:')
    print(f'  Single exit entries: {single_exit_count}')
    print(f'  Multi exit entries: {multi_exit_count}')
    print(f'  Total valid entries: {len(all_entries)}')
    
    # Sort by depth DESCENDING (deepest first), then by size descending
    all_entries.sort(key=lambda x: (-x[1], -len(x[2])))
    
    # Group by depth - no node-based filtering, just ensure each entry is unique
    # Nodes CAN appear in multiple graphs at different depths (same code called from multiple places)
    by_depth: Dict[int, List[Tuple[str, Set[str], List[str]]]] = defaultdict(list)
    
    for entry, depth, reachable, exits in all_entries:
        by_depth[depth].append((entry, reachable, exits))
    
    print(f'\nGrouped by depth:')
    total_valid = sum(len(v) for v in by_depth.values())
    print(f'  Total graphs: {total_valid}')
    for depth in sorted(by_depth.keys(), reverse=True):
        print(f'  Depth {depth}: {len(by_depth[depth])} graphs')
    
    # Create output directories and generate DOT files
    output_dir = Path(args.output_dir)
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    
    print(f'\nGenerating entry graphs to {output_dir}...')
    total_written = 0
    
    for depth in sorted(by_depth.keys()):
        depth_dir = output_dir / f'depth_{depth}'
        depth_dir.mkdir(parents=True, exist_ok=True)
        
        entries_at_depth = by_depth[depth][:args.max_entries_per_depth]
        
        for entry, reachable, exits in entries_at_depth:
            info = node_info.get(entry, ('', '', ''))
            label = info[0] if info[0] else entry[:20]
            safe_label = ''.join(c if c.isalnum() or c in '_-' else '_' for c in str(label)[:30])
            filename = f'{safe_label}_{entry[:8]}.dot'
            
            dot_path = depth_dir / filename
            generate_entry_dot(G, entry, exits, reachable, node_info, pagerank_scores, depth, str(dot_path))
            total_written += 1
        
        print(f'  Depth {depth}: {len(entries_at_depth)} graphs written')
    
    # Write summary
    summary_path = output_dir / 'summary.txt'
    with open(summary_path, 'w') as f:
        f.write(f'Run ID: {run_id}\n')
        f.write(f'Total entry points found: {len(entries):,}\n')
        f.write(f'Single exit entries: {single_exit_count}\n')
        f.write(f'Multi exit entries: {multi_exit_count}\n')
        f.write(f'After duplicate removal (deepest first): {total_valid}\n')
        f.write(f'Total graphs written: {total_written}\n\n')
        f.write('By depth:\n')
        for depth in sorted(by_depth.keys(), reverse=True):
            count = len(by_depth[depth])
            written = min(count, args.max_entries_per_depth)
            f.write(f'  Depth {depth}: {count} unique graphs, {written} written\n')
    
    print(f'\n✓ {total_written} entry graphs written to {output_dir}/')
    print(f'✓ Summary saved to {summary_path}')
    print('\nColor legend:')
    print('  Orange = Entry node')
    print('  Salmon = Exit node(s)')
    print('  Blue = Intermediate node')


if __name__ == '__main__':
    main()
