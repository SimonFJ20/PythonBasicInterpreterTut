#include "dstring.h"
#include "panic.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

void construct_string(String* string)
{
    *string = (String) {
        .size = 0,
        .capacity = STRING_CHAR_CHUNK,
        .value = calloc(STRING_CHAR_CHUNK, sizeof(char)),
    };
}

void destruct_string(String* string)
{
    free(string->value);
}

String* new_string()
{
    String* string = calloc(1, sizeof(String));
    construct_string(string);
    return string;
}

void delete_string(String* string)
{
    destruct_string(string);
    free(string);
}

String* string_from(const char* value)
{
    size_t length = strlen(value);
    size_t capacity = length + (length % STRING_CHAR_CHUNK);
    String* string = calloc(1, sizeof(String));
    *string = (String) {
        .size = length,
        .capacity = capacity,
        .value = calloc(capacity, sizeof(char)),
    };
    strncpy(string->value, value, length);
    return string;
}

String* string_clone(const String* other)
{
    String* string = calloc(1, sizeof(String));
    *string = (String) {
        .size = other->size,
        .capacity = other->capacity,
        .value = calloc(other->capacity, sizeof(char)),
    };
    strncpy(string->value, other->value, other->size);
    return string;
}

size_t string_size(const String* string)
{
    return string->size;
}

char string_at(String* string, size_t index)
{
    if (index < 0 || index > string->size)
        PANIC("index out of bounds");
    return string->value[index];
}

void string_add_char(String* string, char value)
{
    if (string->capacity == string->size) {
        string->capacity += STRING_CHAR_CHUNK;
        string->value = realloc(string->value, string->capacity);
    }
    string->value[string->size] = value;
    string->size++;
    string->value[string->size] = '\0';
}

String* string_add(String* string, String* other)
{
    if (string->capacity - string->size < other->size) {
        string->capacity += other->size + (other->size % STRING_CHAR_CHUNK);
        string->value = realloc(string->value, string->capacity);
    }
    for (size_t i = 0; i < other->size; i++) {
        string->value[string->size] = other->value[i];
        string->size++;
    }
    string->value[string->size] = '\0';
    return string;
}

const char* string_as_cstr(const String* string)
{
    return string->value;
}

uint64_t string_hash(const String* string)
{
    uint64_t hash = STRING_MAGIC_HASH_VALUE;
    for (size_t i = 0; i < string->size; i++)
        hash = ((hash << 5) + hash) + string->value[i];
    return hash;
}
