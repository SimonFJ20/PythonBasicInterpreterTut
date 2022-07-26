#include "utils.h"

short utl_strlen(char* str)
{
    short length = 0;
    char* position = str;
    while (*position)
    {
        length++;
        position++;
    }
    return length;
}




