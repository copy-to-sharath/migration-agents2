; BMS constants and literals

; String literals (INITIAL values, etc.)
(param_value
  (string_literal) @constant.string)

; Numeric values (positions, lengths)
(param_value
  (number) @constant.number)

; Position parameters
(parameter
  (param_name) @_key
  (#eq? @_key "POS")
  (param_list) @constant.position)

; Length parameters
(parameter
  (param_name) @_key
  (#eq? @_key "LENGTH")
  (param_value) @constant.length)

; Size parameters (screen dimensions)
(parameter
  (param_name) @_key
  (#eq? @_key "SIZE")
  (param_list) @constant.size)
