#ifndef TOKENS_H
#define TOKENS_H

#include "position.h"

typedef enum
{
    TT_INT,
    TT_FLOAT,
    TT_STRING,
    TT_IDENTIFIER,
    TT_KEYWORD,
    TT_PLUS,
    TT_MINUS,
    TT_MUL,
    TT_DIV,
    TT_POW,
    TT_EQ,
    TT_LPAREN,
    TT_RPAREN,
    TT_LSQUARE,
    TT_RSQUARE,
    TT_EE,
    TT_NE,
    TT_LT,
    TT_GT,
    TT_LTE,
    TT_GTE,
    TT_COMMA,
    TT_ARROW,
    TT_NEWLINE,
    TT_EOF,
}
TokenType;

typedef enum
{
    TV_INT,
    TV_FLOAT,
    TV_CHAR,
    TV_STRING,
}
TokenValueType;

extern const char* KEYWORDS[];

typedef struct
{
    TokenType type;
    TokenValueType vType;
    union
    {
        int intValue;
        double floatValue;
        char charValue;
        char* stringValue;
    };
    Position pos_start;
    Position pos_end;
}
Token;

int token_init(Token* t,
               TokenType type,
               Position* pos_start,
               Position* pos_end);

int token_set_int(Token* t, int value);
int token_set_float(Token* t, double value);
int token_set_char(Token* t, char value);
int token_set_string(Token* t, char* value);

#endif