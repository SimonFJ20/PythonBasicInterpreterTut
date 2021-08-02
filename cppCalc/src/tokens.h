#ifndef TOKENS_H
#define TOKENS_H

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
    double value;
} Token;

void print_tokens(Token tokens);

#endif
