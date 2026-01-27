/**
 * Tree-sitter grammar for Easytrieve/Easytrieve Plus
 * Easytrieve is IBM's report generation and data manipulation language
 */

module.exports = grammar({
  name: 'easytrieve',

  extras: $ => [
    /[ \t]+/,
  ],

  rules: {
    source_file: $ => repeat(choice(
      $.line,
      $.comment,
      $.blank_line,
    )),

    line: $ => seq(
      $.keyword,
      repeat($.token),
      $.newline,
    ),

    keyword: $ => /[A-Z][A-Z0-9\-]*/i,

    token: $ => choice(
      $.string_literal,
      $.number,
      $.symbol,
      $.identifier,
    ),

    symbol: $ => /[=<>+\-*\/(),.:]/,

    identifier: $ => /[A-Z@#$][A-Z0-9@#$\-]*/i,

    string_literal: $ => /'[^']*'/,

    number: $ => /\d+(\.\d+)?/,

    comment: $ => seq('*', /[^\n]*/, $.newline),

    blank_line: $ => $.newline,

    newline: $ => /\n/,
  },
});
