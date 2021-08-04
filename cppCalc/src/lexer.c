#include "lexer.h"
#include "tokens.h"

#include <stdio.h>

char WHITESPACE[] = " \n\t";
char DIGITS[] = "0123456789";

bool is_char_in(char c, char str[], size_t len)
{
    for (int i = 0; i < len; i++)
        if (c == str[i])
            return true;
    return false;
}

bool is_whitespace(char c)
{
    return is_char_in(c, WHITESPACE, 3);
}

bool is_digit(char c)
{
    return is_char_in(c, DIGITS, 10);
}

