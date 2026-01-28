#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#ifdef _MSC_VER
#pragma optimize("", off)
#elif defined(__clang__)
#pragma clang optimize off
#elif defined(__GNUC__)
#pragma GCC optimize ("O0")
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 35
#define LARGE_STATE_COUNT 25
#define SYMBOL_COUNT 231
#define ALIAS_COUNT 0
#define TOKEN_COUNT 214
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 4
#define PRODUCTION_ID_COUNT 1

enum ts_symbol_identifiers {
  aux_sym_newline_token1 = 1,
  aux_sym_comment_line_token1 = 2,
  sym_sequence_number = 3,
  anon_sym_DOT = 4,
  anon_sym_88 = 5,
  anon_sym_VALUE = 6,
  anon_sym_IS = 7,
  anon_sym_ARE = 8,
  aux_sym_level_number_token1 = 9,
  aux_sym_level_number_token2 = 10,
  anon_sym_66 = 11,
  anon_sym_77 = 12,
  anon_sym_FILLER = 13,
  anon_sym_PIC = 14,
  anon_sym_PICTURE = 15,
  anon_sym_VALUES = 16,
  anon_sym_OCCURS = 17,
  anon_sym_TIMES = 18,
  anon_sym_TO = 19,
  anon_sym_REDEFINES = 20,
  anon_sym_INDEXED = 21,
  anon_sym_BY = 22,
  anon_sym_DEPENDING = 23,
  anon_sym_ON = 24,
  anon_sym_USAGE = 25,
  anon_sym_DISPLAY = 26,
  anon_sym_DISPLAY_DASH1 = 27,
  anon_sym_BINARY = 28,
  anon_sym_COMP = 29,
  anon_sym_COMP_DASH1 = 30,
  anon_sym_COMP_DASH2 = 31,
  anon_sym_COMP_DASH3 = 32,
  anon_sym_COMP_DASH4 = 33,
  anon_sym_COMP_DASH5 = 34,
  anon_sym_COMPUTATIONAL = 35,
  anon_sym_COMPUTATIONAL_DASH1 = 36,
  anon_sym_COMPUTATIONAL_DASH2 = 37,
  anon_sym_COMPUTATIONAL_DASH3 = 38,
  anon_sym_COMPUTATIONAL_DASH4 = 39,
  anon_sym_COMPUTATIONAL_DASH5 = 40,
  anon_sym_PACKED_DASHDECIMAL = 41,
  anon_sym_INDEX = 42,
  anon_sym_POINTER = 43,
  anon_sym_ZERO = 44,
  anon_sym_ZEROS = 45,
  anon_sym_ZEROES = 46,
  anon_sym_SPACE = 47,
  anon_sym_SPACES = 48,
  anon_sym_HIGH_DASHVALUE = 49,
  anon_sym_HIGH_DASHVALUES = 50,
  anon_sym_LOW_DASHVALUE = 51,
  anon_sym_LOW_DASHVALUES = 52,
  anon_sym_QUOTE = 53,
  anon_sym_QUOTES = 54,
  anon_sym_NULL = 55,
  anon_sym_NULLS = 56,
  anon_sym_ALL = 57,
  anon_sym_THRU = 58,
  anon_sym_THROUGH = 59,
  anon_sym_ASCENDING = 60,
  anon_sym_DESCENDING = 61,
  anon_sym_KEY = 62,
  anon_sym_SIGN = 63,
  anon_sym_LEADING = 64,
  anon_sym_TRAILING = 65,
  anon_sym_SEPARATE = 66,
  anon_sym_CHARACTER = 67,
  anon_sym_SYNC = 68,
  anon_sym_SYNCHRONIZED = 69,
  anon_sym_LEFT = 70,
  anon_sym_RIGHT = 71,
  anon_sym_JUST = 72,
  anon_sym_JUSTIFIED = 73,
  anon_sym_BLANK = 74,
  anon_sym_WHEN = 75,
  anon_sym_EXTERNAL = 76,
  anon_sym_GLOBAL = 77,
  anon_sym_AS = 78,
  anon_sym_COPY = 79,
  anon_sym_REPLACING = 80,
  anon_sym_OF = 81,
  anon_sym_IN = 82,
  anon_sym_REPLACE = 83,
  anon_sym_OFF = 84,
  anon_sym_EJECT = 85,
  anon_sym_SKIP1 = 86,
  anon_sym_SKIP2 = 87,
  anon_sym_SKIP3 = 88,
  anon_sym_EXEC = 89,
  anon_sym_EXECUTE = 90,
  anon_sym_SQL = 91,
  anon_sym_SQLIMS = 92,
  anon_sym_DLI = 93,
  anon_sym_END_DASHEXEC = 94,
  anon_sym_IF = 95,
  anon_sym_ELSE = 96,
  anon_sym_END_DASHIF = 97,
  anon_sym_THEN = 98,
  anon_sym_EVALUATE = 99,
  anon_sym_END_DASHEVALUATE = 100,
  anon_sym_OTHER = 101,
  anon_sym_ALSO = 102,
  anon_sym_PERFORM = 103,
  anon_sym_END_DASHPERFORM = 104,
  anon_sym_UNTIL = 105,
  anon_sym_VARYING = 106,
  anon_sym_WITH = 107,
  anon_sym_TEST = 108,
  anon_sym_BEFORE = 109,
  anon_sym_AFTER = 110,
  anon_sym_GO = 111,
  anon_sym_SECTION = 112,
  anon_sym_PARAGRAPH = 113,
  anon_sym_CONTINUE = 114,
  anon_sym_NEXT = 115,
  anon_sym_SENTENCE = 116,
  anon_sym_EXIT = 117,
  anon_sym_STOP = 118,
  anon_sym_RUN = 119,
  anon_sym_MOVE = 120,
  anon_sym_CORRESPONDING = 121,
  anon_sym_CORR = 122,
  anon_sym_INTO = 123,
  anon_sym_SET = 124,
  anon_sym_TRUE = 125,
  anon_sym_FALSE = 126,
  anon_sym_INITIALIZE = 127,
  anon_sym_ALPHABETIC = 128,
  anon_sym_ALPHANUMERIC = 129,
  anon_sym_ALPHANUMERIC_DASHEDITED = 130,
  anon_sym_NUMERIC = 131,
  anon_sym_NUMERIC_DASHEDITED = 132,
  anon_sym_COMPUTE = 133,
  anon_sym_ADD = 134,
  anon_sym_SUBTRACT = 135,
  anon_sym_MULTIPLY = 136,
  anon_sym_DIVIDE = 137,
  anon_sym_GIVING = 138,
  anon_sym_REMAINDER = 139,
  anon_sym_STRING = 140,
  anon_sym_DELIMITED = 141,
  anon_sym_SIZE = 142,
  anon_sym_OVERFLOW = 143,
  anon_sym_NOT = 144,
  anon_sym_END_DASHSTRING = 145,
  anon_sym_UNSTRING = 146,
  anon_sym_COUNT = 147,
  anon_sym_DELIMITER = 148,
  anon_sym_TALLYING = 149,
  anon_sym_END_DASHUNSTRING = 150,
  anon_sym_INSPECT = 151,
  anon_sym_CONVERTING = 152,
  anon_sym_FIRST = 153,
  anon_sym_INITIAL = 154,
  anon_sym_READ = 155,
  anon_sym_WRITE = 156,
  anon_sym_REWRITE = 157,
  anon_sym_DELETE = 158,
  anon_sym_START = 159,
  anon_sym_OPEN = 160,
  anon_sym_CLOSE = 161,
  anon_sym_INPUT = 162,
  anon_sym_OUTPUT = 163,
  anon_sym_I_DASHO = 164,
  anon_sym_EXTEND = 165,
  anon_sym_ACCEPT = 166,
  anon_sym_FROM = 167,
  anon_sym_DATE = 168,
  anon_sym_DAY = 169,
  anon_sym_TIME = 170,
  anon_sym_DAY_DASHOF_DASHWEEK = 171,
  anon_sym_EQUAL = 172,
  anon_sym_GREATER = 173,
  anon_sym_LESS = 174,
  anon_sym_THAN = 175,
  anon_sym_OR = 176,
  anon_sym_AND = 177,
  anon_sym_DFHENTER = 178,
  anon_sym_DFHCLEAR = 179,
  anon_sym_DFHPA1 = 180,
  anon_sym_DFHPA2 = 181,
  anon_sym_DFHPF1 = 182,
  anon_sym_DFHPF2 = 183,
  anon_sym_DFHPF3 = 184,
  anon_sym_DFHPF4 = 185,
  anon_sym_DFHPF5 = 186,
  anon_sym_DFHPF6 = 187,
  anon_sym_DFHPF7 = 188,
  anon_sym_DFHPF8 = 189,
  anon_sym_DFHPF9 = 190,
  anon_sym_DFHPF10 = 191,
  anon_sym_DFHPF11 = 192,
  anon_sym_DFHPF12 = 193,
  anon_sym_EIBAID = 194,
  anon_sym_DFHRED = 195,
  anon_sym_DFHBMASB = 196,
  anon_sym_DFHBMASK = 197,
  aux_sym_identifier_token1 = 198,
  aux_sym_identifier_token2 = 199,
  sym_picture_string = 200,
  aux_sym_string_literal_token1 = 201,
  aux_sym_string_literal_token2 = 202,
  sym_number = 203,
  anon_sym_EQ_EQ = 204,
  anon_sym_EQ = 205,
  anon_sym_GT = 206,
  anon_sym_LT = 207,
  anon_sym_GT_EQ = 208,
  anon_sym_LT_EQ = 209,
  anon_sym_COMMA = 210,
  anon_sym_LPAREN = 211,
  anon_sym_RPAREN = 212,
  anon_sym_COLON = 213,
  sym_source_file = 214,
  sym_newline = 215,
  sym_comment_line = 216,
  sym_statement = 217,
  sym_statement_body = 218,
  sym_embedded_comment = 219,
  sym_continuation_newline = 220,
  sym_level_88_condition = 221,
  sym_level_number = 222,
  sym_keyword = 223,
  sym_identifier = 224,
  sym_string_literal = 225,
  sym_operator = 226,
  sym_parenthesized = 227,
  aux_sym_source_file_repeat1 = 228,
  aux_sym_statement_body_repeat1 = 229,
  aux_sym_parenthesized_repeat1 = 230,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [aux_sym_newline_token1] = "newline_token1",
  [aux_sym_comment_line_token1] = "comment_line_token1",
  [sym_sequence_number] = "sequence_number",
  [anon_sym_DOT] = ".",
  [anon_sym_88] = "88",
  [anon_sym_VALUE] = "VALUE",
  [anon_sym_IS] = "IS",
  [anon_sym_ARE] = "ARE",
  [aux_sym_level_number_token1] = "level_number_token1",
  [aux_sym_level_number_token2] = "level_number_token2",
  [anon_sym_66] = "66",
  [anon_sym_77] = "77",
  [anon_sym_FILLER] = "FILLER",
  [anon_sym_PIC] = "PIC",
  [anon_sym_PICTURE] = "PICTURE",
  [anon_sym_VALUES] = "VALUES",
  [anon_sym_OCCURS] = "OCCURS",
  [anon_sym_TIMES] = "TIMES",
  [anon_sym_TO] = "TO",
  [anon_sym_REDEFINES] = "REDEFINES",
  [anon_sym_INDEXED] = "INDEXED",
  [anon_sym_BY] = "BY",
  [anon_sym_DEPENDING] = "DEPENDING",
  [anon_sym_ON] = "ON",
  [anon_sym_USAGE] = "USAGE",
  [anon_sym_DISPLAY] = "DISPLAY",
  [anon_sym_DISPLAY_DASH1] = "DISPLAY-1",
  [anon_sym_BINARY] = "BINARY",
  [anon_sym_COMP] = "COMP",
  [anon_sym_COMP_DASH1] = "COMP-1",
  [anon_sym_COMP_DASH2] = "COMP-2",
  [anon_sym_COMP_DASH3] = "COMP-3",
  [anon_sym_COMP_DASH4] = "COMP-4",
  [anon_sym_COMP_DASH5] = "COMP-5",
  [anon_sym_COMPUTATIONAL] = "COMPUTATIONAL",
  [anon_sym_COMPUTATIONAL_DASH1] = "COMPUTATIONAL-1",
  [anon_sym_COMPUTATIONAL_DASH2] = "COMPUTATIONAL-2",
  [anon_sym_COMPUTATIONAL_DASH3] = "COMPUTATIONAL-3",
  [anon_sym_COMPUTATIONAL_DASH4] = "COMPUTATIONAL-4",
  [anon_sym_COMPUTATIONAL_DASH5] = "COMPUTATIONAL-5",
  [anon_sym_PACKED_DASHDECIMAL] = "PACKED-DECIMAL",
  [anon_sym_INDEX] = "INDEX",
  [anon_sym_POINTER] = "POINTER",
  [anon_sym_ZERO] = "ZERO",
  [anon_sym_ZEROS] = "ZEROS",
  [anon_sym_ZEROES] = "ZEROES",
  [anon_sym_SPACE] = "SPACE",
  [anon_sym_SPACES] = "SPACES",
  [anon_sym_HIGH_DASHVALUE] = "HIGH-VALUE",
  [anon_sym_HIGH_DASHVALUES] = "HIGH-VALUES",
  [anon_sym_LOW_DASHVALUE] = "LOW-VALUE",
  [anon_sym_LOW_DASHVALUES] = "LOW-VALUES",
  [anon_sym_QUOTE] = "QUOTE",
  [anon_sym_QUOTES] = "QUOTES",
  [anon_sym_NULL] = "NULL",
  [anon_sym_NULLS] = "NULLS",
  [anon_sym_ALL] = "ALL",
  [anon_sym_THRU] = "THRU",
  [anon_sym_THROUGH] = "THROUGH",
  [anon_sym_ASCENDING] = "ASCENDING",
  [anon_sym_DESCENDING] = "DESCENDING",
  [anon_sym_KEY] = "KEY",
  [anon_sym_SIGN] = "SIGN",
  [anon_sym_LEADING] = "LEADING",
  [anon_sym_TRAILING] = "TRAILING",
  [anon_sym_SEPARATE] = "SEPARATE",
  [anon_sym_CHARACTER] = "CHARACTER",
  [anon_sym_SYNC] = "SYNC",
  [anon_sym_SYNCHRONIZED] = "SYNCHRONIZED",
  [anon_sym_LEFT] = "LEFT",
  [anon_sym_RIGHT] = "RIGHT",
  [anon_sym_JUST] = "JUST",
  [anon_sym_JUSTIFIED] = "JUSTIFIED",
  [anon_sym_BLANK] = "BLANK",
  [anon_sym_WHEN] = "WHEN",
  [anon_sym_EXTERNAL] = "EXTERNAL",
  [anon_sym_GLOBAL] = "GLOBAL",
  [anon_sym_AS] = "AS",
  [anon_sym_COPY] = "COPY",
  [anon_sym_REPLACING] = "REPLACING",
  [anon_sym_OF] = "OF",
  [anon_sym_IN] = "IN",
  [anon_sym_REPLACE] = "REPLACE",
  [anon_sym_OFF] = "OFF",
  [anon_sym_EJECT] = "EJECT",
  [anon_sym_SKIP1] = "SKIP1",
  [anon_sym_SKIP2] = "SKIP2",
  [anon_sym_SKIP3] = "SKIP3",
  [anon_sym_EXEC] = "EXEC",
  [anon_sym_EXECUTE] = "EXECUTE",
  [anon_sym_SQL] = "SQL",
  [anon_sym_SQLIMS] = "SQLIMS",
  [anon_sym_DLI] = "DLI",
  [anon_sym_END_DASHEXEC] = "END-EXEC",
  [anon_sym_IF] = "IF",
  [anon_sym_ELSE] = "ELSE",
  [anon_sym_END_DASHIF] = "END-IF",
  [anon_sym_THEN] = "THEN",
  [anon_sym_EVALUATE] = "EVALUATE",
  [anon_sym_END_DASHEVALUATE] = "END-EVALUATE",
  [anon_sym_OTHER] = "OTHER",
  [anon_sym_ALSO] = "ALSO",
  [anon_sym_PERFORM] = "PERFORM",
  [anon_sym_END_DASHPERFORM] = "END-PERFORM",
  [anon_sym_UNTIL] = "UNTIL",
  [anon_sym_VARYING] = "VARYING",
  [anon_sym_WITH] = "WITH",
  [anon_sym_TEST] = "TEST",
  [anon_sym_BEFORE] = "BEFORE",
  [anon_sym_AFTER] = "AFTER",
  [anon_sym_GO] = "GO",
  [anon_sym_SECTION] = "SECTION",
  [anon_sym_PARAGRAPH] = "PARAGRAPH",
  [anon_sym_CONTINUE] = "CONTINUE",
  [anon_sym_NEXT] = "NEXT",
  [anon_sym_SENTENCE] = "SENTENCE",
  [anon_sym_EXIT] = "EXIT",
  [anon_sym_STOP] = "STOP",
  [anon_sym_RUN] = "RUN",
  [anon_sym_MOVE] = "MOVE",
  [anon_sym_CORRESPONDING] = "CORRESPONDING",
  [anon_sym_CORR] = "CORR",
  [anon_sym_INTO] = "INTO",
  [anon_sym_SET] = "SET",
  [anon_sym_TRUE] = "TRUE",
  [anon_sym_FALSE] = "FALSE",
  [anon_sym_INITIALIZE] = "INITIALIZE",
  [anon_sym_ALPHABETIC] = "ALPHABETIC",
  [anon_sym_ALPHANUMERIC] = "ALPHANUMERIC",
  [anon_sym_ALPHANUMERIC_DASHEDITED] = "ALPHANUMERIC-EDITED",
  [anon_sym_NUMERIC] = "NUMERIC",
  [anon_sym_NUMERIC_DASHEDITED] = "NUMERIC-EDITED",
  [anon_sym_COMPUTE] = "COMPUTE",
  [anon_sym_ADD] = "ADD",
  [anon_sym_SUBTRACT] = "SUBTRACT",
  [anon_sym_MULTIPLY] = "MULTIPLY",
  [anon_sym_DIVIDE] = "DIVIDE",
  [anon_sym_GIVING] = "GIVING",
  [anon_sym_REMAINDER] = "REMAINDER",
  [anon_sym_STRING] = "STRING",
  [anon_sym_DELIMITED] = "DELIMITED",
  [anon_sym_SIZE] = "SIZE",
  [anon_sym_OVERFLOW] = "OVERFLOW",
  [anon_sym_NOT] = "NOT",
  [anon_sym_END_DASHSTRING] = "END-STRING",
  [anon_sym_UNSTRING] = "UNSTRING",
  [anon_sym_COUNT] = "COUNT",
  [anon_sym_DELIMITER] = "DELIMITER",
  [anon_sym_TALLYING] = "TALLYING",
  [anon_sym_END_DASHUNSTRING] = "END-UNSTRING",
  [anon_sym_INSPECT] = "INSPECT",
  [anon_sym_CONVERTING] = "CONVERTING",
  [anon_sym_FIRST] = "FIRST",
  [anon_sym_INITIAL] = "INITIAL",
  [anon_sym_READ] = "READ",
  [anon_sym_WRITE] = "WRITE",
  [anon_sym_REWRITE] = "REWRITE",
  [anon_sym_DELETE] = "DELETE",
  [anon_sym_START] = "START",
  [anon_sym_OPEN] = "OPEN",
  [anon_sym_CLOSE] = "CLOSE",
  [anon_sym_INPUT] = "INPUT",
  [anon_sym_OUTPUT] = "OUTPUT",
  [anon_sym_I_DASHO] = "I-O",
  [anon_sym_EXTEND] = "EXTEND",
  [anon_sym_ACCEPT] = "ACCEPT",
  [anon_sym_FROM] = "FROM",
  [anon_sym_DATE] = "DATE",
  [anon_sym_DAY] = "DAY",
  [anon_sym_TIME] = "TIME",
  [anon_sym_DAY_DASHOF_DASHWEEK] = "DAY-OF-WEEK",
  [anon_sym_EQUAL] = "EQUAL",
  [anon_sym_GREATER] = "GREATER",
  [anon_sym_LESS] = "LESS",
  [anon_sym_THAN] = "THAN",
  [anon_sym_OR] = "OR",
  [anon_sym_AND] = "AND",
  [anon_sym_DFHENTER] = "DFHENTER",
  [anon_sym_DFHCLEAR] = "DFHCLEAR",
  [anon_sym_DFHPA1] = "DFHPA1",
  [anon_sym_DFHPA2] = "DFHPA2",
  [anon_sym_DFHPF1] = "DFHPF1",
  [anon_sym_DFHPF2] = "DFHPF2",
  [anon_sym_DFHPF3] = "DFHPF3",
  [anon_sym_DFHPF4] = "DFHPF4",
  [anon_sym_DFHPF5] = "DFHPF5",
  [anon_sym_DFHPF6] = "DFHPF6",
  [anon_sym_DFHPF7] = "DFHPF7",
  [anon_sym_DFHPF8] = "DFHPF8",
  [anon_sym_DFHPF9] = "DFHPF9",
  [anon_sym_DFHPF10] = "DFHPF10",
  [anon_sym_DFHPF11] = "DFHPF11",
  [anon_sym_DFHPF12] = "DFHPF12",
  [anon_sym_EIBAID] = "EIBAID",
  [anon_sym_DFHRED] = "DFHRED",
  [anon_sym_DFHBMASB] = "DFHBMASB",
  [anon_sym_DFHBMASK] = "DFHBMASK",
  [aux_sym_identifier_token1] = "identifier_token1",
  [aux_sym_identifier_token2] = "identifier_token2",
  [sym_picture_string] = "picture_string",
  [aux_sym_string_literal_token1] = "string_literal_token1",
  [aux_sym_string_literal_token2] = "string_literal_token2",
  [sym_number] = "number",
  [anon_sym_EQ_EQ] = "==",
  [anon_sym_EQ] = "=",
  [anon_sym_GT] = ">",
  [anon_sym_LT] = "<",
  [anon_sym_GT_EQ] = ">=",
  [anon_sym_LT_EQ] = "<=",
  [anon_sym_COMMA] = ",",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [anon_sym_COLON] = ":",
  [sym_source_file] = "source_file",
  [sym_newline] = "newline",
  [sym_comment_line] = "comment_line",
  [sym_statement] = "statement",
  [sym_statement_body] = "statement_body",
  [sym_embedded_comment] = "embedded_comment",
  [sym_continuation_newline] = "continuation_newline",
  [sym_level_88_condition] = "level_88_condition",
  [sym_level_number] = "level_number",
  [sym_keyword] = "keyword",
  [sym_identifier] = "identifier",
  [sym_string_literal] = "string_literal",
  [sym_operator] = "operator",
  [sym_parenthesized] = "parenthesized",
  [aux_sym_source_file_repeat1] = "source_file_repeat1",
  [aux_sym_statement_body_repeat1] = "statement_body_repeat1",
  [aux_sym_parenthesized_repeat1] = "parenthesized_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [aux_sym_newline_token1] = aux_sym_newline_token1,
  [aux_sym_comment_line_token1] = aux_sym_comment_line_token1,
  [sym_sequence_number] = sym_sequence_number,
  [anon_sym_DOT] = anon_sym_DOT,
  [anon_sym_88] = anon_sym_88,
  [anon_sym_VALUE] = anon_sym_VALUE,
  [anon_sym_IS] = anon_sym_IS,
  [anon_sym_ARE] = anon_sym_ARE,
  [aux_sym_level_number_token1] = aux_sym_level_number_token1,
  [aux_sym_level_number_token2] = aux_sym_level_number_token2,
  [anon_sym_66] = anon_sym_66,
  [anon_sym_77] = anon_sym_77,
  [anon_sym_FILLER] = anon_sym_FILLER,
  [anon_sym_PIC] = anon_sym_PIC,
  [anon_sym_PICTURE] = anon_sym_PICTURE,
  [anon_sym_VALUES] = anon_sym_VALUES,
  [anon_sym_OCCURS] = anon_sym_OCCURS,
  [anon_sym_TIMES] = anon_sym_TIMES,
  [anon_sym_TO] = anon_sym_TO,
  [anon_sym_REDEFINES] = anon_sym_REDEFINES,
  [anon_sym_INDEXED] = anon_sym_INDEXED,
  [anon_sym_BY] = anon_sym_BY,
  [anon_sym_DEPENDING] = anon_sym_DEPENDING,
  [anon_sym_ON] = anon_sym_ON,
  [anon_sym_USAGE] = anon_sym_USAGE,
  [anon_sym_DISPLAY] = anon_sym_DISPLAY,
  [anon_sym_DISPLAY_DASH1] = anon_sym_DISPLAY_DASH1,
  [anon_sym_BINARY] = anon_sym_BINARY,
  [anon_sym_COMP] = anon_sym_COMP,
  [anon_sym_COMP_DASH1] = anon_sym_COMP_DASH1,
  [anon_sym_COMP_DASH2] = anon_sym_COMP_DASH2,
  [anon_sym_COMP_DASH3] = anon_sym_COMP_DASH3,
  [anon_sym_COMP_DASH4] = anon_sym_COMP_DASH4,
  [anon_sym_COMP_DASH5] = anon_sym_COMP_DASH5,
  [anon_sym_COMPUTATIONAL] = anon_sym_COMPUTATIONAL,
  [anon_sym_COMPUTATIONAL_DASH1] = anon_sym_COMPUTATIONAL_DASH1,
  [anon_sym_COMPUTATIONAL_DASH2] = anon_sym_COMPUTATIONAL_DASH2,
  [anon_sym_COMPUTATIONAL_DASH3] = anon_sym_COMPUTATIONAL_DASH3,
  [anon_sym_COMPUTATIONAL_DASH4] = anon_sym_COMPUTATIONAL_DASH4,
  [anon_sym_COMPUTATIONAL_DASH5] = anon_sym_COMPUTATIONAL_DASH5,
  [anon_sym_PACKED_DASHDECIMAL] = anon_sym_PACKED_DASHDECIMAL,
  [anon_sym_INDEX] = anon_sym_INDEX,
  [anon_sym_POINTER] = anon_sym_POINTER,
  [anon_sym_ZERO] = anon_sym_ZERO,
  [anon_sym_ZEROS] = anon_sym_ZEROS,
  [anon_sym_ZEROES] = anon_sym_ZEROES,
  [anon_sym_SPACE] = anon_sym_SPACE,
  [anon_sym_SPACES] = anon_sym_SPACES,
  [anon_sym_HIGH_DASHVALUE] = anon_sym_HIGH_DASHVALUE,
  [anon_sym_HIGH_DASHVALUES] = anon_sym_HIGH_DASHVALUES,
  [anon_sym_LOW_DASHVALUE] = anon_sym_LOW_DASHVALUE,
  [anon_sym_LOW_DASHVALUES] = anon_sym_LOW_DASHVALUES,
  [anon_sym_QUOTE] = anon_sym_QUOTE,
  [anon_sym_QUOTES] = anon_sym_QUOTES,
  [anon_sym_NULL] = anon_sym_NULL,
  [anon_sym_NULLS] = anon_sym_NULLS,
  [anon_sym_ALL] = anon_sym_ALL,
  [anon_sym_THRU] = anon_sym_THRU,
  [anon_sym_THROUGH] = anon_sym_THROUGH,
  [anon_sym_ASCENDING] = anon_sym_ASCENDING,
  [anon_sym_DESCENDING] = anon_sym_DESCENDING,
  [anon_sym_KEY] = anon_sym_KEY,
  [anon_sym_SIGN] = anon_sym_SIGN,
  [anon_sym_LEADING] = anon_sym_LEADING,
  [anon_sym_TRAILING] = anon_sym_TRAILING,
  [anon_sym_SEPARATE] = anon_sym_SEPARATE,
  [anon_sym_CHARACTER] = anon_sym_CHARACTER,
  [anon_sym_SYNC] = anon_sym_SYNC,
  [anon_sym_SYNCHRONIZED] = anon_sym_SYNCHRONIZED,
  [anon_sym_LEFT] = anon_sym_LEFT,
  [anon_sym_RIGHT] = anon_sym_RIGHT,
  [anon_sym_JUST] = anon_sym_JUST,
  [anon_sym_JUSTIFIED] = anon_sym_JUSTIFIED,
  [anon_sym_BLANK] = anon_sym_BLANK,
  [anon_sym_WHEN] = anon_sym_WHEN,
  [anon_sym_EXTERNAL] = anon_sym_EXTERNAL,
  [anon_sym_GLOBAL] = anon_sym_GLOBAL,
  [anon_sym_AS] = anon_sym_AS,
  [anon_sym_COPY] = anon_sym_COPY,
  [anon_sym_REPLACING] = anon_sym_REPLACING,
  [anon_sym_OF] = anon_sym_OF,
  [anon_sym_IN] = anon_sym_IN,
  [anon_sym_REPLACE] = anon_sym_REPLACE,
  [anon_sym_OFF] = anon_sym_OFF,
  [anon_sym_EJECT] = anon_sym_EJECT,
  [anon_sym_SKIP1] = anon_sym_SKIP1,
  [anon_sym_SKIP2] = anon_sym_SKIP2,
  [anon_sym_SKIP3] = anon_sym_SKIP3,
  [anon_sym_EXEC] = anon_sym_EXEC,
  [anon_sym_EXECUTE] = anon_sym_EXECUTE,
  [anon_sym_SQL] = anon_sym_SQL,
  [anon_sym_SQLIMS] = anon_sym_SQLIMS,
  [anon_sym_DLI] = anon_sym_DLI,
  [anon_sym_END_DASHEXEC] = anon_sym_END_DASHEXEC,
  [anon_sym_IF] = anon_sym_IF,
  [anon_sym_ELSE] = anon_sym_ELSE,
  [anon_sym_END_DASHIF] = anon_sym_END_DASHIF,
  [anon_sym_THEN] = anon_sym_THEN,
  [anon_sym_EVALUATE] = anon_sym_EVALUATE,
  [anon_sym_END_DASHEVALUATE] = anon_sym_END_DASHEVALUATE,
  [anon_sym_OTHER] = anon_sym_OTHER,
  [anon_sym_ALSO] = anon_sym_ALSO,
  [anon_sym_PERFORM] = anon_sym_PERFORM,
  [anon_sym_END_DASHPERFORM] = anon_sym_END_DASHPERFORM,
  [anon_sym_UNTIL] = anon_sym_UNTIL,
  [anon_sym_VARYING] = anon_sym_VARYING,
  [anon_sym_WITH] = anon_sym_WITH,
  [anon_sym_TEST] = anon_sym_TEST,
  [anon_sym_BEFORE] = anon_sym_BEFORE,
  [anon_sym_AFTER] = anon_sym_AFTER,
  [anon_sym_GO] = anon_sym_GO,
  [anon_sym_SECTION] = anon_sym_SECTION,
  [anon_sym_PARAGRAPH] = anon_sym_PARAGRAPH,
  [anon_sym_CONTINUE] = anon_sym_CONTINUE,
  [anon_sym_NEXT] = anon_sym_NEXT,
  [anon_sym_SENTENCE] = anon_sym_SENTENCE,
  [anon_sym_EXIT] = anon_sym_EXIT,
  [anon_sym_STOP] = anon_sym_STOP,
  [anon_sym_RUN] = anon_sym_RUN,
  [anon_sym_MOVE] = anon_sym_MOVE,
  [anon_sym_CORRESPONDING] = anon_sym_CORRESPONDING,
  [anon_sym_CORR] = anon_sym_CORR,
  [anon_sym_INTO] = anon_sym_INTO,
  [anon_sym_SET] = anon_sym_SET,
  [anon_sym_TRUE] = anon_sym_TRUE,
  [anon_sym_FALSE] = anon_sym_FALSE,
  [anon_sym_INITIALIZE] = anon_sym_INITIALIZE,
  [anon_sym_ALPHABETIC] = anon_sym_ALPHABETIC,
  [anon_sym_ALPHANUMERIC] = anon_sym_ALPHANUMERIC,
  [anon_sym_ALPHANUMERIC_DASHEDITED] = anon_sym_ALPHANUMERIC_DASHEDITED,
  [anon_sym_NUMERIC] = anon_sym_NUMERIC,
  [anon_sym_NUMERIC_DASHEDITED] = anon_sym_NUMERIC_DASHEDITED,
  [anon_sym_COMPUTE] = anon_sym_COMPUTE,
  [anon_sym_ADD] = anon_sym_ADD,
  [anon_sym_SUBTRACT] = anon_sym_SUBTRACT,
  [anon_sym_MULTIPLY] = anon_sym_MULTIPLY,
  [anon_sym_DIVIDE] = anon_sym_DIVIDE,
  [anon_sym_GIVING] = anon_sym_GIVING,
  [anon_sym_REMAINDER] = anon_sym_REMAINDER,
  [anon_sym_STRING] = anon_sym_STRING,
  [anon_sym_DELIMITED] = anon_sym_DELIMITED,
  [anon_sym_SIZE] = anon_sym_SIZE,
  [anon_sym_OVERFLOW] = anon_sym_OVERFLOW,
  [anon_sym_NOT] = anon_sym_NOT,
  [anon_sym_END_DASHSTRING] = anon_sym_END_DASHSTRING,
  [anon_sym_UNSTRING] = anon_sym_UNSTRING,
  [anon_sym_COUNT] = anon_sym_COUNT,
  [anon_sym_DELIMITER] = anon_sym_DELIMITER,
  [anon_sym_TALLYING] = anon_sym_TALLYING,
  [anon_sym_END_DASHUNSTRING] = anon_sym_END_DASHUNSTRING,
  [anon_sym_INSPECT] = anon_sym_INSPECT,
  [anon_sym_CONVERTING] = anon_sym_CONVERTING,
  [anon_sym_FIRST] = anon_sym_FIRST,
  [anon_sym_INITIAL] = anon_sym_INITIAL,
  [anon_sym_READ] = anon_sym_READ,
  [anon_sym_WRITE] = anon_sym_WRITE,
  [anon_sym_REWRITE] = anon_sym_REWRITE,
  [anon_sym_DELETE] = anon_sym_DELETE,
  [anon_sym_START] = anon_sym_START,
  [anon_sym_OPEN] = anon_sym_OPEN,
  [anon_sym_CLOSE] = anon_sym_CLOSE,
  [anon_sym_INPUT] = anon_sym_INPUT,
  [anon_sym_OUTPUT] = anon_sym_OUTPUT,
  [anon_sym_I_DASHO] = anon_sym_I_DASHO,
  [anon_sym_EXTEND] = anon_sym_EXTEND,
  [anon_sym_ACCEPT] = anon_sym_ACCEPT,
  [anon_sym_FROM] = anon_sym_FROM,
  [anon_sym_DATE] = anon_sym_DATE,
  [anon_sym_DAY] = anon_sym_DAY,
  [anon_sym_TIME] = anon_sym_TIME,
  [anon_sym_DAY_DASHOF_DASHWEEK] = anon_sym_DAY_DASHOF_DASHWEEK,
  [anon_sym_EQUAL] = anon_sym_EQUAL,
  [anon_sym_GREATER] = anon_sym_GREATER,
  [anon_sym_LESS] = anon_sym_LESS,
  [anon_sym_THAN] = anon_sym_THAN,
  [anon_sym_OR] = anon_sym_OR,
  [anon_sym_AND] = anon_sym_AND,
  [anon_sym_DFHENTER] = anon_sym_DFHENTER,
  [anon_sym_DFHCLEAR] = anon_sym_DFHCLEAR,
  [anon_sym_DFHPA1] = anon_sym_DFHPA1,
  [anon_sym_DFHPA2] = anon_sym_DFHPA2,
  [anon_sym_DFHPF1] = anon_sym_DFHPF1,
  [anon_sym_DFHPF2] = anon_sym_DFHPF2,
  [anon_sym_DFHPF3] = anon_sym_DFHPF3,
  [anon_sym_DFHPF4] = anon_sym_DFHPF4,
  [anon_sym_DFHPF5] = anon_sym_DFHPF5,
  [anon_sym_DFHPF6] = anon_sym_DFHPF6,
  [anon_sym_DFHPF7] = anon_sym_DFHPF7,
  [anon_sym_DFHPF8] = anon_sym_DFHPF8,
  [anon_sym_DFHPF9] = anon_sym_DFHPF9,
  [anon_sym_DFHPF10] = anon_sym_DFHPF10,
  [anon_sym_DFHPF11] = anon_sym_DFHPF11,
  [anon_sym_DFHPF12] = anon_sym_DFHPF12,
  [anon_sym_EIBAID] = anon_sym_EIBAID,
  [anon_sym_DFHRED] = anon_sym_DFHRED,
  [anon_sym_DFHBMASB] = anon_sym_DFHBMASB,
  [anon_sym_DFHBMASK] = anon_sym_DFHBMASK,
  [aux_sym_identifier_token1] = aux_sym_identifier_token1,
  [aux_sym_identifier_token2] = aux_sym_identifier_token2,
  [sym_picture_string] = sym_picture_string,
  [aux_sym_string_literal_token1] = aux_sym_string_literal_token1,
  [aux_sym_string_literal_token2] = aux_sym_string_literal_token2,
  [sym_number] = sym_number,
  [anon_sym_EQ_EQ] = anon_sym_EQ_EQ,
  [anon_sym_EQ] = anon_sym_EQ,
  [anon_sym_GT] = anon_sym_GT,
  [anon_sym_LT] = anon_sym_LT,
  [anon_sym_GT_EQ] = anon_sym_GT_EQ,
  [anon_sym_LT_EQ] = anon_sym_LT_EQ,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [anon_sym_COLON] = anon_sym_COLON,
  [sym_source_file] = sym_source_file,
  [sym_newline] = sym_newline,
  [sym_comment_line] = sym_comment_line,
  [sym_statement] = sym_statement,
  [sym_statement_body] = sym_statement_body,
  [sym_embedded_comment] = sym_embedded_comment,
  [sym_continuation_newline] = sym_continuation_newline,
  [sym_level_88_condition] = sym_level_88_condition,
  [sym_level_number] = sym_level_number,
  [sym_keyword] = sym_keyword,
  [sym_identifier] = sym_identifier,
  [sym_string_literal] = sym_string_literal,
  [sym_operator] = sym_operator,
  [sym_parenthesized] = sym_parenthesized,
  [aux_sym_source_file_repeat1] = aux_sym_source_file_repeat1,
  [aux_sym_statement_body_repeat1] = aux_sym_statement_body_repeat1,
  [aux_sym_parenthesized_repeat1] = aux_sym_parenthesized_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [aux_sym_newline_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_comment_line_token1] = {
    .visible = false,
    .named = false,
  },
  [sym_sequence_number] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_DOT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_88] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_VALUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_IS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ARE] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_level_number_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_level_number_token2] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_66] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_77] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FILLER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PIC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PICTURE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_VALUES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OCCURS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TIMES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_REDEFINES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INDEXED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DEPENDING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ON] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_USAGE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DISPLAY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DISPLAY_DASH1] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BINARY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMP] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMP_DASH1] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMP_DASH2] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMP_DASH3] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMP_DASH4] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMP_DASH5] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTATIONAL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTATIONAL_DASH1] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTATIONAL_DASH2] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTATIONAL_DASH3] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTATIONAL_DASH4] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTATIONAL_DASH5] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PACKED_DASHDECIMAL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INDEX] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_POINTER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ZERO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ZEROS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ZEROES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SPACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SPACES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_HIGH_DASHVALUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_HIGH_DASHVALUES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LOW_DASHVALUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LOW_DASHVALUES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_QUOTE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_QUOTES] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NULL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NULLS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ALL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_THRU] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_THROUGH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ASCENDING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DESCENDING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_KEY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SIGN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LEADING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TRAILING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SEPARATE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CHARACTER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SYNC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SYNCHRONIZED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LEFT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RIGHT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_JUST] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_JUSTIFIED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BLANK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_WHEN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EXTERNAL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GLOBAL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_AS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COPY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_REPLACING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OF] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_IN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_REPLACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OFF] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EJECT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SKIP1] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SKIP2] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SKIP3] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EXEC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EXECUTE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SQL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SQLIMS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DLI] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END_DASHEXEC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_IF] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ELSE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END_DASHIF] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_THEN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EVALUATE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END_DASHEVALUATE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OTHER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ALSO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PERFORM] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END_DASHPERFORM] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_UNTIL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_VARYING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_WITH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TEST] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_BEFORE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_AFTER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SECTION] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_PARAGRAPH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CONTINUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NEXT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SENTENCE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EXIT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STOP] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RUN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_MOVE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CORRESPONDING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CORR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INTO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SET] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TRUE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FALSE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INITIALIZE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ALPHABETIC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ALPHANUMERIC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ALPHANUMERIC_DASHEDITED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NUMERIC] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NUMERIC_DASHEDITED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMPUTE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ADD] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SUBTRACT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_MULTIPLY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DIVIDE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GIVING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_REMAINDER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STRING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DELIMITED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_SIZE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OVERFLOW] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_NOT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END_DASHSTRING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_UNSTRING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COUNT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DELIMITER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TALLYING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_END_DASHUNSTRING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INSPECT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CONVERTING] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FIRST] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INITIAL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_READ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_WRITE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_REWRITE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DELETE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_START] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OPEN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_CLOSE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_INPUT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OUTPUT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_I_DASHO] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EXTEND] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ACCEPT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_FROM] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DATE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DAY] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_TIME] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DAY_DASHOF_DASHWEEK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EQUAL] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GREATER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LESS] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_THAN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_OR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_AND] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHENTER] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHCLEAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPA1] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPA2] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF1] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF2] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF3] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF4] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF5] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF6] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF7] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF8] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF9] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF10] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF11] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHPF12] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EIBAID] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHRED] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHBMASB] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DFHBMASK] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_identifier_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_identifier_token2] = {
    .visible = false,
    .named = false,
  },
  [sym_picture_string] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_string_literal_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_string_literal_token2] = {
    .visible = false,
    .named = false,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_EQ_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LT] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_GT_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LT_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
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
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [sym_source_file] = {
    .visible = true,
    .named = true,
  },
  [sym_newline] = {
    .visible = true,
    .named = true,
  },
  [sym_comment_line] = {
    .visible = true,
    .named = true,
  },
  [sym_statement] = {
    .visible = true,
    .named = true,
  },
  [sym_statement_body] = {
    .visible = true,
    .named = true,
  },
  [sym_embedded_comment] = {
    .visible = true,
    .named = true,
  },
  [sym_continuation_newline] = {
    .visible = true,
    .named = true,
  },
  [sym_level_88_condition] = {
    .visible = true,
    .named = true,
  },
  [sym_level_number] = {
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
  [sym_string_literal] = {
    .visible = true,
    .named = true,
  },
  [sym_operator] = {
    .visible = true,
    .named = true,
  },
  [sym_parenthesized] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_source_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_statement_body_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_parenthesized_repeat1] = {
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
  [27] = 16,
  [28] = 18,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 18,
};

static TSCharacterRange sym_picture_string_character_set_1[] = {
  {'$', '$'}, {'*', '-'}, {'/', '0'}, {'9', '9'}, {'A', 'B'}, {'E', 'E'}, {'P', 'P'}, {'S', 'S'},
  {'V', 'V'}, {'X', 'X'}, {'Z', 'Z'}, {'a', 'b'}, {'e', 'e'}, {'p', 'p'}, {'s', 's'}, {'v', 'v'},
  {'x', 'x'}, {'z', 'z'},
};

static TSCharacterRange sym_picture_string_character_set_2[] = {
  {'$', '$'}, {'(', '('}, {'*', '-'}, {'/', '0'}, {'9', '9'}, {'A', 'B'}, {'E', 'E'}, {'P', 'P'},
  {'S', 'S'}, {'V', 'V'}, {'X', 'X'}, {'Z', 'Z'}, {'a', 'b'}, {'e', 'e'}, {'p', 'p'}, {'s', 's'},
  {'v', 'v'}, {'x', 'x'}, {'z', 'z'},
};

static TSCharacterRange sym_picture_string_character_set_3[] = {
  {'(', ')'}, {'0', '0'}, {'9', '9'}, {'A', 'A'}, {'S', 'S'}, {'V', 'V'}, {'X', 'X'}, {'Z', 'Z'},
  {'a', 'a'}, {'s', 's'}, {'v', 'v'}, {'x', 'x'}, {'z', 'z'},
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(22);
      ADVANCE_MAP(
        '\n', 23,
        '"', 5,
        '\'', 6,
        '(', 789,
        ')', 790,
        '*', 24,
        ',', 788,
        '.', 28,
        '0', 749,
        '5', 778,
        '6', 766,
        '7', 768,
        '8', 770,
        '9', 755,
        ':', 791,
        '<', 784,
        '=', 782,
        '>', 783,
        'A', 231,
        'B', 342,
        'C', 454,
        'D', 249,
        'E', 460,
        'F', 250,
        'G', 461,
        'H', 462,
        'I', 240,
        'J', 711,
        'K', 343,
        'L', 344,
        'M', 589,
        'N', 345,
        'O', 305,
        'P', 251,
        'Q', 712,
        'R', 346,
        'S', 233,
        'T', 262,
        'U', 543,
        'V', 230,
        'W', 458,
        'Z', 234,
        '$', 763,
        '/', 763,
        '+', 760,
        '-', 760,
      );
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0);
      if (lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '4')) ADVANCE(772);
      if (lookahead == 'X' ||
          lookahead == 'a' ||
          lookahead == 's' ||
          lookahead == 'v' ||
          lookahead == 'x' ||
          lookahead == 'z') ADVANCE(236);
      if (lookahead == 'Y' ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 1:
      ADVANCE_MAP(
        '\n', 23,
        '"', 5,
        '\'', 6,
        '(', 789,
        ')', 790,
        '*', 24,
        ',', 788,
        '.', 28,
        '0', 750,
        '5', 779,
        '6', 767,
        '7', 769,
        '8', 771,
        '9', 756,
        ':', 791,
        '<', 784,
        '=', 782,
        '>', 783,
        'A', 232,
        'B', 342,
        'C', 454,
        'D', 249,
        'E', 460,
        'F', 250,
        'G', 461,
        'H', 462,
        'I', 240,
        'J', 711,
        'K', 343,
        'L', 344,
        'M', 589,
        'N', 345,
        'O', 305,
        'P', 251,
        'Q', 712,
        'R', 346,
        'S', 233,
        'T', 262,
        'U', 543,
        'V', 230,
        'W', 458,
        'Z', 234,
        '$', 763,
        '/', 763,
        '+', 760,
        '-', 760,
      );
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(1);
      if (lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '4')) ADVANCE(777);
      if (lookahead == 'X' ||
          lookahead == 'a' ||
          lookahead == 's' ||
          lookahead == 'v' ||
          lookahead == 'x' ||
          lookahead == 'z') ADVANCE(236);
      if (lookahead == 'Y' ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 2:
      ADVANCE_MAP(
        '\n', 23,
        '"', 5,
        '\'', 6,
        '(', 789,
        ')', 790,
        ',', 788,
        '.', 28,
        '0', 750,
        '5', 779,
        '6', 767,
        '7', 769,
        '8', 771,
        '9', 756,
        ':', 791,
        '<', 784,
        '=', 782,
        '>', 783,
        'A', 231,
        'B', 342,
        'C', 454,
        'D', 249,
        'E', 460,
        'F', 250,
        'G', 461,
        'H', 462,
        'I', 240,
        'J', 711,
        'K', 343,
        'L', 344,
        'M', 589,
        'N', 345,
        'O', 305,
        'P', 251,
        'Q', 712,
        'R', 346,
        'S', 233,
        'T', 262,
        'U', 543,
        'V', 230,
        'W', 458,
        'Z', 234,
        '+', 760,
        '-', 760,
      );
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(2);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= '/')) ADVANCE(763);
      if (lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '4')) ADVANCE(777);
      if (lookahead == 'X' ||
          lookahead == 'a' ||
          lookahead == 's' ||
          lookahead == 'v' ||
          lookahead == 'x' ||
          lookahead == 'z') ADVANCE(236);
      if (lookahead == 'Y' ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 3:
      ADVANCE_MAP(
        '\n', 23,
        '"', 5,
        '\'', 6,
        '(', 789,
        ')', 790,
        ',', 788,
        '.', 28,
        '0', 750,
        '5', 779,
        '6', 767,
        '7', 769,
        '8', 771,
        '9', 756,
        ':', 791,
        '<', 784,
        '=', 782,
        '>', 783,
        'A', 232,
        'B', 342,
        'C', 454,
        'D', 249,
        'E', 460,
        'F', 250,
        'G', 461,
        'H', 462,
        'I', 240,
        'J', 711,
        'K', 343,
        'L', 344,
        'M', 589,
        'N', 345,
        'O', 305,
        'P', 251,
        'Q', 712,
        'R', 346,
        'S', 233,
        'T', 262,
        'U', 543,
        'V', 230,
        'W', 458,
        'Z', 234,
        '+', 760,
        '-', 760,
      );
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(3);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= '/')) ADVANCE(763);
      if (lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '4')) ADVANCE(777);
      if (lookahead == 'X' ||
          lookahead == 'a' ||
          lookahead == 's' ||
          lookahead == 'v' ||
          lookahead == 'x' ||
          lookahead == 'z') ADVANCE(236);
      if (lookahead == 'Y' ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 4:
      if (lookahead == '"') ADVANCE(5);
      if (lookahead == '\'') ADVANCE(6);
      if (lookahead == '(') ADVANCE(19);
      if (lookahead == ')') ADVANCE(790);
      if (lookahead == ',') ADVANCE(787);
      if (('+' <= lookahead && lookahead <= '-')) ADVANCE(18);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(4);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 5:
      if (lookahead == '"') ADVANCE(765);
      if (lookahead != 0) ADVANCE(5);
      END_STATE();
    case 6:
      if (lookahead == '\'') ADVANCE(764);
      if (lookahead != 0) ADVANCE(6);
      END_STATE();
    case 7:
      if (lookahead == ')') ADVANCE(746);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 8:
      if (lookahead == ')') ADVANCE(748);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(8);
      END_STATE();
    case 9:
      if (lookahead == ')') ADVANCE(762);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(9);
      END_STATE();
    case 10:
      if (lookahead == ')') ADVANCE(747);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(10);
      if (lookahead == '-' ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 11:
      if (lookahead == 'A') ADVANCE(13);
      END_STATE();
    case 12:
      if (lookahead == 'E') ADVANCE(31);
      END_STATE();
    case 13:
      if (lookahead == 'L') ADVANCE(14);
      END_STATE();
    case 14:
      if (lookahead == 'U') ADVANCE(12);
      END_STATE();
    case 15:
      if (lookahead == 'V') ADVANCE(11);
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(15);
      END_STATE();
    case 16:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(9);
      END_STATE();
    case 17:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(10);
      if (lookahead == '-' ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 18:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 19:
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(8);
      END_STATE();
    case 20:
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(7);
      END_STATE();
    case 21:
      if (eof) ADVANCE(22);
      ADVANCE_MAP(
        '\n', 23,
        '"', 5,
        '\'', 6,
        '(', 789,
        ')', 790,
        '*', 24,
        ',', 788,
        '.', 28,
        '0', 749,
        '5', 778,
        '6', 766,
        '7', 768,
        '8', 770,
        '9', 755,
        ':', 791,
        '<', 784,
        '=', 782,
        '>', 783,
        'A', 232,
        'B', 342,
        'C', 454,
        'D', 249,
        'E', 460,
        'F', 250,
        'G', 461,
        'H', 462,
        'I', 240,
        'J', 711,
        'K', 343,
        'L', 344,
        'M', 589,
        'N', 345,
        'O', 305,
        'P', 251,
        'Q', 712,
        'R', 346,
        'S', 233,
        'T', 262,
        'U', 543,
        'V', 230,
        'W', 458,
        'Z', 234,
        '$', 763,
        '/', 763,
        '+', 760,
        '-', 760,
      );
      if (lookahead == '\t' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(21);
      if (lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '4')) ADVANCE(772);
      if (lookahead == 'X' ||
          lookahead == 'a' ||
          lookahead == 's' ||
          lookahead == 'v' ||
          lookahead == 'x' ||
          lookahead == 'z') ADVANCE(236);
      if (lookahead == 'Y' ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 22:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 23:
      ACCEPT_TOKEN(aux_sym_newline_token1);
      END_STATE();
    case 24:
      ACCEPT_TOKEN(aux_sym_comment_line_token1);
      if (set_contains(sym_picture_string_character_set_1, 18, lookahead)) ADVANCE(24);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(25);
      END_STATE();
    case 25:
      ACCEPT_TOKEN(aux_sym_comment_line_token1);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(25);
      END_STATE();
    case 26:
      ACCEPT_TOKEN(sym_sequence_number);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(756);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(779);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 27:
      ACCEPT_TOKEN(sym_sequence_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 28:
      ACCEPT_TOKEN(anon_sym_DOT);
      END_STATE();
    case 29:
      ACCEPT_TOKEN(anon_sym_88);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(775);
      END_STATE();
    case 30:
      ACCEPT_TOKEN(anon_sym_88);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 31:
      ACCEPT_TOKEN(anon_sym_VALUE);
      END_STATE();
    case 32:
      ACCEPT_TOKEN(anon_sym_VALUE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(48);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 33:
      ACCEPT_TOKEN(anon_sym_IS);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 34:
      ACCEPT_TOKEN(anon_sym_ARE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 35:
      ACCEPT_TOKEN(aux_sym_level_number_token1);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(752);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(775);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 36:
      ACCEPT_TOKEN(aux_sym_level_number_token1);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(756);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(779);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 37:
      ACCEPT_TOKEN(aux_sym_level_number_token1);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(775);
      END_STATE();
    case 38:
      ACCEPT_TOKEN(aux_sym_level_number_token1);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 39:
      ACCEPT_TOKEN(aux_sym_level_number_token2);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(775);
      END_STATE();
    case 40:
      ACCEPT_TOKEN(aux_sym_level_number_token2);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 41:
      ACCEPT_TOKEN(anon_sym_66);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(775);
      END_STATE();
    case 42:
      ACCEPT_TOKEN(anon_sym_66);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 43:
      ACCEPT_TOKEN(anon_sym_77);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(775);
      END_STATE();
    case 44:
      ACCEPT_TOKEN(anon_sym_77);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 45:
      ACCEPT_TOKEN(anon_sym_FILLER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 46:
      ACCEPT_TOKEN(anon_sym_PIC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(722);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 47:
      ACCEPT_TOKEN(anon_sym_PICTURE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 48:
      ACCEPT_TOKEN(anon_sym_VALUES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 49:
      ACCEPT_TOKEN(anon_sym_OCCURS);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 50:
      ACCEPT_TOKEN(anon_sym_TIMES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 51:
      ACCEPT_TOKEN(anon_sym_TO);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 52:
      ACCEPT_TOKEN(anon_sym_REDEFINES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 53:
      ACCEPT_TOKEN(anon_sym_INDEXED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 54:
      ACCEPT_TOKEN(anon_sym_BY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 55:
      ACCEPT_TOKEN(anon_sym_DEPENDING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 56:
      ACCEPT_TOKEN(anon_sym_ON);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 57:
      ACCEPT_TOKEN(anon_sym_USAGE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 58:
      ACCEPT_TOKEN(anon_sym_DISPLAY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(247);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 59:
      ACCEPT_TOKEN(anon_sym_DISPLAY_DASH1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 60:
      ACCEPT_TOKEN(anon_sym_BINARY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 61:
      ACCEPT_TOKEN(anon_sym_COMP);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(244);
      if (lookahead == 'U') ADVANCE(676);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 62:
      ACCEPT_TOKEN(anon_sym_COMP_DASH1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 63:
      ACCEPT_TOKEN(anon_sym_COMP_DASH2);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 64:
      ACCEPT_TOKEN(anon_sym_COMP_DASH3);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 65:
      ACCEPT_TOKEN(anon_sym_COMP_DASH4);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 66:
      ACCEPT_TOKEN(anon_sym_COMP_DASH5);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 67:
      ACCEPT_TOKEN(anon_sym_COMPUTATIONAL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(248);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 68:
      ACCEPT_TOKEN(anon_sym_COMPUTATIONAL_DASH1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 69:
      ACCEPT_TOKEN(anon_sym_COMPUTATIONAL_DASH2);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 70:
      ACCEPT_TOKEN(anon_sym_COMPUTATIONAL_DASH3);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 71:
      ACCEPT_TOKEN(anon_sym_COMPUTATIONAL_DASH4);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 72:
      ACCEPT_TOKEN(anon_sym_COMPUTATIONAL_DASH5);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 73:
      ACCEPT_TOKEN(anon_sym_PACKED_DASHDECIMAL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 74:
      ACCEPT_TOKEN(anon_sym_INDEX);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(325);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 75:
      ACCEPT_TOKEN(anon_sym_POINTER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 76:
      ACCEPT_TOKEN(anon_sym_ZERO);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(650);
      if (lookahead == 'S') ADVANCE(77);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 77:
      ACCEPT_TOKEN(anon_sym_ZEROS);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 78:
      ACCEPT_TOKEN(anon_sym_ZEROES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 79:
      ACCEPT_TOKEN(anon_sym_SPACE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(80);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 80:
      ACCEPT_TOKEN(anon_sym_SPACES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 81:
      ACCEPT_TOKEN(anon_sym_HIGH_DASHVALUE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(82);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 82:
      ACCEPT_TOKEN(anon_sym_HIGH_DASHVALUES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 83:
      ACCEPT_TOKEN(anon_sym_LOW_DASHVALUE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(84);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 84:
      ACCEPT_TOKEN(anon_sym_LOW_DASHVALUES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 85:
      ACCEPT_TOKEN(anon_sym_QUOTE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(86);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 86:
      ACCEPT_TOKEN(anon_sym_QUOTES);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 87:
      ACCEPT_TOKEN(anon_sym_NULL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(88);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 88:
      ACCEPT_TOKEN(anon_sym_NULLS);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 89:
      ACCEPT_TOKEN(anon_sym_ALL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 90:
      ACCEPT_TOKEN(anon_sym_THRU);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 91:
      ACCEPT_TOKEN(anon_sym_THROUGH);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 92:
      ACCEPT_TOKEN(anon_sym_ASCENDING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 93:
      ACCEPT_TOKEN(anon_sym_DESCENDING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 94:
      ACCEPT_TOKEN(anon_sym_KEY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 95:
      ACCEPT_TOKEN(anon_sym_SIGN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 96:
      ACCEPT_TOKEN(anon_sym_LEADING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 97:
      ACCEPT_TOKEN(anon_sym_TRAILING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 98:
      ACCEPT_TOKEN(anon_sym_SEPARATE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 99:
      ACCEPT_TOKEN(anon_sym_CHARACTER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 100:
      ACCEPT_TOKEN(anon_sym_SYNC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(640);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 101:
      ACCEPT_TOKEN(anon_sym_SYNCHRONIZED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 102:
      ACCEPT_TOKEN(anon_sym_LEFT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 103:
      ACCEPT_TOKEN(anon_sym_RIGHT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 104:
      ACCEPT_TOKEN(anon_sym_JUST);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(424);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 105:
      ACCEPT_TOKEN(anon_sym_JUSTIFIED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 106:
      ACCEPT_TOKEN(anon_sym_BLANK);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 107:
      ACCEPT_TOKEN(anon_sym_WHEN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 108:
      ACCEPT_TOKEN(anon_sym_EXTERNAL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 109:
      ACCEPT_TOKEN(anon_sym_GLOBAL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 110:
      ACCEPT_TOKEN(anon_sym_AS);
      if (lookahead == '(') ADVANCE(17);
      if (lookahead == 'C') ADVANCE(396);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          lookahead == 'B' ||
          lookahead == 'E' ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('D' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 111:
      ACCEPT_TOKEN(anon_sym_COPY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 112:
      ACCEPT_TOKEN(anon_sym_REPLACING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 113:
      ACCEPT_TOKEN(anon_sym_OF);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(116);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 114:
      ACCEPT_TOKEN(anon_sym_IN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(380);
      if (lookahead == 'I') ADVANCE(682);
      if (lookahead == 'P') ADVANCE(715);
      if (lookahead == 'S') ADVANCE(613);
      if (lookahead == 'T') ADVANCE(587);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 115:
      ACCEPT_TOKEN(anon_sym_REPLACE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 116:
      ACCEPT_TOKEN(anon_sym_OFF);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 117:
      ACCEPT_TOKEN(anon_sym_EJECT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 118:
      ACCEPT_TOKEN(anon_sym_SKIP1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 119:
      ACCEPT_TOKEN(anon_sym_SKIP2);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 120:
      ACCEPT_TOKEN(anon_sym_SKIP3);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 121:
      ACCEPT_TOKEN(anon_sym_EXEC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(695);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 122:
      ACCEPT_TOKEN(anon_sym_EXECUTE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 123:
      ACCEPT_TOKEN(anon_sym_SQL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(537);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 124:
      ACCEPT_TOKEN(anon_sym_SQLIMS);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 125:
      ACCEPT_TOKEN(anon_sym_DLI);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 126:
      ACCEPT_TOKEN(anon_sym_END_DASHEXEC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 127:
      ACCEPT_TOKEN(anon_sym_IF);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 128:
      ACCEPT_TOKEN(anon_sym_ELSE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 129:
      ACCEPT_TOKEN(anon_sym_END_DASHIF);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 130:
      ACCEPT_TOKEN(anon_sym_THEN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 131:
      ACCEPT_TOKEN(anon_sym_EVALUATE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 132:
      ACCEPT_TOKEN(anon_sym_END_DASHEVALUATE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 133:
      ACCEPT_TOKEN(anon_sym_OTHER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 134:
      ACCEPT_TOKEN(anon_sym_ALSO);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 135:
      ACCEPT_TOKEN(anon_sym_PERFORM);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 136:
      ACCEPT_TOKEN(anon_sym_END_DASHPERFORM);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 137:
      ACCEPT_TOKEN(anon_sym_UNTIL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 138:
      ACCEPT_TOKEN(anon_sym_VARYING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 139:
      ACCEPT_TOKEN(anon_sym_WITH);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 140:
      ACCEPT_TOKEN(anon_sym_TEST);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 141:
      ACCEPT_TOKEN(anon_sym_BEFORE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 142:
      ACCEPT_TOKEN(anon_sym_AFTER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 143:
      ACCEPT_TOKEN(anon_sym_GO);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 144:
      ACCEPT_TOKEN(anon_sym_SECTION);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 145:
      ACCEPT_TOKEN(anon_sym_PARAGRAPH);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 146:
      ACCEPT_TOKEN(anon_sym_CONTINUE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 147:
      ACCEPT_TOKEN(anon_sym_NEXT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 148:
      ACCEPT_TOKEN(anon_sym_SENTENCE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 149:
      ACCEPT_TOKEN(anon_sym_EXIT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 150:
      ACCEPT_TOKEN(anon_sym_STOP);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 151:
      ACCEPT_TOKEN(anon_sym_RUN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 152:
      ACCEPT_TOKEN(anon_sym_MOVE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 153:
      ACCEPT_TOKEN(anon_sym_CORRESPONDING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 154:
      ACCEPT_TOKEN(anon_sym_CORR);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(655);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 155:
      ACCEPT_TOKEN(anon_sym_INTO);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 156:
      ACCEPT_TOKEN(anon_sym_SET);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 157:
      ACCEPT_TOKEN(anon_sym_TRUE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 158:
      ACCEPT_TOKEN(anon_sym_FALSE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 159:
      ACCEPT_TOKEN(anon_sym_INITIALIZE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 160:
      ACCEPT_TOKEN(anon_sym_ALPHABETIC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 161:
      ACCEPT_TOKEN(anon_sym_ALPHANUMERIC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(419);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 162:
      ACCEPT_TOKEN(anon_sym_ALPHANUMERIC_DASHEDITED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 163:
      ACCEPT_TOKEN(anon_sym_NUMERIC);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(399);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 164:
      ACCEPT_TOKEN(anon_sym_NUMERIC_DASHEDITED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 165:
      ACCEPT_TOKEN(anon_sym_COMPUTE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 166:
      ACCEPT_TOKEN(anon_sym_ADD);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 167:
      ACCEPT_TOKEN(anon_sym_SUBTRACT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 168:
      ACCEPT_TOKEN(anon_sym_MULTIPLY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 169:
      ACCEPT_TOKEN(anon_sym_DIVIDE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 170:
      ACCEPT_TOKEN(anon_sym_GIVING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 171:
      ACCEPT_TOKEN(anon_sym_REMAINDER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 172:
      ACCEPT_TOKEN(anon_sym_STRING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 173:
      ACCEPT_TOKEN(anon_sym_DELIMITED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 174:
      ACCEPT_TOKEN(anon_sym_SIZE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 175:
      ACCEPT_TOKEN(anon_sym_OVERFLOW);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 176:
      ACCEPT_TOKEN(anon_sym_NOT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 177:
      ACCEPT_TOKEN(anon_sym_END_DASHSTRING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 178:
      ACCEPT_TOKEN(anon_sym_UNSTRING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 179:
      ACCEPT_TOKEN(anon_sym_COUNT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 180:
      ACCEPT_TOKEN(anon_sym_DELIMITER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 181:
      ACCEPT_TOKEN(anon_sym_TALLYING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 182:
      ACCEPT_TOKEN(anon_sym_END_DASHUNSTRING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 183:
      ACCEPT_TOKEN(anon_sym_INSPECT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 184:
      ACCEPT_TOKEN(anon_sym_CONVERTING);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 185:
      ACCEPT_TOKEN(anon_sym_FIRST);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 186:
      ACCEPT_TOKEN(anon_sym_INITIAL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(743);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 187:
      ACCEPT_TOKEN(anon_sym_READ);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 188:
      ACCEPT_TOKEN(anon_sym_WRITE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 189:
      ACCEPT_TOKEN(anon_sym_REWRITE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 190:
      ACCEPT_TOKEN(anon_sym_DELETE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 191:
      ACCEPT_TOKEN(anon_sym_START);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 192:
      ACCEPT_TOKEN(anon_sym_OPEN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 193:
      ACCEPT_TOKEN(anon_sym_CLOSE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 194:
      ACCEPT_TOKEN(anon_sym_INPUT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 195:
      ACCEPT_TOKEN(anon_sym_OUTPUT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 196:
      ACCEPT_TOKEN(anon_sym_I_DASHO);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 197:
      ACCEPT_TOKEN(anon_sym_EXTEND);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 198:
      ACCEPT_TOKEN(anon_sym_ACCEPT);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 199:
      ACCEPT_TOKEN(anon_sym_FROM);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 200:
      ACCEPT_TOKEN(anon_sym_DATE);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 201:
      ACCEPT_TOKEN(anon_sym_DAY);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(592);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 202:
      ACCEPT_TOKEN(anon_sym_TIME);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(50);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 203:
      ACCEPT_TOKEN(anon_sym_DAY_DASHOF_DASHWEEK);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 204:
      ACCEPT_TOKEN(anon_sym_EQUAL);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 205:
      ACCEPT_TOKEN(anon_sym_GREATER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 206:
      ACCEPT_TOKEN(anon_sym_LESS);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 207:
      ACCEPT_TOKEN(anon_sym_THAN);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 208:
      ACCEPT_TOKEN(anon_sym_OR);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 209:
      ACCEPT_TOKEN(anon_sym_AND);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 210:
      ACCEPT_TOKEN(anon_sym_DFHENTER);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 211:
      ACCEPT_TOKEN(anon_sym_DFHCLEAR);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 212:
      ACCEPT_TOKEN(anon_sym_DFHPA1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 213:
      ACCEPT_TOKEN(anon_sym_DFHPA2);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 214:
      ACCEPT_TOKEN(anon_sym_DFHPF1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '0') ADVANCE(223);
      if (lookahead == '1') ADVANCE(224);
      if (lookahead == '2') ADVANCE(225);
      if (lookahead == '-' ||
          ('3' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 215:
      ACCEPT_TOKEN(anon_sym_DFHPF2);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 216:
      ACCEPT_TOKEN(anon_sym_DFHPF3);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 217:
      ACCEPT_TOKEN(anon_sym_DFHPF4);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 218:
      ACCEPT_TOKEN(anon_sym_DFHPF5);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 219:
      ACCEPT_TOKEN(anon_sym_DFHPF6);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 220:
      ACCEPT_TOKEN(anon_sym_DFHPF7);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 221:
      ACCEPT_TOKEN(anon_sym_DFHPF8);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 222:
      ACCEPT_TOKEN(anon_sym_DFHPF9);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 223:
      ACCEPT_TOKEN(anon_sym_DFHPF10);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 224:
      ACCEPT_TOKEN(anon_sym_DFHPF11);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 225:
      ACCEPT_TOKEN(anon_sym_DFHPF12);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 226:
      ACCEPT_TOKEN(anon_sym_EIBAID);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 227:
      ACCEPT_TOKEN(anon_sym_DFHRED);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 228:
      ACCEPT_TOKEN(anon_sym_DFHBMASB);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 229:
      ACCEPT_TOKEN(anon_sym_DFHBMASK);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 230:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(17);
      if (lookahead == 'A') ADVANCE(235);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          lookahead == 'B' ||
          lookahead == 'E' ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 231:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      ADVANCE_MAP(
        '(', 17,
        'C', 308,
        'D', 318,
        'F', 683,
        'L', 505,
        'N', 319,
        'R', 347,
        'S', 110,
      );
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          ('B' <= lookahead && lookahead <= 'E') ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('G' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 232:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(17);
      if (lookahead == 'C') ADVANCE(308);
      if (lookahead == 'D') ADVANCE(318);
      if (lookahead == 'F') ADVANCE(683);
      if (lookahead == 'L') ADVANCE(505);
      if (lookahead == 'N') ADVANCE(319);
      if (lookahead == 'S') ADVANCE(110);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          ('B' <= lookahead && lookahead <= 'E') ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('G' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 233:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      ADVANCE_MAP(
        '(', 17,
        'E', 315,
        'I', 447,
        'K', 464,
        'P', 257,
        'Q', 507,
        'T', 265,
        'U', 294,
        'Y', 554,
      );
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          lookahead == 'B' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'W') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 234:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(17);
      if (lookahead == 'E') ADVANCE(630);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          lookahead == 'B' ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 235:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(17);
      if (lookahead == 'L') ADVANCE(717);
      if (lookahead == 'R') ADVANCE(741);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          lookahead == 'B' ||
          lookahead == 'E' ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 236:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(17);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (lookahead == '-' ||
          lookahead == 'B' ||
          lookahead == 'E' ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(745);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(236);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 237:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(357);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 238:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(733);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 239:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(728);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 240:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(585);
      if (lookahead == 'F') ADVANCE(127);
      if (lookahead == 'N') ADVANCE(114);
      if (lookahead == 'S') ADVANCE(33);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 241:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(334);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 242:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-') ADVANCE(730);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 243:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '1') ADVANCE(118);
      if (lookahead == '2') ADVANCE(119);
      if (lookahead == '3') ADVANCE(120);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 244:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '1') ADVANCE(62);
      if (lookahead == '2') ADVANCE(63);
      if (lookahead == '3') ADVANCE(64);
      if (lookahead == '4') ADVANCE(65);
      if (lookahead == '5') ADVANCE(66);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 245:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '1') ADVANCE(212);
      if (lookahead == '2') ADVANCE(213);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 246:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      ADVANCE_MAP(
        '(', 20,
        '1', 214,
        '2', 215,
        '3', 216,
        '4', 217,
        '5', 218,
        '6', 219,
        '7', 220,
        '8', 221,
        '9', 222,
      );
      if (lookahead == '-' ||
          lookahead == '0' ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 247:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '1') ADVANCE(59);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 248:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '1') ADVANCE(68);
      if (lookahead == '2') ADVANCE(69);
      if (lookahead == '3') ADVANCE(70);
      if (lookahead == '4') ADVANCE(71);
      if (lookahead == '5') ADVANCE(72);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 249:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(685);
      if (lookahead == 'E') ADVANCE(506);
      if (lookahead == 'F') ADVANCE(450);
      if (lookahead == 'I') ADVANCE(653);
      if (lookahead == 'L') ADVANCE(463);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 250:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(527);
      if (lookahead == 'I') ADVANCE(516);
      if (lookahead == 'R') ADVANCE(590);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 251:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(297);
      if (lookahead == 'E') ADVANCE(614);
      if (lookahead == 'I') ADVANCE(298);
      if (lookahead == 'O') ADVANCE(466);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 252:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(632);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 253:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(524);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 254:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(295);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 255:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(245);
      if (lookahead == 'F') ADVANCE(246);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 256:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(448);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 257:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(313);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 258:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(449);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 259:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(646);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 260:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(335);
      if (lookahead == 'F') ADVANCE(666);
      if (lookahead == 'S') ADVANCE(647);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 261:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(551);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 262:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(519);
      if (lookahead == 'E') ADVANCE(657);
      if (lookahead == 'H') ADVANCE(271);
      if (lookahead == 'I') ADVANCE(539);
      if (lookahead == 'O') ADVANCE(51);
      if (lookahead == 'R') ADVANCE(267);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 263:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(321);
      if (lookahead == 'D') ADVANCE(383);
      if (lookahead == 'M') ADVANCE(286);
      if (lookahead == 'P') ADVANCE(520);
      if (lookahead == 'W') ADVANCE(645);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 264:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(739);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 265:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(636);
      if (lookahead == 'O') ADVANCE(606);
      if (lookahead == 'R') ADVANCE(476);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 266:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(316);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 267:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(471);
      if (lookahead == 'U') ADVANCE(355);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 268:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(306);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 269:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(651);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 270:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(626);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 271:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(547);
      if (lookahead == 'E') ADVANCE(548);
      if (lookahead == 'R') ADVANCE(593);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 272:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(607);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 273:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(509);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 274:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(511);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 275:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(512);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 276:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(528);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 277:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(532);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 278:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(621);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 279:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(513);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 280:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(514);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 281:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(515);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 282:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(468);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 283:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(312);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 284:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(705);
      if (lookahead == 'E') ADVANCE(165);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 285:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(692);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 286:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(479);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 287:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(699);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 288:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(700);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 289:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(701);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 290:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'A') ADVANCE(529);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('B' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 291:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'B') ADVANCE(228);
      if (lookahead == 'K') ADVANCE(229);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 292:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'B') ADVANCE(538);
      if (lookahead == 'C') ADVANCE(525);
      if (lookahead == 'E') ADVANCE(580);
      if (lookahead == 'P') ADVANCE(255);
      if (lookahead == 'R') ADVANCE(387);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 293:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'B') ADVANCE(282);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 294:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'B') ADVANCE(704);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 295:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'B') ADVANCE(416);
      if (lookahead == 'N') ADVANCE(721);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 296:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'B') ADVANCE(274);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 297:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(504);
      if (lookahead == 'R') ADVANCE(258);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('D' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 298:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(46);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 299:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(121);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('D' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 300:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(100);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 301:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(163);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 302:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(126);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 303:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(160);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 304:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(161);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 305:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      ADVANCE_MAP(
        '(', 20,
        'C', 307,
        'F', 113,
        'N', 56,
        'P', 385,
        'R', 208,
        'T', 456,
        'U', 680,
        'V', 381,
      );
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 306:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(369);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 307:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(714);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 308:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(389);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 309:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(670);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 310:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(495);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 311:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(678);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 312:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(679);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 313:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(360);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('D' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 314:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(374);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 315:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(686);
      if (lookahead == 'N') ADVANCE(707);
      if (lookahead == 'P') ADVANCE(259);
      if (lookahead == 'T') ADVANCE(156);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('D' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 316:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(697);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 317:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'C') ADVANCE(420);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 318:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(166);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 319:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(209);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 320:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(237);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 321:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(187);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 322:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(227);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 323:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(226);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 324:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(197);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 325:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(53);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 326:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(173);
      if (lookahead == 'R') ADVANCE(180);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 327:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(105);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 328:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(101);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 329:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(164);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 330:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(162);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 331:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(241);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 332:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(366);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 333:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(409);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 334:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(394);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 335:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(478);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 336:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(485);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 337:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(486);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 338:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(488);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 339:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(491);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 340:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(500);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 341:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'D') ADVANCE(501);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 342:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(423);
      if (lookahead == 'I') ADVANCE(552);
      if (lookahead == 'L') ADVANCE(261);
      if (lookahead == 'Y') ADVANCE(54);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'W') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 343:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(736);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 344:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(260);
      if (lookahead == 'O') ADVANCE(732);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 345:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(735);
      if (lookahead == 'O') ADVANCE(663);
      if (lookahead == 'U') ADVANCE(517);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 346:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(263);
      if (lookahead == 'I') ADVANCE(445);
      if (lookahead == 'U') ADVANCE(544);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 347:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(34);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 348:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(299);
      if (lookahead == 'I') ADVANCE(664);
      if (lookahead == 'T') ADVANCE(351);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 349:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(200);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 350:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(128);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 351:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(559);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 352:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(152);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 353:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(174);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 354:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(202);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 355:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(157);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 356:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(193);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 357:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(729);
      if (lookahead == 'I') ADVANCE(421);
      if (lookahead == 'P') ADVANCE(401);
      if (lookahead == 'S') ADVANCE(709);
      if (lookahead == 'U') ADVANCE(576);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 358:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(158);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 359:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(85);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 360:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(79);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 361:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(57);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 362:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(32);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 363:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(188);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 364:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(141);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 365:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(190);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 366:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(169);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 367:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(122);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 368:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(47);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 369:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(115);
      if (lookahead == 'I') ADVANCE(565);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 370:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(189);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 371:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(146);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 372:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(326);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 373:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(131);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 374:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(148);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 375:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(98);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 376:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(83);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 377:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(81);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 378:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(159);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 379:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(132);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 380:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(734);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 381:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(625);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 382:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(503);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 383:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(428);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 384:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(309);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 385:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(545);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 386:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(616);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 387:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(322);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 388:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(285);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 389:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(609);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 390:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(302);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 391:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(652);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 392:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(331);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 393:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(617);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 394:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(310);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 395:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(549);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 396:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(581);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 397:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(618);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 398:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(327);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 399:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(340);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 400:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(328);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 401:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(644);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 402:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(329);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 403:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(619);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 404:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(330);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 405:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(620);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 406:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(575);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 407:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(622);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 408:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(623);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 409:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(624);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 410:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(382);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 411:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(311);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 412:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(278);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 413:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(631);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 414:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(637);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 415:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(633);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 416:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(688);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 417:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(691);
      if (lookahead == 'I') ADVANCE(542);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 418:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(582);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 419:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(341);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 420:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'E') ADVANCE(583);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 421:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(129);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 422:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(238);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 423:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(594);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 424:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(492);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 425:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(521);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 426:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(595);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 427:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(597);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 428:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'F') ADVANCE(481);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 429:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(170);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 430:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(172);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 431:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(96);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 432:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(138);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 433:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(181);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 434:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(97);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 435:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(178);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 436:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(92);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 437:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(55);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 438:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(112);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 439:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(184);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 440:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(93);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 441:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(177);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 442:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(182);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 443:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(153);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 444:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(459);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 445:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(457);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 446:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(452);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 447:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(546);
      if (lookahead == 'Z') ADVANCE(353);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Y') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 448:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(361);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 449:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'G') ADVANCE(635);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 450:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(292);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 451:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(139);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 452:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(91);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 453:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(145);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 454:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(252);
      if (lookahead == 'L') ADVANCE(601);
      if (lookahead == 'O') ADVANCE(533);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 455:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(254);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 456:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(393);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 457:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(673);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 458:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(395);
      if (lookahead == 'I') ADVANCE(681);
      if (lookahead == 'R') ADVANCE(497);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 459:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'H') ADVANCE(242);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 460:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      ADVANCE_MAP(
        '(', 20,
        'I', 293,
        'J', 384,
        'L', 656,
        'N', 320,
        'Q', 713,
        'V', 253,
        'X', 348,
      );
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 461:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(727);
      if (lookahead == 'L') ADVANCE(600);
      if (lookahead == 'O') ADVANCE(143);
      if (lookahead == 'R') ADVANCE(388);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 462:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(444);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 463:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(125);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 464:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(605);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 465:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(332);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 466:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(578);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 467:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(301);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 468:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(323);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 469:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(303);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 470:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(596);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 471:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(530);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 472:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(304);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 473:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(510);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 474:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(553);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 475:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(602);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 476:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(555);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 477:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(573);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 478:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(556);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 479:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(574);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 480:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(557);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 481:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(572);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 482:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(558);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 483:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(560);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 484:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(561);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 485:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(562);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 486:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(563);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 487:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(567);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 488:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(568);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 489:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(569);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 490:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(570);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 491:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(571);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 492:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(398);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 493:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(744);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 494:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(608);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 495:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(540);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 496:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(275);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 497:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(690);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 498:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(696);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 499:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(698);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 500:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(702);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 501:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'I') ADVANCE(703);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 502:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'K') ADVANCE(106);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 503:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'K') ADVANCE(203);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 504:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'K') ADVANCE(392);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 505:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(89);
      if (lookahead == 'P') ADVANCE(455);
      if (lookahead == 'S') ADVANCE(586);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 506:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(417);
      if (lookahead == 'P') ADVANCE(418);
      if (lookahead == 'S') ADVANCE(317);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 507:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(123);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 508:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(87);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 509:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(204);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 510:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(137);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 511:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(109);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 512:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(186);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 513:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(108);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 514:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(67);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 515:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(73);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 516:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(523);
      if (lookahead == 'R') ADVANCE(659);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 517:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(508);
      if (lookahead == 'M') ADVANCE(413);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 518:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(740);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 519:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(531);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 520:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(268);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 521:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(591);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 522:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(264);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 523:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(397);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 524:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(724);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 525:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(412);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 526:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(684);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 527:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(661);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 528:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(719);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 529:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(720);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 530:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(483);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 531:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(742);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 532:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'L') ADVANCE(725);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 533:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(604);
      if (lookahead == 'N') ADVANCE(706);
      if (lookahead == 'P') ADVANCE(737);
      if (lookahead == 'R') ADVANCE(615);
      if (lookahead == 'U') ADVANCE(564);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 534:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(199);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 535:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(135);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 536:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(136);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 537:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(649);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 538:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(269);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 539:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(354);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 540:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(281);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 541:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(415);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 542:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'M') ADVANCE(499);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 543:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(658);
      if (lookahead == 'S') ADVANCE(256);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 544:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(151);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 545:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(192);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 546:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(95);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 547:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(207);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 548:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(130);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 549:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(107);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 550:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(144);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 551:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(502);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 552:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(270);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 553:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(429);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 554:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(300);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 555:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(430);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 556:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(431);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 557:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(432);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 558:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(433);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 559:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(324);
      if (lookahead == 'R') ADVANCE(577);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 560:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(434);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 561:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(435);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 562:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(436);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 563:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(437);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 564:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(669);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 565:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(438);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 566:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(493);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 567:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(439);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 568:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(440);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 569:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(441);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 570:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(442);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 571:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(443);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 572:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(391);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 573:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(718);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 574:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(333);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 575:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(314);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 576:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(662);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 577:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(279);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 578:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(693);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 579:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(280);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 580:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(694);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 581:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(336);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 582:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(337);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 583:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(338);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 584:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'N') ADVANCE(339);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 585:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(196);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 586:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(134);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 587:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(155);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 588:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(76);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 589:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(726);
      if (lookahead == 'U') ADVANCE(526);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 590:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(534);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 591:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(731);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 592:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(422);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 593:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(723);
      if (lookahead == 'U') ADVANCE(90);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 594:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(638);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 595:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(628);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 596:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(550);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 597:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(629);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 598:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(566);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 599:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(689);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 600:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(296);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 601:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(660);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 602:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(579);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 603:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'O') ADVANCE(584);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 604:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(61);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 605:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(243);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 606:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(150);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 607:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(453);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 608:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(518);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 609:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(675);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 610:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(716);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 611:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(522);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 612:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(603);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 613:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'P') ADVANCE(411);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 614:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(426);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 615:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(154);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 616:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(142);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 617:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(133);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 618:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(45);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 619:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(205);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 620:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(75);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 621:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(211);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 622:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(210);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 623:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(99);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 624:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(171);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 625:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(425);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 626:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(738);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 627:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(648);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 628:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(535);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 629:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(536);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 630:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(588);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 631:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(467);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 632:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(266);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 633:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(472);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 634:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(283);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 635:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(272);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 636:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(674);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 637:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(708);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 638:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(364);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 639:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(368);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 640:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(598);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 641:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(484);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 642:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(489);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 643:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(490);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 644:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(427);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 645:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(498);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 646:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'R') ADVANCE(288);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 647:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(206);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 648:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(49);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 649:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(124);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 650:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(78);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 651:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(291);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 652:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(52);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 653:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(611);
      if (lookahead == 'V') ADVANCE(465);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 654:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(665);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 655:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(612);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 656:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(350);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 657:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(668);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 658:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(687);
      if (lookahead == 'T') ADVANCE(473);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 659:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(671);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 660:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(356);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 661:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(358);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 662:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'S') ADVANCE(710);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 663:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(176);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 664:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(149);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 665:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(104);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 666:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(102);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 667:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(147);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 668:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(140);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 669:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(179);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 670:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(117);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 671:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(185);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 672:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(194);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 673:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(103);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 674:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(191);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 675:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(198);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 676:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(284);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 677:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(195);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 678:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(183);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 679:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(167);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 680:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(610);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 681:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(451);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 682:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(496);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 683:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(386);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 684:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(494);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 685:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(349);
      if (lookahead == 'Y') ADVANCE(201);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 686:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(470);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 687:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(641);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 688:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(469);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 689:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(359);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 690:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(363);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 691:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(365);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 692:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(403);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 693:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(405);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 694:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(407);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 695:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(367);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 696:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(370);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 697:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(408);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 698:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(372);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 699:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(373);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 700:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(375);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 701:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(379);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 702:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(402);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 703:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(404);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 704:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(634);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 705:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(475);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 706:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(477);
      if (lookahead == 'V') ADVANCE(414);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 707:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(406);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 708:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(487);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 709:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(642);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 710:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'T') ADVANCE(643);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 711:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(654);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 712:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(599);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 713:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(273);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 714:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(627);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 715:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(672);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 716:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(677);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 717:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(362);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 718:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(371);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 719:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(376);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 720:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(377);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 721:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(541);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 722:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(639);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 723:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(446);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 724:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(287);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 725:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'U') ADVANCE(289);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 726:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'V') ADVANCE(352);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 727:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'V') ADVANCE(474);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 728:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'V') ADVANCE(276);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 729:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'V') ADVANCE(277);
      if (lookahead == 'X') ADVANCE(390);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 730:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'V') ADVANCE(290);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 731:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'W') ADVANCE(175);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 732:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'W') ADVANCE(239);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 733:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'W') ADVANCE(410);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 734:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'X') ADVANCE(74);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 735:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'X') ADVANCE(667);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 736:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(94);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 737:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(111);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 738:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(60);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 739:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(58);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 740:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(168);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 741:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(480);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 742:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Y') ADVANCE(482);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 743:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Z') ADVANCE(378);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Y') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 744:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == 'Z') ADVANCE(400);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Y') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 745:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= ',') ||
          lookahead == '/') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(745);
      if (('1' <= lookahead && lookahead <= '8') ||
          ('C' <= lookahead && lookahead <= 'Y') ||
          ('c' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 746:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      if (lookahead == '(') ADVANCE(20);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(746);
      END_STATE();
    case 747:
      ACCEPT_TOKEN(aux_sym_identifier_token1);
      ADVANCE_MAP(
        '(', 761,
        ')', 762,
        '0', 747,
        '9', 747,
        'A', 747,
        'S', 747,
        'V', 747,
        'X', 747,
        'Z', 747,
        'a', 747,
        's', 747,
        'v', 747,
        'x', 747,
        'z', 747,
      );
      if (lookahead == '-' ||
          ('1' <= lookahead && lookahead <= '8') ||
          ('B' <= lookahead && lookahead <= 'Y') ||
          ('b' <= lookahead && lookahead <= 'y')) ADVANCE(746);
      END_STATE();
    case 748:
      ACCEPT_TOKEN(aux_sym_identifier_token2);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(748);
      END_STATE();
    case 749:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0') ADVANCE(754);
      if (lookahead == '9') ADVANCE(35);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(37);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 750:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0') ADVANCE(756);
      if (lookahead == '9') ADVANCE(36);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(38);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 751:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(26);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(27);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 752:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(753);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(774);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 753:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(751);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(773);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 754:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(752);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(775);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 755:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(754);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(776);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 756:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(756);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(779);
      if ((set_contains(sym_picture_string_character_set_3, 13, lookahead)) &&
          lookahead != '(' &&
          lookahead != ')') ADVANCE(757);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(763);
      END_STATE();
    case 757:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '(') ADVANCE(16);
      if (lookahead == '$' ||
          ('*' <= lookahead && lookahead <= '-') ||
          lookahead == '/' ||
          lookahead == 'B' ||
          lookahead == 'E' ||
          lookahead == 'P' ||
          lookahead == 'b' ||
          lookahead == 'e' ||
          lookahead == 'p') ADVANCE(763);
      if (set_contains(sym_picture_string_character_set_2, 19, lookahead)) ADVANCE(757);
      END_STATE();
    case 758:
      ACCEPT_TOKEN(sym_picture_string);
      ADVANCE_MAP(
        '(', 762,
        ')', 747,
        '0', 758,
        '9', 758,
        'A', 758,
        'S', 758,
        'V', 758,
        'X', 758,
        'Z', 758,
        'a', 758,
        's', 758,
        'v', 758,
        'x', 758,
        'z', 758,
      );
      if (lookahead == '-' ||
          ('1' <= lookahead && lookahead <= '8') ||
          ('B' <= lookahead && lookahead <= 'Y') ||
          ('b' <= lookahead && lookahead <= 'y')) ADVANCE(7);
      END_STATE();
    case 759:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(759);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(779);
      if (set_contains(sym_picture_string_character_set_1, 18, lookahead)) ADVANCE(763);
      END_STATE();
    case 760:
      ACCEPT_TOKEN(sym_picture_string);
      if (lookahead == '0' ||
          lookahead == '9') ADVANCE(759);
      if (('1' <= lookahead && lookahead <= '8')) ADVANCE(779);
      if (set_contains(sym_picture_string_character_set_1, 18, lookahead)) ADVANCE(763);
      END_STATE();
    case 761:
      ACCEPT_TOKEN(sym_picture_string);
      ADVANCE_MAP(
        '(', 762,
        ')', 762,
        '0', 758,
        '9', 758,
        'A', 758,
        'S', 758,
        'V', 758,
        'X', 758,
        'Z', 758,
        'a', 758,
        's', 758,
        'v', 758,
        'x', 758,
        'z', 758,
      );
      if (lookahead == '-' ||
          ('1' <= lookahead && lookahead <= '8') ||
          ('B' <= lookahead && lookahead <= 'Y') ||
          ('b' <= lookahead && lookahead <= 'y')) ADVANCE(7);
      END_STATE();
    case 762:
      ACCEPT_TOKEN(sym_picture_string);
      ADVANCE_MAP(
        '(', 762,
        ')', 762,
        '0', 762,
        '9', 762,
        'A', 762,
        'S', 762,
        'V', 762,
        'X', 762,
        'Z', 762,
        'a', 762,
        's', 762,
        'v', 762,
        'x', 762,
        'z', 762,
      );
      END_STATE();
    case 763:
      ACCEPT_TOKEN(sym_picture_string);
      if (set_contains(sym_picture_string_character_set_1, 18, lookahead)) ADVANCE(763);
      END_STATE();
    case 764:
      ACCEPT_TOKEN(aux_sym_string_literal_token1);
      END_STATE();
    case 765:
      ACCEPT_TOKEN(aux_sym_string_literal_token2);
      END_STATE();
    case 766:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '6') ADVANCE(41);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(776);
      END_STATE();
    case 767:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '6') ADVANCE(42);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 768:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '7') ADVANCE(43);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(776);
      END_STATE();
    case 769:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '7') ADVANCE(44);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 770:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '8') ADVANCE(29);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(776);
      END_STATE();
    case 771:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (lookahead == '8') ADVANCE(30);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 772:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(39);
      END_STATE();
    case 773:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(27);
      END_STATE();
    case 774:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(773);
      END_STATE();
    case 775:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(774);
      END_STATE();
    case 776:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(775);
      END_STATE();
    case 777:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(40);
      END_STATE();
    case 778:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(776);
      END_STATE();
    case 779:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(780);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(779);
      END_STATE();
    case 780:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(780);
      END_STATE();
    case 781:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      END_STATE();
    case 782:
      ACCEPT_TOKEN(anon_sym_EQ);
      if (lookahead == '=') ADVANCE(781);
      END_STATE();
    case 783:
      ACCEPT_TOKEN(anon_sym_GT);
      if (lookahead == '=') ADVANCE(785);
      END_STATE();
    case 784:
      ACCEPT_TOKEN(anon_sym_LT);
      if (lookahead == '=') ADVANCE(786);
      END_STATE();
    case 785:
      ACCEPT_TOKEN(anon_sym_GT_EQ);
      END_STATE();
    case 786:
      ACCEPT_TOKEN(anon_sym_LT_EQ);
      END_STATE();
    case 787:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 788:
      ACCEPT_TOKEN(anon_sym_COMMA);
      if (set_contains(sym_picture_string_character_set_1, 18, lookahead)) ADVANCE(763);
      END_STATE();
    case 789:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(8);
      END_STATE();
    case 790:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 791:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 21},
  [2] = {.lex_state = 21},
  [3] = {.lex_state = 21},
  [4] = {.lex_state = 1},
  [5] = {.lex_state = 3},
  [6] = {.lex_state = 3},
  [7] = {.lex_state = 21},
  [8] = {.lex_state = 3},
  [9] = {.lex_state = 21},
  [10] = {.lex_state = 21},
  [11] = {.lex_state = 21},
  [12] = {.lex_state = 21},
  [13] = {.lex_state = 21},
  [14] = {.lex_state = 1},
  [15] = {.lex_state = 2},
  [16] = {.lex_state = 3},
  [17] = {.lex_state = 3},
  [18] = {.lex_state = 3},
  [19] = {.lex_state = 3},
  [20] = {.lex_state = 3},
  [21] = {.lex_state = 3},
  [22] = {.lex_state = 3},
  [23] = {.lex_state = 3},
  [24] = {.lex_state = 3},
  [25] = {.lex_state = 4},
  [26] = {.lex_state = 4},
  [27] = {.lex_state = 4},
  [28] = {.lex_state = 4},
  [29] = {.lex_state = 4},
  [30] = {.lex_state = 0},
  [31] = {.lex_state = 0},
  [32] = {.lex_state = 15},
  [33] = {.lex_state = 0},
  [34] = {.lex_state = 15},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [aux_sym_newline_token1] = ACTIONS(1),
    [aux_sym_comment_line_token1] = ACTIONS(1),
    [sym_sequence_number] = ACTIONS(1),
    [anon_sym_DOT] = ACTIONS(1),
    [anon_sym_88] = ACTIONS(1),
    [anon_sym_VALUE] = ACTIONS(1),
    [anon_sym_IS] = ACTIONS(1),
    [anon_sym_ARE] = ACTIONS(1),
    [aux_sym_level_number_token1] = ACTIONS(1),
    [aux_sym_level_number_token2] = ACTIONS(1),
    [anon_sym_66] = ACTIONS(1),
    [anon_sym_77] = ACTIONS(1),
    [anon_sym_FILLER] = ACTIONS(1),
    [anon_sym_PIC] = ACTIONS(1),
    [anon_sym_PICTURE] = ACTIONS(1),
    [anon_sym_VALUES] = ACTIONS(1),
    [anon_sym_OCCURS] = ACTIONS(1),
    [anon_sym_TIMES] = ACTIONS(1),
    [anon_sym_TO] = ACTIONS(1),
    [anon_sym_REDEFINES] = ACTIONS(1),
    [anon_sym_INDEXED] = ACTIONS(1),
    [anon_sym_BY] = ACTIONS(1),
    [anon_sym_DEPENDING] = ACTIONS(1),
    [anon_sym_ON] = ACTIONS(1),
    [anon_sym_USAGE] = ACTIONS(1),
    [anon_sym_DISPLAY] = ACTIONS(1),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(1),
    [anon_sym_BINARY] = ACTIONS(1),
    [anon_sym_COMP] = ACTIONS(1),
    [anon_sym_COMP_DASH1] = ACTIONS(1),
    [anon_sym_COMP_DASH2] = ACTIONS(1),
    [anon_sym_COMP_DASH3] = ACTIONS(1),
    [anon_sym_COMP_DASH4] = ACTIONS(1),
    [anon_sym_COMP_DASH5] = ACTIONS(1),
    [anon_sym_COMPUTATIONAL] = ACTIONS(1),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(1),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(1),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(1),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(1),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(1),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(1),
    [anon_sym_INDEX] = ACTIONS(1),
    [anon_sym_POINTER] = ACTIONS(1),
    [anon_sym_ZERO] = ACTIONS(1),
    [anon_sym_ZEROS] = ACTIONS(1),
    [anon_sym_ZEROES] = ACTIONS(1),
    [anon_sym_SPACE] = ACTIONS(1),
    [anon_sym_SPACES] = ACTIONS(1),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(1),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(1),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(1),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(1),
    [anon_sym_QUOTE] = ACTIONS(1),
    [anon_sym_QUOTES] = ACTIONS(1),
    [anon_sym_NULL] = ACTIONS(1),
    [anon_sym_NULLS] = ACTIONS(1),
    [anon_sym_ALL] = ACTIONS(1),
    [anon_sym_THRU] = ACTIONS(1),
    [anon_sym_THROUGH] = ACTIONS(1),
    [anon_sym_ASCENDING] = ACTIONS(1),
    [anon_sym_DESCENDING] = ACTIONS(1),
    [anon_sym_KEY] = ACTIONS(1),
    [anon_sym_SIGN] = ACTIONS(1),
    [anon_sym_LEADING] = ACTIONS(1),
    [anon_sym_TRAILING] = ACTIONS(1),
    [anon_sym_SEPARATE] = ACTIONS(1),
    [anon_sym_CHARACTER] = ACTIONS(1),
    [anon_sym_SYNC] = ACTIONS(1),
    [anon_sym_SYNCHRONIZED] = ACTIONS(1),
    [anon_sym_LEFT] = ACTIONS(1),
    [anon_sym_RIGHT] = ACTIONS(1),
    [anon_sym_JUST] = ACTIONS(1),
    [anon_sym_JUSTIFIED] = ACTIONS(1),
    [anon_sym_BLANK] = ACTIONS(1),
    [anon_sym_WHEN] = ACTIONS(1),
    [anon_sym_EXTERNAL] = ACTIONS(1),
    [anon_sym_GLOBAL] = ACTIONS(1),
    [anon_sym_AS] = ACTIONS(1),
    [anon_sym_COPY] = ACTIONS(1),
    [anon_sym_REPLACING] = ACTIONS(1),
    [anon_sym_OF] = ACTIONS(1),
    [anon_sym_IN] = ACTIONS(1),
    [anon_sym_REPLACE] = ACTIONS(1),
    [anon_sym_OFF] = ACTIONS(1),
    [anon_sym_EJECT] = ACTIONS(1),
    [anon_sym_SKIP1] = ACTIONS(1),
    [anon_sym_SKIP2] = ACTIONS(1),
    [anon_sym_SKIP3] = ACTIONS(1),
    [anon_sym_EXEC] = ACTIONS(1),
    [anon_sym_EXECUTE] = ACTIONS(1),
    [anon_sym_SQL] = ACTIONS(1),
    [anon_sym_SQLIMS] = ACTIONS(1),
    [anon_sym_DLI] = ACTIONS(1),
    [anon_sym_END_DASHEXEC] = ACTIONS(1),
    [anon_sym_IF] = ACTIONS(1),
    [anon_sym_ELSE] = ACTIONS(1),
    [anon_sym_END_DASHIF] = ACTIONS(1),
    [anon_sym_THEN] = ACTIONS(1),
    [anon_sym_EVALUATE] = ACTIONS(1),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(1),
    [anon_sym_OTHER] = ACTIONS(1),
    [anon_sym_ALSO] = ACTIONS(1),
    [anon_sym_PERFORM] = ACTIONS(1),
    [anon_sym_END_DASHPERFORM] = ACTIONS(1),
    [anon_sym_UNTIL] = ACTIONS(1),
    [anon_sym_VARYING] = ACTIONS(1),
    [anon_sym_WITH] = ACTIONS(1),
    [anon_sym_TEST] = ACTIONS(1),
    [anon_sym_BEFORE] = ACTIONS(1),
    [anon_sym_AFTER] = ACTIONS(1),
    [anon_sym_GO] = ACTIONS(1),
    [anon_sym_SECTION] = ACTIONS(1),
    [anon_sym_PARAGRAPH] = ACTIONS(1),
    [anon_sym_CONTINUE] = ACTIONS(1),
    [anon_sym_NEXT] = ACTIONS(1),
    [anon_sym_SENTENCE] = ACTIONS(1),
    [anon_sym_EXIT] = ACTIONS(1),
    [anon_sym_STOP] = ACTIONS(1),
    [anon_sym_RUN] = ACTIONS(1),
    [anon_sym_MOVE] = ACTIONS(1),
    [anon_sym_CORRESPONDING] = ACTIONS(1),
    [anon_sym_CORR] = ACTIONS(1),
    [anon_sym_INTO] = ACTIONS(1),
    [anon_sym_SET] = ACTIONS(1),
    [anon_sym_TRUE] = ACTIONS(1),
    [anon_sym_FALSE] = ACTIONS(1),
    [anon_sym_INITIALIZE] = ACTIONS(1),
    [anon_sym_ALPHABETIC] = ACTIONS(1),
    [anon_sym_ALPHANUMERIC] = ACTIONS(1),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(1),
    [anon_sym_NUMERIC] = ACTIONS(1),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(1),
    [anon_sym_COMPUTE] = ACTIONS(1),
    [anon_sym_ADD] = ACTIONS(1),
    [anon_sym_SUBTRACT] = ACTIONS(1),
    [anon_sym_MULTIPLY] = ACTIONS(1),
    [anon_sym_DIVIDE] = ACTIONS(1),
    [anon_sym_GIVING] = ACTIONS(1),
    [anon_sym_REMAINDER] = ACTIONS(1),
    [anon_sym_STRING] = ACTIONS(1),
    [anon_sym_DELIMITED] = ACTIONS(1),
    [anon_sym_SIZE] = ACTIONS(1),
    [anon_sym_OVERFLOW] = ACTIONS(1),
    [anon_sym_NOT] = ACTIONS(1),
    [anon_sym_END_DASHSTRING] = ACTIONS(1),
    [anon_sym_UNSTRING] = ACTIONS(1),
    [anon_sym_COUNT] = ACTIONS(1),
    [anon_sym_DELIMITER] = ACTIONS(1),
    [anon_sym_TALLYING] = ACTIONS(1),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(1),
    [anon_sym_INSPECT] = ACTIONS(1),
    [anon_sym_CONVERTING] = ACTIONS(1),
    [anon_sym_FIRST] = ACTIONS(1),
    [anon_sym_INITIAL] = ACTIONS(1),
    [anon_sym_READ] = ACTIONS(1),
    [anon_sym_WRITE] = ACTIONS(1),
    [anon_sym_REWRITE] = ACTIONS(1),
    [anon_sym_DELETE] = ACTIONS(1),
    [anon_sym_START] = ACTIONS(1),
    [anon_sym_OPEN] = ACTIONS(1),
    [anon_sym_CLOSE] = ACTIONS(1),
    [anon_sym_INPUT] = ACTIONS(1),
    [anon_sym_OUTPUT] = ACTIONS(1),
    [anon_sym_I_DASHO] = ACTIONS(1),
    [anon_sym_EXTEND] = ACTIONS(1),
    [anon_sym_ACCEPT] = ACTIONS(1),
    [anon_sym_FROM] = ACTIONS(1),
    [anon_sym_DATE] = ACTIONS(1),
    [anon_sym_DAY] = ACTIONS(1),
    [anon_sym_TIME] = ACTIONS(1),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(1),
    [anon_sym_EQUAL] = ACTIONS(1),
    [anon_sym_GREATER] = ACTIONS(1),
    [anon_sym_LESS] = ACTIONS(1),
    [anon_sym_THAN] = ACTIONS(1),
    [anon_sym_OR] = ACTIONS(1),
    [anon_sym_AND] = ACTIONS(1),
    [anon_sym_DFHENTER] = ACTIONS(1),
    [anon_sym_DFHCLEAR] = ACTIONS(1),
    [anon_sym_DFHPA1] = ACTIONS(1),
    [anon_sym_DFHPA2] = ACTIONS(1),
    [anon_sym_DFHPF1] = ACTIONS(1),
    [anon_sym_DFHPF2] = ACTIONS(1),
    [anon_sym_DFHPF3] = ACTIONS(1),
    [anon_sym_DFHPF4] = ACTIONS(1),
    [anon_sym_DFHPF5] = ACTIONS(1),
    [anon_sym_DFHPF6] = ACTIONS(1),
    [anon_sym_DFHPF7] = ACTIONS(1),
    [anon_sym_DFHPF8] = ACTIONS(1),
    [anon_sym_DFHPF9] = ACTIONS(1),
    [anon_sym_DFHPF10] = ACTIONS(1),
    [anon_sym_DFHPF11] = ACTIONS(1),
    [anon_sym_DFHPF12] = ACTIONS(1),
    [anon_sym_EIBAID] = ACTIONS(1),
    [anon_sym_DFHRED] = ACTIONS(1),
    [anon_sym_DFHBMASB] = ACTIONS(1),
    [anon_sym_DFHBMASK] = ACTIONS(1),
    [aux_sym_identifier_token1] = ACTIONS(1),
    [aux_sym_identifier_token2] = ACTIONS(1),
    [sym_picture_string] = ACTIONS(1),
    [aux_sym_string_literal_token1] = ACTIONS(1),
    [aux_sym_string_literal_token2] = ACTIONS(1),
    [sym_number] = ACTIONS(1),
    [anon_sym_EQ_EQ] = ACTIONS(1),
    [anon_sym_EQ] = ACTIONS(1),
    [anon_sym_GT] = ACTIONS(1),
    [anon_sym_LT] = ACTIONS(1),
    [anon_sym_GT_EQ] = ACTIONS(1),
    [anon_sym_LT_EQ] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
  },
  [1] = {
    [sym_source_file] = STATE(30),
    [sym_newline] = STATE(2),
    [sym_comment_line] = STATE(2),
    [sym_statement] = STATE(2),
    [sym_statement_body] = STATE(31),
    [sym_embedded_comment] = STATE(5),
    [sym_continuation_newline] = STATE(5),
    [sym_level_88_condition] = STATE(5),
    [sym_level_number] = STATE(5),
    [sym_keyword] = STATE(5),
    [sym_identifier] = STATE(5),
    [sym_string_literal] = STATE(5),
    [sym_operator] = STATE(5),
    [sym_parenthesized] = STATE(5),
    [aux_sym_source_file_repeat1] = STATE(2),
    [aux_sym_statement_body_repeat1] = STATE(5),
    [ts_builtin_sym_end] = ACTIONS(3),
    [aux_sym_newline_token1] = ACTIONS(5),
    [aux_sym_comment_line_token1] = ACTIONS(7),
    [sym_sequence_number] = ACTIONS(9),
    [anon_sym_DOT] = ACTIONS(11),
    [anon_sym_88] = ACTIONS(13),
    [anon_sym_VALUE] = ACTIONS(15),
    [anon_sym_IS] = ACTIONS(15),
    [aux_sym_level_number_token1] = ACTIONS(17),
    [aux_sym_level_number_token2] = ACTIONS(17),
    [anon_sym_66] = ACTIONS(17),
    [anon_sym_77] = ACTIONS(17),
    [anon_sym_FILLER] = ACTIONS(15),
    [anon_sym_PIC] = ACTIONS(15),
    [anon_sym_PICTURE] = ACTIONS(15),
    [anon_sym_VALUES] = ACTIONS(15),
    [anon_sym_OCCURS] = ACTIONS(15),
    [anon_sym_TIMES] = ACTIONS(15),
    [anon_sym_TO] = ACTIONS(15),
    [anon_sym_REDEFINES] = ACTIONS(15),
    [anon_sym_INDEXED] = ACTIONS(15),
    [anon_sym_BY] = ACTIONS(15),
    [anon_sym_DEPENDING] = ACTIONS(15),
    [anon_sym_ON] = ACTIONS(15),
    [anon_sym_USAGE] = ACTIONS(15),
    [anon_sym_DISPLAY] = ACTIONS(15),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(15),
    [anon_sym_BINARY] = ACTIONS(15),
    [anon_sym_COMP] = ACTIONS(15),
    [anon_sym_COMP_DASH1] = ACTIONS(15),
    [anon_sym_COMP_DASH2] = ACTIONS(15),
    [anon_sym_COMP_DASH3] = ACTIONS(15),
    [anon_sym_COMP_DASH4] = ACTIONS(15),
    [anon_sym_COMP_DASH5] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(15),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(15),
    [anon_sym_INDEX] = ACTIONS(15),
    [anon_sym_POINTER] = ACTIONS(15),
    [anon_sym_ZERO] = ACTIONS(15),
    [anon_sym_ZEROS] = ACTIONS(15),
    [anon_sym_ZEROES] = ACTIONS(15),
    [anon_sym_SPACE] = ACTIONS(15),
    [anon_sym_SPACES] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(15),
    [anon_sym_QUOTE] = ACTIONS(15),
    [anon_sym_QUOTES] = ACTIONS(15),
    [anon_sym_NULL] = ACTIONS(15),
    [anon_sym_NULLS] = ACTIONS(15),
    [anon_sym_ALL] = ACTIONS(15),
    [anon_sym_THRU] = ACTIONS(15),
    [anon_sym_THROUGH] = ACTIONS(15),
    [anon_sym_ASCENDING] = ACTIONS(15),
    [anon_sym_DESCENDING] = ACTIONS(15),
    [anon_sym_KEY] = ACTIONS(15),
    [anon_sym_SIGN] = ACTIONS(15),
    [anon_sym_LEADING] = ACTIONS(15),
    [anon_sym_TRAILING] = ACTIONS(15),
    [anon_sym_SEPARATE] = ACTIONS(15),
    [anon_sym_CHARACTER] = ACTIONS(15),
    [anon_sym_SYNC] = ACTIONS(15),
    [anon_sym_SYNCHRONIZED] = ACTIONS(15),
    [anon_sym_LEFT] = ACTIONS(15),
    [anon_sym_RIGHT] = ACTIONS(15),
    [anon_sym_JUST] = ACTIONS(15),
    [anon_sym_JUSTIFIED] = ACTIONS(15),
    [anon_sym_BLANK] = ACTIONS(15),
    [anon_sym_WHEN] = ACTIONS(15),
    [anon_sym_EXTERNAL] = ACTIONS(15),
    [anon_sym_GLOBAL] = ACTIONS(15),
    [anon_sym_AS] = ACTIONS(15),
    [anon_sym_COPY] = ACTIONS(15),
    [anon_sym_REPLACING] = ACTIONS(15),
    [anon_sym_OF] = ACTIONS(15),
    [anon_sym_IN] = ACTIONS(15),
    [anon_sym_REPLACE] = ACTIONS(15),
    [anon_sym_OFF] = ACTIONS(15),
    [anon_sym_EJECT] = ACTIONS(15),
    [anon_sym_SKIP1] = ACTIONS(15),
    [anon_sym_SKIP2] = ACTIONS(15),
    [anon_sym_SKIP3] = ACTIONS(15),
    [anon_sym_EXEC] = ACTIONS(15),
    [anon_sym_EXECUTE] = ACTIONS(15),
    [anon_sym_SQL] = ACTIONS(15),
    [anon_sym_SQLIMS] = ACTIONS(15),
    [anon_sym_DLI] = ACTIONS(15),
    [anon_sym_END_DASHEXEC] = ACTIONS(15),
    [anon_sym_IF] = ACTIONS(15),
    [anon_sym_ELSE] = ACTIONS(15),
    [anon_sym_END_DASHIF] = ACTIONS(15),
    [anon_sym_THEN] = ACTIONS(15),
    [anon_sym_EVALUATE] = ACTIONS(15),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(15),
    [anon_sym_OTHER] = ACTIONS(15),
    [anon_sym_ALSO] = ACTIONS(15),
    [anon_sym_PERFORM] = ACTIONS(15),
    [anon_sym_END_DASHPERFORM] = ACTIONS(15),
    [anon_sym_UNTIL] = ACTIONS(15),
    [anon_sym_VARYING] = ACTIONS(15),
    [anon_sym_WITH] = ACTIONS(15),
    [anon_sym_TEST] = ACTIONS(15),
    [anon_sym_BEFORE] = ACTIONS(15),
    [anon_sym_AFTER] = ACTIONS(15),
    [anon_sym_GO] = ACTIONS(15),
    [anon_sym_SECTION] = ACTIONS(15),
    [anon_sym_PARAGRAPH] = ACTIONS(15),
    [anon_sym_CONTINUE] = ACTIONS(15),
    [anon_sym_NEXT] = ACTIONS(15),
    [anon_sym_SENTENCE] = ACTIONS(15),
    [anon_sym_EXIT] = ACTIONS(15),
    [anon_sym_STOP] = ACTIONS(15),
    [anon_sym_RUN] = ACTIONS(15),
    [anon_sym_MOVE] = ACTIONS(15),
    [anon_sym_CORRESPONDING] = ACTIONS(15),
    [anon_sym_CORR] = ACTIONS(15),
    [anon_sym_INTO] = ACTIONS(15),
    [anon_sym_SET] = ACTIONS(15),
    [anon_sym_TRUE] = ACTIONS(15),
    [anon_sym_FALSE] = ACTIONS(15),
    [anon_sym_INITIALIZE] = ACTIONS(15),
    [anon_sym_ALPHABETIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_NUMERIC] = ACTIONS(15),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_COMPUTE] = ACTIONS(15),
    [anon_sym_ADD] = ACTIONS(15),
    [anon_sym_SUBTRACT] = ACTIONS(15),
    [anon_sym_MULTIPLY] = ACTIONS(15),
    [anon_sym_DIVIDE] = ACTIONS(15),
    [anon_sym_GIVING] = ACTIONS(15),
    [anon_sym_REMAINDER] = ACTIONS(15),
    [anon_sym_STRING] = ACTIONS(15),
    [anon_sym_DELIMITED] = ACTIONS(15),
    [anon_sym_SIZE] = ACTIONS(15),
    [anon_sym_OVERFLOW] = ACTIONS(15),
    [anon_sym_NOT] = ACTIONS(15),
    [anon_sym_END_DASHSTRING] = ACTIONS(15),
    [anon_sym_UNSTRING] = ACTIONS(15),
    [anon_sym_COUNT] = ACTIONS(15),
    [anon_sym_DELIMITER] = ACTIONS(15),
    [anon_sym_TALLYING] = ACTIONS(15),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(15),
    [anon_sym_INSPECT] = ACTIONS(15),
    [anon_sym_CONVERTING] = ACTIONS(15),
    [anon_sym_FIRST] = ACTIONS(15),
    [anon_sym_INITIAL] = ACTIONS(15),
    [anon_sym_READ] = ACTIONS(15),
    [anon_sym_WRITE] = ACTIONS(15),
    [anon_sym_REWRITE] = ACTIONS(15),
    [anon_sym_DELETE] = ACTIONS(15),
    [anon_sym_START] = ACTIONS(15),
    [anon_sym_OPEN] = ACTIONS(15),
    [anon_sym_CLOSE] = ACTIONS(15),
    [anon_sym_INPUT] = ACTIONS(15),
    [anon_sym_OUTPUT] = ACTIONS(15),
    [anon_sym_I_DASHO] = ACTIONS(15),
    [anon_sym_EXTEND] = ACTIONS(15),
    [anon_sym_ACCEPT] = ACTIONS(15),
    [anon_sym_FROM] = ACTIONS(15),
    [anon_sym_DATE] = ACTIONS(15),
    [anon_sym_DAY] = ACTIONS(15),
    [anon_sym_TIME] = ACTIONS(15),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(15),
    [anon_sym_EQUAL] = ACTIONS(15),
    [anon_sym_GREATER] = ACTIONS(15),
    [anon_sym_LESS] = ACTIONS(15),
    [anon_sym_THAN] = ACTIONS(15),
    [anon_sym_OR] = ACTIONS(15),
    [anon_sym_AND] = ACTIONS(15),
    [anon_sym_DFHENTER] = ACTIONS(15),
    [anon_sym_DFHCLEAR] = ACTIONS(15),
    [anon_sym_DFHPA1] = ACTIONS(15),
    [anon_sym_DFHPA2] = ACTIONS(15),
    [anon_sym_DFHPF1] = ACTIONS(15),
    [anon_sym_DFHPF2] = ACTIONS(15),
    [anon_sym_DFHPF3] = ACTIONS(15),
    [anon_sym_DFHPF4] = ACTIONS(15),
    [anon_sym_DFHPF5] = ACTIONS(15),
    [anon_sym_DFHPF6] = ACTIONS(15),
    [anon_sym_DFHPF7] = ACTIONS(15),
    [anon_sym_DFHPF8] = ACTIONS(15),
    [anon_sym_DFHPF9] = ACTIONS(15),
    [anon_sym_DFHPF10] = ACTIONS(15),
    [anon_sym_DFHPF11] = ACTIONS(15),
    [anon_sym_DFHPF12] = ACTIONS(15),
    [anon_sym_EIBAID] = ACTIONS(15),
    [anon_sym_DFHRED] = ACTIONS(15),
    [anon_sym_DFHBMASB] = ACTIONS(15),
    [anon_sym_DFHBMASK] = ACTIONS(15),
    [aux_sym_identifier_token1] = ACTIONS(19),
    [aux_sym_identifier_token2] = ACTIONS(21),
    [sym_picture_string] = ACTIONS(23),
    [aux_sym_string_literal_token1] = ACTIONS(25),
    [aux_sym_string_literal_token2] = ACTIONS(25),
    [sym_number] = ACTIONS(23),
    [anon_sym_EQ_EQ] = ACTIONS(27),
    [anon_sym_EQ] = ACTIONS(29),
    [anon_sym_GT] = ACTIONS(29),
    [anon_sym_LT] = ACTIONS(29),
    [anon_sym_GT_EQ] = ACTIONS(27),
    [anon_sym_LT_EQ] = ACTIONS(27),
    [anon_sym_COMMA] = ACTIONS(29),
    [anon_sym_LPAREN] = ACTIONS(31),
    [anon_sym_RPAREN] = ACTIONS(27),
    [anon_sym_COLON] = ACTIONS(27),
  },
  [2] = {
    [sym_newline] = STATE(3),
    [sym_comment_line] = STATE(3),
    [sym_statement] = STATE(3),
    [sym_statement_body] = STATE(31),
    [sym_embedded_comment] = STATE(5),
    [sym_continuation_newline] = STATE(5),
    [sym_level_88_condition] = STATE(5),
    [sym_level_number] = STATE(5),
    [sym_keyword] = STATE(5),
    [sym_identifier] = STATE(5),
    [sym_string_literal] = STATE(5),
    [sym_operator] = STATE(5),
    [sym_parenthesized] = STATE(5),
    [aux_sym_source_file_repeat1] = STATE(3),
    [aux_sym_statement_body_repeat1] = STATE(5),
    [ts_builtin_sym_end] = ACTIONS(33),
    [aux_sym_newline_token1] = ACTIONS(5),
    [aux_sym_comment_line_token1] = ACTIONS(7),
    [sym_sequence_number] = ACTIONS(9),
    [anon_sym_DOT] = ACTIONS(11),
    [anon_sym_88] = ACTIONS(13),
    [anon_sym_VALUE] = ACTIONS(15),
    [anon_sym_IS] = ACTIONS(15),
    [aux_sym_level_number_token1] = ACTIONS(17),
    [aux_sym_level_number_token2] = ACTIONS(17),
    [anon_sym_66] = ACTIONS(17),
    [anon_sym_77] = ACTIONS(17),
    [anon_sym_FILLER] = ACTIONS(15),
    [anon_sym_PIC] = ACTIONS(15),
    [anon_sym_PICTURE] = ACTIONS(15),
    [anon_sym_VALUES] = ACTIONS(15),
    [anon_sym_OCCURS] = ACTIONS(15),
    [anon_sym_TIMES] = ACTIONS(15),
    [anon_sym_TO] = ACTIONS(15),
    [anon_sym_REDEFINES] = ACTIONS(15),
    [anon_sym_INDEXED] = ACTIONS(15),
    [anon_sym_BY] = ACTIONS(15),
    [anon_sym_DEPENDING] = ACTIONS(15),
    [anon_sym_ON] = ACTIONS(15),
    [anon_sym_USAGE] = ACTIONS(15),
    [anon_sym_DISPLAY] = ACTIONS(15),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(15),
    [anon_sym_BINARY] = ACTIONS(15),
    [anon_sym_COMP] = ACTIONS(15),
    [anon_sym_COMP_DASH1] = ACTIONS(15),
    [anon_sym_COMP_DASH2] = ACTIONS(15),
    [anon_sym_COMP_DASH3] = ACTIONS(15),
    [anon_sym_COMP_DASH4] = ACTIONS(15),
    [anon_sym_COMP_DASH5] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(15),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(15),
    [anon_sym_INDEX] = ACTIONS(15),
    [anon_sym_POINTER] = ACTIONS(15),
    [anon_sym_ZERO] = ACTIONS(15),
    [anon_sym_ZEROS] = ACTIONS(15),
    [anon_sym_ZEROES] = ACTIONS(15),
    [anon_sym_SPACE] = ACTIONS(15),
    [anon_sym_SPACES] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(15),
    [anon_sym_QUOTE] = ACTIONS(15),
    [anon_sym_QUOTES] = ACTIONS(15),
    [anon_sym_NULL] = ACTIONS(15),
    [anon_sym_NULLS] = ACTIONS(15),
    [anon_sym_ALL] = ACTIONS(15),
    [anon_sym_THRU] = ACTIONS(15),
    [anon_sym_THROUGH] = ACTIONS(15),
    [anon_sym_ASCENDING] = ACTIONS(15),
    [anon_sym_DESCENDING] = ACTIONS(15),
    [anon_sym_KEY] = ACTIONS(15),
    [anon_sym_SIGN] = ACTIONS(15),
    [anon_sym_LEADING] = ACTIONS(15),
    [anon_sym_TRAILING] = ACTIONS(15),
    [anon_sym_SEPARATE] = ACTIONS(15),
    [anon_sym_CHARACTER] = ACTIONS(15),
    [anon_sym_SYNC] = ACTIONS(15),
    [anon_sym_SYNCHRONIZED] = ACTIONS(15),
    [anon_sym_LEFT] = ACTIONS(15),
    [anon_sym_RIGHT] = ACTIONS(15),
    [anon_sym_JUST] = ACTIONS(15),
    [anon_sym_JUSTIFIED] = ACTIONS(15),
    [anon_sym_BLANK] = ACTIONS(15),
    [anon_sym_WHEN] = ACTIONS(15),
    [anon_sym_EXTERNAL] = ACTIONS(15),
    [anon_sym_GLOBAL] = ACTIONS(15),
    [anon_sym_AS] = ACTIONS(15),
    [anon_sym_COPY] = ACTIONS(15),
    [anon_sym_REPLACING] = ACTIONS(15),
    [anon_sym_OF] = ACTIONS(15),
    [anon_sym_IN] = ACTIONS(15),
    [anon_sym_REPLACE] = ACTIONS(15),
    [anon_sym_OFF] = ACTIONS(15),
    [anon_sym_EJECT] = ACTIONS(15),
    [anon_sym_SKIP1] = ACTIONS(15),
    [anon_sym_SKIP2] = ACTIONS(15),
    [anon_sym_SKIP3] = ACTIONS(15),
    [anon_sym_EXEC] = ACTIONS(15),
    [anon_sym_EXECUTE] = ACTIONS(15),
    [anon_sym_SQL] = ACTIONS(15),
    [anon_sym_SQLIMS] = ACTIONS(15),
    [anon_sym_DLI] = ACTIONS(15),
    [anon_sym_END_DASHEXEC] = ACTIONS(15),
    [anon_sym_IF] = ACTIONS(15),
    [anon_sym_ELSE] = ACTIONS(15),
    [anon_sym_END_DASHIF] = ACTIONS(15),
    [anon_sym_THEN] = ACTIONS(15),
    [anon_sym_EVALUATE] = ACTIONS(15),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(15),
    [anon_sym_OTHER] = ACTIONS(15),
    [anon_sym_ALSO] = ACTIONS(15),
    [anon_sym_PERFORM] = ACTIONS(15),
    [anon_sym_END_DASHPERFORM] = ACTIONS(15),
    [anon_sym_UNTIL] = ACTIONS(15),
    [anon_sym_VARYING] = ACTIONS(15),
    [anon_sym_WITH] = ACTIONS(15),
    [anon_sym_TEST] = ACTIONS(15),
    [anon_sym_BEFORE] = ACTIONS(15),
    [anon_sym_AFTER] = ACTIONS(15),
    [anon_sym_GO] = ACTIONS(15),
    [anon_sym_SECTION] = ACTIONS(15),
    [anon_sym_PARAGRAPH] = ACTIONS(15),
    [anon_sym_CONTINUE] = ACTIONS(15),
    [anon_sym_NEXT] = ACTIONS(15),
    [anon_sym_SENTENCE] = ACTIONS(15),
    [anon_sym_EXIT] = ACTIONS(15),
    [anon_sym_STOP] = ACTIONS(15),
    [anon_sym_RUN] = ACTIONS(15),
    [anon_sym_MOVE] = ACTIONS(15),
    [anon_sym_CORRESPONDING] = ACTIONS(15),
    [anon_sym_CORR] = ACTIONS(15),
    [anon_sym_INTO] = ACTIONS(15),
    [anon_sym_SET] = ACTIONS(15),
    [anon_sym_TRUE] = ACTIONS(15),
    [anon_sym_FALSE] = ACTIONS(15),
    [anon_sym_INITIALIZE] = ACTIONS(15),
    [anon_sym_ALPHABETIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_NUMERIC] = ACTIONS(15),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_COMPUTE] = ACTIONS(15),
    [anon_sym_ADD] = ACTIONS(15),
    [anon_sym_SUBTRACT] = ACTIONS(15),
    [anon_sym_MULTIPLY] = ACTIONS(15),
    [anon_sym_DIVIDE] = ACTIONS(15),
    [anon_sym_GIVING] = ACTIONS(15),
    [anon_sym_REMAINDER] = ACTIONS(15),
    [anon_sym_STRING] = ACTIONS(15),
    [anon_sym_DELIMITED] = ACTIONS(15),
    [anon_sym_SIZE] = ACTIONS(15),
    [anon_sym_OVERFLOW] = ACTIONS(15),
    [anon_sym_NOT] = ACTIONS(15),
    [anon_sym_END_DASHSTRING] = ACTIONS(15),
    [anon_sym_UNSTRING] = ACTIONS(15),
    [anon_sym_COUNT] = ACTIONS(15),
    [anon_sym_DELIMITER] = ACTIONS(15),
    [anon_sym_TALLYING] = ACTIONS(15),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(15),
    [anon_sym_INSPECT] = ACTIONS(15),
    [anon_sym_CONVERTING] = ACTIONS(15),
    [anon_sym_FIRST] = ACTIONS(15),
    [anon_sym_INITIAL] = ACTIONS(15),
    [anon_sym_READ] = ACTIONS(15),
    [anon_sym_WRITE] = ACTIONS(15),
    [anon_sym_REWRITE] = ACTIONS(15),
    [anon_sym_DELETE] = ACTIONS(15),
    [anon_sym_START] = ACTIONS(15),
    [anon_sym_OPEN] = ACTIONS(15),
    [anon_sym_CLOSE] = ACTIONS(15),
    [anon_sym_INPUT] = ACTIONS(15),
    [anon_sym_OUTPUT] = ACTIONS(15),
    [anon_sym_I_DASHO] = ACTIONS(15),
    [anon_sym_EXTEND] = ACTIONS(15),
    [anon_sym_ACCEPT] = ACTIONS(15),
    [anon_sym_FROM] = ACTIONS(15),
    [anon_sym_DATE] = ACTIONS(15),
    [anon_sym_DAY] = ACTIONS(15),
    [anon_sym_TIME] = ACTIONS(15),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(15),
    [anon_sym_EQUAL] = ACTIONS(15),
    [anon_sym_GREATER] = ACTIONS(15),
    [anon_sym_LESS] = ACTIONS(15),
    [anon_sym_THAN] = ACTIONS(15),
    [anon_sym_OR] = ACTIONS(15),
    [anon_sym_AND] = ACTIONS(15),
    [anon_sym_DFHENTER] = ACTIONS(15),
    [anon_sym_DFHCLEAR] = ACTIONS(15),
    [anon_sym_DFHPA1] = ACTIONS(15),
    [anon_sym_DFHPA2] = ACTIONS(15),
    [anon_sym_DFHPF1] = ACTIONS(15),
    [anon_sym_DFHPF2] = ACTIONS(15),
    [anon_sym_DFHPF3] = ACTIONS(15),
    [anon_sym_DFHPF4] = ACTIONS(15),
    [anon_sym_DFHPF5] = ACTIONS(15),
    [anon_sym_DFHPF6] = ACTIONS(15),
    [anon_sym_DFHPF7] = ACTIONS(15),
    [anon_sym_DFHPF8] = ACTIONS(15),
    [anon_sym_DFHPF9] = ACTIONS(15),
    [anon_sym_DFHPF10] = ACTIONS(15),
    [anon_sym_DFHPF11] = ACTIONS(15),
    [anon_sym_DFHPF12] = ACTIONS(15),
    [anon_sym_EIBAID] = ACTIONS(15),
    [anon_sym_DFHRED] = ACTIONS(15),
    [anon_sym_DFHBMASB] = ACTIONS(15),
    [anon_sym_DFHBMASK] = ACTIONS(15),
    [aux_sym_identifier_token1] = ACTIONS(19),
    [aux_sym_identifier_token2] = ACTIONS(21),
    [sym_picture_string] = ACTIONS(23),
    [aux_sym_string_literal_token1] = ACTIONS(25),
    [aux_sym_string_literal_token2] = ACTIONS(25),
    [sym_number] = ACTIONS(23),
    [anon_sym_EQ_EQ] = ACTIONS(27),
    [anon_sym_EQ] = ACTIONS(29),
    [anon_sym_GT] = ACTIONS(29),
    [anon_sym_LT] = ACTIONS(29),
    [anon_sym_GT_EQ] = ACTIONS(27),
    [anon_sym_LT_EQ] = ACTIONS(27),
    [anon_sym_COMMA] = ACTIONS(29),
    [anon_sym_LPAREN] = ACTIONS(31),
    [anon_sym_RPAREN] = ACTIONS(27),
    [anon_sym_COLON] = ACTIONS(27),
  },
  [3] = {
    [sym_newline] = STATE(3),
    [sym_comment_line] = STATE(3),
    [sym_statement] = STATE(3),
    [sym_statement_body] = STATE(31),
    [sym_embedded_comment] = STATE(5),
    [sym_continuation_newline] = STATE(5),
    [sym_level_88_condition] = STATE(5),
    [sym_level_number] = STATE(5),
    [sym_keyword] = STATE(5),
    [sym_identifier] = STATE(5),
    [sym_string_literal] = STATE(5),
    [sym_operator] = STATE(5),
    [sym_parenthesized] = STATE(5),
    [aux_sym_source_file_repeat1] = STATE(3),
    [aux_sym_statement_body_repeat1] = STATE(5),
    [ts_builtin_sym_end] = ACTIONS(35),
    [aux_sym_newline_token1] = ACTIONS(37),
    [aux_sym_comment_line_token1] = ACTIONS(40),
    [sym_sequence_number] = ACTIONS(43),
    [anon_sym_DOT] = ACTIONS(46),
    [anon_sym_88] = ACTIONS(49),
    [anon_sym_VALUE] = ACTIONS(52),
    [anon_sym_IS] = ACTIONS(52),
    [aux_sym_level_number_token1] = ACTIONS(55),
    [aux_sym_level_number_token2] = ACTIONS(55),
    [anon_sym_66] = ACTIONS(55),
    [anon_sym_77] = ACTIONS(55),
    [anon_sym_FILLER] = ACTIONS(52),
    [anon_sym_PIC] = ACTIONS(52),
    [anon_sym_PICTURE] = ACTIONS(52),
    [anon_sym_VALUES] = ACTIONS(52),
    [anon_sym_OCCURS] = ACTIONS(52),
    [anon_sym_TIMES] = ACTIONS(52),
    [anon_sym_TO] = ACTIONS(52),
    [anon_sym_REDEFINES] = ACTIONS(52),
    [anon_sym_INDEXED] = ACTIONS(52),
    [anon_sym_BY] = ACTIONS(52),
    [anon_sym_DEPENDING] = ACTIONS(52),
    [anon_sym_ON] = ACTIONS(52),
    [anon_sym_USAGE] = ACTIONS(52),
    [anon_sym_DISPLAY] = ACTIONS(52),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(52),
    [anon_sym_BINARY] = ACTIONS(52),
    [anon_sym_COMP] = ACTIONS(52),
    [anon_sym_COMP_DASH1] = ACTIONS(52),
    [anon_sym_COMP_DASH2] = ACTIONS(52),
    [anon_sym_COMP_DASH3] = ACTIONS(52),
    [anon_sym_COMP_DASH4] = ACTIONS(52),
    [anon_sym_COMP_DASH5] = ACTIONS(52),
    [anon_sym_COMPUTATIONAL] = ACTIONS(52),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(52),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(52),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(52),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(52),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(52),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(52),
    [anon_sym_INDEX] = ACTIONS(52),
    [anon_sym_POINTER] = ACTIONS(52),
    [anon_sym_ZERO] = ACTIONS(52),
    [anon_sym_ZEROS] = ACTIONS(52),
    [anon_sym_ZEROES] = ACTIONS(52),
    [anon_sym_SPACE] = ACTIONS(52),
    [anon_sym_SPACES] = ACTIONS(52),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(52),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(52),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(52),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(52),
    [anon_sym_QUOTE] = ACTIONS(52),
    [anon_sym_QUOTES] = ACTIONS(52),
    [anon_sym_NULL] = ACTIONS(52),
    [anon_sym_NULLS] = ACTIONS(52),
    [anon_sym_ALL] = ACTIONS(52),
    [anon_sym_THRU] = ACTIONS(52),
    [anon_sym_THROUGH] = ACTIONS(52),
    [anon_sym_ASCENDING] = ACTIONS(52),
    [anon_sym_DESCENDING] = ACTIONS(52),
    [anon_sym_KEY] = ACTIONS(52),
    [anon_sym_SIGN] = ACTIONS(52),
    [anon_sym_LEADING] = ACTIONS(52),
    [anon_sym_TRAILING] = ACTIONS(52),
    [anon_sym_SEPARATE] = ACTIONS(52),
    [anon_sym_CHARACTER] = ACTIONS(52),
    [anon_sym_SYNC] = ACTIONS(52),
    [anon_sym_SYNCHRONIZED] = ACTIONS(52),
    [anon_sym_LEFT] = ACTIONS(52),
    [anon_sym_RIGHT] = ACTIONS(52),
    [anon_sym_JUST] = ACTIONS(52),
    [anon_sym_JUSTIFIED] = ACTIONS(52),
    [anon_sym_BLANK] = ACTIONS(52),
    [anon_sym_WHEN] = ACTIONS(52),
    [anon_sym_EXTERNAL] = ACTIONS(52),
    [anon_sym_GLOBAL] = ACTIONS(52),
    [anon_sym_AS] = ACTIONS(52),
    [anon_sym_COPY] = ACTIONS(52),
    [anon_sym_REPLACING] = ACTIONS(52),
    [anon_sym_OF] = ACTIONS(52),
    [anon_sym_IN] = ACTIONS(52),
    [anon_sym_REPLACE] = ACTIONS(52),
    [anon_sym_OFF] = ACTIONS(52),
    [anon_sym_EJECT] = ACTIONS(52),
    [anon_sym_SKIP1] = ACTIONS(52),
    [anon_sym_SKIP2] = ACTIONS(52),
    [anon_sym_SKIP3] = ACTIONS(52),
    [anon_sym_EXEC] = ACTIONS(52),
    [anon_sym_EXECUTE] = ACTIONS(52),
    [anon_sym_SQL] = ACTIONS(52),
    [anon_sym_SQLIMS] = ACTIONS(52),
    [anon_sym_DLI] = ACTIONS(52),
    [anon_sym_END_DASHEXEC] = ACTIONS(52),
    [anon_sym_IF] = ACTIONS(52),
    [anon_sym_ELSE] = ACTIONS(52),
    [anon_sym_END_DASHIF] = ACTIONS(52),
    [anon_sym_THEN] = ACTIONS(52),
    [anon_sym_EVALUATE] = ACTIONS(52),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(52),
    [anon_sym_OTHER] = ACTIONS(52),
    [anon_sym_ALSO] = ACTIONS(52),
    [anon_sym_PERFORM] = ACTIONS(52),
    [anon_sym_END_DASHPERFORM] = ACTIONS(52),
    [anon_sym_UNTIL] = ACTIONS(52),
    [anon_sym_VARYING] = ACTIONS(52),
    [anon_sym_WITH] = ACTIONS(52),
    [anon_sym_TEST] = ACTIONS(52),
    [anon_sym_BEFORE] = ACTIONS(52),
    [anon_sym_AFTER] = ACTIONS(52),
    [anon_sym_GO] = ACTIONS(52),
    [anon_sym_SECTION] = ACTIONS(52),
    [anon_sym_PARAGRAPH] = ACTIONS(52),
    [anon_sym_CONTINUE] = ACTIONS(52),
    [anon_sym_NEXT] = ACTIONS(52),
    [anon_sym_SENTENCE] = ACTIONS(52),
    [anon_sym_EXIT] = ACTIONS(52),
    [anon_sym_STOP] = ACTIONS(52),
    [anon_sym_RUN] = ACTIONS(52),
    [anon_sym_MOVE] = ACTIONS(52),
    [anon_sym_CORRESPONDING] = ACTIONS(52),
    [anon_sym_CORR] = ACTIONS(52),
    [anon_sym_INTO] = ACTIONS(52),
    [anon_sym_SET] = ACTIONS(52),
    [anon_sym_TRUE] = ACTIONS(52),
    [anon_sym_FALSE] = ACTIONS(52),
    [anon_sym_INITIALIZE] = ACTIONS(52),
    [anon_sym_ALPHABETIC] = ACTIONS(52),
    [anon_sym_ALPHANUMERIC] = ACTIONS(52),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(52),
    [anon_sym_NUMERIC] = ACTIONS(52),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(52),
    [anon_sym_COMPUTE] = ACTIONS(52),
    [anon_sym_ADD] = ACTIONS(52),
    [anon_sym_SUBTRACT] = ACTIONS(52),
    [anon_sym_MULTIPLY] = ACTIONS(52),
    [anon_sym_DIVIDE] = ACTIONS(52),
    [anon_sym_GIVING] = ACTIONS(52),
    [anon_sym_REMAINDER] = ACTIONS(52),
    [anon_sym_STRING] = ACTIONS(52),
    [anon_sym_DELIMITED] = ACTIONS(52),
    [anon_sym_SIZE] = ACTIONS(52),
    [anon_sym_OVERFLOW] = ACTIONS(52),
    [anon_sym_NOT] = ACTIONS(52),
    [anon_sym_END_DASHSTRING] = ACTIONS(52),
    [anon_sym_UNSTRING] = ACTIONS(52),
    [anon_sym_COUNT] = ACTIONS(52),
    [anon_sym_DELIMITER] = ACTIONS(52),
    [anon_sym_TALLYING] = ACTIONS(52),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(52),
    [anon_sym_INSPECT] = ACTIONS(52),
    [anon_sym_CONVERTING] = ACTIONS(52),
    [anon_sym_FIRST] = ACTIONS(52),
    [anon_sym_INITIAL] = ACTIONS(52),
    [anon_sym_READ] = ACTIONS(52),
    [anon_sym_WRITE] = ACTIONS(52),
    [anon_sym_REWRITE] = ACTIONS(52),
    [anon_sym_DELETE] = ACTIONS(52),
    [anon_sym_START] = ACTIONS(52),
    [anon_sym_OPEN] = ACTIONS(52),
    [anon_sym_CLOSE] = ACTIONS(52),
    [anon_sym_INPUT] = ACTIONS(52),
    [anon_sym_OUTPUT] = ACTIONS(52),
    [anon_sym_I_DASHO] = ACTIONS(52),
    [anon_sym_EXTEND] = ACTIONS(52),
    [anon_sym_ACCEPT] = ACTIONS(52),
    [anon_sym_FROM] = ACTIONS(52),
    [anon_sym_DATE] = ACTIONS(52),
    [anon_sym_DAY] = ACTIONS(52),
    [anon_sym_TIME] = ACTIONS(52),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(52),
    [anon_sym_EQUAL] = ACTIONS(52),
    [anon_sym_GREATER] = ACTIONS(52),
    [anon_sym_LESS] = ACTIONS(52),
    [anon_sym_THAN] = ACTIONS(52),
    [anon_sym_OR] = ACTIONS(52),
    [anon_sym_AND] = ACTIONS(52),
    [anon_sym_DFHENTER] = ACTIONS(52),
    [anon_sym_DFHCLEAR] = ACTIONS(52),
    [anon_sym_DFHPA1] = ACTIONS(52),
    [anon_sym_DFHPA2] = ACTIONS(52),
    [anon_sym_DFHPF1] = ACTIONS(52),
    [anon_sym_DFHPF2] = ACTIONS(52),
    [anon_sym_DFHPF3] = ACTIONS(52),
    [anon_sym_DFHPF4] = ACTIONS(52),
    [anon_sym_DFHPF5] = ACTIONS(52),
    [anon_sym_DFHPF6] = ACTIONS(52),
    [anon_sym_DFHPF7] = ACTIONS(52),
    [anon_sym_DFHPF8] = ACTIONS(52),
    [anon_sym_DFHPF9] = ACTIONS(52),
    [anon_sym_DFHPF10] = ACTIONS(52),
    [anon_sym_DFHPF11] = ACTIONS(52),
    [anon_sym_DFHPF12] = ACTIONS(52),
    [anon_sym_EIBAID] = ACTIONS(52),
    [anon_sym_DFHRED] = ACTIONS(52),
    [anon_sym_DFHBMASB] = ACTIONS(52),
    [anon_sym_DFHBMASK] = ACTIONS(52),
    [aux_sym_identifier_token1] = ACTIONS(58),
    [aux_sym_identifier_token2] = ACTIONS(61),
    [sym_picture_string] = ACTIONS(64),
    [aux_sym_string_literal_token1] = ACTIONS(67),
    [aux_sym_string_literal_token2] = ACTIONS(67),
    [sym_number] = ACTIONS(64),
    [anon_sym_EQ_EQ] = ACTIONS(70),
    [anon_sym_EQ] = ACTIONS(73),
    [anon_sym_GT] = ACTIONS(73),
    [anon_sym_LT] = ACTIONS(73),
    [anon_sym_GT_EQ] = ACTIONS(70),
    [anon_sym_LT_EQ] = ACTIONS(70),
    [anon_sym_COMMA] = ACTIONS(73),
    [anon_sym_LPAREN] = ACTIONS(76),
    [anon_sym_RPAREN] = ACTIONS(70),
    [anon_sym_COLON] = ACTIONS(70),
  },
  [4] = {
    [sym_statement_body] = STATE(33),
    [sym_embedded_comment] = STATE(5),
    [sym_continuation_newline] = STATE(5),
    [sym_level_88_condition] = STATE(5),
    [sym_level_number] = STATE(5),
    [sym_keyword] = STATE(5),
    [sym_identifier] = STATE(5),
    [sym_string_literal] = STATE(5),
    [sym_operator] = STATE(5),
    [sym_parenthesized] = STATE(5),
    [aux_sym_statement_body_repeat1] = STATE(5),
    [aux_sym_newline_token1] = ACTIONS(79),
    [aux_sym_comment_line_token1] = ACTIONS(81),
    [anon_sym_DOT] = ACTIONS(83),
    [anon_sym_88] = ACTIONS(13),
    [anon_sym_VALUE] = ACTIONS(15),
    [anon_sym_IS] = ACTIONS(15),
    [aux_sym_level_number_token1] = ACTIONS(17),
    [aux_sym_level_number_token2] = ACTIONS(17),
    [anon_sym_66] = ACTIONS(17),
    [anon_sym_77] = ACTIONS(17),
    [anon_sym_FILLER] = ACTIONS(15),
    [anon_sym_PIC] = ACTIONS(15),
    [anon_sym_PICTURE] = ACTIONS(15),
    [anon_sym_VALUES] = ACTIONS(15),
    [anon_sym_OCCURS] = ACTIONS(15),
    [anon_sym_TIMES] = ACTIONS(15),
    [anon_sym_TO] = ACTIONS(15),
    [anon_sym_REDEFINES] = ACTIONS(15),
    [anon_sym_INDEXED] = ACTIONS(15),
    [anon_sym_BY] = ACTIONS(15),
    [anon_sym_DEPENDING] = ACTIONS(15),
    [anon_sym_ON] = ACTIONS(15),
    [anon_sym_USAGE] = ACTIONS(15),
    [anon_sym_DISPLAY] = ACTIONS(15),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(15),
    [anon_sym_BINARY] = ACTIONS(15),
    [anon_sym_COMP] = ACTIONS(15),
    [anon_sym_COMP_DASH1] = ACTIONS(15),
    [anon_sym_COMP_DASH2] = ACTIONS(15),
    [anon_sym_COMP_DASH3] = ACTIONS(15),
    [anon_sym_COMP_DASH4] = ACTIONS(15),
    [anon_sym_COMP_DASH5] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(15),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(15),
    [anon_sym_INDEX] = ACTIONS(15),
    [anon_sym_POINTER] = ACTIONS(15),
    [anon_sym_ZERO] = ACTIONS(15),
    [anon_sym_ZEROS] = ACTIONS(15),
    [anon_sym_ZEROES] = ACTIONS(15),
    [anon_sym_SPACE] = ACTIONS(15),
    [anon_sym_SPACES] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(15),
    [anon_sym_QUOTE] = ACTIONS(15),
    [anon_sym_QUOTES] = ACTIONS(15),
    [anon_sym_NULL] = ACTIONS(15),
    [anon_sym_NULLS] = ACTIONS(15),
    [anon_sym_ALL] = ACTIONS(15),
    [anon_sym_THRU] = ACTIONS(15),
    [anon_sym_THROUGH] = ACTIONS(15),
    [anon_sym_ASCENDING] = ACTIONS(15),
    [anon_sym_DESCENDING] = ACTIONS(15),
    [anon_sym_KEY] = ACTIONS(15),
    [anon_sym_SIGN] = ACTIONS(15),
    [anon_sym_LEADING] = ACTIONS(15),
    [anon_sym_TRAILING] = ACTIONS(15),
    [anon_sym_SEPARATE] = ACTIONS(15),
    [anon_sym_CHARACTER] = ACTIONS(15),
    [anon_sym_SYNC] = ACTIONS(15),
    [anon_sym_SYNCHRONIZED] = ACTIONS(15),
    [anon_sym_LEFT] = ACTIONS(15),
    [anon_sym_RIGHT] = ACTIONS(15),
    [anon_sym_JUST] = ACTIONS(15),
    [anon_sym_JUSTIFIED] = ACTIONS(15),
    [anon_sym_BLANK] = ACTIONS(15),
    [anon_sym_WHEN] = ACTIONS(15),
    [anon_sym_EXTERNAL] = ACTIONS(15),
    [anon_sym_GLOBAL] = ACTIONS(15),
    [anon_sym_AS] = ACTIONS(15),
    [anon_sym_COPY] = ACTIONS(15),
    [anon_sym_REPLACING] = ACTIONS(15),
    [anon_sym_OF] = ACTIONS(15),
    [anon_sym_IN] = ACTIONS(15),
    [anon_sym_REPLACE] = ACTIONS(15),
    [anon_sym_OFF] = ACTIONS(15),
    [anon_sym_EJECT] = ACTIONS(15),
    [anon_sym_SKIP1] = ACTIONS(15),
    [anon_sym_SKIP2] = ACTIONS(15),
    [anon_sym_SKIP3] = ACTIONS(15),
    [anon_sym_EXEC] = ACTIONS(15),
    [anon_sym_EXECUTE] = ACTIONS(15),
    [anon_sym_SQL] = ACTIONS(15),
    [anon_sym_SQLIMS] = ACTIONS(15),
    [anon_sym_DLI] = ACTIONS(15),
    [anon_sym_END_DASHEXEC] = ACTIONS(15),
    [anon_sym_IF] = ACTIONS(15),
    [anon_sym_ELSE] = ACTIONS(15),
    [anon_sym_END_DASHIF] = ACTIONS(15),
    [anon_sym_THEN] = ACTIONS(15),
    [anon_sym_EVALUATE] = ACTIONS(15),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(15),
    [anon_sym_OTHER] = ACTIONS(15),
    [anon_sym_ALSO] = ACTIONS(15),
    [anon_sym_PERFORM] = ACTIONS(15),
    [anon_sym_END_DASHPERFORM] = ACTIONS(15),
    [anon_sym_UNTIL] = ACTIONS(15),
    [anon_sym_VARYING] = ACTIONS(15),
    [anon_sym_WITH] = ACTIONS(15),
    [anon_sym_TEST] = ACTIONS(15),
    [anon_sym_BEFORE] = ACTIONS(15),
    [anon_sym_AFTER] = ACTIONS(15),
    [anon_sym_GO] = ACTIONS(15),
    [anon_sym_SECTION] = ACTIONS(15),
    [anon_sym_PARAGRAPH] = ACTIONS(15),
    [anon_sym_CONTINUE] = ACTIONS(15),
    [anon_sym_NEXT] = ACTIONS(15),
    [anon_sym_SENTENCE] = ACTIONS(15),
    [anon_sym_EXIT] = ACTIONS(15),
    [anon_sym_STOP] = ACTIONS(15),
    [anon_sym_RUN] = ACTIONS(15),
    [anon_sym_MOVE] = ACTIONS(15),
    [anon_sym_CORRESPONDING] = ACTIONS(15),
    [anon_sym_CORR] = ACTIONS(15),
    [anon_sym_INTO] = ACTIONS(15),
    [anon_sym_SET] = ACTIONS(15),
    [anon_sym_TRUE] = ACTIONS(15),
    [anon_sym_FALSE] = ACTIONS(15),
    [anon_sym_INITIALIZE] = ACTIONS(15),
    [anon_sym_ALPHABETIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_NUMERIC] = ACTIONS(15),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_COMPUTE] = ACTIONS(15),
    [anon_sym_ADD] = ACTIONS(15),
    [anon_sym_SUBTRACT] = ACTIONS(15),
    [anon_sym_MULTIPLY] = ACTIONS(15),
    [anon_sym_DIVIDE] = ACTIONS(15),
    [anon_sym_GIVING] = ACTIONS(15),
    [anon_sym_REMAINDER] = ACTIONS(15),
    [anon_sym_STRING] = ACTIONS(15),
    [anon_sym_DELIMITED] = ACTIONS(15),
    [anon_sym_SIZE] = ACTIONS(15),
    [anon_sym_OVERFLOW] = ACTIONS(15),
    [anon_sym_NOT] = ACTIONS(15),
    [anon_sym_END_DASHSTRING] = ACTIONS(15),
    [anon_sym_UNSTRING] = ACTIONS(15),
    [anon_sym_COUNT] = ACTIONS(15),
    [anon_sym_DELIMITER] = ACTIONS(15),
    [anon_sym_TALLYING] = ACTIONS(15),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(15),
    [anon_sym_INSPECT] = ACTIONS(15),
    [anon_sym_CONVERTING] = ACTIONS(15),
    [anon_sym_FIRST] = ACTIONS(15),
    [anon_sym_INITIAL] = ACTIONS(15),
    [anon_sym_READ] = ACTIONS(15),
    [anon_sym_WRITE] = ACTIONS(15),
    [anon_sym_REWRITE] = ACTIONS(15),
    [anon_sym_DELETE] = ACTIONS(15),
    [anon_sym_START] = ACTIONS(15),
    [anon_sym_OPEN] = ACTIONS(15),
    [anon_sym_CLOSE] = ACTIONS(15),
    [anon_sym_INPUT] = ACTIONS(15),
    [anon_sym_OUTPUT] = ACTIONS(15),
    [anon_sym_I_DASHO] = ACTIONS(15),
    [anon_sym_EXTEND] = ACTIONS(15),
    [anon_sym_ACCEPT] = ACTIONS(15),
    [anon_sym_FROM] = ACTIONS(15),
    [anon_sym_DATE] = ACTIONS(15),
    [anon_sym_DAY] = ACTIONS(15),
    [anon_sym_TIME] = ACTIONS(15),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(15),
    [anon_sym_EQUAL] = ACTIONS(15),
    [anon_sym_GREATER] = ACTIONS(15),
    [anon_sym_LESS] = ACTIONS(15),
    [anon_sym_THAN] = ACTIONS(15),
    [anon_sym_OR] = ACTIONS(15),
    [anon_sym_AND] = ACTIONS(15),
    [anon_sym_DFHENTER] = ACTIONS(15),
    [anon_sym_DFHCLEAR] = ACTIONS(15),
    [anon_sym_DFHPA1] = ACTIONS(15),
    [anon_sym_DFHPA2] = ACTIONS(15),
    [anon_sym_DFHPF1] = ACTIONS(15),
    [anon_sym_DFHPF2] = ACTIONS(15),
    [anon_sym_DFHPF3] = ACTIONS(15),
    [anon_sym_DFHPF4] = ACTIONS(15),
    [anon_sym_DFHPF5] = ACTIONS(15),
    [anon_sym_DFHPF6] = ACTIONS(15),
    [anon_sym_DFHPF7] = ACTIONS(15),
    [anon_sym_DFHPF8] = ACTIONS(15),
    [anon_sym_DFHPF9] = ACTIONS(15),
    [anon_sym_DFHPF10] = ACTIONS(15),
    [anon_sym_DFHPF11] = ACTIONS(15),
    [anon_sym_DFHPF12] = ACTIONS(15),
    [anon_sym_EIBAID] = ACTIONS(15),
    [anon_sym_DFHRED] = ACTIONS(15),
    [anon_sym_DFHBMASB] = ACTIONS(15),
    [anon_sym_DFHBMASK] = ACTIONS(15),
    [aux_sym_identifier_token1] = ACTIONS(19),
    [aux_sym_identifier_token2] = ACTIONS(21),
    [sym_picture_string] = ACTIONS(23),
    [aux_sym_string_literal_token1] = ACTIONS(25),
    [aux_sym_string_literal_token2] = ACTIONS(25),
    [sym_number] = ACTIONS(23),
    [anon_sym_EQ_EQ] = ACTIONS(27),
    [anon_sym_EQ] = ACTIONS(29),
    [anon_sym_GT] = ACTIONS(29),
    [anon_sym_LT] = ACTIONS(29),
    [anon_sym_GT_EQ] = ACTIONS(27),
    [anon_sym_LT_EQ] = ACTIONS(27),
    [anon_sym_COMMA] = ACTIONS(29),
    [anon_sym_LPAREN] = ACTIONS(31),
    [anon_sym_RPAREN] = ACTIONS(27),
    [anon_sym_COLON] = ACTIONS(27),
  },
  [5] = {
    [sym_embedded_comment] = STATE(6),
    [sym_continuation_newline] = STATE(6),
    [sym_level_88_condition] = STATE(6),
    [sym_level_number] = STATE(6),
    [sym_keyword] = STATE(6),
    [sym_identifier] = STATE(6),
    [sym_string_literal] = STATE(6),
    [sym_operator] = STATE(6),
    [sym_parenthesized] = STATE(6),
    [aux_sym_statement_body_repeat1] = STATE(6),
    [aux_sym_newline_token1] = ACTIONS(79),
    [anon_sym_DOT] = ACTIONS(85),
    [anon_sym_88] = ACTIONS(13),
    [anon_sym_VALUE] = ACTIONS(15),
    [anon_sym_IS] = ACTIONS(15),
    [aux_sym_level_number_token1] = ACTIONS(17),
    [aux_sym_level_number_token2] = ACTIONS(17),
    [anon_sym_66] = ACTIONS(17),
    [anon_sym_77] = ACTIONS(17),
    [anon_sym_FILLER] = ACTIONS(15),
    [anon_sym_PIC] = ACTIONS(15),
    [anon_sym_PICTURE] = ACTIONS(15),
    [anon_sym_VALUES] = ACTIONS(15),
    [anon_sym_OCCURS] = ACTIONS(15),
    [anon_sym_TIMES] = ACTIONS(15),
    [anon_sym_TO] = ACTIONS(15),
    [anon_sym_REDEFINES] = ACTIONS(15),
    [anon_sym_INDEXED] = ACTIONS(15),
    [anon_sym_BY] = ACTIONS(15),
    [anon_sym_DEPENDING] = ACTIONS(15),
    [anon_sym_ON] = ACTIONS(15),
    [anon_sym_USAGE] = ACTIONS(15),
    [anon_sym_DISPLAY] = ACTIONS(15),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(15),
    [anon_sym_BINARY] = ACTIONS(15),
    [anon_sym_COMP] = ACTIONS(15),
    [anon_sym_COMP_DASH1] = ACTIONS(15),
    [anon_sym_COMP_DASH2] = ACTIONS(15),
    [anon_sym_COMP_DASH3] = ACTIONS(15),
    [anon_sym_COMP_DASH4] = ACTIONS(15),
    [anon_sym_COMP_DASH5] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(15),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(15),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(15),
    [anon_sym_INDEX] = ACTIONS(15),
    [anon_sym_POINTER] = ACTIONS(15),
    [anon_sym_ZERO] = ACTIONS(15),
    [anon_sym_ZEROS] = ACTIONS(15),
    [anon_sym_ZEROES] = ACTIONS(15),
    [anon_sym_SPACE] = ACTIONS(15),
    [anon_sym_SPACES] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(15),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(15),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(15),
    [anon_sym_QUOTE] = ACTIONS(15),
    [anon_sym_QUOTES] = ACTIONS(15),
    [anon_sym_NULL] = ACTIONS(15),
    [anon_sym_NULLS] = ACTIONS(15),
    [anon_sym_ALL] = ACTIONS(15),
    [anon_sym_THRU] = ACTIONS(15),
    [anon_sym_THROUGH] = ACTIONS(15),
    [anon_sym_ASCENDING] = ACTIONS(15),
    [anon_sym_DESCENDING] = ACTIONS(15),
    [anon_sym_KEY] = ACTIONS(15),
    [anon_sym_SIGN] = ACTIONS(15),
    [anon_sym_LEADING] = ACTIONS(15),
    [anon_sym_TRAILING] = ACTIONS(15),
    [anon_sym_SEPARATE] = ACTIONS(15),
    [anon_sym_CHARACTER] = ACTIONS(15),
    [anon_sym_SYNC] = ACTIONS(15),
    [anon_sym_SYNCHRONIZED] = ACTIONS(15),
    [anon_sym_LEFT] = ACTIONS(15),
    [anon_sym_RIGHT] = ACTIONS(15),
    [anon_sym_JUST] = ACTIONS(15),
    [anon_sym_JUSTIFIED] = ACTIONS(15),
    [anon_sym_BLANK] = ACTIONS(15),
    [anon_sym_WHEN] = ACTIONS(15),
    [anon_sym_EXTERNAL] = ACTIONS(15),
    [anon_sym_GLOBAL] = ACTIONS(15),
    [anon_sym_AS] = ACTIONS(15),
    [anon_sym_COPY] = ACTIONS(15),
    [anon_sym_REPLACING] = ACTIONS(15),
    [anon_sym_OF] = ACTIONS(15),
    [anon_sym_IN] = ACTIONS(15),
    [anon_sym_REPLACE] = ACTIONS(15),
    [anon_sym_OFF] = ACTIONS(15),
    [anon_sym_EJECT] = ACTIONS(15),
    [anon_sym_SKIP1] = ACTIONS(15),
    [anon_sym_SKIP2] = ACTIONS(15),
    [anon_sym_SKIP3] = ACTIONS(15),
    [anon_sym_EXEC] = ACTIONS(15),
    [anon_sym_EXECUTE] = ACTIONS(15),
    [anon_sym_SQL] = ACTIONS(15),
    [anon_sym_SQLIMS] = ACTIONS(15),
    [anon_sym_DLI] = ACTIONS(15),
    [anon_sym_END_DASHEXEC] = ACTIONS(15),
    [anon_sym_IF] = ACTIONS(15),
    [anon_sym_ELSE] = ACTIONS(15),
    [anon_sym_END_DASHIF] = ACTIONS(15),
    [anon_sym_THEN] = ACTIONS(15),
    [anon_sym_EVALUATE] = ACTIONS(15),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(15),
    [anon_sym_OTHER] = ACTIONS(15),
    [anon_sym_ALSO] = ACTIONS(15),
    [anon_sym_PERFORM] = ACTIONS(15),
    [anon_sym_END_DASHPERFORM] = ACTIONS(15),
    [anon_sym_UNTIL] = ACTIONS(15),
    [anon_sym_VARYING] = ACTIONS(15),
    [anon_sym_WITH] = ACTIONS(15),
    [anon_sym_TEST] = ACTIONS(15),
    [anon_sym_BEFORE] = ACTIONS(15),
    [anon_sym_AFTER] = ACTIONS(15),
    [anon_sym_GO] = ACTIONS(15),
    [anon_sym_SECTION] = ACTIONS(15),
    [anon_sym_PARAGRAPH] = ACTIONS(15),
    [anon_sym_CONTINUE] = ACTIONS(15),
    [anon_sym_NEXT] = ACTIONS(15),
    [anon_sym_SENTENCE] = ACTIONS(15),
    [anon_sym_EXIT] = ACTIONS(15),
    [anon_sym_STOP] = ACTIONS(15),
    [anon_sym_RUN] = ACTIONS(15),
    [anon_sym_MOVE] = ACTIONS(15),
    [anon_sym_CORRESPONDING] = ACTIONS(15),
    [anon_sym_CORR] = ACTIONS(15),
    [anon_sym_INTO] = ACTIONS(15),
    [anon_sym_SET] = ACTIONS(15),
    [anon_sym_TRUE] = ACTIONS(15),
    [anon_sym_FALSE] = ACTIONS(15),
    [anon_sym_INITIALIZE] = ACTIONS(15),
    [anon_sym_ALPHABETIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC] = ACTIONS(15),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_NUMERIC] = ACTIONS(15),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(15),
    [anon_sym_COMPUTE] = ACTIONS(15),
    [anon_sym_ADD] = ACTIONS(15),
    [anon_sym_SUBTRACT] = ACTIONS(15),
    [anon_sym_MULTIPLY] = ACTIONS(15),
    [anon_sym_DIVIDE] = ACTIONS(15),
    [anon_sym_GIVING] = ACTIONS(15),
    [anon_sym_REMAINDER] = ACTIONS(15),
    [anon_sym_STRING] = ACTIONS(15),
    [anon_sym_DELIMITED] = ACTIONS(15),
    [anon_sym_SIZE] = ACTIONS(15),
    [anon_sym_OVERFLOW] = ACTIONS(15),
    [anon_sym_NOT] = ACTIONS(15),
    [anon_sym_END_DASHSTRING] = ACTIONS(15),
    [anon_sym_UNSTRING] = ACTIONS(15),
    [anon_sym_COUNT] = ACTIONS(15),
    [anon_sym_DELIMITER] = ACTIONS(15),
    [anon_sym_TALLYING] = ACTIONS(15),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(15),
    [anon_sym_INSPECT] = ACTIONS(15),
    [anon_sym_CONVERTING] = ACTIONS(15),
    [anon_sym_FIRST] = ACTIONS(15),
    [anon_sym_INITIAL] = ACTIONS(15),
    [anon_sym_READ] = ACTIONS(15),
    [anon_sym_WRITE] = ACTIONS(15),
    [anon_sym_REWRITE] = ACTIONS(15),
    [anon_sym_DELETE] = ACTIONS(15),
    [anon_sym_START] = ACTIONS(15),
    [anon_sym_OPEN] = ACTIONS(15),
    [anon_sym_CLOSE] = ACTIONS(15),
    [anon_sym_INPUT] = ACTIONS(15),
    [anon_sym_OUTPUT] = ACTIONS(15),
    [anon_sym_I_DASHO] = ACTIONS(15),
    [anon_sym_EXTEND] = ACTIONS(15),
    [anon_sym_ACCEPT] = ACTIONS(15),
    [anon_sym_FROM] = ACTIONS(15),
    [anon_sym_DATE] = ACTIONS(15),
    [anon_sym_DAY] = ACTIONS(15),
    [anon_sym_TIME] = ACTIONS(15),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(15),
    [anon_sym_EQUAL] = ACTIONS(15),
    [anon_sym_GREATER] = ACTIONS(15),
    [anon_sym_LESS] = ACTIONS(15),
    [anon_sym_THAN] = ACTIONS(15),
    [anon_sym_OR] = ACTIONS(15),
    [anon_sym_AND] = ACTIONS(15),
    [anon_sym_DFHENTER] = ACTIONS(15),
    [anon_sym_DFHCLEAR] = ACTIONS(15),
    [anon_sym_DFHPA1] = ACTIONS(15),
    [anon_sym_DFHPA2] = ACTIONS(15),
    [anon_sym_DFHPF1] = ACTIONS(15),
    [anon_sym_DFHPF2] = ACTIONS(15),
    [anon_sym_DFHPF3] = ACTIONS(15),
    [anon_sym_DFHPF4] = ACTIONS(15),
    [anon_sym_DFHPF5] = ACTIONS(15),
    [anon_sym_DFHPF6] = ACTIONS(15),
    [anon_sym_DFHPF7] = ACTIONS(15),
    [anon_sym_DFHPF8] = ACTIONS(15),
    [anon_sym_DFHPF9] = ACTIONS(15),
    [anon_sym_DFHPF10] = ACTIONS(15),
    [anon_sym_DFHPF11] = ACTIONS(15),
    [anon_sym_DFHPF12] = ACTIONS(15),
    [anon_sym_EIBAID] = ACTIONS(15),
    [anon_sym_DFHRED] = ACTIONS(15),
    [anon_sym_DFHBMASB] = ACTIONS(15),
    [anon_sym_DFHBMASK] = ACTIONS(15),
    [aux_sym_identifier_token1] = ACTIONS(19),
    [aux_sym_identifier_token2] = ACTIONS(21),
    [sym_picture_string] = ACTIONS(87),
    [aux_sym_string_literal_token1] = ACTIONS(25),
    [aux_sym_string_literal_token2] = ACTIONS(25),
    [sym_number] = ACTIONS(87),
    [anon_sym_EQ_EQ] = ACTIONS(27),
    [anon_sym_EQ] = ACTIONS(29),
    [anon_sym_GT] = ACTIONS(29),
    [anon_sym_LT] = ACTIONS(29),
    [anon_sym_GT_EQ] = ACTIONS(27),
    [anon_sym_LT_EQ] = ACTIONS(27),
    [anon_sym_COMMA] = ACTIONS(29),
    [anon_sym_LPAREN] = ACTIONS(31),
    [anon_sym_RPAREN] = ACTIONS(27),
    [anon_sym_COLON] = ACTIONS(27),
  },
  [6] = {
    [sym_embedded_comment] = STATE(6),
    [sym_continuation_newline] = STATE(6),
    [sym_level_88_condition] = STATE(6),
    [sym_level_number] = STATE(6),
    [sym_keyword] = STATE(6),
    [sym_identifier] = STATE(6),
    [sym_string_literal] = STATE(6),
    [sym_operator] = STATE(6),
    [sym_parenthesized] = STATE(6),
    [aux_sym_statement_body_repeat1] = STATE(6),
    [aux_sym_newline_token1] = ACTIONS(89),
    [anon_sym_DOT] = ACTIONS(92),
    [anon_sym_88] = ACTIONS(94),
    [anon_sym_VALUE] = ACTIONS(97),
    [anon_sym_IS] = ACTIONS(97),
    [aux_sym_level_number_token1] = ACTIONS(100),
    [aux_sym_level_number_token2] = ACTIONS(100),
    [anon_sym_66] = ACTIONS(100),
    [anon_sym_77] = ACTIONS(100),
    [anon_sym_FILLER] = ACTIONS(97),
    [anon_sym_PIC] = ACTIONS(97),
    [anon_sym_PICTURE] = ACTIONS(97),
    [anon_sym_VALUES] = ACTIONS(97),
    [anon_sym_OCCURS] = ACTIONS(97),
    [anon_sym_TIMES] = ACTIONS(97),
    [anon_sym_TO] = ACTIONS(97),
    [anon_sym_REDEFINES] = ACTIONS(97),
    [anon_sym_INDEXED] = ACTIONS(97),
    [anon_sym_BY] = ACTIONS(97),
    [anon_sym_DEPENDING] = ACTIONS(97),
    [anon_sym_ON] = ACTIONS(97),
    [anon_sym_USAGE] = ACTIONS(97),
    [anon_sym_DISPLAY] = ACTIONS(97),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(97),
    [anon_sym_BINARY] = ACTIONS(97),
    [anon_sym_COMP] = ACTIONS(97),
    [anon_sym_COMP_DASH1] = ACTIONS(97),
    [anon_sym_COMP_DASH2] = ACTIONS(97),
    [anon_sym_COMP_DASH3] = ACTIONS(97),
    [anon_sym_COMP_DASH4] = ACTIONS(97),
    [anon_sym_COMP_DASH5] = ACTIONS(97),
    [anon_sym_COMPUTATIONAL] = ACTIONS(97),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(97),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(97),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(97),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(97),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(97),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(97),
    [anon_sym_INDEX] = ACTIONS(97),
    [anon_sym_POINTER] = ACTIONS(97),
    [anon_sym_ZERO] = ACTIONS(97),
    [anon_sym_ZEROS] = ACTIONS(97),
    [anon_sym_ZEROES] = ACTIONS(97),
    [anon_sym_SPACE] = ACTIONS(97),
    [anon_sym_SPACES] = ACTIONS(97),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(97),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(97),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(97),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(97),
    [anon_sym_QUOTE] = ACTIONS(97),
    [anon_sym_QUOTES] = ACTIONS(97),
    [anon_sym_NULL] = ACTIONS(97),
    [anon_sym_NULLS] = ACTIONS(97),
    [anon_sym_ALL] = ACTIONS(97),
    [anon_sym_THRU] = ACTIONS(97),
    [anon_sym_THROUGH] = ACTIONS(97),
    [anon_sym_ASCENDING] = ACTIONS(97),
    [anon_sym_DESCENDING] = ACTIONS(97),
    [anon_sym_KEY] = ACTIONS(97),
    [anon_sym_SIGN] = ACTIONS(97),
    [anon_sym_LEADING] = ACTIONS(97),
    [anon_sym_TRAILING] = ACTIONS(97),
    [anon_sym_SEPARATE] = ACTIONS(97),
    [anon_sym_CHARACTER] = ACTIONS(97),
    [anon_sym_SYNC] = ACTIONS(97),
    [anon_sym_SYNCHRONIZED] = ACTIONS(97),
    [anon_sym_LEFT] = ACTIONS(97),
    [anon_sym_RIGHT] = ACTIONS(97),
    [anon_sym_JUST] = ACTIONS(97),
    [anon_sym_JUSTIFIED] = ACTIONS(97),
    [anon_sym_BLANK] = ACTIONS(97),
    [anon_sym_WHEN] = ACTIONS(97),
    [anon_sym_EXTERNAL] = ACTIONS(97),
    [anon_sym_GLOBAL] = ACTIONS(97),
    [anon_sym_AS] = ACTIONS(97),
    [anon_sym_COPY] = ACTIONS(97),
    [anon_sym_REPLACING] = ACTIONS(97),
    [anon_sym_OF] = ACTIONS(97),
    [anon_sym_IN] = ACTIONS(97),
    [anon_sym_REPLACE] = ACTIONS(97),
    [anon_sym_OFF] = ACTIONS(97),
    [anon_sym_EJECT] = ACTIONS(97),
    [anon_sym_SKIP1] = ACTIONS(97),
    [anon_sym_SKIP2] = ACTIONS(97),
    [anon_sym_SKIP3] = ACTIONS(97),
    [anon_sym_EXEC] = ACTIONS(97),
    [anon_sym_EXECUTE] = ACTIONS(97),
    [anon_sym_SQL] = ACTIONS(97),
    [anon_sym_SQLIMS] = ACTIONS(97),
    [anon_sym_DLI] = ACTIONS(97),
    [anon_sym_END_DASHEXEC] = ACTIONS(97),
    [anon_sym_IF] = ACTIONS(97),
    [anon_sym_ELSE] = ACTIONS(97),
    [anon_sym_END_DASHIF] = ACTIONS(97),
    [anon_sym_THEN] = ACTIONS(97),
    [anon_sym_EVALUATE] = ACTIONS(97),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(97),
    [anon_sym_OTHER] = ACTIONS(97),
    [anon_sym_ALSO] = ACTIONS(97),
    [anon_sym_PERFORM] = ACTIONS(97),
    [anon_sym_END_DASHPERFORM] = ACTIONS(97),
    [anon_sym_UNTIL] = ACTIONS(97),
    [anon_sym_VARYING] = ACTIONS(97),
    [anon_sym_WITH] = ACTIONS(97),
    [anon_sym_TEST] = ACTIONS(97),
    [anon_sym_BEFORE] = ACTIONS(97),
    [anon_sym_AFTER] = ACTIONS(97),
    [anon_sym_GO] = ACTIONS(97),
    [anon_sym_SECTION] = ACTIONS(97),
    [anon_sym_PARAGRAPH] = ACTIONS(97),
    [anon_sym_CONTINUE] = ACTIONS(97),
    [anon_sym_NEXT] = ACTIONS(97),
    [anon_sym_SENTENCE] = ACTIONS(97),
    [anon_sym_EXIT] = ACTIONS(97),
    [anon_sym_STOP] = ACTIONS(97),
    [anon_sym_RUN] = ACTIONS(97),
    [anon_sym_MOVE] = ACTIONS(97),
    [anon_sym_CORRESPONDING] = ACTIONS(97),
    [anon_sym_CORR] = ACTIONS(97),
    [anon_sym_INTO] = ACTIONS(97),
    [anon_sym_SET] = ACTIONS(97),
    [anon_sym_TRUE] = ACTIONS(97),
    [anon_sym_FALSE] = ACTIONS(97),
    [anon_sym_INITIALIZE] = ACTIONS(97),
    [anon_sym_ALPHABETIC] = ACTIONS(97),
    [anon_sym_ALPHANUMERIC] = ACTIONS(97),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(97),
    [anon_sym_NUMERIC] = ACTIONS(97),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(97),
    [anon_sym_COMPUTE] = ACTIONS(97),
    [anon_sym_ADD] = ACTIONS(97),
    [anon_sym_SUBTRACT] = ACTIONS(97),
    [anon_sym_MULTIPLY] = ACTIONS(97),
    [anon_sym_DIVIDE] = ACTIONS(97),
    [anon_sym_GIVING] = ACTIONS(97),
    [anon_sym_REMAINDER] = ACTIONS(97),
    [anon_sym_STRING] = ACTIONS(97),
    [anon_sym_DELIMITED] = ACTIONS(97),
    [anon_sym_SIZE] = ACTIONS(97),
    [anon_sym_OVERFLOW] = ACTIONS(97),
    [anon_sym_NOT] = ACTIONS(97),
    [anon_sym_END_DASHSTRING] = ACTIONS(97),
    [anon_sym_UNSTRING] = ACTIONS(97),
    [anon_sym_COUNT] = ACTIONS(97),
    [anon_sym_DELIMITER] = ACTIONS(97),
    [anon_sym_TALLYING] = ACTIONS(97),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(97),
    [anon_sym_INSPECT] = ACTIONS(97),
    [anon_sym_CONVERTING] = ACTIONS(97),
    [anon_sym_FIRST] = ACTIONS(97),
    [anon_sym_INITIAL] = ACTIONS(97),
    [anon_sym_READ] = ACTIONS(97),
    [anon_sym_WRITE] = ACTIONS(97),
    [anon_sym_REWRITE] = ACTIONS(97),
    [anon_sym_DELETE] = ACTIONS(97),
    [anon_sym_START] = ACTIONS(97),
    [anon_sym_OPEN] = ACTIONS(97),
    [anon_sym_CLOSE] = ACTIONS(97),
    [anon_sym_INPUT] = ACTIONS(97),
    [anon_sym_OUTPUT] = ACTIONS(97),
    [anon_sym_I_DASHO] = ACTIONS(97),
    [anon_sym_EXTEND] = ACTIONS(97),
    [anon_sym_ACCEPT] = ACTIONS(97),
    [anon_sym_FROM] = ACTIONS(97),
    [anon_sym_DATE] = ACTIONS(97),
    [anon_sym_DAY] = ACTIONS(97),
    [anon_sym_TIME] = ACTIONS(97),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(97),
    [anon_sym_EQUAL] = ACTIONS(97),
    [anon_sym_GREATER] = ACTIONS(97),
    [anon_sym_LESS] = ACTIONS(97),
    [anon_sym_THAN] = ACTIONS(97),
    [anon_sym_OR] = ACTIONS(97),
    [anon_sym_AND] = ACTIONS(97),
    [anon_sym_DFHENTER] = ACTIONS(97),
    [anon_sym_DFHCLEAR] = ACTIONS(97),
    [anon_sym_DFHPA1] = ACTIONS(97),
    [anon_sym_DFHPA2] = ACTIONS(97),
    [anon_sym_DFHPF1] = ACTIONS(97),
    [anon_sym_DFHPF2] = ACTIONS(97),
    [anon_sym_DFHPF3] = ACTIONS(97),
    [anon_sym_DFHPF4] = ACTIONS(97),
    [anon_sym_DFHPF5] = ACTIONS(97),
    [anon_sym_DFHPF6] = ACTIONS(97),
    [anon_sym_DFHPF7] = ACTIONS(97),
    [anon_sym_DFHPF8] = ACTIONS(97),
    [anon_sym_DFHPF9] = ACTIONS(97),
    [anon_sym_DFHPF10] = ACTIONS(97),
    [anon_sym_DFHPF11] = ACTIONS(97),
    [anon_sym_DFHPF12] = ACTIONS(97),
    [anon_sym_EIBAID] = ACTIONS(97),
    [anon_sym_DFHRED] = ACTIONS(97),
    [anon_sym_DFHBMASB] = ACTIONS(97),
    [anon_sym_DFHBMASK] = ACTIONS(97),
    [aux_sym_identifier_token1] = ACTIONS(103),
    [aux_sym_identifier_token2] = ACTIONS(106),
    [sym_picture_string] = ACTIONS(109),
    [aux_sym_string_literal_token1] = ACTIONS(112),
    [aux_sym_string_literal_token2] = ACTIONS(112),
    [sym_number] = ACTIONS(109),
    [anon_sym_EQ_EQ] = ACTIONS(115),
    [anon_sym_EQ] = ACTIONS(118),
    [anon_sym_GT] = ACTIONS(118),
    [anon_sym_LT] = ACTIONS(118),
    [anon_sym_GT_EQ] = ACTIONS(115),
    [anon_sym_LT_EQ] = ACTIONS(115),
    [anon_sym_COMMA] = ACTIONS(118),
    [anon_sym_LPAREN] = ACTIONS(121),
    [anon_sym_RPAREN] = ACTIONS(115),
    [anon_sym_COLON] = ACTIONS(115),
  },
  [7] = {
    [ts_builtin_sym_end] = ACTIONS(124),
    [aux_sym_newline_token1] = ACTIONS(124),
    [aux_sym_comment_line_token1] = ACTIONS(126),
    [sym_sequence_number] = ACTIONS(128),
    [anon_sym_DOT] = ACTIONS(124),
    [anon_sym_88] = ACTIONS(128),
    [anon_sym_VALUE] = ACTIONS(128),
    [anon_sym_IS] = ACTIONS(128),
    [aux_sym_level_number_token1] = ACTIONS(128),
    [aux_sym_level_number_token2] = ACTIONS(128),
    [anon_sym_66] = ACTIONS(128),
    [anon_sym_77] = ACTIONS(128),
    [anon_sym_FILLER] = ACTIONS(128),
    [anon_sym_PIC] = ACTIONS(128),
    [anon_sym_PICTURE] = ACTIONS(128),
    [anon_sym_VALUES] = ACTIONS(128),
    [anon_sym_OCCURS] = ACTIONS(128),
    [anon_sym_TIMES] = ACTIONS(128),
    [anon_sym_TO] = ACTIONS(128),
    [anon_sym_REDEFINES] = ACTIONS(128),
    [anon_sym_INDEXED] = ACTIONS(128),
    [anon_sym_BY] = ACTIONS(128),
    [anon_sym_DEPENDING] = ACTIONS(128),
    [anon_sym_ON] = ACTIONS(128),
    [anon_sym_USAGE] = ACTIONS(128),
    [anon_sym_DISPLAY] = ACTIONS(128),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(128),
    [anon_sym_BINARY] = ACTIONS(128),
    [anon_sym_COMP] = ACTIONS(128),
    [anon_sym_COMP_DASH1] = ACTIONS(128),
    [anon_sym_COMP_DASH2] = ACTIONS(128),
    [anon_sym_COMP_DASH3] = ACTIONS(128),
    [anon_sym_COMP_DASH4] = ACTIONS(128),
    [anon_sym_COMP_DASH5] = ACTIONS(128),
    [anon_sym_COMPUTATIONAL] = ACTIONS(128),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(128),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(128),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(128),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(128),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(128),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(128),
    [anon_sym_INDEX] = ACTIONS(128),
    [anon_sym_POINTER] = ACTIONS(128),
    [anon_sym_ZERO] = ACTIONS(128),
    [anon_sym_ZEROS] = ACTIONS(128),
    [anon_sym_ZEROES] = ACTIONS(128),
    [anon_sym_SPACE] = ACTIONS(128),
    [anon_sym_SPACES] = ACTIONS(128),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(128),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(128),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(128),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(128),
    [anon_sym_QUOTE] = ACTIONS(128),
    [anon_sym_QUOTES] = ACTIONS(128),
    [anon_sym_NULL] = ACTIONS(128),
    [anon_sym_NULLS] = ACTIONS(128),
    [anon_sym_ALL] = ACTIONS(128),
    [anon_sym_THRU] = ACTIONS(128),
    [anon_sym_THROUGH] = ACTIONS(128),
    [anon_sym_ASCENDING] = ACTIONS(128),
    [anon_sym_DESCENDING] = ACTIONS(128),
    [anon_sym_KEY] = ACTIONS(128),
    [anon_sym_SIGN] = ACTIONS(128),
    [anon_sym_LEADING] = ACTIONS(128),
    [anon_sym_TRAILING] = ACTIONS(128),
    [anon_sym_SEPARATE] = ACTIONS(128),
    [anon_sym_CHARACTER] = ACTIONS(128),
    [anon_sym_SYNC] = ACTIONS(128),
    [anon_sym_SYNCHRONIZED] = ACTIONS(128),
    [anon_sym_LEFT] = ACTIONS(128),
    [anon_sym_RIGHT] = ACTIONS(128),
    [anon_sym_JUST] = ACTIONS(128),
    [anon_sym_JUSTIFIED] = ACTIONS(128),
    [anon_sym_BLANK] = ACTIONS(128),
    [anon_sym_WHEN] = ACTIONS(128),
    [anon_sym_EXTERNAL] = ACTIONS(128),
    [anon_sym_GLOBAL] = ACTIONS(128),
    [anon_sym_AS] = ACTIONS(128),
    [anon_sym_COPY] = ACTIONS(128),
    [anon_sym_REPLACING] = ACTIONS(128),
    [anon_sym_OF] = ACTIONS(128),
    [anon_sym_IN] = ACTIONS(128),
    [anon_sym_REPLACE] = ACTIONS(128),
    [anon_sym_OFF] = ACTIONS(128),
    [anon_sym_EJECT] = ACTIONS(128),
    [anon_sym_SKIP1] = ACTIONS(128),
    [anon_sym_SKIP2] = ACTIONS(128),
    [anon_sym_SKIP3] = ACTIONS(128),
    [anon_sym_EXEC] = ACTIONS(128),
    [anon_sym_EXECUTE] = ACTIONS(128),
    [anon_sym_SQL] = ACTIONS(128),
    [anon_sym_SQLIMS] = ACTIONS(128),
    [anon_sym_DLI] = ACTIONS(128),
    [anon_sym_END_DASHEXEC] = ACTIONS(128),
    [anon_sym_IF] = ACTIONS(128),
    [anon_sym_ELSE] = ACTIONS(128),
    [anon_sym_END_DASHIF] = ACTIONS(128),
    [anon_sym_THEN] = ACTIONS(128),
    [anon_sym_EVALUATE] = ACTIONS(128),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(128),
    [anon_sym_OTHER] = ACTIONS(128),
    [anon_sym_ALSO] = ACTIONS(128),
    [anon_sym_PERFORM] = ACTIONS(128),
    [anon_sym_END_DASHPERFORM] = ACTIONS(128),
    [anon_sym_UNTIL] = ACTIONS(128),
    [anon_sym_VARYING] = ACTIONS(128),
    [anon_sym_WITH] = ACTIONS(128),
    [anon_sym_TEST] = ACTIONS(128),
    [anon_sym_BEFORE] = ACTIONS(128),
    [anon_sym_AFTER] = ACTIONS(128),
    [anon_sym_GO] = ACTIONS(128),
    [anon_sym_SECTION] = ACTIONS(128),
    [anon_sym_PARAGRAPH] = ACTIONS(128),
    [anon_sym_CONTINUE] = ACTIONS(128),
    [anon_sym_NEXT] = ACTIONS(128),
    [anon_sym_SENTENCE] = ACTIONS(128),
    [anon_sym_EXIT] = ACTIONS(128),
    [anon_sym_STOP] = ACTIONS(128),
    [anon_sym_RUN] = ACTIONS(128),
    [anon_sym_MOVE] = ACTIONS(128),
    [anon_sym_CORRESPONDING] = ACTIONS(128),
    [anon_sym_CORR] = ACTIONS(128),
    [anon_sym_INTO] = ACTIONS(128),
    [anon_sym_SET] = ACTIONS(128),
    [anon_sym_TRUE] = ACTIONS(128),
    [anon_sym_FALSE] = ACTIONS(128),
    [anon_sym_INITIALIZE] = ACTIONS(128),
    [anon_sym_ALPHABETIC] = ACTIONS(128),
    [anon_sym_ALPHANUMERIC] = ACTIONS(128),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(128),
    [anon_sym_NUMERIC] = ACTIONS(128),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(128),
    [anon_sym_COMPUTE] = ACTIONS(128),
    [anon_sym_ADD] = ACTIONS(128),
    [anon_sym_SUBTRACT] = ACTIONS(128),
    [anon_sym_MULTIPLY] = ACTIONS(128),
    [anon_sym_DIVIDE] = ACTIONS(128),
    [anon_sym_GIVING] = ACTIONS(128),
    [anon_sym_REMAINDER] = ACTIONS(128),
    [anon_sym_STRING] = ACTIONS(128),
    [anon_sym_DELIMITED] = ACTIONS(128),
    [anon_sym_SIZE] = ACTIONS(128),
    [anon_sym_OVERFLOW] = ACTIONS(128),
    [anon_sym_NOT] = ACTIONS(128),
    [anon_sym_END_DASHSTRING] = ACTIONS(128),
    [anon_sym_UNSTRING] = ACTIONS(128),
    [anon_sym_COUNT] = ACTIONS(128),
    [anon_sym_DELIMITER] = ACTIONS(128),
    [anon_sym_TALLYING] = ACTIONS(128),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(128),
    [anon_sym_INSPECT] = ACTIONS(128),
    [anon_sym_CONVERTING] = ACTIONS(128),
    [anon_sym_FIRST] = ACTIONS(128),
    [anon_sym_INITIAL] = ACTIONS(128),
    [anon_sym_READ] = ACTIONS(128),
    [anon_sym_WRITE] = ACTIONS(128),
    [anon_sym_REWRITE] = ACTIONS(128),
    [anon_sym_DELETE] = ACTIONS(128),
    [anon_sym_START] = ACTIONS(128),
    [anon_sym_OPEN] = ACTIONS(128),
    [anon_sym_CLOSE] = ACTIONS(128),
    [anon_sym_INPUT] = ACTIONS(128),
    [anon_sym_OUTPUT] = ACTIONS(128),
    [anon_sym_I_DASHO] = ACTIONS(128),
    [anon_sym_EXTEND] = ACTIONS(128),
    [anon_sym_ACCEPT] = ACTIONS(128),
    [anon_sym_FROM] = ACTIONS(128),
    [anon_sym_DATE] = ACTIONS(128),
    [anon_sym_DAY] = ACTIONS(128),
    [anon_sym_TIME] = ACTIONS(128),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(128),
    [anon_sym_EQUAL] = ACTIONS(128),
    [anon_sym_GREATER] = ACTIONS(128),
    [anon_sym_LESS] = ACTIONS(128),
    [anon_sym_THAN] = ACTIONS(128),
    [anon_sym_OR] = ACTIONS(128),
    [anon_sym_AND] = ACTIONS(128),
    [anon_sym_DFHENTER] = ACTIONS(128),
    [anon_sym_DFHCLEAR] = ACTIONS(128),
    [anon_sym_DFHPA1] = ACTIONS(128),
    [anon_sym_DFHPA2] = ACTIONS(128),
    [anon_sym_DFHPF1] = ACTIONS(128),
    [anon_sym_DFHPF2] = ACTIONS(128),
    [anon_sym_DFHPF3] = ACTIONS(128),
    [anon_sym_DFHPF4] = ACTIONS(128),
    [anon_sym_DFHPF5] = ACTIONS(128),
    [anon_sym_DFHPF6] = ACTIONS(128),
    [anon_sym_DFHPF7] = ACTIONS(128),
    [anon_sym_DFHPF8] = ACTIONS(128),
    [anon_sym_DFHPF9] = ACTIONS(128),
    [anon_sym_DFHPF10] = ACTIONS(128),
    [anon_sym_DFHPF11] = ACTIONS(128),
    [anon_sym_DFHPF12] = ACTIONS(128),
    [anon_sym_EIBAID] = ACTIONS(128),
    [anon_sym_DFHRED] = ACTIONS(128),
    [anon_sym_DFHBMASB] = ACTIONS(128),
    [anon_sym_DFHBMASK] = ACTIONS(128),
    [aux_sym_identifier_token1] = ACTIONS(128),
    [aux_sym_identifier_token2] = ACTIONS(124),
    [sym_picture_string] = ACTIONS(128),
    [aux_sym_string_literal_token1] = ACTIONS(124),
    [aux_sym_string_literal_token2] = ACTIONS(124),
    [sym_number] = ACTIONS(128),
    [anon_sym_EQ_EQ] = ACTIONS(124),
    [anon_sym_EQ] = ACTIONS(128),
    [anon_sym_GT] = ACTIONS(128),
    [anon_sym_LT] = ACTIONS(128),
    [anon_sym_GT_EQ] = ACTIONS(124),
    [anon_sym_LT_EQ] = ACTIONS(124),
    [anon_sym_COMMA] = ACTIONS(128),
    [anon_sym_LPAREN] = ACTIONS(128),
    [anon_sym_RPAREN] = ACTIONS(124),
    [anon_sym_COLON] = ACTIONS(124),
  },
  [8] = {
    [sym_identifier] = STATE(26),
    [sym_string_literal] = STATE(26),
    [aux_sym_parenthesized_repeat1] = STATE(26),
    [aux_sym_newline_token1] = ACTIONS(130),
    [anon_sym_DOT] = ACTIONS(130),
    [anon_sym_88] = ACTIONS(132),
    [anon_sym_VALUE] = ACTIONS(132),
    [anon_sym_IS] = ACTIONS(132),
    [aux_sym_level_number_token1] = ACTIONS(132),
    [aux_sym_level_number_token2] = ACTIONS(132),
    [anon_sym_66] = ACTIONS(132),
    [anon_sym_77] = ACTIONS(132),
    [anon_sym_FILLER] = ACTIONS(132),
    [anon_sym_PIC] = ACTIONS(132),
    [anon_sym_PICTURE] = ACTIONS(132),
    [anon_sym_VALUES] = ACTIONS(132),
    [anon_sym_OCCURS] = ACTIONS(132),
    [anon_sym_TIMES] = ACTIONS(132),
    [anon_sym_TO] = ACTIONS(132),
    [anon_sym_REDEFINES] = ACTIONS(132),
    [anon_sym_INDEXED] = ACTIONS(132),
    [anon_sym_BY] = ACTIONS(132),
    [anon_sym_DEPENDING] = ACTIONS(132),
    [anon_sym_ON] = ACTIONS(132),
    [anon_sym_USAGE] = ACTIONS(132),
    [anon_sym_DISPLAY] = ACTIONS(132),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(132),
    [anon_sym_BINARY] = ACTIONS(132),
    [anon_sym_COMP] = ACTIONS(132),
    [anon_sym_COMP_DASH1] = ACTIONS(132),
    [anon_sym_COMP_DASH2] = ACTIONS(132),
    [anon_sym_COMP_DASH3] = ACTIONS(132),
    [anon_sym_COMP_DASH4] = ACTIONS(132),
    [anon_sym_COMP_DASH5] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(132),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(132),
    [anon_sym_INDEX] = ACTIONS(132),
    [anon_sym_POINTER] = ACTIONS(132),
    [anon_sym_ZERO] = ACTIONS(132),
    [anon_sym_ZEROS] = ACTIONS(132),
    [anon_sym_ZEROES] = ACTIONS(132),
    [anon_sym_SPACE] = ACTIONS(132),
    [anon_sym_SPACES] = ACTIONS(132),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(132),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(132),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(132),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(132),
    [anon_sym_QUOTE] = ACTIONS(132),
    [anon_sym_QUOTES] = ACTIONS(132),
    [anon_sym_NULL] = ACTIONS(132),
    [anon_sym_NULLS] = ACTIONS(132),
    [anon_sym_ALL] = ACTIONS(132),
    [anon_sym_THRU] = ACTIONS(132),
    [anon_sym_THROUGH] = ACTIONS(132),
    [anon_sym_ASCENDING] = ACTIONS(132),
    [anon_sym_DESCENDING] = ACTIONS(132),
    [anon_sym_KEY] = ACTIONS(132),
    [anon_sym_SIGN] = ACTIONS(132),
    [anon_sym_LEADING] = ACTIONS(132),
    [anon_sym_TRAILING] = ACTIONS(132),
    [anon_sym_SEPARATE] = ACTIONS(132),
    [anon_sym_CHARACTER] = ACTIONS(132),
    [anon_sym_SYNC] = ACTIONS(132),
    [anon_sym_SYNCHRONIZED] = ACTIONS(132),
    [anon_sym_LEFT] = ACTIONS(132),
    [anon_sym_RIGHT] = ACTIONS(132),
    [anon_sym_JUST] = ACTIONS(132),
    [anon_sym_JUSTIFIED] = ACTIONS(132),
    [anon_sym_BLANK] = ACTIONS(132),
    [anon_sym_WHEN] = ACTIONS(132),
    [anon_sym_EXTERNAL] = ACTIONS(132),
    [anon_sym_GLOBAL] = ACTIONS(132),
    [anon_sym_AS] = ACTIONS(132),
    [anon_sym_COPY] = ACTIONS(132),
    [anon_sym_REPLACING] = ACTIONS(132),
    [anon_sym_OF] = ACTIONS(132),
    [anon_sym_IN] = ACTIONS(132),
    [anon_sym_REPLACE] = ACTIONS(132),
    [anon_sym_OFF] = ACTIONS(132),
    [anon_sym_EJECT] = ACTIONS(132),
    [anon_sym_SKIP1] = ACTIONS(132),
    [anon_sym_SKIP2] = ACTIONS(132),
    [anon_sym_SKIP3] = ACTIONS(132),
    [anon_sym_EXEC] = ACTIONS(132),
    [anon_sym_EXECUTE] = ACTIONS(132),
    [anon_sym_SQL] = ACTIONS(132),
    [anon_sym_SQLIMS] = ACTIONS(132),
    [anon_sym_DLI] = ACTIONS(132),
    [anon_sym_END_DASHEXEC] = ACTIONS(132),
    [anon_sym_IF] = ACTIONS(132),
    [anon_sym_ELSE] = ACTIONS(132),
    [anon_sym_END_DASHIF] = ACTIONS(132),
    [anon_sym_THEN] = ACTIONS(132),
    [anon_sym_EVALUATE] = ACTIONS(132),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(132),
    [anon_sym_OTHER] = ACTIONS(132),
    [anon_sym_ALSO] = ACTIONS(132),
    [anon_sym_PERFORM] = ACTIONS(132),
    [anon_sym_END_DASHPERFORM] = ACTIONS(132),
    [anon_sym_UNTIL] = ACTIONS(132),
    [anon_sym_VARYING] = ACTIONS(132),
    [anon_sym_WITH] = ACTIONS(132),
    [anon_sym_TEST] = ACTIONS(132),
    [anon_sym_BEFORE] = ACTIONS(132),
    [anon_sym_AFTER] = ACTIONS(132),
    [anon_sym_GO] = ACTIONS(132),
    [anon_sym_SECTION] = ACTIONS(132),
    [anon_sym_PARAGRAPH] = ACTIONS(132),
    [anon_sym_CONTINUE] = ACTIONS(132),
    [anon_sym_NEXT] = ACTIONS(132),
    [anon_sym_SENTENCE] = ACTIONS(132),
    [anon_sym_EXIT] = ACTIONS(132),
    [anon_sym_STOP] = ACTIONS(132),
    [anon_sym_RUN] = ACTIONS(132),
    [anon_sym_MOVE] = ACTIONS(132),
    [anon_sym_CORRESPONDING] = ACTIONS(132),
    [anon_sym_CORR] = ACTIONS(132),
    [anon_sym_INTO] = ACTIONS(132),
    [anon_sym_SET] = ACTIONS(132),
    [anon_sym_TRUE] = ACTIONS(132),
    [anon_sym_FALSE] = ACTIONS(132),
    [anon_sym_INITIALIZE] = ACTIONS(132),
    [anon_sym_ALPHABETIC] = ACTIONS(132),
    [anon_sym_ALPHANUMERIC] = ACTIONS(132),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(132),
    [anon_sym_NUMERIC] = ACTIONS(132),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(132),
    [anon_sym_COMPUTE] = ACTIONS(132),
    [anon_sym_ADD] = ACTIONS(132),
    [anon_sym_SUBTRACT] = ACTIONS(132),
    [anon_sym_MULTIPLY] = ACTIONS(132),
    [anon_sym_DIVIDE] = ACTIONS(132),
    [anon_sym_GIVING] = ACTIONS(132),
    [anon_sym_REMAINDER] = ACTIONS(132),
    [anon_sym_STRING] = ACTIONS(132),
    [anon_sym_DELIMITED] = ACTIONS(132),
    [anon_sym_SIZE] = ACTIONS(132),
    [anon_sym_OVERFLOW] = ACTIONS(132),
    [anon_sym_NOT] = ACTIONS(132),
    [anon_sym_END_DASHSTRING] = ACTIONS(132),
    [anon_sym_UNSTRING] = ACTIONS(132),
    [anon_sym_COUNT] = ACTIONS(132),
    [anon_sym_DELIMITER] = ACTIONS(132),
    [anon_sym_TALLYING] = ACTIONS(132),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(132),
    [anon_sym_INSPECT] = ACTIONS(132),
    [anon_sym_CONVERTING] = ACTIONS(132),
    [anon_sym_FIRST] = ACTIONS(132),
    [anon_sym_INITIAL] = ACTIONS(132),
    [anon_sym_READ] = ACTIONS(132),
    [anon_sym_WRITE] = ACTIONS(132),
    [anon_sym_REWRITE] = ACTIONS(132),
    [anon_sym_DELETE] = ACTIONS(132),
    [anon_sym_START] = ACTIONS(132),
    [anon_sym_OPEN] = ACTIONS(132),
    [anon_sym_CLOSE] = ACTIONS(132),
    [anon_sym_INPUT] = ACTIONS(132),
    [anon_sym_OUTPUT] = ACTIONS(132),
    [anon_sym_I_DASHO] = ACTIONS(132),
    [anon_sym_EXTEND] = ACTIONS(132),
    [anon_sym_ACCEPT] = ACTIONS(132),
    [anon_sym_FROM] = ACTIONS(132),
    [anon_sym_DATE] = ACTIONS(132),
    [anon_sym_DAY] = ACTIONS(132),
    [anon_sym_TIME] = ACTIONS(132),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(132),
    [anon_sym_EQUAL] = ACTIONS(132),
    [anon_sym_GREATER] = ACTIONS(132),
    [anon_sym_LESS] = ACTIONS(132),
    [anon_sym_THAN] = ACTIONS(132),
    [anon_sym_OR] = ACTIONS(132),
    [anon_sym_AND] = ACTIONS(132),
    [anon_sym_DFHENTER] = ACTIONS(132),
    [anon_sym_DFHCLEAR] = ACTIONS(132),
    [anon_sym_DFHPA1] = ACTIONS(132),
    [anon_sym_DFHPA2] = ACTIONS(132),
    [anon_sym_DFHPF1] = ACTIONS(132),
    [anon_sym_DFHPF2] = ACTIONS(132),
    [anon_sym_DFHPF3] = ACTIONS(132),
    [anon_sym_DFHPF4] = ACTIONS(132),
    [anon_sym_DFHPF5] = ACTIONS(132),
    [anon_sym_DFHPF6] = ACTIONS(132),
    [anon_sym_DFHPF7] = ACTIONS(132),
    [anon_sym_DFHPF8] = ACTIONS(132),
    [anon_sym_DFHPF9] = ACTIONS(132),
    [anon_sym_DFHPF10] = ACTIONS(132),
    [anon_sym_DFHPF11] = ACTIONS(132),
    [anon_sym_DFHPF12] = ACTIONS(132),
    [anon_sym_EIBAID] = ACTIONS(132),
    [anon_sym_DFHRED] = ACTIONS(132),
    [anon_sym_DFHBMASB] = ACTIONS(132),
    [anon_sym_DFHBMASK] = ACTIONS(132),
    [aux_sym_identifier_token1] = ACTIONS(134),
    [aux_sym_identifier_token2] = ACTIONS(136),
    [sym_picture_string] = ACTIONS(132),
    [aux_sym_string_literal_token1] = ACTIONS(138),
    [aux_sym_string_literal_token2] = ACTIONS(138),
    [sym_number] = ACTIONS(140),
    [anon_sym_EQ_EQ] = ACTIONS(130),
    [anon_sym_EQ] = ACTIONS(132),
    [anon_sym_GT] = ACTIONS(132),
    [anon_sym_LT] = ACTIONS(132),
    [anon_sym_GT_EQ] = ACTIONS(130),
    [anon_sym_LT_EQ] = ACTIONS(130),
    [anon_sym_COMMA] = ACTIONS(140),
    [anon_sym_LPAREN] = ACTIONS(132),
    [anon_sym_RPAREN] = ACTIONS(142),
    [anon_sym_COLON] = ACTIONS(130),
  },
  [9] = {
    [ts_builtin_sym_end] = ACTIONS(144),
    [aux_sym_newline_token1] = ACTIONS(144),
    [aux_sym_comment_line_token1] = ACTIONS(144),
    [sym_sequence_number] = ACTIONS(146),
    [anon_sym_DOT] = ACTIONS(144),
    [anon_sym_88] = ACTIONS(146),
    [anon_sym_VALUE] = ACTIONS(146),
    [anon_sym_IS] = ACTIONS(146),
    [aux_sym_level_number_token1] = ACTIONS(146),
    [aux_sym_level_number_token2] = ACTIONS(146),
    [anon_sym_66] = ACTIONS(146),
    [anon_sym_77] = ACTIONS(146),
    [anon_sym_FILLER] = ACTIONS(146),
    [anon_sym_PIC] = ACTIONS(146),
    [anon_sym_PICTURE] = ACTIONS(146),
    [anon_sym_VALUES] = ACTIONS(146),
    [anon_sym_OCCURS] = ACTIONS(146),
    [anon_sym_TIMES] = ACTIONS(146),
    [anon_sym_TO] = ACTIONS(146),
    [anon_sym_REDEFINES] = ACTIONS(146),
    [anon_sym_INDEXED] = ACTIONS(146),
    [anon_sym_BY] = ACTIONS(146),
    [anon_sym_DEPENDING] = ACTIONS(146),
    [anon_sym_ON] = ACTIONS(146),
    [anon_sym_USAGE] = ACTIONS(146),
    [anon_sym_DISPLAY] = ACTIONS(146),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(146),
    [anon_sym_BINARY] = ACTIONS(146),
    [anon_sym_COMP] = ACTIONS(146),
    [anon_sym_COMP_DASH1] = ACTIONS(146),
    [anon_sym_COMP_DASH2] = ACTIONS(146),
    [anon_sym_COMP_DASH3] = ACTIONS(146),
    [anon_sym_COMP_DASH4] = ACTIONS(146),
    [anon_sym_COMP_DASH5] = ACTIONS(146),
    [anon_sym_COMPUTATIONAL] = ACTIONS(146),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(146),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(146),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(146),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(146),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(146),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(146),
    [anon_sym_INDEX] = ACTIONS(146),
    [anon_sym_POINTER] = ACTIONS(146),
    [anon_sym_ZERO] = ACTIONS(146),
    [anon_sym_ZEROS] = ACTIONS(146),
    [anon_sym_ZEROES] = ACTIONS(146),
    [anon_sym_SPACE] = ACTIONS(146),
    [anon_sym_SPACES] = ACTIONS(146),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(146),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(146),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(146),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(146),
    [anon_sym_QUOTE] = ACTIONS(146),
    [anon_sym_QUOTES] = ACTIONS(146),
    [anon_sym_NULL] = ACTIONS(146),
    [anon_sym_NULLS] = ACTIONS(146),
    [anon_sym_ALL] = ACTIONS(146),
    [anon_sym_THRU] = ACTIONS(146),
    [anon_sym_THROUGH] = ACTIONS(146),
    [anon_sym_ASCENDING] = ACTIONS(146),
    [anon_sym_DESCENDING] = ACTIONS(146),
    [anon_sym_KEY] = ACTIONS(146),
    [anon_sym_SIGN] = ACTIONS(146),
    [anon_sym_LEADING] = ACTIONS(146),
    [anon_sym_TRAILING] = ACTIONS(146),
    [anon_sym_SEPARATE] = ACTIONS(146),
    [anon_sym_CHARACTER] = ACTIONS(146),
    [anon_sym_SYNC] = ACTIONS(146),
    [anon_sym_SYNCHRONIZED] = ACTIONS(146),
    [anon_sym_LEFT] = ACTIONS(146),
    [anon_sym_RIGHT] = ACTIONS(146),
    [anon_sym_JUST] = ACTIONS(146),
    [anon_sym_JUSTIFIED] = ACTIONS(146),
    [anon_sym_BLANK] = ACTIONS(146),
    [anon_sym_WHEN] = ACTIONS(146),
    [anon_sym_EXTERNAL] = ACTIONS(146),
    [anon_sym_GLOBAL] = ACTIONS(146),
    [anon_sym_AS] = ACTIONS(146),
    [anon_sym_COPY] = ACTIONS(146),
    [anon_sym_REPLACING] = ACTIONS(146),
    [anon_sym_OF] = ACTIONS(146),
    [anon_sym_IN] = ACTIONS(146),
    [anon_sym_REPLACE] = ACTIONS(146),
    [anon_sym_OFF] = ACTIONS(146),
    [anon_sym_EJECT] = ACTIONS(146),
    [anon_sym_SKIP1] = ACTIONS(146),
    [anon_sym_SKIP2] = ACTIONS(146),
    [anon_sym_SKIP3] = ACTIONS(146),
    [anon_sym_EXEC] = ACTIONS(146),
    [anon_sym_EXECUTE] = ACTIONS(146),
    [anon_sym_SQL] = ACTIONS(146),
    [anon_sym_SQLIMS] = ACTIONS(146),
    [anon_sym_DLI] = ACTIONS(146),
    [anon_sym_END_DASHEXEC] = ACTIONS(146),
    [anon_sym_IF] = ACTIONS(146),
    [anon_sym_ELSE] = ACTIONS(146),
    [anon_sym_END_DASHIF] = ACTIONS(146),
    [anon_sym_THEN] = ACTIONS(146),
    [anon_sym_EVALUATE] = ACTIONS(146),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(146),
    [anon_sym_OTHER] = ACTIONS(146),
    [anon_sym_ALSO] = ACTIONS(146),
    [anon_sym_PERFORM] = ACTIONS(146),
    [anon_sym_END_DASHPERFORM] = ACTIONS(146),
    [anon_sym_UNTIL] = ACTIONS(146),
    [anon_sym_VARYING] = ACTIONS(146),
    [anon_sym_WITH] = ACTIONS(146),
    [anon_sym_TEST] = ACTIONS(146),
    [anon_sym_BEFORE] = ACTIONS(146),
    [anon_sym_AFTER] = ACTIONS(146),
    [anon_sym_GO] = ACTIONS(146),
    [anon_sym_SECTION] = ACTIONS(146),
    [anon_sym_PARAGRAPH] = ACTIONS(146),
    [anon_sym_CONTINUE] = ACTIONS(146),
    [anon_sym_NEXT] = ACTIONS(146),
    [anon_sym_SENTENCE] = ACTIONS(146),
    [anon_sym_EXIT] = ACTIONS(146),
    [anon_sym_STOP] = ACTIONS(146),
    [anon_sym_RUN] = ACTIONS(146),
    [anon_sym_MOVE] = ACTIONS(146),
    [anon_sym_CORRESPONDING] = ACTIONS(146),
    [anon_sym_CORR] = ACTIONS(146),
    [anon_sym_INTO] = ACTIONS(146),
    [anon_sym_SET] = ACTIONS(146),
    [anon_sym_TRUE] = ACTIONS(146),
    [anon_sym_FALSE] = ACTIONS(146),
    [anon_sym_INITIALIZE] = ACTIONS(146),
    [anon_sym_ALPHABETIC] = ACTIONS(146),
    [anon_sym_ALPHANUMERIC] = ACTIONS(146),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(146),
    [anon_sym_NUMERIC] = ACTIONS(146),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(146),
    [anon_sym_COMPUTE] = ACTIONS(146),
    [anon_sym_ADD] = ACTIONS(146),
    [anon_sym_SUBTRACT] = ACTIONS(146),
    [anon_sym_MULTIPLY] = ACTIONS(146),
    [anon_sym_DIVIDE] = ACTIONS(146),
    [anon_sym_GIVING] = ACTIONS(146),
    [anon_sym_REMAINDER] = ACTIONS(146),
    [anon_sym_STRING] = ACTIONS(146),
    [anon_sym_DELIMITED] = ACTIONS(146),
    [anon_sym_SIZE] = ACTIONS(146),
    [anon_sym_OVERFLOW] = ACTIONS(146),
    [anon_sym_NOT] = ACTIONS(146),
    [anon_sym_END_DASHSTRING] = ACTIONS(146),
    [anon_sym_UNSTRING] = ACTIONS(146),
    [anon_sym_COUNT] = ACTIONS(146),
    [anon_sym_DELIMITER] = ACTIONS(146),
    [anon_sym_TALLYING] = ACTIONS(146),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(146),
    [anon_sym_INSPECT] = ACTIONS(146),
    [anon_sym_CONVERTING] = ACTIONS(146),
    [anon_sym_FIRST] = ACTIONS(146),
    [anon_sym_INITIAL] = ACTIONS(146),
    [anon_sym_READ] = ACTIONS(146),
    [anon_sym_WRITE] = ACTIONS(146),
    [anon_sym_REWRITE] = ACTIONS(146),
    [anon_sym_DELETE] = ACTIONS(146),
    [anon_sym_START] = ACTIONS(146),
    [anon_sym_OPEN] = ACTIONS(146),
    [anon_sym_CLOSE] = ACTIONS(146),
    [anon_sym_INPUT] = ACTIONS(146),
    [anon_sym_OUTPUT] = ACTIONS(146),
    [anon_sym_I_DASHO] = ACTIONS(146),
    [anon_sym_EXTEND] = ACTIONS(146),
    [anon_sym_ACCEPT] = ACTIONS(146),
    [anon_sym_FROM] = ACTIONS(146),
    [anon_sym_DATE] = ACTIONS(146),
    [anon_sym_DAY] = ACTIONS(146),
    [anon_sym_TIME] = ACTIONS(146),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(146),
    [anon_sym_EQUAL] = ACTIONS(146),
    [anon_sym_GREATER] = ACTIONS(146),
    [anon_sym_LESS] = ACTIONS(146),
    [anon_sym_THAN] = ACTIONS(146),
    [anon_sym_OR] = ACTIONS(146),
    [anon_sym_AND] = ACTIONS(146),
    [anon_sym_DFHENTER] = ACTIONS(146),
    [anon_sym_DFHCLEAR] = ACTIONS(146),
    [anon_sym_DFHPA1] = ACTIONS(146),
    [anon_sym_DFHPA2] = ACTIONS(146),
    [anon_sym_DFHPF1] = ACTIONS(146),
    [anon_sym_DFHPF2] = ACTIONS(146),
    [anon_sym_DFHPF3] = ACTIONS(146),
    [anon_sym_DFHPF4] = ACTIONS(146),
    [anon_sym_DFHPF5] = ACTIONS(146),
    [anon_sym_DFHPF6] = ACTIONS(146),
    [anon_sym_DFHPF7] = ACTIONS(146),
    [anon_sym_DFHPF8] = ACTIONS(146),
    [anon_sym_DFHPF9] = ACTIONS(146),
    [anon_sym_DFHPF10] = ACTIONS(146),
    [anon_sym_DFHPF11] = ACTIONS(146),
    [anon_sym_DFHPF12] = ACTIONS(146),
    [anon_sym_EIBAID] = ACTIONS(146),
    [anon_sym_DFHRED] = ACTIONS(146),
    [anon_sym_DFHBMASB] = ACTIONS(146),
    [anon_sym_DFHBMASK] = ACTIONS(146),
    [aux_sym_identifier_token1] = ACTIONS(146),
    [aux_sym_identifier_token2] = ACTIONS(144),
    [sym_picture_string] = ACTIONS(146),
    [aux_sym_string_literal_token1] = ACTIONS(144),
    [aux_sym_string_literal_token2] = ACTIONS(144),
    [sym_number] = ACTIONS(146),
    [anon_sym_EQ_EQ] = ACTIONS(144),
    [anon_sym_EQ] = ACTIONS(146),
    [anon_sym_GT] = ACTIONS(146),
    [anon_sym_LT] = ACTIONS(146),
    [anon_sym_GT_EQ] = ACTIONS(144),
    [anon_sym_LT_EQ] = ACTIONS(144),
    [anon_sym_COMMA] = ACTIONS(146),
    [anon_sym_LPAREN] = ACTIONS(146),
    [anon_sym_RPAREN] = ACTIONS(144),
    [anon_sym_COLON] = ACTIONS(144),
  },
  [10] = {
    [ts_builtin_sym_end] = ACTIONS(148),
    [aux_sym_newline_token1] = ACTIONS(148),
    [aux_sym_comment_line_token1] = ACTIONS(148),
    [sym_sequence_number] = ACTIONS(150),
    [anon_sym_DOT] = ACTIONS(148),
    [anon_sym_88] = ACTIONS(150),
    [anon_sym_VALUE] = ACTIONS(150),
    [anon_sym_IS] = ACTIONS(150),
    [aux_sym_level_number_token1] = ACTIONS(150),
    [aux_sym_level_number_token2] = ACTIONS(150),
    [anon_sym_66] = ACTIONS(150),
    [anon_sym_77] = ACTIONS(150),
    [anon_sym_FILLER] = ACTIONS(150),
    [anon_sym_PIC] = ACTIONS(150),
    [anon_sym_PICTURE] = ACTIONS(150),
    [anon_sym_VALUES] = ACTIONS(150),
    [anon_sym_OCCURS] = ACTIONS(150),
    [anon_sym_TIMES] = ACTIONS(150),
    [anon_sym_TO] = ACTIONS(150),
    [anon_sym_REDEFINES] = ACTIONS(150),
    [anon_sym_INDEXED] = ACTIONS(150),
    [anon_sym_BY] = ACTIONS(150),
    [anon_sym_DEPENDING] = ACTIONS(150),
    [anon_sym_ON] = ACTIONS(150),
    [anon_sym_USAGE] = ACTIONS(150),
    [anon_sym_DISPLAY] = ACTIONS(150),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(150),
    [anon_sym_BINARY] = ACTIONS(150),
    [anon_sym_COMP] = ACTIONS(150),
    [anon_sym_COMP_DASH1] = ACTIONS(150),
    [anon_sym_COMP_DASH2] = ACTIONS(150),
    [anon_sym_COMP_DASH3] = ACTIONS(150),
    [anon_sym_COMP_DASH4] = ACTIONS(150),
    [anon_sym_COMP_DASH5] = ACTIONS(150),
    [anon_sym_COMPUTATIONAL] = ACTIONS(150),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(150),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(150),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(150),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(150),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(150),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(150),
    [anon_sym_INDEX] = ACTIONS(150),
    [anon_sym_POINTER] = ACTIONS(150),
    [anon_sym_ZERO] = ACTIONS(150),
    [anon_sym_ZEROS] = ACTIONS(150),
    [anon_sym_ZEROES] = ACTIONS(150),
    [anon_sym_SPACE] = ACTIONS(150),
    [anon_sym_SPACES] = ACTIONS(150),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(150),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(150),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(150),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(150),
    [anon_sym_QUOTE] = ACTIONS(150),
    [anon_sym_QUOTES] = ACTIONS(150),
    [anon_sym_NULL] = ACTIONS(150),
    [anon_sym_NULLS] = ACTIONS(150),
    [anon_sym_ALL] = ACTIONS(150),
    [anon_sym_THRU] = ACTIONS(150),
    [anon_sym_THROUGH] = ACTIONS(150),
    [anon_sym_ASCENDING] = ACTIONS(150),
    [anon_sym_DESCENDING] = ACTIONS(150),
    [anon_sym_KEY] = ACTIONS(150),
    [anon_sym_SIGN] = ACTIONS(150),
    [anon_sym_LEADING] = ACTIONS(150),
    [anon_sym_TRAILING] = ACTIONS(150),
    [anon_sym_SEPARATE] = ACTIONS(150),
    [anon_sym_CHARACTER] = ACTIONS(150),
    [anon_sym_SYNC] = ACTIONS(150),
    [anon_sym_SYNCHRONIZED] = ACTIONS(150),
    [anon_sym_LEFT] = ACTIONS(150),
    [anon_sym_RIGHT] = ACTIONS(150),
    [anon_sym_JUST] = ACTIONS(150),
    [anon_sym_JUSTIFIED] = ACTIONS(150),
    [anon_sym_BLANK] = ACTIONS(150),
    [anon_sym_WHEN] = ACTIONS(150),
    [anon_sym_EXTERNAL] = ACTIONS(150),
    [anon_sym_GLOBAL] = ACTIONS(150),
    [anon_sym_AS] = ACTIONS(150),
    [anon_sym_COPY] = ACTIONS(150),
    [anon_sym_REPLACING] = ACTIONS(150),
    [anon_sym_OF] = ACTIONS(150),
    [anon_sym_IN] = ACTIONS(150),
    [anon_sym_REPLACE] = ACTIONS(150),
    [anon_sym_OFF] = ACTIONS(150),
    [anon_sym_EJECT] = ACTIONS(150),
    [anon_sym_SKIP1] = ACTIONS(150),
    [anon_sym_SKIP2] = ACTIONS(150),
    [anon_sym_SKIP3] = ACTIONS(150),
    [anon_sym_EXEC] = ACTIONS(150),
    [anon_sym_EXECUTE] = ACTIONS(150),
    [anon_sym_SQL] = ACTIONS(150),
    [anon_sym_SQLIMS] = ACTIONS(150),
    [anon_sym_DLI] = ACTIONS(150),
    [anon_sym_END_DASHEXEC] = ACTIONS(150),
    [anon_sym_IF] = ACTIONS(150),
    [anon_sym_ELSE] = ACTIONS(150),
    [anon_sym_END_DASHIF] = ACTIONS(150),
    [anon_sym_THEN] = ACTIONS(150),
    [anon_sym_EVALUATE] = ACTIONS(150),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(150),
    [anon_sym_OTHER] = ACTIONS(150),
    [anon_sym_ALSO] = ACTIONS(150),
    [anon_sym_PERFORM] = ACTIONS(150),
    [anon_sym_END_DASHPERFORM] = ACTIONS(150),
    [anon_sym_UNTIL] = ACTIONS(150),
    [anon_sym_VARYING] = ACTIONS(150),
    [anon_sym_WITH] = ACTIONS(150),
    [anon_sym_TEST] = ACTIONS(150),
    [anon_sym_BEFORE] = ACTIONS(150),
    [anon_sym_AFTER] = ACTIONS(150),
    [anon_sym_GO] = ACTIONS(150),
    [anon_sym_SECTION] = ACTIONS(150),
    [anon_sym_PARAGRAPH] = ACTIONS(150),
    [anon_sym_CONTINUE] = ACTIONS(150),
    [anon_sym_NEXT] = ACTIONS(150),
    [anon_sym_SENTENCE] = ACTIONS(150),
    [anon_sym_EXIT] = ACTIONS(150),
    [anon_sym_STOP] = ACTIONS(150),
    [anon_sym_RUN] = ACTIONS(150),
    [anon_sym_MOVE] = ACTIONS(150),
    [anon_sym_CORRESPONDING] = ACTIONS(150),
    [anon_sym_CORR] = ACTIONS(150),
    [anon_sym_INTO] = ACTIONS(150),
    [anon_sym_SET] = ACTIONS(150),
    [anon_sym_TRUE] = ACTIONS(150),
    [anon_sym_FALSE] = ACTIONS(150),
    [anon_sym_INITIALIZE] = ACTIONS(150),
    [anon_sym_ALPHABETIC] = ACTIONS(150),
    [anon_sym_ALPHANUMERIC] = ACTIONS(150),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(150),
    [anon_sym_NUMERIC] = ACTIONS(150),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(150),
    [anon_sym_COMPUTE] = ACTIONS(150),
    [anon_sym_ADD] = ACTIONS(150),
    [anon_sym_SUBTRACT] = ACTIONS(150),
    [anon_sym_MULTIPLY] = ACTIONS(150),
    [anon_sym_DIVIDE] = ACTIONS(150),
    [anon_sym_GIVING] = ACTIONS(150),
    [anon_sym_REMAINDER] = ACTIONS(150),
    [anon_sym_STRING] = ACTIONS(150),
    [anon_sym_DELIMITED] = ACTIONS(150),
    [anon_sym_SIZE] = ACTIONS(150),
    [anon_sym_OVERFLOW] = ACTIONS(150),
    [anon_sym_NOT] = ACTIONS(150),
    [anon_sym_END_DASHSTRING] = ACTIONS(150),
    [anon_sym_UNSTRING] = ACTIONS(150),
    [anon_sym_COUNT] = ACTIONS(150),
    [anon_sym_DELIMITER] = ACTIONS(150),
    [anon_sym_TALLYING] = ACTIONS(150),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(150),
    [anon_sym_INSPECT] = ACTIONS(150),
    [anon_sym_CONVERTING] = ACTIONS(150),
    [anon_sym_FIRST] = ACTIONS(150),
    [anon_sym_INITIAL] = ACTIONS(150),
    [anon_sym_READ] = ACTIONS(150),
    [anon_sym_WRITE] = ACTIONS(150),
    [anon_sym_REWRITE] = ACTIONS(150),
    [anon_sym_DELETE] = ACTIONS(150),
    [anon_sym_START] = ACTIONS(150),
    [anon_sym_OPEN] = ACTIONS(150),
    [anon_sym_CLOSE] = ACTIONS(150),
    [anon_sym_INPUT] = ACTIONS(150),
    [anon_sym_OUTPUT] = ACTIONS(150),
    [anon_sym_I_DASHO] = ACTIONS(150),
    [anon_sym_EXTEND] = ACTIONS(150),
    [anon_sym_ACCEPT] = ACTIONS(150),
    [anon_sym_FROM] = ACTIONS(150),
    [anon_sym_DATE] = ACTIONS(150),
    [anon_sym_DAY] = ACTIONS(150),
    [anon_sym_TIME] = ACTIONS(150),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(150),
    [anon_sym_EQUAL] = ACTIONS(150),
    [anon_sym_GREATER] = ACTIONS(150),
    [anon_sym_LESS] = ACTIONS(150),
    [anon_sym_THAN] = ACTIONS(150),
    [anon_sym_OR] = ACTIONS(150),
    [anon_sym_AND] = ACTIONS(150),
    [anon_sym_DFHENTER] = ACTIONS(150),
    [anon_sym_DFHCLEAR] = ACTIONS(150),
    [anon_sym_DFHPA1] = ACTIONS(150),
    [anon_sym_DFHPA2] = ACTIONS(150),
    [anon_sym_DFHPF1] = ACTIONS(150),
    [anon_sym_DFHPF2] = ACTIONS(150),
    [anon_sym_DFHPF3] = ACTIONS(150),
    [anon_sym_DFHPF4] = ACTIONS(150),
    [anon_sym_DFHPF5] = ACTIONS(150),
    [anon_sym_DFHPF6] = ACTIONS(150),
    [anon_sym_DFHPF7] = ACTIONS(150),
    [anon_sym_DFHPF8] = ACTIONS(150),
    [anon_sym_DFHPF9] = ACTIONS(150),
    [anon_sym_DFHPF10] = ACTIONS(150),
    [anon_sym_DFHPF11] = ACTIONS(150),
    [anon_sym_DFHPF12] = ACTIONS(150),
    [anon_sym_EIBAID] = ACTIONS(150),
    [anon_sym_DFHRED] = ACTIONS(150),
    [anon_sym_DFHBMASB] = ACTIONS(150),
    [anon_sym_DFHBMASK] = ACTIONS(150),
    [aux_sym_identifier_token1] = ACTIONS(150),
    [aux_sym_identifier_token2] = ACTIONS(148),
    [sym_picture_string] = ACTIONS(150),
    [aux_sym_string_literal_token1] = ACTIONS(148),
    [aux_sym_string_literal_token2] = ACTIONS(148),
    [sym_number] = ACTIONS(150),
    [anon_sym_EQ_EQ] = ACTIONS(148),
    [anon_sym_EQ] = ACTIONS(150),
    [anon_sym_GT] = ACTIONS(150),
    [anon_sym_LT] = ACTIONS(150),
    [anon_sym_GT_EQ] = ACTIONS(148),
    [anon_sym_LT_EQ] = ACTIONS(148),
    [anon_sym_COMMA] = ACTIONS(150),
    [anon_sym_LPAREN] = ACTIONS(150),
    [anon_sym_RPAREN] = ACTIONS(148),
    [anon_sym_COLON] = ACTIONS(148),
  },
  [11] = {
    [ts_builtin_sym_end] = ACTIONS(152),
    [aux_sym_newline_token1] = ACTIONS(152),
    [aux_sym_comment_line_token1] = ACTIONS(152),
    [sym_sequence_number] = ACTIONS(154),
    [anon_sym_DOT] = ACTIONS(152),
    [anon_sym_88] = ACTIONS(154),
    [anon_sym_VALUE] = ACTIONS(154),
    [anon_sym_IS] = ACTIONS(154),
    [aux_sym_level_number_token1] = ACTIONS(154),
    [aux_sym_level_number_token2] = ACTIONS(154),
    [anon_sym_66] = ACTIONS(154),
    [anon_sym_77] = ACTIONS(154),
    [anon_sym_FILLER] = ACTIONS(154),
    [anon_sym_PIC] = ACTIONS(154),
    [anon_sym_PICTURE] = ACTIONS(154),
    [anon_sym_VALUES] = ACTIONS(154),
    [anon_sym_OCCURS] = ACTIONS(154),
    [anon_sym_TIMES] = ACTIONS(154),
    [anon_sym_TO] = ACTIONS(154),
    [anon_sym_REDEFINES] = ACTIONS(154),
    [anon_sym_INDEXED] = ACTIONS(154),
    [anon_sym_BY] = ACTIONS(154),
    [anon_sym_DEPENDING] = ACTIONS(154),
    [anon_sym_ON] = ACTIONS(154),
    [anon_sym_USAGE] = ACTIONS(154),
    [anon_sym_DISPLAY] = ACTIONS(154),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(154),
    [anon_sym_BINARY] = ACTIONS(154),
    [anon_sym_COMP] = ACTIONS(154),
    [anon_sym_COMP_DASH1] = ACTIONS(154),
    [anon_sym_COMP_DASH2] = ACTIONS(154),
    [anon_sym_COMP_DASH3] = ACTIONS(154),
    [anon_sym_COMP_DASH4] = ACTIONS(154),
    [anon_sym_COMP_DASH5] = ACTIONS(154),
    [anon_sym_COMPUTATIONAL] = ACTIONS(154),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(154),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(154),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(154),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(154),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(154),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(154),
    [anon_sym_INDEX] = ACTIONS(154),
    [anon_sym_POINTER] = ACTIONS(154),
    [anon_sym_ZERO] = ACTIONS(154),
    [anon_sym_ZEROS] = ACTIONS(154),
    [anon_sym_ZEROES] = ACTIONS(154),
    [anon_sym_SPACE] = ACTIONS(154),
    [anon_sym_SPACES] = ACTIONS(154),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(154),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(154),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(154),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(154),
    [anon_sym_QUOTE] = ACTIONS(154),
    [anon_sym_QUOTES] = ACTIONS(154),
    [anon_sym_NULL] = ACTIONS(154),
    [anon_sym_NULLS] = ACTIONS(154),
    [anon_sym_ALL] = ACTIONS(154),
    [anon_sym_THRU] = ACTIONS(154),
    [anon_sym_THROUGH] = ACTIONS(154),
    [anon_sym_ASCENDING] = ACTIONS(154),
    [anon_sym_DESCENDING] = ACTIONS(154),
    [anon_sym_KEY] = ACTIONS(154),
    [anon_sym_SIGN] = ACTIONS(154),
    [anon_sym_LEADING] = ACTIONS(154),
    [anon_sym_TRAILING] = ACTIONS(154),
    [anon_sym_SEPARATE] = ACTIONS(154),
    [anon_sym_CHARACTER] = ACTIONS(154),
    [anon_sym_SYNC] = ACTIONS(154),
    [anon_sym_SYNCHRONIZED] = ACTIONS(154),
    [anon_sym_LEFT] = ACTIONS(154),
    [anon_sym_RIGHT] = ACTIONS(154),
    [anon_sym_JUST] = ACTIONS(154),
    [anon_sym_JUSTIFIED] = ACTIONS(154),
    [anon_sym_BLANK] = ACTIONS(154),
    [anon_sym_WHEN] = ACTIONS(154),
    [anon_sym_EXTERNAL] = ACTIONS(154),
    [anon_sym_GLOBAL] = ACTIONS(154),
    [anon_sym_AS] = ACTIONS(154),
    [anon_sym_COPY] = ACTIONS(154),
    [anon_sym_REPLACING] = ACTIONS(154),
    [anon_sym_OF] = ACTIONS(154),
    [anon_sym_IN] = ACTIONS(154),
    [anon_sym_REPLACE] = ACTIONS(154),
    [anon_sym_OFF] = ACTIONS(154),
    [anon_sym_EJECT] = ACTIONS(154),
    [anon_sym_SKIP1] = ACTIONS(154),
    [anon_sym_SKIP2] = ACTIONS(154),
    [anon_sym_SKIP3] = ACTIONS(154),
    [anon_sym_EXEC] = ACTIONS(154),
    [anon_sym_EXECUTE] = ACTIONS(154),
    [anon_sym_SQL] = ACTIONS(154),
    [anon_sym_SQLIMS] = ACTIONS(154),
    [anon_sym_DLI] = ACTIONS(154),
    [anon_sym_END_DASHEXEC] = ACTIONS(154),
    [anon_sym_IF] = ACTIONS(154),
    [anon_sym_ELSE] = ACTIONS(154),
    [anon_sym_END_DASHIF] = ACTIONS(154),
    [anon_sym_THEN] = ACTIONS(154),
    [anon_sym_EVALUATE] = ACTIONS(154),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(154),
    [anon_sym_OTHER] = ACTIONS(154),
    [anon_sym_ALSO] = ACTIONS(154),
    [anon_sym_PERFORM] = ACTIONS(154),
    [anon_sym_END_DASHPERFORM] = ACTIONS(154),
    [anon_sym_UNTIL] = ACTIONS(154),
    [anon_sym_VARYING] = ACTIONS(154),
    [anon_sym_WITH] = ACTIONS(154),
    [anon_sym_TEST] = ACTIONS(154),
    [anon_sym_BEFORE] = ACTIONS(154),
    [anon_sym_AFTER] = ACTIONS(154),
    [anon_sym_GO] = ACTIONS(154),
    [anon_sym_SECTION] = ACTIONS(154),
    [anon_sym_PARAGRAPH] = ACTIONS(154),
    [anon_sym_CONTINUE] = ACTIONS(154),
    [anon_sym_NEXT] = ACTIONS(154),
    [anon_sym_SENTENCE] = ACTIONS(154),
    [anon_sym_EXIT] = ACTIONS(154),
    [anon_sym_STOP] = ACTIONS(154),
    [anon_sym_RUN] = ACTIONS(154),
    [anon_sym_MOVE] = ACTIONS(154),
    [anon_sym_CORRESPONDING] = ACTIONS(154),
    [anon_sym_CORR] = ACTIONS(154),
    [anon_sym_INTO] = ACTIONS(154),
    [anon_sym_SET] = ACTIONS(154),
    [anon_sym_TRUE] = ACTIONS(154),
    [anon_sym_FALSE] = ACTIONS(154),
    [anon_sym_INITIALIZE] = ACTIONS(154),
    [anon_sym_ALPHABETIC] = ACTIONS(154),
    [anon_sym_ALPHANUMERIC] = ACTIONS(154),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(154),
    [anon_sym_NUMERIC] = ACTIONS(154),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(154),
    [anon_sym_COMPUTE] = ACTIONS(154),
    [anon_sym_ADD] = ACTIONS(154),
    [anon_sym_SUBTRACT] = ACTIONS(154),
    [anon_sym_MULTIPLY] = ACTIONS(154),
    [anon_sym_DIVIDE] = ACTIONS(154),
    [anon_sym_GIVING] = ACTIONS(154),
    [anon_sym_REMAINDER] = ACTIONS(154),
    [anon_sym_STRING] = ACTIONS(154),
    [anon_sym_DELIMITED] = ACTIONS(154),
    [anon_sym_SIZE] = ACTIONS(154),
    [anon_sym_OVERFLOW] = ACTIONS(154),
    [anon_sym_NOT] = ACTIONS(154),
    [anon_sym_END_DASHSTRING] = ACTIONS(154),
    [anon_sym_UNSTRING] = ACTIONS(154),
    [anon_sym_COUNT] = ACTIONS(154),
    [anon_sym_DELIMITER] = ACTIONS(154),
    [anon_sym_TALLYING] = ACTIONS(154),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(154),
    [anon_sym_INSPECT] = ACTIONS(154),
    [anon_sym_CONVERTING] = ACTIONS(154),
    [anon_sym_FIRST] = ACTIONS(154),
    [anon_sym_INITIAL] = ACTIONS(154),
    [anon_sym_READ] = ACTIONS(154),
    [anon_sym_WRITE] = ACTIONS(154),
    [anon_sym_REWRITE] = ACTIONS(154),
    [anon_sym_DELETE] = ACTIONS(154),
    [anon_sym_START] = ACTIONS(154),
    [anon_sym_OPEN] = ACTIONS(154),
    [anon_sym_CLOSE] = ACTIONS(154),
    [anon_sym_INPUT] = ACTIONS(154),
    [anon_sym_OUTPUT] = ACTIONS(154),
    [anon_sym_I_DASHO] = ACTIONS(154),
    [anon_sym_EXTEND] = ACTIONS(154),
    [anon_sym_ACCEPT] = ACTIONS(154),
    [anon_sym_FROM] = ACTIONS(154),
    [anon_sym_DATE] = ACTIONS(154),
    [anon_sym_DAY] = ACTIONS(154),
    [anon_sym_TIME] = ACTIONS(154),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(154),
    [anon_sym_EQUAL] = ACTIONS(154),
    [anon_sym_GREATER] = ACTIONS(154),
    [anon_sym_LESS] = ACTIONS(154),
    [anon_sym_THAN] = ACTIONS(154),
    [anon_sym_OR] = ACTIONS(154),
    [anon_sym_AND] = ACTIONS(154),
    [anon_sym_DFHENTER] = ACTIONS(154),
    [anon_sym_DFHCLEAR] = ACTIONS(154),
    [anon_sym_DFHPA1] = ACTIONS(154),
    [anon_sym_DFHPA2] = ACTIONS(154),
    [anon_sym_DFHPF1] = ACTIONS(154),
    [anon_sym_DFHPF2] = ACTIONS(154),
    [anon_sym_DFHPF3] = ACTIONS(154),
    [anon_sym_DFHPF4] = ACTIONS(154),
    [anon_sym_DFHPF5] = ACTIONS(154),
    [anon_sym_DFHPF6] = ACTIONS(154),
    [anon_sym_DFHPF7] = ACTIONS(154),
    [anon_sym_DFHPF8] = ACTIONS(154),
    [anon_sym_DFHPF9] = ACTIONS(154),
    [anon_sym_DFHPF10] = ACTIONS(154),
    [anon_sym_DFHPF11] = ACTIONS(154),
    [anon_sym_DFHPF12] = ACTIONS(154),
    [anon_sym_EIBAID] = ACTIONS(154),
    [anon_sym_DFHRED] = ACTIONS(154),
    [anon_sym_DFHBMASB] = ACTIONS(154),
    [anon_sym_DFHBMASK] = ACTIONS(154),
    [aux_sym_identifier_token1] = ACTIONS(154),
    [aux_sym_identifier_token2] = ACTIONS(152),
    [sym_picture_string] = ACTIONS(154),
    [aux_sym_string_literal_token1] = ACTIONS(152),
    [aux_sym_string_literal_token2] = ACTIONS(152),
    [sym_number] = ACTIONS(154),
    [anon_sym_EQ_EQ] = ACTIONS(152),
    [anon_sym_EQ] = ACTIONS(154),
    [anon_sym_GT] = ACTIONS(154),
    [anon_sym_LT] = ACTIONS(154),
    [anon_sym_GT_EQ] = ACTIONS(152),
    [anon_sym_LT_EQ] = ACTIONS(152),
    [anon_sym_COMMA] = ACTIONS(154),
    [anon_sym_LPAREN] = ACTIONS(154),
    [anon_sym_RPAREN] = ACTIONS(152),
    [anon_sym_COLON] = ACTIONS(152),
  },
  [12] = {
    [ts_builtin_sym_end] = ACTIONS(156),
    [aux_sym_newline_token1] = ACTIONS(156),
    [aux_sym_comment_line_token1] = ACTIONS(156),
    [sym_sequence_number] = ACTIONS(158),
    [anon_sym_DOT] = ACTIONS(156),
    [anon_sym_88] = ACTIONS(158),
    [anon_sym_VALUE] = ACTIONS(158),
    [anon_sym_IS] = ACTIONS(158),
    [aux_sym_level_number_token1] = ACTIONS(158),
    [aux_sym_level_number_token2] = ACTIONS(158),
    [anon_sym_66] = ACTIONS(158),
    [anon_sym_77] = ACTIONS(158),
    [anon_sym_FILLER] = ACTIONS(158),
    [anon_sym_PIC] = ACTIONS(158),
    [anon_sym_PICTURE] = ACTIONS(158),
    [anon_sym_VALUES] = ACTIONS(158),
    [anon_sym_OCCURS] = ACTIONS(158),
    [anon_sym_TIMES] = ACTIONS(158),
    [anon_sym_TO] = ACTIONS(158),
    [anon_sym_REDEFINES] = ACTIONS(158),
    [anon_sym_INDEXED] = ACTIONS(158),
    [anon_sym_BY] = ACTIONS(158),
    [anon_sym_DEPENDING] = ACTIONS(158),
    [anon_sym_ON] = ACTIONS(158),
    [anon_sym_USAGE] = ACTIONS(158),
    [anon_sym_DISPLAY] = ACTIONS(158),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(158),
    [anon_sym_BINARY] = ACTIONS(158),
    [anon_sym_COMP] = ACTIONS(158),
    [anon_sym_COMP_DASH1] = ACTIONS(158),
    [anon_sym_COMP_DASH2] = ACTIONS(158),
    [anon_sym_COMP_DASH3] = ACTIONS(158),
    [anon_sym_COMP_DASH4] = ACTIONS(158),
    [anon_sym_COMP_DASH5] = ACTIONS(158),
    [anon_sym_COMPUTATIONAL] = ACTIONS(158),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(158),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(158),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(158),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(158),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(158),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(158),
    [anon_sym_INDEX] = ACTIONS(158),
    [anon_sym_POINTER] = ACTIONS(158),
    [anon_sym_ZERO] = ACTIONS(158),
    [anon_sym_ZEROS] = ACTIONS(158),
    [anon_sym_ZEROES] = ACTIONS(158),
    [anon_sym_SPACE] = ACTIONS(158),
    [anon_sym_SPACES] = ACTIONS(158),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(158),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(158),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(158),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(158),
    [anon_sym_QUOTE] = ACTIONS(158),
    [anon_sym_QUOTES] = ACTIONS(158),
    [anon_sym_NULL] = ACTIONS(158),
    [anon_sym_NULLS] = ACTIONS(158),
    [anon_sym_ALL] = ACTIONS(158),
    [anon_sym_THRU] = ACTIONS(158),
    [anon_sym_THROUGH] = ACTIONS(158),
    [anon_sym_ASCENDING] = ACTIONS(158),
    [anon_sym_DESCENDING] = ACTIONS(158),
    [anon_sym_KEY] = ACTIONS(158),
    [anon_sym_SIGN] = ACTIONS(158),
    [anon_sym_LEADING] = ACTIONS(158),
    [anon_sym_TRAILING] = ACTIONS(158),
    [anon_sym_SEPARATE] = ACTIONS(158),
    [anon_sym_CHARACTER] = ACTIONS(158),
    [anon_sym_SYNC] = ACTIONS(158),
    [anon_sym_SYNCHRONIZED] = ACTIONS(158),
    [anon_sym_LEFT] = ACTIONS(158),
    [anon_sym_RIGHT] = ACTIONS(158),
    [anon_sym_JUST] = ACTIONS(158),
    [anon_sym_JUSTIFIED] = ACTIONS(158),
    [anon_sym_BLANK] = ACTIONS(158),
    [anon_sym_WHEN] = ACTIONS(158),
    [anon_sym_EXTERNAL] = ACTIONS(158),
    [anon_sym_GLOBAL] = ACTIONS(158),
    [anon_sym_AS] = ACTIONS(158),
    [anon_sym_COPY] = ACTIONS(158),
    [anon_sym_REPLACING] = ACTIONS(158),
    [anon_sym_OF] = ACTIONS(158),
    [anon_sym_IN] = ACTIONS(158),
    [anon_sym_REPLACE] = ACTIONS(158),
    [anon_sym_OFF] = ACTIONS(158),
    [anon_sym_EJECT] = ACTIONS(158),
    [anon_sym_SKIP1] = ACTIONS(158),
    [anon_sym_SKIP2] = ACTIONS(158),
    [anon_sym_SKIP3] = ACTIONS(158),
    [anon_sym_EXEC] = ACTIONS(158),
    [anon_sym_EXECUTE] = ACTIONS(158),
    [anon_sym_SQL] = ACTIONS(158),
    [anon_sym_SQLIMS] = ACTIONS(158),
    [anon_sym_DLI] = ACTIONS(158),
    [anon_sym_END_DASHEXEC] = ACTIONS(158),
    [anon_sym_IF] = ACTIONS(158),
    [anon_sym_ELSE] = ACTIONS(158),
    [anon_sym_END_DASHIF] = ACTIONS(158),
    [anon_sym_THEN] = ACTIONS(158),
    [anon_sym_EVALUATE] = ACTIONS(158),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(158),
    [anon_sym_OTHER] = ACTIONS(158),
    [anon_sym_ALSO] = ACTIONS(158),
    [anon_sym_PERFORM] = ACTIONS(158),
    [anon_sym_END_DASHPERFORM] = ACTIONS(158),
    [anon_sym_UNTIL] = ACTIONS(158),
    [anon_sym_VARYING] = ACTIONS(158),
    [anon_sym_WITH] = ACTIONS(158),
    [anon_sym_TEST] = ACTIONS(158),
    [anon_sym_BEFORE] = ACTIONS(158),
    [anon_sym_AFTER] = ACTIONS(158),
    [anon_sym_GO] = ACTIONS(158),
    [anon_sym_SECTION] = ACTIONS(158),
    [anon_sym_PARAGRAPH] = ACTIONS(158),
    [anon_sym_CONTINUE] = ACTIONS(158),
    [anon_sym_NEXT] = ACTIONS(158),
    [anon_sym_SENTENCE] = ACTIONS(158),
    [anon_sym_EXIT] = ACTIONS(158),
    [anon_sym_STOP] = ACTIONS(158),
    [anon_sym_RUN] = ACTIONS(158),
    [anon_sym_MOVE] = ACTIONS(158),
    [anon_sym_CORRESPONDING] = ACTIONS(158),
    [anon_sym_CORR] = ACTIONS(158),
    [anon_sym_INTO] = ACTIONS(158),
    [anon_sym_SET] = ACTIONS(158),
    [anon_sym_TRUE] = ACTIONS(158),
    [anon_sym_FALSE] = ACTIONS(158),
    [anon_sym_INITIALIZE] = ACTIONS(158),
    [anon_sym_ALPHABETIC] = ACTIONS(158),
    [anon_sym_ALPHANUMERIC] = ACTIONS(158),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(158),
    [anon_sym_NUMERIC] = ACTIONS(158),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(158),
    [anon_sym_COMPUTE] = ACTIONS(158),
    [anon_sym_ADD] = ACTIONS(158),
    [anon_sym_SUBTRACT] = ACTIONS(158),
    [anon_sym_MULTIPLY] = ACTIONS(158),
    [anon_sym_DIVIDE] = ACTIONS(158),
    [anon_sym_GIVING] = ACTIONS(158),
    [anon_sym_REMAINDER] = ACTIONS(158),
    [anon_sym_STRING] = ACTIONS(158),
    [anon_sym_DELIMITED] = ACTIONS(158),
    [anon_sym_SIZE] = ACTIONS(158),
    [anon_sym_OVERFLOW] = ACTIONS(158),
    [anon_sym_NOT] = ACTIONS(158),
    [anon_sym_END_DASHSTRING] = ACTIONS(158),
    [anon_sym_UNSTRING] = ACTIONS(158),
    [anon_sym_COUNT] = ACTIONS(158),
    [anon_sym_DELIMITER] = ACTIONS(158),
    [anon_sym_TALLYING] = ACTIONS(158),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(158),
    [anon_sym_INSPECT] = ACTIONS(158),
    [anon_sym_CONVERTING] = ACTIONS(158),
    [anon_sym_FIRST] = ACTIONS(158),
    [anon_sym_INITIAL] = ACTIONS(158),
    [anon_sym_READ] = ACTIONS(158),
    [anon_sym_WRITE] = ACTIONS(158),
    [anon_sym_REWRITE] = ACTIONS(158),
    [anon_sym_DELETE] = ACTIONS(158),
    [anon_sym_START] = ACTIONS(158),
    [anon_sym_OPEN] = ACTIONS(158),
    [anon_sym_CLOSE] = ACTIONS(158),
    [anon_sym_INPUT] = ACTIONS(158),
    [anon_sym_OUTPUT] = ACTIONS(158),
    [anon_sym_I_DASHO] = ACTIONS(158),
    [anon_sym_EXTEND] = ACTIONS(158),
    [anon_sym_ACCEPT] = ACTIONS(158),
    [anon_sym_FROM] = ACTIONS(158),
    [anon_sym_DATE] = ACTIONS(158),
    [anon_sym_DAY] = ACTIONS(158),
    [anon_sym_TIME] = ACTIONS(158),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(158),
    [anon_sym_EQUAL] = ACTIONS(158),
    [anon_sym_GREATER] = ACTIONS(158),
    [anon_sym_LESS] = ACTIONS(158),
    [anon_sym_THAN] = ACTIONS(158),
    [anon_sym_OR] = ACTIONS(158),
    [anon_sym_AND] = ACTIONS(158),
    [anon_sym_DFHENTER] = ACTIONS(158),
    [anon_sym_DFHCLEAR] = ACTIONS(158),
    [anon_sym_DFHPA1] = ACTIONS(158),
    [anon_sym_DFHPA2] = ACTIONS(158),
    [anon_sym_DFHPF1] = ACTIONS(158),
    [anon_sym_DFHPF2] = ACTIONS(158),
    [anon_sym_DFHPF3] = ACTIONS(158),
    [anon_sym_DFHPF4] = ACTIONS(158),
    [anon_sym_DFHPF5] = ACTIONS(158),
    [anon_sym_DFHPF6] = ACTIONS(158),
    [anon_sym_DFHPF7] = ACTIONS(158),
    [anon_sym_DFHPF8] = ACTIONS(158),
    [anon_sym_DFHPF9] = ACTIONS(158),
    [anon_sym_DFHPF10] = ACTIONS(158),
    [anon_sym_DFHPF11] = ACTIONS(158),
    [anon_sym_DFHPF12] = ACTIONS(158),
    [anon_sym_EIBAID] = ACTIONS(158),
    [anon_sym_DFHRED] = ACTIONS(158),
    [anon_sym_DFHBMASB] = ACTIONS(158),
    [anon_sym_DFHBMASK] = ACTIONS(158),
    [aux_sym_identifier_token1] = ACTIONS(158),
    [aux_sym_identifier_token2] = ACTIONS(156),
    [sym_picture_string] = ACTIONS(158),
    [aux_sym_string_literal_token1] = ACTIONS(156),
    [aux_sym_string_literal_token2] = ACTIONS(156),
    [sym_number] = ACTIONS(158),
    [anon_sym_EQ_EQ] = ACTIONS(156),
    [anon_sym_EQ] = ACTIONS(158),
    [anon_sym_GT] = ACTIONS(158),
    [anon_sym_LT] = ACTIONS(158),
    [anon_sym_GT_EQ] = ACTIONS(156),
    [anon_sym_LT_EQ] = ACTIONS(156),
    [anon_sym_COMMA] = ACTIONS(158),
    [anon_sym_LPAREN] = ACTIONS(158),
    [anon_sym_RPAREN] = ACTIONS(156),
    [anon_sym_COLON] = ACTIONS(156),
  },
  [13] = {
    [ts_builtin_sym_end] = ACTIONS(160),
    [aux_sym_newline_token1] = ACTIONS(160),
    [aux_sym_comment_line_token1] = ACTIONS(160),
    [sym_sequence_number] = ACTIONS(162),
    [anon_sym_DOT] = ACTIONS(160),
    [anon_sym_88] = ACTIONS(162),
    [anon_sym_VALUE] = ACTIONS(162),
    [anon_sym_IS] = ACTIONS(162),
    [aux_sym_level_number_token1] = ACTIONS(162),
    [aux_sym_level_number_token2] = ACTIONS(162),
    [anon_sym_66] = ACTIONS(162),
    [anon_sym_77] = ACTIONS(162),
    [anon_sym_FILLER] = ACTIONS(162),
    [anon_sym_PIC] = ACTIONS(162),
    [anon_sym_PICTURE] = ACTIONS(162),
    [anon_sym_VALUES] = ACTIONS(162),
    [anon_sym_OCCURS] = ACTIONS(162),
    [anon_sym_TIMES] = ACTIONS(162),
    [anon_sym_TO] = ACTIONS(162),
    [anon_sym_REDEFINES] = ACTIONS(162),
    [anon_sym_INDEXED] = ACTIONS(162),
    [anon_sym_BY] = ACTIONS(162),
    [anon_sym_DEPENDING] = ACTIONS(162),
    [anon_sym_ON] = ACTIONS(162),
    [anon_sym_USAGE] = ACTIONS(162),
    [anon_sym_DISPLAY] = ACTIONS(162),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(162),
    [anon_sym_BINARY] = ACTIONS(162),
    [anon_sym_COMP] = ACTIONS(162),
    [anon_sym_COMP_DASH1] = ACTIONS(162),
    [anon_sym_COMP_DASH2] = ACTIONS(162),
    [anon_sym_COMP_DASH3] = ACTIONS(162),
    [anon_sym_COMP_DASH4] = ACTIONS(162),
    [anon_sym_COMP_DASH5] = ACTIONS(162),
    [anon_sym_COMPUTATIONAL] = ACTIONS(162),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(162),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(162),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(162),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(162),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(162),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(162),
    [anon_sym_INDEX] = ACTIONS(162),
    [anon_sym_POINTER] = ACTIONS(162),
    [anon_sym_ZERO] = ACTIONS(162),
    [anon_sym_ZEROS] = ACTIONS(162),
    [anon_sym_ZEROES] = ACTIONS(162),
    [anon_sym_SPACE] = ACTIONS(162),
    [anon_sym_SPACES] = ACTIONS(162),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(162),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(162),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(162),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(162),
    [anon_sym_QUOTE] = ACTIONS(162),
    [anon_sym_QUOTES] = ACTIONS(162),
    [anon_sym_NULL] = ACTIONS(162),
    [anon_sym_NULLS] = ACTIONS(162),
    [anon_sym_ALL] = ACTIONS(162),
    [anon_sym_THRU] = ACTIONS(162),
    [anon_sym_THROUGH] = ACTIONS(162),
    [anon_sym_ASCENDING] = ACTIONS(162),
    [anon_sym_DESCENDING] = ACTIONS(162),
    [anon_sym_KEY] = ACTIONS(162),
    [anon_sym_SIGN] = ACTIONS(162),
    [anon_sym_LEADING] = ACTIONS(162),
    [anon_sym_TRAILING] = ACTIONS(162),
    [anon_sym_SEPARATE] = ACTIONS(162),
    [anon_sym_CHARACTER] = ACTIONS(162),
    [anon_sym_SYNC] = ACTIONS(162),
    [anon_sym_SYNCHRONIZED] = ACTIONS(162),
    [anon_sym_LEFT] = ACTIONS(162),
    [anon_sym_RIGHT] = ACTIONS(162),
    [anon_sym_JUST] = ACTIONS(162),
    [anon_sym_JUSTIFIED] = ACTIONS(162),
    [anon_sym_BLANK] = ACTIONS(162),
    [anon_sym_WHEN] = ACTIONS(162),
    [anon_sym_EXTERNAL] = ACTIONS(162),
    [anon_sym_GLOBAL] = ACTIONS(162),
    [anon_sym_AS] = ACTIONS(162),
    [anon_sym_COPY] = ACTIONS(162),
    [anon_sym_REPLACING] = ACTIONS(162),
    [anon_sym_OF] = ACTIONS(162),
    [anon_sym_IN] = ACTIONS(162),
    [anon_sym_REPLACE] = ACTIONS(162),
    [anon_sym_OFF] = ACTIONS(162),
    [anon_sym_EJECT] = ACTIONS(162),
    [anon_sym_SKIP1] = ACTIONS(162),
    [anon_sym_SKIP2] = ACTIONS(162),
    [anon_sym_SKIP3] = ACTIONS(162),
    [anon_sym_EXEC] = ACTIONS(162),
    [anon_sym_EXECUTE] = ACTIONS(162),
    [anon_sym_SQL] = ACTIONS(162),
    [anon_sym_SQLIMS] = ACTIONS(162),
    [anon_sym_DLI] = ACTIONS(162),
    [anon_sym_END_DASHEXEC] = ACTIONS(162),
    [anon_sym_IF] = ACTIONS(162),
    [anon_sym_ELSE] = ACTIONS(162),
    [anon_sym_END_DASHIF] = ACTIONS(162),
    [anon_sym_THEN] = ACTIONS(162),
    [anon_sym_EVALUATE] = ACTIONS(162),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(162),
    [anon_sym_OTHER] = ACTIONS(162),
    [anon_sym_ALSO] = ACTIONS(162),
    [anon_sym_PERFORM] = ACTIONS(162),
    [anon_sym_END_DASHPERFORM] = ACTIONS(162),
    [anon_sym_UNTIL] = ACTIONS(162),
    [anon_sym_VARYING] = ACTIONS(162),
    [anon_sym_WITH] = ACTIONS(162),
    [anon_sym_TEST] = ACTIONS(162),
    [anon_sym_BEFORE] = ACTIONS(162),
    [anon_sym_AFTER] = ACTIONS(162),
    [anon_sym_GO] = ACTIONS(162),
    [anon_sym_SECTION] = ACTIONS(162),
    [anon_sym_PARAGRAPH] = ACTIONS(162),
    [anon_sym_CONTINUE] = ACTIONS(162),
    [anon_sym_NEXT] = ACTIONS(162),
    [anon_sym_SENTENCE] = ACTIONS(162),
    [anon_sym_EXIT] = ACTIONS(162),
    [anon_sym_STOP] = ACTIONS(162),
    [anon_sym_RUN] = ACTIONS(162),
    [anon_sym_MOVE] = ACTIONS(162),
    [anon_sym_CORRESPONDING] = ACTIONS(162),
    [anon_sym_CORR] = ACTIONS(162),
    [anon_sym_INTO] = ACTIONS(162),
    [anon_sym_SET] = ACTIONS(162),
    [anon_sym_TRUE] = ACTIONS(162),
    [anon_sym_FALSE] = ACTIONS(162),
    [anon_sym_INITIALIZE] = ACTIONS(162),
    [anon_sym_ALPHABETIC] = ACTIONS(162),
    [anon_sym_ALPHANUMERIC] = ACTIONS(162),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(162),
    [anon_sym_NUMERIC] = ACTIONS(162),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(162),
    [anon_sym_COMPUTE] = ACTIONS(162),
    [anon_sym_ADD] = ACTIONS(162),
    [anon_sym_SUBTRACT] = ACTIONS(162),
    [anon_sym_MULTIPLY] = ACTIONS(162),
    [anon_sym_DIVIDE] = ACTIONS(162),
    [anon_sym_GIVING] = ACTIONS(162),
    [anon_sym_REMAINDER] = ACTIONS(162),
    [anon_sym_STRING] = ACTIONS(162),
    [anon_sym_DELIMITED] = ACTIONS(162),
    [anon_sym_SIZE] = ACTIONS(162),
    [anon_sym_OVERFLOW] = ACTIONS(162),
    [anon_sym_NOT] = ACTIONS(162),
    [anon_sym_END_DASHSTRING] = ACTIONS(162),
    [anon_sym_UNSTRING] = ACTIONS(162),
    [anon_sym_COUNT] = ACTIONS(162),
    [anon_sym_DELIMITER] = ACTIONS(162),
    [anon_sym_TALLYING] = ACTIONS(162),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(162),
    [anon_sym_INSPECT] = ACTIONS(162),
    [anon_sym_CONVERTING] = ACTIONS(162),
    [anon_sym_FIRST] = ACTIONS(162),
    [anon_sym_INITIAL] = ACTIONS(162),
    [anon_sym_READ] = ACTIONS(162),
    [anon_sym_WRITE] = ACTIONS(162),
    [anon_sym_REWRITE] = ACTIONS(162),
    [anon_sym_DELETE] = ACTIONS(162),
    [anon_sym_START] = ACTIONS(162),
    [anon_sym_OPEN] = ACTIONS(162),
    [anon_sym_CLOSE] = ACTIONS(162),
    [anon_sym_INPUT] = ACTIONS(162),
    [anon_sym_OUTPUT] = ACTIONS(162),
    [anon_sym_I_DASHO] = ACTIONS(162),
    [anon_sym_EXTEND] = ACTIONS(162),
    [anon_sym_ACCEPT] = ACTIONS(162),
    [anon_sym_FROM] = ACTIONS(162),
    [anon_sym_DATE] = ACTIONS(162),
    [anon_sym_DAY] = ACTIONS(162),
    [anon_sym_TIME] = ACTIONS(162),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(162),
    [anon_sym_EQUAL] = ACTIONS(162),
    [anon_sym_GREATER] = ACTIONS(162),
    [anon_sym_LESS] = ACTIONS(162),
    [anon_sym_THAN] = ACTIONS(162),
    [anon_sym_OR] = ACTIONS(162),
    [anon_sym_AND] = ACTIONS(162),
    [anon_sym_DFHENTER] = ACTIONS(162),
    [anon_sym_DFHCLEAR] = ACTIONS(162),
    [anon_sym_DFHPA1] = ACTIONS(162),
    [anon_sym_DFHPA2] = ACTIONS(162),
    [anon_sym_DFHPF1] = ACTIONS(162),
    [anon_sym_DFHPF2] = ACTIONS(162),
    [anon_sym_DFHPF3] = ACTIONS(162),
    [anon_sym_DFHPF4] = ACTIONS(162),
    [anon_sym_DFHPF5] = ACTIONS(162),
    [anon_sym_DFHPF6] = ACTIONS(162),
    [anon_sym_DFHPF7] = ACTIONS(162),
    [anon_sym_DFHPF8] = ACTIONS(162),
    [anon_sym_DFHPF9] = ACTIONS(162),
    [anon_sym_DFHPF10] = ACTIONS(162),
    [anon_sym_DFHPF11] = ACTIONS(162),
    [anon_sym_DFHPF12] = ACTIONS(162),
    [anon_sym_EIBAID] = ACTIONS(162),
    [anon_sym_DFHRED] = ACTIONS(162),
    [anon_sym_DFHBMASB] = ACTIONS(162),
    [anon_sym_DFHBMASK] = ACTIONS(162),
    [aux_sym_identifier_token1] = ACTIONS(162),
    [aux_sym_identifier_token2] = ACTIONS(160),
    [sym_picture_string] = ACTIONS(162),
    [aux_sym_string_literal_token1] = ACTIONS(160),
    [aux_sym_string_literal_token2] = ACTIONS(160),
    [sym_number] = ACTIONS(162),
    [anon_sym_EQ_EQ] = ACTIONS(160),
    [anon_sym_EQ] = ACTIONS(162),
    [anon_sym_GT] = ACTIONS(162),
    [anon_sym_LT] = ACTIONS(162),
    [anon_sym_GT_EQ] = ACTIONS(160),
    [anon_sym_LT_EQ] = ACTIONS(160),
    [anon_sym_COMMA] = ACTIONS(162),
    [anon_sym_LPAREN] = ACTIONS(162),
    [anon_sym_RPAREN] = ACTIONS(160),
    [anon_sym_COLON] = ACTIONS(160),
  },
  [14] = {
    [aux_sym_newline_token1] = ACTIONS(164),
    [aux_sym_comment_line_token1] = ACTIONS(126),
    [anon_sym_DOT] = ACTIONS(164),
    [anon_sym_88] = ACTIONS(166),
    [anon_sym_VALUE] = ACTIONS(166),
    [anon_sym_IS] = ACTIONS(166),
    [aux_sym_level_number_token1] = ACTIONS(166),
    [aux_sym_level_number_token2] = ACTIONS(166),
    [anon_sym_66] = ACTIONS(166),
    [anon_sym_77] = ACTIONS(166),
    [anon_sym_FILLER] = ACTIONS(166),
    [anon_sym_PIC] = ACTIONS(166),
    [anon_sym_PICTURE] = ACTIONS(166),
    [anon_sym_VALUES] = ACTIONS(166),
    [anon_sym_OCCURS] = ACTIONS(166),
    [anon_sym_TIMES] = ACTIONS(166),
    [anon_sym_TO] = ACTIONS(166),
    [anon_sym_REDEFINES] = ACTIONS(166),
    [anon_sym_INDEXED] = ACTIONS(166),
    [anon_sym_BY] = ACTIONS(166),
    [anon_sym_DEPENDING] = ACTIONS(166),
    [anon_sym_ON] = ACTIONS(166),
    [anon_sym_USAGE] = ACTIONS(166),
    [anon_sym_DISPLAY] = ACTIONS(166),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(166),
    [anon_sym_BINARY] = ACTIONS(166),
    [anon_sym_COMP] = ACTIONS(166),
    [anon_sym_COMP_DASH1] = ACTIONS(166),
    [anon_sym_COMP_DASH2] = ACTIONS(166),
    [anon_sym_COMP_DASH3] = ACTIONS(166),
    [anon_sym_COMP_DASH4] = ACTIONS(166),
    [anon_sym_COMP_DASH5] = ACTIONS(166),
    [anon_sym_COMPUTATIONAL] = ACTIONS(166),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(166),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(166),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(166),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(166),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(166),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(166),
    [anon_sym_INDEX] = ACTIONS(166),
    [anon_sym_POINTER] = ACTIONS(166),
    [anon_sym_ZERO] = ACTIONS(166),
    [anon_sym_ZEROS] = ACTIONS(166),
    [anon_sym_ZEROES] = ACTIONS(166),
    [anon_sym_SPACE] = ACTIONS(166),
    [anon_sym_SPACES] = ACTIONS(166),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(166),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(166),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(166),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(166),
    [anon_sym_QUOTE] = ACTIONS(166),
    [anon_sym_QUOTES] = ACTIONS(166),
    [anon_sym_NULL] = ACTIONS(166),
    [anon_sym_NULLS] = ACTIONS(166),
    [anon_sym_ALL] = ACTIONS(166),
    [anon_sym_THRU] = ACTIONS(166),
    [anon_sym_THROUGH] = ACTIONS(166),
    [anon_sym_ASCENDING] = ACTIONS(166),
    [anon_sym_DESCENDING] = ACTIONS(166),
    [anon_sym_KEY] = ACTIONS(166),
    [anon_sym_SIGN] = ACTIONS(166),
    [anon_sym_LEADING] = ACTIONS(166),
    [anon_sym_TRAILING] = ACTIONS(166),
    [anon_sym_SEPARATE] = ACTIONS(166),
    [anon_sym_CHARACTER] = ACTIONS(166),
    [anon_sym_SYNC] = ACTIONS(166),
    [anon_sym_SYNCHRONIZED] = ACTIONS(166),
    [anon_sym_LEFT] = ACTIONS(166),
    [anon_sym_RIGHT] = ACTIONS(166),
    [anon_sym_JUST] = ACTIONS(166),
    [anon_sym_JUSTIFIED] = ACTIONS(166),
    [anon_sym_BLANK] = ACTIONS(166),
    [anon_sym_WHEN] = ACTIONS(166),
    [anon_sym_EXTERNAL] = ACTIONS(166),
    [anon_sym_GLOBAL] = ACTIONS(166),
    [anon_sym_AS] = ACTIONS(166),
    [anon_sym_COPY] = ACTIONS(166),
    [anon_sym_REPLACING] = ACTIONS(166),
    [anon_sym_OF] = ACTIONS(166),
    [anon_sym_IN] = ACTIONS(166),
    [anon_sym_REPLACE] = ACTIONS(166),
    [anon_sym_OFF] = ACTIONS(166),
    [anon_sym_EJECT] = ACTIONS(166),
    [anon_sym_SKIP1] = ACTIONS(166),
    [anon_sym_SKIP2] = ACTIONS(166),
    [anon_sym_SKIP3] = ACTIONS(166),
    [anon_sym_EXEC] = ACTIONS(166),
    [anon_sym_EXECUTE] = ACTIONS(166),
    [anon_sym_SQL] = ACTIONS(166),
    [anon_sym_SQLIMS] = ACTIONS(166),
    [anon_sym_DLI] = ACTIONS(166),
    [anon_sym_END_DASHEXEC] = ACTIONS(166),
    [anon_sym_IF] = ACTIONS(166),
    [anon_sym_ELSE] = ACTIONS(166),
    [anon_sym_END_DASHIF] = ACTIONS(166),
    [anon_sym_THEN] = ACTIONS(166),
    [anon_sym_EVALUATE] = ACTIONS(166),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(166),
    [anon_sym_OTHER] = ACTIONS(166),
    [anon_sym_ALSO] = ACTIONS(166),
    [anon_sym_PERFORM] = ACTIONS(166),
    [anon_sym_END_DASHPERFORM] = ACTIONS(166),
    [anon_sym_UNTIL] = ACTIONS(166),
    [anon_sym_VARYING] = ACTIONS(166),
    [anon_sym_WITH] = ACTIONS(166),
    [anon_sym_TEST] = ACTIONS(166),
    [anon_sym_BEFORE] = ACTIONS(166),
    [anon_sym_AFTER] = ACTIONS(166),
    [anon_sym_GO] = ACTIONS(166),
    [anon_sym_SECTION] = ACTIONS(166),
    [anon_sym_PARAGRAPH] = ACTIONS(166),
    [anon_sym_CONTINUE] = ACTIONS(166),
    [anon_sym_NEXT] = ACTIONS(166),
    [anon_sym_SENTENCE] = ACTIONS(166),
    [anon_sym_EXIT] = ACTIONS(166),
    [anon_sym_STOP] = ACTIONS(166),
    [anon_sym_RUN] = ACTIONS(166),
    [anon_sym_MOVE] = ACTIONS(166),
    [anon_sym_CORRESPONDING] = ACTIONS(166),
    [anon_sym_CORR] = ACTIONS(166),
    [anon_sym_INTO] = ACTIONS(166),
    [anon_sym_SET] = ACTIONS(166),
    [anon_sym_TRUE] = ACTIONS(166),
    [anon_sym_FALSE] = ACTIONS(166),
    [anon_sym_INITIALIZE] = ACTIONS(166),
    [anon_sym_ALPHABETIC] = ACTIONS(166),
    [anon_sym_ALPHANUMERIC] = ACTIONS(166),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(166),
    [anon_sym_NUMERIC] = ACTIONS(166),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(166),
    [anon_sym_COMPUTE] = ACTIONS(166),
    [anon_sym_ADD] = ACTIONS(166),
    [anon_sym_SUBTRACT] = ACTIONS(166),
    [anon_sym_MULTIPLY] = ACTIONS(166),
    [anon_sym_DIVIDE] = ACTIONS(166),
    [anon_sym_GIVING] = ACTIONS(166),
    [anon_sym_REMAINDER] = ACTIONS(166),
    [anon_sym_STRING] = ACTIONS(166),
    [anon_sym_DELIMITED] = ACTIONS(166),
    [anon_sym_SIZE] = ACTIONS(166),
    [anon_sym_OVERFLOW] = ACTIONS(166),
    [anon_sym_NOT] = ACTIONS(166),
    [anon_sym_END_DASHSTRING] = ACTIONS(166),
    [anon_sym_UNSTRING] = ACTIONS(166),
    [anon_sym_COUNT] = ACTIONS(166),
    [anon_sym_DELIMITER] = ACTIONS(166),
    [anon_sym_TALLYING] = ACTIONS(166),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(166),
    [anon_sym_INSPECT] = ACTIONS(166),
    [anon_sym_CONVERTING] = ACTIONS(166),
    [anon_sym_FIRST] = ACTIONS(166),
    [anon_sym_INITIAL] = ACTIONS(166),
    [anon_sym_READ] = ACTIONS(166),
    [anon_sym_WRITE] = ACTIONS(166),
    [anon_sym_REWRITE] = ACTIONS(166),
    [anon_sym_DELETE] = ACTIONS(166),
    [anon_sym_START] = ACTIONS(166),
    [anon_sym_OPEN] = ACTIONS(166),
    [anon_sym_CLOSE] = ACTIONS(166),
    [anon_sym_INPUT] = ACTIONS(166),
    [anon_sym_OUTPUT] = ACTIONS(166),
    [anon_sym_I_DASHO] = ACTIONS(166),
    [anon_sym_EXTEND] = ACTIONS(166),
    [anon_sym_ACCEPT] = ACTIONS(166),
    [anon_sym_FROM] = ACTIONS(166),
    [anon_sym_DATE] = ACTIONS(166),
    [anon_sym_DAY] = ACTIONS(166),
    [anon_sym_TIME] = ACTIONS(166),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(166),
    [anon_sym_EQUAL] = ACTIONS(166),
    [anon_sym_GREATER] = ACTIONS(166),
    [anon_sym_LESS] = ACTIONS(166),
    [anon_sym_THAN] = ACTIONS(166),
    [anon_sym_OR] = ACTIONS(166),
    [anon_sym_AND] = ACTIONS(166),
    [anon_sym_DFHENTER] = ACTIONS(166),
    [anon_sym_DFHCLEAR] = ACTIONS(166),
    [anon_sym_DFHPA1] = ACTIONS(166),
    [anon_sym_DFHPA2] = ACTIONS(166),
    [anon_sym_DFHPF1] = ACTIONS(166),
    [anon_sym_DFHPF2] = ACTIONS(166),
    [anon_sym_DFHPF3] = ACTIONS(166),
    [anon_sym_DFHPF4] = ACTIONS(166),
    [anon_sym_DFHPF5] = ACTIONS(166),
    [anon_sym_DFHPF6] = ACTIONS(166),
    [anon_sym_DFHPF7] = ACTIONS(166),
    [anon_sym_DFHPF8] = ACTIONS(166),
    [anon_sym_DFHPF9] = ACTIONS(166),
    [anon_sym_DFHPF10] = ACTIONS(166),
    [anon_sym_DFHPF11] = ACTIONS(166),
    [anon_sym_DFHPF12] = ACTIONS(166),
    [anon_sym_EIBAID] = ACTIONS(166),
    [anon_sym_DFHRED] = ACTIONS(166),
    [anon_sym_DFHBMASB] = ACTIONS(166),
    [anon_sym_DFHBMASK] = ACTIONS(166),
    [aux_sym_identifier_token1] = ACTIONS(166),
    [aux_sym_identifier_token2] = ACTIONS(164),
    [sym_picture_string] = ACTIONS(166),
    [aux_sym_string_literal_token1] = ACTIONS(164),
    [aux_sym_string_literal_token2] = ACTIONS(164),
    [sym_number] = ACTIONS(166),
    [anon_sym_EQ_EQ] = ACTIONS(164),
    [anon_sym_EQ] = ACTIONS(166),
    [anon_sym_GT] = ACTIONS(166),
    [anon_sym_LT] = ACTIONS(166),
    [anon_sym_GT_EQ] = ACTIONS(164),
    [anon_sym_LT_EQ] = ACTIONS(164),
    [anon_sym_COMMA] = ACTIONS(166),
    [anon_sym_LPAREN] = ACTIONS(166),
    [anon_sym_RPAREN] = ACTIONS(164),
    [anon_sym_COLON] = ACTIONS(164),
  },
  [15] = {
    [aux_sym_newline_token1] = ACTIONS(168),
    [anon_sym_DOT] = ACTIONS(168),
    [anon_sym_88] = ACTIONS(170),
    [anon_sym_VALUE] = ACTIONS(170),
    [anon_sym_IS] = ACTIONS(170),
    [anon_sym_ARE] = ACTIONS(172),
    [aux_sym_level_number_token1] = ACTIONS(170),
    [aux_sym_level_number_token2] = ACTIONS(170),
    [anon_sym_66] = ACTIONS(170),
    [anon_sym_77] = ACTIONS(170),
    [anon_sym_FILLER] = ACTIONS(170),
    [anon_sym_PIC] = ACTIONS(170),
    [anon_sym_PICTURE] = ACTIONS(170),
    [anon_sym_VALUES] = ACTIONS(170),
    [anon_sym_OCCURS] = ACTIONS(170),
    [anon_sym_TIMES] = ACTIONS(170),
    [anon_sym_TO] = ACTIONS(170),
    [anon_sym_REDEFINES] = ACTIONS(170),
    [anon_sym_INDEXED] = ACTIONS(170),
    [anon_sym_BY] = ACTIONS(170),
    [anon_sym_DEPENDING] = ACTIONS(170),
    [anon_sym_ON] = ACTIONS(170),
    [anon_sym_USAGE] = ACTIONS(170),
    [anon_sym_DISPLAY] = ACTIONS(170),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(170),
    [anon_sym_BINARY] = ACTIONS(170),
    [anon_sym_COMP] = ACTIONS(170),
    [anon_sym_COMP_DASH1] = ACTIONS(170),
    [anon_sym_COMP_DASH2] = ACTIONS(170),
    [anon_sym_COMP_DASH3] = ACTIONS(170),
    [anon_sym_COMP_DASH4] = ACTIONS(170),
    [anon_sym_COMP_DASH5] = ACTIONS(170),
    [anon_sym_COMPUTATIONAL] = ACTIONS(170),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(170),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(170),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(170),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(170),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(170),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(170),
    [anon_sym_INDEX] = ACTIONS(170),
    [anon_sym_POINTER] = ACTIONS(170),
    [anon_sym_ZERO] = ACTIONS(170),
    [anon_sym_ZEROS] = ACTIONS(170),
    [anon_sym_ZEROES] = ACTIONS(170),
    [anon_sym_SPACE] = ACTIONS(170),
    [anon_sym_SPACES] = ACTIONS(170),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(170),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(170),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(170),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(170),
    [anon_sym_QUOTE] = ACTIONS(170),
    [anon_sym_QUOTES] = ACTIONS(170),
    [anon_sym_NULL] = ACTIONS(170),
    [anon_sym_NULLS] = ACTIONS(170),
    [anon_sym_ALL] = ACTIONS(170),
    [anon_sym_THRU] = ACTIONS(170),
    [anon_sym_THROUGH] = ACTIONS(170),
    [anon_sym_ASCENDING] = ACTIONS(170),
    [anon_sym_DESCENDING] = ACTIONS(170),
    [anon_sym_KEY] = ACTIONS(170),
    [anon_sym_SIGN] = ACTIONS(170),
    [anon_sym_LEADING] = ACTIONS(170),
    [anon_sym_TRAILING] = ACTIONS(170),
    [anon_sym_SEPARATE] = ACTIONS(170),
    [anon_sym_CHARACTER] = ACTIONS(170),
    [anon_sym_SYNC] = ACTIONS(170),
    [anon_sym_SYNCHRONIZED] = ACTIONS(170),
    [anon_sym_LEFT] = ACTIONS(170),
    [anon_sym_RIGHT] = ACTIONS(170),
    [anon_sym_JUST] = ACTIONS(170),
    [anon_sym_JUSTIFIED] = ACTIONS(170),
    [anon_sym_BLANK] = ACTIONS(170),
    [anon_sym_WHEN] = ACTIONS(170),
    [anon_sym_EXTERNAL] = ACTIONS(170),
    [anon_sym_GLOBAL] = ACTIONS(170),
    [anon_sym_AS] = ACTIONS(170),
    [anon_sym_COPY] = ACTIONS(170),
    [anon_sym_REPLACING] = ACTIONS(170),
    [anon_sym_OF] = ACTIONS(170),
    [anon_sym_IN] = ACTIONS(170),
    [anon_sym_REPLACE] = ACTIONS(170),
    [anon_sym_OFF] = ACTIONS(170),
    [anon_sym_EJECT] = ACTIONS(170),
    [anon_sym_SKIP1] = ACTIONS(170),
    [anon_sym_SKIP2] = ACTIONS(170),
    [anon_sym_SKIP3] = ACTIONS(170),
    [anon_sym_EXEC] = ACTIONS(170),
    [anon_sym_EXECUTE] = ACTIONS(170),
    [anon_sym_SQL] = ACTIONS(170),
    [anon_sym_SQLIMS] = ACTIONS(170),
    [anon_sym_DLI] = ACTIONS(170),
    [anon_sym_END_DASHEXEC] = ACTIONS(170),
    [anon_sym_IF] = ACTIONS(170),
    [anon_sym_ELSE] = ACTIONS(170),
    [anon_sym_END_DASHIF] = ACTIONS(170),
    [anon_sym_THEN] = ACTIONS(170),
    [anon_sym_EVALUATE] = ACTIONS(170),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(170),
    [anon_sym_OTHER] = ACTIONS(170),
    [anon_sym_ALSO] = ACTIONS(170),
    [anon_sym_PERFORM] = ACTIONS(170),
    [anon_sym_END_DASHPERFORM] = ACTIONS(170),
    [anon_sym_UNTIL] = ACTIONS(170),
    [anon_sym_VARYING] = ACTIONS(170),
    [anon_sym_WITH] = ACTIONS(170),
    [anon_sym_TEST] = ACTIONS(170),
    [anon_sym_BEFORE] = ACTIONS(170),
    [anon_sym_AFTER] = ACTIONS(170),
    [anon_sym_GO] = ACTIONS(170),
    [anon_sym_SECTION] = ACTIONS(170),
    [anon_sym_PARAGRAPH] = ACTIONS(170),
    [anon_sym_CONTINUE] = ACTIONS(170),
    [anon_sym_NEXT] = ACTIONS(170),
    [anon_sym_SENTENCE] = ACTIONS(170),
    [anon_sym_EXIT] = ACTIONS(170),
    [anon_sym_STOP] = ACTIONS(170),
    [anon_sym_RUN] = ACTIONS(170),
    [anon_sym_MOVE] = ACTIONS(170),
    [anon_sym_CORRESPONDING] = ACTIONS(170),
    [anon_sym_CORR] = ACTIONS(170),
    [anon_sym_INTO] = ACTIONS(170),
    [anon_sym_SET] = ACTIONS(170),
    [anon_sym_TRUE] = ACTIONS(170),
    [anon_sym_FALSE] = ACTIONS(170),
    [anon_sym_INITIALIZE] = ACTIONS(170),
    [anon_sym_ALPHABETIC] = ACTIONS(170),
    [anon_sym_ALPHANUMERIC] = ACTIONS(170),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(170),
    [anon_sym_NUMERIC] = ACTIONS(170),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(170),
    [anon_sym_COMPUTE] = ACTIONS(170),
    [anon_sym_ADD] = ACTIONS(170),
    [anon_sym_SUBTRACT] = ACTIONS(170),
    [anon_sym_MULTIPLY] = ACTIONS(170),
    [anon_sym_DIVIDE] = ACTIONS(170),
    [anon_sym_GIVING] = ACTIONS(170),
    [anon_sym_REMAINDER] = ACTIONS(170),
    [anon_sym_STRING] = ACTIONS(170),
    [anon_sym_DELIMITED] = ACTIONS(170),
    [anon_sym_SIZE] = ACTIONS(170),
    [anon_sym_OVERFLOW] = ACTIONS(170),
    [anon_sym_NOT] = ACTIONS(170),
    [anon_sym_END_DASHSTRING] = ACTIONS(170),
    [anon_sym_UNSTRING] = ACTIONS(170),
    [anon_sym_COUNT] = ACTIONS(170),
    [anon_sym_DELIMITER] = ACTIONS(170),
    [anon_sym_TALLYING] = ACTIONS(170),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(170),
    [anon_sym_INSPECT] = ACTIONS(170),
    [anon_sym_CONVERTING] = ACTIONS(170),
    [anon_sym_FIRST] = ACTIONS(170),
    [anon_sym_INITIAL] = ACTIONS(170),
    [anon_sym_READ] = ACTIONS(170),
    [anon_sym_WRITE] = ACTIONS(170),
    [anon_sym_REWRITE] = ACTIONS(170),
    [anon_sym_DELETE] = ACTIONS(170),
    [anon_sym_START] = ACTIONS(170),
    [anon_sym_OPEN] = ACTIONS(170),
    [anon_sym_CLOSE] = ACTIONS(170),
    [anon_sym_INPUT] = ACTIONS(170),
    [anon_sym_OUTPUT] = ACTIONS(170),
    [anon_sym_I_DASHO] = ACTIONS(170),
    [anon_sym_EXTEND] = ACTIONS(170),
    [anon_sym_ACCEPT] = ACTIONS(170),
    [anon_sym_FROM] = ACTIONS(170),
    [anon_sym_DATE] = ACTIONS(170),
    [anon_sym_DAY] = ACTIONS(170),
    [anon_sym_TIME] = ACTIONS(170),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(170),
    [anon_sym_EQUAL] = ACTIONS(170),
    [anon_sym_GREATER] = ACTIONS(170),
    [anon_sym_LESS] = ACTIONS(170),
    [anon_sym_THAN] = ACTIONS(170),
    [anon_sym_OR] = ACTIONS(170),
    [anon_sym_AND] = ACTIONS(170),
    [anon_sym_DFHENTER] = ACTIONS(170),
    [anon_sym_DFHCLEAR] = ACTIONS(170),
    [anon_sym_DFHPA1] = ACTIONS(170),
    [anon_sym_DFHPA2] = ACTIONS(170),
    [anon_sym_DFHPF1] = ACTIONS(170),
    [anon_sym_DFHPF2] = ACTIONS(170),
    [anon_sym_DFHPF3] = ACTIONS(170),
    [anon_sym_DFHPF4] = ACTIONS(170),
    [anon_sym_DFHPF5] = ACTIONS(170),
    [anon_sym_DFHPF6] = ACTIONS(170),
    [anon_sym_DFHPF7] = ACTIONS(170),
    [anon_sym_DFHPF8] = ACTIONS(170),
    [anon_sym_DFHPF9] = ACTIONS(170),
    [anon_sym_DFHPF10] = ACTIONS(170),
    [anon_sym_DFHPF11] = ACTIONS(170),
    [anon_sym_DFHPF12] = ACTIONS(170),
    [anon_sym_EIBAID] = ACTIONS(170),
    [anon_sym_DFHRED] = ACTIONS(170),
    [anon_sym_DFHBMASB] = ACTIONS(170),
    [anon_sym_DFHBMASK] = ACTIONS(170),
    [aux_sym_identifier_token1] = ACTIONS(170),
    [aux_sym_identifier_token2] = ACTIONS(168),
    [sym_picture_string] = ACTIONS(170),
    [aux_sym_string_literal_token1] = ACTIONS(168),
    [aux_sym_string_literal_token2] = ACTIONS(168),
    [sym_number] = ACTIONS(170),
    [anon_sym_EQ_EQ] = ACTIONS(168),
    [anon_sym_EQ] = ACTIONS(170),
    [anon_sym_GT] = ACTIONS(170),
    [anon_sym_LT] = ACTIONS(170),
    [anon_sym_GT_EQ] = ACTIONS(168),
    [anon_sym_LT_EQ] = ACTIONS(168),
    [anon_sym_COMMA] = ACTIONS(170),
    [anon_sym_LPAREN] = ACTIONS(170),
    [anon_sym_RPAREN] = ACTIONS(168),
    [anon_sym_COLON] = ACTIONS(168),
  },
  [16] = {
    [aux_sym_newline_token1] = ACTIONS(174),
    [anon_sym_DOT] = ACTIONS(174),
    [anon_sym_88] = ACTIONS(176),
    [anon_sym_VALUE] = ACTIONS(176),
    [anon_sym_IS] = ACTIONS(176),
    [aux_sym_level_number_token1] = ACTIONS(176),
    [aux_sym_level_number_token2] = ACTIONS(176),
    [anon_sym_66] = ACTIONS(176),
    [anon_sym_77] = ACTIONS(176),
    [anon_sym_FILLER] = ACTIONS(176),
    [anon_sym_PIC] = ACTIONS(176),
    [anon_sym_PICTURE] = ACTIONS(176),
    [anon_sym_VALUES] = ACTIONS(176),
    [anon_sym_OCCURS] = ACTIONS(176),
    [anon_sym_TIMES] = ACTIONS(176),
    [anon_sym_TO] = ACTIONS(176),
    [anon_sym_REDEFINES] = ACTIONS(176),
    [anon_sym_INDEXED] = ACTIONS(176),
    [anon_sym_BY] = ACTIONS(176),
    [anon_sym_DEPENDING] = ACTIONS(176),
    [anon_sym_ON] = ACTIONS(176),
    [anon_sym_USAGE] = ACTIONS(176),
    [anon_sym_DISPLAY] = ACTIONS(176),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(176),
    [anon_sym_BINARY] = ACTIONS(176),
    [anon_sym_COMP] = ACTIONS(176),
    [anon_sym_COMP_DASH1] = ACTIONS(176),
    [anon_sym_COMP_DASH2] = ACTIONS(176),
    [anon_sym_COMP_DASH3] = ACTIONS(176),
    [anon_sym_COMP_DASH4] = ACTIONS(176),
    [anon_sym_COMP_DASH5] = ACTIONS(176),
    [anon_sym_COMPUTATIONAL] = ACTIONS(176),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(176),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(176),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(176),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(176),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(176),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(176),
    [anon_sym_INDEX] = ACTIONS(176),
    [anon_sym_POINTER] = ACTIONS(176),
    [anon_sym_ZERO] = ACTIONS(176),
    [anon_sym_ZEROS] = ACTIONS(176),
    [anon_sym_ZEROES] = ACTIONS(176),
    [anon_sym_SPACE] = ACTIONS(176),
    [anon_sym_SPACES] = ACTIONS(176),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(176),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(176),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(176),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(176),
    [anon_sym_QUOTE] = ACTIONS(176),
    [anon_sym_QUOTES] = ACTIONS(176),
    [anon_sym_NULL] = ACTIONS(176),
    [anon_sym_NULLS] = ACTIONS(176),
    [anon_sym_ALL] = ACTIONS(176),
    [anon_sym_THRU] = ACTIONS(176),
    [anon_sym_THROUGH] = ACTIONS(176),
    [anon_sym_ASCENDING] = ACTIONS(176),
    [anon_sym_DESCENDING] = ACTIONS(176),
    [anon_sym_KEY] = ACTIONS(176),
    [anon_sym_SIGN] = ACTIONS(176),
    [anon_sym_LEADING] = ACTIONS(176),
    [anon_sym_TRAILING] = ACTIONS(176),
    [anon_sym_SEPARATE] = ACTIONS(176),
    [anon_sym_CHARACTER] = ACTIONS(176),
    [anon_sym_SYNC] = ACTIONS(176),
    [anon_sym_SYNCHRONIZED] = ACTIONS(176),
    [anon_sym_LEFT] = ACTIONS(176),
    [anon_sym_RIGHT] = ACTIONS(176),
    [anon_sym_JUST] = ACTIONS(176),
    [anon_sym_JUSTIFIED] = ACTIONS(176),
    [anon_sym_BLANK] = ACTIONS(176),
    [anon_sym_WHEN] = ACTIONS(176),
    [anon_sym_EXTERNAL] = ACTIONS(176),
    [anon_sym_GLOBAL] = ACTIONS(176),
    [anon_sym_AS] = ACTIONS(176),
    [anon_sym_COPY] = ACTIONS(176),
    [anon_sym_REPLACING] = ACTIONS(176),
    [anon_sym_OF] = ACTIONS(176),
    [anon_sym_IN] = ACTIONS(176),
    [anon_sym_REPLACE] = ACTIONS(176),
    [anon_sym_OFF] = ACTIONS(176),
    [anon_sym_EJECT] = ACTIONS(176),
    [anon_sym_SKIP1] = ACTIONS(176),
    [anon_sym_SKIP2] = ACTIONS(176),
    [anon_sym_SKIP3] = ACTIONS(176),
    [anon_sym_EXEC] = ACTIONS(176),
    [anon_sym_EXECUTE] = ACTIONS(176),
    [anon_sym_SQL] = ACTIONS(176),
    [anon_sym_SQLIMS] = ACTIONS(176),
    [anon_sym_DLI] = ACTIONS(176),
    [anon_sym_END_DASHEXEC] = ACTIONS(176),
    [anon_sym_IF] = ACTIONS(176),
    [anon_sym_ELSE] = ACTIONS(176),
    [anon_sym_END_DASHIF] = ACTIONS(176),
    [anon_sym_THEN] = ACTIONS(176),
    [anon_sym_EVALUATE] = ACTIONS(176),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(176),
    [anon_sym_OTHER] = ACTIONS(176),
    [anon_sym_ALSO] = ACTIONS(176),
    [anon_sym_PERFORM] = ACTIONS(176),
    [anon_sym_END_DASHPERFORM] = ACTIONS(176),
    [anon_sym_UNTIL] = ACTIONS(176),
    [anon_sym_VARYING] = ACTIONS(176),
    [anon_sym_WITH] = ACTIONS(176),
    [anon_sym_TEST] = ACTIONS(176),
    [anon_sym_BEFORE] = ACTIONS(176),
    [anon_sym_AFTER] = ACTIONS(176),
    [anon_sym_GO] = ACTIONS(176),
    [anon_sym_SECTION] = ACTIONS(176),
    [anon_sym_PARAGRAPH] = ACTIONS(176),
    [anon_sym_CONTINUE] = ACTIONS(176),
    [anon_sym_NEXT] = ACTIONS(176),
    [anon_sym_SENTENCE] = ACTIONS(176),
    [anon_sym_EXIT] = ACTIONS(176),
    [anon_sym_STOP] = ACTIONS(176),
    [anon_sym_RUN] = ACTIONS(176),
    [anon_sym_MOVE] = ACTIONS(176),
    [anon_sym_CORRESPONDING] = ACTIONS(176),
    [anon_sym_CORR] = ACTIONS(176),
    [anon_sym_INTO] = ACTIONS(176),
    [anon_sym_SET] = ACTIONS(176),
    [anon_sym_TRUE] = ACTIONS(176),
    [anon_sym_FALSE] = ACTIONS(176),
    [anon_sym_INITIALIZE] = ACTIONS(176),
    [anon_sym_ALPHABETIC] = ACTIONS(176),
    [anon_sym_ALPHANUMERIC] = ACTIONS(176),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(176),
    [anon_sym_NUMERIC] = ACTIONS(176),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(176),
    [anon_sym_COMPUTE] = ACTIONS(176),
    [anon_sym_ADD] = ACTIONS(176),
    [anon_sym_SUBTRACT] = ACTIONS(176),
    [anon_sym_MULTIPLY] = ACTIONS(176),
    [anon_sym_DIVIDE] = ACTIONS(176),
    [anon_sym_GIVING] = ACTIONS(176),
    [anon_sym_REMAINDER] = ACTIONS(176),
    [anon_sym_STRING] = ACTIONS(176),
    [anon_sym_DELIMITED] = ACTIONS(176),
    [anon_sym_SIZE] = ACTIONS(176),
    [anon_sym_OVERFLOW] = ACTIONS(176),
    [anon_sym_NOT] = ACTIONS(176),
    [anon_sym_END_DASHSTRING] = ACTIONS(176),
    [anon_sym_UNSTRING] = ACTIONS(176),
    [anon_sym_COUNT] = ACTIONS(176),
    [anon_sym_DELIMITER] = ACTIONS(176),
    [anon_sym_TALLYING] = ACTIONS(176),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(176),
    [anon_sym_INSPECT] = ACTIONS(176),
    [anon_sym_CONVERTING] = ACTIONS(176),
    [anon_sym_FIRST] = ACTIONS(176),
    [anon_sym_INITIAL] = ACTIONS(176),
    [anon_sym_READ] = ACTIONS(176),
    [anon_sym_WRITE] = ACTIONS(176),
    [anon_sym_REWRITE] = ACTIONS(176),
    [anon_sym_DELETE] = ACTIONS(176),
    [anon_sym_START] = ACTIONS(176),
    [anon_sym_OPEN] = ACTIONS(176),
    [anon_sym_CLOSE] = ACTIONS(176),
    [anon_sym_INPUT] = ACTIONS(176),
    [anon_sym_OUTPUT] = ACTIONS(176),
    [anon_sym_I_DASHO] = ACTIONS(176),
    [anon_sym_EXTEND] = ACTIONS(176),
    [anon_sym_ACCEPT] = ACTIONS(176),
    [anon_sym_FROM] = ACTIONS(176),
    [anon_sym_DATE] = ACTIONS(176),
    [anon_sym_DAY] = ACTIONS(176),
    [anon_sym_TIME] = ACTIONS(176),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(176),
    [anon_sym_EQUAL] = ACTIONS(176),
    [anon_sym_GREATER] = ACTIONS(176),
    [anon_sym_LESS] = ACTIONS(176),
    [anon_sym_THAN] = ACTIONS(176),
    [anon_sym_OR] = ACTIONS(176),
    [anon_sym_AND] = ACTIONS(176),
    [anon_sym_DFHENTER] = ACTIONS(176),
    [anon_sym_DFHCLEAR] = ACTIONS(176),
    [anon_sym_DFHPA1] = ACTIONS(176),
    [anon_sym_DFHPA2] = ACTIONS(176),
    [anon_sym_DFHPF1] = ACTIONS(176),
    [anon_sym_DFHPF2] = ACTIONS(176),
    [anon_sym_DFHPF3] = ACTIONS(176),
    [anon_sym_DFHPF4] = ACTIONS(176),
    [anon_sym_DFHPF5] = ACTIONS(176),
    [anon_sym_DFHPF6] = ACTIONS(176),
    [anon_sym_DFHPF7] = ACTIONS(176),
    [anon_sym_DFHPF8] = ACTIONS(176),
    [anon_sym_DFHPF9] = ACTIONS(176),
    [anon_sym_DFHPF10] = ACTIONS(176),
    [anon_sym_DFHPF11] = ACTIONS(176),
    [anon_sym_DFHPF12] = ACTIONS(176),
    [anon_sym_EIBAID] = ACTIONS(176),
    [anon_sym_DFHRED] = ACTIONS(176),
    [anon_sym_DFHBMASB] = ACTIONS(176),
    [anon_sym_DFHBMASK] = ACTIONS(176),
    [aux_sym_identifier_token1] = ACTIONS(176),
    [aux_sym_identifier_token2] = ACTIONS(174),
    [sym_picture_string] = ACTIONS(176),
    [aux_sym_string_literal_token1] = ACTIONS(174),
    [aux_sym_string_literal_token2] = ACTIONS(174),
    [sym_number] = ACTIONS(176),
    [anon_sym_EQ_EQ] = ACTIONS(174),
    [anon_sym_EQ] = ACTIONS(176),
    [anon_sym_GT] = ACTIONS(176),
    [anon_sym_LT] = ACTIONS(176),
    [anon_sym_GT_EQ] = ACTIONS(174),
    [anon_sym_LT_EQ] = ACTIONS(174),
    [anon_sym_COMMA] = ACTIONS(176),
    [anon_sym_LPAREN] = ACTIONS(176),
    [anon_sym_RPAREN] = ACTIONS(174),
    [anon_sym_COLON] = ACTIONS(174),
  },
  [17] = {
    [aux_sym_newline_token1] = ACTIONS(130),
    [anon_sym_DOT] = ACTIONS(130),
    [anon_sym_88] = ACTIONS(132),
    [anon_sym_VALUE] = ACTIONS(132),
    [anon_sym_IS] = ACTIONS(132),
    [aux_sym_level_number_token1] = ACTIONS(132),
    [aux_sym_level_number_token2] = ACTIONS(132),
    [anon_sym_66] = ACTIONS(132),
    [anon_sym_77] = ACTIONS(132),
    [anon_sym_FILLER] = ACTIONS(132),
    [anon_sym_PIC] = ACTIONS(132),
    [anon_sym_PICTURE] = ACTIONS(132),
    [anon_sym_VALUES] = ACTIONS(132),
    [anon_sym_OCCURS] = ACTIONS(132),
    [anon_sym_TIMES] = ACTIONS(132),
    [anon_sym_TO] = ACTIONS(132),
    [anon_sym_REDEFINES] = ACTIONS(132),
    [anon_sym_INDEXED] = ACTIONS(132),
    [anon_sym_BY] = ACTIONS(132),
    [anon_sym_DEPENDING] = ACTIONS(132),
    [anon_sym_ON] = ACTIONS(132),
    [anon_sym_USAGE] = ACTIONS(132),
    [anon_sym_DISPLAY] = ACTIONS(132),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(132),
    [anon_sym_BINARY] = ACTIONS(132),
    [anon_sym_COMP] = ACTIONS(132),
    [anon_sym_COMP_DASH1] = ACTIONS(132),
    [anon_sym_COMP_DASH2] = ACTIONS(132),
    [anon_sym_COMP_DASH3] = ACTIONS(132),
    [anon_sym_COMP_DASH4] = ACTIONS(132),
    [anon_sym_COMP_DASH5] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(132),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(132),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(132),
    [anon_sym_INDEX] = ACTIONS(132),
    [anon_sym_POINTER] = ACTIONS(132),
    [anon_sym_ZERO] = ACTIONS(132),
    [anon_sym_ZEROS] = ACTIONS(132),
    [anon_sym_ZEROES] = ACTIONS(132),
    [anon_sym_SPACE] = ACTIONS(132),
    [anon_sym_SPACES] = ACTIONS(132),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(132),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(132),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(132),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(132),
    [anon_sym_QUOTE] = ACTIONS(132),
    [anon_sym_QUOTES] = ACTIONS(132),
    [anon_sym_NULL] = ACTIONS(132),
    [anon_sym_NULLS] = ACTIONS(132),
    [anon_sym_ALL] = ACTIONS(132),
    [anon_sym_THRU] = ACTIONS(132),
    [anon_sym_THROUGH] = ACTIONS(132),
    [anon_sym_ASCENDING] = ACTIONS(132),
    [anon_sym_DESCENDING] = ACTIONS(132),
    [anon_sym_KEY] = ACTIONS(132),
    [anon_sym_SIGN] = ACTIONS(132),
    [anon_sym_LEADING] = ACTIONS(132),
    [anon_sym_TRAILING] = ACTIONS(132),
    [anon_sym_SEPARATE] = ACTIONS(132),
    [anon_sym_CHARACTER] = ACTIONS(132),
    [anon_sym_SYNC] = ACTIONS(132),
    [anon_sym_SYNCHRONIZED] = ACTIONS(132),
    [anon_sym_LEFT] = ACTIONS(132),
    [anon_sym_RIGHT] = ACTIONS(132),
    [anon_sym_JUST] = ACTIONS(132),
    [anon_sym_JUSTIFIED] = ACTIONS(132),
    [anon_sym_BLANK] = ACTIONS(132),
    [anon_sym_WHEN] = ACTIONS(132),
    [anon_sym_EXTERNAL] = ACTIONS(132),
    [anon_sym_GLOBAL] = ACTIONS(132),
    [anon_sym_AS] = ACTIONS(132),
    [anon_sym_COPY] = ACTIONS(132),
    [anon_sym_REPLACING] = ACTIONS(132),
    [anon_sym_OF] = ACTIONS(132),
    [anon_sym_IN] = ACTIONS(132),
    [anon_sym_REPLACE] = ACTIONS(132),
    [anon_sym_OFF] = ACTIONS(132),
    [anon_sym_EJECT] = ACTIONS(132),
    [anon_sym_SKIP1] = ACTIONS(132),
    [anon_sym_SKIP2] = ACTIONS(132),
    [anon_sym_SKIP3] = ACTIONS(132),
    [anon_sym_EXEC] = ACTIONS(132),
    [anon_sym_EXECUTE] = ACTIONS(132),
    [anon_sym_SQL] = ACTIONS(132),
    [anon_sym_SQLIMS] = ACTIONS(132),
    [anon_sym_DLI] = ACTIONS(132),
    [anon_sym_END_DASHEXEC] = ACTIONS(132),
    [anon_sym_IF] = ACTIONS(132),
    [anon_sym_ELSE] = ACTIONS(132),
    [anon_sym_END_DASHIF] = ACTIONS(132),
    [anon_sym_THEN] = ACTIONS(132),
    [anon_sym_EVALUATE] = ACTIONS(132),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(132),
    [anon_sym_OTHER] = ACTIONS(132),
    [anon_sym_ALSO] = ACTIONS(132),
    [anon_sym_PERFORM] = ACTIONS(132),
    [anon_sym_END_DASHPERFORM] = ACTIONS(132),
    [anon_sym_UNTIL] = ACTIONS(132),
    [anon_sym_VARYING] = ACTIONS(132),
    [anon_sym_WITH] = ACTIONS(132),
    [anon_sym_TEST] = ACTIONS(132),
    [anon_sym_BEFORE] = ACTIONS(132),
    [anon_sym_AFTER] = ACTIONS(132),
    [anon_sym_GO] = ACTIONS(132),
    [anon_sym_SECTION] = ACTIONS(132),
    [anon_sym_PARAGRAPH] = ACTIONS(132),
    [anon_sym_CONTINUE] = ACTIONS(132),
    [anon_sym_NEXT] = ACTIONS(132),
    [anon_sym_SENTENCE] = ACTIONS(132),
    [anon_sym_EXIT] = ACTIONS(132),
    [anon_sym_STOP] = ACTIONS(132),
    [anon_sym_RUN] = ACTIONS(132),
    [anon_sym_MOVE] = ACTIONS(132),
    [anon_sym_CORRESPONDING] = ACTIONS(132),
    [anon_sym_CORR] = ACTIONS(132),
    [anon_sym_INTO] = ACTIONS(132),
    [anon_sym_SET] = ACTIONS(132),
    [anon_sym_TRUE] = ACTIONS(132),
    [anon_sym_FALSE] = ACTIONS(132),
    [anon_sym_INITIALIZE] = ACTIONS(132),
    [anon_sym_ALPHABETIC] = ACTIONS(132),
    [anon_sym_ALPHANUMERIC] = ACTIONS(132),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(132),
    [anon_sym_NUMERIC] = ACTIONS(132),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(132),
    [anon_sym_COMPUTE] = ACTIONS(132),
    [anon_sym_ADD] = ACTIONS(132),
    [anon_sym_SUBTRACT] = ACTIONS(132),
    [anon_sym_MULTIPLY] = ACTIONS(132),
    [anon_sym_DIVIDE] = ACTIONS(132),
    [anon_sym_GIVING] = ACTIONS(132),
    [anon_sym_REMAINDER] = ACTIONS(132),
    [anon_sym_STRING] = ACTIONS(132),
    [anon_sym_DELIMITED] = ACTIONS(132),
    [anon_sym_SIZE] = ACTIONS(132),
    [anon_sym_OVERFLOW] = ACTIONS(132),
    [anon_sym_NOT] = ACTIONS(132),
    [anon_sym_END_DASHSTRING] = ACTIONS(132),
    [anon_sym_UNSTRING] = ACTIONS(132),
    [anon_sym_COUNT] = ACTIONS(132),
    [anon_sym_DELIMITER] = ACTIONS(132),
    [anon_sym_TALLYING] = ACTIONS(132),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(132),
    [anon_sym_INSPECT] = ACTIONS(132),
    [anon_sym_CONVERTING] = ACTIONS(132),
    [anon_sym_FIRST] = ACTIONS(132),
    [anon_sym_INITIAL] = ACTIONS(132),
    [anon_sym_READ] = ACTIONS(132),
    [anon_sym_WRITE] = ACTIONS(132),
    [anon_sym_REWRITE] = ACTIONS(132),
    [anon_sym_DELETE] = ACTIONS(132),
    [anon_sym_START] = ACTIONS(132),
    [anon_sym_OPEN] = ACTIONS(132),
    [anon_sym_CLOSE] = ACTIONS(132),
    [anon_sym_INPUT] = ACTIONS(132),
    [anon_sym_OUTPUT] = ACTIONS(132),
    [anon_sym_I_DASHO] = ACTIONS(132),
    [anon_sym_EXTEND] = ACTIONS(132),
    [anon_sym_ACCEPT] = ACTIONS(132),
    [anon_sym_FROM] = ACTIONS(132),
    [anon_sym_DATE] = ACTIONS(132),
    [anon_sym_DAY] = ACTIONS(132),
    [anon_sym_TIME] = ACTIONS(132),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(132),
    [anon_sym_EQUAL] = ACTIONS(132),
    [anon_sym_GREATER] = ACTIONS(132),
    [anon_sym_LESS] = ACTIONS(132),
    [anon_sym_THAN] = ACTIONS(132),
    [anon_sym_OR] = ACTIONS(132),
    [anon_sym_AND] = ACTIONS(132),
    [anon_sym_DFHENTER] = ACTIONS(132),
    [anon_sym_DFHCLEAR] = ACTIONS(132),
    [anon_sym_DFHPA1] = ACTIONS(132),
    [anon_sym_DFHPA2] = ACTIONS(132),
    [anon_sym_DFHPF1] = ACTIONS(132),
    [anon_sym_DFHPF2] = ACTIONS(132),
    [anon_sym_DFHPF3] = ACTIONS(132),
    [anon_sym_DFHPF4] = ACTIONS(132),
    [anon_sym_DFHPF5] = ACTIONS(132),
    [anon_sym_DFHPF6] = ACTIONS(132),
    [anon_sym_DFHPF7] = ACTIONS(132),
    [anon_sym_DFHPF8] = ACTIONS(132),
    [anon_sym_DFHPF9] = ACTIONS(132),
    [anon_sym_DFHPF10] = ACTIONS(132),
    [anon_sym_DFHPF11] = ACTIONS(132),
    [anon_sym_DFHPF12] = ACTIONS(132),
    [anon_sym_EIBAID] = ACTIONS(132),
    [anon_sym_DFHRED] = ACTIONS(132),
    [anon_sym_DFHBMASB] = ACTIONS(132),
    [anon_sym_DFHBMASK] = ACTIONS(132),
    [aux_sym_identifier_token1] = ACTIONS(132),
    [aux_sym_identifier_token2] = ACTIONS(130),
    [sym_picture_string] = ACTIONS(132),
    [aux_sym_string_literal_token1] = ACTIONS(130),
    [aux_sym_string_literal_token2] = ACTIONS(130),
    [sym_number] = ACTIONS(132),
    [anon_sym_EQ_EQ] = ACTIONS(130),
    [anon_sym_EQ] = ACTIONS(132),
    [anon_sym_GT] = ACTIONS(132),
    [anon_sym_LT] = ACTIONS(132),
    [anon_sym_GT_EQ] = ACTIONS(130),
    [anon_sym_LT_EQ] = ACTIONS(130),
    [anon_sym_COMMA] = ACTIONS(132),
    [anon_sym_LPAREN] = ACTIONS(132),
    [anon_sym_RPAREN] = ACTIONS(130),
    [anon_sym_COLON] = ACTIONS(130),
  },
  [18] = {
    [aux_sym_newline_token1] = ACTIONS(178),
    [anon_sym_DOT] = ACTIONS(178),
    [anon_sym_88] = ACTIONS(180),
    [anon_sym_VALUE] = ACTIONS(180),
    [anon_sym_IS] = ACTIONS(180),
    [aux_sym_level_number_token1] = ACTIONS(180),
    [aux_sym_level_number_token2] = ACTIONS(180),
    [anon_sym_66] = ACTIONS(180),
    [anon_sym_77] = ACTIONS(180),
    [anon_sym_FILLER] = ACTIONS(180),
    [anon_sym_PIC] = ACTIONS(180),
    [anon_sym_PICTURE] = ACTIONS(180),
    [anon_sym_VALUES] = ACTIONS(180),
    [anon_sym_OCCURS] = ACTIONS(180),
    [anon_sym_TIMES] = ACTIONS(180),
    [anon_sym_TO] = ACTIONS(180),
    [anon_sym_REDEFINES] = ACTIONS(180),
    [anon_sym_INDEXED] = ACTIONS(180),
    [anon_sym_BY] = ACTIONS(180),
    [anon_sym_DEPENDING] = ACTIONS(180),
    [anon_sym_ON] = ACTIONS(180),
    [anon_sym_USAGE] = ACTIONS(180),
    [anon_sym_DISPLAY] = ACTIONS(180),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(180),
    [anon_sym_BINARY] = ACTIONS(180),
    [anon_sym_COMP] = ACTIONS(180),
    [anon_sym_COMP_DASH1] = ACTIONS(180),
    [anon_sym_COMP_DASH2] = ACTIONS(180),
    [anon_sym_COMP_DASH3] = ACTIONS(180),
    [anon_sym_COMP_DASH4] = ACTIONS(180),
    [anon_sym_COMP_DASH5] = ACTIONS(180),
    [anon_sym_COMPUTATIONAL] = ACTIONS(180),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(180),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(180),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(180),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(180),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(180),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(180),
    [anon_sym_INDEX] = ACTIONS(180),
    [anon_sym_POINTER] = ACTIONS(180),
    [anon_sym_ZERO] = ACTIONS(180),
    [anon_sym_ZEROS] = ACTIONS(180),
    [anon_sym_ZEROES] = ACTIONS(180),
    [anon_sym_SPACE] = ACTIONS(180),
    [anon_sym_SPACES] = ACTIONS(180),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(180),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(180),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(180),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(180),
    [anon_sym_QUOTE] = ACTIONS(180),
    [anon_sym_QUOTES] = ACTIONS(180),
    [anon_sym_NULL] = ACTIONS(180),
    [anon_sym_NULLS] = ACTIONS(180),
    [anon_sym_ALL] = ACTIONS(180),
    [anon_sym_THRU] = ACTIONS(180),
    [anon_sym_THROUGH] = ACTIONS(180),
    [anon_sym_ASCENDING] = ACTIONS(180),
    [anon_sym_DESCENDING] = ACTIONS(180),
    [anon_sym_KEY] = ACTIONS(180),
    [anon_sym_SIGN] = ACTIONS(180),
    [anon_sym_LEADING] = ACTIONS(180),
    [anon_sym_TRAILING] = ACTIONS(180),
    [anon_sym_SEPARATE] = ACTIONS(180),
    [anon_sym_CHARACTER] = ACTIONS(180),
    [anon_sym_SYNC] = ACTIONS(180),
    [anon_sym_SYNCHRONIZED] = ACTIONS(180),
    [anon_sym_LEFT] = ACTIONS(180),
    [anon_sym_RIGHT] = ACTIONS(180),
    [anon_sym_JUST] = ACTIONS(180),
    [anon_sym_JUSTIFIED] = ACTIONS(180),
    [anon_sym_BLANK] = ACTIONS(180),
    [anon_sym_WHEN] = ACTIONS(180),
    [anon_sym_EXTERNAL] = ACTIONS(180),
    [anon_sym_GLOBAL] = ACTIONS(180),
    [anon_sym_AS] = ACTIONS(180),
    [anon_sym_COPY] = ACTIONS(180),
    [anon_sym_REPLACING] = ACTIONS(180),
    [anon_sym_OF] = ACTIONS(180),
    [anon_sym_IN] = ACTIONS(180),
    [anon_sym_REPLACE] = ACTIONS(180),
    [anon_sym_OFF] = ACTIONS(180),
    [anon_sym_EJECT] = ACTIONS(180),
    [anon_sym_SKIP1] = ACTIONS(180),
    [anon_sym_SKIP2] = ACTIONS(180),
    [anon_sym_SKIP3] = ACTIONS(180),
    [anon_sym_EXEC] = ACTIONS(180),
    [anon_sym_EXECUTE] = ACTIONS(180),
    [anon_sym_SQL] = ACTIONS(180),
    [anon_sym_SQLIMS] = ACTIONS(180),
    [anon_sym_DLI] = ACTIONS(180),
    [anon_sym_END_DASHEXEC] = ACTIONS(180),
    [anon_sym_IF] = ACTIONS(180),
    [anon_sym_ELSE] = ACTIONS(180),
    [anon_sym_END_DASHIF] = ACTIONS(180),
    [anon_sym_THEN] = ACTIONS(180),
    [anon_sym_EVALUATE] = ACTIONS(180),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(180),
    [anon_sym_OTHER] = ACTIONS(180),
    [anon_sym_ALSO] = ACTIONS(180),
    [anon_sym_PERFORM] = ACTIONS(180),
    [anon_sym_END_DASHPERFORM] = ACTIONS(180),
    [anon_sym_UNTIL] = ACTIONS(180),
    [anon_sym_VARYING] = ACTIONS(180),
    [anon_sym_WITH] = ACTIONS(180),
    [anon_sym_TEST] = ACTIONS(180),
    [anon_sym_BEFORE] = ACTIONS(180),
    [anon_sym_AFTER] = ACTIONS(180),
    [anon_sym_GO] = ACTIONS(180),
    [anon_sym_SECTION] = ACTIONS(180),
    [anon_sym_PARAGRAPH] = ACTIONS(180),
    [anon_sym_CONTINUE] = ACTIONS(180),
    [anon_sym_NEXT] = ACTIONS(180),
    [anon_sym_SENTENCE] = ACTIONS(180),
    [anon_sym_EXIT] = ACTIONS(180),
    [anon_sym_STOP] = ACTIONS(180),
    [anon_sym_RUN] = ACTIONS(180),
    [anon_sym_MOVE] = ACTIONS(180),
    [anon_sym_CORRESPONDING] = ACTIONS(180),
    [anon_sym_CORR] = ACTIONS(180),
    [anon_sym_INTO] = ACTIONS(180),
    [anon_sym_SET] = ACTIONS(180),
    [anon_sym_TRUE] = ACTIONS(180),
    [anon_sym_FALSE] = ACTIONS(180),
    [anon_sym_INITIALIZE] = ACTIONS(180),
    [anon_sym_ALPHABETIC] = ACTIONS(180),
    [anon_sym_ALPHANUMERIC] = ACTIONS(180),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(180),
    [anon_sym_NUMERIC] = ACTIONS(180),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(180),
    [anon_sym_COMPUTE] = ACTIONS(180),
    [anon_sym_ADD] = ACTIONS(180),
    [anon_sym_SUBTRACT] = ACTIONS(180),
    [anon_sym_MULTIPLY] = ACTIONS(180),
    [anon_sym_DIVIDE] = ACTIONS(180),
    [anon_sym_GIVING] = ACTIONS(180),
    [anon_sym_REMAINDER] = ACTIONS(180),
    [anon_sym_STRING] = ACTIONS(180),
    [anon_sym_DELIMITED] = ACTIONS(180),
    [anon_sym_SIZE] = ACTIONS(180),
    [anon_sym_OVERFLOW] = ACTIONS(180),
    [anon_sym_NOT] = ACTIONS(180),
    [anon_sym_END_DASHSTRING] = ACTIONS(180),
    [anon_sym_UNSTRING] = ACTIONS(180),
    [anon_sym_COUNT] = ACTIONS(180),
    [anon_sym_DELIMITER] = ACTIONS(180),
    [anon_sym_TALLYING] = ACTIONS(180),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(180),
    [anon_sym_INSPECT] = ACTIONS(180),
    [anon_sym_CONVERTING] = ACTIONS(180),
    [anon_sym_FIRST] = ACTIONS(180),
    [anon_sym_INITIAL] = ACTIONS(180),
    [anon_sym_READ] = ACTIONS(180),
    [anon_sym_WRITE] = ACTIONS(180),
    [anon_sym_REWRITE] = ACTIONS(180),
    [anon_sym_DELETE] = ACTIONS(180),
    [anon_sym_START] = ACTIONS(180),
    [anon_sym_OPEN] = ACTIONS(180),
    [anon_sym_CLOSE] = ACTIONS(180),
    [anon_sym_INPUT] = ACTIONS(180),
    [anon_sym_OUTPUT] = ACTIONS(180),
    [anon_sym_I_DASHO] = ACTIONS(180),
    [anon_sym_EXTEND] = ACTIONS(180),
    [anon_sym_ACCEPT] = ACTIONS(180),
    [anon_sym_FROM] = ACTIONS(180),
    [anon_sym_DATE] = ACTIONS(180),
    [anon_sym_DAY] = ACTIONS(180),
    [anon_sym_TIME] = ACTIONS(180),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(180),
    [anon_sym_EQUAL] = ACTIONS(180),
    [anon_sym_GREATER] = ACTIONS(180),
    [anon_sym_LESS] = ACTIONS(180),
    [anon_sym_THAN] = ACTIONS(180),
    [anon_sym_OR] = ACTIONS(180),
    [anon_sym_AND] = ACTIONS(180),
    [anon_sym_DFHENTER] = ACTIONS(180),
    [anon_sym_DFHCLEAR] = ACTIONS(180),
    [anon_sym_DFHPA1] = ACTIONS(180),
    [anon_sym_DFHPA2] = ACTIONS(180),
    [anon_sym_DFHPF1] = ACTIONS(180),
    [anon_sym_DFHPF2] = ACTIONS(180),
    [anon_sym_DFHPF3] = ACTIONS(180),
    [anon_sym_DFHPF4] = ACTIONS(180),
    [anon_sym_DFHPF5] = ACTIONS(180),
    [anon_sym_DFHPF6] = ACTIONS(180),
    [anon_sym_DFHPF7] = ACTIONS(180),
    [anon_sym_DFHPF8] = ACTIONS(180),
    [anon_sym_DFHPF9] = ACTIONS(180),
    [anon_sym_DFHPF10] = ACTIONS(180),
    [anon_sym_DFHPF11] = ACTIONS(180),
    [anon_sym_DFHPF12] = ACTIONS(180),
    [anon_sym_EIBAID] = ACTIONS(180),
    [anon_sym_DFHRED] = ACTIONS(180),
    [anon_sym_DFHBMASB] = ACTIONS(180),
    [anon_sym_DFHBMASK] = ACTIONS(180),
    [aux_sym_identifier_token1] = ACTIONS(180),
    [aux_sym_identifier_token2] = ACTIONS(178),
    [sym_picture_string] = ACTIONS(180),
    [aux_sym_string_literal_token1] = ACTIONS(178),
    [aux_sym_string_literal_token2] = ACTIONS(178),
    [sym_number] = ACTIONS(180),
    [anon_sym_EQ_EQ] = ACTIONS(178),
    [anon_sym_EQ] = ACTIONS(180),
    [anon_sym_GT] = ACTIONS(180),
    [anon_sym_LT] = ACTIONS(180),
    [anon_sym_GT_EQ] = ACTIONS(178),
    [anon_sym_LT_EQ] = ACTIONS(178),
    [anon_sym_COMMA] = ACTIONS(180),
    [anon_sym_LPAREN] = ACTIONS(180),
    [anon_sym_RPAREN] = ACTIONS(178),
    [anon_sym_COLON] = ACTIONS(178),
  },
  [19] = {
    [aux_sym_newline_token1] = ACTIONS(182),
    [anon_sym_DOT] = ACTIONS(182),
    [anon_sym_88] = ACTIONS(184),
    [anon_sym_VALUE] = ACTIONS(184),
    [anon_sym_IS] = ACTIONS(184),
    [aux_sym_level_number_token1] = ACTIONS(184),
    [aux_sym_level_number_token2] = ACTIONS(184),
    [anon_sym_66] = ACTIONS(184),
    [anon_sym_77] = ACTIONS(184),
    [anon_sym_FILLER] = ACTIONS(184),
    [anon_sym_PIC] = ACTIONS(184),
    [anon_sym_PICTURE] = ACTIONS(184),
    [anon_sym_VALUES] = ACTIONS(184),
    [anon_sym_OCCURS] = ACTIONS(184),
    [anon_sym_TIMES] = ACTIONS(184),
    [anon_sym_TO] = ACTIONS(184),
    [anon_sym_REDEFINES] = ACTIONS(184),
    [anon_sym_INDEXED] = ACTIONS(184),
    [anon_sym_BY] = ACTIONS(184),
    [anon_sym_DEPENDING] = ACTIONS(184),
    [anon_sym_ON] = ACTIONS(184),
    [anon_sym_USAGE] = ACTIONS(184),
    [anon_sym_DISPLAY] = ACTIONS(184),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(184),
    [anon_sym_BINARY] = ACTIONS(184),
    [anon_sym_COMP] = ACTIONS(184),
    [anon_sym_COMP_DASH1] = ACTIONS(184),
    [anon_sym_COMP_DASH2] = ACTIONS(184),
    [anon_sym_COMP_DASH3] = ACTIONS(184),
    [anon_sym_COMP_DASH4] = ACTIONS(184),
    [anon_sym_COMP_DASH5] = ACTIONS(184),
    [anon_sym_COMPUTATIONAL] = ACTIONS(184),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(184),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(184),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(184),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(184),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(184),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(184),
    [anon_sym_INDEX] = ACTIONS(184),
    [anon_sym_POINTER] = ACTIONS(184),
    [anon_sym_ZERO] = ACTIONS(184),
    [anon_sym_ZEROS] = ACTIONS(184),
    [anon_sym_ZEROES] = ACTIONS(184),
    [anon_sym_SPACE] = ACTIONS(184),
    [anon_sym_SPACES] = ACTIONS(184),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(184),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(184),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(184),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(184),
    [anon_sym_QUOTE] = ACTIONS(184),
    [anon_sym_QUOTES] = ACTIONS(184),
    [anon_sym_NULL] = ACTIONS(184),
    [anon_sym_NULLS] = ACTIONS(184),
    [anon_sym_ALL] = ACTIONS(184),
    [anon_sym_THRU] = ACTIONS(184),
    [anon_sym_THROUGH] = ACTIONS(184),
    [anon_sym_ASCENDING] = ACTIONS(184),
    [anon_sym_DESCENDING] = ACTIONS(184),
    [anon_sym_KEY] = ACTIONS(184),
    [anon_sym_SIGN] = ACTIONS(184),
    [anon_sym_LEADING] = ACTIONS(184),
    [anon_sym_TRAILING] = ACTIONS(184),
    [anon_sym_SEPARATE] = ACTIONS(184),
    [anon_sym_CHARACTER] = ACTIONS(184),
    [anon_sym_SYNC] = ACTIONS(184),
    [anon_sym_SYNCHRONIZED] = ACTIONS(184),
    [anon_sym_LEFT] = ACTIONS(184),
    [anon_sym_RIGHT] = ACTIONS(184),
    [anon_sym_JUST] = ACTIONS(184),
    [anon_sym_JUSTIFIED] = ACTIONS(184),
    [anon_sym_BLANK] = ACTIONS(184),
    [anon_sym_WHEN] = ACTIONS(184),
    [anon_sym_EXTERNAL] = ACTIONS(184),
    [anon_sym_GLOBAL] = ACTIONS(184),
    [anon_sym_AS] = ACTIONS(184),
    [anon_sym_COPY] = ACTIONS(184),
    [anon_sym_REPLACING] = ACTIONS(184),
    [anon_sym_OF] = ACTIONS(184),
    [anon_sym_IN] = ACTIONS(184),
    [anon_sym_REPLACE] = ACTIONS(184),
    [anon_sym_OFF] = ACTIONS(184),
    [anon_sym_EJECT] = ACTIONS(184),
    [anon_sym_SKIP1] = ACTIONS(184),
    [anon_sym_SKIP2] = ACTIONS(184),
    [anon_sym_SKIP3] = ACTIONS(184),
    [anon_sym_EXEC] = ACTIONS(184),
    [anon_sym_EXECUTE] = ACTIONS(184),
    [anon_sym_SQL] = ACTIONS(184),
    [anon_sym_SQLIMS] = ACTIONS(184),
    [anon_sym_DLI] = ACTIONS(184),
    [anon_sym_END_DASHEXEC] = ACTIONS(184),
    [anon_sym_IF] = ACTIONS(184),
    [anon_sym_ELSE] = ACTIONS(184),
    [anon_sym_END_DASHIF] = ACTIONS(184),
    [anon_sym_THEN] = ACTIONS(184),
    [anon_sym_EVALUATE] = ACTIONS(184),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(184),
    [anon_sym_OTHER] = ACTIONS(184),
    [anon_sym_ALSO] = ACTIONS(184),
    [anon_sym_PERFORM] = ACTIONS(184),
    [anon_sym_END_DASHPERFORM] = ACTIONS(184),
    [anon_sym_UNTIL] = ACTIONS(184),
    [anon_sym_VARYING] = ACTIONS(184),
    [anon_sym_WITH] = ACTIONS(184),
    [anon_sym_TEST] = ACTIONS(184),
    [anon_sym_BEFORE] = ACTIONS(184),
    [anon_sym_AFTER] = ACTIONS(184),
    [anon_sym_GO] = ACTIONS(184),
    [anon_sym_SECTION] = ACTIONS(184),
    [anon_sym_PARAGRAPH] = ACTIONS(184),
    [anon_sym_CONTINUE] = ACTIONS(184),
    [anon_sym_NEXT] = ACTIONS(184),
    [anon_sym_SENTENCE] = ACTIONS(184),
    [anon_sym_EXIT] = ACTIONS(184),
    [anon_sym_STOP] = ACTIONS(184),
    [anon_sym_RUN] = ACTIONS(184),
    [anon_sym_MOVE] = ACTIONS(184),
    [anon_sym_CORRESPONDING] = ACTIONS(184),
    [anon_sym_CORR] = ACTIONS(184),
    [anon_sym_INTO] = ACTIONS(184),
    [anon_sym_SET] = ACTIONS(184),
    [anon_sym_TRUE] = ACTIONS(184),
    [anon_sym_FALSE] = ACTIONS(184),
    [anon_sym_INITIALIZE] = ACTIONS(184),
    [anon_sym_ALPHABETIC] = ACTIONS(184),
    [anon_sym_ALPHANUMERIC] = ACTIONS(184),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(184),
    [anon_sym_NUMERIC] = ACTIONS(184),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(184),
    [anon_sym_COMPUTE] = ACTIONS(184),
    [anon_sym_ADD] = ACTIONS(184),
    [anon_sym_SUBTRACT] = ACTIONS(184),
    [anon_sym_MULTIPLY] = ACTIONS(184),
    [anon_sym_DIVIDE] = ACTIONS(184),
    [anon_sym_GIVING] = ACTIONS(184),
    [anon_sym_REMAINDER] = ACTIONS(184),
    [anon_sym_STRING] = ACTIONS(184),
    [anon_sym_DELIMITED] = ACTIONS(184),
    [anon_sym_SIZE] = ACTIONS(184),
    [anon_sym_OVERFLOW] = ACTIONS(184),
    [anon_sym_NOT] = ACTIONS(184),
    [anon_sym_END_DASHSTRING] = ACTIONS(184),
    [anon_sym_UNSTRING] = ACTIONS(184),
    [anon_sym_COUNT] = ACTIONS(184),
    [anon_sym_DELIMITER] = ACTIONS(184),
    [anon_sym_TALLYING] = ACTIONS(184),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(184),
    [anon_sym_INSPECT] = ACTIONS(184),
    [anon_sym_CONVERTING] = ACTIONS(184),
    [anon_sym_FIRST] = ACTIONS(184),
    [anon_sym_INITIAL] = ACTIONS(184),
    [anon_sym_READ] = ACTIONS(184),
    [anon_sym_WRITE] = ACTIONS(184),
    [anon_sym_REWRITE] = ACTIONS(184),
    [anon_sym_DELETE] = ACTIONS(184),
    [anon_sym_START] = ACTIONS(184),
    [anon_sym_OPEN] = ACTIONS(184),
    [anon_sym_CLOSE] = ACTIONS(184),
    [anon_sym_INPUT] = ACTIONS(184),
    [anon_sym_OUTPUT] = ACTIONS(184),
    [anon_sym_I_DASHO] = ACTIONS(184),
    [anon_sym_EXTEND] = ACTIONS(184),
    [anon_sym_ACCEPT] = ACTIONS(184),
    [anon_sym_FROM] = ACTIONS(184),
    [anon_sym_DATE] = ACTIONS(184),
    [anon_sym_DAY] = ACTIONS(184),
    [anon_sym_TIME] = ACTIONS(184),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(184),
    [anon_sym_EQUAL] = ACTIONS(184),
    [anon_sym_GREATER] = ACTIONS(184),
    [anon_sym_LESS] = ACTIONS(184),
    [anon_sym_THAN] = ACTIONS(184),
    [anon_sym_OR] = ACTIONS(184),
    [anon_sym_AND] = ACTIONS(184),
    [anon_sym_DFHENTER] = ACTIONS(184),
    [anon_sym_DFHCLEAR] = ACTIONS(184),
    [anon_sym_DFHPA1] = ACTIONS(184),
    [anon_sym_DFHPA2] = ACTIONS(184),
    [anon_sym_DFHPF1] = ACTIONS(184),
    [anon_sym_DFHPF2] = ACTIONS(184),
    [anon_sym_DFHPF3] = ACTIONS(184),
    [anon_sym_DFHPF4] = ACTIONS(184),
    [anon_sym_DFHPF5] = ACTIONS(184),
    [anon_sym_DFHPF6] = ACTIONS(184),
    [anon_sym_DFHPF7] = ACTIONS(184),
    [anon_sym_DFHPF8] = ACTIONS(184),
    [anon_sym_DFHPF9] = ACTIONS(184),
    [anon_sym_DFHPF10] = ACTIONS(184),
    [anon_sym_DFHPF11] = ACTIONS(184),
    [anon_sym_DFHPF12] = ACTIONS(184),
    [anon_sym_EIBAID] = ACTIONS(184),
    [anon_sym_DFHRED] = ACTIONS(184),
    [anon_sym_DFHBMASB] = ACTIONS(184),
    [anon_sym_DFHBMASK] = ACTIONS(184),
    [aux_sym_identifier_token1] = ACTIONS(184),
    [aux_sym_identifier_token2] = ACTIONS(182),
    [sym_picture_string] = ACTIONS(184),
    [aux_sym_string_literal_token1] = ACTIONS(182),
    [aux_sym_string_literal_token2] = ACTIONS(182),
    [sym_number] = ACTIONS(184),
    [anon_sym_EQ_EQ] = ACTIONS(182),
    [anon_sym_EQ] = ACTIONS(184),
    [anon_sym_GT] = ACTIONS(184),
    [anon_sym_LT] = ACTIONS(184),
    [anon_sym_GT_EQ] = ACTIONS(182),
    [anon_sym_LT_EQ] = ACTIONS(182),
    [anon_sym_COMMA] = ACTIONS(184),
    [anon_sym_LPAREN] = ACTIONS(184),
    [anon_sym_RPAREN] = ACTIONS(182),
    [anon_sym_COLON] = ACTIONS(182),
  },
  [20] = {
    [aux_sym_newline_token1] = ACTIONS(186),
    [anon_sym_DOT] = ACTIONS(186),
    [anon_sym_88] = ACTIONS(188),
    [anon_sym_VALUE] = ACTIONS(188),
    [anon_sym_IS] = ACTIONS(188),
    [aux_sym_level_number_token1] = ACTIONS(188),
    [aux_sym_level_number_token2] = ACTIONS(188),
    [anon_sym_66] = ACTIONS(188),
    [anon_sym_77] = ACTIONS(188),
    [anon_sym_FILLER] = ACTIONS(188),
    [anon_sym_PIC] = ACTIONS(188),
    [anon_sym_PICTURE] = ACTIONS(188),
    [anon_sym_VALUES] = ACTIONS(188),
    [anon_sym_OCCURS] = ACTIONS(188),
    [anon_sym_TIMES] = ACTIONS(188),
    [anon_sym_TO] = ACTIONS(188),
    [anon_sym_REDEFINES] = ACTIONS(188),
    [anon_sym_INDEXED] = ACTIONS(188),
    [anon_sym_BY] = ACTIONS(188),
    [anon_sym_DEPENDING] = ACTIONS(188),
    [anon_sym_ON] = ACTIONS(188),
    [anon_sym_USAGE] = ACTIONS(188),
    [anon_sym_DISPLAY] = ACTIONS(188),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(188),
    [anon_sym_BINARY] = ACTIONS(188),
    [anon_sym_COMP] = ACTIONS(188),
    [anon_sym_COMP_DASH1] = ACTIONS(188),
    [anon_sym_COMP_DASH2] = ACTIONS(188),
    [anon_sym_COMP_DASH3] = ACTIONS(188),
    [anon_sym_COMP_DASH4] = ACTIONS(188),
    [anon_sym_COMP_DASH5] = ACTIONS(188),
    [anon_sym_COMPUTATIONAL] = ACTIONS(188),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(188),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(188),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(188),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(188),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(188),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(188),
    [anon_sym_INDEX] = ACTIONS(188),
    [anon_sym_POINTER] = ACTIONS(188),
    [anon_sym_ZERO] = ACTIONS(188),
    [anon_sym_ZEROS] = ACTIONS(188),
    [anon_sym_ZEROES] = ACTIONS(188),
    [anon_sym_SPACE] = ACTIONS(188),
    [anon_sym_SPACES] = ACTIONS(188),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(188),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(188),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(188),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(188),
    [anon_sym_QUOTE] = ACTIONS(188),
    [anon_sym_QUOTES] = ACTIONS(188),
    [anon_sym_NULL] = ACTIONS(188),
    [anon_sym_NULLS] = ACTIONS(188),
    [anon_sym_ALL] = ACTIONS(188),
    [anon_sym_THRU] = ACTIONS(188),
    [anon_sym_THROUGH] = ACTIONS(188),
    [anon_sym_ASCENDING] = ACTIONS(188),
    [anon_sym_DESCENDING] = ACTIONS(188),
    [anon_sym_KEY] = ACTIONS(188),
    [anon_sym_SIGN] = ACTIONS(188),
    [anon_sym_LEADING] = ACTIONS(188),
    [anon_sym_TRAILING] = ACTIONS(188),
    [anon_sym_SEPARATE] = ACTIONS(188),
    [anon_sym_CHARACTER] = ACTIONS(188),
    [anon_sym_SYNC] = ACTIONS(188),
    [anon_sym_SYNCHRONIZED] = ACTIONS(188),
    [anon_sym_LEFT] = ACTIONS(188),
    [anon_sym_RIGHT] = ACTIONS(188),
    [anon_sym_JUST] = ACTIONS(188),
    [anon_sym_JUSTIFIED] = ACTIONS(188),
    [anon_sym_BLANK] = ACTIONS(188),
    [anon_sym_WHEN] = ACTIONS(188),
    [anon_sym_EXTERNAL] = ACTIONS(188),
    [anon_sym_GLOBAL] = ACTIONS(188),
    [anon_sym_AS] = ACTIONS(188),
    [anon_sym_COPY] = ACTIONS(188),
    [anon_sym_REPLACING] = ACTIONS(188),
    [anon_sym_OF] = ACTIONS(188),
    [anon_sym_IN] = ACTIONS(188),
    [anon_sym_REPLACE] = ACTIONS(188),
    [anon_sym_OFF] = ACTIONS(188),
    [anon_sym_EJECT] = ACTIONS(188),
    [anon_sym_SKIP1] = ACTIONS(188),
    [anon_sym_SKIP2] = ACTIONS(188),
    [anon_sym_SKIP3] = ACTIONS(188),
    [anon_sym_EXEC] = ACTIONS(188),
    [anon_sym_EXECUTE] = ACTIONS(188),
    [anon_sym_SQL] = ACTIONS(188),
    [anon_sym_SQLIMS] = ACTIONS(188),
    [anon_sym_DLI] = ACTIONS(188),
    [anon_sym_END_DASHEXEC] = ACTIONS(188),
    [anon_sym_IF] = ACTIONS(188),
    [anon_sym_ELSE] = ACTIONS(188),
    [anon_sym_END_DASHIF] = ACTIONS(188),
    [anon_sym_THEN] = ACTIONS(188),
    [anon_sym_EVALUATE] = ACTIONS(188),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(188),
    [anon_sym_OTHER] = ACTIONS(188),
    [anon_sym_ALSO] = ACTIONS(188),
    [anon_sym_PERFORM] = ACTIONS(188),
    [anon_sym_END_DASHPERFORM] = ACTIONS(188),
    [anon_sym_UNTIL] = ACTIONS(188),
    [anon_sym_VARYING] = ACTIONS(188),
    [anon_sym_WITH] = ACTIONS(188),
    [anon_sym_TEST] = ACTIONS(188),
    [anon_sym_BEFORE] = ACTIONS(188),
    [anon_sym_AFTER] = ACTIONS(188),
    [anon_sym_GO] = ACTIONS(188),
    [anon_sym_SECTION] = ACTIONS(188),
    [anon_sym_PARAGRAPH] = ACTIONS(188),
    [anon_sym_CONTINUE] = ACTIONS(188),
    [anon_sym_NEXT] = ACTIONS(188),
    [anon_sym_SENTENCE] = ACTIONS(188),
    [anon_sym_EXIT] = ACTIONS(188),
    [anon_sym_STOP] = ACTIONS(188),
    [anon_sym_RUN] = ACTIONS(188),
    [anon_sym_MOVE] = ACTIONS(188),
    [anon_sym_CORRESPONDING] = ACTIONS(188),
    [anon_sym_CORR] = ACTIONS(188),
    [anon_sym_INTO] = ACTIONS(188),
    [anon_sym_SET] = ACTIONS(188),
    [anon_sym_TRUE] = ACTIONS(188),
    [anon_sym_FALSE] = ACTIONS(188),
    [anon_sym_INITIALIZE] = ACTIONS(188),
    [anon_sym_ALPHABETIC] = ACTIONS(188),
    [anon_sym_ALPHANUMERIC] = ACTIONS(188),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(188),
    [anon_sym_NUMERIC] = ACTIONS(188),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(188),
    [anon_sym_COMPUTE] = ACTIONS(188),
    [anon_sym_ADD] = ACTIONS(188),
    [anon_sym_SUBTRACT] = ACTIONS(188),
    [anon_sym_MULTIPLY] = ACTIONS(188),
    [anon_sym_DIVIDE] = ACTIONS(188),
    [anon_sym_GIVING] = ACTIONS(188),
    [anon_sym_REMAINDER] = ACTIONS(188),
    [anon_sym_STRING] = ACTIONS(188),
    [anon_sym_DELIMITED] = ACTIONS(188),
    [anon_sym_SIZE] = ACTIONS(188),
    [anon_sym_OVERFLOW] = ACTIONS(188),
    [anon_sym_NOT] = ACTIONS(188),
    [anon_sym_END_DASHSTRING] = ACTIONS(188),
    [anon_sym_UNSTRING] = ACTIONS(188),
    [anon_sym_COUNT] = ACTIONS(188),
    [anon_sym_DELIMITER] = ACTIONS(188),
    [anon_sym_TALLYING] = ACTIONS(188),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(188),
    [anon_sym_INSPECT] = ACTIONS(188),
    [anon_sym_CONVERTING] = ACTIONS(188),
    [anon_sym_FIRST] = ACTIONS(188),
    [anon_sym_INITIAL] = ACTIONS(188),
    [anon_sym_READ] = ACTIONS(188),
    [anon_sym_WRITE] = ACTIONS(188),
    [anon_sym_REWRITE] = ACTIONS(188),
    [anon_sym_DELETE] = ACTIONS(188),
    [anon_sym_START] = ACTIONS(188),
    [anon_sym_OPEN] = ACTIONS(188),
    [anon_sym_CLOSE] = ACTIONS(188),
    [anon_sym_INPUT] = ACTIONS(188),
    [anon_sym_OUTPUT] = ACTIONS(188),
    [anon_sym_I_DASHO] = ACTIONS(188),
    [anon_sym_EXTEND] = ACTIONS(188),
    [anon_sym_ACCEPT] = ACTIONS(188),
    [anon_sym_FROM] = ACTIONS(188),
    [anon_sym_DATE] = ACTIONS(188),
    [anon_sym_DAY] = ACTIONS(188),
    [anon_sym_TIME] = ACTIONS(188),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(188),
    [anon_sym_EQUAL] = ACTIONS(188),
    [anon_sym_GREATER] = ACTIONS(188),
    [anon_sym_LESS] = ACTIONS(188),
    [anon_sym_THAN] = ACTIONS(188),
    [anon_sym_OR] = ACTIONS(188),
    [anon_sym_AND] = ACTIONS(188),
    [anon_sym_DFHENTER] = ACTIONS(188),
    [anon_sym_DFHCLEAR] = ACTIONS(188),
    [anon_sym_DFHPA1] = ACTIONS(188),
    [anon_sym_DFHPA2] = ACTIONS(188),
    [anon_sym_DFHPF1] = ACTIONS(188),
    [anon_sym_DFHPF2] = ACTIONS(188),
    [anon_sym_DFHPF3] = ACTIONS(188),
    [anon_sym_DFHPF4] = ACTIONS(188),
    [anon_sym_DFHPF5] = ACTIONS(188),
    [anon_sym_DFHPF6] = ACTIONS(188),
    [anon_sym_DFHPF7] = ACTIONS(188),
    [anon_sym_DFHPF8] = ACTIONS(188),
    [anon_sym_DFHPF9] = ACTIONS(188),
    [anon_sym_DFHPF10] = ACTIONS(188),
    [anon_sym_DFHPF11] = ACTIONS(188),
    [anon_sym_DFHPF12] = ACTIONS(188),
    [anon_sym_EIBAID] = ACTIONS(188),
    [anon_sym_DFHRED] = ACTIONS(188),
    [anon_sym_DFHBMASB] = ACTIONS(188),
    [anon_sym_DFHBMASK] = ACTIONS(188),
    [aux_sym_identifier_token1] = ACTIONS(188),
    [aux_sym_identifier_token2] = ACTIONS(186),
    [sym_picture_string] = ACTIONS(188),
    [aux_sym_string_literal_token1] = ACTIONS(186),
    [aux_sym_string_literal_token2] = ACTIONS(186),
    [sym_number] = ACTIONS(188),
    [anon_sym_EQ_EQ] = ACTIONS(186),
    [anon_sym_EQ] = ACTIONS(188),
    [anon_sym_GT] = ACTIONS(188),
    [anon_sym_LT] = ACTIONS(188),
    [anon_sym_GT_EQ] = ACTIONS(186),
    [anon_sym_LT_EQ] = ACTIONS(186),
    [anon_sym_COMMA] = ACTIONS(188),
    [anon_sym_LPAREN] = ACTIONS(188),
    [anon_sym_RPAREN] = ACTIONS(186),
    [anon_sym_COLON] = ACTIONS(186),
  },
  [21] = {
    [aux_sym_newline_token1] = ACTIONS(190),
    [anon_sym_DOT] = ACTIONS(190),
    [anon_sym_88] = ACTIONS(192),
    [anon_sym_VALUE] = ACTIONS(192),
    [anon_sym_IS] = ACTIONS(192),
    [aux_sym_level_number_token1] = ACTIONS(192),
    [aux_sym_level_number_token2] = ACTIONS(192),
    [anon_sym_66] = ACTIONS(192),
    [anon_sym_77] = ACTIONS(192),
    [anon_sym_FILLER] = ACTIONS(192),
    [anon_sym_PIC] = ACTIONS(192),
    [anon_sym_PICTURE] = ACTIONS(192),
    [anon_sym_VALUES] = ACTIONS(192),
    [anon_sym_OCCURS] = ACTIONS(192),
    [anon_sym_TIMES] = ACTIONS(192),
    [anon_sym_TO] = ACTIONS(192),
    [anon_sym_REDEFINES] = ACTIONS(192),
    [anon_sym_INDEXED] = ACTIONS(192),
    [anon_sym_BY] = ACTIONS(192),
    [anon_sym_DEPENDING] = ACTIONS(192),
    [anon_sym_ON] = ACTIONS(192),
    [anon_sym_USAGE] = ACTIONS(192),
    [anon_sym_DISPLAY] = ACTIONS(192),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(192),
    [anon_sym_BINARY] = ACTIONS(192),
    [anon_sym_COMP] = ACTIONS(192),
    [anon_sym_COMP_DASH1] = ACTIONS(192),
    [anon_sym_COMP_DASH2] = ACTIONS(192),
    [anon_sym_COMP_DASH3] = ACTIONS(192),
    [anon_sym_COMP_DASH4] = ACTIONS(192),
    [anon_sym_COMP_DASH5] = ACTIONS(192),
    [anon_sym_COMPUTATIONAL] = ACTIONS(192),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(192),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(192),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(192),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(192),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(192),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(192),
    [anon_sym_INDEX] = ACTIONS(192),
    [anon_sym_POINTER] = ACTIONS(192),
    [anon_sym_ZERO] = ACTIONS(192),
    [anon_sym_ZEROS] = ACTIONS(192),
    [anon_sym_ZEROES] = ACTIONS(192),
    [anon_sym_SPACE] = ACTIONS(192),
    [anon_sym_SPACES] = ACTIONS(192),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(192),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(192),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(192),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(192),
    [anon_sym_QUOTE] = ACTIONS(192),
    [anon_sym_QUOTES] = ACTIONS(192),
    [anon_sym_NULL] = ACTIONS(192),
    [anon_sym_NULLS] = ACTIONS(192),
    [anon_sym_ALL] = ACTIONS(192),
    [anon_sym_THRU] = ACTIONS(192),
    [anon_sym_THROUGH] = ACTIONS(192),
    [anon_sym_ASCENDING] = ACTIONS(192),
    [anon_sym_DESCENDING] = ACTIONS(192),
    [anon_sym_KEY] = ACTIONS(192),
    [anon_sym_SIGN] = ACTIONS(192),
    [anon_sym_LEADING] = ACTIONS(192),
    [anon_sym_TRAILING] = ACTIONS(192),
    [anon_sym_SEPARATE] = ACTIONS(192),
    [anon_sym_CHARACTER] = ACTIONS(192),
    [anon_sym_SYNC] = ACTIONS(192),
    [anon_sym_SYNCHRONIZED] = ACTIONS(192),
    [anon_sym_LEFT] = ACTIONS(192),
    [anon_sym_RIGHT] = ACTIONS(192),
    [anon_sym_JUST] = ACTIONS(192),
    [anon_sym_JUSTIFIED] = ACTIONS(192),
    [anon_sym_BLANK] = ACTIONS(192),
    [anon_sym_WHEN] = ACTIONS(192),
    [anon_sym_EXTERNAL] = ACTIONS(192),
    [anon_sym_GLOBAL] = ACTIONS(192),
    [anon_sym_AS] = ACTIONS(192),
    [anon_sym_COPY] = ACTIONS(192),
    [anon_sym_REPLACING] = ACTIONS(192),
    [anon_sym_OF] = ACTIONS(192),
    [anon_sym_IN] = ACTIONS(192),
    [anon_sym_REPLACE] = ACTIONS(192),
    [anon_sym_OFF] = ACTIONS(192),
    [anon_sym_EJECT] = ACTIONS(192),
    [anon_sym_SKIP1] = ACTIONS(192),
    [anon_sym_SKIP2] = ACTIONS(192),
    [anon_sym_SKIP3] = ACTIONS(192),
    [anon_sym_EXEC] = ACTIONS(192),
    [anon_sym_EXECUTE] = ACTIONS(192),
    [anon_sym_SQL] = ACTIONS(192),
    [anon_sym_SQLIMS] = ACTIONS(192),
    [anon_sym_DLI] = ACTIONS(192),
    [anon_sym_END_DASHEXEC] = ACTIONS(192),
    [anon_sym_IF] = ACTIONS(192),
    [anon_sym_ELSE] = ACTIONS(192),
    [anon_sym_END_DASHIF] = ACTIONS(192),
    [anon_sym_THEN] = ACTIONS(192),
    [anon_sym_EVALUATE] = ACTIONS(192),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(192),
    [anon_sym_OTHER] = ACTIONS(192),
    [anon_sym_ALSO] = ACTIONS(192),
    [anon_sym_PERFORM] = ACTIONS(192),
    [anon_sym_END_DASHPERFORM] = ACTIONS(192),
    [anon_sym_UNTIL] = ACTIONS(192),
    [anon_sym_VARYING] = ACTIONS(192),
    [anon_sym_WITH] = ACTIONS(192),
    [anon_sym_TEST] = ACTIONS(192),
    [anon_sym_BEFORE] = ACTIONS(192),
    [anon_sym_AFTER] = ACTIONS(192),
    [anon_sym_GO] = ACTIONS(192),
    [anon_sym_SECTION] = ACTIONS(192),
    [anon_sym_PARAGRAPH] = ACTIONS(192),
    [anon_sym_CONTINUE] = ACTIONS(192),
    [anon_sym_NEXT] = ACTIONS(192),
    [anon_sym_SENTENCE] = ACTIONS(192),
    [anon_sym_EXIT] = ACTIONS(192),
    [anon_sym_STOP] = ACTIONS(192),
    [anon_sym_RUN] = ACTIONS(192),
    [anon_sym_MOVE] = ACTIONS(192),
    [anon_sym_CORRESPONDING] = ACTIONS(192),
    [anon_sym_CORR] = ACTIONS(192),
    [anon_sym_INTO] = ACTIONS(192),
    [anon_sym_SET] = ACTIONS(192),
    [anon_sym_TRUE] = ACTIONS(192),
    [anon_sym_FALSE] = ACTIONS(192),
    [anon_sym_INITIALIZE] = ACTIONS(192),
    [anon_sym_ALPHABETIC] = ACTIONS(192),
    [anon_sym_ALPHANUMERIC] = ACTIONS(192),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(192),
    [anon_sym_NUMERIC] = ACTIONS(192),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(192),
    [anon_sym_COMPUTE] = ACTIONS(192),
    [anon_sym_ADD] = ACTIONS(192),
    [anon_sym_SUBTRACT] = ACTIONS(192),
    [anon_sym_MULTIPLY] = ACTIONS(192),
    [anon_sym_DIVIDE] = ACTIONS(192),
    [anon_sym_GIVING] = ACTIONS(192),
    [anon_sym_REMAINDER] = ACTIONS(192),
    [anon_sym_STRING] = ACTIONS(192),
    [anon_sym_DELIMITED] = ACTIONS(192),
    [anon_sym_SIZE] = ACTIONS(192),
    [anon_sym_OVERFLOW] = ACTIONS(192),
    [anon_sym_NOT] = ACTIONS(192),
    [anon_sym_END_DASHSTRING] = ACTIONS(192),
    [anon_sym_UNSTRING] = ACTIONS(192),
    [anon_sym_COUNT] = ACTIONS(192),
    [anon_sym_DELIMITER] = ACTIONS(192),
    [anon_sym_TALLYING] = ACTIONS(192),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(192),
    [anon_sym_INSPECT] = ACTIONS(192),
    [anon_sym_CONVERTING] = ACTIONS(192),
    [anon_sym_FIRST] = ACTIONS(192),
    [anon_sym_INITIAL] = ACTIONS(192),
    [anon_sym_READ] = ACTIONS(192),
    [anon_sym_WRITE] = ACTIONS(192),
    [anon_sym_REWRITE] = ACTIONS(192),
    [anon_sym_DELETE] = ACTIONS(192),
    [anon_sym_START] = ACTIONS(192),
    [anon_sym_OPEN] = ACTIONS(192),
    [anon_sym_CLOSE] = ACTIONS(192),
    [anon_sym_INPUT] = ACTIONS(192),
    [anon_sym_OUTPUT] = ACTIONS(192),
    [anon_sym_I_DASHO] = ACTIONS(192),
    [anon_sym_EXTEND] = ACTIONS(192),
    [anon_sym_ACCEPT] = ACTIONS(192),
    [anon_sym_FROM] = ACTIONS(192),
    [anon_sym_DATE] = ACTIONS(192),
    [anon_sym_DAY] = ACTIONS(192),
    [anon_sym_TIME] = ACTIONS(192),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(192),
    [anon_sym_EQUAL] = ACTIONS(192),
    [anon_sym_GREATER] = ACTIONS(192),
    [anon_sym_LESS] = ACTIONS(192),
    [anon_sym_THAN] = ACTIONS(192),
    [anon_sym_OR] = ACTIONS(192),
    [anon_sym_AND] = ACTIONS(192),
    [anon_sym_DFHENTER] = ACTIONS(192),
    [anon_sym_DFHCLEAR] = ACTIONS(192),
    [anon_sym_DFHPA1] = ACTIONS(192),
    [anon_sym_DFHPA2] = ACTIONS(192),
    [anon_sym_DFHPF1] = ACTIONS(192),
    [anon_sym_DFHPF2] = ACTIONS(192),
    [anon_sym_DFHPF3] = ACTIONS(192),
    [anon_sym_DFHPF4] = ACTIONS(192),
    [anon_sym_DFHPF5] = ACTIONS(192),
    [anon_sym_DFHPF6] = ACTIONS(192),
    [anon_sym_DFHPF7] = ACTIONS(192),
    [anon_sym_DFHPF8] = ACTIONS(192),
    [anon_sym_DFHPF9] = ACTIONS(192),
    [anon_sym_DFHPF10] = ACTIONS(192),
    [anon_sym_DFHPF11] = ACTIONS(192),
    [anon_sym_DFHPF12] = ACTIONS(192),
    [anon_sym_EIBAID] = ACTIONS(192),
    [anon_sym_DFHRED] = ACTIONS(192),
    [anon_sym_DFHBMASB] = ACTIONS(192),
    [anon_sym_DFHBMASK] = ACTIONS(192),
    [aux_sym_identifier_token1] = ACTIONS(192),
    [aux_sym_identifier_token2] = ACTIONS(190),
    [sym_picture_string] = ACTIONS(192),
    [aux_sym_string_literal_token1] = ACTIONS(190),
    [aux_sym_string_literal_token2] = ACTIONS(190),
    [sym_number] = ACTIONS(192),
    [anon_sym_EQ_EQ] = ACTIONS(190),
    [anon_sym_EQ] = ACTIONS(192),
    [anon_sym_GT] = ACTIONS(192),
    [anon_sym_LT] = ACTIONS(192),
    [anon_sym_GT_EQ] = ACTIONS(190),
    [anon_sym_LT_EQ] = ACTIONS(190),
    [anon_sym_COMMA] = ACTIONS(192),
    [anon_sym_LPAREN] = ACTIONS(192),
    [anon_sym_RPAREN] = ACTIONS(190),
    [anon_sym_COLON] = ACTIONS(190),
  },
  [22] = {
    [aux_sym_newline_token1] = ACTIONS(194),
    [anon_sym_DOT] = ACTIONS(194),
    [anon_sym_88] = ACTIONS(196),
    [anon_sym_VALUE] = ACTIONS(196),
    [anon_sym_IS] = ACTIONS(196),
    [aux_sym_level_number_token1] = ACTIONS(196),
    [aux_sym_level_number_token2] = ACTIONS(196),
    [anon_sym_66] = ACTIONS(196),
    [anon_sym_77] = ACTIONS(196),
    [anon_sym_FILLER] = ACTIONS(196),
    [anon_sym_PIC] = ACTIONS(196),
    [anon_sym_PICTURE] = ACTIONS(196),
    [anon_sym_VALUES] = ACTIONS(196),
    [anon_sym_OCCURS] = ACTIONS(196),
    [anon_sym_TIMES] = ACTIONS(196),
    [anon_sym_TO] = ACTIONS(196),
    [anon_sym_REDEFINES] = ACTIONS(196),
    [anon_sym_INDEXED] = ACTIONS(196),
    [anon_sym_BY] = ACTIONS(196),
    [anon_sym_DEPENDING] = ACTIONS(196),
    [anon_sym_ON] = ACTIONS(196),
    [anon_sym_USAGE] = ACTIONS(196),
    [anon_sym_DISPLAY] = ACTIONS(196),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(196),
    [anon_sym_BINARY] = ACTIONS(196),
    [anon_sym_COMP] = ACTIONS(196),
    [anon_sym_COMP_DASH1] = ACTIONS(196),
    [anon_sym_COMP_DASH2] = ACTIONS(196),
    [anon_sym_COMP_DASH3] = ACTIONS(196),
    [anon_sym_COMP_DASH4] = ACTIONS(196),
    [anon_sym_COMP_DASH5] = ACTIONS(196),
    [anon_sym_COMPUTATIONAL] = ACTIONS(196),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(196),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(196),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(196),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(196),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(196),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(196),
    [anon_sym_INDEX] = ACTIONS(196),
    [anon_sym_POINTER] = ACTIONS(196),
    [anon_sym_ZERO] = ACTIONS(196),
    [anon_sym_ZEROS] = ACTIONS(196),
    [anon_sym_ZEROES] = ACTIONS(196),
    [anon_sym_SPACE] = ACTIONS(196),
    [anon_sym_SPACES] = ACTIONS(196),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(196),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(196),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(196),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(196),
    [anon_sym_QUOTE] = ACTIONS(196),
    [anon_sym_QUOTES] = ACTIONS(196),
    [anon_sym_NULL] = ACTIONS(196),
    [anon_sym_NULLS] = ACTIONS(196),
    [anon_sym_ALL] = ACTIONS(196),
    [anon_sym_THRU] = ACTIONS(196),
    [anon_sym_THROUGH] = ACTIONS(196),
    [anon_sym_ASCENDING] = ACTIONS(196),
    [anon_sym_DESCENDING] = ACTIONS(196),
    [anon_sym_KEY] = ACTIONS(196),
    [anon_sym_SIGN] = ACTIONS(196),
    [anon_sym_LEADING] = ACTIONS(196),
    [anon_sym_TRAILING] = ACTIONS(196),
    [anon_sym_SEPARATE] = ACTIONS(196),
    [anon_sym_CHARACTER] = ACTIONS(196),
    [anon_sym_SYNC] = ACTIONS(196),
    [anon_sym_SYNCHRONIZED] = ACTIONS(196),
    [anon_sym_LEFT] = ACTIONS(196),
    [anon_sym_RIGHT] = ACTIONS(196),
    [anon_sym_JUST] = ACTIONS(196),
    [anon_sym_JUSTIFIED] = ACTIONS(196),
    [anon_sym_BLANK] = ACTIONS(196),
    [anon_sym_WHEN] = ACTIONS(196),
    [anon_sym_EXTERNAL] = ACTIONS(196),
    [anon_sym_GLOBAL] = ACTIONS(196),
    [anon_sym_AS] = ACTIONS(196),
    [anon_sym_COPY] = ACTIONS(196),
    [anon_sym_REPLACING] = ACTIONS(196),
    [anon_sym_OF] = ACTIONS(196),
    [anon_sym_IN] = ACTIONS(196),
    [anon_sym_REPLACE] = ACTIONS(196),
    [anon_sym_OFF] = ACTIONS(196),
    [anon_sym_EJECT] = ACTIONS(196),
    [anon_sym_SKIP1] = ACTIONS(196),
    [anon_sym_SKIP2] = ACTIONS(196),
    [anon_sym_SKIP3] = ACTIONS(196),
    [anon_sym_EXEC] = ACTIONS(196),
    [anon_sym_EXECUTE] = ACTIONS(196),
    [anon_sym_SQL] = ACTIONS(196),
    [anon_sym_SQLIMS] = ACTIONS(196),
    [anon_sym_DLI] = ACTIONS(196),
    [anon_sym_END_DASHEXEC] = ACTIONS(196),
    [anon_sym_IF] = ACTIONS(196),
    [anon_sym_ELSE] = ACTIONS(196),
    [anon_sym_END_DASHIF] = ACTIONS(196),
    [anon_sym_THEN] = ACTIONS(196),
    [anon_sym_EVALUATE] = ACTIONS(196),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(196),
    [anon_sym_OTHER] = ACTIONS(196),
    [anon_sym_ALSO] = ACTIONS(196),
    [anon_sym_PERFORM] = ACTIONS(196),
    [anon_sym_END_DASHPERFORM] = ACTIONS(196),
    [anon_sym_UNTIL] = ACTIONS(196),
    [anon_sym_VARYING] = ACTIONS(196),
    [anon_sym_WITH] = ACTIONS(196),
    [anon_sym_TEST] = ACTIONS(196),
    [anon_sym_BEFORE] = ACTIONS(196),
    [anon_sym_AFTER] = ACTIONS(196),
    [anon_sym_GO] = ACTIONS(196),
    [anon_sym_SECTION] = ACTIONS(196),
    [anon_sym_PARAGRAPH] = ACTIONS(196),
    [anon_sym_CONTINUE] = ACTIONS(196),
    [anon_sym_NEXT] = ACTIONS(196),
    [anon_sym_SENTENCE] = ACTIONS(196),
    [anon_sym_EXIT] = ACTIONS(196),
    [anon_sym_STOP] = ACTIONS(196),
    [anon_sym_RUN] = ACTIONS(196),
    [anon_sym_MOVE] = ACTIONS(196),
    [anon_sym_CORRESPONDING] = ACTIONS(196),
    [anon_sym_CORR] = ACTIONS(196),
    [anon_sym_INTO] = ACTIONS(196),
    [anon_sym_SET] = ACTIONS(196),
    [anon_sym_TRUE] = ACTIONS(196),
    [anon_sym_FALSE] = ACTIONS(196),
    [anon_sym_INITIALIZE] = ACTIONS(196),
    [anon_sym_ALPHABETIC] = ACTIONS(196),
    [anon_sym_ALPHANUMERIC] = ACTIONS(196),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(196),
    [anon_sym_NUMERIC] = ACTIONS(196),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(196),
    [anon_sym_COMPUTE] = ACTIONS(196),
    [anon_sym_ADD] = ACTIONS(196),
    [anon_sym_SUBTRACT] = ACTIONS(196),
    [anon_sym_MULTIPLY] = ACTIONS(196),
    [anon_sym_DIVIDE] = ACTIONS(196),
    [anon_sym_GIVING] = ACTIONS(196),
    [anon_sym_REMAINDER] = ACTIONS(196),
    [anon_sym_STRING] = ACTIONS(196),
    [anon_sym_DELIMITED] = ACTIONS(196),
    [anon_sym_SIZE] = ACTIONS(196),
    [anon_sym_OVERFLOW] = ACTIONS(196),
    [anon_sym_NOT] = ACTIONS(196),
    [anon_sym_END_DASHSTRING] = ACTIONS(196),
    [anon_sym_UNSTRING] = ACTIONS(196),
    [anon_sym_COUNT] = ACTIONS(196),
    [anon_sym_DELIMITER] = ACTIONS(196),
    [anon_sym_TALLYING] = ACTIONS(196),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(196),
    [anon_sym_INSPECT] = ACTIONS(196),
    [anon_sym_CONVERTING] = ACTIONS(196),
    [anon_sym_FIRST] = ACTIONS(196),
    [anon_sym_INITIAL] = ACTIONS(196),
    [anon_sym_READ] = ACTIONS(196),
    [anon_sym_WRITE] = ACTIONS(196),
    [anon_sym_REWRITE] = ACTIONS(196),
    [anon_sym_DELETE] = ACTIONS(196),
    [anon_sym_START] = ACTIONS(196),
    [anon_sym_OPEN] = ACTIONS(196),
    [anon_sym_CLOSE] = ACTIONS(196),
    [anon_sym_INPUT] = ACTIONS(196),
    [anon_sym_OUTPUT] = ACTIONS(196),
    [anon_sym_I_DASHO] = ACTIONS(196),
    [anon_sym_EXTEND] = ACTIONS(196),
    [anon_sym_ACCEPT] = ACTIONS(196),
    [anon_sym_FROM] = ACTIONS(196),
    [anon_sym_DATE] = ACTIONS(196),
    [anon_sym_DAY] = ACTIONS(196),
    [anon_sym_TIME] = ACTIONS(196),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(196),
    [anon_sym_EQUAL] = ACTIONS(196),
    [anon_sym_GREATER] = ACTIONS(196),
    [anon_sym_LESS] = ACTIONS(196),
    [anon_sym_THAN] = ACTIONS(196),
    [anon_sym_OR] = ACTIONS(196),
    [anon_sym_AND] = ACTIONS(196),
    [anon_sym_DFHENTER] = ACTIONS(196),
    [anon_sym_DFHCLEAR] = ACTIONS(196),
    [anon_sym_DFHPA1] = ACTIONS(196),
    [anon_sym_DFHPA2] = ACTIONS(196),
    [anon_sym_DFHPF1] = ACTIONS(196),
    [anon_sym_DFHPF2] = ACTIONS(196),
    [anon_sym_DFHPF3] = ACTIONS(196),
    [anon_sym_DFHPF4] = ACTIONS(196),
    [anon_sym_DFHPF5] = ACTIONS(196),
    [anon_sym_DFHPF6] = ACTIONS(196),
    [anon_sym_DFHPF7] = ACTIONS(196),
    [anon_sym_DFHPF8] = ACTIONS(196),
    [anon_sym_DFHPF9] = ACTIONS(196),
    [anon_sym_DFHPF10] = ACTIONS(196),
    [anon_sym_DFHPF11] = ACTIONS(196),
    [anon_sym_DFHPF12] = ACTIONS(196),
    [anon_sym_EIBAID] = ACTIONS(196),
    [anon_sym_DFHRED] = ACTIONS(196),
    [anon_sym_DFHBMASB] = ACTIONS(196),
    [anon_sym_DFHBMASK] = ACTIONS(196),
    [aux_sym_identifier_token1] = ACTIONS(196),
    [aux_sym_identifier_token2] = ACTIONS(194),
    [sym_picture_string] = ACTIONS(196),
    [aux_sym_string_literal_token1] = ACTIONS(194),
    [aux_sym_string_literal_token2] = ACTIONS(194),
    [sym_number] = ACTIONS(196),
    [anon_sym_EQ_EQ] = ACTIONS(194),
    [anon_sym_EQ] = ACTIONS(196),
    [anon_sym_GT] = ACTIONS(196),
    [anon_sym_LT] = ACTIONS(196),
    [anon_sym_GT_EQ] = ACTIONS(194),
    [anon_sym_LT_EQ] = ACTIONS(194),
    [anon_sym_COMMA] = ACTIONS(196),
    [anon_sym_LPAREN] = ACTIONS(196),
    [anon_sym_RPAREN] = ACTIONS(194),
    [anon_sym_COLON] = ACTIONS(194),
  },
  [23] = {
    [aux_sym_newline_token1] = ACTIONS(198),
    [anon_sym_DOT] = ACTIONS(198),
    [anon_sym_88] = ACTIONS(200),
    [anon_sym_VALUE] = ACTIONS(200),
    [anon_sym_IS] = ACTIONS(200),
    [aux_sym_level_number_token1] = ACTIONS(200),
    [aux_sym_level_number_token2] = ACTIONS(200),
    [anon_sym_66] = ACTIONS(200),
    [anon_sym_77] = ACTIONS(200),
    [anon_sym_FILLER] = ACTIONS(200),
    [anon_sym_PIC] = ACTIONS(200),
    [anon_sym_PICTURE] = ACTIONS(200),
    [anon_sym_VALUES] = ACTIONS(200),
    [anon_sym_OCCURS] = ACTIONS(200),
    [anon_sym_TIMES] = ACTIONS(200),
    [anon_sym_TO] = ACTIONS(200),
    [anon_sym_REDEFINES] = ACTIONS(200),
    [anon_sym_INDEXED] = ACTIONS(200),
    [anon_sym_BY] = ACTIONS(200),
    [anon_sym_DEPENDING] = ACTIONS(200),
    [anon_sym_ON] = ACTIONS(200),
    [anon_sym_USAGE] = ACTIONS(200),
    [anon_sym_DISPLAY] = ACTIONS(200),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(200),
    [anon_sym_BINARY] = ACTIONS(200),
    [anon_sym_COMP] = ACTIONS(200),
    [anon_sym_COMP_DASH1] = ACTIONS(200),
    [anon_sym_COMP_DASH2] = ACTIONS(200),
    [anon_sym_COMP_DASH3] = ACTIONS(200),
    [anon_sym_COMP_DASH4] = ACTIONS(200),
    [anon_sym_COMP_DASH5] = ACTIONS(200),
    [anon_sym_COMPUTATIONAL] = ACTIONS(200),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(200),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(200),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(200),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(200),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(200),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(200),
    [anon_sym_INDEX] = ACTIONS(200),
    [anon_sym_POINTER] = ACTIONS(200),
    [anon_sym_ZERO] = ACTIONS(200),
    [anon_sym_ZEROS] = ACTIONS(200),
    [anon_sym_ZEROES] = ACTIONS(200),
    [anon_sym_SPACE] = ACTIONS(200),
    [anon_sym_SPACES] = ACTIONS(200),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(200),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(200),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(200),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(200),
    [anon_sym_QUOTE] = ACTIONS(200),
    [anon_sym_QUOTES] = ACTIONS(200),
    [anon_sym_NULL] = ACTIONS(200),
    [anon_sym_NULLS] = ACTIONS(200),
    [anon_sym_ALL] = ACTIONS(200),
    [anon_sym_THRU] = ACTIONS(200),
    [anon_sym_THROUGH] = ACTIONS(200),
    [anon_sym_ASCENDING] = ACTIONS(200),
    [anon_sym_DESCENDING] = ACTIONS(200),
    [anon_sym_KEY] = ACTIONS(200),
    [anon_sym_SIGN] = ACTIONS(200),
    [anon_sym_LEADING] = ACTIONS(200),
    [anon_sym_TRAILING] = ACTIONS(200),
    [anon_sym_SEPARATE] = ACTIONS(200),
    [anon_sym_CHARACTER] = ACTIONS(200),
    [anon_sym_SYNC] = ACTIONS(200),
    [anon_sym_SYNCHRONIZED] = ACTIONS(200),
    [anon_sym_LEFT] = ACTIONS(200),
    [anon_sym_RIGHT] = ACTIONS(200),
    [anon_sym_JUST] = ACTIONS(200),
    [anon_sym_JUSTIFIED] = ACTIONS(200),
    [anon_sym_BLANK] = ACTIONS(200),
    [anon_sym_WHEN] = ACTIONS(200),
    [anon_sym_EXTERNAL] = ACTIONS(200),
    [anon_sym_GLOBAL] = ACTIONS(200),
    [anon_sym_AS] = ACTIONS(200),
    [anon_sym_COPY] = ACTIONS(200),
    [anon_sym_REPLACING] = ACTIONS(200),
    [anon_sym_OF] = ACTIONS(200),
    [anon_sym_IN] = ACTIONS(200),
    [anon_sym_REPLACE] = ACTIONS(200),
    [anon_sym_OFF] = ACTIONS(200),
    [anon_sym_EJECT] = ACTIONS(200),
    [anon_sym_SKIP1] = ACTIONS(200),
    [anon_sym_SKIP2] = ACTIONS(200),
    [anon_sym_SKIP3] = ACTIONS(200),
    [anon_sym_EXEC] = ACTIONS(200),
    [anon_sym_EXECUTE] = ACTIONS(200),
    [anon_sym_SQL] = ACTIONS(200),
    [anon_sym_SQLIMS] = ACTIONS(200),
    [anon_sym_DLI] = ACTIONS(200),
    [anon_sym_END_DASHEXEC] = ACTIONS(200),
    [anon_sym_IF] = ACTIONS(200),
    [anon_sym_ELSE] = ACTIONS(200),
    [anon_sym_END_DASHIF] = ACTIONS(200),
    [anon_sym_THEN] = ACTIONS(200),
    [anon_sym_EVALUATE] = ACTIONS(200),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(200),
    [anon_sym_OTHER] = ACTIONS(200),
    [anon_sym_ALSO] = ACTIONS(200),
    [anon_sym_PERFORM] = ACTIONS(200),
    [anon_sym_END_DASHPERFORM] = ACTIONS(200),
    [anon_sym_UNTIL] = ACTIONS(200),
    [anon_sym_VARYING] = ACTIONS(200),
    [anon_sym_WITH] = ACTIONS(200),
    [anon_sym_TEST] = ACTIONS(200),
    [anon_sym_BEFORE] = ACTIONS(200),
    [anon_sym_AFTER] = ACTIONS(200),
    [anon_sym_GO] = ACTIONS(200),
    [anon_sym_SECTION] = ACTIONS(200),
    [anon_sym_PARAGRAPH] = ACTIONS(200),
    [anon_sym_CONTINUE] = ACTIONS(200),
    [anon_sym_NEXT] = ACTIONS(200),
    [anon_sym_SENTENCE] = ACTIONS(200),
    [anon_sym_EXIT] = ACTIONS(200),
    [anon_sym_STOP] = ACTIONS(200),
    [anon_sym_RUN] = ACTIONS(200),
    [anon_sym_MOVE] = ACTIONS(200),
    [anon_sym_CORRESPONDING] = ACTIONS(200),
    [anon_sym_CORR] = ACTIONS(200),
    [anon_sym_INTO] = ACTIONS(200),
    [anon_sym_SET] = ACTIONS(200),
    [anon_sym_TRUE] = ACTIONS(200),
    [anon_sym_FALSE] = ACTIONS(200),
    [anon_sym_INITIALIZE] = ACTIONS(200),
    [anon_sym_ALPHABETIC] = ACTIONS(200),
    [anon_sym_ALPHANUMERIC] = ACTIONS(200),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(200),
    [anon_sym_NUMERIC] = ACTIONS(200),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(200),
    [anon_sym_COMPUTE] = ACTIONS(200),
    [anon_sym_ADD] = ACTIONS(200),
    [anon_sym_SUBTRACT] = ACTIONS(200),
    [anon_sym_MULTIPLY] = ACTIONS(200),
    [anon_sym_DIVIDE] = ACTIONS(200),
    [anon_sym_GIVING] = ACTIONS(200),
    [anon_sym_REMAINDER] = ACTIONS(200),
    [anon_sym_STRING] = ACTIONS(200),
    [anon_sym_DELIMITED] = ACTIONS(200),
    [anon_sym_SIZE] = ACTIONS(200),
    [anon_sym_OVERFLOW] = ACTIONS(200),
    [anon_sym_NOT] = ACTIONS(200),
    [anon_sym_END_DASHSTRING] = ACTIONS(200),
    [anon_sym_UNSTRING] = ACTIONS(200),
    [anon_sym_COUNT] = ACTIONS(200),
    [anon_sym_DELIMITER] = ACTIONS(200),
    [anon_sym_TALLYING] = ACTIONS(200),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(200),
    [anon_sym_INSPECT] = ACTIONS(200),
    [anon_sym_CONVERTING] = ACTIONS(200),
    [anon_sym_FIRST] = ACTIONS(200),
    [anon_sym_INITIAL] = ACTIONS(200),
    [anon_sym_READ] = ACTIONS(200),
    [anon_sym_WRITE] = ACTIONS(200),
    [anon_sym_REWRITE] = ACTIONS(200),
    [anon_sym_DELETE] = ACTIONS(200),
    [anon_sym_START] = ACTIONS(200),
    [anon_sym_OPEN] = ACTIONS(200),
    [anon_sym_CLOSE] = ACTIONS(200),
    [anon_sym_INPUT] = ACTIONS(200),
    [anon_sym_OUTPUT] = ACTIONS(200),
    [anon_sym_I_DASHO] = ACTIONS(200),
    [anon_sym_EXTEND] = ACTIONS(200),
    [anon_sym_ACCEPT] = ACTIONS(200),
    [anon_sym_FROM] = ACTIONS(200),
    [anon_sym_DATE] = ACTIONS(200),
    [anon_sym_DAY] = ACTIONS(200),
    [anon_sym_TIME] = ACTIONS(200),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(200),
    [anon_sym_EQUAL] = ACTIONS(200),
    [anon_sym_GREATER] = ACTIONS(200),
    [anon_sym_LESS] = ACTIONS(200),
    [anon_sym_THAN] = ACTIONS(200),
    [anon_sym_OR] = ACTIONS(200),
    [anon_sym_AND] = ACTIONS(200),
    [anon_sym_DFHENTER] = ACTIONS(200),
    [anon_sym_DFHCLEAR] = ACTIONS(200),
    [anon_sym_DFHPA1] = ACTIONS(200),
    [anon_sym_DFHPA2] = ACTIONS(200),
    [anon_sym_DFHPF1] = ACTIONS(200),
    [anon_sym_DFHPF2] = ACTIONS(200),
    [anon_sym_DFHPF3] = ACTIONS(200),
    [anon_sym_DFHPF4] = ACTIONS(200),
    [anon_sym_DFHPF5] = ACTIONS(200),
    [anon_sym_DFHPF6] = ACTIONS(200),
    [anon_sym_DFHPF7] = ACTIONS(200),
    [anon_sym_DFHPF8] = ACTIONS(200),
    [anon_sym_DFHPF9] = ACTIONS(200),
    [anon_sym_DFHPF10] = ACTIONS(200),
    [anon_sym_DFHPF11] = ACTIONS(200),
    [anon_sym_DFHPF12] = ACTIONS(200),
    [anon_sym_EIBAID] = ACTIONS(200),
    [anon_sym_DFHRED] = ACTIONS(200),
    [anon_sym_DFHBMASB] = ACTIONS(200),
    [anon_sym_DFHBMASK] = ACTIONS(200),
    [aux_sym_identifier_token1] = ACTIONS(200),
    [aux_sym_identifier_token2] = ACTIONS(198),
    [sym_picture_string] = ACTIONS(200),
    [aux_sym_string_literal_token1] = ACTIONS(198),
    [aux_sym_string_literal_token2] = ACTIONS(198),
    [sym_number] = ACTIONS(200),
    [anon_sym_EQ_EQ] = ACTIONS(198),
    [anon_sym_EQ] = ACTIONS(200),
    [anon_sym_GT] = ACTIONS(200),
    [anon_sym_LT] = ACTIONS(200),
    [anon_sym_GT_EQ] = ACTIONS(198),
    [anon_sym_LT_EQ] = ACTIONS(198),
    [anon_sym_COMMA] = ACTIONS(200),
    [anon_sym_LPAREN] = ACTIONS(200),
    [anon_sym_RPAREN] = ACTIONS(198),
    [anon_sym_COLON] = ACTIONS(198),
  },
  [24] = {
    [aux_sym_newline_token1] = ACTIONS(202),
    [anon_sym_DOT] = ACTIONS(202),
    [anon_sym_88] = ACTIONS(204),
    [anon_sym_VALUE] = ACTIONS(204),
    [anon_sym_IS] = ACTIONS(204),
    [aux_sym_level_number_token1] = ACTIONS(204),
    [aux_sym_level_number_token2] = ACTIONS(204),
    [anon_sym_66] = ACTIONS(204),
    [anon_sym_77] = ACTIONS(204),
    [anon_sym_FILLER] = ACTIONS(204),
    [anon_sym_PIC] = ACTIONS(204),
    [anon_sym_PICTURE] = ACTIONS(204),
    [anon_sym_VALUES] = ACTIONS(204),
    [anon_sym_OCCURS] = ACTIONS(204),
    [anon_sym_TIMES] = ACTIONS(204),
    [anon_sym_TO] = ACTIONS(204),
    [anon_sym_REDEFINES] = ACTIONS(204),
    [anon_sym_INDEXED] = ACTIONS(204),
    [anon_sym_BY] = ACTIONS(204),
    [anon_sym_DEPENDING] = ACTIONS(204),
    [anon_sym_ON] = ACTIONS(204),
    [anon_sym_USAGE] = ACTIONS(204),
    [anon_sym_DISPLAY] = ACTIONS(204),
    [anon_sym_DISPLAY_DASH1] = ACTIONS(204),
    [anon_sym_BINARY] = ACTIONS(204),
    [anon_sym_COMP] = ACTIONS(204),
    [anon_sym_COMP_DASH1] = ACTIONS(204),
    [anon_sym_COMP_DASH2] = ACTIONS(204),
    [anon_sym_COMP_DASH3] = ACTIONS(204),
    [anon_sym_COMP_DASH4] = ACTIONS(204),
    [anon_sym_COMP_DASH5] = ACTIONS(204),
    [anon_sym_COMPUTATIONAL] = ACTIONS(204),
    [anon_sym_COMPUTATIONAL_DASH1] = ACTIONS(204),
    [anon_sym_COMPUTATIONAL_DASH2] = ACTIONS(204),
    [anon_sym_COMPUTATIONAL_DASH3] = ACTIONS(204),
    [anon_sym_COMPUTATIONAL_DASH4] = ACTIONS(204),
    [anon_sym_COMPUTATIONAL_DASH5] = ACTIONS(204),
    [anon_sym_PACKED_DASHDECIMAL] = ACTIONS(204),
    [anon_sym_INDEX] = ACTIONS(204),
    [anon_sym_POINTER] = ACTIONS(204),
    [anon_sym_ZERO] = ACTIONS(204),
    [anon_sym_ZEROS] = ACTIONS(204),
    [anon_sym_ZEROES] = ACTIONS(204),
    [anon_sym_SPACE] = ACTIONS(204),
    [anon_sym_SPACES] = ACTIONS(204),
    [anon_sym_HIGH_DASHVALUE] = ACTIONS(204),
    [anon_sym_HIGH_DASHVALUES] = ACTIONS(204),
    [anon_sym_LOW_DASHVALUE] = ACTIONS(204),
    [anon_sym_LOW_DASHVALUES] = ACTIONS(204),
    [anon_sym_QUOTE] = ACTIONS(204),
    [anon_sym_QUOTES] = ACTIONS(204),
    [anon_sym_NULL] = ACTIONS(204),
    [anon_sym_NULLS] = ACTIONS(204),
    [anon_sym_ALL] = ACTIONS(204),
    [anon_sym_THRU] = ACTIONS(204),
    [anon_sym_THROUGH] = ACTIONS(204),
    [anon_sym_ASCENDING] = ACTIONS(204),
    [anon_sym_DESCENDING] = ACTIONS(204),
    [anon_sym_KEY] = ACTIONS(204),
    [anon_sym_SIGN] = ACTIONS(204),
    [anon_sym_LEADING] = ACTIONS(204),
    [anon_sym_TRAILING] = ACTIONS(204),
    [anon_sym_SEPARATE] = ACTIONS(204),
    [anon_sym_CHARACTER] = ACTIONS(204),
    [anon_sym_SYNC] = ACTIONS(204),
    [anon_sym_SYNCHRONIZED] = ACTIONS(204),
    [anon_sym_LEFT] = ACTIONS(204),
    [anon_sym_RIGHT] = ACTIONS(204),
    [anon_sym_JUST] = ACTIONS(204),
    [anon_sym_JUSTIFIED] = ACTIONS(204),
    [anon_sym_BLANK] = ACTIONS(204),
    [anon_sym_WHEN] = ACTIONS(204),
    [anon_sym_EXTERNAL] = ACTIONS(204),
    [anon_sym_GLOBAL] = ACTIONS(204),
    [anon_sym_AS] = ACTIONS(204),
    [anon_sym_COPY] = ACTIONS(204),
    [anon_sym_REPLACING] = ACTIONS(204),
    [anon_sym_OF] = ACTIONS(204),
    [anon_sym_IN] = ACTIONS(204),
    [anon_sym_REPLACE] = ACTIONS(204),
    [anon_sym_OFF] = ACTIONS(204),
    [anon_sym_EJECT] = ACTIONS(204),
    [anon_sym_SKIP1] = ACTIONS(204),
    [anon_sym_SKIP2] = ACTIONS(204),
    [anon_sym_SKIP3] = ACTIONS(204),
    [anon_sym_EXEC] = ACTIONS(204),
    [anon_sym_EXECUTE] = ACTIONS(204),
    [anon_sym_SQL] = ACTIONS(204),
    [anon_sym_SQLIMS] = ACTIONS(204),
    [anon_sym_DLI] = ACTIONS(204),
    [anon_sym_END_DASHEXEC] = ACTIONS(204),
    [anon_sym_IF] = ACTIONS(204),
    [anon_sym_ELSE] = ACTIONS(204),
    [anon_sym_END_DASHIF] = ACTIONS(204),
    [anon_sym_THEN] = ACTIONS(204),
    [anon_sym_EVALUATE] = ACTIONS(204),
    [anon_sym_END_DASHEVALUATE] = ACTIONS(204),
    [anon_sym_OTHER] = ACTIONS(204),
    [anon_sym_ALSO] = ACTIONS(204),
    [anon_sym_PERFORM] = ACTIONS(204),
    [anon_sym_END_DASHPERFORM] = ACTIONS(204),
    [anon_sym_UNTIL] = ACTIONS(204),
    [anon_sym_VARYING] = ACTIONS(204),
    [anon_sym_WITH] = ACTIONS(204),
    [anon_sym_TEST] = ACTIONS(204),
    [anon_sym_BEFORE] = ACTIONS(204),
    [anon_sym_AFTER] = ACTIONS(204),
    [anon_sym_GO] = ACTIONS(204),
    [anon_sym_SECTION] = ACTIONS(204),
    [anon_sym_PARAGRAPH] = ACTIONS(204),
    [anon_sym_CONTINUE] = ACTIONS(204),
    [anon_sym_NEXT] = ACTIONS(204),
    [anon_sym_SENTENCE] = ACTIONS(204),
    [anon_sym_EXIT] = ACTIONS(204),
    [anon_sym_STOP] = ACTIONS(204),
    [anon_sym_RUN] = ACTIONS(204),
    [anon_sym_MOVE] = ACTIONS(204),
    [anon_sym_CORRESPONDING] = ACTIONS(204),
    [anon_sym_CORR] = ACTIONS(204),
    [anon_sym_INTO] = ACTIONS(204),
    [anon_sym_SET] = ACTIONS(204),
    [anon_sym_TRUE] = ACTIONS(204),
    [anon_sym_FALSE] = ACTIONS(204),
    [anon_sym_INITIALIZE] = ACTIONS(204),
    [anon_sym_ALPHABETIC] = ACTIONS(204),
    [anon_sym_ALPHANUMERIC] = ACTIONS(204),
    [anon_sym_ALPHANUMERIC_DASHEDITED] = ACTIONS(204),
    [anon_sym_NUMERIC] = ACTIONS(204),
    [anon_sym_NUMERIC_DASHEDITED] = ACTIONS(204),
    [anon_sym_COMPUTE] = ACTIONS(204),
    [anon_sym_ADD] = ACTIONS(204),
    [anon_sym_SUBTRACT] = ACTIONS(204),
    [anon_sym_MULTIPLY] = ACTIONS(204),
    [anon_sym_DIVIDE] = ACTIONS(204),
    [anon_sym_GIVING] = ACTIONS(204),
    [anon_sym_REMAINDER] = ACTIONS(204),
    [anon_sym_STRING] = ACTIONS(204),
    [anon_sym_DELIMITED] = ACTIONS(204),
    [anon_sym_SIZE] = ACTIONS(204),
    [anon_sym_OVERFLOW] = ACTIONS(204),
    [anon_sym_NOT] = ACTIONS(204),
    [anon_sym_END_DASHSTRING] = ACTIONS(204),
    [anon_sym_UNSTRING] = ACTIONS(204),
    [anon_sym_COUNT] = ACTIONS(204),
    [anon_sym_DELIMITER] = ACTIONS(204),
    [anon_sym_TALLYING] = ACTIONS(204),
    [anon_sym_END_DASHUNSTRING] = ACTIONS(204),
    [anon_sym_INSPECT] = ACTIONS(204),
    [anon_sym_CONVERTING] = ACTIONS(204),
    [anon_sym_FIRST] = ACTIONS(204),
    [anon_sym_INITIAL] = ACTIONS(204),
    [anon_sym_READ] = ACTIONS(204),
    [anon_sym_WRITE] = ACTIONS(204),
    [anon_sym_REWRITE] = ACTIONS(204),
    [anon_sym_DELETE] = ACTIONS(204),
    [anon_sym_START] = ACTIONS(204),
    [anon_sym_OPEN] = ACTIONS(204),
    [anon_sym_CLOSE] = ACTIONS(204),
    [anon_sym_INPUT] = ACTIONS(204),
    [anon_sym_OUTPUT] = ACTIONS(204),
    [anon_sym_I_DASHO] = ACTIONS(204),
    [anon_sym_EXTEND] = ACTIONS(204),
    [anon_sym_ACCEPT] = ACTIONS(204),
    [anon_sym_FROM] = ACTIONS(204),
    [anon_sym_DATE] = ACTIONS(204),
    [anon_sym_DAY] = ACTIONS(204),
    [anon_sym_TIME] = ACTIONS(204),
    [anon_sym_DAY_DASHOF_DASHWEEK] = ACTIONS(204),
    [anon_sym_EQUAL] = ACTIONS(204),
    [anon_sym_GREATER] = ACTIONS(204),
    [anon_sym_LESS] = ACTIONS(204),
    [anon_sym_THAN] = ACTIONS(204),
    [anon_sym_OR] = ACTIONS(204),
    [anon_sym_AND] = ACTIONS(204),
    [anon_sym_DFHENTER] = ACTIONS(204),
    [anon_sym_DFHCLEAR] = ACTIONS(204),
    [anon_sym_DFHPA1] = ACTIONS(204),
    [anon_sym_DFHPA2] = ACTIONS(204),
    [anon_sym_DFHPF1] = ACTIONS(204),
    [anon_sym_DFHPF2] = ACTIONS(204),
    [anon_sym_DFHPF3] = ACTIONS(204),
    [anon_sym_DFHPF4] = ACTIONS(204),
    [anon_sym_DFHPF5] = ACTIONS(204),
    [anon_sym_DFHPF6] = ACTIONS(204),
    [anon_sym_DFHPF7] = ACTIONS(204),
    [anon_sym_DFHPF8] = ACTIONS(204),
    [anon_sym_DFHPF9] = ACTIONS(204),
    [anon_sym_DFHPF10] = ACTIONS(204),
    [anon_sym_DFHPF11] = ACTIONS(204),
    [anon_sym_DFHPF12] = ACTIONS(204),
    [anon_sym_EIBAID] = ACTIONS(204),
    [anon_sym_DFHRED] = ACTIONS(204),
    [anon_sym_DFHBMASB] = ACTIONS(204),
    [anon_sym_DFHBMASK] = ACTIONS(204),
    [aux_sym_identifier_token1] = ACTIONS(204),
    [aux_sym_identifier_token2] = ACTIONS(202),
    [sym_picture_string] = ACTIONS(204),
    [aux_sym_string_literal_token1] = ACTIONS(202),
    [aux_sym_string_literal_token2] = ACTIONS(202),
    [sym_number] = ACTIONS(204),
    [anon_sym_EQ_EQ] = ACTIONS(202),
    [anon_sym_EQ] = ACTIONS(204),
    [anon_sym_GT] = ACTIONS(204),
    [anon_sym_LT] = ACTIONS(204),
    [anon_sym_GT_EQ] = ACTIONS(202),
    [anon_sym_LT_EQ] = ACTIONS(202),
    [anon_sym_COMMA] = ACTIONS(204),
    [anon_sym_LPAREN] = ACTIONS(204),
    [anon_sym_RPAREN] = ACTIONS(202),
    [anon_sym_COLON] = ACTIONS(202),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 5,
    ACTIONS(215), 1,
      anon_sym_RPAREN,
    ACTIONS(206), 2,
      aux_sym_identifier_token1,
      aux_sym_identifier_token2,
    ACTIONS(209), 2,
      aux_sym_string_literal_token1,
      aux_sym_string_literal_token2,
    ACTIONS(212), 2,
      sym_number,
      anon_sym_COMMA,
    STATE(25), 3,
      sym_identifier,
      sym_string_literal,
      aux_sym_parenthesized_repeat1,
  [21] = 5,
    ACTIONS(219), 1,
      anon_sym_RPAREN,
    ACTIONS(136), 2,
      aux_sym_identifier_token1,
      aux_sym_identifier_token2,
    ACTIONS(138), 2,
      aux_sym_string_literal_token1,
      aux_sym_string_literal_token2,
    ACTIONS(217), 2,
      sym_number,
      anon_sym_COMMA,
    STATE(25), 3,
      sym_identifier,
      sym_string_literal,
      aux_sym_parenthesized_repeat1,
  [42] = 1,
    ACTIONS(174), 7,
      aux_sym_identifier_token1,
      aux_sym_identifier_token2,
      aux_sym_string_literal_token1,
      aux_sym_string_literal_token2,
      sym_number,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [52] = 1,
    ACTIONS(178), 7,
      aux_sym_identifier_token1,
      aux_sym_identifier_token2,
      aux_sym_string_literal_token1,
      aux_sym_string_literal_token2,
      sym_number,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [62] = 2,
    STATE(32), 1,
      sym_identifier,
    ACTIONS(221), 2,
      aux_sym_identifier_token1,
      aux_sym_identifier_token2,
  [70] = 1,
    ACTIONS(223), 1,
      ts_builtin_sym_end,
  [74] = 1,
    ACTIONS(83), 1,
      anon_sym_DOT,
  [78] = 1,
    ACTIONS(225), 1,
      anon_sym_VALUE,
  [82] = 1,
    ACTIONS(227), 1,
      anon_sym_DOT,
  [86] = 1,
    ACTIONS(178), 1,
      anon_sym_VALUE,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(25)] = 0,
  [SMALL_STATE(26)] = 21,
  [SMALL_STATE(27)] = 42,
  [SMALL_STATE(28)] = 52,
  [SMALL_STATE(29)] = 62,
  [SMALL_STATE(30)] = 70,
  [SMALL_STATE(31)] = 74,
  [SMALL_STATE(32)] = 78,
  [SMALL_STATE(33)] = 82,
  [SMALL_STATE(34)] = 86,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(7),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [9] = {.entry = {.count = 1, .reusable = false}}, SHIFT(4),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [13] = {.entry = {.count = 1, .reusable = false}}, SHIFT(29),
  [15] = {.entry = {.count = 1, .reusable = false}}, SHIFT(20),
  [17] = {.entry = {.count = 1, .reusable = false}}, SHIFT(19),
  [19] = {.entry = {.count = 1, .reusable = false}}, SHIFT(18),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [23] = {.entry = {.count = 1, .reusable = false}}, SHIFT(5),
  [25] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [27] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [29] = {.entry = {.count = 1, .reusable = false}}, SHIFT(17),
  [31] = {.entry = {.count = 1, .reusable = false}}, SHIFT(8),
  [33] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [35] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [37] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(7),
  [40] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(9),
  [43] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(4),
  [46] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(13),
  [49] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(29),
  [52] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(20),
  [55] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(19),
  [58] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(18),
  [61] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(18),
  [64] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(5),
  [67] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(16),
  [70] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(17),
  [73] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(17),
  [76] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(8),
  [79] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [81] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [83] = {.entry = {.count = 1, .reusable = true}}, SHIFT(11),
  [85] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement_body, 1, 0, 0),
  [87] = {.entry = {.count = 1, .reusable = false}}, SHIFT(6),
  [89] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(14),
  [92] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0),
  [94] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(29),
  [97] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(20),
  [100] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(19),
  [103] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(18),
  [106] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(18),
  [109] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(6),
  [112] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(16),
  [115] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(17),
  [118] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(17),
  [121] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_statement_body_repeat1, 2, 0, 0), SHIFT_REPEAT(8),
  [124] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_newline, 1, 0, 0),
  [126] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [128] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_newline, 1, 0, 0),
  [130] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_operator, 1, 0, 0),
  [132] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_operator, 1, 0, 0),
  [134] = {.entry = {.count = 1, .reusable = false}}, SHIFT(28),
  [136] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [138] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [140] = {.entry = {.count = 1, .reusable = false}}, SHIFT(26),
  [142] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [144] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_comment_line, 1, 0, 0),
  [146] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_comment_line, 1, 0, 0),
  [148] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_comment_line, 2, 0, 0),
  [150] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_comment_line, 2, 0, 0),
  [152] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement, 2, 0, 0),
  [154] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_statement, 2, 0, 0),
  [156] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement, 3, 0, 0),
  [158] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_statement, 3, 0, 0),
  [160] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_statement, 1, 0, 0),
  [162] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_statement, 1, 0, 0),
  [164] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_continuation_newline, 1, 0, 0),
  [166] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_continuation_newline, 1, 0, 0),
  [168] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_level_88_condition, 3, 0, 0),
  [170] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_level_88_condition, 3, 0, 0),
  [172] = {.entry = {.count = 1, .reusable = false}}, SHIFT(24),
  [174] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_string_literal, 1, 0, 0),
  [176] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_string_literal, 1, 0, 0),
  [178] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [180] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_identifier, 1, 0, 0),
  [182] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_level_number, 1, 0, 0),
  [184] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_level_number, 1, 0, 0),
  [186] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_keyword, 1, 0, 0),
  [188] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_keyword, 1, 0, 0),
  [190] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_embedded_comment, 2, 0, 0),
  [192] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_embedded_comment, 2, 0, 0),
  [194] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_parenthesized, 3, 0, 0),
  [196] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_parenthesized, 3, 0, 0),
  [198] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_parenthesized, 2, 0, 0),
  [200] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_parenthesized, 2, 0, 0),
  [202] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_level_88_condition, 4, 0, 0),
  [204] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_level_88_condition, 4, 0, 0),
  [206] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_parenthesized_repeat1, 2, 0, 0), SHIFT_REPEAT(28),
  [209] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_parenthesized_repeat1, 2, 0, 0), SHIFT_REPEAT(27),
  [212] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_parenthesized_repeat1, 2, 0, 0), SHIFT_REPEAT(25),
  [215] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_parenthesized_repeat1, 2, 0, 0),
  [217] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [219] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [221] = {.entry = {.count = 1, .reusable = true}}, SHIFT(34),
  [223] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [225] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [227] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
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

TS_PUBLIC const TSLanguage *tree_sitter_copybook(void) {
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
