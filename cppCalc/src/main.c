#include <stdio.h>
#include <string.h>

int main()
{
    
    while (1)
    {
        printf("calc > ");
        char str[128];
        fgets(str, 128, stdin);
        printf("You wrote: %s\n", str);
        strcpy(str, "");
    }

}

