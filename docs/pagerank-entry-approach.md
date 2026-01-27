# PageRank Entry/Exit Approach

This document explains how we use PageRank to select entry points and rank exits,
including the math used in the Domain Architect stage.

## Graph Model

We build a directed graph `G = (V, E)` from code artifacts:

- **Nodes** (`V`):
  - `symbol`: a defined function/method/class from parser outputs.
  - `callsite`: synthetic caller node when the caller symbol is missing.
  - `callee`: synthetic callee node when the callee symbol is missing.
  - `sql_site`: a symbol that executes a data-access query (SQL, ORM, etc).
  - `data_asset`: a generic target for data access (table, view, stored procedure,
    DB function, ORM entity, queue, in-memory store). Current implementation uses
    `table` as the concrete `data_asset` kind until generalized.
- **Edges** (`E`):
  - `call`: caller → callee
  - `data_access`: SQL site → table

Each node has a stable `node_id`. Edges use `from_id` and `to_id`.

## PageRank Definition

Let `N = |V|`. PageRank is a stationary distribution over nodes:

```
PR(v) = (1 - d)/N + d * sum_{u in In(v)} PR(u) / OutDegree(u)
```

Where:
- `d` is the damping factor (default 0.85 in NetworkX).
- `In(v)` are nodes that point to `v`.
- `OutDegree(u)` is the number of outgoing edges from `u`.

We compute PageRank for all nodes in the graph using `nx.pagerank` with a
personalization vector derived from node-type weights.

Personalization weights are applied per node type:

```
p(v) = weight(node_type(v)) / sum_{u in V} weight(node_type(u))
```

This biases rank toward specific node types (e.g., data access sites).

## Entry Selection (per slice)

We map nodes to slices and select one entry node per slice.

**Default rule** (`entry_filter = pagerank_non_sink`):

1. Candidate nodes are those with `out_degree > 0` (non‑sinks).
2. Pick the node with max PageRank:

```
entry(slice) = argmax_{v in candidates} PR(v)
```

**Strict rule** (`entry_filter = in_degree_zero`):

1. Candidate nodes have `in_degree = 0` and `out_degree > 0`.
2. Pick the node with max PageRank among these.

This yields a stable entry even when explicit endpoints are missing.

## Recursion Handling

We detect recursive nodes using strongly connected components (SCCs):

- Any SCC with more than one node is recursive.
- Any node with a self‑edge is recursive.

When `exclude_recursive_entries=true`, recursive nodes are removed from entry
candidate sets before PageRank selection. This avoids picking a recursive
loop as a primary entry point.

## Exit Selection (per endpoint)

We traverse the graph from the entry to compute reachable nodes, then filter exits.

**Default rule** (`exit_filter = table_nodes`):

```
exit_candidates = { v | v is a table node }
```

Alternative rules:
- `out_degree_zero`: nodes with no outgoing edges
- `table_or_sink`: union of table nodes and sinks

Exit candidates are ranked by PageRank:

```
ranked_exits = sort(exit_candidates, key=PR, descending=True)
```

## Context Scoring (PageRank + Vector)

For each slice or context group:

- `pagerank_score` = average PageRank of nodes in the group.
- `vector_score` is derived from vector cluster presence.
- `graph_score` is derived from graph cluster presence.
- `coverage_score` measures evidence density.
