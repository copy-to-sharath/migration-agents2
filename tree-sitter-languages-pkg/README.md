# Migration Agents Tree-Sitter Languages

Pre-built tree-sitter language grammars for mainframe code migration.

## Included Languages (20 total)

### Mainframe Languages
- **COBOL** - Full COBOL grammar
- **JCL** - Job Control Language
- **BMS** - Basic Mapping Support (CICS screens)
- **CICS** - CICS command grammar
- **CSD** - CICS System Definition
- **IDCAMS** - Access Method Services control statements
- **HLASM** - High Level Assembler
- **Easytrieve** - Easytrieve Plus reporting language
- **Copybook** - COBOL copybook fragments (data definitions, procedure division snippets)

### Modern Languages
- Python, JavaScript, TypeScript, C#, Java, VB.NET
- HTML, CSS, XML, PHP, SQL

## Installation

```bash
pip install migration-agents-tree-sitter-languages
```

## Usage

```python
from ts_languages import load_language
import tree_sitter

# Load a language
lang = load_language('copybook')
parser = tree_sitter.Parser(lang)

# Parse COBOL copybook
source = b'''
      01 CUSTOMER-RECORD.
         05 CUST-ID     PIC 9(10).
         05 CUST-NAME   PIC X(30).
'''
tree = parser.parse(source)
print(tree.root_node.sexp())
```

## Available Languages

| Language | Function Name |
|----------|---------------|
| COBOL | `tree_sitter_COBOL` |
| JCL | `tree_sitter_jcl` |
| BMS | `tree_sitter_bms` |
| CICS | `tree_sitter_cics` |
| CSD | `tree_sitter_csd` |
| IDCAMS | `tree_sitter_idcams` |
| HLASM | `tree_sitter_hlasm` |
| Easytrieve | `tree_sitter_easytrieve` |
| Copybook | `tree_sitter_copybook` |
| Python | `tree_sitter_python` |
| JavaScript | `tree_sitter_javascript` |
| TypeScript | `tree_sitter_typescript` |
| C# | `tree_sitter_c_sharp` |
| Java | `tree_sitter_java` |
| VB.NET | `tree_sitter_vb` |
| HTML | `tree_sitter_html` |
| CSS | `tree_sitter_css` |
| XML | `tree_sitter_xml` |
| PHP | `tree_sitter_php` |
| SQL | `tree_sitter_sql` |

## Platform Support

- Windows x64 (pre-built)
- Linux x64 (requires rebuild)
- macOS (requires rebuild)

## License

MIT
