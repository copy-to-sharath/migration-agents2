; CICS data access queries - file operations, queues, etc.

; READ file operations
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "READ")
  (option
    (keyword) @_key
    (#eq? @_key "FILE")
    (value) @file_name)) @definition.read

; WRITE file operations
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "WRITE")
  (option
    (keyword) @_key
    (#eq? @_key "FILE")
    (value) @file_name)) @definition.write

; REWRITE file operations
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "REWRITE")
  (option
    (keyword) @_key
    (#eq? @_key "FILE")
    (value) @file_name)) @definition.rewrite

; DELETE file operations
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "DELETE")
  (option
    (keyword) @_key
    (#eq? @_key "FILE")
    (value) @file_name)) @definition.delete

; STARTBR - Start browse
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "STARTBR")
  (option
    (keyword) @_key
    (#eq? @_key "FILE")
    (value) @file_name)) @definition.browse

; READQ TS - Temporary storage read
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "READQ")
  (option
    (keyword) @_key
    (#eq? @_key "QUEUE")
    (value) @queue_name)) @definition.readq

; WRITEQ TS - Temporary storage write
(exec_cics_block
  (command_name) @_cmd
  (#match? @_cmd "WRITEQ")
  (option
    (keyword) @_key
    (#eq? @_key "QUEUE")
    (value) @queue_name)) @definition.writeq
