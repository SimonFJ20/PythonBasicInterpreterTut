#ifndef LEXER_H
#define LEXER_H

#include <stdlib.h>
#include <stdbool.h>

bool is_char_in(char c, char str[], size_t len);
bool is_whitespace(char c);
bool is_digit(char c);

#endif
