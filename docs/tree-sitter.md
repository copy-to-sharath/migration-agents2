# Tree-Sitter Language Grammars

This document describes the tree-sitter language grammars used for parsing mainframe and modern source code.

## Overview

The migration-agents project uses tree-sitter for parsing source files. Tree-sitter provides:
- Fast, incremental parsing
- Error recovery (partial parsing of invalid code)
- Concrete Syntax Trees (CST) with full positional information

## Included Languages (20 total)

### Mainframe Languages

| Language | Grammar Name | Extensions | Description |
|----------|--------------|------------|-------------|
| COBOL | `COBOL` | `.cbl`, `.cl2`, `.cob` | Full COBOL-85/2002 grammar |
| JCL | `jcl` | `.jcl`, `.prc` | IBM Job Control Language |
| BMS | `bms` | `.bms` | CICS Basic Mapping Support |
| CICS | `cics` | - | CICS command grammar |
| CSD | `csd` | `.CSD`, `.csd` | CICS System Definition |
| IDCAMS | `idcams` | `.CTL`, `.ctl` | Access Method Services control statements |
| HLASM | `hlasm` | `.asm` | High Level Assembler |
| Easytrieve | `easytrieve` | `.ezt` | Easytrieve Plus reporting |
| Copybook | `copybook` | (no extension) | COBOL copybook fragments |

### Modern Languages

| Language | Grammar Name | Extensions |
|----------|--------------|------------|
| Python | `python` | `.py` |
| JavaScript | `javascript` | `.js` |
| TypeScript | `typescript` | `.ts` |
| C# | `c_sharp` | `.cs` |
| Java | `java` | `.java` |
| VB.NET | `vb` | `.vb` |
| HTML | `html` | `.html` |
| CSS | `css` | `.css` |
| XML | `xml` | `.xml` |
| PHP | `php` | `.php` |
| SQL | `sql` | `.sql` |

## Installation

### Option 1: Using the Pre-built Package

```bash
pip install migration_agents_tree_sitter_languages-0.1.0-py3-none-any.whl
```

### Option 2: Building from Source

Requires:
- Visual Studio 2022 (Windows) or GCC/Clang (Linux/Mac)
- Node.js (for grammar generation)
- Python 3.10+

```bash
# Windows (from Developer Command Prompt)
uv run python -m migration_agents.parser.build_languages --config config/tree_sitter_build.json

# Linux/Mac
./scripts/build_treesitter.sh
```

## Usage

### Using the Package API

```python
from ts_languages import load_language, list_languages
import tree_sitter

# List available languages
print(list_languages())

# Load a language
lang = load_language('copybook')
parser = tree_sitter.Parser(lang)

# Parse source code
source = b'''
      01 CUSTOMER-RECORD.
         05 CUST-ID     PIC 9(10).
         05 CUST-NAME   PIC X(30).
'''
tree = parser.parse(source)

# Access the syntax tree
print(tree.root_node.sexp())
```

### Using Direct ctypes Loading

```python
import ctypes
from pathlib import Path
import tree_sitter

# Load the DLL
dll = Path('tree-sitter/languages.dll').resolve()
lib = ctypes.cdll.LoadLibrary(str(dll))

# Get language function
func = getattr(lib, 'tree_sitter_copybook')
func.restype = ctypes.c_void_p
lang_ptr = func()

# Create parser
lang = tree_sitter.Language(lang_ptr)
parser = tree_sitter.Parser(lang)

# Parse
tree = parser.parse(b'01 MY-FIELD PIC X(10).')
```

## Grammar Details

### Copybook Grammar

The copybook grammar parses COBOL copybook fragments which contain:

- **Data Division items**: Level numbers (01-49, 66, 77, 88), PIC clauses, VALUE clauses
- **Procedure Division fragments**: IF/EVALUATE/PERFORM statements
- **Template variables**: Patterns like `(TESTVAR1)`, `FLG-(TESTVAR1)-NOT-OK`
- **Comments**: Lines starting with `*` in column 7

```cobol
      *******************************************************
      * Customer Record Layout
      *******************************************************
       01 CUSTOMER-RECORD.
          05 CUST-ID         PIC 9(10).
          05 CUST-NAME       PIC X(30).
          05 CUST-STATUS     PIC X(1).
             88 CUST-ACTIVE  VALUE 'A'.
             88 CUST-INACTIVE VALUE 'I'.
```

#### Supported Constructs

| Construct | Example |
|-----------|---------|
| Level numbers | `01`, `05`, `10`, `15`, `20`, `66`, `77`, `88` |
| PIC clauses | `PIC X(10)`, `PIC 9(5)V99`, `PIC S9(7) COMP-3` |
| VALUE clauses | `VALUE 'ABC'`, `VALUE ZEROS`, `VALUE 100` |
| OCCURS | `OCCURS 10 TIMES`, `OCCURS 1 TO 100 DEPENDING ON X` |
| REDEFINES | `05 ALT-FIELD REDEFINES MAIN-FIELD` |
| Template identifiers | `(TESTVAR1)`, `FLG-(VAR)-OK` |
| Embedded comments | Comments within multi-line statements |

### BMS Grammar

Parses CICS BMS macro definitions:

```
TESTMAP  DFHMSD TYPE=MAP,LANG=COBOL,MODE=INOUT
TESTFLD  DFHMDF POS=(01,01),LENGTH=10,ATTRB=(ASKIP,BRT)
         DFHMSD TYPE=FINAL
```

### JCL Grammar

Parses IBM JCL and procedures:

```jcl
//MYJOB   JOB (ACCT),'MY JOB',CLASS=A,MSGCLASS=X
//STEP1   EXEC PGM=IEFBR14
//DD1     DD DSN=MY.DATASET,DISP=SHR
```

### CSD Grammar

Parses CICS System Definition commands:

```
DEFINE PROGRAM(MYPROG) GROUP(MYGROUP)
       LANGUAGE(COBOL)
       DESCRIPTION(MY PROGRAM)
```

### IDCAMS Grammar

Parses Access Method Services control statements:

```
DEFINE CLUSTER (NAME(MY.CLUSTER) -
                VOLUMES(VOL001) -
                RECORDS(1000 5000))
```

## Working with Syntax Trees

### Traversing Nodes

```python
def visit(node, indent=0):
    print('  ' * indent + f'{node.type}: {node.text[:50]}')
    for child in node.children:
        visit(child, indent + 1)

visit(tree.root_node)
```

### Finding Specific Nodes

```python
def find_nodes(node, node_type):
    results = []
    if node.type == node_type:
        results.append(node)
    for child in node.children:
        results.extend(find_nodes(child, node_type))
    return results

# Find all identifiers
identifiers = find_nodes(tree.root_node, 'identifier')
```

### Error Detection

```python
def count_errors(node):
    count = 1 if node.type == 'ERROR' else 0
    for child in node.children:
        count += count_errors(child)
    return count

errors = count_errors(tree.root_node)
print(f'Parse errors: {errors}')
```

### Using Tree-Sitter Queries

```python
# Query for all level numbers and their identifiers
query = lang.query('''
(statement
  (statement_body
    (level_number) @level
    (identifier) @name))
''')

captures = query.captures(tree.root_node)
for node, name in captures:
    print(f'{name}: {node.text.decode()}')
```

## File Structure

```
vendor/tree-sitter/
├── copybook/
│   ├── grammar.js          # Grammar definition
│   ├── package.json
│   └── src/
│       ├── grammar.json    # Generated
│       ├── parser.c        # Generated C parser
│       └── tree_sitter/
│           └── parser.h
├── bms/
├── jcl/
├── cics/
├── csd/
├── idcams/
├── hlasm/
├── easytrieve/
└── ... (other grammars)

tree-sitter/
├── languages.dll           # Windows x64 compiled library
├── languages.lib
└── languages.exp

config/
└── tree_sitter_build.json  # Build configuration
```

## Build Configuration

The `config/tree_sitter_build.json` file defines all grammars:

```json
{
  "output": "tree-sitter/languages.dll",
  "languages": [
    {
      "name": "copybook",
      "path": "vendor/tree-sitter/copybook"
    },
    {
      "name": "COBOL",
      "path": "vendor/tree-sitter/cobol"
    }
    // ... more languages
  ]
}
```

## Troubleshooting

### DLL Not Loading

**Error**: `FileNotFoundError` or `OSError` when loading DLL

**Solutions**:
1. Ensure the DLL path is absolute
2. On Windows, check Visual C++ Redistributable is installed
3. Check McAfee/antivirus isn't blocking the DLL

### Grammar Generation Fails

**Error**: `Failed to run node - program not found`

**Solution**: Add Node.js to PATH:
```powershell
$env:PATH = "C:\Program Files\nodejs;$env:PATH"
```

### Parse Errors

If files aren't parsing correctly:

1. Check the file encoding (should be UTF-8 or ASCII)
2. Verify the correct grammar is being used for the file type
3. Use the error detection code above to find problematic sections

## Platform Support

| Platform | Status | Library |
|----------|--------|---------|
| Windows x64 | ✅ Pre-built | `languages.dll` |
| Linux x64 | 🔧 Requires build | `languages.so` |
| macOS x64 | 🔧 Requires build | `languages.dylib` |
| macOS ARM | 🔧 Requires build | `languages.dylib` |

## Performance

Tree-sitter is designed for IDE-level performance:

- **Parsing speed**: ~10MB/s for most grammars
- **Incremental updates**: Only re-parses changed portions
- **Memory efficient**: Shared memory for identical subtrees

For batch processing of large codebases, consider:
- Parallel parsing with multiprocessing
- Caching parsed trees
- Using the incremental parsing API for repeated edits

## References

- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [Tree-sitter Python Bindings](https://github.com/tree-sitter/py-tree-sitter)
- [Writing Tree-sitter Grammars](https://tree-sitter.github.io/tree-sitter/creating-parsers)
