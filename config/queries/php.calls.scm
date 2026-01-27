; Function call: function_name()
(function_call_expression
  function: (name) @callee) @call

; Method call: $obj->method() - capture receiver
(member_call_expression
  object: (_) @receiver
  name: (name) @callee) @call

; Static call: ClassName::method()
(scoped_call_expression
  scope: (name) @receiver
  name: (name) @callee) @call

; Object creation: new ClassName()
(object_creation_expression
  (name) @callee) @call
