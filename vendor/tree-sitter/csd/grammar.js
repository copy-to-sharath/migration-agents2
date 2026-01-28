// CICS System Definition (CSD) Grammar
// Handles DEFINE commands for FILE, MAPSET, PROGRAM, TRANSACTION, etc.

module.exports = grammar({
  name: 'csd',

  extras: $ => [
    /[ \t]+/,
    /\r?\n/,
  ],

  rules: {
    source_file: $ => repeat(choice(
      $.definition,
      $.comment
    )),

    comment: $ => /\/\*[^\n]*\*?\/?/,

    // CSD definitions
    definition: $ => choice(
      $.define_file,
      $.define_mapset,
      $.define_program,
      $.define_transaction,
      $.define_tdqueue,
      $.define_tsqueue,
      $.define_connection,
      $.define_sessions,
      $.generic_define
    ),

    // DEFINE FILE
    define_file: $ => seq(
      'DEFINE',
      'FILE',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE MAPSET
    define_mapset: $ => seq(
      'DEFINE',
      'MAPSET',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE PROGRAM
    define_program: $ => seq(
      'DEFINE',
      'PROGRAM',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE TRANSACTION
    define_transaction: $ => seq(
      'DEFINE',
      'TRANSACTION',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE TDQUEUE (Transient Data Queue)
    define_tdqueue: $ => seq(
      'DEFINE',
      'TDQUEUE',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE TSQUEUE (Temporary Storage Queue)
    define_tsqueue: $ => seq(
      'DEFINE',
      choice('TSQUEUE', 'TSMODEL'),
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE CONNECTION
    define_connection: $ => seq(
      'DEFINE',
      'CONNECTION',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // DEFINE SESSIONS
    define_sessions: $ => seq(
      'DEFINE',
      'SESSIONS',
      '(',
      $.resource_name,
      ')',
      repeat($.attribute)
    ),

    // Generic DEFINE for other resource types
    generic_define: $ => seq(
      'DEFINE',
      $.resource_type,
      optional(seq('(', $.resource_name, ')')),
      repeat($.attribute)
    ),

    // Attributes: KEYWORD(value) or KEYWORD
    attribute: $ => choice(
      // DESCRIPTION is special - can have spaces in value
      seq('DESCRIPTION', '(', $.description_text, ')'),
      // GROUP(name)
      seq('GROUP', '(', $.group_name, ')'),
      // Regular attributes
      seq($.attribute_name, '(', $.attribute_value, ')'),
      // Flag attributes without value
      $.attribute_name
    ),

    attribute_name: $ => /[A-Z][A-Z0-9]*/,

    attribute_value: $ => choice(
      $.datetime,
      $.number_list,
      $.dataset_name,
      $.number,
      $.identifier,
      $.yes_no
    ),

    // Comma-separated numbers like 0,0,0 for WAITTIME
    number_list: $ => seq(
      $.number,
      repeat1(seq(',', $.number))
    ),

    description_text: $ => /[A-Z0-9 _\-]+/,

    group_name: $ => /[A-Z][A-Z0-9]*/,

    resource_type: $ => /[A-Z][A-Z0-9]*/,

    resource_name: $ => /[A-Z][A-Z0-9]*/,

    dataset_name: $ => /[A-Z][A-Z0-9]*(\.[A-Z0-9]+)*/,

    datetime: $ => /\d{2}\/\d{2}\/\d{2}[ ]\d{2}:\d{2}:\d{2}/,

    number: $ => /\d+/,

    identifier: $ => /[A-Z][A-Z0-9]*/,

    yes_no: $ => choice('YES', 'NO'),
  }
});
