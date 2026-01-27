; TypeScript symbol extraction

; Functions
(function_declaration name: (identifier) @name) @symbol
(generator_function_declaration name: (identifier) @name) @symbol
(arrow_function) @symbol

; Classes and interfaces
(class_declaration name: (type_identifier) @name) @symbol
(interface_declaration name: (type_identifier) @name) @symbol
(type_alias_declaration name: (type_identifier) @name) @symbol
(enum_declaration name: (identifier) @name) @symbol

; Methods
(method_definition name: (property_identifier) @name) @symbol
(method_signature name: (property_identifier) @name) @symbol

; Variables
(variable_declarator name: (identifier) @name) @symbol
