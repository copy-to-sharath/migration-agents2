; C# symbol extraction - minimal working version

; Classes, structs, interfaces, enums
(class_declaration name: (identifier) @name) @symbol
(struct_declaration name: (identifier) @name) @symbol
(interface_declaration name: (identifier) @name) @symbol
(enum_declaration name: (identifier) @name) @symbol
(record_declaration name: (identifier) @name) @symbol

; Methods and constructors
(method_declaration name: (identifier) @name) @symbol
(constructor_declaration name: (identifier) @name) @symbol

; Properties
(property_declaration name: (identifier) @name) @symbol

; Fields
(field_declaration
  (variable_declaration
    (variable_declarator (identifier) @name))) @symbol

; Namespaces
(namespace_declaration name: (_) @name) @symbol

; Delegates and events
(delegate_declaration name: (identifier) @name) @symbol
(event_declaration name: (identifier) @name) @symbol
(event_field_declaration) @symbol
