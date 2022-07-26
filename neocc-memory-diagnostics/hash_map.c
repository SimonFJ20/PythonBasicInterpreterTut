#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "utils.h"


uint64_t hash_string(const char* value)
{
    // https://cp-algorithms.com/string/string-hashing.html
    // 0 <= char <= 127
    const int p = 131;
    const int m = 1e9 + 9;
    size_t string_length = strlen(value);
    long long hash_value = 0;
    long long p_pow = 1;
    for (int i = 0; i < string_length; i++) {
        hash_value = (hash_value + (value[i] + 1) * p_pow) % m;
        p_pow = (p_pow * p) % m;
    }
    return hash_value;
}

StringHashMapElement* new_string_hash_map_element(char* key, uint64_t hash, void* value)
{
    static_assert(sizeof(StringHashMapElement) == 24, "incomplete construction of StringHashMapElement");
    StringHashMapElement* self = calloc(1, sizeof(StringHashMapElement));
    *self = (StringHashMapElement) {
        .key = key,
        .hash = hash,
        .value = value,
    };
    return self;
}

void delete_string_hash_map_element(StringHashMapElement* self)
{
    free(self->key);
    free(self);
}

StringHashMap* new_string_hash_map()
{
    static_assert(sizeof(Map) == 40, "incomplete implementation of Map");
    static_assert(sizeof(StringHashMap) == 56, "incomplete construction of StringHashMap");
    StringHashMap* self = calloc(1, sizeof(StringHashMap));
    *self = (StringHashMap) {
        .delete = delete_string_hash_map,
        .length = string_hash_map_length,
        .get = string_hash_map_get,
        .set = string_hash_map_set,
        .contains_key = string_hash_map_contains_key,
        .m_length = 0,
        .m_elements = (List*) new_array_list(),
    };
    return self;
}

void delete_string_hash_map(StringHashMap* self)
{
    list_delete_all_and_self(self->m_elements, (void (*)(void*)) delete_string_hash_map_element);
    free(self);
}

size_t string_hash_map_length(StringHashMap* self)
{
    return self->m_length;
}

void* string_hash_map_get(StringHashMap* self, const char* string)
{
    // TODO binary search
    uint64_t hash = hash_string(string);
    for (int i = 0; i < self->m_elements->length(self->m_elements); i++) {
        StringHashMapElement* element = self->m_elements->get(self->m_elements, i);
        if (element->hash == hash)
            return element->value;
    }
    assert(!"element with key not found");
}

void string_hash_map_set(StringHashMap* self, const char* string, void* value)
{
    uint64_t hash = hash_string(string);
    for (int i = 0; i < self->m_elements->length(self->m_elements); i++) {
        StringHashMapElement* element = self->m_elements->get(self->m_elements, i);
        if (element->hash == hash) {
            element->value = value;
            return;
        }
    }
    self->m_elements->add(self->m_elements, new_string_hash_map_element(copy_string(string), hash, value));
}

bool string_hash_map_contains_key(StringHashMap* self, const char* string)
{
    // TODO binary search
    uint64_t hash = hash_string(string);
    for (int i = 0; i < self->m_elements->length(self->m_elements); i++) {
        StringHashMapElement* element = self->m_elements->get(self->m_elements, i);
        if (element->hash == hash)
            return true;
    }
    return false;
}
