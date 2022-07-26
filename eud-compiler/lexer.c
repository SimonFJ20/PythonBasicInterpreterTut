#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lexer.h"

Token* new_token(TokenType type, const char* value, size_t length) 
{
    char* valuestr = calloc(length, sizeof (char));
    memcpy(valuestr, value, length);
    Token* self = calloc(1, sizeof (Token));
    *self = (Token) {
        .type = type,
        .value = valuestr,
        .length = length,
    };
    return self;
}

void delete_token(Token* self)
{
    free(self);
}

LexerIteration* new_lexer_iteration(bool done, Token* value)
{
    LexerIteration* self = calloc(1, sizeof(LexerIteration));
    *self = (LexerIteration) {
        .done = done,
        .value = value,
    };
    return self;
}

void delete_lexer_iteration(LexerIteration* self)
{
    free(self);
}

Token* lexer_iteration_unwrap(LexerIteration* self)
{
    Token* value = self->value;
    delete_lexer_iteration(self);
    return value;
}

Lexer* new_lexer(Reader* reader)
{
    Lexer* self = calloc(1, sizeof (Lexer));
    *self = (Lexer) {
        .done = false,
        .shouldStep = true,
        .reader = reader,
        .c = '\0',
    };
    return self;
}

void delete_lexer(Lexer* self)
{
    free(self);
}

LexerIteration* lexer_next(Lexer* self)
{
    if (self->done)
        return new_lexer_iteration(true, NULL);
    if (self->shouldStep)
        lexer_next_char(self);
    self->shouldStep = true;
    if (self->c >= 48 && self->c <= 57) {
        return lexer_make_int(self);
    } else {
        switch (self->c) {
        case '(':
            return new_lexer_iteration(false, new_token(TT_LPAREN, &self->c, 1));
        case ')':
            return new_lexer_iteration(false, new_token(TT_RPAREN, &self->c, 1));
        case '{':
            return new_lexer_iteration(false, new_token(TT_LBRACE, &self->c, 1));
        case '}':
            return new_lexer_iteration(false, new_token(TT_RBRACE, &self->c, 1));
        case '[':
            return new_lexer_iteration(false, new_token(TT_LBRACKET, &self->c, 1));
        case ']':
            return new_lexer_iteration(false, new_token(TT_RBRACKET, &self->c, 1));
        case ';':
            return new_lexer_iteration(false, new_token(TT_LBRACE, &self->c, 1));
        case EOF:
            return new_lexer_iteration(self->done = true, NULL);
        default:
            lexer_fail_unexpected_char(self);
            return NULL;
        }
    }
}

LexerIteration* lexer_make_int(Lexer* self)
{
    return NULL;
}

void lexer_fail_unexpected_char(Lexer* self)
{
    printf("fatal: unexpected character '%c'\n", self->c);
    exit(1);
}

void lexer_next_char(Lexer* self)
{
    self->c = self->reader->getc(self->reader);
}
