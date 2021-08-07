#include <stdio.h>
#include <string.h>
#include "tokens.h"
#include "lexer.h"
#include "tests.h"

int main()
{

    // test_all();

    while (1)
    {
        printf("calc > ");
        char str[128];
        fgets(str, 128, stdin);
        //printf("You wrote: %s\n", str);
        Lexer lexer;
        lexer_init(lexer, str, 128);
        Token tokens[128];
        lexer_generate_tokens(lexer, tokens);
        print_tokens(tokens, 128);
    }

}

