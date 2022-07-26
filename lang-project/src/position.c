#include "position.h"
#include <string.h>

int position_init(Position* p, 
                  int idx, 
                  int ln, 
                  int col, 
                  char* fn, 
                  char* ftxt)
{
    p->idx = idx;
    p->ln = ln;
    p->col = col;

    p->fn[0] = '\0';
    p->ftxt[0] = '\0';

    strcpy(p->fn, fn);
    strcpy(p->ftxt, ftxt);

    return 0;
}

int position_advance(Position* p, char current_char)
{
    p->idx++;
    p->col++;
    if (current_char == '\n')
    {
        p->ln++;
        p->col = 0;
    }
    return 0;
}

int position_copy(Position* origin, Position* clone)
{
    clone->idx = origin->idx;
    clone->ln = origin->ln;
    clone->col = origin->col;

    clone->fn[0] = '\0';
    clone->ftxt[0] = '\0';

    strcpy(clone->fn, origin->fn);
    strcpy(clone->ftxt, origin->ftxt);

    return 0;
}

