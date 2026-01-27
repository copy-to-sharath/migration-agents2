; BMS data structure queries
; BMS defines screen layouts which become COBOL copybooks

; DSECT type declaration - generates COBOL copybook
(bms_statement
  (macro_name) @_macro
  (#match? @_macro "DFHMSD")) @definition.dsect

; LANG parameter - target language for copybook
(parameter
  (param_name) @_key
  (#eq? @_key "LANG")
  (param_value) @language) @definition.language

; TYPE parameter
(parameter
  (param_name) @_key
  (#eq? @_key "TYPE")
  (param_value) @type_value) @definition.type

; Field definitions
(bms_statement
  (label) @field_name
  (macro_name) @_macro
  (#match? @_macro "DFHMDF")) @definition.data_field
