#ifndef STRINGUTILS_H
#define STRINGUTILS_H

#include <stdlib.h>
#include <stdbool.h>

#define NULLCHAR '\0'

bool is_char_in(char c, char str[], size_t len);
bool is_whitespace(char c);
bool is_digit(char c);

int parse_int(char str[], size_t len);

#endif