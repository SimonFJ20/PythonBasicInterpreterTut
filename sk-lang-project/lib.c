#include "lib.h"

#include <assert.h>

void print_int(int v)
{
    printf("%d\n", v);
}

void vec_push(Vec* v, uint64_t item)
{
    v->size++;
    if (v->size > v->capacity) {
        v->capacity = v->size + v->size % 8;
        v->items = realloc(v->items, sizeof (uint64_t) * v->capacity);
    }
    v->items[v->size - 1] = item;
}

void vec_reserve(Vec* v,  size_t slots)
{
    size_t required = v->size + slots;
    if (required > v->capacity) {
        v->capacity = required + required % 8;
        v->items = realloc(v->items, sizeof (uint64_t) * v->capacity);
    }
}

uint64_t vec_pop(Vec* v)
{
    assert(v->size > 0);
    v->size--;
    return v->items[v->size];
}

uint64_t vec_get(Vec* v, size_t i)
{
    if (i < 0)
        return vec_get(v, v->size - i);
    assert(v->size > i);
    return v->items[i];
}

size_t vec_length(Vec* v)
{
    return v->size;
}

Vec* vec_from_string(const char* string)
{
    Vec* v = calloc(1, sizeof (Vec));
    vec_reserve(v, strlen(string));
    for (int i = 0; string[i]; i++)
        vec_push(v, string[i]);
    return v;
}

bool string_match(Vec* a, Vec* b)
{
    if (a->size != b->size)
        return false;
    for (int i = 0; i < a->size; i++) {
        if (a->items[i] != b->items[i])
            return false;
    }
    return true;
}

void print(Vec* s)
{
    char* buffer = calloc(s->size + 1, sizeof (char));
    int i = 0;
    while (i < s->size)
    {
        buffer[i] = (char)s->items[i];
        i++;
    }
    buffer[i] = '\0';
    puts(buffer);
}
