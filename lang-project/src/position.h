#ifndef POSITION_H
#define POSITION_H

typedef struct
{
    int idx;
    int ln;
    int col;
    char fn[64];
    char ftxt[65536];
}
Position;

int position_init(Position* p, 
                  int idx, 
                  int ln, 
                  int col, 
                  char* fn, 
                  char* ftxt); 

int position_advance(Position* p, char current_char);

int position_copy(Position* origin, Position* clone);

#endif
