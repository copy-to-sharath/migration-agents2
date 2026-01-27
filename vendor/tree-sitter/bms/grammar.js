/**
 * Tree-sitter grammar for BMS (Basic Mapping Support)
 * BMS is IBM's screen definition language for CICS
 * BMS macros define screen layouts for 3270 terminals
 */

module.exports = grammar({
  name: 'bms',

  extras: $ => [
    /[ \t]/,  // Whitespace but NOT newlines
  ],

  rules: {
    source_file: $ => repeat(choice(
      $.bms_statement,
      $.end_statement,
      $.comment,
      $.blank_line,
    )),

    bms_statement: $ => seq(
      optional($.label),
      $.macro_name,
      optional($.parameters),
      $._eol,
    ),

    end_statement: $ => seq(
      optional($.label),
      /END/i,
      $._eol,
    ),

    label: $ => /[A-Z@#$][A-Z0-9@#$]*/i,

    macro_name: $ => choice(
      /DFHMSD/i,
      /DFHMDI/i,
      /DFHMDF/i,
    ),

    parameters: $ => repeat1($.parameter),

    parameter: $ => seq(
      $.param_name,
      '=',
      choice(
        $.param_list,
        $.param_value,
      ),
      optional(','),
    ),

    param_name: $ => /[A-Z][A-Z0-9]*/i,

    param_list: $ => seq(
      '(',
      $.param_value,
      repeat(seq(',', $.param_value)),
      ')',
    ),

    param_value: $ => choice(
      $.string_literal,
      $.hex_literal,
      $.number,
      $.identifier,
    ),

    identifier: $ => /[A-Z@#$][A-Z0-9@#$-]*/i,

    string_literal: $ => /'[^']*'/,

    hex_literal: $ => /X'[0-9A-Fa-f]+'/i,

    number: $ => /-?\d+/,

    comment: $ => seq('*', /[^\n]*/, $._eol),

    blank_line: $ => $._eol,

    _eol: $ => /\r?\n/,
  },
});
