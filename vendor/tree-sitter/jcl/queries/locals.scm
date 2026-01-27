; Local scope queries for JCL

; Job definitions create a scope
(job_statement
  (label
    (name) @local.definition.job))

; Step definitions (EXEC statements) create local scopes
(exec_statement
  (label
    (name) @local.definition.step))

; DD names create references within steps
(dd_statement
  (label
    (name) @local.definition.dd))

; Procedure definitions create their own scope
(proc_statement
  (label
    (name) @local.definition.procedure))

; Dataset names are references
(dataset_name) @local.reference.dataset

; Program names are references
(program_name) @local.reference.program

; Procedure calls are references
(proc_name) @local.reference.procedure