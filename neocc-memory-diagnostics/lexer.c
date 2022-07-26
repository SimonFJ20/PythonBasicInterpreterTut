#include "parser.h"
#include "utils.h"
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

List* tokenize(char* text)
{
    Lexer* lexer = new_lexer(text);
    List* result = lexer_tokenize(lexer);
    delete_lexer(lexer);
    return result;
}

const char* token_type_to_string(TokenType type)
{
    switch (type) {
    case TOKEN_TYPE_IDENTIFIER:
        return "TOKEN_TYPE_IDENTIFIER";
    case TOKEN_TYPE_KW_VOID:
        return "TOKEN_TYPE_KW_VOID";
    case TOKEN_TYPE_KW_INT:
        return "TOKEN_TYPE_KW_INT";
    case TOKEN_TYPE_KW_IF:
        return "TOKEN_TYPE_KW_IF";
    case TOKEN_TYPE_KW_ELSE:
        return "TOKEN_TYPE_KW_ELSE";
    case TOKEN_TYPE_KW_FOR:
        return "TOKEN_TYPE_KW_FOR";
    case TOKEN_TYPE_KW_WHILE:
        return "TOKEN_TYPE_KW_WHILE";
    case TOKEN_TYPE_KW_SWITCH:
        return "TOKEN_TYPE_KW_SWITCH";
    case TOKEN_TYPE_KW_CASE:
        return "TOKEN_TYPE_KW_CASE";
    case TOKEN_TYPE_KW_RETURN:
        return "TOKEN_TYPE_KW_RETURN";
    case TOKEN_TYPE_KW_CONTINUE:
        return "TOKEN_TYPE_KW_CONTINUE";
    case TOKEN_TYPE_KW_BREAK:
        return "TOKEN_TYPE_KW_BREAK";
    case TOKEN_TYPE_INT_LITERAL:
        return "TOKEN_TYPE_INT_LITERAL";
    case TOKEN_TYPE_LPAREN:
        return "TOKEN_TYPE_LPAREN";
    case TOKEN_TYPE_RPAREN:
        return "TOKEN_TYPE_RPAREN";
    case TOKEN_TYPE_LBRACE:
        return "TOKEN_TYPE_LBRACE";
    case TOKEN_TYPE_RBRACE:
        return "TOKEN_TYPE_RBRACE";
    case TOKEN_TYPE_LBRACKET:
        return "TOKEN_TYPE_LBRACKET";
    case TOKEN_TYPE_RBRACKET:
        return "TOKEN_TYPE_RBRACKET";
    case TOKEN_TYPE_COMMA:
        return "TOKEN_TYPE_COMMA";
    case TOKEN_TYPE_ASSIGN:
        return "TOKEN_TYPE_ASSIGN";
    case TOKEN_TYPE_EQUAL:
        return "TOKEN_TYPE_EQUAL";
    case TOKEN_TYPE_PLUS:
        return "TOKEN_TYPE_PLUS";
    case TOKEN_TYPE_EOL:
        return "TOKEN_TYPE_EOL";
    case TOKEN_TYPE_EOF:
        return "TOKEN_TYPE_EOF";
    }
    assert(0 && "unreachable");
}

Token* new_token(
    const TokenType type,
    const char* value,
    const size_t length)
{
    Token* self = calloc(1, sizeof(Token));
    *self = (Token) {
        .type = type,
        .value = value,
        .length = length,
    };
    return self;
}

void delete_token(Token* self)
{
    free(self);
}

char* token_to_string(Token* self)
{
    char* value_str = chars_to_string(self->value, self->length);

    char* buffer = calloc(8192, sizeof(char));
    snprintf(buffer, 8192, "Token(%s, '%s', %ld)", token_type_to_string(self->type), value_str, self->length);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(value_str);

    return buffer;
}

Lexer* new_lexer(char* text)
{
    static_assert(sizeof(Lexer) == 16, "incomplete construction of Lexer");
    Lexer* self = calloc(1, sizeof(Lexer));
    *self = (Lexer) {
        .text = text,
        .index = 0,
        .c = text[0],
        .done = false,
    };
    return self;
}

void delete_lexer(Lexer* self)
{
    free(self);
}

static inline bool is_whitespace(const char c) { return c == ' ' || c == '\t' || c == '\n' || c == '\r'; }
static inline bool is_digit(const char c) { return c >= '0' && c <= '9'; }
static inline bool is_letter(const char c) { return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'; }

List* lexer_tokenize(Lexer* self)
{
    List* tokens = (List*) new_array_list();

    while (!self->done) {
        if (is_whitespace(self->c)) {
            lexer_next(self);
        } else if (is_digit(self->c)) {
            tokens->add(tokens, lexer_make_number(self));
        } else if (is_letter(self->c)) {
            tokens->add(tokens, lexer_make_name(self));
        } else {
            tokens->add(tokens, lexer_match_char(self));
        }
    }

    tokens->add(tokens, new_token(TOKEN_TYPE_EOF, self->text + self->index, 1));
    return tokens;
}

static inline Token* call_next_after(Lexer* self, Token* token)
{
    lexer_next(self);
    return token;
}

static inline Token* make_single_char_token_and_call_next_after(Lexer* self, TokenType type)
{
    return call_next_after(self, new_token(type, &self->text[self->index], 1));
}

Token* lexer_match_char(Lexer* self)
{
    switch (self->c) {
    case '(':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_LPAREN);
    case ')':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_RPAREN);
    case '{':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_LBRACE);
    case '}':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_RBRACE);
    case '[':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_LBRACKET);
    case ']':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_RBRACKET);
    case '=':
        return lexer_make_equal_or_assign(self);
    case '+':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_PLUS);
    case ';':
        return make_single_char_token_and_call_next_after(self, TOKEN_TYPE_EOL);
    default:
        printf("unexpected char %d == '%c'\n", self->c, self->c);
        assert(!"unexpected char");
    }
}

Token* lexer_make_number(Lexer* self)
{
    const char* value = &self->text[self->index];
    size_t value_length = 1;
    lexer_next(self);
    while (!self->done && is_digit(self->c)) {
        value_length++;
        lexer_next(self);
    }
    return new_token(TOKEN_TYPE_INT_LITERAL, value, value_length);
}

#define CHECK_KEYWORD(identifier, type, keyword) \
    ({                                                   \
        if (strncmp(identifer, keyword, strlen(keyword)) == 0)    \
            return type;                                 \
    })

static inline TokenType identifier_or_kw_token_type(const char* identifer)
{
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_VOID, "void");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_INT, "int");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_IF, "if");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_ELSE, "else");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_FOR, "for");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_WHILE, "while");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_SWITCH, "switch");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_CASE, "case");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_RETURN, "return");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_CONTINUE, "continue");
    CHECK_KEYWORD(identifer, TOKEN_TYPE_KW_BREAK, "break");
    return TOKEN_TYPE_IDENTIFIER;
}

Token* lexer_make_name(Lexer* self)
{
    const char* value = &self->text[self->index];
    size_t value_length = 1;
    lexer_next(self);
    while (!self->done && (is_digit(self->c) || is_letter(self->c))) {
        value_length++;
        lexer_next(self);
    }
    TokenType type = identifier_or_kw_token_type(value);
    return new_token(type, value, value_length);
}

Token* lexer_make_equal_or_assign(Lexer* self)
{
    const char* value = &self->text[self->index];
    lexer_next(self);
    if (self->c == '=') {
        lexer_next(self);
        return new_token(TOKEN_TYPE_EQUAL, value, 2);
    }
    return new_token(TOKEN_TYPE_ASSIGN, value, 1);
}

void lexer_next(Lexer* self)
{
    self->c = self->text[++self->index];
    self->done = self->c == '\0';
}
