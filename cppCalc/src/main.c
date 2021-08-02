#include <stdio.h>
#include <string.h>
#include "tokens.h"


int main()
{

    Token tokens[4];

    tokens[0].type = TT_MINUS;
    tokens[0].has_value = false;
 
    tokens[1].type = TT_NUMBER;
    tokens[1].has_value = true;
    tokens[1].value = 5.0;   

    tokens[2].type = TT_PLUS;
    tokens[2].has_value = false;

    tokens[3].type = TT_NUMBER;
    tokens[3].has_value = true;
    tokens[3].value = 3.7;

    print_tokens(tokens, 4);

    while (1)
    {
        printf("calc > ");
        char str[128];
        fgets(str, 128, stdin);
        printf("You wrote: %s\n", str);
    }

}

