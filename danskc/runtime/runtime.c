#include "dstring.h"
#include <stdint.h>
#include <stdio.h>

int main()
{
    String* hello = string_from("hello");
    String* world = string_from("world");
    String* string = string_add(hello, world);
    const char* value = string_as_cstr(string);
    size_t length = string_size(string);
    uint64_t hash = string_hash(string);
    printf("value: \"%s\", length: %ld, hash: %ld\n", value, length, hash);
    delete_string(string);
}
