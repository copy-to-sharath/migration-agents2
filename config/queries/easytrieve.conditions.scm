; Easytrieve condition/control flow queries

; IF statements
(line
  (keyword) @_kw
  (#eq? @_kw "IF")) @definition.condition

; ELSE statements
(line
  (keyword) @_kw
  (#eq? @_kw "ELSE")) @definition.else

; END-IF
(line
  (keyword) @_kw
  (#eq? @_kw "END-IF")) @definition.endif

; WHEN (case-like)
(line
  (keyword) @_kw
  (#eq? @_kw "WHEN")) @definition.when
