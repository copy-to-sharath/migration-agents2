# Tree-sitter JCL

A [tree-sitter](https://tree-sitter.github.io/) grammar for JCL (Job Control Language), primarily targeting z/OS mainframe environments.

## Features

- **Complete JCL Syntax Support**: JOB, EXEC, DD statements with parameters
- **Advanced Constructs**: PROC definitions, conditional execution (IF/THEN/ELSE)
- **Data Handling**: Inline data support, dataset references, temporary datasets
- **Analysis Ready**: Query patterns designed for code analysis and dependency mapping
- **Python Integration**: Bindings ready for integration with Python-based mainframe tools

## Installation

### For Development

```bash
git clone <repository-url>
cd tree-sitter-jcl
npm install
npx tree-sitter generate
```

### Python Bindings (Future)

```bash
cd bindings/python
pip install .
```

## Usage

### Parsing JCL Files

```bash
# Parse a JCL file
npx tree-sitter parse examples/simple.jcl

# Run tests
npx tree-sitter test
npm test
```

### Query Patterns

The grammar includes pre-built query patterns for common analysis tasks:

- `queries/highlights.scm` - Syntax highlighting
- `queries/analysis.scm` - Code analysis and dependency extraction
- `queries/patterns.scm` - Common JCL patterns

### Python Integration

```python
import tree_sitter
from tree_sitter_jcl import language

parser = tree_sitter.Parser()
parser.set_language(language())

jcl_code = """
//MYJOB    JOB (ACCT),'TEST JOB'
//STEP1    EXEC PGM=IEFBR14
"""

tree = parser.parse(jcl_code.encode('utf-8'))
print(tree.root_node.sexp())
```

## Supported JCL Constructs

### Basic Statements
- **JOB**: Job definition with accounting and parameters
- **EXEC**: Program and procedure execution
- **DD**: Data definition statements
- **Comments**: //* comment lines

### Advanced Features
- **PROC/PEND**: Procedure definitions
- **IF/THEN/ELSE/ENDIF**: Conditional execution
- **INCLUDE**: Member inclusion
- **JCLLIB**: Library order specification
- **SET**: Symbol assignments

### Data Handling
- Dataset names (qualified, temporary, referbacks)
- Inline data (DD * statements)
- Parameter lists and keywords
- Continuation lines

## Development

This project follows strict **Test-Driven Development (TDD)**:

1. Write a failing test in `test/corpus/`
2. Implement the minimal grammar rule to pass
3. Refactor while keeping tests green

### Commands

```bash
npm test                    # Run unit tests
npx tree-sitter test       # Run corpus tests
npx tree-sitter generate   # Generate parser
npm run lint               # Lint code
```

### Adding New Grammar Rules

1. Create test case in `test/corpus/`
2. Add grammar rule in `grammar.js`
3. Update query patterns as needed
4. Test with real JCL examples

## Roadmap

- [ ] Complete JCL statement coverage
- [ ] Enhanced error recovery
- [ ] Performance optimization for large files
- [ ] Additional JCL dialect support
- [ ] Neo4j integration examples
- [ ] VSCode syntax highlighting

## Contributing

1. Follow TDD practices - no code without tests
2. Test with real mainframe JCL examples
3. Update query patterns for new constructs
4. Document complex grammar decisions
