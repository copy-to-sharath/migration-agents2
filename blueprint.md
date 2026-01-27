# Autonomous Software Engineer for Legacy-to-Modern Transitions

Below is the missing depth on the "how" and the "why" across the four most critical layers.

## Agent Architecture

The pipeline is orchestrated by 3 agents defined in `.github/agents/`:

| Agent | Responsibility | MCP Tools |
|-------|----------------|-----------|
| **01-analyzer** | One-time setup (Steps 1-3): Ingest, Parse, Slice | `analyzer` (step: ingest/parse/slice) |
| **02-builder** | Per-slice code generation: Rules, Domain, Tests, Code | `builder_generate`, `builder_fix` |
| **03-judge** | Validation and fix loop: Build, Test, Citations, Coverage | `judge_validate` |

**Workflow:**
```
01-analyzer (one-time) → handoff → 02-builder ↔ 03-judge (fix loop per slice)
```

The agents use MCP tools exposed by `src/migration_agents/mcp/` for autonomous execution.
See `docs/mcp.md` for VS Code integration and auto-approve configuration.

## Current Implementation Status (as of this repo)

The following components are implemented in the codebase today:

- **Stage 0: Intake and Normalization (Ingestion)** — `src/migration_agents/ingestion/`
  - Scans source trees, computes checksums, extracts text (including PDF/DOCX),
    chunks content, and writes Parquet tables:
    `intake_source_index`, `intake_source_chunks`, `intake_build_context`,
    `intake_schema_snapshot`.
  - Incremental mode uses MCP-backed DuckDB queries to skip unchanged files.
- **Stage 1: Parser and Lakehouse Loader** — `src/migration_agents/parser/`
  - Tree-sitter parsing with per-language `.scm` queries and a coverage gate.
  - Optional Roslyn path (configurable) for C# / VB.NET / solution files.
  - Outputs Parquet tables:
    `symbols`, `calls`, `conditions`, `constants`, `data_access`, `parse_audit`.
  - Generates `coverage_summary` from the latest `parse_audit` run.
- **Stage 2: Graph Generation (Parser)** — `src/migration_agents/parser/`
  - Builds code graph nodes/edges, graph metrics, and entry/exit maps from
    parsed symbols/calls/data access.
  - Outputs Parquet tables:
    `code_graph_nodes`, `code_graph_edges`, `graph_metadata`, `entry_exit_map`.
- **Stage 3: Slice Extractor** — `src/migration_agents/slice_extractor/`
  - Groups graph nodes by community and emits slice manifests and context.
  - Outputs Parquet tables:
    `slice_manifest`, `slice_context`, `slice_source_refs`.
- **Stage 4: Logic Manifester** — `src/migration_agents/logic_manifester/`
  - Derives Logic Manifest rules with traceability from slice artifacts.
  - Outputs Parquet tables:
    `logic_rules`, `logic_edges`, `trace_map`.
- **Stage 5: Domain Architect** — `src/migration_agents/domain_architect/`
  - Derives entities, value objects, aggregates, and context maps from logic rules.
  - Outputs Parquet tables:
    `domain_entities`, `value_objects`, `aggregates`, `context_map`, `domain_insights`.
Infrastructure details are captured in the "Infrastructure (Implemented)" section below.

All later stages described below are planned and captured as the target pipeline,
but are not yet implemented in this repo.

## Infrastructure (Implemented)

Status: Implemented in this repo.

- **MCP DuckDB Server** — `src/migration_agents/mcp/`
  - Stdio JSON-RPC server that exposes DuckDB views over Parquet datasets.
  - `duckdb_query` tool and `resources/list` / `resources/read` endpoints.

## 1. The Graph + Context Extraction Layer

Note: The full context extraction layer is planned; current implementation covers
Stage 0 (Intake), Stage 1 (Parser), Stage 2 (Graph Generation), Stage 3 (Slice Extractor),
Stage 4 (Logic Manifester), and Stage 5 (Domain Architect).

Standard RAG (Retrieval-Augmented Generation) is not enough for legacy migration. You need GraphRAG.

- **Call Chain Tracing:** An agent must use NetworkX to map every "Entry Point" (Controller/Main) to its "Exit Point" (SQL/External API). If the AI doesn't know that Function A calls Function B which then updates Table C, it will hallucinate the business rule.
- **Feature Slicing:** Instead of migrating file-by-file, the agent extracts a Vertical Slice. It gathers all code across 50 files that contribute to "Calculate Loan Interest" and feeds it as a single context window to the LLM.
- **English Source of Truth:** The factory produces a Logic_Manifest.md. This is a human-readable "contract" that defines the logic found in the legacy code. It is the only thing used to generate the new code, ensuring no legacy "bugs" are accidentally ported over.

## 2. The Multi-Agent "Assembly Line"

Note: The agentic stages below are planned; the Parser, Graph Generation, Slice Extractor,
Logic Manifester, Domain Architect, and MCP foundations exist in code today.
Memory artifacts can now be loaded via the memory loader (memory_episodic,
memory_short_term, memory_long_term).

You aren't using one agent; you are orchestrating a team with distinct cognitive profiles:

- **The Parser (Python/DuckDB):** A specialized script (non-LLM) that turns the legacy code into a structured Parquet "Lakehouse." Use Python 3.13 with tree-sitter for language parsing and uv for package management. Use multiprocessing where applicable for parsing and indexing.
- **The Domain Architect:** Analyzes the legacy slice and defines the Bounded Contexts and Aggregates. It asks: "Is this a 'Loan' or is this a 'Payment'?"
- **The TDD Engineer:** It writes XUnit tests for the new .NET 8.0 logic before the code is even written. It uses the Logic_Manifest.md as its requirement.
- **The Implementer:** Writes the .NET 8.0 Clean Architecture code to make the tests pass.

## 3. The "Judge" & Self-Correction Loop

This is where most systems fail. Your factory must include a Compiler-in-the-Loop feedback system:

1) Agent generates .NET 8.0 code.  
2) System attempts to run `dotnet build`.  
3) Compiler error is fed back to a Fixer Agent.  
4) Unit tests are executed. If they fail, the Debugger Agent reads the stack trace and legacy spec to find the discrepancy.  
5) Iteration repeats until the AI Judge verifies the code matches the English Manifest and has 100% test coverage.

### Judge Policy (Single vs Multi-Judge)

- **MVP:** single Judge for speed and cost.
- **Production:** two-tier judges:
  - **Judge 1 (fast):** verifies build/lint/test status, citation completeness, schema compliance.
  - **Judge 2 (deep):** validates Logic_Manifest to code/test alignment and BRD traceability.
  - **Tie-breaker:** if judges disagree, run a third arbiter or require human review.

## 4. The .NET 8.0 "Gold Standard" Target

The factory is hard-coded to produce Clean Architecture. This prevents the new system from becoming the next "legacy monolith."

- **Domain Layer:** Contains rich Domain Models (not anemic ones). Logic like interest calculation is inside the Loan entity, not a "service."
- **Application Layer:** Uses MediatR for CQRS. This makes the system "side-effect free" and easy to scale.
- **Infrastructure Layer:** Uses EF Core 8 interceptors to automatically dispatch Domain Events (e.g., LoanApprovedEvent) to a message bus.

## Engineering Standards (Clean Code, Typing, Linting, Modularization)

All generated code must follow clean-code practices with strong typing, linting, and modular boundaries.

- **Typing:** Strict typing enabled for all languages and tools (e.g., C# nullable reference types, TypeScript strict mode, Python type hints with mypy).
- **Linting:** Enforce lint rules and formatting in CI (e.g., dotnet format, eslint/biome, ruff/black).
- **Modularization:** Clear module boundaries aligned to bounded contexts; no cross-layer leakage (Domain → Application → Infrastructure only).
- **Code quality gates:** Build, lint, and tests must pass before promotion to the next stage.

## Parallelism and Throughput

Use multiprocessing or parallel execution wherever applicable, especially for parsing, embedding generation, graph metric computation, and test execution. Parallelism must preserve determinism by isolating outputs per `run_id` and `artifact_version`.

## Endpoint Processing Rule

Agents must process one endpoint at a time (per run/slice), not all endpoints at once. Each agent must limit context to the current endpoint and its citations to avoid cross-contamination.

## Configuration Management

All code must use structured JSON configuration files (no hard-coded values). Config must be typed, validated, and loaded per `run_id` with environment overrides for paths, thresholds, and model settings.

## Agent System Prompts

Each agent must have a dedicated system prompt stored as Markdown in `.github/agents/`. These prompts define role responsibilities, required inputs (DuckDB views), required outputs (Parquet tables), and citation/versioning rules. All non-judge agents must consult judge reports and self-correct before finalizing outputs. MVP order of execution:

1) **Analyzer (Ingest + Parse + Slice)** — `.github/agents/01-analyzer.agent.md`
2) **Builder (Logic + Domain + TDD + Implementer + Fix)** — `.github/agents/02-builder.agent.md`
3) **Judge (Single)** — `.github/agents/03-judge.agent.md`

### Retry and Escalation Policy

- **Max retries:** 3 per stage.
- **Retry trigger:** Any judge report with errors, missing citations, or schema violations.
- **Escalation:** After 3 failed retries, halt the slice and require human review with a summary of gaps and suggested fixes.

## The "Factory Master" Dashboard

To manage this, you need a dashboard that shows:

- **Velocity:** How many "Functional Slices" are migrated per hour.
- **Quality Score:** The average "Judge" rating across the migrated modules.
- **Citations:** A clickable map where you can see a line of modern C# code and immediately see the original legacy code it replaced.

## Storage and Artifact Rule

All artifacts and all data must be stored as Parquet. DuckDB is the only supported query/read layer for those Parquet artifacts, and all DuckDB access must be performed via the MCP server. No ad-hoc JSON/CSV files are allowed for artifacts or handoffs. Any human-readable outputs (like Logic_Manifest.md) must be generated from DuckDB-backed Parquet and have a durable backing table.

All artifacts must include citations. Every table must carry a `source_ref` (or equivalent) column that points to the legacy evidence (file/line, SQL, API call, or prior artifact row) used to derive it.

The MCP server must expose queries to list all available endpoints and identify dead code. These outputs must be backed by Parquet and readable via DuckDB.

### Endpoint and Dead Code Catalog

- **Parquet tables:**
  - `endpoints` (endpoint_id, name, entry_point, route, method, symbol_id, entry_node_id, source_ref)
  - `endpoint_flows` (endpoint_id, flow_summary, exit_tables, path_steps, coverage_ratio, source_ref)
  - `endpoint_coverage` (coverage_id, covered_nodes, total_nodes, coverage_ratio, source_ref)
  - `dead_code` (symbol_id, file_path, line, reason, source_ref)
- **DuckDB views:**
  - `v_endpoints`
  - `v_dead_code`

## Versioning During Migration

Every artifact is versioned across pipeline iterations and slice revisions. Versioning is stored in Parquet and queried via DuckDB.

- **Version columns (required in all tables):**
  - `artifact_version` (integer, monotonic per slice)
  - `run_id` (pipeline execution id)
  - `slice_id` (logical feature slice id)
  - `created_at` (UTC timestamp)
  - `supersedes_version` (nullable int)
- **Mutation policy:**
  - No in-place updates. New versions append new rows/partitions.
  - Latest view is a DuckDB view filtering `artifact_version = max()` per `slice_id`.
- **Schema evolution:**
  - New columns are additive only; deprecations use `*_deprecated_at`.
  - Backfills are recorded as new `artifact_version` rows.

## Agent Memory (Episodic, Short-Term, Long-Term)

Agents must read and write memory artifacts from Parquet via DuckDB. Memory tables are Parquet datasets and must follow the global versioning rules. All memory is tied to `run_id` and `slice_id` when applicable.

- **Episodic memory (per run/step):**
  - `memory_episodic` (episode_id, run_id, slice_id, agent_id, event_type, summary, source_ref, created_at, artifact_version, supersedes_version)
- **Short-term memory (task window):**
  - `memory_short_term` (memory_id, run_id, slice_id, agent_id, key, value, confidence, created_at, artifact_version, supersedes_version)
- **Long-term memory (cross-run knowledge):**
  - `memory_long_term` (memory_id, domain, key, value, provenance, decay_score, created_at, artifact_version, supersedes_version)
- **DuckDB views:**
  - `v_memory_episodic`
  - `v_memory_short_term`
  - `v_memory_long_term`

All agents must consult episodic, short-term, and long-term memory before producing outputs, and must persist any new findings back to the appropriate memory table.

Retention and Decay Policies
- **Episodic:** retain by run for auditability; prune by age after export to long-term summary.
- **Short-term:** TTL-based expiry (e.g., 14-30 days) with automatic decay; keep only latest version per `run_id` and `slice_id`.
- **Long-term:** decay_score drives relevance; periodic recompute from usage frequency and recency.

## Step 2: Parquet-Only Pipeline Artifacts (DuckDB Read Layer)

Each stage writes Parquet tables and exposes DuckDB views for downstream agents.

## Mandatory Pre-Step: Ubiquitous Language and BDD Artifacts

Before any other pipeline steps, the system must establish a shared ubiquitous language and produce BDD artifacts. These are stored as Parquet and read via DuckDB.

- **Parquet tables:**
  - `ubiquitous_language_terms` (term_id, term, definition, synonyms, source_ref)
  - `bdd_features` (feature_id, slice_id, name, description)
  - `bdd_scenarios` (scenario_id, feature_id, title, narrative, priority)
  - `bdd_steps` (scenario_id, step_order, step_text, step_type)
  - `event_storming_events` (event_id, slice_id, name, description, source_ref)
  - `event_storming_commands` (command_id, slice_id, name, description, triggers_event_id)
  - `event_storming_policies` (policy_id, slice_id, name, description, triggers_command_id)
  - `event_storming_read_models` (read_model_id, slice_id, name, description)
  - `event_storming_aggregates` (aggregate_id, slice_id, name, invariants)
  - `event_storming_flows` (flow_id, from_type, from_id, to_type, to_id, rationale)
- **DuckDB views:**
  - `v_ubiquitous_language_terms`
  - `v_bdd_features`
  - `v_bdd_scenarios`
  - `v_bdd_steps`
  - `v_event_storming_events`
  - `v_event_storming_commands`
  - `v_event_storming_policies`
  - `v_event_storming_read_models`
  - `v_event_storming_aggregates`
  - `v_event_storming_flows`

All downstream stages must use these terms, BDD scenarios, and event storming artifacts as the authoritative language and acceptance criteria.

All pre-step artifacts are versioned using the same versioning rules (artifact_version, run_id, slice_id, created_at, supersedes_version).

### BRD Generation from BDD

From BDD, the system must generate a Business Requirements Document (BRD) that captures actors and journeys. The BRD is derived from Parquet and stored as Parquet-backed artifacts.

- **Parquet tables:**
  - `brd_actors` (actor_id, actor_type, name, description, source_ref)
  - `brd_user_journeys_l1` (journey_id, actor_id, title, summary, group_label, priority)
  - `brd_user_journeys_l2` (step_id, journey_id, step_order, detail, bdd_ref)
  - `brd_trace` (brd_id, bdd_feature_id, bdd_scenario_id, rationale)
- **DuckDB views:**
  - `v_brd_actors`
  - `v_brd_user_journeys_l1`
  - `v_brd_user_journeys_l2`
  - `v_brd_trace`

The BRD must include human actors and system actors, plus user journeys at Level 1 (grouped by actor) and Level 2 (detailed steps per actor).

The BRD must be written in clean English, readable by business analysts and product owners, with no technical jargon, and generated from DuckDB-backed Parquet.

BRD content must be traceable back to DDD artifacts (ubiquitous language terms, aggregates, and event storming) via Parquet-backed trace tables.

### Stage 0: Intake and Normalization (Implemented)

Status: Implemented in this repo.

- **Parquet tables:**
  - `intake_source_index` (file_path, language, loc, module, checksum)
  - `intake_source_chunks` (file_path, line_start, line_end, content, checksum, source_ref)
  - `intake_build_context` (tool, version, flags, env_key, env_value)
  - `intake_schema_snapshot` (object_type, object_name, ddl, source)
- **DuckDB views:**
  - `v_source_index`
  - `v_source_chunks`
  - `v_build_context`
  - `v_schema_snapshot`
- **Incremental ingestion:**
  - Use `checksum` diffs to append only changed files.
  - Preserve prior versions via `artifact_version` and `supersedes_version`.
  - Partition Parquet by `run_id` and `artifact_version` to minimize re-reads.

### Stage 1: Parser and Lakehouse Loader (Implemented)

Status: Implemented in this repo.

- **Parquet tables:**
  - `symbols` (symbol_id, name, kind, signature, file_path, line)
  - `calls` (caller_id, callee_id, file_path, line)
  - `data_access` (symbol_id, table_name, op, sql_text, file_path, line)
  - `constants` (name, value, file_path, line)
  - `conditions` (symbol_id, predicate, file_path, line)
  - `parse_audit` (file_path, language, method, status, source_ref)
- **DuckDB views:**
  - `v_symbols`
  - `v_calls`
  - `v_data_access`
  - **Parser implementation:** use tree-sitter with exhaustive per-language query files (scm) to extract symbols, calls, conditions, constants, and data access. Queries are configured externally and executed per file.
  - **SCM coverage rule:** `.scm` queries must be exhaustive for supported languages and artifact types; missing patterns are treated as parser defects and must be fixed before promotion.
  - **Pipeline priority:** graph-first. Build and validate call/data graphs before vector embeddings or clustering.
  - **Coverage gate:** parser stage must fail if a supported language lacks required `.scm` query files for symbols, calls, conditions, constants, and data_access.
  - **Roslyn-first rule:** for Roslyn-supported languages (C# and VB.NET), use Roslyn if configured; otherwise fallback to tree-sitter and record the method in `parse_audit`.

### Stage 2: Graph Generation (Implemented)

Status: Implemented in this repo.

- **Parquet tables:**
  - `code_graph_nodes` (node_id, node_type, symbol_id, table_name, label)
  - `code_graph_edges` (from_id, to_id, edge_type, file_path, line)
  - `code_vectors` (node_id, vector, model, dims, source_ref)
  - `graph_metadata` (node_id, degree, pagerank, community_id, source_ref)
  - `vector_metadata` (node_id, model, dims, embedding_norm, cluster_hint, source_ref)
  - `entry_exit_map` (entry_node_id, exit_node_id, effect_type)
  - `slice_candidates` (slice_id, label, rationale, score)
- **DuckDB views:**
  - `v_code_graph_nodes`
  - `v_code_graph_edges`
  - `v_code_vectors`
  - `v_graph_metadata`
  - `v_vector_metadata`
  - `v_entry_exit_map`
  - `v_slice_candidates`

### Advanced Clustering (Graph + Vector from DuckDB) (Planned)

Status: Planned, not implemented yet.

- **Requirement:** clustering uses both graph topology (from `v_code_graph_nodes`/`v_code_graph_edges`) and embeddings (from `v_code_vectors`), all queried via DuckDB.
- **Algorithms:** Leiden/Louvain for graph communities, HDBSCAN for vector density, and hybrid clustering via feature fusion (graph metrics + embeddings).
- **Parquet outputs:**
  - `clusters` (cluster_id, slice_id, method, score, rationale)
  - `cluster_members` (cluster_id, node_id, membership_score)
- **DuckDB views:**
  - `v_clusters`
  - `v_cluster_members`

### Leiden + HDBSCAN Fusion (Mathematics)

Let $G=(V,E)$ be the weighted call/data graph with adjacency $W$, and each node $i$ has embedding $x_i \in \mathbb{R}^d$.

- **Edge weights:** $w_{ij} = \sum_k \alpha_k \cdot \mathbf{1}\{\text{edge}_k(i,j)\}$ (e.g., calls, data_access, shared_table).
- **Leiden optimizes modularity:**

$$
Q = \frac{1}{2m}\sum_{i,j}\left[w_{ij} - \frac{k_i k_j}{2m}\right]\mathbf{1}\{c_i = c_j\}
$$

$$
k_i = \sum_j w_{ij}, \quad m = \frac{1}{2}\sum_{i,j} w_{ij}
$$

- **Graph affinity:** $A_{ij} = \mathbf{1}\{c_i = c_j\}$ or a continuous score from PPR/node2vec.
- **HDBSCAN mutual reachability distance:**

$$
d_{\text{mr}}(i,j) = \max(\text{core}_k(i), \text{core}_k(j), d(i,j))
$$

$$
d(i,j) = 1 - \cos(x_i, x_j)
$$

- **Vector affinity:** HDBSCAN yields membership probabilities $p_i$; define $V_{ij} = p_i p_j$ if same cluster, else 0.
- **Fusion:**

$$
F_{ij} = \alpha A_{ij} + (1 - \alpha) V_{ij}
$$

Default $\alpha = 0.6$.

- **Merge rule:**

$$
\text{Link } i,j \text{ if } F_{ij} \ge \tau, \text{ or if } A_{ij} \ge \tau_g \text{ OR } V_{ij} \ge \tau_v
$$

Typical defaults: $\tau_g = 0.55$, $\tau_v = 0.78$.

### Example: Leiden + HDBSCAN Fusion (Why It Works)

**Setup**
- Nodes: A, B, C, D
- Edges: A–B (call), B–C (data_access), D isolated
- Embedding cosine similarities:
  - sim(A,B)=0.92, sim(B,C)=0.81, sim(A,C)=0.40, sim(D,*)≈0.10

**Leiden (graph communities)**
- C1 = {A,B,C}, C2 = {D}
- Graph affinity: $A_{ij} = 1$ if same community, else 0.

**HDBSCAN (vector density)**
- V1 = {A,B} (dense); C is borderline; D is noise
- Vector affinity: $V_{ij} = p_i p_j$ for same HDBSCAN cluster, else 0.

**Fusion with $\alpha=0.6$**

$$
F_{ij} = \alpha A_{ij} + (1-\alpha) V_{ij}
$$

- $F_{AB} = 0.6*1 + 0.4*0.81 = 0.924$
- $F_{BC} = 0.6*1 + 0.4*0 = 0.6$
- $F_{AC} = 0.6*1 + 0.4*0 = 0.6$
- $F_{AD} = 0$

If $\tau=0.6$, then A, B, C link into one cluster; D stays separate. If $\tau=0.7$, then A,B stay and C splits out (vector affinity did not support it).

**Why the fusion works**
- Graph captures structural flow (calls/data access), even if embeddings are noisy.
- Embeddings capture semantic similarity, even when the call graph is incomplete.
- Fusion reduces false positives from either signal alone and lets you tune strictness via $\alpha$ and $\tau$.

### Stage 3: Slice Extractor (Implemented)

Status: Implemented in this repo.

- **Parquet tables:**
  - `slice_manifest` (slice_id, file_path, symbol_id, table_name, external_ref)
  - `slice_context` (slice_id, summary, risks, assumptions)
  - `slice_source_refs` (slice_id, file_path, line, excerpt)
- **DuckDB views:**
  - `v_slice_manifest`
  - `v_slice_context`
  - `v_slice_source_refs`

### Stage 4: Logic Manifester (Implemented)

Status: Implemented in this repo.

- **Parquet tables:**
  - `logic_rules` (rule_id, slice_id, rule_text, inputs, outputs, invariants)
  - `logic_edges` (rule_id, symbol_id, file_path, line, evidence)
  - `trace_map` (rule_id, file_path, line, rationale)
- **DuckDB views:**
  - `v_logic_rules`
  - `v_logic_edges`
  - `v_trace_map`
- **Human-readable outputs (derived):**
  - Logic_Manifest.md generated from `v_logic_rules` + `v_trace_map`.

### Stage 5: Domain Architect (Implemented)

Status: Implemented in this repo.

- **Parquet tables:**
  - `domain_entities` (entity_id, slice_id, name, invariants)
  - `value_objects` (vo_id, slice_id, name, invariants)
  - `aggregates` (aggregate_id, slice_id, name, root_entity_id)
  - `context_map` (context_id, slice_id, name, boundaries)
- **DuckDB views:**
  - `v_domain_entities`
  - `v_value_objects`
  - `v_aggregates`
  - `v_context_map`

### Stage 6: TDD Engineer (Planned)

Status: Planned, not implemented yet.

- **Parquet tables:**
  - `tests` (test_id, slice_id, test_name, description)
  - `test_cases` (test_id, input_json, expected_json, rationale)
  - `test_coverage` (test_id, rule_id, coverage_type)
- **DuckDB views:**
  - `v_tests`
  - `v_test_cases`
  - `v_test_coverage`

### Stage 7: Implementer (Planned)

Status: Planned, not implemented yet.

- **Parquet tables:**
  - `code_artifacts` (artifact_id, slice_id, layer, file_path, content, checksum)
  - `api_contracts` (contract_id, slice_id, route, method, request_schema, response_schema)
- **DuckDB views:**
  - `v_code_artifacts`
  - `v_api_contracts`

### Stage 8: Build and Test Loop (Planned)

Status: Planned, not implemented yet.

- **Parquet tables:**
  - `build_reports` (build_id, slice_id, status, error_code, stderr_excerpt)
  - `test_reports` (test_run_id, slice_id, status, failed_tests, stdout_excerpt)
  - `fix_queue` (issue_id, slice_id, issue_type, details, source_ref)
- **DuckDB views:**
  - `v_build_reports`
  - `v_test_reports`
  - `v_fix_queue`

### Stage 9: Fixer and Debugger (Planned)

Status: Planned, not implemented yet.

- **Parquet tables:**
  - `fix_log` (fix_id, slice_id, change_summary, root_cause)
  - `code_changes` (fix_id, file_path, diff_excerpt)
- **DuckDB views:**
  - `v_fix_log`
  - `v_code_changes`

### Stage 10: Judge (Planned)

Status: Planned, not implemented yet.

- **Parquet tables:**
  - `judge_reports` (judge_id, slice_id, score, verdict, gaps)
  - `rule_coverage` (slice_id, rule_id, covered_by_tests, covered_by_code)
- **DuckDB views:**
  - `v_judge_reports`
  - `v_rule_coverage`
