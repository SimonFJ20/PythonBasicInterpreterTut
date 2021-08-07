#include "lexer.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "tokens.h"
#include "stringutils.h"

void lexer_init(Lexer this, char text[], size_t len)
{
    strcpy(this.text, text);
    // for (int i = 0; i < len; i++)
    // {
    //     this.text[i] = text[i];
    // }
    this.text_len = len;
    this.current_char = NULLCHAR;
    this.index = -1;
    lexer_advance(this);
}

void lexer_advance(Lexer this)
{
    this.index++;
    this.current_char = this.text[this.index];
}

void lexer_generate_tokens(Lexer this, Token tokens[])
{
    int i = 0;
    printf("lexing text: '''\n%s\n'''\n", this.text);
    printf("handling char '%c' at idx:%d\n", this.current_char, this.index);
    while (this.current_char != NULLCHAR && i != this.text_len)
    {
        printf("handling char '%c' at idx:%d\n", this.current_char, this.index);
        if (is_whitespace(this.current_char))
        {
            lexer_advance(this);
        }
        else if (is_digit(this.current_char))
        {
            tokens[i] = lexer_make_number(this);
        }
        else
        {
            switch (this.current_char)
            {
                case '+':
                    tokens[i] = newToken(TT_PLUS, TOKEN_NULL);
                    lexer_advance(this);
                    break;
                case '-':
                    tokens[i] = newToken(TT_MINUS, TOKEN_NULL);
                    lexer_advance(this);
                    break;
                case '*':
                    tokens[i] = newToken(TT_MULTIPLY, TOKEN_NULL);
                    lexer_advance(this);
                    break;
                case '/':
                    tokens[i] = newToken(TT_DIVIDE, TOKEN_NULL);
                    lexer_advance(this);
                    break;
                case '(':
                    tokens[i] = newToken(TT_LPAREN, TOKEN_NULL);
                    lexer_advance(this);
                    break;
                case ')':
                    tokens[i] = newToken(TT_RPAREN, TOKEN_NULL);
                    lexer_advance(this);
                    break;
                default:
                    printf("Illegal Charactor '%c'\n", this.current_char);
                    return;
                    break;
            }
        }
        i++;
    }
    return;
}

Token lexer_make_number(Lexer this)
{
    int dec_point_count = 0;
    char num_str[64];
    num_str[0] = this.current_char;
    lexer_advance(this);

    for (int i = 1; this.current_char != NULLCHAR 
        && (this.current_char == '.' || is_digit(this.current_char)); i++)
    {
        if (this.current_char == '.')
        {
            dec_point_count++;
            if (dec_point_count > 1)
                break;
        }
        
        num_str[i] = this.current_char;
        lexer_advance(this);
    }

    size_t len = sizeof(num_str) / sizeof(num_str[0]);
    return newToken(TT_NUMBER, parse_int(num_str, len));
}
