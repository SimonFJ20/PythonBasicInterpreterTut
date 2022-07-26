#include "utils.h"
#include <stdlib.h>
#include <string.h>

void list_free_all_and_self(List* list)
{
    list->free_all(list);
    list->delete(list);
}

void list_delete_all_and_self(List* list, void (*deletor)(void *))
{
    list->delete_all(list, deletor);
    list->delete(list);
}

void println_and_free(char* string)
{
    printf("%s\n", string);
    free(string);
}

char* chars_to_string(const char* chars, size_t amount)
{
    char* buffer = calloc(amount + 1, sizeof(char));
    strncpy(buffer, chars, amount);
    return buffer;
}

char* copy_string(const char* string)
{
    size_t length = strlen(string);
    char* copy = calloc(length + 1, sizeof(char));
    strncpy(copy, string, length);
    return copy;
}
