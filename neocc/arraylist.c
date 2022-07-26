#include "parser.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

ArrayList* new_array_list()
{
    static_assert(sizeof(List) == 48, "incomplete implementation of List");
    static_assert(sizeof(ArrayList) == 64, "incomplete construction of ArrayList");
    ArrayList* self = calloc(1, sizeof(ArrayList));
    *self = (ArrayList) {
        .delete = delete_array_list,
        .length = array_list_length,
        .get = array_list_get,
        .add = array_list_add,
        .free_all = array_list_free_all,
        .delete_all = array_list_delete_all,
        .m_length = 0,
        .m_elements = NULL,
    };
    return self;
}

void delete_array_list(ArrayList* self)
{
    free(self->m_elements);
    free(self);
}

size_t array_list_length(ArrayList* self)
{
    return self->m_length;
}

void* array_list_get(ArrayList* self, int index)
{
    if (index < 0)
        return array_list_get(self, self->m_length - index);
    assert(index < self->m_length && "index out of range");
    return self->m_elements[index];
}

void array_list_add(ArrayList* self, void* element)
{
    self->m_length++;
    self->m_elements = realloc(self->m_elements, sizeof(void*) * self->m_length);
    self->m_elements[self->m_length - 1] = element;
}

void array_list_free_all(ArrayList* self)
{
    for (int i = 0; i < self->m_length; i++)
        free(self->m_elements[i]);
}

void array_list_delete_all(ArrayList* self, void (*deletor)(void* element))
{
    for (int i = 0; i < self->m_length; i++)
        deletor(self->m_elements[i]);
}
