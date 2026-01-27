; C# call extraction - minimal working version

; Method invocation: obj.Method() or Method()
(invocation_expression
  function: (member_access_expression
    name: (identifier) @callee)) @call

(invocation_expression
  function: (identifier) @callee) @call

; Object creation: new ClassName()
(object_creation_expression
  type: (_) @callee) @call

; Member access (property/field access)
(member_access_expression
  name: (identifier) @callee) @call
