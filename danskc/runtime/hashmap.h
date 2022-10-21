#ifndef HASHMAP_H
#define HASHMAP_H

#include "array.h"
#include "dstring.h"
#include "object.h"
#include <stdint.h>

typedef struct HashMapPair {
    uint64_t key;
    void* value;
} HashMapPair;

typedef struct HashMap {
    Array* pairs; // Array<HashMapPair>
} HashMap;

void construct_hashmap(HashMap* hashmap);
void destruct_hashmap(HashMap* hashmap);
HashMap* new_hashmap();
void delete_hashmap(HashMap* hashmap);
void hashmap_set(HashMap* hashmap, const String* key, void* value);
void* hashmap_get_maybe(const HashMap* hashmap, const String* key);
void hashmap_delete(HashMap* hashmap, const String* key);

#endif