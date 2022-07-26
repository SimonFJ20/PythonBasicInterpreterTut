#ifndef ERROR_H
#define ERROR_H

#include "position.h"

typedef enum
{
    IllegalCharError,
    ExpectedCharError,
    InvalidSyntaxError,
    RTError
}
ErrorType;

typedef struct
{
    ErrorType type;
    Position* pos_start;
    Position* pos_end;
    char name[32];
    char details[256];
}
Error;

int error_init(Error* e,
               ErrorType type, 
               Position* pos_start, 
               Position* pos_end, 
               char* name, 
               char* details);

int error_to_string(Error* e, char* result);

#endif
