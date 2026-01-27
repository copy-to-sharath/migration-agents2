; CICS condition/exception handling queries

; HANDLE CONDITION - Exception handlers
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "HANDLE")
  (option
    (keyword) @condition)) @definition.handler

; IGNORE CONDITION
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "IGNORE")) @definition.ignore

; RESP/RESP2 options for inline error checking
(option
  (keyword) @_key
  (#match? @_key "RESP")
  (value) @resp_var) @definition.resp_check
