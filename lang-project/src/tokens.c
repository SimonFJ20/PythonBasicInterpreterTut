#include "tokens.h"
#include "position.h"
#include <string.h>

const char* KEYWORDS[] = {
    "VAR",
    "AND",
    "OR",
    "NOT",
    "IF",
    "ELIF",
    "ELSE",
    "FOR",
    "TO",
    "STEP",
    "WHILE",
    "FUN",
    "THEN",
    "DO",
    "END",
    "RETURN",
    "CONTINUE",
    "BREAK"
};

int token_init(Token* t,
               TokenType type,
               Position* pos_start,
               Position* pos_end)
{
    t->type = type;

    position_copy(pos_start, &t->pos_start);
    position_copy(pos_end, &t->pos_end);

    return 0;
} 

int token_set_int(Token* t, int value)
{
    t->type = TV_INT;
    t->intValue = value;

    return 0;
}
int token_set_float(Token* t, double value)
{
    t->type = TV_FLOAT;
    t->floatValue = value;

    return 0;
}
int token_set_char(Token* t, char value)
{
    t->type = TV_CHAR;
    t->charValue = value;

    return 0;
}
int token_set_string(Token* t, char* value)
{
    t->type = TV_STRING;
    t->stringValue[0] = '\0';
    strcpy(t->stringValue, value);

    return 0;
}