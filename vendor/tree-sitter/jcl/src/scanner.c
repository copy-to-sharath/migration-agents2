#include "tree_sitter/parser.h"
#include <wctype.h>
#include <string.h>

enum TokenType {
  INLINE_DATA_CONTENT,
};

void *tree_sitter_jcl_external_scanner_create() { return NULL; }
void tree_sitter_jcl_external_scanner_destroy(void *payload) {}
void tree_sitter_jcl_external_scanner_reset(void *payload) {}
unsigned tree_sitter_jcl_external_scanner_serialize(void *payload, char *buffer) { return 0; }
void tree_sitter_jcl_external_scanner_deserialize(void *payload, const char *buffer, unsigned length) {}

static void advance(TSLexer *lexer) { lexer->advance(lexer, false); }
static void skip(TSLexer *lexer) { lexer->advance(lexer, true); }

bool tree_sitter_jcl_external_scanner_scan(void *payload, TSLexer *lexer, const bool *valid_symbols) {
  if (!valid_symbols[INLINE_DATA_CONTENT]) {
    return false;
  }

  // Only match inline data at column 0 (start of line)
  // This is critical to avoid matching content within JCL statements
  if (lexer->get_column(lexer) != 0) {
    return false;
  }

  // Lines starting with / are JCL statements, not inline data
  if (lexer->lookahead == '/') {
    return false;
  }
  
  // Check if at end of file
  if (lexer->eof(lexer)) {
    return false;
  }
  
  // Consume characters until end of line
  bool has_content = false;
  while (!lexer->eof(lexer) && lexer->lookahead != '\n' && lexer->lookahead != '\r') {
    has_content = true;
    advance(lexer);
  }
  
  if (has_content) {
    lexer->result_symbol = INLINE_DATA_CONTENT;
    return true;
  }
  
  return false;
}
