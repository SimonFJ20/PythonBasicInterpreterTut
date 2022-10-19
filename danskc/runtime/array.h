#ifndef ARRAY_H
#define ARRAY_H

#include <stdlib.h>

#define ARRAY_ELEMENT_CHUNK 8

typedef struct Array {
    size_t size, capacity;
    void** ptr;
} Array;

void construct_array(Array* array);
void destruct_array(Array* array);
Array* new_array();
void delete_array(Array* array);
size_t array_size(const Array* array);
void* array_at(const Array* array, size_t index);
void array_push(Array* array, void* value);
void* array_pop(Array* array);
void array_add(Array* array, size_t amount, void** values);

#endif