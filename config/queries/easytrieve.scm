; Tree-sitter queries for Easytrieve (simplified grammar)
; Captures report generation constructs

; Lines with keywords
(line
  (keyword) @keyword)

; FILE definitions
(line
  (keyword) @_kw
  (#eq? @_kw "FILE")
  (token
    (identifier) @name)) @definition.file

; JOB statements
(line
  (keyword) @_kw
  (#eq? @_kw "JOB")) @definition.job

; PROC statements (procedures)
(line
  (keyword) @_kw
  (#match? @_kw "PROC")
  (token
    (identifier) @name)?) @definition.proc

; Field definitions (field name followed by position, length, type)
(line
  (keyword) @field_name
  (token (number) @position)
  (token (number) @length)
  (token (identifier) @type)) @definition.field

; String literals
(token
  (string_literal) @literal.string)

; Numbers
(token
  (number) @literal.number)

; Identifiers
(token
  (identifier) @reference)
