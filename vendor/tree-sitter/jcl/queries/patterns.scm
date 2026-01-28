
; Pattern: Program execution with parameters
(exec_statement
  (label
    (name) @program_exec.step)
  (program_name) @program_exec.name
  (parameter
    (keyword) @_parm_keyword
    (#eq? @_parm_keyword "PARM")
    (parameter_value) @program_exec.parameters))

; Pattern: Conditional execution blocks
(if_statement
  (label
    (name) @condition.label)
  (condition) @condition.test)

; Pattern: Library includes
(include_statement
  (member_name) @include.member)

; Pattern: JCLLIB order dependencies
(jcllib_statement
  (library_list) @jcllib.libraries)

; Pattern: Job accounting information
(job_statement
  (label
    (name) @job.name)
  (accounting_info) @job.accounting)

; Pattern: DD statements with inline data
(dd_statement
  (label
    (name) @inline_data.dd_name)
  "*"
  (inline_data) @inline_data.content)