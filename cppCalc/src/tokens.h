#ifndef TOKENS_H
#define TOKENS_H

#include <stdlib.h>
#include <stdbool.h>

#define TT_NUMBER   0
#define TT_PLUS     1
#define TT_MINUS    2
#define TT_MULTIPLY 3
#define TT_DIVIDE   4
#define TT_LPAREN   5
#define TT_RPAREN   6

typedef struct
{
    int type;
    bool has_value;
    double value;
} Token;

void print_tokens(Token tokens[], size_t len);

#endif
