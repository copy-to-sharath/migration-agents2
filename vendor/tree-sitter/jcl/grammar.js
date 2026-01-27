module.exports = grammar({
  name: 'jcl',

  extras: $ => [
    /\s/,
  ],

  conflicts: $ => [
    [$.job_statement],
    [$.dd_statement],
    [$.parameter_value, $.quoted_string],
    [$.parameter_value, $.dataset_name],
    [$._statement, $.proc_definition],
    [$.inline_data],
    [$.subparameter, $.keyword]
  ],

  rules: {
    source_file: $ => repeat($._statement),

    _statement: $ => choice(
      $.job_statement,
      $.exec_statement,
      $.dd_statement,
      $.comment,
      $.proc_definition,
      $.proc_statement,
      $.pend_statement,
      $.if_statement,
      $.else_statement,
      $.endif_statement,
      $.set_statement,
      $.include_statement,
      $.jcllib_statement
    ),

    // JOB Statement  
    job_statement: $ => seq(
      $.label,
      'JOB',
      optional($.quoted_string),
      repeat(seq(',', $.parameter)),
      optional(seq(',', repeat($.continuation_line)))
    ),

    // EXEC Statement
    exec_statement: $ => seq(
      $.label,
      'EXEC',
      choice(
        seq('PGM=', $.program_name),
        seq('PROC=', $.proc_name),
        $.proc_name
      ),
      repeat(seq(',', $.parameter))
    ),

    // DD Statement
    dd_statement: $ => seq(
      $.label,
      'DD',
      optional(choice(
        'DUMMY',
        $.inline_data,  // Combined inline data
        seq(
          $.parameter,
          repeat(seq(',', $.parameter)),
          optional(seq(',', repeat($.continuation_line)))
        )
      ))
    ),

    // PROC Statement  
    proc_statement: $ => seq(
      $.label,
      'PROC',
      optional(seq(
        $.parameter,
        repeat(seq(',', $.parameter))
      ))
    ),

    // PEND Statement
    pend_statement: $ => seq(
      $.label,
      'PEND'
    ),

    // PROC Definition (PROC...PEND block)
    proc_definition: $ => seq(
      $.proc_statement,
      repeat(choice(
        $.exec_statement,
        $.dd_statement,
        $.set_statement,
        $.include_statement,
        $.if_statement,
        $.else_statement,
        $.endif_statement,
        $.comment
      )),
      $.pend_statement
    ),

    // IF Statement
    if_statement: $ => seq(
      $.label,
      'IF',
      $.condition
    ),

    // ELSE Statement
    else_statement: $ => seq(
      $.label,
      'ELSE'
    ),

    // ENDIF Statement
    endif_statement: $ => seq(
      $.label,
      'ENDIF'
    ),

    // SET Statement
    set_statement: $ => seq(
      $.label,
      'SET',
      $.symbol_assignment
    ),

    // INCLUDE Statement
    include_statement: $ => seq(
      $.label,
      'INCLUDE',
      'MEMBER=',
      $.member_name
    ),

    // JCLLIB Statement
    jcllib_statement: $ => seq(
      $.label,
      'JCLLIB',
      'ORDER=',
      $.library_list
    ),

    // Comment
    comment: $ => /\/\/\*.*/,

    // Label (job name, step name, DD name, etc.)
    label: $ => seq(
      '//',
      optional($.name)
    ),

    // Basic identifiers
    name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    program_name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    proc_name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    member_name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    dataset_name: $ => choice(
      // Simple dataset name
      /[A-Z][A-Z0-9]*(\.[A-Z][A-Z0-9]*)*/,
      // Dataset with member
      seq(
        /[A-Z][A-Z0-9]*(\.[A-Z][A-Z0-9]*)*/,
        '(',
        $.member_name,
        ')'
      ),
      // GDG dataset
      $.gdg_dataset,
      // Temporary dataset
      /&&[A-Z][A-Z0-9]*/,
      // Referback
      /\*\.[A-Z][A-Z0-9]*(\.[A-Z][A-Z0-9]*)*/
    ),

    // GDG Dataset Support - Generation Data Group notation
    gdg_dataset: $ => seq(
      /[A-Z][A-Z0-9]*(\.[A-Z][A-Z0-9]*)*/,
      '(',
      choice(
        /[+-]?\d+/,  // (+1), (0), (-1), etc.
        'GDG'        // Special GDG keyword
      ),
      ')'
    ),

    // Parameters
    parameter_list: $ => repeat1(choice(
      $.parameter,
      seq(',', $.parameter)
    )),

    accounting_info: $ => seq(
      '(',
      /[^)]+/,
      ')',
      optional(seq(',', $.quoted_string))
    ),

    parameter: $ => choice(
      // Keyword=value parameter - prioritize quoted_string first
      seq($.keyword, '=', $.quoted_string),
      seq($.keyword, '=', $.parameter_value),
      seq($.keyword, '=', $.symbolic_parameter),
      seq($.keyword, '=', $.subparameter_list),
      // Special case for DSN dataset references
      seq(alias('DSN', 'keyword'), '=', $.dataset_name),
      // Special case for SYSOUT=*
      seq(alias('SYSOUT', 'keyword'), '=', $.sysout_value),
      // Positional parameter
      $.parameter_value,
      $.symbolic_parameter
    ),

    sysout_value: $ => '*',

    keyword: $ => /[A-Z]+/,

    parameter_value: $ => /[A-Z0-9#@$*]+/,

    simple_value: $ => /[A-Z0-9#@$*]+/,

    quoted_string: $ => /\'[^\']*\'/,

    symbolic_parameter: $ => /&[A-Z][A-Z0-9]*/,

    subparameter_list: $ => seq(
      '(',
      optional(seq(
        $.subparameter,
        repeat(seq(',', $.subparameter))
      )),
      ')'
    ),

    _subparameter_item: $ => choice(
      /\d+/,  // Direct number pattern
      $.simple_value,
      $.quoted_string,
      seq($.keyword, '=', choice($.simple_value, /\d+/)),
      $.subparameter_list  // Nested lists like SPACE=(CYL,(1,1),RLSE)
    ),

    subparameter: $ => choice(
      // Numbers
      /\d+/,
      // Keyword=value pairs (like RECFM=FB, LRECL=80) - must come before simple identifiers
      seq(/[A-Z]+/, '=', choice(/[A-Z0-9#@$*]+/, /\d+/)),
      // Simple identifiers (like NEW, CATLG, DELETE, CYL, RLSE)
      /[A-Z][A-Z0-9#@$*]*/,
      // Quoted strings
      /\'[^\']*\'/,
      // Nested parameter lists like (10,5)
      $.subparameter_list
    ),

    // Inline data marker (simplified)
    inline_data: $ => '*',
    
    inline_delimiter: $ => '/*',

    // Conditions for IF statements
    condition: $ => choice(
      // RC condition
      seq('RC', $.comparison_operator, $.number),
      // ABEND condition
      seq('ABEND', '=', choice('TRUE', 'FALSE')),
      // Complex condition
      seq('(', $.condition, ')', optional(seq($.logical_operator, $.condition)))
    ),

    comparison_operator: $ => choice('=', '!=', '<', '>', '<=', '>=', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),

    logical_operator: $ => choice('AND', 'OR', '&', '|'),

    number: $ => /\d+/,

    // Symbol assignment for SET
    symbol_assignment: $ => seq(
      $.symbol_name,
      '=',
      $.symbol_value
    ),

    symbol_name: $ => choice(
      /&[A-Z][A-Z0-9]*/,  // Symbol reference
      /[A-Z][A-Z0-9]*/    // Symbol definition in SET
    ),

    symbol_value: $ => choice(
      /\'[^\']*\'/,        // Direct quoted string pattern
      /[A-Z0-9#@$*]+/,    // Direct simple value pattern  
      /&[A-Z][A-Z0-9]*/   // Direct symbol reference pattern
    ),

    // Library list for JCLLIB
    library_list: $ => choice(
      $.dataset_name,
      seq('(', $.dataset_name, repeat(seq(',', $.dataset_name)), ')')
    ),

    // Continuation handling
    continuation_line: $ => seq(
      '//',
      /\s+/,
      repeat1(choice(
        $.parameter,
        seq(',', $.parameter)
      ))
    ),
  }
});