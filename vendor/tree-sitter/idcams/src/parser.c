#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 24
#define LARGE_STATE_COUNT 7
#define SYMBOL_COUNT 32
#define ALIAS_COUNT 0
#define TOKEN_COUNT 20
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 4
#define PRODUCTION_ID_COUNT 1

enum ts_symbol_identifiers {
  sym_comment = 1,
  anon_sym_REPRO = 2,
  anon_sym_DEFINE = 3,
  anon_sym_DELETE = 4,
  anon_sym_PRINT = 5,
  anon_sym_LISTCAT = 6,
  anon_sym_SET = 7,
  anon_sym_VERIFY = 8,
  anon_sym_ALTER = 9,
  anon_sym_BLDINDEX = 10,
  anon_sym_EXPORT = 11,
  anon_sym_IMPORT = 12,
  anon_sym_LPAREN = 13,
  anon_sym_RPAREN = 14,
  anon_sym_COMMA = 15,
  sym_continuation = 16,
  aux_sym_keyword_token1 = 17,
  sym_dataset_name = 18,
  sym_number = 19,
  sym_source_file = 20,
  sym_statement = 21,
  sym_command = 22,
  sym_parameter = 23,
  sym_keyword_param = 24,
  sym_param_content = 25,
  sym_nested_paren = 26,
  sym_keyword = 27,
  sym_identifier = 28,
  aux_sym_source_file_repeat1 = 29,
  aux_sym_statement_repeat1 = 30,
  aux_sym_param_content_repeat1 = 31,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_comment] = "comment",
  [anon_sym_REPRO] = "REPRO",
  [anon_sym_DEFINE] = "DEFINE",
  [anon_sym_DELETE] = "DELETE",
  [anon_sym_PRINT] = "PRINT",
  [anon_sym_LISTCAT] = "LISTCAT",
  [anon_sym_SET] = "SET",
  [anon_sym_VERIFY] = "VERIFY",
  [anon_sym_ALTER] = "ALTER",
  [anon_sym_BLDINDEX] = "BLDINDEX",
  [anon_sym_EXPORT] = "EXPORT",
  [anon_sym_IMPORT] = "IMPORT",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_COMMA] = ",",
  [sym_continuation] = "continuation",
  [aux_sym_keyword_token1] = "keyword_token1",
  [sym_dataset_name] = "dataset_name",
  [sym_number] = "number",
  [sym_source_file] = "source_file",
  [sym_statement] = "statement",
  [sym_command] = "command",
  [sym_parameter] = "parameter",
  [sym_keyword_param] = "keyword_param",
  [sym_param_content] = "param_content",
  [sym_nested_paren] = "nested_paren",
  [sym_keyword] = "keyword",
  [sym_identifier] = "identifier",
  [aux_sym_source_file_repeat1] = "source_file_repeat1",
  [aux_sym_statement_repeat1] = "statement_repeat1",
  [aux_sym_param_content_repeat1] = "param_content_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_comment] = sym_comment,
  [anon_sym_REPRO] = anon_sym_REPRO,
  [anon_sym_DEFINE] = anon_sym_DEFINE,
  [anon_sym_DELETE] = anon_sym_DELETE,
  [anon_sym_PRINT] = anon_sym_PRINT,
  [anon_sym_LISTCAT] = anon_sym_LISTCAT,
  [anon_sym_SET] = anon_sym_SET,
  [anon_sym_VERIFY] = anon_sym_VERIFY,
  [anon_sym_ALTER] = anon_sym_ALTER,
  [anon_sym_BLDINDEX] = anon_sym_BLDINDEX,
  [anon_sym_EXPORT] = anon_sym_EXPORT,
  [anon_sym_IMPORT] = anon_sym_IMPORT,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [sym_continuation] = sym_continuation,
  [aux_sym_keyword_token1] = aux_sym_keyword_token1,
  [sym_dataset_name] = sym_dataset_name,
  [sym_number] = sym_number,
  [sym_source_file] = sym_source_file,
  [sym_statement] = sym_statement,
  [sym_command] = sym_command,
  [sym_parameter] = sym_parameter,
  [sym_keyword_param] = sym_keyword_param,
  [sym_param_content] = sym_param_content,
  [sym_nested_paren] = sym_nested_paren,
  [sym_keyword] = sym_keyword,
  [sym_identifier] = sym_identifier,
  [aux_sym_source_file_repeat1] = aux_sym_source_file_repeat1,
  [aux_sym_statement_repeat1] = aux_sym_statement_repeat1,
  [aux_sym_param_content_repeat1] = aux_sym_param_content_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_comment] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_REPRO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DEFINE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DELETE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PRINT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LISTCAT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SET] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_VERIFY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ALTER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BLDINDEX] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EXPORT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_IMPORT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [sym_continuation] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_keyword_token1] = {
    .visible = false,
    .named = false,
  },
  [sym_dataset_name] = {
    .visible = true,
    .named = true,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [sym_source_file] = {
    .visible = true,
    .named = true,
  },
  [sym_statement] = {
    .visible = true,
    .named = true,
  },
  [sym_command] = {
    .visible = true,
    .named = true,
  },
  [sym_parameter] = {
    .visible = true,
    .named = true,
  },
  [sym_keyword_param] = {
    .visible = true,
    .named = true,
  },
  [sym_param_content] = {
    .visible = true,
    .named = true,
  },
  [sym_nested_paren] = {
    .visible = true,
    .named = true,
  },
  [sym_keyword] = {
    .visible = true,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_source_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_statement_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_param_content_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 7,
  [21] = 21,
  [22] = 22,
  [23] = 23,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(6);
      if (lookahead == '\n') SKIP(0);
      if (lookahead == '\r') SKIP(5);
      if (lookahead == '(') ADVANCE(19);
      if (lookahead == ')') ADVANCE(20);
      if (lookahead == ',') ADVANCE(21);
      if (lookahead == '-') ADVANCE(22);
      if (lookahead == '/') ADVANCE(3);
      if (lookahead == 'A') ADVANCE(44);
      if (lookahead == 'B') ADVANCE(45);
      if (lookahead == 'D') ADVANCE(28);
      if (lookahead == 'E') ADVANCE(71);
      if (lookahead == 'I') ADVANCE(46);
      if (lookahead == 'L') ADVANCE(39);
      if (lookahead == 'P') ADVANCE(57);
      if (lookahead == 'R') ADVANCE(33);
      if (lookahead == 'S') ADVANCE(32);
      if (lookahead == 'V') ADVANCE(35);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(76);
      if (('C' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 1:
      if (lookahead == '\n') SKIP(2);
      END_STATE();
    case 2:
      if (lookahead == '\n') SKIP(2);
      if (lookahead == '\r') SKIP(1);
      if (lookahead == '(') ADVANCE(19);
      if (lookahead == ')') ADVANCE(20);
      if (lookahead == ',') ADVANCE(21);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(76);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(23);
      END_STATE();
    case 3:
      if (lookahead == '*') ADVANCE(7);
      END_STATE();
    case 4:
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(75);
      END_STATE();
    case 5:
      if (eof) ADVANCE(6);
      if (lookahead == '\n') SKIP(0);
      END_STATE();
    case 6:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 7:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '*') ADVANCE(7);
      if (lookahead == '/') ADVANCE(7);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(7);
      END_STATE();
    case 8:
      ACCEPT_TOKEN(anon_sym_REPRO);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 9:
      ACCEPT_TOKEN(anon_sym_DEFINE);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 10:
      ACCEPT_TOKEN(anon_sym_DELETE);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 11:
      ACCEPT_TOKEN(anon_sym_PRINT);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 12:
      ACCEPT_TOKEN(anon_sym_LISTCAT);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 13:
      ACCEPT_TOKEN(anon_sym_SET);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 14:
      ACCEPT_TOKEN(anon_sym_VERIFY);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 15:
      ACCEPT_TOKEN(anon_sym_ALTER);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 16:
      ACCEPT_TOKEN(anon_sym_BLDINDEX);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 17:
      ACCEPT_TOKEN(anon_sym_EXPORT);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 18:
      ACCEPT_TOKEN(anon_sym_IMPORT);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 19:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 20:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 21:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 22:
      ACCEPT_TOKEN(sym_continuation);
      END_STATE();
    case 23:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == '.') ADVANCE(4);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(23);
      END_STATE();
    case 24:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'A') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 25:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'C') ADVANCE(24);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 26:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'D') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 27:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'D') ADVANCE(31);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 28:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(38);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 29:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(9);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 30:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(10);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 31:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(72);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 32:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(63);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(54);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(56);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(59);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'E') ADVANCE(70);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'F') ADVANCE(73);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'F') ADVANCE(43);
      if (lookahead == 'L') ADVANCE(36);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'I') ADVANCE(62);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'I') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'I') ADVANCE(37);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'I') ADVANCE(47);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'I') ADVANCE(49);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'L') ADVANCE(69);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'L') ADVANCE(26);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'M') ADVANCE(55);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'N') ADVANCE(27);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'N') ADVANCE(65);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'N') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'O') ADVANCE(8);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'O') ADVANCE(60);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'O') ADVANCE(61);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'P') ADVANCE(51);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'P') ADVANCE(58);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'P') ADVANCE(52);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'R') ADVANCE(15);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'R') ADVANCE(40);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'R') ADVANCE(50);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'R') ADVANCE(41);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'R') ADVANCE(66);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'R') ADVANCE(67);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'S') ADVANCE(64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(13);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(25);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(11);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(17);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(18);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(12);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(34);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'T') ADVANCE(30);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'X') ADVANCE(53);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'X') ADVANCE(16);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (lookahead == 'Y') ADVANCE(14);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(aux_sym_keyword_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(74);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(sym_dataset_name);
      if (lookahead == '.') ADVANCE(4);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(75);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(76);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 0},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 0},
  [4] = {.lex_state = 0},
  [5] = {.lex_state = 0},
  [6] = {.lex_state = 0},
  [7] = {.lex_state = 0},
  [8] = {.lex_state = 0},
  [9] = {.lex_state = 0},
  [10] = {.lex_state = 0},
  [11] = {.lex_state = 0},
  [12] = {.lex_state = 0},
  [13] = {.lex_state = 0},
  [14] = {.lex_state = 2},
  [15] = {.lex_state = 2},
  [16] = {.lex_state = 2},
  [17] = {.lex_state = 2},
  [18] = {.lex_state = 2},
  [19] = {.lex_state = 2},
  [20] = {.lex_state = 2},
  [21] = {.lex_state = 0},
  [22] = {.lex_state = 0},
  [23] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_comment] = ACTIONS(1),
    [anon_sym_REPRO] = ACTIONS(1),
    [anon_sym_DEFINE] = ACTIONS(1),
    [anon_sym_DELETE] = ACTIONS(1),
    [anon_sym_PRINT] = ACTIONS(1),
    [anon_sym_LISTCAT] = ACTIONS(1),
    [anon_sym_SET] = ACTIONS(1),
    [anon_sym_VERIFY] = ACTIONS(1),
    [anon_sym_ALTER] = ACTIONS(1),
    [anon_sym_BLDINDEX] = ACTIONS(1),
    [anon_sym_EXPORT] = ACTIONS(1),
    [anon_sym_IMPORT] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [sym_continuation] = ACTIONS(1),
    [aux_sym_keyword_token1] = ACTIONS(1),
    [sym_number] = ACTIONS(1),
  },
  [1] = {
    [sym_source_file] = STATE(21),
    [sym_statement] = STATE(5),
    [sym_command] = STATE(2),
    [sym_identifier] = STATE(10),
    [aux_sym_source_file_repeat1] = STATE(5),
    [ts_builtin_sym_end] = ACTIONS(3),
    [sym_comment] = ACTIONS(5),
    [anon_sym_REPRO] = ACTIONS(7),
    [anon_sym_DEFINE] = ACTIONS(7),
    [anon_sym_DELETE] = ACTIONS(7),
    [anon_sym_PRINT] = ACTIONS(7),
    [anon_sym_LISTCAT] = ACTIONS(7),
    [anon_sym_SET] = ACTIONS(7),
    [anon_sym_VERIFY] = ACTIONS(7),
    [anon_sym_ALTER] = ACTIONS(7),
    [anon_sym_BLDINDEX] = ACTIONS(7),
    [anon_sym_EXPORT] = ACTIONS(7),
    [anon_sym_IMPORT] = ACTIONS(7),
    [aux_sym_keyword_token1] = ACTIONS(9),
  },
  [2] = {
    [sym_parameter] = STATE(3),
    [sym_keyword_param] = STATE(11),
    [sym_keyword] = STATE(8),
    [aux_sym_statement_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(11),
    [sym_comment] = ACTIONS(11),
    [anon_sym_REPRO] = ACTIONS(13),
    [anon_sym_DEFINE] = ACTIONS(13),
    [anon_sym_DELETE] = ACTIONS(13),
    [anon_sym_PRINT] = ACTIONS(13),
    [anon_sym_LISTCAT] = ACTIONS(13),
    [anon_sym_SET] = ACTIONS(13),
    [anon_sym_VERIFY] = ACTIONS(13),
    [anon_sym_ALTER] = ACTIONS(13),
    [anon_sym_BLDINDEX] = ACTIONS(13),
    [anon_sym_EXPORT] = ACTIONS(13),
    [anon_sym_IMPORT] = ACTIONS(13),
    [sym_continuation] = ACTIONS(15),
    [aux_sym_keyword_token1] = ACTIONS(17),
  },
  [3] = {
    [sym_parameter] = STATE(4),
    [sym_keyword_param] = STATE(11),
    [sym_keyword] = STATE(8),
    [aux_sym_statement_repeat1] = STATE(4),
    [ts_builtin_sym_end] = ACTIONS(20),
    [sym_comment] = ACTIONS(20),
    [anon_sym_REPRO] = ACTIONS(22),
    [anon_sym_DEFINE] = ACTIONS(22),
    [anon_sym_DELETE] = ACTIONS(22),
    [anon_sym_PRINT] = ACTIONS(22),
    [anon_sym_LISTCAT] = ACTIONS(22),
    [anon_sym_SET] = ACTIONS(22),
    [anon_sym_VERIFY] = ACTIONS(22),
    [anon_sym_ALTER] = ACTIONS(22),
    [anon_sym_BLDINDEX] = ACTIONS(22),
    [anon_sym_EXPORT] = ACTIONS(22),
    [anon_sym_IMPORT] = ACTIONS(22),
    [sym_continuation] = ACTIONS(15),
    [aux_sym_keyword_token1] = ACTIONS(24),
  },
  [4] = {
    [sym_parameter] = STATE(4),
    [sym_keyword_param] = STATE(11),
    [sym_keyword] = STATE(8),
    [aux_sym_statement_repeat1] = STATE(4),
    [ts_builtin_sym_end] = ACTIONS(27),
    [sym_comment] = ACTIONS(27),
    [anon_sym_REPRO] = ACTIONS(29),
    [anon_sym_DEFINE] = ACTIONS(29),
    [anon_sym_DELETE] = ACTIONS(29),
    [anon_sym_PRINT] = ACTIONS(29),
    [anon_sym_LISTCAT] = ACTIONS(29),
    [anon_sym_SET] = ACTIONS(29),
    [anon_sym_VERIFY] = ACTIONS(29),
    [anon_sym_ALTER] = ACTIONS(29),
    [anon_sym_BLDINDEX] = ACTIONS(29),
    [anon_sym_EXPORT] = ACTIONS(29),
    [anon_sym_IMPORT] = ACTIONS(29),
    [sym_continuation] = ACTIONS(31),
    [aux_sym_keyword_token1] = ACTIONS(34),
  },
  [5] = {
    [sym_statement] = STATE(6),
    [sym_command] = STATE(2),
    [sym_identifier] = STATE(10),
    [aux_sym_source_file_repeat1] = STATE(6),
    [ts_builtin_sym_end] = ACTIONS(37),
    [sym_comment] = ACTIONS(39),
    [anon_sym_REPRO] = ACTIONS(7),
    [anon_sym_DEFINE] = ACTIONS(7),
    [anon_sym_DELETE] = ACTIONS(7),
    [anon_sym_PRINT] = ACTIONS(7),
    [anon_sym_LISTCAT] = ACTIONS(7),
    [anon_sym_SET] = ACTIONS(7),
    [anon_sym_VERIFY] = ACTIONS(7),
    [anon_sym_ALTER] = ACTIONS(7),
    [anon_sym_BLDINDEX] = ACTIONS(7),
    [anon_sym_EXPORT] = ACTIONS(7),
    [anon_sym_IMPORT] = ACTIONS(7),
    [aux_sym_keyword_token1] = ACTIONS(9),
  },
  [6] = {
    [sym_statement] = STATE(6),
    [sym_command] = STATE(2),
    [sym_identifier] = STATE(10),
    [aux_sym_source_file_repeat1] = STATE(6),
    [ts_builtin_sym_end] = ACTIONS(41),
    [sym_comment] = ACTIONS(43),
    [anon_sym_REPRO] = ACTIONS(46),
    [anon_sym_DEFINE] = ACTIONS(46),
    [anon_sym_DELETE] = ACTIONS(46),
    [anon_sym_PRINT] = ACTIONS(46),
    [anon_sym_LISTCAT] = ACTIONS(46),
    [anon_sym_SET] = ACTIONS(46),
    [anon_sym_VERIFY] = ACTIONS(46),
    [anon_sym_ALTER] = ACTIONS(46),
    [anon_sym_BLDINDEX] = ACTIONS(46),
    [anon_sym_EXPORT] = ACTIONS(46),
    [anon_sym_IMPORT] = ACTIONS(46),
    [aux_sym_keyword_token1] = ACTIONS(49),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 2,
    ACTIONS(52), 4,
      ts_builtin_sym_end,
      sym_comment,
      anon_sym_LPAREN,
      sym_continuation,
    ACTIONS(54), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [21] = 3,
    ACTIONS(60), 1,
      anon_sym_LPAREN,
    ACTIONS(56), 3,
      ts_builtin_sym_end,
      sym_comment,
      sym_continuation,
    ACTIONS(58), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [44] = 2,
    ACTIONS(62), 3,
      ts_builtin_sym_end,
      sym_comment,
      sym_continuation,
    ACTIONS(64), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [64] = 2,
    ACTIONS(66), 3,
      ts_builtin_sym_end,
      sym_comment,
      sym_continuation,
    ACTIONS(68), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [84] = 2,
    ACTIONS(70), 3,
      ts_builtin_sym_end,
      sym_comment,
      sym_continuation,
    ACTIONS(72), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [104] = 2,
    ACTIONS(74), 3,
      ts_builtin_sym_end,
      sym_comment,
      sym_continuation,
    ACTIONS(76), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [124] = 2,
    ACTIONS(78), 3,
      ts_builtin_sym_end,
      sym_comment,
      sym_continuation,
    ACTIONS(80), 12,
      anon_sym_REPRO,
      anon_sym_DEFINE,
      anon_sym_DELETE,
      anon_sym_PRINT,
      anon_sym_LISTCAT,
      anon_sym_SET,
      anon_sym_VERIFY,
      anon_sym_ALTER,
      anon_sym_BLDINDEX,
      anon_sym_EXPORT,
      anon_sym_IMPORT,
      aux_sym_keyword_token1,
  [144] = 6,
    ACTIONS(82), 1,
      anon_sym_LPAREN,
    ACTIONS(84), 1,
      anon_sym_RPAREN,
    ACTIONS(88), 1,
      aux_sym_keyword_token1,
    STATE(23), 1,
      sym_param_content,
    ACTIONS(86), 3,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
    STATE(16), 3,
      sym_nested_paren,
      sym_keyword,
      aux_sym_param_content_repeat1,
  [167] = 6,
    ACTIONS(82), 1,
      anon_sym_LPAREN,
    ACTIONS(88), 1,
      aux_sym_keyword_token1,
    ACTIONS(90), 1,
      anon_sym_RPAREN,
    STATE(22), 1,
      sym_param_content,
    ACTIONS(86), 3,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
    STATE(16), 3,
      sym_nested_paren,
      sym_keyword,
      aux_sym_param_content_repeat1,
  [190] = 5,
    ACTIONS(82), 1,
      anon_sym_LPAREN,
    ACTIONS(88), 1,
      aux_sym_keyword_token1,
    ACTIONS(92), 1,
      anon_sym_RPAREN,
    ACTIONS(94), 3,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
    STATE(17), 3,
      sym_nested_paren,
      sym_keyword,
      aux_sym_param_content_repeat1,
  [210] = 5,
    ACTIONS(96), 1,
      anon_sym_LPAREN,
    ACTIONS(99), 1,
      anon_sym_RPAREN,
    ACTIONS(104), 1,
      aux_sym_keyword_token1,
    ACTIONS(101), 3,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
    STATE(17), 3,
      sym_nested_paren,
      sym_keyword,
      aux_sym_param_content_repeat1,
  [230] = 2,
    ACTIONS(109), 1,
      aux_sym_keyword_token1,
    ACTIONS(107), 5,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
  [241] = 2,
    ACTIONS(113), 1,
      aux_sym_keyword_token1,
    ACTIONS(111), 5,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
  [252] = 2,
    ACTIONS(54), 1,
      aux_sym_keyword_token1,
    ACTIONS(52), 5,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_COMMA,
      sym_dataset_name,
      sym_number,
  [263] = 1,
    ACTIONS(115), 1,
      ts_builtin_sym_end,
  [267] = 1,
    ACTIONS(117), 1,
      anon_sym_RPAREN,
  [271] = 1,
    ACTIONS(119), 1,
      anon_sym_RPAREN,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(7)] = 0,
  [SMALL_STATE(8)] = 21,
  [SMALL_STATE(9)] = 44,
  [SMALL_STATE(10)] = 64,
  [SMALL_STATE(11)] = 84,
  [SMALL_STATE(12)] = 104,
  [SMALL_STATE(13)] = 124,
  [SMALL_STATE(14)] = 144,
  [SMALL_STATE(15)] = 167,
  [SMALL_STATE(16)] = 190,
  [SMALL_STATE(17)] = 210,
  [SMALL_STATE(18)] = 230,
  [SMALL_STATE(19)] = 241,
  [SMALL_STATE(20)] = 252,
  [SMALL_STATE(21)] = 263,
  [SMALL_STATE(22)] = 267,
  [SMALL_STATE(23)] = 271,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(10),
  [9] = {.entry = {.count = 1, .reusable = false}}, SHIFT(9),
  [11] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement, 1, 0, 0),
  [13] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_statement, 1, 0, 0),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [17] = {.entry = {.count = 2, .reusable = false}}, REDUCE(sym_statement, 1, 0, 0), SHIFT(7),
  [20] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement, 2, 0, 0),
  [22] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_statement, 2, 0, 0),
  [24] = {.entry = {.count = 2, .reusable = false}}, REDUCE(sym_statement, 2, 0, 0), SHIFT(7),
  [27] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_statement_repeat1, 2, 0, 0),
  [29] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_statement_repeat1, 2, 0, 0),
  [31] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_statement_repeat1, 2, 0, 0), SHIFT_REPEAT(11),
  [34] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_repeat1, 2, 0, 0), SHIFT_REPEAT(7),
  [37] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [39] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [41] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [43] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(6),
  [46] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(10),
  [49] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(9),
  [52] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_keyword, 1, 0, 0),
  [54] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_keyword, 1, 0, 0),
  [56] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_keyword_param, 1, 0, 0),
  [58] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_keyword_param, 1, 0, 0),
  [60] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [62] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [64] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_identifier, 1, 0, 0),
  [66] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_command, 1, 0, 0),
  [68] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_command, 1, 0, 0),
  [70] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_parameter, 1, 0, 0),
  [72] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_parameter, 1, 0, 0),
  [74] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_keyword_param, 3, 0, 0),
  [76] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_keyword_param, 3, 0, 0),
  [78] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_keyword_param, 4, 0, 0),
  [80] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_keyword_param, 4, 0, 0),
  [82] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [84] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [86] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [88] = {.entry = {.count = 1, .reusable = false}}, SHIFT(20),
  [90] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [92] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_param_content, 1, 0, 0),
  [94] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [96] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_param_content_repeat1, 2, 0, 0), SHIFT_REPEAT(15),
  [99] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_param_content_repeat1, 2, 0, 0),
  [101] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_param_content_repeat1, 2, 0, 0), SHIFT_REPEAT(17),
  [104] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_param_content_repeat1, 2, 0, 0), SHIFT_REPEAT(20),
  [107] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_nested_paren, 2, 0, 0),
  [109] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_nested_paren, 2, 0, 0),
  [111] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_nested_paren, 3, 0, 0),
  [113] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_nested_paren, 3, 0, 0),
  [115] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [117] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [119] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef TREE_SITTER_HIDE_SYMBOLS
#define TS_PUBLIC
#elif defined(_WIN32)
#define TS_PUBLIC __declspec(dllexport)
#else
#define TS_PUBLIC __attribute__((visibility("default")))
#endif

TS_PUBLIC const TSLanguage *tree_sitter_idcams(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
