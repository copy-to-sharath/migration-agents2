"""Lightweight semantic analysis built on tree-sitter syntax trees.

This module provides type resolution without requiring Roslyn or a full compiler.
It works by:
1. Building a symbol table from declarations
2. Tracking variable/field types from declarations
3. Following using/import statements
4. Building class hierarchy from inheritance
5. Resolving calls using accumulated context
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from tree_sitter import Language, Node, Query, QueryCursor


@dataclass
class TypeInfo:
    """Represents a resolved type."""
    name: str
    namespace: str = ""
    is_generic: bool = False
    type_args: list[str] = field(default_factory=list)
    
    @property
    def qualified_name(self) -> str:
        if self.namespace:
            return f"{self.namespace}.{self.name}"
        return self.name


@dataclass
class SymbolInfo:
    """Symbol with type information."""
    symbol_id: str
    name: str
    kind: str  # class, method, field, property, variable
    type_info: TypeInfo | None
    file_path: str
    line: int
    parent_class: str = ""
    base_class: str = ""
    interfaces: list[str] = field(default_factory=list)


@dataclass
class FileContext:
    """Semantic context for a single file."""
    file_path: str
    imports: list[str] = field(default_factory=list)  # using statements
    classes: dict[str, SymbolInfo] = field(default_factory=dict)
    fields: dict[str, TypeInfo] = field(default_factory=dict)  # field_name -> type
    variables: dict[str, TypeInfo] = field(default_factory=dict)  # var_name -> type
    class_hierarchy: dict[str, str] = field(default_factory=dict)  # class -> base_class


@dataclass
class SemanticContext:
    """Global semantic context across all files."""
    files: dict[str, FileContext] = field(default_factory=dict)
    symbol_table: dict[str, SymbolInfo] = field(default_factory=dict)  # qualified_name -> symbol
    class_to_file: dict[str, str] = field(default_factory=dict)  # class_name -> file_path
    

# Tree-sitter queries for semantic extraction
CSHARP_SEMANTIC_QUERIES = {
    "imports": """
        (using_directive
          (qualified_name) @import)
        (using_directive
          (identifier) @import)
        (using_directive
          name: (qualified_name) @import)
    """,
    
    "class_declarations": """
        (class_declaration
          name: (identifier) @class_name
          bases: (base_list
            (identifier) @base_class)?
          bases: (base_list
            (qualified_name) @base_class)?)
        
        (interface_declaration
          name: (identifier) @class_name
          bases: (base_list
            (identifier) @base_class)?)
        
        (struct_declaration
          name: (identifier) @class_name
          bases: (base_list
            (identifier) @base_class)?)
        
        (record_declaration
          name: (identifier) @class_name
          bases: (base_list
            (identifier) @base_class)?)
        
        (enum_declaration
          name: (identifier) @class_name)
        
        (delegate_declaration
          name: (identifier) @class_name
          return_type: (_) @return_type)
    """,
    
    "field_declarations": """
        (field_declaration
          type: (_) @field_type
          (variable_declaration
            (variable_declarator
              name: (identifier) @field_name)))
        
        (event_field_declaration
          type: (_) @field_type
          (variable_declaration
            (variable_declarator
              name: (identifier) @field_name)))
        
        (constant_declaration
          type: (_) @field_type
          (variable_declaration
            (variable_declarator
              name: (identifier) @field_name)))
    """,
    
    "property_declarations": """
        (property_declaration
          type: (_) @prop_type
          name: (identifier) @prop_name)
        
        (indexer_declaration
          type: (_) @prop_type)
        
        (event_declaration
          type: (_) @prop_type
          name: (identifier) @prop_name)
    """,
    
    "variable_declarations": """
        (local_declaration_statement
          (variable_declaration
            type: (_) @var_type
            (variable_declarator
              name: (identifier) @var_name
              (equals_value_clause
                value: (_) @var_value)?)))
        
        (for_each_statement
          type: (_) @var_type
          left: (identifier) @var_name)
        
        (catch_clause
          (catch_declaration
            type: (_) @var_type
            name: (identifier) @var_name))
    """,
    
    "method_declarations": """
        (method_declaration
          returns: (_) @return_type
          name: (identifier) @method_name
          parameters: (parameter_list
            (parameter
              type: (_) @param_type
              name: (identifier) @param_name)*)?)
        
        (local_function_statement
          returns: (_) @return_type
          name: (identifier) @method_name)
        
        (constructor_declaration
          name: (identifier) @method_name
          parameters: (parameter_list
            (parameter
              type: (_) @param_type
              name: (identifier) @param_name)*)?)
        
        (destructor_declaration
          name: (identifier) @method_name)
        
        (operator_declaration
          type: (_) @return_type)
    """,
}

PYTHON_SEMANTIC_QUERIES = {
    "imports": """
        (import_statement
          name: (dotted_name) @import)
        (import_from_statement
          module_name: (dotted_name) @import)
    """,
    
    "class_declarations": """
        (class_definition
          name: (identifier) @class_name
          superclasses: (argument_list
            (identifier) @base_class)?)
    """,
    
    "field_declarations": """
        (expression_statement
          (assignment
            left: (attribute
              object: (identifier) @self_ref
              attribute: (identifier) @field_name)
            type: (type)? @field_type))
    """,
    
    "variable_declarations": """
        (assignment
          left: (identifier) @var_name
          type: (type)? @var_type)
    """,
    
    "method_declarations": """
        (function_definition
          name: (identifier) @method_name
          parameters: (parameters
            (typed_parameter
              name: (identifier) @param_name
              type: (type) @param_type)?)*
          return_type: (type)? @return_type)
    """,
}

JAVA_SEMANTIC_QUERIES = {
    "imports": """
        (import_declaration
          (scoped_identifier) @import)
        (import_declaration
          (identifier) @import)
        (package_declaration
          (scoped_identifier) @import)
    """,
    
    "class_declarations": """
        (class_declaration
          name: (identifier) @class_name
          superclass: (superclass
            (type_identifier) @base_class)?
          interfaces: (super_interfaces
            (type_list
              (type_identifier) @interface_name))?)
        
        (interface_declaration
          name: (identifier) @class_name
          (extends_interfaces
            (type_list
              (type_identifier) @base_class))?)
        
        (enum_declaration
          name: (identifier) @class_name
          interfaces: (super_interfaces
            (type_list
              (type_identifier) @interface_name))?)
        
        (record_declaration
          name: (identifier) @class_name
          interfaces: (super_interfaces
            (type_list
              (type_identifier) @interface_name))?)
        
        (annotation_type_declaration
          name: (identifier) @class_name)
    """,
    
    "field_declarations": """
        (field_declaration
          type: (_) @field_type
          declarator: (variable_declarator
            name: (identifier) @field_name))
        
        (enum_constant
          name: (identifier) @field_name)
        
        (annotation_type_element_declaration
          type: (_) @field_type
          name: (identifier) @field_name)
    """,
    
    "variable_declarations": """
        (local_variable_declaration
          type: (_) @var_type
          declarator: (variable_declarator
            name: (identifier) @var_name))
        
        (enhanced_for_statement
          type: (_) @var_type
          name: (identifier) @var_name)
        
        (catch_clause
          (catch_formal_parameter
            (catch_type) @var_type
            name: (identifier) @var_name))
        
        (try_with_resources_statement
          resources: (resource_specification
            (resource
              type: (_) @var_type
              name: (identifier) @var_name)))
        
        (lambda_expression
          parameters: (inferred_parameters
            (identifier) @var_name))
    """,
    
    "method_declarations": """
        (method_declaration
          type: (_) @return_type
          name: (identifier) @method_name
          parameters: (formal_parameters
            (formal_parameter
              type: (_) @param_type
              name: (identifier) @param_name)*)?)
        
        (constructor_declaration
          name: (identifier) @method_name
          parameters: (formal_parameters
            (formal_parameter
              type: (_) @param_type
              name: (identifier) @param_name)*)?)
        
        (static_initializer
          (block)) @method_name
        
        (instance_initializer
          (block)) @method_name
    """,
}

TYPESCRIPT_SEMANTIC_QUERIES = {
    "imports": """
        (import_statement
          (import_clause
            (named_imports
              (import_specifier
                name: (identifier) @import))))
        (import_statement
          source: (string) @import_source)
    """,
    
    "class_declarations": """
        (class_declaration
          name: (type_identifier) @class_name
          (class_heritage
            (extends_clause
              value: (identifier) @base_class))?
          (class_heritage
            (implements_clause
              (type_identifier) @interface_name))?)
        
        (interface_declaration
          name: (type_identifier) @class_name
          (extends_type_clause
            (type_identifier) @base_class)?)
        
        (type_alias_declaration
          name: (type_identifier) @class_name)
        
        (enum_declaration
          name: (identifier) @class_name)
    """,
    
    "field_declarations": """
        (public_field_definition
          name: (property_identifier) @field_name
          type: (type_annotation
            (_) @field_type)?)
    """,
    
    "variable_declarations": """
        (variable_declaration
          name: (identifier) @var_name
          type: (type_annotation
            (_) @var_type)?)
    """,
    
    "method_declarations": """
        (method_definition
          name: (property_identifier) @method_name
          return_type: (type_annotation
            (_) @return_type)?)
    """,
}

PHP_SEMANTIC_QUERIES = {
    "imports": """
        (namespace_use_declaration
          (namespace_use_clause
            (qualified_name) @import))
    """,
    
    "class_declarations": """
        (class_declaration
          name: (name) @class_name
          (base_clause
            (name) @base_class)?
          (class_interface_clause
            (name) @interface_name)?)
    """,
    
    "field_declarations": """
        (property_declaration
          (property_element
            (variable_name) @field_name)
          type: (type_list)? @field_type)
    """,
    
    "variable_declarations": """
        (simple_parameter
          name: (variable_name) @var_name
          type: (type_list)? @var_type)
    """,
    
    "method_declarations": """
        (method_declaration
          name: (name) @method_name
          return_type: (return_type)? @return_type)
    """,
}

PERL_SEMANTIC_QUERIES = {
    "imports": """
        (use_statement
          (package_name) @import)
        (require_statement
          (bareword) @import)
    """,
    
    "class_declarations": """
        (package_statement
          (package_name) @class_name)
    """,
    
    "field_declarations": """
        (hash_element_expression
          key: (string) @field_name)
    """,
    
    "variable_declarations": """
        (variable_declaration
          (scalar) @var_name)
    """,
    
    "method_declarations": """
        (subroutine_declaration
          name: (identifier) @method_name)
    """,
}

COBOL_SEMANTIC_QUERIES = {
    "imports": """
        ; COPY statements
        (copy_statement
          (qualified_word) @import)
        ; EXEC SQL INCLUDE
        (exec_sql_include
          (identifier) @import)
    """,
    
    "class_declarations": """
        ; Program identification
        (program_id_paragraph
          (qualified_word) @class_name)
        ; OO COBOL classes
        (class_id_paragraph
          (qualified_word) @class_name)
        ; Factory/Object definitions
        (factory_paragraph
          (qualified_word) @class_name)
        (object_paragraph
          (qualified_word) @class_name)
    """,
    
    "field_declarations": """
        ; Data descriptions with PICTURE
        (data_description
          name: (qualified_word) @field_name
          picture: (_)? @field_type)
        ; Level 01 records
        (data_description
          level: (level_number) @level
          name: (qualified_word) @field_name
          (#eq? @level "01"))
        ; File section FDs
        (file_description
          (qualified_word) @field_name)
        ; Index definitions
        (indexed_by
          (qualified_word) @field_name)
        ; 88-level condition names
        (condition_value
          (qualified_word) @field_name)
    """,
    
    "variable_declarations": """
        ; Working-storage variables
        (working_storage_section
          (data_description
            name: (qualified_word) @var_name))
        ; Local-storage variables
        (local_storage_section
          (data_description
            name: (qualified_word) @var_name))
        ; Linkage section parameters
        (linkage_section
          (data_description
            name: (qualified_word) @var_name))
        ; File status variables
        (file_status
          (qualified_word) @var_name)
        ; SPECIAL-NAMES conditions
        (special_names_paragraph
          (mnemonic_name) @var_name)
    """,
    
    "method_declarations": """
        ; Section headers (major procedures)
        (section_header
          (word) @method_name)
        ; Paragraph names
        (paragraph
          (word) @method_name)
        ; ENTRY points
        (entry_statement
          (string) @method_name)
        ; OO COBOL methods
        (method_id_paragraph
          (qualified_word) @method_name)
    """,
}

JCL_SEMANTIC_QUERIES = {
    "imports": """
        ; INCLUDE statements
        (include_statement
          (dataset_name) @import)
        ; JCLLIB for procedure search
        (jcllib_statement
          (dataset_name) @import)
        ; Cataloged procedure references
        (cataloged_proc_call
          (proc_name) @import)
    """,
    
    "class_declarations": """
        ; JOB card defines the unit of work
        (job_statement
          (job_name) @class_name)
        ; PROC definitions
        (proc_statement
          (proc_name) @class_name)
    """,
    
    "field_declarations": """
        ; DD statements define datasets
        (dd_statement
          (dd_name) @field_name
          (dataset_name)? @field_type)
        ; STEPLIB datasets
        (dd_statement
          (dd_name) @field_name
          (#eq? @field_name "STEPLIB"))
        ; GDG definitions
        (gdg_definition
          (dataset_name) @field_name)
    """,
    
    "variable_declarations": """
        ; SET statement symbolics
        (set_statement
          (symbolic_name) @var_name
          (symbolic_value) @var_type)
        ; Symbolic parameters
        (symbolic_parameter
          (parameter_name) @var_name)
        ; PROC parameters
        (proc_parm
          (parameter_name) @var_name
          (parameter_value) @var_type)
    """,
    
    "method_declarations": """
        ; EXEC PGM - program execution
        (exec_statement
          (exec_pgm
            (program_name) @method_name))
        ; EXEC PROC - procedure execution
        (exec_statement
          (exec_proc
            (proc_name) @method_name))
        ; Step names
        (step_name) @method_name
    """,
}

CICS_SEMANTIC_QUERIES = {
    "imports": """
        ; COPY statements for BMS maps
        (copy_statement
          (qualified_word) @import)
        ; EXEC SQL INCLUDE
        (exec_sql_include
          (identifier) @import)
        ; CICS LOAD programs
        (cics_load
          (load_program
            (program_name) @import))
    """,
    
    "class_declarations": """
        ; Program identification
        (program_id_paragraph
          (qualified_word) @class_name)
        ; Transaction IDs
        (return_transid
          (transaction_id) @class_name)
    """,
    
    "field_declarations": """
        ; COBOL data descriptions
        (data_description
          name: (qualified_word) @field_name)
        ; Commarea fields
        (data_description
          name: (qualified_word) @field_name
          (#match? @field_name "^(DFHCOMMAREA|WS-COMMAREA)"))
        ; BMS map fields
        (data_description
          name: (qualified_word) @field_name
          (#match? @field_name ".*I$|.*O$"))
    """,
    
    "variable_declarations": """
        ; Working-storage
        (working_storage_section
          (data_description
            name: (qualified_word) @var_name))
        ; EIB (Exec Interface Block) references
        (eib_field) @var_name
        ; Container data areas
        (get_container_into
          (identifier) @var_name)
    """,
    
    "method_declarations": """
        ; Section headers
        (section_header
          (word) @method_name)
        ; Paragraph names
        (paragraph
          (word) @method_name)
        ; CICS LINK targets
        (cics_link
          (link_program
            (program_name) @method_name))
        ; CICS XCTL targets
        (cics_xctl
          (xctl_program
            (program_name) @method_name))
    """,
}

BMS_SEMANTIC_QUERIES = {
    "imports": """
        ; No direct imports in BMS - maps are assembled
    """,
    
    "class_declarations": """
        ; MAPSET defines the overall structure (like a class)
        (dfhmsd
          name: (mapset_name) @class_name)
        (mapset_definition
          (mapset_name) @class_name)
    """,
    
    "field_declarations": """
        ; DFHMDF defines screen fields
        (dfhmdf
          name: (field_name) @field_name)
        (field_definition
          (field_name) @field_name)
        ; Field with attributes
        (dfhmdf
          name: (field_name) @field_name
          (dfhmdf_attrb)? @field_type)
        ; Field with position
        (dfhmdf
          name: (field_name) @field_name
          (dfhmdf_pos) @field_pos)
    """,
    
    "variable_declarations": """
        ; Field initial values
        (dfhmdf
          name: (field_name) @var_name
          (dfhmdf_initial
            (_) @var_type))
        ; Symbolic cursor positioning
        (dfhmdf
          name: (field_name) @var_name
          (dfhmdf_cursor))
    """,
    
    "method_declarations": """
        ; MAPs define logical screen sections (like methods)
        (dfhmdi
          name: (map_name) @method_name)
        (map_definition
          (map_name) @method_name)
    """,
}

EASYTRIEVE_SEMANTIC_QUERIES = {
    "imports": """
        ; Library includes
        (library_include
          (member_name) @import)
        ; SQL includes
        (exec_sql_include
          (identifier) @import)
    """,
    
    "class_declarations": """
        ; Program identification
        (program_statement
          (program_name) @class_name)
        ; JOB names
        (job_statement
          name: (job_name) @class_name)
    """,
    
    "field_declarations": """
        ; Field definitions
        (field_definition
          name: (field_name) @field_name)
        ; Field with type
        (field_definition
          name: (field_name) @field_name
          (field_type) @field_type)
        ; Working storage fields
        (w_field
          (field_name) @field_name)
        (working_field
          (field_name) @field_name)
    """,
    
    "variable_declarations": """
        ; Working storage definitions
        (working_storage
          (field_definition
            name: (field_name) @var_name))
        ; Parm values
        (parm_statement
          (parm_option) @var_name)
        ; Macro variables
        (macro_definition
          (macro_name) @var_name)
    """,
    
    "method_declarations": """
        ; FILE definitions (like classes)
        (file_statement
          name: (file_name) @method_name)
        ; PROC definitions
        (proc_statement
          name: (proc_name) @method_name)
        ; SORT statements
        (sort_statement
          (sort_name) @method_name)
        ; REPORT definitions
        (report_statement
          (report_name) @method_name)
    """,
}

SQL_SEMANTIC_QUERIES = {
    "imports": """
        (use_statement
          (identifier) @import)
    """,
    
    "class_declarations": """
        (create_table_statement
          name: (identifier) @class_name)
        (create_view_statement
          name: (identifier) @class_name)
    """,
    
    "field_declarations": """
        (column_definition
          name: (identifier) @field_name
          type: (_) @field_type)
    """,
    
    "variable_declarations": """
        (declare_statement
          (identifier) @var_name
          (data_type) @var_type)
    """,
    
    "method_declarations": """
        (create_procedure_statement
          name: (identifier) @method_name)
        (create_function_statement
          name: (identifier) @method_name)
    """,
}

CSS_SEMANTIC_QUERIES = {
    "imports": """
        (import_statement
          (string_value) @import)
    """,
    
    "class_declarations": """
        (rule_set
          (selectors
            (class_selector
              (class_name) @class_name)))
    """,
    
    "field_declarations": """
        (declaration
          (property_name) @field_name
          (property_value) @field_type)
    """,
    
    "variable_declarations": """
        (declaration
          (property_name) @var_name
          (#match? @var_name "^--"))
    """,
    
    "method_declarations": """
        (call_expression
          (function_name) @method_name)
    """,
}

HTML_SEMANTIC_QUERIES = {
    "imports": """
        (element
          (start_tag
            (tag_name) @tag
            (attribute
              (attribute_name) @attr
              (quoted_attribute_value
                (attribute_value) @import))
            (#eq? @tag "script")
            (#eq? @attr "src")))
        (element
          (self_closing_tag
            (tag_name) @tag
            (attribute
              (attribute_name) @attr
              (quoted_attribute_value
                (attribute_value) @import))
            (#eq? @tag "link")
            (#eq? @attr "href")))
    """,
    
    "class_declarations": """
        (element
          (start_tag
            (attribute
              (attribute_name) @attr
              (quoted_attribute_value
                (attribute_value) @class_name))
            (#eq? @attr "id")))
    """,
    
    "field_declarations": """
        (element
          (start_tag
            (attribute
              (attribute_name) @field_name
              (quoted_attribute_value
                (attribute_value) @field_type))))
    """,
    
    "variable_declarations": """
        (element
          (start_tag
            (attribute
              (attribute_name) @attr
              (quoted_attribute_value
                (attribute_value) @var_name))
            (#match? @attr "^(runat|id|name)$")))
    """,
    
    "method_declarations": """
        (element
          (start_tag
            (attribute
              (attribute_name) @attr
              (quoted_attribute_value
                (attribute_value) @method_name))
            (#match? @attr "^On")))
    """,
}

XML_SEMANTIC_QUERIES = {
    "imports": """
        (attribute
          (attribute_name) @attr
          (attribute_value) @import
          (#match? @attr "^(schemaLocation|xmlns)"))
    """,
    
    "class_declarations": """
        (element
          (start_tag
            (tag_name) @class_name))
    """,
    
    "field_declarations": """
        (attribute
          (attribute_name) @field_name
          (attribute_value) @field_type)
    """,
    
    "variable_declarations": """
        (element
          (start_tag
            (tag_name) @var_name)
          (text) @var_type)
    """,
    
    "method_declarations": """
        (processing_instruction
          (tag_name) @method_name)
    """,
}

# Map language names to their query sets
LANGUAGE_QUERIES = {
    # Modern languages
    "c_sharp": CSHARP_SEMANTIC_QUERIES,
    "vbnet": CSHARP_SEMANTIC_QUERIES,  # Similar structure
    "python": PYTHON_SEMANTIC_QUERIES,
    "java": JAVA_SEMANTIC_QUERIES,
    "typescript": TYPESCRIPT_SEMANTIC_QUERIES,
    "javascript": TYPESCRIPT_SEMANTIC_QUERIES,  # Similar structure
    "php": PHP_SEMANTIC_QUERIES,
    "perl": PERL_SEMANTIC_QUERIES,
    # Database
    "sql": SQL_SEMANTIC_QUERIES,
    # Mainframe
    "cobol": COBOL_SEMANTIC_QUERIES,
    "jcl": JCL_SEMANTIC_QUERIES,
    "cics": CICS_SEMANTIC_QUERIES,
    "bms": BMS_SEMANTIC_QUERIES,
    "easytrieve": EASYTRIEVE_SEMANTIC_QUERIES,
    # Markup/Config
    "css": CSS_SEMANTIC_QUERIES,
    "html": HTML_SEMANTIC_QUERIES,
    "xml": XML_SEMANTIC_QUERIES,
}


def _node_text(node: Node) -> str:
    """Extract text from a tree-sitter node."""
    try:
        return node.text.decode("utf-8", errors="ignore")
    except AttributeError:
        return ""


def _hash_id(text: str) -> str:
    """Create a stable hash ID."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_type(type_node: Node) -> TypeInfo:
    """Parse a type node into TypeInfo."""
    text = _node_text(type_node)
    
    # Handle generic types: List<T>, Dictionary<K, V>
    generic_match = re.match(r"(\w+)<(.+)>", text)
    if generic_match:
        name = generic_match.group(1)
        args = [a.strip() for a in generic_match.group(2).split(",")]
        return TypeInfo(name=name, is_generic=True, type_args=args)
    
    # Handle qualified names: Namespace.ClassName
    if "." in text:
        parts = text.rsplit(".", 1)
        return TypeInfo(name=parts[1], namespace=parts[0])
    
    # Handle nullable: string?
    if text.endswith("?"):
        return TypeInfo(name=text[:-1])
    
    # Simple type
    return TypeInfo(name=text)


def extract_file_context(
    language: Language,
    tree,
    file_path: str,
    language_name: str = "c_sharp",
) -> FileContext:
    """Extract semantic context from a single file."""
    ctx = FileContext(file_path=file_path)
    
    # Get language-specific queries (fallback to C# if not found)
    queries = LANGUAGE_QUERIES.get(language_name, CSHARP_SEMANTIC_QUERIES)
    
    # Extract imports
    try:
        import_query = Query(language, queries["imports"])
        cursor = QueryCursor(import_query)
        captures = cursor.captures(tree.root_node)
        for node in captures.get("import", []):
            ctx.imports.append(_node_text(node))
    except Exception:
        pass  # Query may not be valid for this language
    
    # Extract class declarations with inheritance
    try:
        class_query = Query(language, queries["class_declarations"])
        cursor = QueryCursor(class_query)
        captures = cursor.captures(tree.root_node)
        
        class_nodes = captures.get("class_name", [])
        base_nodes = captures.get("base_class", [])
        
        for node in class_nodes:
            class_name = _node_text(node)
            line = node.start_point[0] + 1
            symbol_id = _hash_id(f"{file_path}:{class_name}:{line}")
            
            # Find base class (simplified - matches by proximity)
            base_class = ""
            for base_node in base_nodes:
                if abs(base_node.start_point[0] - node.start_point[0]) < 5:
                    base_class = _node_text(base_node)
                    break
            
            ctx.classes[class_name] = SymbolInfo(
                symbol_id=symbol_id,
                name=class_name,
                kind="class",
                type_info=TypeInfo(name=class_name),
                file_path=file_path,
                line=line,
                base_class=base_class,
            )
            ctx.class_hierarchy[class_name] = base_class
    except Exception:
        pass
    
    # Extract field declarations
    try:
        field_query = Query(language, queries["field_declarations"])
        cursor = QueryCursor(field_query)
        captures = cursor.captures(tree.root_node)
        
        type_nodes = captures.get("field_type", [])
        name_nodes = captures.get("field_name", [])
        
        for type_node, name_node in zip(type_nodes, name_nodes):
            field_name = _node_text(name_node)
            field_type = _parse_type(type_node)
            ctx.fields[field_name] = field_type
    except Exception:
        pass
    
    # Extract variable declarations with types
    try:
        var_query = Query(language, queries["variable_declarations"])
        cursor = QueryCursor(var_query)
        captures = cursor.captures(tree.root_node)
        
        type_nodes = captures.get("var_type", [])
        name_nodes = captures.get("var_name", [])
        
        for type_node, name_node in zip(type_nodes, name_nodes):
            var_name = _node_text(name_node)
            var_type_text = _node_text(type_node)
            
            # Skip 'var' - would need inference
            if var_type_text != "var":
                ctx.variables[var_name] = _parse_type(type_node)
    except Exception:
        pass
    
    return ctx


def build_semantic_context(file_contexts: Iterable[FileContext]) -> SemanticContext:
    """Build global semantic context from all file contexts."""
    ctx = SemanticContext()
    
    for file_ctx in file_contexts:
        ctx.files[file_ctx.file_path] = file_ctx
        
        # Index classes
        for class_name, symbol in file_ctx.classes.items():
            ctx.symbol_table[class_name] = symbol
            ctx.class_to_file[class_name] = file_ctx.file_path
            
            # Also index with full file path for disambiguation
            file_base = Path(file_ctx.file_path).stem
            ctx.symbol_table[f"{file_base}.{class_name}"] = symbol
    
    return ctx


def resolve_call_type(
    receiver: str,
    method_name: str,
    file_context: FileContext,
    global_context: SemanticContext,
) -> str | None:
    """Resolve a method call to its target symbol ID.
    
    Args:
        receiver: The receiver expression (e.g., "_customerManager", "CustomerManager")
        method_name: The method being called (e.g., "GetById")
        file_context: Semantic context for the current file
        global_context: Global semantic context
        
    Returns:
        Symbol ID if resolved, None otherwise
    """
    # Strategy 1: Receiver is a type name (static call)
    if receiver and receiver[0].isupper():
        qualified = f"{receiver}.{method_name}"
        if qualified in global_context.symbol_table:
            return global_context.symbol_table[qualified].symbol_id
    
    # Strategy 2: Receiver is a field - look up field type
    if receiver in file_context.fields:
        field_type = file_context.fields[receiver]
        qualified = f"{field_type.name}.{method_name}"
        if qualified in global_context.symbol_table:
            return global_context.symbol_table[qualified].symbol_id
    
    # Strategy 3: Receiver is a variable - look up variable type
    # Handle underscore prefix convention
    receiver_clean = receiver.lstrip("_")
    for var_name, var_type in file_context.variables.items():
        if var_name == receiver or var_name == receiver_clean:
            qualified = f"{var_type.name}.{method_name}"
            if qualified in global_context.symbol_table:
                return global_context.symbol_table[qualified].symbol_id
    
    # Strategy 4: Try field with underscore stripped
    for field_name, field_type in file_context.fields.items():
        if field_name.lstrip("_") == receiver_clean:
            qualified = f"{field_type.name}.{method_name}"
            if qualified in global_context.symbol_table:
                return global_context.symbol_table[qualified].symbol_id
    
    # Strategy 5: Try import resolution
    for imp in file_context.imports:
        # Check if import ends with a class name that has our method
        qualified = f"{imp}.{method_name}"
        if qualified in global_context.symbol_table:
            return global_context.symbol_table[qualified].symbol_id
        # Check just the last part of the import
        parts = imp.split(".")
        if parts:
            qualified = f"{parts[-1]}.{method_name}"
            if qualified in global_context.symbol_table:
                return global_context.symbol_table[qualified].symbol_id
    
    # Strategy 6: Search for method in base classes
    for class_name, class_info in file_context.classes.items():
        if class_info.base_class:
            qualified = f"{class_info.base_class}.{method_name}"
            if qualified in global_context.symbol_table:
                return global_context.symbol_table[qualified].symbol_id
    
    return None


def resolve_method_calls(
    calls: list[dict],
    file_context: FileContext,
    global_context: SemanticContext,
) -> list[dict]:
    """Resolve method calls to their actual symbol IDs.
    
    Args:
        calls: List of call dictionaries with receiver/callee_name
        file_context: Semantic context for the current file
        global_context: Global semantic context
        
    Returns:
        Updated calls with resolved callee_ids where possible
    """
    resolved = []
    for call in calls:
        receiver = call.get("receiver", "")
        callee_name = call.get("callee_name", "")
        
        if receiver and callee_name:
            resolved_id = resolve_call_type(
                receiver, callee_name, file_context, global_context
            )
            if resolved_id:
                call = dict(call)
                call["callee_id"] = resolved_id
                call["resolved"] = True
        
        resolved.append(call)
    
    return resolved
