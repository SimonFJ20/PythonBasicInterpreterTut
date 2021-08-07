#ifndef LEXER_H
#define LEXER_H

#include <stdlib.h>
#include "tokens.h"

typedef struct
{
    char text[4096];
    size_t text_len;
    char current_char;
    int index;
} Lexer;

void lexer_init(Lexer this, char text[], size_t len);
void lexer_advance(Lexer this);
void lexer_generate_tokens(Lexer this, Token tokens[]);
Token lexer_make_number(Lexer this);


#endif
