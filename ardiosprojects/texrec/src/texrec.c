#include "texrec.h"
#include "utils.h"

char tr_test(char* test, char* input)
{
    short lTest = utl_strlen(test);
    short lInput = utl_strlen(input);

    char stringMatch = 0;
    for (short i = 0; i < lInput - lTest && !stringMatch; i++)
    {
        char charMatch = 1;
        for (short j = 0; j < lTest && input[i + j] != test[j]; j++)
            charMatch = 0;
        if (charMatch)
            stringMatch = 1;
    }

    return stringMatch;
}

