; Tree-sitter queries for BMS (Basic Mapping Support)
; Captures screen definitions for CICS terminals

; Map Set definitions (DFHMSD)
(bms_statement
  (macro_name) @_macro
  (#match? @_macro "DFHMSD")
  (label)? @name) @definition.mapset

; Map definitions (DFHMDI)
(bms_statement
  (macro_name) @_macro
  (#match? @_macro "DFHMDI")
  (label)? @name) @definition.map

; Field definitions (DFHMDF)
(bms_statement
  (macro_name) @_macro
  (#match? @_macro "DFHMDF")
  (label)? @name) @definition.field

; All labels
(bms_statement
  (label) @name)

; All parameters
(parameter
  (param_name) @param_key
  (param_value) @param_value)

; List parameters (like SIZE=(24,80))
(parameter
  (param_name) @param_key
  (param_list) @param_list)
