// IDCAMS (Access Method Services) Grammar
// Handles REPRO, DEFINE, DELETE, PRINT, LISTCAT and other AMS commands

module.exports = grammar({
  name: 'idcams',

  extras: $ => [
    /[ \t]+/,
    /\r?\n/,
  ],

  conflicts: $ => [
    [$.statement],
  ],

  rules: {
    source_file: $ => repeat(choice(
      $.statement,
      $.comment
    )),

    comment: $ => /\/\*[^\n]*\*?\/?/,

    // IDCAMS statement - command with parameters
    statement: $ => seq(
      $.command,
      repeat($.parameter)
    ),

    // IDCAMS commands
    command: $ => choice(
      'REPRO',
      'DEFINE',
      'DELETE',
      'PRINT',
      'LISTCAT',
      'SET',
      'VERIFY',
      'ALTER',
      'BLDINDEX',
      'EXPORT',
      'IMPORT',
      $.identifier  // For other commands
    ),

    // Parameters
    parameter: $ => choice(
      $.keyword_param,
      $.continuation
    ),

    // Keyword parameter: KEYWORD(value) or KEYWORD(val1 val2) or just KEYWORD
    keyword_param: $ => seq(
      $.keyword,
      optional(seq(
        '(',
        optional($.param_content),
        ')'
      ))
    ),

    // Content inside parentheses - can be nested
    param_content: $ => repeat1(choice(
      $.nested_paren,
      $.dataset_name,
      $.number,
      $.keyword,
      ','
    )),

    nested_paren: $ => seq(
      '(',
      optional($.param_content),
      ')'
    ),

    // Continuation marker (dash)
    continuation: $ => '-',

    // Keywords/identifiers
    keyword: $ => /[A-Z][A-Z0-9]*/,

    identifier: $ => /[A-Z][A-Z0-9]*/,

    dataset_name: $ => /[A-Z][A-Z0-9]*\.[A-Z0-9]+(\.[A-Z0-9]+)*/,

    number: $ => /\d+/,
  }
});
