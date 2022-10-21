#ifndef DSTRING_H
#define DSTRING_H

#include <stdint.h>
#include <stdlib.h>

#define STRING_CHAR_CHUNK 8
#define STRING_MAGIC_HASH_VALUE 5381

typedef struct String {
    size_t size, capacity;
    char* value;
} String;

void construct_string(String* string);
void destruct_string(String* string);
String* new_string();
void delete_string(String* string);
String* string_from(const char* value);
String* string_clone(const String* other);
size_t string_size(const String* string);
char string_at(String* string, size_t index);
void string_add_char(String* string, char value);
String* string_add(String* string, String* other);
const char* string_as_cstr(const String* string);
uint64_t string_hash(const String* string);

#endif