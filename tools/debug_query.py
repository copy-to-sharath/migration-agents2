import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

from migration_agents.parser.tree_sitter_loader import load_language
from tree_sitter import Parser, Query, QueryCursor

# Load Language
lib_path = os.path.abspath("tree-sitter/languages.so")
print(f"Loading library from: {lib_path}")
bundle = load_language(lib_path, "html")
lang = bundle.language

parser = Parser()
parser.language = lang

# Sample ASPX
# code = b"""
# <asp:Button ID="btnSave" runat="server" OnClick="btnSave_Click" Text="Save" />
# """
path = "/home/sharath/code/nopCommerce-release-1.90/NopCommerceStore/Account.aspx"
with open(path, "rb") as f:
    code = f.read()

print("File start:", code[:100])

tree = parser.parse(code)
# print("Tree root:", tree.root_node.sexp())
print("Root node type:", tree.root_node.type)
print("Root node string:", str(tree.root_node))

query_scm = """
(attribute
  (attribute_name) @id_attr
  (quoted_attribute_value
    (attribute_value) @name)
  (#eq? @id_attr "ID"))
"""

try:
    query = Query(lang, query_scm)
    cursor = QueryCursor(query)
    captures = cursor.captures(tree.root_node)
    print("\nSymbol Captures:")
    for name, nodes in captures.items():
        for node in nodes:
            print(f"  {name}: {node.text.decode('utf-8')}")
except Exception as e:
    print(f"\nSymbol Query Error: {e}")
    
call_scm = """
(element
  (start_tag
    (tag_name) @tag
    (attribute
      (attribute_name) @attr_name
      (quoted_attribute_value
        (attribute_value) @callee)
      (#match? @attr_name "^(OnClick|OnLoad)$"))))
"""
try:
    query = Query(lang, call_scm)
    cursor = QueryCursor(query)
    captures = cursor.captures(tree.root_node)
    print("\nCall Captures:")
    for name, nodes in captures.items():
        for node in nodes:
            print(f"  {name}: {node.text.decode('utf-8')}")
except Exception as e:
    print(f"\nCall Query Error: {e}")
