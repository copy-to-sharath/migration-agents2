; BMS condition-like attributes
; Captures field attributes that affect display/input behavior

; Field attributes (ASKIP, UNPROT, BRT, DRK, etc.)
(parameter
  (param_name) @_key
  (#eq? @_key "ATTRB")
  (param_list) @attributes) @definition.field_attrs

; INITIAL value (default text)
(parameter
  (param_name) @_key
  (#eq? @_key "INITIAL")
  (param_value) @initial_value) @definition.initial
