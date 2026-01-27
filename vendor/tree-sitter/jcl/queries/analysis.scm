; Analysis queries for JCL code analysis and Neo4j mapping

; Job dependencies - capture job names and their relationships
(job_statement
  (label
    (name) @job.name))

; Step definitions within jobs
(exec_statement
  (label
    (name) @step.name)
  (program_name) @step.program)

(exec_statement
  (label
    (name) @step.name)
  (proc_name) @step.procedure)

; Dataset usage tracking
(dd_statement
  (label
    (name) @dd.name)
  (parameter
    (keyword) @dd.keyword
    (parameter_value) @dd.value))

; Procedure definitions
(proc_statement
  (label
    (name) @procedure.definition))

; Dataset references in parameters
(parameter
  (keyword) @parameter.keyword
  (#eq? @parameter.keyword "DSN")
  (parameter_value) @dataset.reference)

; DISP parameter tracking for dataset lifecycle
(parameter
  (keyword) @parameter.keyword
  (#eq? @parameter.keyword "DISP")
  (parameter_value) @dataset.disposition)

; Include statements for modular analysis
(include_statement
  (member_name) @include.member)

; JCLLIB statements for library dependencies
(jcllib_statement
  (library_list
    (dataset_name) @library.dataset))

; Conditional execution
(if_statement
  (condition) @condition.expression)

; Symbol assignments
(set_statement
  (symbol_assignment
    (symbol_name) @symbol.name
    (symbol_value) @symbol.value))

; Program invocations for call graph analysis
(exec_statement
  (program_name) @program.invocation)