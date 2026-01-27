; CICS constants and literal values

; String literals in CICS commands (program names, file names, etc.)
(value
  (string_literal) @constant.string)

; Numeric literals
(option
  (keyword) @_key
  (#match? @_key "LENGTH|KEYLENGTH|NUMREC")
  (value) @constant.number)
