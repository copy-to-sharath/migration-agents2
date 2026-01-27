# Migration Agents - Architecture Diagram

This diagram shows the complete end-to-end workflow for the migration-agents pipeline.

## Workflow Overview

```mermaid
flowchart TB
    subgraph LegacySource["🏛️ Legacy Source Code"]
        direction TB
        SRC["Source Files<br/>C#, VB.NET, COBOL, etc."]
        DOCS["Documentation<br/>PDF, DOCX"]
        SQL["Database Schemas"]
    end

    subgraph Analyzer["01-ANALYZER (One-Time Setup)"]
        direction TB
        
        subgraph Stage0["Stage 0: Intake & Normalization"]
            INGEST["analyzer step='ingest'"]
            SI["intake_source_index"]
            SC["intake_source_chunks"]
            BC["intake_build_context"]
        end
        
        subgraph Stage1["Stage 1: Parser"]
            PARSE["analyzer step='parse'"]
            ROSLYN{"Roslyn?"}
            TREESITTER["Tree-Sitter Parsing"]
            ROSLYNP["Roslyn Analyzer<br/>C#/VB.NET"]
            SYM["symbols"]
            CALLS["calls"]
            COND["conditions"]
            CONST["constants"]
            DATA["data_access"]
            AUDIT["parse_audit"]
        end
        
        subgraph Stage2["Stage 2: Graph Generation"]
            GRAPH["Graph Builder"]
            NODES["code_graph_nodes"]
            EDGES["code_graph_edges"]
            META["graph_metadata"]
            ENTRY["entry_exit_map"]
            ENTRYGRAPH["entry_graphs"]
        end
        
        subgraph Stage3["Stage 3: Slice Extraction"]
            SLICE["analyzer step='slice'"]
            SM["slice_manifest"]
            SCTX["slice_context"]
            SREF["slice_source_refs"]
        end
    end

    subgraph DDD["🎯 DDD-First Analysis"]
        direction TB
        DDD_ANALYZE["ddd_analyze_all_endpoints"]
        DDD_BC["Bounded Contexts"]
        DDD_AGG["Aggregates"]
        DDD_UL["Ubiquitous Language"]
        DDD_BUILD["batch_ddd_build_model"]
        SME_REVIEW["SME Review Gate"]
    end

    subgraph Builder["02-BUILDER (Per-Slice Generation)"]
        direction TB
        
        subgraph Stage4["Stage 4: Logic Manifester"]
            LOGIC["Logic Rules Extraction"]
            RULES["logic_rules"]
            LEDGES["logic_edges"]
            TRACE["trace_map"]
            MANIFEST["Logic_Manifest.md"]
        end
        
        subgraph Stage5["Stage 5: Domain Architect"]
            DOMAIN["Domain Model"]
            ENTITIES["domain_entities"]
            VOBJ["value_objects"]
            AGG["aggregates"]
            CMAP["context_map"]
        end
        
        subgraph Stage6["Stage 6: TDD Engineer"]
            TDD["Test Generation"]
            TESTS["tests"]
            TCASES["test_cases"]
            TCOV["test_coverage"]
        end
        
        subgraph Stage7["Stage 7: Code Generation"]
            CODEGEN["builder_generate"]
            ARTIFACTS["code_artifacts"]
            CONTRACTS["api_contracts"]
            GHERKIN["Gherkin/BDD Specs"]
            OPENAPI["OpenAPI Contract"]
        end
    end

    subgraph Judge["03-JUDGE (Validation Loop)"]
        direction TB
        VALIDATE["judge_validate"]
        
        subgraph BuildTest["Stage 8: Build & Test"]
            BUILD["dotnet build"]
            TEST["dotnet test"]
            BREPORT["build_reports"]
            TREPORT["test_reports"]
        end
        
        subgraph Validation["Validation Checks"]
            CITE["Citation Check"]
            SCHEMA["Schema Compliance"]
            COVERAGE["Coverage Check"]
        end
        
        JREPORT["judge_reports"]
        FIXQ["fix_queue"]
    end

    subgraph Fixer["🔧 Fix Loop"]
        direction TB
        FIX["builder_fix"]
        FLOG["fix_log"]
        CHANGES["code_changes"]
    end

    subgraph Storage["💾 Data Layer"]
        direction LR
        PARQUET[("Parquet Files<br/>data/parquet/")]
        DUCKDB[("DuckDB<br/>data/duckdb/")]
        MCP["MCP Server<br/>JSON-RPC"]
    end

    subgraph Output["🎉 .NET 8.0 Clean Architecture"]
        direction TB
        DOMAINL["Domain Layer<br/>Rich Domain Models"]
        APPL["Application Layer<br/>CQRS + MediatR"]
        INFRAL["Infrastructure Layer<br/>EF Core 8"]
        APIL["API Layer<br/>Minimal APIs"]
    end

    %% Flow connections
    SRC --> INGEST
    DOCS --> INGEST
    SQL --> INGEST
    
    INGEST --> SI & SC & BC
    SI & SC --> PARSE
    
    PARSE --> ROSLYN
    ROSLYN -->|Yes| ROSLYNP
    ROSLYN -->|No| TREESITTER
    ROSLYNP --> SYM
    TREESITTER --> SYM
    SYM --> CALLS & COND & CONST & DATA & AUDIT
    
    CALLS & DATA --> GRAPH
    GRAPH --> NODES & EDGES & META & ENTRY & ENTRYGRAPH
    
    NODES & EDGES --> SLICE
    SLICE --> SM & SCTX & SREF
    
    SM --> DDD_ANALYZE
    DDD_ANALYZE --> DDD_BC & DDD_AGG & DDD_UL
    DDD_BC --> DDD_BUILD
    DDD_BUILD --> SME_REVIEW
    SME_REVIEW -->|Approved| LOGIC
    
    SREF --> LOGIC
    LOGIC --> RULES & LEDGES & TRACE & MANIFEST
    
    MANIFEST --> DOMAIN
    DOMAIN --> ENTITIES & VOBJ & AGG & CMAP
    
    ENTITIES --> TDD
    TDD --> TESTS & TCASES & TCOV
    
    TCASES --> CODEGEN
    CODEGEN --> ARTIFACTS & CONTRACTS & GHERKIN & OPENAPI
    
    ARTIFACTS --> BUILD
    BUILD --> BREPORT
    BREPORT --> TEST
    TEST --> TREPORT
    
    TREPORT --> VALIDATE
    VALIDATE --> CITE & SCHEMA & COVERAGE
    CITE & SCHEMA & COVERAGE --> JREPORT
    
    JREPORT --> FIXQ
    FIXQ -->|Has Fixes| FIX
    FIX --> FLOG & CHANGES
    CHANGES --> CODEGEN
    
    JREPORT -->|All Pass| DOMAINL
    DOMAINL --> APPL --> INFRAL --> APIL
    
    %% Storage connections
    SI & SC & BC -.-> PARQUET
    SYM & CALLS -.-> PARQUET
    NODES & EDGES -.-> PARQUET
    SM & SCTX -.-> PARQUET
    RULES -.-> PARQUET
    ENTITIES -.-> PARQUET
    TESTS -.-> PARQUET
    ARTIFACTS -.-> PARQUET
    JREPORT -.-> PARQUET
    
    PARQUET <-.-> DUCKDB
    DUCKDB <-.-> MCP

    %% Styling
    classDef analyzer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef builder fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef judge fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef storage fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef output fill:#e8eaf6,stroke:#1a237e,stroke-width:2px
    classDef ddd fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class Stage0,Stage1,Stage2,Stage3 analyzer
    class Stage4,Stage5,Stage6,Stage7 builder
    class BuildTest,Validation judge
    class PARQUET,DUCKDB,MCP storage
    class DOMAINL,APPL,INFRAL,APIL output
    class DDD_ANALYZE,DDD_BC,DDD_AGG,DDD_UL,DDD_BUILD,SME_REVIEW ddd
```

## Agent Responsibilities

| Agent | Stages | MCP Tools | Description |
|-------|--------|-----------|-------------|
| **01-analyzer** | 0-3 | `analyzer` (ingest/parse/slice) | One-time analysis setup |
| **02-builder** | 4-7 | `builder_generate`, `builder_fix`, `ddd_*` | Per-slice code generation |
| **03-judge** | 8+ | `judge_validate` | Validation with fix loop |

## Data Flow Summary

1. **Intake**: Legacy source → Parquet chunks with checksums
2. **Parse**: Tree-sitter/Roslyn → Symbols, calls, data access
3. **Graph**: Build call/data graphs → Entry/exit maps
4. **Slice**: Extract vertical slices by depth workflows
5. **DDD**: Analyze bounded contexts, aggregates, ubiquitous language
6. **Logic**: Extract business rules → Logic Manifest
7. **Domain**: Model entities, value objects, aggregates
8. **TDD**: Generate tests before code
9. **Code**: Generate .NET 8.0 Clean Architecture
10. **Judge**: Build, test, validate citations & coverage
11. **Fix Loop**: Auto-correct until all validations pass

## Storage Architecture

- **Parquet**: All artifacts stored as columnar data
- **DuckDB**: Read layer with views per table
- **MCP Server**: JSON-RPC interface for agent access
- **Per-run databases**: `data/duckdb/run_YYYYMMDDHHMMSS.duckdb`
