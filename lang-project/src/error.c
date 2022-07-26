#include <string.h>
#include <stdio.h>
#include "error.h"
#include "stringutils.h"

int error_init(Error* e,
               ErrorType type, 
               Position* pos_start, 
               Position* pos_end, 
               char* name, 
               char* details)
{
    e->type = type;
    e->pos_start = pos_start;
    e->pos_end = pos_end;

    e->name[0] = '\0';
    e->details[0] = '\0';

    strcpy(e->name, name);
    strcpy(e->details, details);

    return 0;
} 

int error_to_string(Error* e, char* result) 
{
    result[0] = '\0';

    char swa[64] = {'\0'};

    str_string_with_arrows(
            e->pos_start->ftxt, 
            swa, 
            e->pos_start, 
            e->pos_end);

    sprintf(result, 
            "%s: %s\nOn line %d, in \"%s\"\n\n%s",
            e->name,
            e->details,
            e->pos_start->ln - 1,
            e->pos_start->fn, 
            swa);
    
    return 0;
}


