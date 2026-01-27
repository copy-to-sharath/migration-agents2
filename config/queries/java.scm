; Java symbol extraction - minimal working version

; Classes and interfaces
(class_declaration name: (identifier) @name) @symbol
(interface_declaration name: (identifier) @name) @symbol
(enum_declaration name: (identifier) @name) @symbol
(record_declaration name: (identifier) @name) @symbol
(annotation_type_declaration name: (identifier) @name) @symbol

; Methods and constructors
(method_declaration name: (identifier) @name) @symbol
(constructor_declaration name: (identifier) @name) @symbol

; Fields
(field_declaration
  declarator: (variable_declarator name: (identifier) @name)) @symbol
