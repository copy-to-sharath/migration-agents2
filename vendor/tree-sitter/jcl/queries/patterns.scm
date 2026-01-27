; Common JCL patterns for code analysis

; Pattern: Find all jobs and their steps
(job_statement
  (label
    (name) @job.name)
  .
  (exec_statement
    (label
      (name) @job.step.name)
    (program_name) @job.step.program)* @job.steps)

; Pattern: Dataset creation and usage
(dd_statement
  (label
    (name) @dataset.dd_name)
  (parameter
    (keyword) @_disp_keyword
    (#eq? @_disp_keyword "DISP")
    (parameter_value) @dataset.disposition))

; Pattern: Procedure calls with parameters
(exec_statement
  (label
    (name) @procedure_call.step)
  (proc_name) @procedure_call.name
  (parameter)* @procedure_call.parameters)

; Pattern: Temporary datasets
(dataset_name) @temp.dataset
(#match? @temp.dataset "^&&.*")

; Pattern: System datasets
(dataset_name) @system.dataset
(#match? @system.dataset "^SYS.*")

; Pattern: User datasets
(dataset_name) @user.dataset
(#match? @user.dataset "^[A-Z][A-Z0-9]*\\.[A-Z].*")

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