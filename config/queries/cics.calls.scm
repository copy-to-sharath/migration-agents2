; CICS call extraction queries
; Captures CICS API calls for call graph building

; LINK - Call to another program
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "LINK")
  (option
    (keyword) @_key
    (#eq? @_key "PROGRAM")
    (value) @callee)) @call

; XCTL - Transfer control to program
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "XCTL")
  (option
    (keyword) @_key
    (#eq? @_key "PROGRAM")
    (value) @callee)) @call

; START - Start a transaction
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "START")
  (option
    (keyword) @_key
    (#eq? @_key "TRANSID")
    (value) @callee)) @call

; RETURN TRANSID - Return with transaction start
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "RETURN")
  (option
    (keyword) @_key
    (#eq? @_key "TRANSID")
    (value) @callee)) @call
