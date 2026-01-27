; Syntax highlighting queries for JCL

; Comments
(comment) @comment

; Keywords
"JOB" @keyword
"EXEC" @keyword
"DD" @keyword
"PROC" @keyword
"PEND" @keyword
"IF" @keyword
"ELSE" @keyword
"ENDIF" @keyword
"SET" @keyword
"INCLUDE" @keyword
"JCLLIB" @keyword

; Special keywords
"PGM" @keyword.special
"DSN" @keyword.special
"DISP" @keyword.special
"DUMMY" @keyword.special

; Identifiers
(name) @variable
(program_name) @function
(proc_name) @function
(dataset_name) @string.special

; Strings and parameters
(quoted_string) @string
(simple_value) @constant

; Operators
"=" @operator
"," @punctuation.delimiter
"(" @punctuation.bracket
")" @punctuation.bracket

; Labels
"//" @punctuation.special