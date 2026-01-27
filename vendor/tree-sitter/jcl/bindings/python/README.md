# Tree-sitter JCL Python Bindings

Python bindings for the tree-sitter JCL (Job Control Language) grammar.

## Installation

```bash
pip install tree-sitter-jcl
```

## Usage

```python
import tree_sitter
from tree_sitter_jcl import language

# Create a parser
parser = tree_sitter.Parser()
parser.set_language(language())

# Parse JCL code
jcl_code = """
//MYJOB    JOB (ACCT),'MY JOB',CLASS=A
//STEP1    EXEC PGM=IEFBR14
//SYSOUT   DD SYSOUT=*
"""

tree = parser.parse(jcl_code.encode('utf-8'))
print(tree.root_node.sexp())
```

## Features

- Full JCL syntax support including:
  - JOB, EXEC, DD statements
  - PROC definitions and calls
  - Conditional execution (IF/THEN/ELSE)
  - Comments and continuation lines
  - Dataset names and parameters
  - Inline data support

## Query Patterns

The package includes pre-built query patterns for common analysis tasks:

```python
import tree_sitter
from tree_sitter_jcl import language

# Load query patterns for analysis
with open('queries/analysis.scm', 'r') as f:
    query = language().query(f.read())

# Find all job names
matches = query.captures(tree.root_node)
job_names = [match.node.text for match in matches if match.capture == 'job.name']
```

## Development

This package is designed to integrate with mainframe code analysis pipelines and Neo4j graph databases for tracking JCL dependencies and data flow.