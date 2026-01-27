; JavaScript symbol extraction

; Functions
(function_declaration name: (identifier) @name) @symbol
(generator_function_declaration name: (identifier) @name) @symbol
(arrow_function) @symbol

; Classes
(class_declaration name: (identifier) @name) @symbol
(method_definition name: (property_identifier) @name) @symbol

; Variables
(variable_declarator name: (identifier) @name) @symbol
(lexical_declaration (variable_declarator name: (identifier) @name)) @symbol
