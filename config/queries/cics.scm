; Tree-sitter queries for CICS (simplified grammar)
; Captures EXEC CICS blocks, commands, and options

; Capture CICS command blocks
(exec_cics_block) @definition.cics_command

; Capture command names (LINK, READ, WRITE, SEND, etc.)
(exec_cics_block
  (command_name) @name) @definition.command

; Capture all options within CICS commands
(option
  (keyword) @name) @definition.option

; Capture values (strings, qualified names)
(value
  (string_literal) @literal)

(value
  (qualified_name) @reference)
