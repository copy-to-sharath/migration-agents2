; HLASM symbol extraction queries
; Works with simplified grammar

; Labeled statements (CSECT, DSECT, START, ENTRY, EQU, DC, DS, etc.)
(statement
  (label) @name
  (operation) @kind) @definition.symbol

; All labels are potential entry points or data definitions
(statement
  (label) @name) @definition.label
