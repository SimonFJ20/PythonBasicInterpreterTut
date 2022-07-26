#include "utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

StringBuilder* new_string_builder()
{
    static_assert(sizeof(StringBuilder) == 16, "incomplete construction of StringBuilder");
    StringBuilder* self = calloc(1, sizeof(StringBuilder));
    *self = (StringBuilder) {
        .m_length = 0,
        .m_buffer = calloc(1, sizeof(char)),
    };
    return self;
}

void delete_string_builder(StringBuilder* self)
{
    free(self->m_buffer);
    free(self);
}

size_t string_builder_length(StringBuilder* self)
{
    return self->m_length;
}

char* string_builder_c_string(StringBuilder* self)
{
    char* buffer = calloc(1, self->m_length * sizeof(char) + 1);
    memcpy(buffer, self->m_buffer, self->m_length);
    return buffer;
}

char* string_builder_buffer(StringBuilder* self)
{
    return self->m_buffer;
}

void string_builder_write(StringBuilder* self, char* string)
{
    size_t old_length = self->m_length;
    self->m_length += strlen(string);
    self->m_buffer = realloc(self->m_buffer, self->m_length * sizeof(char) + 1);
    memset(self->m_buffer + sizeof(char) * old_length, '\0', self->m_length - old_length);
    strcat(self->m_buffer, string);
}

void string_builder_write_fmt(StringBuilder* self, const char* fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    char buffer[8192] = "";
    vsnprintf(buffer, 8192, fmt, args);
    string_builder_write(self, buffer);
}
