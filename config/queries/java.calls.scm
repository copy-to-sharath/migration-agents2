; Java call extraction

; Method invocation
(method_invocation name: (identifier) @callee) @call

; Object creation
(object_creation_expression type: (_) @callee) @call

; Field access
(field_access field: (identifier) @callee) @call
