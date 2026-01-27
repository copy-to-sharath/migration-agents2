/**
 * Tree-sitter grammar for IBM HLASM (High Level Assembler)
 * Simplified grammar for symbol and call extraction
 */

module.exports = grammar({
  name: 'hlasm',

  extras: $ => [/[ \t]+/],

  rules: {
    source_file: $ => repeat($._line),

    _line: $ => choice(
      $.comment_line,
      $.statement,
      $.blank_line
    ),

    blank_line: $ => /\r?\n/,

    // Full-line comment (starts with * in column 1)
    comment_line: $ => seq(
      '*',
      optional(/[^\r\n]+/),
      /\r?\n/
    ),

    // Main statement: [label] operation [operands] [comment]
    statement: $ => seq(
      optional($.label),
      $.operation,
      optional($.operands),
      /\r?\n/
    ),

    // Label in column 1
    label: $ => /[A-Z@#$_][A-Z0-9@#$_]{0,62}/,

    // Operation (mnemonic, directive, or macro name)
    operation: $ => /[A-Z@#$_][A-Z0-9@#$_]*/,

    // Everything after operation until newline
    operands: $ => /[^\r\n]+/
  }
});
