#!/usr/bin/env python3
import duckdb
import networkx as nx

con = duckdb.connect()
path = 'data/parquet/verify_run/run_20260120151424/stage_1'

# Load symbols and calls
symbols = con.execute(f"SELECT SymbolId, Name FROM read_parquet('{path}/symbols/**/*.parquet')").fetchdf()
calls = con.execute(f"""
    SELECT CallerId, CalleeId
    FROM read_parquet('{path}/calls/**/*.parquet')
    WHERE CallerId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
      AND CalleeId IN (SELECT SymbolId FROM read_parquet('{path}/symbols/**/*.parquet'))
""").fetchdf()

symbol_names = dict(zip(symbols['SymbolId'], symbols['Name']))

G = nx.DiGraph()
G.add_edges_from(zip(calls['CallerId'], calls['CalleeId']))

print(f'Total nodes in graph: {G.number_of_nodes():,}')

# Find entries and compute reachable nodes
entries = [n for n in G.nodes() if G.in_degree(n) == 0]
print(f'Entry points: {len(entries):,}')

reachable = set()
for entry in entries:
    reachable.update(nx.descendants(G, entry))
    reachable.add(entry)

print(f'Reachable from entries: {len(reachable):,}')
print(f'Missing nodes: {G.number_of_nodes() - len(reachable):,}')

unreachable = set(G.nodes()) - reachable
if unreachable:
    print(f'\nUnreachable nodes (likely cycles):')
    for node_id in list(unreachable)[:15]:
        name = symbol_names.get(node_id, '<unknown>')
        in_deg = G.in_degree(node_id)
        out_deg = G.out_degree(node_id)
        print(f'  {name[:60]} (in={in_deg}, out={out_deg})')
    
    # Check if they form cycles
    print(f'\nChecking for cycles among unreachable nodes...')
    unreachable_subgraph = G.subgraph(unreachable)
    try:
        cycles = list(nx.simple_cycles(unreachable_subgraph))
        if cycles:
            print(f'Found {len(cycles)} cycles')
            for i, cycle in enumerate(cycles[:3], 1):
                print(f'\nCycle {i} ({len(cycle)} nodes):')
                for node_id in cycle[:5]:
                    name = symbol_names.get(node_id, '<unknown>')
                    print(f'  → {name[:60]}')
                if len(cycle) > 5:
                    print(f'  ... and {len(cycle) - 5} more')
        else:
            print('No cycles found among unreachable nodes')
    except Exception as e:
        print(f'Error checking cycles: {e}')
