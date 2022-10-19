#include "array.h"
#include "panic.h"
#include <stdlib.h>

void construct_array(Array* array)
{
    *array = (Array) {
        .size = 0,
        .capacity = ARRAY_ELEMENT_CHUNK,
        .ptr = calloc(ARRAY_ELEMENT_CHUNK, sizeof(void*)),
    };
}

void destruct_array(Array* array)
{
    free(array->ptr);
}

Array* new_array()
{
    Array* array = calloc(1, sizeof(Array));
    construct_array(array);
    return array;
}

void delete_array(Array* array)
{
    destruct_array(array);
    free(array);
}

size_t array_size(const Array* array)
{
    return array->size;
}

void* array_at(const Array* array, size_t index)
{
    if (index < 0 || index >= array->size)
        PANIC("index out of bounds");
    return array->ptr[index];
}

void array_push(Array* array, void* value)
{
    if (array->size == array->capacity) {
        array->capacity += ARRAY_ELEMENT_CHUNK;
        array->ptr = realloc(array->ptr, sizeof(void*) * array->capacity);
    }
    array->ptr[array->size] = value;
    array->size++;
}

void* array_pop(Array* array)
{
    if (array->size == 0)
        PANIC("cannot pop from empty array");
    array->size--;
    void* value = array->ptr[array->size];
    array->ptr[array->size] = NULL;
    return value;
}

void array_add(Array* array, size_t amount, void** values)
{
    if (array->capacity - array->size < amount) {
        array->capacity = array->size + amount + (amount % ARRAY_ELEMENT_CHUNK);
        array->ptr = realloc(array->ptr, sizeof(void*) * array->capacity);
    }
    for (int i = 0; i < amount; i++) {
        array->ptr[array->size] = values[i];
        array->size++;
    }
}
