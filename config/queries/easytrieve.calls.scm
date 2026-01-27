; Easytrieve call/procedure invocation queries

; PERFORM - Call a procedure
(line
  (keyword) @_kw
  (#eq? @_kw "PERFORM")
  (token
    (identifier) @callee)) @call

; DO - Loop/call construct
(line
  (keyword) @_kw
  (#eq? @_kw "DO")
  (token
    (identifier) @callee)?) @call
