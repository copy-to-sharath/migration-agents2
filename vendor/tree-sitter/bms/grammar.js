/**
 * Tree-sitter grammar for BMS (Basic Mapping Support)
 * BMS is IBM's screen definition language for CICS
 * BMS macros define screen layouts for 3270 terminals
 * 
 * Uses an external scanner to handle HLASM card format:
 * - Columns 1-71: Content
 * - Column 72: Continuation marker (non-blank = continued)
 * - Columns 73-80: Sequence numbers (ignored)
 */

module.exports = grammar({
  name: 'bms',

  externals: $ => [
    $.statement_line,    // A single physical line of content (columns 1-71)
    $.comment_line,      // Full comment line (starts with *)
  ],

  extras: $ => [
    /[ \t]+/,
  ],

  rules: {
    source_file: $ => repeat($._line),

    _line: $ => choice(
      $.statement_line,
      $.comment_line,
      $.blank_line,
    ),

    blank_line: $ => /\r?\n/,
  },
});
