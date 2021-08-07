#include <stdio.h>
#include "tokens.h"

int test_tokens()
{
    printf("Testing 'tokens.h' && 'tokens.c'\n");
    Token tokens[4];

    tokens[0] = newToken(TT_MINUS, TOKEN_NULL);
    tokens[1] = newToken(TT_NUMBER, 5.0);
    tokens[2] = newToken(TT_PLUS, TOKEN_NULL);
    tokens[3] = newToken(TT_NUMBER, 3.7);

    print_tokens(tokens, 4);
    printf("Done\n");
    return 0;
}

int test_all()
{
    printf("Testing everything\n");
    test_tokens();
    printf("All done\n");
    return 0;
}
