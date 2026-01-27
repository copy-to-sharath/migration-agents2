/**
 * Tree-sitter grammar for CICS (Customer Information Control System)
 * CICS is IBM's transaction processing system for mainframes
 * Handles EXEC CICS commands embedded in COBOL/Assembler
 */

module.exports = grammar({
  name: 'cics',

  extras: $ => [
    /\s/,
  ],

  rules: {
    source_file: $ => repeat(choice(
      $.exec_cics_block,
      $.comment,
      $.other_line,
    )),

    // EXEC CICS ... END-EXEC block
    exec_cics_block: $ => seq(
      /EXEC\s+CICS/i,
      $.command_name,
      repeat($.option),
      /END-EXEC/i,
    ),

    // CICS Command names
    command_name: $ => /[A-Z][A-Z0-9]*/i,

    // CICS Options - keyword or keyword(value)
    option: $ => choice(
      seq($.keyword, '(', $.value, ')'),
      $.keyword,
    ),

    keyword: $ => /[A-Z][A-Z0-9]*/i,

    value: $ => choice(
      $.qualified_name,
      $.string_literal,
      $.number,
    ),

    qualified_name: $ => /[A-Z][A-Z0-9\-]*(\.[A-Z][A-Z0-9\-]*)*/i,

    string_literal: $ => /'[^']*'/,

    number: $ => /\d+/,

    comment: $ => /\*[^\n]*/,

    other_line: $ => /[^\n]+\n/,
  },
});
