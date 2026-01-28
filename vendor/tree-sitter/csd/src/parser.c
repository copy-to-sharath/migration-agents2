#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 74
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 47
#define ALIAS_COUNT 0
#define TOKEN_COUNT 24
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 1

enum ts_symbol_identifiers {
  sym_comment = 1,
  anon_sym_DEFINE = 2,
  anon_sym_FILE = 3,
  anon_sym_LPAREN = 4,
  anon_sym_RPAREN = 5,
  anon_sym_MAPSET = 6,
  anon_sym_PROGRAM = 7,
  anon_sym_TRANSACTION = 8,
  anon_sym_TDQUEUE = 9,
  anon_sym_TSQUEUE = 10,
  anon_sym_TSMODEL = 11,
  anon_sym_CONNECTION = 12,
  anon_sym_SESSIONS = 13,
  anon_sym_DESCRIPTION = 14,
  anon_sym_GROUP = 15,
  aux_sym_attribute_name_token1 = 16,
  anon_sym_COMMA = 17,
  sym_description_text = 18,
  sym_dataset_name = 19,
  sym_datetime = 20,
  sym_number = 21,
  anon_sym_YES = 22,
  anon_sym_NO = 23,
  sym_source_file = 24,
  sym_definition = 25,
  sym_define_file = 26,
  sym_define_mapset = 27,
  sym_define_program = 28,
  sym_define_transaction = 29,
  sym_define_tdqueue = 30,
  sym_define_tsqueue = 31,
  sym_define_connection = 32,
  sym_define_sessions = 33,
  sym_generic_define = 34,
  sym_attribute = 35,
  sym_attribute_name = 36,
  sym_attribute_value = 37,
  sym_number_list = 38,
  sym_group_name = 39,
  sym_resource_type = 40,
  sym_resource_name = 41,
  sym_identifier = 42,
  sym_yes_no = 43,
  aux_sym_source_file_repeat1 = 44,
  aux_sym_define_file_repeat1 = 45,
  aux_sym_number_list_repeat1 = 46,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_comment] = "comment",
  [anon_sym_DEFINE] = "DEFINE",
  [anon_sym_FILE] = "FILE",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_MAPSET] = "MAPSET",
  [anon_sym_PROGRAM] = "PROGRAM",
  [anon_sym_TRANSACTION] = "TRANSACTION",
  [anon_sym_TDQUEUE] = "TDQUEUE",
  [anon_sym_TSQUEUE] = "TSQUEUE",
  [anon_sym_TSMODEL] = "TSMODEL",
  [anon_sym_CONNECTION] = "CONNECTION",
  [anon_sym_SESSIONS] = "SESSIONS",
  [anon_sym_DESCRIPTION] = "DESCRIPTION",
  [anon_sym_GROUP] = "GROUP",
  [aux_sym_attribute_name_token1] = "attribute_name_token1",
  [anon_sym_COMMA] = ",",
  [sym_description_text] = "description_text",
  [sym_dataset_name] = "dataset_name",
  [sym_datetime] = "datetime",
  [sym_number] = "number",
  [anon_sym_YES] = "YES",
  [anon_sym_NO] = "NO",
  [sym_source_file] = "source_file",
  [sym_definition] = "definition",
  [sym_define_file] = "define_file",
  [sym_define_mapset] = "define_mapset",
  [sym_define_program] = "define_program",
  [sym_define_transaction] = "define_transaction",
  [sym_define_tdqueue] = "define_tdqueue",
  [sym_define_tsqueue] = "define_tsqueue",
  [sym_define_connection] = "define_connection",
  [sym_define_sessions] = "define_sessions",
  [sym_generic_define] = "generic_define",
  [sym_attribute] = "attribute",
  [sym_attribute_name] = "attribute_name",
  [sym_attribute_value] = "attribute_value",
  [sym_number_list] = "number_list",
  [sym_group_name] = "group_name",
  [sym_resource_type] = "resource_type",
  [sym_resource_name] = "resource_name",
  [sym_identifier] = "identifier",
  [sym_yes_no] = "yes_no",
  [aux_sym_source_file_repeat1] = "source_file_repeat1",
  [aux_sym_define_file_repeat1] = "define_file_repeat1",
  [aux_sym_number_list_repeat1] = "number_list_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_comment] = sym_comment,
  [anon_sym_DEFINE] = anon_sym_DEFINE,
  [anon_sym_FILE] = anon_sym_FILE,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_MAPSET] = anon_sym_MAPSET,
  [anon_sym_PROGRAM] = anon_sym_PROGRAM,
  [anon_sym_TRANSACTION] = anon_sym_TRANSACTION,
  [anon_sym_TDQUEUE] = anon_sym_TDQUEUE,
  [anon_sym_TSQUEUE] = anon_sym_TSQUEUE,
  [anon_sym_TSMODEL] = anon_sym_TSMODEL,
  [anon_sym_CONNECTION] = anon_sym_CONNECTION,
  [anon_sym_SESSIONS] = anon_sym_SESSIONS,
  [anon_sym_DESCRIPTION] = anon_sym_DESCRIPTION,
  [anon_sym_GROUP] = anon_sym_GROUP,
  [aux_sym_attribute_name_token1] = aux_sym_attribute_name_token1,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [sym_description_text] = sym_description_text,
  [sym_dataset_name] = sym_dataset_name,
  [sym_datetime] = sym_datetime,
  [sym_number] = sym_number,
  [anon_sym_YES] = anon_sym_YES,
  [anon_sym_NO] = anon_sym_NO,
  [sym_source_file] = sym_source_file,
  [sym_definition] = sym_definition,
  [sym_define_file] = sym_define_file,
  [sym_define_mapset] = sym_define_mapset,
  [sym_define_program] = sym_define_program,
  [sym_define_transaction] = sym_define_transaction,
  [sym_define_tdqueue] = sym_define_tdqueue,
  [sym_define_tsqueue] = sym_define_tsqueue,
  [sym_define_connection] = sym_define_connection,
  [sym_define_sessions] = sym_define_sessions,
  [sym_generic_define] = sym_generic_define,
  [sym_attribute] = sym_attribute,
  [sym_attribute_name] = sym_attribute_name,
  [sym_attribute_value] = sym_attribute_value,
  [sym_number_list] = sym_number_list,
  [sym_group_name] = sym_group_name,
  [sym_resource_type] = sym_resource_type,
  [sym_resource_name] = sym_resource_name,
  [sym_identifier] = sym_identifier,
  [sym_yes_no] = sym_yes_no,
  [aux_sym_source_file_repeat1] = aux_sym_source_file_repeat1,
  [aux_sym_define_file_repeat1] = aux_sym_define_file_repeat1,
  [aux_sym_number_list_repeat1] = aux_sym_number_list_repeat1,
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
  [anon_sym_DEFINE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FILE] = {
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
  [anon_sym_MAPSET] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PROGRAM] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TRANSACTION] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TDQUEUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TSQUEUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TSMODEL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CONNECTION] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SESSIONS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DESCRIPTION] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GROUP] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_attribute_name_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [sym_description_text] = {
    .visible = true,
    .named = true,
  },
  [sym_dataset_name] = {
    .visible = true,
    .named = true,
  },
  [sym_datetime] = {
    .visible = true,
    .named = true,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_YES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NO] = {
    .visible = true,
    .named = false,
  },
  [sym_source_file] = {
    .visible = true,
    .named = true,
  },
  [sym_definition] = {
    .visible = true,
    .named = true,
  },
  [sym_define_file] = {
    .visible = true,
    .named = true,
  },
  [sym_define_mapset] = {
    .visible = true,
    .named = true,
  },
  [sym_define_program] = {
    .visible = true,
    .named = true,
  },
  [sym_define_transaction] = {
    .visible = true,
    .named = true,
  },
  [sym_define_tdqueue] = {
    .visible = true,
    .named = true,
  },
  [sym_define_tsqueue] = {
    .visible = true,
    .named = true,
  },
  [sym_define_connection] = {
    .visible = true,
    .named = true,
  },
  [sym_define_sessions] = {
    .visible = true,
    .named = true,
  },
  [sym_generic_define] = {
    .visible = true,
    .named = true,
  },
  [sym_attribute] = {
    .visible = true,
    .named = true,
  },
  [sym_attribute_name] = {
    .visible = true,
    .named = true,
  },
  [sym_attribute_value] = {
    .visible = true,
    .named = true,
  },
  [sym_number_list] = {
    .visible = true,
    .named = true,
  },
  [sym_group_name] = {
    .visible = true,
    .named = true,
  },
  [sym_resource_type] = {
    .visible = true,
    .named = true,
  },
  [sym_resource_name] = {
    .visible = true,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [sym_yes_no] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_source_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_define_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_number_list_repeat1] = {
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
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 48,
  [49] = 49,
  [50] = 50,
  [51] = 51,
  [52] = 52,
  [53] = 53,
  [54] = 54,
  [55] = 55,
  [56] = 56,
  [57] = 57,
  [58] = 58,
  [59] = 59,
  [60] = 60,
  [61] = 61,
  [62] = 62,
  [63] = 63,
  [64] = 64,
  [65] = 65,
  [66] = 66,
  [67] = 67,
  [68] = 68,
  [69] = 69,
  [70] = 70,
  [71] = 71,
  [72] = 72,
  [73] = 73,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(35);
      if (lookahead == '\n') SKIP(0);
      if (lookahead == '\r') SKIP(30);
      if (lookahead == '(') ADVANCE(40);
      if (lookahead == ')') ADVANCE(41);
      if (lookahead == ',') ADVANCE(131);
      if (lookahead == '/') ADVANCE(10);
      if (lookahead == 'C') ADVANCE(98);
      if (lookahead == 'D') ADVANCE(65);
      if (lookahead == 'F') ADVANCE(79);
      if (lookahead == 'G') ADVANCE(111);
      if (lookahead == 'M') ADVANCE(56);
      if (lookahead == 'N') ADVANCE(99);
      if (lookahead == 'P') ADVANCE(113);
      if (lookahead == 'S') ADVANCE(66);
      if (lookahead == 'T') ADVANCE(63);
      if (lookahead == 'Y') ADVANCE(73);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(137);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 1:
      if (lookahead == '\t') SKIP(1);
      if (lookahead == '\n') SKIP(1);
      if (lookahead == '\r') SKIP(8);
      if (lookahead == ' ') ADVANCE(132);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_') ADVANCE(133);
      END_STATE();
    case 2:
      if (lookahead == '\n') SKIP(3);
      END_STATE();
    case 3:
      if (lookahead == '\n') SKIP(3);
      if (lookahead == '\r') SKIP(2);
      if (lookahead == 'C') ADVANCE(98);
      if (lookahead == 'F') ADVANCE(79);
      if (lookahead == 'M') ADVANCE(56);
      if (lookahead == 'P') ADVANCE(113);
      if (lookahead == 'S') ADVANCE(66);
      if (lookahead == 'T') ADVANCE(63);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(3);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 4:
      if (lookahead == '\n') SKIP(5);
      END_STATE();
    case 5:
      if (lookahead == '\n') SKIP(5);
      if (lookahead == '\r') SKIP(4);
      if (lookahead == 'N') ADVANCE(53);
      if (lookahead == 'Y') ADVANCE(52);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(5);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(137);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 6:
      if (lookahead == '\n') SKIP(7);
      END_STATE();
    case 7:
      if (lookahead == '\n') SKIP(7);
      if (lookahead == '\r') SKIP(6);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(7);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 8:
      if (lookahead == '\n') SKIP(1);
      END_STATE();
    case 9:
      if (lookahead == ' ') ADVANCE(25);
      END_STATE();
    case 10:
      if (lookahead == '*') ADVANCE(36);
      END_STATE();
    case 11:
      if (lookahead == '/') ADVANCE(24);
      END_STATE();
    case 12:
      if (lookahead == ':') ADVANCE(26);
      END_STATE();
    case 13:
      if (lookahead == ':') ADVANCE(28);
      END_STATE();
    case 14:
      if (lookahead == 'E') ADVANCE(16);
      END_STATE();
    case 15:
      if (lookahead == 'E') ADVANCE(37);
      END_STATE();
    case 16:
      if (lookahead == 'F') ADVANCE(17);
      END_STATE();
    case 17:
      if (lookahead == 'I') ADVANCE(18);
      END_STATE();
    case 18:
      if (lookahead == 'N') ADVANCE(15);
      END_STATE();
    case 19:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      END_STATE();
    case 20:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(9);
      END_STATE();
    case 21:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(13);
      END_STATE();
    case 22:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(135);
      END_STATE();
    case 23:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      END_STATE();
    case 24:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(20);
      END_STATE();
    case 25:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(21);
      END_STATE();
    case 26:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(22);
      END_STATE();
    case 27:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(12);
      END_STATE();
    case 28:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(27);
      END_STATE();
    case 29:
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(134);
      END_STATE();
    case 30:
      if (eof) ADVANCE(35);
      if (lookahead == '\n') SKIP(0);
      END_STATE();
    case 31:
      if (eof) ADVANCE(35);
      if (lookahead == '\n') SKIP(32);
      END_STATE();
    case 32:
      if (eof) ADVANCE(35);
      if (lookahead == '\n') SKIP(32);
      if (lookahead == '\r') SKIP(31);
      if (lookahead == '/') ADVANCE(10);
      if (lookahead == 'D') ADVANCE(14);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(32);
      END_STATE();
    case 33:
      if (eof) ADVANCE(35);
      if (lookahead == '\n') SKIP(34);
      END_STATE();
    case 34:
      if (eof) ADVANCE(35);
      if (lookahead == '\n') SKIP(34);
      if (lookahead == '\r') SKIP(33);
      if (lookahead == '(') ADVANCE(40);
      if (lookahead == '/') ADVANCE(10);
      if (lookahead == 'D') ADVANCE(65);
      if (lookahead == 'G') ADVANCE(111);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(34);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '*') ADVANCE(36);
      if (lookahead == '/') ADVANCE(36);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(36);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(anon_sym_DEFINE);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(anon_sym_DEFINE);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(anon_sym_FILE);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(anon_sym_MAPSET);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(anon_sym_PROGRAM);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(anon_sym_TRANSACTION);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(anon_sym_TDQUEUE);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(anon_sym_TSQUEUE);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(anon_sym_TSMODEL);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(anon_sym_CONNECTION);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(anon_sym_SESSIONS);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(anon_sym_DESCRIPTION);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(anon_sym_GROUP);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == '.') ADVANCE(29);
      if (lookahead == 'E') ADVANCE(54);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == '.') ADVANCE(29);
      if (lookahead == 'O') ADVANCE(141);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == '.') ADVANCE(29);
      if (lookahead == 'S') ADVANCE(139);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == '.') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'A') ADVANCE(108);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'A') ADVANCE(88);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'A') ADVANCE(95);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'A') ADVANCE(62);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'C') ADVANCE(114);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'C') ADVANCE(122);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'C') ADVANCE(124);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'D') ADVANCE(110);
      if (lookahead == 'R') ADVANCE(58);
      if (lookahead == 'S') ADVANCE(89);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'D') ADVANCE(72);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(77);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(119);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(39);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(121);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(38);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(45);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(46);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(86);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(115);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(61);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(127);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'E') ADVANCE(128);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'F') ADVANCE(82);
      if (lookahead == 'S') ADVANCE(60);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'G') ADVANCE(112);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(87);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(109);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(106);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(97);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(103);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(104);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'I') ADVANCE(105);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'L') ADVANCE(47);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'L') ADVANCE(67);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'M') ADVANCE(43);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'M') ADVANCE(102);
      if (lookahead == 'Q') ADVANCE(129);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(48);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(50);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(94);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(74);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(118);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(116);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'N') ADVANCE(69);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(93);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(142);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(125);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(78);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(64);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(90);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(91);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(92);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 106:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'O') ADVANCE(96);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 107:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'P') ADVANCE(51);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 108:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'P') ADVANCE(120);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 109:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'P') ADVANCE(123);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 110:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'Q') ADVANCE(126);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 111:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'R') ADVANCE(100);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 112:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'R') ADVANCE(57);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 113:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'R') ADVANCE(101);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 114:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'R') ADVANCE(80);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 115:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'S') ADVANCE(140);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 116:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'S') ADVANCE(49);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 117:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'S') ADVANCE(81);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 118:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'S') ADVANCE(59);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 119:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'S') ADVANCE(117);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 120:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'S') ADVANCE(68);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 121:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'T') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 122:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'T') ADVANCE(83);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 123:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'T') ADVANCE(84);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 124:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'T') ADVANCE(85);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 125:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'U') ADVANCE(107);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 126:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'U') ADVANCE(75);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 127:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'U') ADVANCE(70);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 128:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'U') ADVANCE(71);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 129:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (lookahead == 'U') ADVANCE(76);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 130:
      ACCEPT_TOKEN(aux_sym_attribute_name_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 131:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 132:
      ACCEPT_TOKEN(sym_description_text);
      if (lookahead == ' ') ADVANCE(132);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_') ADVANCE(133);
      END_STATE();
    case 133:
      ACCEPT_TOKEN(sym_description_text);
      if (lookahead == ' ' ||
          lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_') ADVANCE(133);
      END_STATE();
    case 134:
      ACCEPT_TOKEN(sym_dataset_name);
      if (lookahead == '.') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(134);
      END_STATE();
    case 135:
      ACCEPT_TOKEN(sym_datetime);
      END_STATE();
    case 136:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '/') ADVANCE(23);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(138);
      END_STATE();
    case 137:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(136);
      END_STATE();
    case 138:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(138);
      END_STATE();
    case 139:
      ACCEPT_TOKEN(anon_sym_YES);
      if (lookahead == '.') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 140:
      ACCEPT_TOKEN(anon_sym_YES);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    case 141:
      ACCEPT_TOKEN(anon_sym_NO);
      if (lookahead == '.') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(55);
      END_STATE();
    case 142:
      ACCEPT_TOKEN(anon_sym_NO);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z')) ADVANCE(130);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 32},
  [2] = {.lex_state = 32},
  [3] = {.lex_state = 32},
  [4] = {.lex_state = 3},
  [5] = {.lex_state = 34},
  [6] = {.lex_state = 5},
  [7] = {.lex_state = 34},
  [8] = {.lex_state = 34},
  [9] = {.lex_state = 34},
  [10] = {.lex_state = 34},
  [11] = {.lex_state = 34},
  [12] = {.lex_state = 34},
  [13] = {.lex_state = 34},
  [14] = {.lex_state = 34},
  [15] = {.lex_state = 34},
  [16] = {.lex_state = 34},
  [17] = {.lex_state = 34},
  [18] = {.lex_state = 34},
  [19] = {.lex_state = 34},
  [20] = {.lex_state = 34},
  [21] = {.lex_state = 34},
  [22] = {.lex_state = 34},
  [23] = {.lex_state = 34},
  [24] = {.lex_state = 34},
  [25] = {.lex_state = 34},
  [26] = {.lex_state = 34},
  [27] = {.lex_state = 34},
  [28] = {.lex_state = 34},
  [29] = {.lex_state = 34},
  [30] = {.lex_state = 34},
  [31] = {.lex_state = 32},
  [32] = {.lex_state = 0},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 0},
  [35] = {.lex_state = 7},
  [36] = {.lex_state = 7},
  [37] = {.lex_state = 7},
  [38] = {.lex_state = 7},
  [39] = {.lex_state = 7},
  [40] = {.lex_state = 7},
  [41] = {.lex_state = 7},
  [42] = {.lex_state = 7},
  [43] = {.lex_state = 7},
  [44] = {.lex_state = 7},
  [45] = {.lex_state = 0},
  [46] = {.lex_state = 0},
  [47] = {.lex_state = 0},
  [48] = {.lex_state = 0},
  [49] = {.lex_state = 0},
  [50] = {.lex_state = 0},
  [51] = {.lex_state = 0},
  [52] = {.lex_state = 0},
  [53] = {.lex_state = 0},
  [54] = {.lex_state = 0},
  [55] = {.lex_state = 0},
  [56] = {.lex_state = 0},
  [57] = {.lex_state = 0},
  [58] = {.lex_state = 0},
  [59] = {.lex_state = 0},
  [60] = {.lex_state = 1},
  [61] = {.lex_state = 0},
  [62] = {.lex_state = 0},
  [63] = {.lex_state = 0},
  [64] = {.lex_state = 0},
  [65] = {.lex_state = 0},
  [66] = {.lex_state = 0},
  [67] = {.lex_state = 0},
  [68] = {.lex_state = 0},
  [69] = {.lex_state = 0},
  [70] = {.lex_state = 0},
  [71] = {.lex_state = 0},
  [72] = {.lex_state = 0},
  [73] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_comment] = ACTIONS(1),
    [anon_sym_DEFINE] = ACTIONS(1),
    [anon_sym_FILE] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_MAPSET] = ACTIONS(1),
    [anon_sym_PROGRAM] = ACTIONS(1),
    [anon_sym_TRANSACTION] = ACTIONS(1),
    [anon_sym_TDQUEUE] = ACTIONS(1),
    [anon_sym_TSQUEUE] = ACTIONS(1),
    [anon_sym_TSMODEL] = ACTIONS(1),
    [anon_sym_CONNECTION] = ACTIONS(1),
    [anon_sym_SESSIONS] = ACTIONS(1),
    [anon_sym_DESCRIPTION] = ACTIONS(1),
    [anon_sym_GROUP] = ACTIONS(1),
    [aux_sym_attribute_name_token1] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [sym_datetime] = ACTIONS(1),
    [sym_number] = ACTIONS(1),
    [anon_sym_YES] = ACTIONS(1),
    [anon_sym_NO] = ACTIONS(1),
  },
  [1] = {
    [sym_source_file] = STATE(72),
    [sym_definition] = STATE(3),
    [sym_define_file] = STATE(31),
    [sym_define_mapset] = STATE(31),
    [sym_define_program] = STATE(31),
    [sym_define_transaction] = STATE(31),
    [sym_define_tdqueue] = STATE(31),
    [sym_define_tsqueue] = STATE(31),
    [sym_define_connection] = STATE(31),
    [sym_define_sessions] = STATE(31),
    [sym_generic_define] = STATE(31),
    [aux_sym_source_file_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(3),
    [sym_comment] = ACTIONS(5),
    [anon_sym_DEFINE] = ACTIONS(7),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 5,
    ACTIONS(9), 1,
      ts_builtin_sym_end,
    ACTIONS(11), 1,
      sym_comment,
    ACTIONS(14), 1,
      anon_sym_DEFINE,
    STATE(2), 2,
      sym_definition,
      aux_sym_source_file_repeat1,
    STATE(31), 9,
      sym_define_file,
      sym_define_mapset,
      sym_define_program,
      sym_define_transaction,
      sym_define_tdqueue,
      sym_define_tsqueue,
      sym_define_connection,
      sym_define_sessions,
      sym_generic_define,
  [25] = 5,
    ACTIONS(7), 1,
      anon_sym_DEFINE,
    ACTIONS(17), 1,
      ts_builtin_sym_end,
    ACTIONS(19), 1,
      sym_comment,
    STATE(2), 2,
      sym_definition,
      aux_sym_source_file_repeat1,
    STATE(31), 9,
      sym_define_file,
      sym_define_mapset,
      sym_define_program,
      sym_define_transaction,
      sym_define_tdqueue,
      sym_define_tsqueue,
      sym_define_connection,
      sym_define_sessions,
      sym_generic_define,
  [50] = 10,
    ACTIONS(21), 1,
      anon_sym_FILE,
    ACTIONS(23), 1,
      anon_sym_MAPSET,
    ACTIONS(25), 1,
      anon_sym_PROGRAM,
    ACTIONS(27), 1,
      anon_sym_TRANSACTION,
    ACTIONS(29), 1,
      anon_sym_TDQUEUE,
    ACTIONS(33), 1,
      anon_sym_CONNECTION,
    ACTIONS(35), 1,
      anon_sym_SESSIONS,
    ACTIONS(37), 1,
      aux_sym_attribute_name_token1,
    STATE(5), 1,
      sym_resource_type,
    ACTIONS(31), 2,
      anon_sym_TSQUEUE,
      anon_sym_TSMODEL,
  [82] = 8,
    ACTIONS(41), 1,
      anon_sym_DEFINE,
    ACTIONS(43), 1,
      anon_sym_LPAREN,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(39), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(8), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [109] = 7,
    ACTIONS(51), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(53), 1,
      sym_dataset_name,
    ACTIONS(55), 1,
      sym_datetime,
    ACTIONS(57), 1,
      sym_number,
    STATE(54), 1,
      sym_attribute_value,
    ACTIONS(59), 2,
      anon_sym_YES,
      anon_sym_NO,
    STATE(57), 3,
      sym_number_list,
      sym_identifier,
      sym_yes_no,
  [134] = 7,
    ACTIONS(63), 1,
      anon_sym_DEFINE,
    ACTIONS(65), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(68), 1,
      anon_sym_GROUP,
    ACTIONS(71), 1,
      aux_sym_attribute_name_token1,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(61), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [158] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(76), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(74), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [182] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(80), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(78), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(18), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [206] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(84), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(82), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(19), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [230] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(88), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(86), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(20), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [254] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(92), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(90), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(21), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [278] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(96), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(94), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(22), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [302] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(100), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(98), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(23), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [326] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(104), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(102), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(24), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [350] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(108), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(106), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(25), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [374] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(112), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(110), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(26), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [398] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(116), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(114), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [422] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(120), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(118), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [446] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(124), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(122), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [470] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(128), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(126), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [494] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(132), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(130), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [518] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(136), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(134), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [542] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(140), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(138), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [566] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(144), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(142), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [590] = 7,
    ACTIONS(45), 1,
      anon_sym_DESCRIPTION,
    ACTIONS(47), 1,
      anon_sym_GROUP,
    ACTIONS(49), 1,
      aux_sym_attribute_name_token1,
    ACTIONS(148), 1,
      anon_sym_DEFINE,
    STATE(28), 1,
      sym_attribute_name,
    ACTIONS(146), 2,
      ts_builtin_sym_end,
      sym_comment,
    STATE(7), 2,
      sym_attribute,
      aux_sym_define_file_repeat1,
  [614] = 2,
    ACTIONS(150), 3,
      ts_builtin_sym_end,
      sym_comment,
      anon_sym_LPAREN,
    ACTIONS(152), 4,
      anon_sym_DEFINE,
      anon_sym_DESCRIPTION,
      anon_sym_GROUP,
      aux_sym_attribute_name_token1,
  [626] = 3,
    ACTIONS(158), 1,
      anon_sym_LPAREN,
    ACTIONS(154), 2,
      ts_builtin_sym_end,
      sym_comment,
    ACTIONS(156), 4,
      anon_sym_DEFINE,
      anon_sym_DESCRIPTION,
      anon_sym_GROUP,
      aux_sym_attribute_name_token1,
  [640] = 2,
    ACTIONS(160), 3,
      ts_builtin_sym_end,
      sym_comment,
      anon_sym_LPAREN,
    ACTIONS(162), 4,
      anon_sym_DEFINE,
      anon_sym_DESCRIPTION,
      anon_sym_GROUP,
      aux_sym_attribute_name_token1,
  [652] = 2,
    ACTIONS(164), 2,
      ts_builtin_sym_end,
      sym_comment,
    ACTIONS(166), 4,
      anon_sym_DEFINE,
      anon_sym_DESCRIPTION,
      anon_sym_GROUP,
      aux_sym_attribute_name_token1,
  [663] = 1,
    ACTIONS(168), 3,
      ts_builtin_sym_end,
      sym_comment,
      anon_sym_DEFINE,
  [669] = 3,
    ACTIONS(170), 1,
      anon_sym_RPAREN,
    ACTIONS(172), 1,
      anon_sym_COMMA,
    STATE(32), 1,
      aux_sym_number_list_repeat1,
  [679] = 3,
    ACTIONS(175), 1,
      anon_sym_RPAREN,
    ACTIONS(177), 1,
      anon_sym_COMMA,
    STATE(34), 1,
      aux_sym_number_list_repeat1,
  [689] = 3,
    ACTIONS(177), 1,
      anon_sym_COMMA,
    ACTIONS(179), 1,
      anon_sym_RPAREN,
    STATE(32), 1,
      aux_sym_number_list_repeat1,
  [699] = 2,
    ACTIONS(181), 1,
      aux_sym_attribute_name_token1,
    STATE(54), 1,
      sym_group_name,
  [706] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(61), 1,
      sym_resource_name,
  [713] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(49), 1,
      sym_resource_name,
  [720] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(50), 1,
      sym_resource_name,
  [727] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(47), 1,
      sym_resource_name,
  [734] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(67), 1,
      sym_resource_name,
  [741] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(52), 1,
      sym_resource_name,
  [748] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(53), 1,
      sym_resource_name,
  [755] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(51), 1,
      sym_resource_name,
  [762] = 2,
    ACTIONS(183), 1,
      aux_sym_attribute_name_token1,
    STATE(58), 1,
      sym_resource_name,
  [769] = 1,
    ACTIONS(170), 2,
      anon_sym_RPAREN,
      anon_sym_COMMA,
  [774] = 1,
    ACTIONS(185), 1,
      anon_sym_LPAREN,
  [778] = 1,
    ACTIONS(187), 1,
      anon_sym_RPAREN,
  [782] = 1,
    ACTIONS(189), 1,
      anon_sym_LPAREN,
  [786] = 1,
    ACTIONS(191), 1,
      anon_sym_RPAREN,
  [790] = 1,
    ACTIONS(193), 1,
      anon_sym_RPAREN,
  [794] = 1,
    ACTIONS(195), 1,
      anon_sym_RPAREN,
  [798] = 1,
    ACTIONS(197), 1,
      anon_sym_RPAREN,
  [802] = 1,
    ACTIONS(199), 1,
      anon_sym_RPAREN,
  [806] = 1,
    ACTIONS(201), 1,
      anon_sym_RPAREN,
  [810] = 1,
    ACTIONS(203), 1,
      anon_sym_RPAREN,
  [814] = 1,
    ACTIONS(205), 1,
      anon_sym_RPAREN,
  [818] = 1,
    ACTIONS(175), 1,
      anon_sym_RPAREN,
  [822] = 1,
    ACTIONS(207), 1,
      anon_sym_RPAREN,
  [826] = 1,
    ACTIONS(209), 1,
      anon_sym_RPAREN,
  [830] = 1,
    ACTIONS(211), 1,
      sym_description_text,
  [834] = 1,
    ACTIONS(213), 1,
      anon_sym_RPAREN,
  [838] = 1,
    ACTIONS(215), 1,
      anon_sym_LPAREN,
  [842] = 1,
    ACTIONS(217), 1,
      anon_sym_LPAREN,
  [846] = 1,
    ACTIONS(219), 1,
      anon_sym_LPAREN,
  [850] = 1,
    ACTIONS(221), 1,
      anon_sym_LPAREN,
  [854] = 1,
    ACTIONS(223), 1,
      anon_sym_LPAREN,
  [858] = 1,
    ACTIONS(225), 1,
      anon_sym_RPAREN,
  [862] = 1,
    ACTIONS(227), 1,
      anon_sym_LPAREN,
  [866] = 1,
    ACTIONS(229), 1,
      anon_sym_RPAREN,
  [870] = 1,
    ACTIONS(231), 1,
      sym_number,
  [874] = 1,
    ACTIONS(233), 1,
      anon_sym_LPAREN,
  [878] = 1,
    ACTIONS(235), 1,
      ts_builtin_sym_end,
  [882] = 1,
    ACTIONS(237), 1,
      anon_sym_LPAREN,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 25,
  [SMALL_STATE(4)] = 50,
  [SMALL_STATE(5)] = 82,
  [SMALL_STATE(6)] = 109,
  [SMALL_STATE(7)] = 134,
  [SMALL_STATE(8)] = 158,
  [SMALL_STATE(9)] = 182,
  [SMALL_STATE(10)] = 206,
  [SMALL_STATE(11)] = 230,
  [SMALL_STATE(12)] = 254,
  [SMALL_STATE(13)] = 278,
  [SMALL_STATE(14)] = 302,
  [SMALL_STATE(15)] = 326,
  [SMALL_STATE(16)] = 350,
  [SMALL_STATE(17)] = 374,
  [SMALL_STATE(18)] = 398,
  [SMALL_STATE(19)] = 422,
  [SMALL_STATE(20)] = 446,
  [SMALL_STATE(21)] = 470,
  [SMALL_STATE(22)] = 494,
  [SMALL_STATE(23)] = 518,
  [SMALL_STATE(24)] = 542,
  [SMALL_STATE(25)] = 566,
  [SMALL_STATE(26)] = 590,
  [SMALL_STATE(27)] = 614,
  [SMALL_STATE(28)] = 626,
  [SMALL_STATE(29)] = 640,
  [SMALL_STATE(30)] = 652,
  [SMALL_STATE(31)] = 663,
  [SMALL_STATE(32)] = 669,
  [SMALL_STATE(33)] = 679,
  [SMALL_STATE(34)] = 689,
  [SMALL_STATE(35)] = 699,
  [SMALL_STATE(36)] = 706,
  [SMALL_STATE(37)] = 713,
  [SMALL_STATE(38)] = 720,
  [SMALL_STATE(39)] = 727,
  [SMALL_STATE(40)] = 734,
  [SMALL_STATE(41)] = 741,
  [SMALL_STATE(42)] = 748,
  [SMALL_STATE(43)] = 755,
  [SMALL_STATE(44)] = 762,
  [SMALL_STATE(45)] = 769,
  [SMALL_STATE(46)] = 774,
  [SMALL_STATE(47)] = 778,
  [SMALL_STATE(48)] = 782,
  [SMALL_STATE(49)] = 786,
  [SMALL_STATE(50)] = 790,
  [SMALL_STATE(51)] = 794,
  [SMALL_STATE(52)] = 798,
  [SMALL_STATE(53)] = 802,
  [SMALL_STATE(54)] = 806,
  [SMALL_STATE(55)] = 810,
  [SMALL_STATE(56)] = 814,
  [SMALL_STATE(57)] = 818,
  [SMALL_STATE(58)] = 822,
  [SMALL_STATE(59)] = 826,
  [SMALL_STATE(60)] = 830,
  [SMALL_STATE(61)] = 834,
  [SMALL_STATE(62)] = 838,
  [SMALL_STATE(63)] = 842,
  [SMALL_STATE(64)] = 846,
  [SMALL_STATE(65)] = 850,
  [SMALL_STATE(66)] = 854,
  [SMALL_STATE(67)] = 858,
  [SMALL_STATE(68)] = 862,
  [SMALL_STATE(69)] = 866,
  [SMALL_STATE(70)] = 870,
  [SMALL_STATE(71)] = 874,
  [SMALL_STATE(72)] = 878,
  [SMALL_STATE(73)] = 882,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [9] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [11] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(2),
  [14] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(4),
  [17] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [21] = {.entry = {.count = 1, .reusable = false}}, SHIFT(73),
  [23] = {.entry = {.count = 1, .reusable = false}}, SHIFT(48),
  [25] = {.entry = {.count = 1, .reusable = false}}, SHIFT(66),
  [27] = {.entry = {.count = 1, .reusable = false}}, SHIFT(46),
  [29] = {.entry = {.count = 1, .reusable = false}}, SHIFT(68),
  [31] = {.entry = {.count = 1, .reusable = false}}, SHIFT(62),
  [33] = {.entry = {.count = 1, .reusable = false}}, SHIFT(63),
  [35] = {.entry = {.count = 1, .reusable = false}}, SHIFT(71),
  [37] = {.entry = {.count = 1, .reusable = false}}, SHIFT(29),
  [39] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_generic_define, 2, 0, 0),
  [41] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_generic_define, 2, 0, 0),
  [43] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
  [45] = {.entry = {.count = 1, .reusable = false}}, SHIFT(64),
  [47] = {.entry = {.count = 1, .reusable = false}}, SHIFT(65),
  [49] = {.entry = {.count = 1, .reusable = false}}, SHIFT(27),
  [51] = {.entry = {.count = 1, .reusable = false}}, SHIFT(56),
  [53] = {.entry = {.count = 1, .reusable = false}}, SHIFT(57),
  [55] = {.entry = {.count = 1, .reusable = true}}, SHIFT(57),
  [57] = {.entry = {.count = 1, .reusable = false}}, SHIFT(33),
  [59] = {.entry = {.count = 1, .reusable = false}}, SHIFT(59),
  [61] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_define_file_repeat1, 2, 0, 0),
  [63] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_define_file_repeat1, 2, 0, 0),
  [65] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_define_file_repeat1, 2, 0, 0), SHIFT_REPEAT(64),
  [68] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_define_file_repeat1, 2, 0, 0), SHIFT_REPEAT(65),
  [71] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_define_file_repeat1, 2, 0, 0), SHIFT_REPEAT(27),
  [74] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_generic_define, 3, 0, 0),
  [76] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_generic_define, 3, 0, 0),
  [78] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_file, 5, 0, 0),
  [80] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_file, 5, 0, 0),
  [82] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_mapset, 5, 0, 0),
  [84] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_mapset, 5, 0, 0),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_program, 5, 0, 0),
  [88] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_program, 5, 0, 0),
  [90] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_transaction, 5, 0, 0),
  [92] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_transaction, 5, 0, 0),
  [94] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_tdqueue, 5, 0, 0),
  [96] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_tdqueue, 5, 0, 0),
  [98] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_tsqueue, 5, 0, 0),
  [100] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_tsqueue, 5, 0, 0),
  [102] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_connection, 5, 0, 0),
  [104] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_connection, 5, 0, 0),
  [106] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_sessions, 5, 0, 0),
  [108] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_sessions, 5, 0, 0),
  [110] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_generic_define, 5, 0, 0),
  [112] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_generic_define, 5, 0, 0),
  [114] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_file, 6, 0, 0),
  [116] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_file, 6, 0, 0),
  [118] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_mapset, 6, 0, 0),
  [120] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_mapset, 6, 0, 0),
  [122] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_program, 6, 0, 0),
  [124] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_program, 6, 0, 0),
  [126] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_transaction, 6, 0, 0),
  [128] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_transaction, 6, 0, 0),
  [130] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_tdqueue, 6, 0, 0),
  [132] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_tdqueue, 6, 0, 0),
  [134] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_tsqueue, 6, 0, 0),
  [136] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_tsqueue, 6, 0, 0),
  [138] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_connection, 6, 0, 0),
  [140] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_connection, 6, 0, 0),
  [142] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_define_sessions, 6, 0, 0),
  [144] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_define_sessions, 6, 0, 0),
  [146] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_generic_define, 6, 0, 0),
  [148] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_generic_define, 6, 0, 0),
  [150] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_attribute_name, 1, 0, 0),
  [152] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_attribute_name, 1, 0, 0),
  [154] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_attribute, 1, 0, 0),
  [156] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_attribute, 1, 0, 0),
  [158] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [160] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_resource_type, 1, 0, 0),
  [162] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_resource_type, 1, 0, 0),
  [164] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_attribute, 4, 0, 0),
  [166] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_attribute, 4, 0, 0),
  [168] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_definition, 1, 0, 0),
  [170] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_number_list_repeat1, 2, 0, 0),
  [172] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_number_list_repeat1, 2, 0, 0), SHIFT_REPEAT(70),
  [175] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_attribute_value, 1, 0, 0),
  [177] = {.entry = {.count = 1, .reusable = true}}, SHIFT(70),
  [179] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_number_list, 2, 0, 0),
  [181] = {.entry = {.count = 1, .reusable = true}}, SHIFT(55),
  [183] = {.entry = {.count = 1, .reusable = true}}, SHIFT(69),
  [185] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [187] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [189] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [191] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [193] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [195] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [197] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [199] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [201] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [203] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_group_name, 1, 0, 0),
  [205] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [207] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [209] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_yes_no, 1, 0, 0),
  [211] = {.entry = {.count = 1, .reusable = true}}, SHIFT(54),
  [213] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [215] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
  [217] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [219] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [221] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [223] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [225] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [227] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [229] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_resource_name, 1, 0, 0),
  [231] = {.entry = {.count = 1, .reusable = true}}, SHIFT(45),
  [233] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [235] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [237] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
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

TS_PUBLIC const TSLanguage *tree_sitter_csd(void) {
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
