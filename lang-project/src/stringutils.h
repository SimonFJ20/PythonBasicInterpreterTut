#ifndef STRINGUTILS_H
#define STRINGUTILS_H

#include "position.h"

int str_index_of(char* text, char c, int start, int end);

int str_last_index_of(char* text, char c, int start, int end);

int str_string_with_arrows(char* text, char* output, Position* start, Position* end);

#endif
