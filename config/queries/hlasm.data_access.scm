; HLASM data access queries
; Works with simplified grammar

; DC/DS statements define data
(statement
  (label) @data_name
  (operation) @op
  (#match? @op "^D[CS]$")
  (operands) @data_def) @data.definition

; DSECT statements define data structures
(statement
  (label) @dsect_name
  (operation) @op
  (#match? @op "^DSECT$")) @data.dsect
