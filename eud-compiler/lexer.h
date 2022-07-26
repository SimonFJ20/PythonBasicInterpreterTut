#ifndef LEXER_H
#define LEXER_H

#include "utils.h"
#include <stdbool.h>
#include <stdlib.h>

typedef enum {
    TT_IDENTIFIER,
    TT_KEYWORD,
    TT_INT,
    TT_LPAREN,
    TT_RPAREN,
    TT_LBRACE,
    TT_RBRACE,
    TT_LBRACKET,
    TT_RBRACKET,
    TT_SEMICOLON
} TokenType;

typedef struct {
    TokenType type;
    const char* value;
    size_t length;
} Token;

Token* new_token(TokenType type, const char* value, size_t length);
void delete_token(Token* self);

typedef struct {
    bool done;
    Token* value;
} LexerIteration;

LexerIteration* new_lexer_iteration(bool done, Token* value);
void delete_lexer_iteration(LexerIteration* self);
Token* lexer_iteration_unwrap(LexerIteration* self);

typedef struct {
    bool done;
    bool shouldStep;
    Reader* reader;
    char c;
} Lexer;

Lexer* new_lexer();
void delete_lexer(Lexer* self);

LexerIteration* lexer_next(Lexer* self);
LexerIteration* lexer_make_int(Lexer* self);
void lexer_fail_unexpected_char(Lexer* self);
void lexer_next_char(Lexer* self);

#endif