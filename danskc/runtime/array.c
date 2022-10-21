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
    if (array->size != 0)
        PANIC("cannot destruct non-empty array");
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

void array_destruct_deep(Array* array, void (*destructor)(void* value))
{
    array_destruct_values(array, destructor);
    destruct_array(array);
}

void array_destruct_values(Array* array, void (*destructor)(void* value))
{
    while (array->size) {
        array->size--;
        destructor(array->ptr[array->size]);
    }
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
    for (size_t i = 0; i < amount; i++) {
        array->ptr[array->size] = values[i];
        array->size++;
    }
}

void array_insert_at(Array* array, void* value, size_t index)
{
    if (index > array->size)
        PANIC("index out of bounds");
    Array buffer;
    construct_array(&buffer);
    while (array->size > index)
        array_push(&buffer, array_pop(array));
    array_push(array, value);
    for (size_t i = 0; i < array_size(&buffer); i++)
        array_push(array, array_pop(&buffer));
    destruct_array(&buffer);
}

void array_remove_and_shift_at(Array* array, size_t index)
{
    if (index >= array->size)
        PANIC("index out of bounds");
    Array buffer;
    construct_array(&buffer);
    while (array->size > index)
        array_push(&buffer, array_pop(array));
    array_pop(array);
    for (size_t i = 0; i < array_size(&buffer); i++)
        array_push(array, array_pop(&buffer));
    destruct_array(&buffer);
}
