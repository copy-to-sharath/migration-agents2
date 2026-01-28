/**
 * External scanner for BMS (Basic Mapping Support)
 * Handles HLASM-style card format:
 * - Columns 1-71: Content  
 * - Column 72: Continuation marker (non-blank = continued)
 * - Columns 73-80: Sequence numbers (ignored)
 */

#include "tree_sitter/parser.h"
#include <wctype.h>

enum TokenType {
    STATEMENT_LINE,     // A single physical line of content (cols 1-71)
    COMMENT_LINE,       // Full comment line
};

void *tree_sitter_bms_external_scanner_create() {
    return NULL;
}

void tree_sitter_bms_external_scanner_destroy(void *payload) {
}

unsigned tree_sitter_bms_external_scanner_serialize(void *payload, char *buffer) {
    return 0;
}

void tree_sitter_bms_external_scanner_deserialize(void *payload, const char *buffer, unsigned length) {
}

bool tree_sitter_bms_external_scanner_scan(void *payload, TSLexer *lexer, const bool *valid_symbols) {
    // Skip whitespace extras manually to ensure we start at beginning of content
    while (lexer->lookahead == ' ' || lexer->lookahead == '\t') {
        lexer->advance(lexer, true);
    }
    
    // Check for comment line (starts with * in column 0)
    if (valid_symbols[COMMENT_LINE] && lexer->lookahead == '*') {
        // Advance through comment content until newline or column 72
        do {
            lexer->advance(lexer, false);
        } while (lexer->lookahead != '\n' && lexer->lookahead != '\r' && 
                 lexer->lookahead != 0 && lexer->get_column(lexer) < 72);
        
        lexer->mark_end(lexer);
        
        // Skip remaining columns (72-80) until newline
        while (lexer->lookahead != '\n' && lexer->lookahead != '\r' && lexer->lookahead != 0) {
            lexer->advance(lexer, true);
        }
        
        lexer->result_symbol = COMMENT_LINE;
        return true;
    }

    // Handle statement line - content until newline or column 72
    if (valid_symbols[STATEMENT_LINE]) {
        // Must have some content
        if (lexer->lookahead == '\n' || lexer->lookahead == '\r' || lexer->lookahead == 0) {
            return false;
        }
        
        // Advance through statement content
        do {
            lexer->advance(lexer, false);
        } while (lexer->lookahead != '\n' && lexer->lookahead != '\r' && 
                 lexer->lookahead != 0 && lexer->get_column(lexer) < 72);
        
        lexer->mark_end(lexer);
        
        // Skip remaining columns until newline
        while (lexer->lookahead != '\n' && lexer->lookahead != '\r' && lexer->lookahead != 0) {
            lexer->advance(lexer, true);
        }
        
        lexer->result_symbol = STATEMENT_LINE;
        return true;
    }
    
    return false;
}
