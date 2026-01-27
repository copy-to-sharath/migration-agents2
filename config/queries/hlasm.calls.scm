; HLASM call extraction queries
; Works with simplified grammar

; Branch/call instructions (operation contains the callee info in operands)
; Match operations that are typically calls: BAL, BALR, BAS, BASR, CALL, macro invocations
(statement
  (operation) @caller
  (operands) @operand_text) @call

; COPY statements  
(statement
  (operation) @op
  (#match? @op "^COPY$")
  (operands) @callee) @call.copy

; EXEC statements (CICS/SQL)
(statement
  (operation) @op
  (#match? @op "^EXEC$")
  (operands) @callee) @call.exec
