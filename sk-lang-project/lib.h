#ifndef LIB_H
#define LIB_H

#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define new(s) (calloc(1, sizeof (s)))
#define delete(o) (free(o))

void print_int(int v);

typedef struct {
    uint64_t* items;
    size_t size;
    size_t capacity;
} Vec;

typedef Vec String;

void vec_push(Vec* v, uint64_t item);
void vec_reserve(Vec* v,  size_t slots);
uint64_t vec_pop(Vec* v);
uint64_t vec_get(Vec* v, size_t i);
size_t vec_length(Vec* v);

Vec* vec_from_string(const char* string);
bool string_match(Vec* a, Vec* b);
void print(Vec* s);

#endif
