#include "stringutils.h"
#include <string.h>
#include <stdlib.h>

int str_index_of(char* text, char c, int start, int end)
{   
    int len = strlen(text);
    if (end)
        len = end;
    for (int i = start; i < len; i++)
        if (text[i] == c)
            return i;
    return -1;
}

int str_last_index_of(char* text, char c, int start, int end)
{   
    int len = strlen(text);
    if (end)
        len = end;

    int lastIndex = -1;
    for (int i = start; i < len; i++)
        if (text[i] == c)
            lastIndex = i;
    return lastIndex;
}

int str_string_with_arrows(char* text, char* output, Position* start, Position* end)
{
    size_t output_size = 0;

    int idx_start = str_last_index_of(text, '\n', 0, start->idx);
    int idx_end = str_index_of(text, '\n', idx_start + 1, 0);

    if (idx_end < 0)
        idx_end = strlen(text);

    int line_count = end->ln - start->ln + 1;
    for (int i = 0; i < line_count; i++)
    {
        char line[256];// = text[idx_start:idx_end];
        for (int j = 0; j < idx_end - idx_start; j++)
            line[j] = text[idx_start + j];
        int col_start = (i == 0) ? start->col : 0;
        int col_end = (i == line_count - 1) ? end->col : strlen(line) - 1;
        
        for (int j = 0; j < strlen(line); j++)
            output[output_size++] = line[j];
        line[output_size++] = '\n';
        for (int j = 0; j < col_start; j++)
            output[output_size++] = ' ';
        for (int j = 0; j < (col_start - col_end); j++)
            output[output_size++] = '^';
        idx_start = idx_end;
        idx_end = str_index_of(text, '\n', idx_start + 1, 0);
    }
    output[output_size++] = '\0';

    return 0;
}

