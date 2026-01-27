; Easytrieve data access queries

; FILE definitions
(line
  (keyword) @_kw
  (#eq? @_kw "FILE")
  (token
    (identifier) @file_name)) @definition.file

; GET - Read from file
(line
  (keyword) @_kw
  (#eq? @_kw "GET")
  (token
    (identifier) @file_ref)?) @definition.read

; PUT - Write to file
(line
  (keyword) @_kw
  (#eq? @_kw "PUT")
  (token
    (identifier) @file_ref)?) @definition.write

; PRINT - Output
(line
  (keyword) @_kw
  (#eq? @_kw "PRINT")) @definition.print

; DISPLAY - Output
(line
  (keyword) @_kw
  (#eq? @_kw "DISPLAY")) @definition.display

; SORT - Sort operation
(line
  (keyword) @_kw
  (#eq? @_kw "SORT")) @definition.sort

; SUM - Aggregation
(line
  (keyword) @_kw
  (#eq? @_kw "SUM")) @definition.sum
