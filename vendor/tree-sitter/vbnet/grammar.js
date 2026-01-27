module.exports = grammar({
  name: 'vb',

  extras: $ => [
    $._horizontal_whitespace,
    seq('_', /[\n\r]*/),
    $.comment
  ],

  precedences: $ => [
    [
      "new",
      "call",
      "member",
      "exponential",
      "multiplicative",
      "additive",
      "boolean",
      $.unary_expression,
      $.binary_expression,
      $._expression
    ],
    [
      "assign",
      "branch",
      "invocation",
      $._expression
    ],
    [
      $.array_element,
      $.argument,
      $.identifier
    ],
    [
      $.array_identifier,
      $.new_identifier
    ],
    [
      $._variable_declaration_assignment,
      $.variable_list
    ]
  ],

  rules: {
    source_file: $ => repeat(
      seq($._statement, $._whitespace),
    ),

    _statement: $ => choice(
      $.subroutine,
      $.function,
      $.ptrsafe_function_declaration,
      $._inline_statement
    ),

    _inline_statement: $ => choice(
      $.variable_assignment,
      $.if_statement,
      $.for_statement,
      $.while_statement,
      $.do_statement,
      $.exit_statement,
      $.error_statement,
      $.const_declaration,
      $.variable_declaration,
      $.event_declaration,
      $.redim,
      $.invocation_statement,
    ),

    variable_assignment: $ => prec.left('assign',seq(
      choice(
        $.array_element,
        $.identifier
      ),
      $._equal,
      $._expression
    )),

    _inline_statement_block: $ => choice(
      repeat1(
        seq($._inline_statement, $._whitespace)
      ),
      $._whitespace
    ),

    invocation_statement: $ => prec.left('invocation',seq(
      $._expression,
      optional($.argument_list)
    )),

    comment: $ => token(choice(
        seq("'", /.*/),
        seq(/[Rr][Ee][Mm]/, /.*/)
    )),

    exit_statement: $ => seq(
      /[Ee][Xx][Ii][Tt]/,
      choice(
        /[Ff][Oo][Rr]/,
        /[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]/,
        /[Ss][Uu][Bb]/,
        /[Dd][Oo]/,
        /[Ww][Hh][Ii][Ll][Ee]/
      )
    ),

    error_statement: $ => seq(
      /[Oo][Nn] [Ee][Rr][Rr][Oo][Rr]/,
      choice(
        seq(
          /[Gg][Oo][Tt][Oo]/,
          choice(
            '0',
            $.new_identifier
          )
        ),
        /[Rr][Ee][Ss][Uu][Mm][Ee] [Nn][Ee][Xx][Tt]/
      )
    ),

    if_statement: $ => prec('branch',seq(
      /[Ii][Ff]/,
      $._expression,
      /[Tt][Hh][Ee][Nn]/,
      $._whitespace,
      $._inline_statement_block,
      optional(choice(
        repeat(seq(
          /[Ee][Ll][Ss][Ee][Ii][Ff]/,
          $._expression,
          /[Tt][Hh][Ee][Nn]/,
          $._whitespace,
          $._inline_statement_block
        )),
        seq(
          /[Ee][Ll][Ss][Ee]/,
          $._whitespace,
          $._inline_statement_block
        ),
      )),
      /[Ee][Nn][Dd] [Ii][Ff]/
    )),

    for_statement: $ => prec('branch',seq(
      /[Ff][Oo][Rr]/,
      $.identifier,
      $._equal,
      $._expression,
      /[Tt][Oo]/,
      $._expression,
      optional(seq(
        /[Ss][Tt][Ee][Pp]/,
        $._expression
      )),
      $._whitespace,
      $._inline_statement_block,
      /[Nn][Ee][Xx][Tt]/,
      $.identifier
    )),

    while_statement: $ => prec('branch',seq(
      /[Ww][Hh][Ii][Ll][Ee]/,
      $._expression,
      $._whitespace,
      $._inline_statement_block,
      /[Ww][Ee][Nn][Dd]/
    )),

    do_statement: $ => prec('branch',seq(
      /[Dd][Oo]/,
      $._whitespace,
      $._inline_statement_block,
      /[Ll][Oo][Oo][Pp]/,
      choice(
        /[Ww][Hh][Ii][Ll][Ee]/,
        /[Uu][Nn][Tt][Ii][Ll]/
      ),
      $._expression
    )),

    subroutine: $ => seq(
      /[Ss][Uu][Bb]/,
      $.new_identifier,
      '(',
      optional($.parameter_list),
      ')',
      $._whitespace,
      $._inline_statement_block,
      /[Ee][Nn][Dd] [Ss][Uu][Bb]/
    ),

    function: $ => seq(
      optional($.visibility),
      /[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]/,
      $.new_identifier,
      '(',
      optional($.parameter_list),
      ')',
      optional($.type_definition),
      $._whitespace,
      $._inline_statement_block,
      /[Ee][Nn][Dd] [Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]/
    ),

    const_declaration: $ => seq(
      /[Cc][Oo][Nn][Ss][Tt]/,
      $._variable_declaration_assignment,
    ),

    variable_declaration: $ => seq(
      /[Dd][Ii][Mm]/,
      choice(
        $._variable_declaration_assignment,
        $.variable_list
      )
    ),

    event_declaration: $ => seq(
      optional($.visibility),
      /[Ee][Vv][Ee][Nn][Tt]/,
      $.new_identifier,
      '(',
      optional($.parameter_list),
      ')'
    ),

    redim: $ => seq(
      /[Rr][Ee][Dd][Ii][Mm]/,
      optional(/[Pp][Rr][Ee][Ss][Ee][Rr][Vv][Ee]/),
      $._expression
    ),

    _variable_declaration_assignment: $ => seq(
      $.variable_declaration_identifier,
      optional($.type_definition),
      $._equal,
      $._expression
    ),

    variable_declaration_identifier: $ => choice(
      $.array_identifier,
      $.new_identifier
    ),

    array_identifier: $ => seq(
      $.new_identifier,
      '(',
      optional(seq(
        $.number,
        /[Tt][Oo]/,
        $.number
      )),
      ')'
    ),

    type_definition: $=> seq(
      /[Aa][Ss]/,
      $.type
    ),

    variable_list: $ => seq(
      $.variable_declaration_identifier,
      repeat(seq(
        ',',
        $.variable_declaration_identifier
      )),
      optional($.type_definition)
    ),

    ptrsafe_function_declaration: $ => seq(
      /[Pp][Rr][Ii][Vv][Aa][Tt][Ee]/,
      /[Dd][Ee][Cc][Ll][Aa][Rr][Ee]/,
      /[Pp][Tt][Rr][Ss][Aa][Ff][Ee]/,
      /[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn]/,
      $.new_identifier,
      /[Ll][Ii][Bb]/,
      $.string_literal,
      optional(seq(/[Aa][Ll][Ii][Aa][Ss]/, $.string_literal)),
      '(',
      optional($.parameter_list),
      ')',
      $.type_definition
    ),

    parameter_list: $ => seq(
      $.parameter,
      repeat(seq(
        ',',
        $.parameter
      ))
    ),

    parameter: $ => seq(
      optional($.modifier),
      $.new_identifier,
      optional($.type_definition)
    ),

    modifier: $ => choice(
      /[Bb][Yy][Vv][Aa][Ll]/,
      /[Bb][Yy][Rr][Ee][Ff]/,
      /[Oo][Pp][Tt][Ii][Oo][Nn][Aa][Ll]/,
      /[Pp][Aa][Rr][Aa][Mm][Aa][Rr][Rr][Aa][Yy]/
    ),

    visibility: $ => choice(
      /[Pp][Rr][Ii][Vv][Aa][Tt][Ee]/,
      /[Pp][Uu][Bb][Ll][Ii][Cc]/
    ),

    type: $ => choice(
      $.type_terminal,
      $.array_type
    ),

    type_terminal: $ => choice(
      /[Aa][Nn][Yy]/,
      /[Bb][Oo][Oo][Ll][Ee][Aa][Nn]/,
      /[Bb][Yy][Tt][Ee]/,
      /[Cc][Oo][Ll][Ll][Ee][Cc][Tt][Ii][Oo][Nn]/,
      /[Cc][Uu][Rr][Rr][Ee][Nn][Cc][Yy]/,
      /[Dd][Aa][Tt][Ee]/,
      /[Dd][Ee][Cc][Ii][Mm][Aa][Ll]/,
      /[Dd][Ii][Cc][Tt][Ii][Oo][Nn][Aa][Rr][Yy]/,
      /[Dd][Oo][Uu][Bb][Ll][Ee]/,
      /[Ii][Nn][Tt][Ee][Gg][Ee][Rr]/,
      /[Ll][Oo][Nn][Gg]/,
      /[Ll][Oo][Nn][Gg][Ll][Oo][Nn][Gg]/,
      /[Ll][Oo][Nn][Gg][Pp][Tt][Rr]/,
      /[Oo][Bb][Jj][Ee][Cc][Tt]/,
      /[Ss][Ii][Nn][Gg][Ll][Ee]/,
      /[Ss][Tt][Rr][Ii][Nn][Gg]/,
      /[Vv][Aa][Rr][Ii][Aa][Nn][Tt]/,
      $.type_member_expression,
    ),

    array_type: $ => seq(
      $.type,
      '()'
    ),

    _expression: $ => choice(
      $.member_expression,
      $.function_call,
      $.event_raise,
      seq('(',$._expression, ')'),
      $.new_expression,
      $.literal,
      $.binary_expression,
      $.unary_expression,
      $.identifier
    ),

    new_expression: $ => prec('new', seq(
      /[Nn][Ee][Ww]/,
      choice(
        $.identifier,
        $.type_member_expression
      )
    )),

    type_member_expression: $ => prec('member',seq(
      choice(
        $.identifier,
        $.member_expression
      ),
      '.',
      choice($.identifier)
    )),

    member_expression: $ => prec('member',seq(
      $._expression,
      '.',
      choice(
        $.function_call,
        $.identifier
      )
    )),

    binary_expression: $ => prec.left(choice(
      prec('additive',seq($._expression, '+', $._expression)),
      prec('additive',seq($._expression, '-', $._expression)),
      prec('multiplicative',seq($._expression, '*', $._expression)),
      prec('multiplicative',seq($._expression, '/', $._expression)),
      prec('multiplicative',seq($._expression, /[Mm][Oo][Dd]/, $._expression)),
      prec('exponential', seq($._expression, '^', $._expression)),
      prec('boolean',seq($._expression, '&', $._expression)),
      prec('boolean',seq($._expression, /[Aa][Nn][Dd]/, $._expression)),
      prec('boolean',seq($._expression, /[Oo][Rr]/, $._expression)),
      prec('boolean',seq($._expression, /[Xx][Oo][Rr]/, $._expression)),
      prec('boolean',seq($._expression, $._equal, $._expression)),
      prec('boolean',seq($._expression, '<>', $._expression)),
      prec('boolean',seq($._expression, '<', $._expression)),
      prec('boolean',seq($._expression, '>', $._expression)),
      prec('boolean',seq($._expression, '<=', $._expression)),
      prec('boolean',seq($._expression, '>=', $._expression))
    )),

    unary_expression: $ => prec.right(choice(
      seq('-', $._expression),
      seq(/[Nn][Oo][Tt]/, $._expression)
    )),

    function_call: $ => prec('call',seq(
      optional(/[Cc][Aa][Ll][Ll]/),
      $.identifier,
      '(',
      optional($.argument_list),
      ')'
    )),

    event_raise: $ => prec('call',seq(
      /[Rr][Aa][Ii][Ss][Ee][Ee][Vv][Ee][Nn][Tt]]/,
      $.identifier,
      '(',
      optional($.argument_list),
      ')'
    )),

    argument_list: $ => seq(
      $.argument,
      repeat(seq(
        ',',
        $.argument
      ))
    ),

    argument: $ => choice(
        $._expression,
        $.keyword_argument
    ),

    keyword_argument: $ => seq(
      $.identifier,
      ':=',
      $._expression
    ),

    array_element: $ => seq(
      $.identifier,
      '(',
      $._expression,
      ')'
    ),

    literal: $ => choice(
      $.number,
      $.string_literal,
      $.boolean
    ),

    number: $ => /\d+/,

    string_literal: $ => seq('"', /[^"]*/, '"'),

    boolean: $ => choice(/[Tt][Rr][Uu][Ee]/, /[Ff][Aa][Ll][Ss][Ee]/),

    new_identifier: $ => $.identifier,

    identifier: $ => /[a-zA-Z_]\w*/,

    _equal: $ => '=',

    _whitespace: $ => repeat1(/[\n\r]/),

    _horizontal_whitespace: $=> /[ \t]+/
  }
});

