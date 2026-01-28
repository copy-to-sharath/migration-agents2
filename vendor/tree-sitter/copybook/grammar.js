/**
 * Tree-sitter grammar for COBOL Copybooks
 * 
 * Copybooks are COBOL code fragments that are included via COPY statements.
 * They typically contain:
 * - Data definitions (01, 05, 10 levels with PIC clauses)
 * - Working storage items
 * - Record layouts
 * - Comments
 * 
 * First line recognition patterns:
 * - Comment lines: spaces + '*'
 * - Level numbers: 01, 05, 10, 15, 20, etc.
 * - Sequence numbers in columns 1-6 (optional)
 */

module.exports = grammar({
  name: 'copybook',

  extras: $ => [/[ \t\r]+/],

  rules: {
    source_file: $ => repeat(choice(
      $.statement,
      $.comment_line,
      $.newline
    )),

    // Newlines
    newline: $ => /\n/,

    // Comment line - asterisk in column 7 (captures to end of line)
    // High precedence to match before picture_string
    comment_line: $ => prec(10, seq(
      optional($.sequence_number),
      /\*[^\n]*/
    )),

    // Sequence number in columns 1-6
    sequence_number: $ => /[0-9]{6}/,

    // Any COBOL statement ending with period
    statement: $ => seq(
      optional($.sequence_number),
      optional($.statement_body),
      '.'
    ),

    // Statement body - captures content before the period
    // Allows newlines within statements for multi-line COBOL
    statement_body: $ => repeat1(choice(
      $.level_88_condition,
      $.level_number,
      $.keyword,
      $.identifier,
      $.picture_string,
      $.string_literal,
      $.number,
      $.operator,
      $.parenthesized,
      $.embedded_comment,
      $.continuation_newline
    )),

    // Comment embedded within a statement (newline + asterisk)
    embedded_comment: $ => prec(5, seq(/\n/, /\*[^\n]*/)),

    // Newline within a statement (continuation) - only if not followed by asterisk
    continuation_newline: $ => prec(-1, /\n/),

    // Level 88 condition - special handling
    level_88_condition: $ => prec.left(2, seq(
      '88',
      $.identifier,
      'VALUE',
      optional(choice('IS', 'ARE'))
    )),

    // Level numbers
    level_number: $ => prec(1, choice(
      /0[1-9]/,
      /[1-4][0-9]/,
      '66', '77'
    )),

    // COBOL keywords - Data Division and Procedure Division
    keyword: $ => choice(
      // Data Division
      'FILLER',
      'PIC', 'PICTURE',
      'VALUE', 'VALUES',
      'OCCURS', 'TIMES', 'TO',
      'REDEFINES',
      'INDEXED', 'BY',
      'DEPENDING', 'ON',
      'USAGE', 'IS',
      'DISPLAY', 'DISPLAY-1',
      'BINARY', 'COMP', 'COMP-1', 'COMP-2', 'COMP-3', 'COMP-4', 'COMP-5',
      'COMPUTATIONAL', 'COMPUTATIONAL-1', 'COMPUTATIONAL-2', 'COMPUTATIONAL-3', 'COMPUTATIONAL-4', 'COMPUTATIONAL-5',
      'PACKED-DECIMAL',
      'INDEX', 'POINTER',
      'ZERO', 'ZEROS', 'ZEROES',
      'SPACE', 'SPACES',
      'HIGH-VALUE', 'HIGH-VALUES',
      'LOW-VALUE', 'LOW-VALUES',
      'QUOTE', 'QUOTES',
      'NULL', 'NULLS',
      'ALL',
      'THRU', 'THROUGH',
      'ASCENDING', 'DESCENDING', 'KEY',
      'SIGN', 'LEADING', 'TRAILING', 'SEPARATE', 'CHARACTER',
      'SYNC', 'SYNCHRONIZED', 'LEFT', 'RIGHT',
      'JUST', 'JUSTIFIED',
      'BLANK', 'WHEN',
      'EXTERNAL', 'GLOBAL', 'AS',
      'COPY', 'REPLACING', 'OF', 'IN',
      'REPLACE', 'OFF',
      'EJECT', 'SKIP1', 'SKIP2', 'SKIP3',
      'EXEC', 'EXECUTE', 'SQL', 'SQLIMS', 'DLI', 'END-EXEC',
      // Procedure Division - Control flow
      'IF', 'ELSE', 'END-IF', 'THEN',
      'EVALUATE', 'END-EVALUATE', 'OTHER', 'ALSO',
      'PERFORM', 'END-PERFORM', 'UNTIL', 'VARYING', 'TIMES', 'WITH', 'TEST', 'BEFORE', 'AFTER',
      'GO', 'SECTION', 'PARAGRAPH',
      'CONTINUE', 'NEXT', 'SENTENCE',
      'EXIT', 'STOP', 'RUN',
      // Procedure Division - Data manipulation
      'MOVE', 'CORRESPONDING', 'CORR', 'INTO',
      'SET', 'TRUE', 'FALSE',
      'INITIALIZE', 'REPLACING', 'ALPHABETIC', 'ALPHANUMERIC', 'ALPHANUMERIC-EDITED', 'NUMERIC', 'NUMERIC-EDITED',
      'COMPUTE', 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'GIVING', 'REMAINDER',
      'STRING', 'DELIMITED', 'SIZE', 'OVERFLOW', 'NOT', 'END-STRING',
      'UNSTRING', 'COUNT', 'DELIMITER', 'TALLYING', 'END-UNSTRING',
      'INSPECT', 'CONVERTING', 'FIRST', 'INITIAL',
      // Procedure Division - I/O
      'READ', 'WRITE', 'REWRITE', 'DELETE', 'START',
      'OPEN', 'CLOSE', 'INPUT', 'OUTPUT', 'I-O', 'EXTEND',
      'ACCEPT', 'FROM', 'DATE', 'DAY', 'TIME', 'DAY-OF-WEEK',
      // Procedure Division - Comparisons
      'EQUAL', 'GREATER', 'LESS', 'THAN', 'OR', 'AND',
      // Procedure Division - CICS
      'DFHENTER', 'DFHCLEAR', 'DFHPA1', 'DFHPA2', 'DFHPF1', 'DFHPF2', 'DFHPF3', 'DFHPF4', 'DFHPF5',
      'DFHPF6', 'DFHPF7', 'DFHPF8', 'DFHPF9', 'DFHPF10', 'DFHPF11', 'DFHPF12',
      'EIBAID', 'DFHRED', 'DFHBMASB', 'DFHBMASK'
    ),

    // Identifier - data names, paragraph names, including template vars like (TESTVAR1)
    // Also handles compound identifiers like FLG-(TESTVAR1)-NOT-OK
    // And parenthesized identifiers like (SCRNVAR2)C
    identifier: $ => choice(
      /[A-Za-z][A-Za-z0-9\-]*(\([A-Za-z0-9\-]+\)[A-Za-z0-9\-]*)*/,
      /\([A-Za-z0-9\-]+\)[A-Za-z0-9\-]*/
    ),

    // Picture string
    picture_string: $ => /[AXS9VZ0]+\([0-9]+\)[AXS9VZ0\(\)]*|[AXS9VZ0\+\-\*\/\,\$BPE]+/i,

    // String literals
    string_literal: $ => choice(
      /'[^']*'/,
      /"[^"]*"/
    ),

    // Numbers
    number: $ => /[\+\-]?[0-9]+\.?[0-9]*/,

    // Operators and punctuation
    operator: $ => choice(
      '==', '=',
      '>', '<', '>=', '<=',
      ',',
      '(', ')',
      ':'
    ),

    // Parenthesized content - lower precedence than standalone parens
    parenthesized: $ => prec(1, seq(
      '(',
      repeat(choice(
        $.identifier,
        $.number,
        $.string_literal,
        ','
      )),
      ')'
    ))
  }
});
