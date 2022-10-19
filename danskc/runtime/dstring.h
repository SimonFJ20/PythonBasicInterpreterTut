#ifndef DSTRING_H
#define DSTRING_H

#include <stdint.h>
#include <stdlib.h>

typedef struct String {
    size_t size, capacity;
    char* value;
} String;

void construct_string(String* string);
void destruct_string(String* string);
String* new_string();
void delete_string(String* string);
String* string_from(const char* value);
uint64_t string_hash(String* string);

#endif