module.exports = grammar({
  name: 'jcl',

  // External scanner for inline data content
  externals: $ => [
    $.inline_data_content,
  ],

  // Don't treat newlines as whitespace - they're significant in JCL
  extras: $ => [
    / +/,  // Only horizontal whitespace (spaces)
    /\t+/,  // Tabs
  ],

  // Only keep truly necessary conflicts for complex statement parsing
  conflicts: $ => [
    [$._statement, $.proc_definition],
    [$.continuation_line],
  ],

  rules: {
    source_file: $ => repeat(choice($._statement, $._newline)),

    _newline: $ => /\r?\n/,

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
      $.export_statement,
      $.include_statement,
      $.jcllib_statement,
      $.inline_data_end,
      $.inline_data_content  // External scanner - lines not starting with /
    ),

    // JOB Statement  
    // Format: //name JOB (acct),'programmer',params OR //name JOB acctinfo,'programmer',params
    job_statement: $ => seq(
      $.label,
      'JOB',
      optional(choice(
        // Parenthesized accounting info followed by optional programmer name
        seq($.accounting_info, optional(seq(',', $.quoted_string))),
        // Just a quoted string (no accounting info)
        $.quoted_string
      )),
      repeat(seq(',', $.parameter)),
      repeat($.continuation_line)
    ),

    accounting_info: $ => choice(
      // Parenthesized accounting info
      seq('(', /[^)]+/, ')'),
      // Simple accounting info without parentheses (e.g., ACTINFO1)
      /[A-Z][A-Z0-9]*/
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
      repeat(seq(',', $.parameter)),
      repeat($.continuation_line)
    ),

    // DD Statement
    dd_statement: $ => seq(
      $.label,
      'DD',
      optional(choice(
        'DUMMY',
        // DD * with parameters like SYMBOLS=JCLONLY, DLM=XX
        seq($.inline_data_block, repeat(seq(',', $.parameter))),
        seq(
          $.parameter,
          repeat(seq(',', $.parameter)),
          repeat($.continuation_line)
        )
      ))
    ),

    // Continuation line: comma at end, newline, // with spaces, more parameters
    // Each continuation line starts with comma (from previous line) + newline + //
    // and contains parameters that may themselves end with comma (for next continuation)
    // Comments may appear between continuation lines
    continuation_line: $ => seq(
      ',',
      $._newline,
      repeat(seq($.comment, $._newline)),  // Allow comments between continuations
      '//',
      $.parameter,
      repeat(seq(',', $.parameter))
    ),

    // PROC Statement  
    proc_statement: $ => seq(
      $.label,
      'PROC',
      optional(seq(
        $.parameter,
        repeat(seq(',', $.parameter)),
        repeat($.continuation_line)  // Support continuation lines in PROC
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
      $.condition,
      optional('THEN')
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

    // EXPORT Statement (for JCL symbol export)
    export_statement: $ => seq(
      $.label,
      'EXPORT',
      'SYMLIST=',
      choice('*', /[A-Z][A-Z0-9]*/)  // * for all or specific symbol name
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
      choice(
        $.library_list,
        $.quoted_string,         // Single quoted library
        seq('(', $.quoted_string, ')'),  // Quoted in parens
        seq('(', $.quoted_string, repeat(seq(',', $.quoted_string)), ')')  // Multiple quoted
      )
    ),

    // Comment
    comment: $ => /\/\/\*.*/,

    // Label (job name, step name, DD name, etc.) - can be empty for DD concatenation
    // Supports step.ddname pattern like //PRC001.FILEIN DD
    label: $ => seq(
      '//',
      optional(choice(
        seq($.name, '.', $.name),  // step.ddname override
        $.name
      ))
    ),

    // Basic identifiers
    name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    program_name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    proc_name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    member_name: $ => /[A-Z][A-Z0-9#@$]{0,7}/,
    
    dataset_name: $ => choice(
      // Dataset with member - highest precedence
      prec(3, seq(
        /[A-Z][A-Z0-9]*(\.[A-Z0-9]+)*/,
        '(',
        $.member_name,
        ')'
      )),
      // GDG dataset
      prec(2, $.gdg_dataset),
      // Qualified dataset name (with dots) - note: qualifiers can start with letter or digit after dot
      prec(1, /[A-Z][A-Z0-9]*\.[A-Z0-9]+(\.[A-Z0-9]+)*/),
      // Temporary dataset
      prec(1, /&&[A-Z][A-Z0-9]*/),
      // Referback
      prec(1, /\*\.[A-Z][A-Z0-9]*(\.[A-Z][A-Z0-9]*)*/),
      // Simple dataset name - lowest precedence
      prec(0, /[A-Z][A-Z0-9]*/)
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

    parameter: $ => choice(
      // Empty value (MEMNAME=,) - highest precedence to catch trailing comma pattern
      prec(6, seq($.keyword, '=')),
      // Keyword=value parameters - higher precedence
      prec(5, seq($.keyword, '=', $.quoted_string)),
      prec(4, seq($.keyword, '=', $.subparameter_list)),
      prec(3, seq($.keyword, '=', $.symbolic_parameter)),
      // Keyword with dotted value (must have dots - for dataset names)
      prec(2, seq($.keyword, '=', $.dotted_value)),
      // DCB=BLKSIZE=400 pattern (keyword=keyword=value without parens)
      prec(2, seq($.keyword, '=', /[A-Z]+=[A-Z0-9]+/)),
      // DCB=BLKSIZE=&SYM pattern (keyword=keyword=symbolic)
      prec(2, seq($.keyword, '=', /[A-Z]+=&[A-Z][A-Z0-9]*/)),
      prec(1, seq($.keyword, '=', $.parameter_value)),
      // Special case for SYSOUT=*, RESTART=*, DEST=* etc.
      prec(3, seq($.keyword, '=', '*')),
      // Positional parameters - lower precedence
      prec(0, $.symbolic_parameter),
      prec(-1, $.parameter_value)
    ),

    // Referback pattern for DCB, etc.
    referback: $ => /\*\.[A-Z][A-Z0-9]*/,

    // keyword for parameter names - don't use token() so it's contextual
    keyword: $ => /[A-Z]+/,

    // parameter_value - no token() so parser context can disambiguate
    parameter_value: $ => prec(-1, /[A-Z0-9#@$][A-Z0-9#@$*]*|\*[A-Z0-9#@$]+/),

    // Dotted value for dataset names - handles:
    // - Simple dotted: AWS.M2.CARDDEMO
    // - Symbolic prefix: &HLQ..CARDDEMO (double dot after symbol)
    // - Mixed: &CICSHLQ..CICS.SDFHLOAD
    // - Embedded symbolic: OEM.DB2.&SSID..SDSNEXIT (symbol in middle)
    // - With member: &HLQ..COBOL.SRC(MEMBERNAME)
    // - Symbolic with symbolic member: &SRCLIB(&MEMNAME)
    // - Symbolic with literal member: &DFHSAMP(DFHEILID)
    // - Temporary datasets: &&SYSCIN
    // - Temporary with dots: &&LOADSET
    // - GDG notation: DATASET.NAME(+1), (0), (-1)
    dotted_value: $ => choice(
      // Temp dataset with double ampersand
      prec(7, /&&[A-Z][A-Z0-9]*/),
      // Embedded symbolic in middle: OEM.DB2.&SSID..SDSNEXIT
      prec(6, /[A-Z][A-Z0-9]*(\.[A-Z0-9]+)*\.&[A-Z][A-Z0-9]*\.\.[A-Z0-9]+(\.[A-Z0-9]+)*/),
      // Symbolic with symbolic member: &SRCLIB(&MEMNAME)
      prec(5, /&[A-Z][A-Z0-9]*\(&[A-Z][A-Z0-9]*\)/),
      // Symbolic with literal member: &DFHSAMP(DFHEILID)
      prec(5, /&[A-Z][A-Z0-9]*\([A-Z][A-Z0-9#@$]*\)/),
      // Symbolic with member notation: &HLQ..CICSLOAD(MEMBER)
      prec(4, /&[A-Z][A-Z0-9]*\.\.[A-Z0-9]+(\.[A-Z0-9]+)*\([A-Z][A-Z0-9#@$]*\)/),
      // Symbolic with symbolic member after dots: &HLQ..SRC(&MEMNAME)
      prec(4, /&[A-Z][A-Z0-9]*\.\.[A-Z0-9]+(\.[A-Z0-9]+)*\(&[A-Z][A-Z0-9]*\)/),
      // Symbolic with GDG generation: &HLQ..DATASET(+1) or (0)
      prec(4, /&[A-Z][A-Z0-9]*\.\.[A-Z0-9]+(\.[A-Z0-9]+)*\([+-]?\d+\)/),
      // With symbolic prefix and double dot
      prec(3, /&[A-Z][A-Z0-9]*\.\.[A-Z0-9]+(\.[A-Z0-9]+)*/),
      // Dotted with GDG generation number: DATASET.NAME(+1)
      prec(2, /[A-Z][A-Z0-9]*\.[A-Z0-9]+(\.[A-Z0-9]+)*\([+-]?\d+\)/),
      // Simple dotted value with member: DATASET.NAME(MEMBER)
      prec(2, /[A-Z][A-Z0-9]*\.[A-Z0-9]+(\.[A-Z0-9]+)*\([A-Z][A-Z0-9#@$]*\)/),
      // Simple dotted value
      prec(1, /[A-Z][A-Z0-9]*\.[A-Z0-9]+(\.[A-Z0-9]+)*/)
    ),

    simple_value: $ => token(/[A-Z0-9#@$*]+/),

    // quoted_string uses token() for atomic matching
    quoted_string: $ => token(/\'[^\']*\'/),

    symbolic_parameter: $ => /&[A-Z][A-Z0-9]*/,

    subparameter_list: $ => seq(
      '(',
      optional(seq(
        optional($.subparameter),  // First subparameter is optional for patterns like (,PASS)
        repeat(seq(',', optional($.subparameter)))
      )),
      ')'
    ),

    subparameter: $ => choice(
      // Numbers - highest precedence for pure numeric
      prec(3, /\d+/),
      // Quoted strings
      prec(3, /\'[^\']*\'/),
      // Referback pattern: *.DDNAME
      prec(3, /\*\.[A-Z][A-Z0-9]*/),
      // Standalone asterisk (for SYSOUT=(*,INTRDR))
      prec(3, '*'),
      // Symbolic parameters like &SYSLBLK
      prec(3, /&[A-Z][A-Z0-9]*/),
      // Keyword=value pairs (like RECFM=FB, LRECL=80, BLKSIZE=3200) - use single regex
      prec(2, /[A-Z]+=[A-Z0-9]+/),
      // Keyword=symbolic pairs (like BLKSIZE=&SYSLBLK)
      prec(2, /[A-Z]+=&[A-Z][A-Z0-9]*/),
      // Simple identifiers (like NEW, CATLG, DELETE, CYL, RLSE, INTRDR)
      prec(1, /[A-Z][A-Z0-9]*/),
      // Nested parameter lists like (10,5)
      prec(0, $.subparameter_list)
    ),

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
      /&[A-Z][A-Z0-9]*\.\.[A-Z0-9]+(\.[A-Z0-9]+)*/,  // Symbolic with double dot: &HLQ..CBL
      /[A-Z][A-Z0-9]*(\.[A-Z0-9]+)+/,  // Dotted value like AWS.M2
      /[A-Z0-9#@$*]+/,    // Direct simple value pattern  
      /&[A-Z][A-Z0-9]*/   // Direct symbol reference pattern
    ),

    // Library list for JCLLIB - can have symbolic references with ..
    library_list: $ => choice(
      $.library_name,
      seq('(', $.library_name, repeat(seq(',', $.library_name)), ')')
    ),

    // Library name can include symbolic references like &HLQ..CARDDEMO.PRC
    library_name: $ => /(&[A-Z][A-Z0-9]*\.?)+[A-Z0-9]*(\.[A-Z0-9]+)*/,

    // Inline data block: DD * followed by data until /*
    // Note: Inline data content is simplified - actual parsing may need external scanner
    inline_data_block: $ => '*',

    // Inline data line - matches lines that don't start with // or /*
    // This captures free-form inline data content after DD * statements
    // Pattern: starts with space/letter/digit but NOT with /
    inline_data_line: $ => prec(-10, /[^\/\r\n][^\r\n]*/),

    // Inline data delimiter - line starting with /* 
    inline_data_end: $ => /\/\*[^\r\n]*/,
  }
});