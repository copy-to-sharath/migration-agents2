; Function call: function_name()
(function_call_expression
  (identifier) @callee) @call

; Method call: $obj->method()
(method_call_expression
  invocant: (_) @receiver
  method: (identifier) @callee) @call

; Package method call: Package::method()
(function_call_expression
  function: (package_name) @receiver
  function: (identifier) @callee) @call

; Constructor: Package->new()
(method_call_expression
  invocant: (bareword) @receiver
  method: (identifier) @callee) @call
