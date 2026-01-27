# Parser (Stage 1)

The parser stage converts intake chunks into structured tables
(symbols, calls, conditions, constants, data access) using tree-sitter
or Roslyn, and generates a code graph from those signals.

## Responsibilities

- Load source chunks from Parquet via MCP (DuckDB).
- Map file extensions to parser language names.
- Use tree-sitter queries (`config/queries/*.scm`) to extract signals.
- Optionally use Roslyn for C# and VB.NET when configured.
- Produce a `parse_audit` log and `coverage_summary` metrics.
- Build code graph tables (`code_graph_nodes`, `code_graph_edges`,
  `graph_metadata`, `entry_exit_map`) directly from parsed outputs.
- Build entry graphs (`entry_graphs`, `entry_graph_state`,
  `entry_graph_processing_summary`) with depth-based scores.
- Optionally render DOT/PNG graphs for the full graph and top entry graphs.

## Tree-sitter workflow

- `language_library_path` points to a compiled `languages.so`.
- Each language must have required query files in `queries_dir`:
  - `LANG.scm` for symbols
  - `LANG.calls.scm`
  - `LANG.conditions.scm`
  - `LANG.constants.scm`
  - `LANG.data_access.scm`
- The parser fails if required files are missing (coverage gate).

## Roslyn workflow

If `roslyn_cmd` is provided and the language is in `roslyn_languages`,
the parser runs Roslyn and expects JSON output with keys:
`symbols`, `calls`, `conditions`, `constants`, `data_access`.

## Output tables

- `symbols`
- `calls`
- `conditions`
- `constants`
- `data_access`
- `code_graph_nodes`
- `code_graph_edges`
- `graph_metadata`
- `entry_exit_map`
- `entry_graphs`
- `entry_graph_state`
- `entry_graph_processing_summary`
- `entry_graph_summaries`
- `parse_audit`
- `coverage_summary` (generated from latest run)

All tables include versioning columns:
`run_id`, `artifact_version`, `slice_id`, `created_at`, `supersedes_version`.

## Supported Languages

### Fully Supported (16 languages)

| Language | Extension(s) | Grammar Source | Notes |
|----------|--------------|----------------|-------|
| **COBOL** | .cob, .cbl, .cobol, .cpy | yutaro-sakamoto/tree-sitter-cobol | Mainframe |
| **JCL** | .jcl, .proc, .prc | garner007/tree-sitter-jcl | Job Control Language |
| **CICS** | .cics, .csd | Custom (vendor/tree-sitter/cics) | EXEC CICS commands |
| **BMS** | .bms | Custom (vendor/tree-sitter/bms) | Screen definitions |
| **Easytrieve** | .ezt, .eztplus | Custom (vendor/tree-sitter/easytrieve) | Report generation |
| C# | .cs | tree-sitter/tree-sitter-c-sharp | Also supports Roslyn |
| VB.NET | .vb | tree-sitter-grammars/tree-sitter-vbnet | Also supports Roslyn |
| Java | .java | tree-sitter/tree-sitter-java | |
| Python | .py | tree-sitter/tree-sitter-python | |
| JavaScript | .js, .jsx | tree-sitter/tree-sitter-javascript | |
| TypeScript | .ts, .tsx | tree-sitter/tree-sitter-typescript | |
| PHP | .php | tree-sitter/tree-sitter-php | |
| SQL | .sql | DerekStride/tree-sitter-sql | |
| HTML | .html, .htm, .aspx, .ascx | tree-sitter/tree-sitter-html | |
| CSS | .css | tree-sitter/tree-sitter-css | |
| XML | .xml, .config, .csproj | tree-sitter-grammars/tree-sitter-xml | |

---

## Tree-sitter Compilation Guide

### Prerequisites

```bash
# Rust toolchain (for tree-sitter-cli)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# Install tree-sitter CLI via Cargo
cargo install tree-sitter-cli

# C/C++ compiler (for parser compilation)
sudo apt-get install build-essential  # Ubuntu/Debian
# or: brew install gcc                 # macOS
```

### Directory Structure

```
migration-agents/
├── vendor/tree-sitter/          # Grammar source directories
│   ├── cobol/
│   │   ├── grammar.js           # Grammar definition
│   │   └── src/
│   │       ├── parser.c         # Generated parser
│   │       ├── scanner.c        # External scanner (optional)
│   │       └── tree_sitter/     # Header files
│   ├── jcl/
│   ├── cics/
│   ├── bms/
│   ├── easytrieve/
│   └── ... (other languages)
├── build/tree-sitter/           # Compiled object files
│   ├── cobol_parser.o
│   ├── cobol_scanner.o
│   └── ...
├── tree-sitter/
│   └── languages.so             # Final shared library
└── config/queries/              # Query files (.scm)
```

### Step 1: Clone Grammar Repositories

```bash
cd vendor/tree-sitter

# Example: Clone COBOL grammar
git clone https://github.com/yutaro-sakamoto/tree-sitter-cobol cobol

# Example: Clone JCL grammar
git clone https://github.com/garner007/tree-sitter-jcl jcl
```

### Step 2: Generate Parser (using Rust tree-sitter-cli)

```bash
source "$HOME/.cargo/env"

# Generate parser from grammar.js
cd vendor/tree-sitter/cobol
tree-sitter generate

# This creates:
#   src/parser.c      - The parser implementation
#   src/grammar.json  - Grammar metadata
#   src/node-types.json - Node type definitions
```

### Step 3: Compile Object Files

```bash
cd /path/to/migration-agents

# Compile parser (always needed)
cc -fPIC -I vendor/tree-sitter/cobol/src \
   -c vendor/tree-sitter/cobol/src/parser.c \
   -o build/tree-sitter/cobol_parser.o

# Compile scanner if it exists (check for scanner.c or scanner.cc)
# For C scanner:
cc -fPIC -I vendor/tree-sitter/cobol/src \
   -c vendor/tree-sitter/cobol/src/scanner.c \
   -o build/tree-sitter/cobol_scanner.o

# For C++ scanner (.cc extension):
c++ -fPIC -I vendor/tree-sitter/sql/src \
   -c vendor/tree-sitter/sql/src/scanner.cc \
   -o build/tree-sitter/sql_scanner.o
```

### Step 4: Link into languages.so

```bash
# Link all object files into shared library
c++ -shared -o tree-sitter/languages.so \
    build/tree-sitter/cobol_parser.o \
    build/tree-sitter/cobol_scanner.o \
    build/tree-sitter/jcl_parser.o \
    build/tree-sitter/cics_parser.o \
    build/tree-sitter/bms_parser.o \
    build/tree-sitter/easytrieve_parser.o \
    build/tree-sitter/c_sharp_parser.o \
    build/tree-sitter/c_sharp_scanner.o \
    build/tree-sitter/css_parser.o \
    build/tree-sitter/css_scanner.o \
    build/tree-sitter/html_parser.o \
    build/tree-sitter/html_scanner.o \
    build/tree-sitter/java_parser.o \
    build/tree-sitter/javascript_parser.o \
    build/tree-sitter/javascript_scanner.o \
    build/tree-sitter/php_parser.o \
    build/tree-sitter/php_scanner.o \
    build/tree-sitter/python_parser.o \
    build/tree-sitter/python_scanner.o \
    build/tree-sitter/sql_parser.o \
    build/tree-sitter/sql_scanner.o \
    build/tree-sitter/typescript_parser.o \
    build/tree-sitter/typescript_scanner.o \
    build/tree-sitter/vbnet_parser.o \
    build/tree-sitter/xml_parser.o \
    build/tree-sitter/xml_scanner.o
```

### Step 5: Verify

```bash
# Check exported symbols
nm tree-sitter/languages.so | grep tree_sitter_

# Should show:
# T tree_sitter_COBOL
# T tree_sitter_bms
# T tree_sitter_cics
# T tree_sitter_c_sharp
# ... etc
```

### Quick Rebuild Script

```bash
#!/bin/bash
# rebuild_languages.sh

set -e
source "$HOME/.cargo/env"

BASE=/path/to/migration-agents
BUILD=$BASE/build/tree-sitter

# Regenerate all grammars
for lang in cobol jcl cics bms easytrieve; do
    echo "=== Regenerating $lang ==="
    cd $BASE/vendor/tree-sitter/$lang
    tree-sitter generate
done

cd $BASE

# Compile all parsers
compile_lang() {
    local name=$1
    local src=$2
    echo "Compiling $name..."
    cc -fPIC -I $src -c $src/parser.c -o $BUILD/${name}_parser.o
    
    if [ -f "$src/scanner.c" ]; then
        cc -fPIC -I $src -c $src/scanner.c -o $BUILD/${name}_scanner.o
    elif [ -f "$src/scanner.cc" ]; then
        c++ -fPIC -I $src -c $src/scanner.cc -o $BUILD/${name}_scanner.o
    fi
}

compile_lang cobol vendor/tree-sitter/cobol/src
compile_lang jcl vendor/tree-sitter/jcl/src
compile_lang cics vendor/tree-sitter/cics/src
compile_lang bms vendor/tree-sitter/bms/src
compile_lang easytrieve vendor/tree-sitter/easytrieve/src
# ... add other languages

# Link
c++ -shared -o tree-sitter/languages.so $BUILD/*.o

echo "✅ languages.so rebuilt"
```

### Adding a New Language

1. **Create or clone grammar:**
   ```bash
   cd vendor/tree-sitter
   git clone https://github.com/owner/tree-sitter-LANG LANG
   # or create grammar.js manually
   ```

2. **Generate parser:**
   ```bash
   cd vendor/tree-sitter/LANG
   tree-sitter generate
   ```

3. **Create query files** in `config/queries/`:
   - `LANG.scm` - Symbol definitions
   - `LANG.calls.scm` - Function/method calls
   - `LANG.conditions.scm` - Control flow
   - `LANG.constants.scm` - Literals
   - `LANG.data_access.scm` - Data operations

4. **Update extension mapping** in `config/parser.json`:
   ```json
   "extension_map": {
       ".ext": "LANG"
   }
   ```

5. **Compile and link** (see steps 3-4 above)

6. **Test:**
   ```python
   from migration_agents.parser.tree_sitter_loader import load_language
   lang = load_language(Path("tree-sitter/languages.so"), "LANG")
   ```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `tree_sitter/parser.h: No such file` | Add `-I vendor/tree-sitter/LANG/src` to compile command |
| `invalid conversion` errors with c++ | Use `cc` instead of `c++` for C scanners |
| Grammar conflicts | Simplify grammar or add `conflicts: []` array |
| Symbol not found in .so | Verify grammar exports `tree_sitter_LANG` function |
| Query compilation errors | Check node types match grammar with `tree-sitter parse` |

### Build Environment

Current build uses:
- **Rust**: 1.93.0
- **tree-sitter-cli**: 0.26.3
- **ABI version**: 14
- **Compiler**: GCC (cc/c++)
