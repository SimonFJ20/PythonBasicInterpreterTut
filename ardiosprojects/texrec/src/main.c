#include <stdio.h>
#include "texrec.h"

int main()
{
    printf("\n=== PROGRAM BEGIN ===\n\n");

    char test[] = "very";
    char input[] = "this is a very long sentence";

    if (tr_test(test, input))
        printf("\"%s\"\n\ndoes exist in\n\n\"%s\"", test, input);
    else
        printf("\"%s\"\n\ndoes not exist in\n\n\"%s\"", test, input);

    printf("\n\n=== PROGRAM END ===\n\n");
    return 0;
}

