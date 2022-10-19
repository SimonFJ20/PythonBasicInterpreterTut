#ifndef HASHMAP_H
#define HASHMAP_H

#include "array.h"
#include <stdint.h>

typedef struct HashMapPair {
    uint64_t key;
    void* value;
} HashMapPair;

typedef struct HashMap {
    Array* pairs; // <HashMapPair>
} HashMap;

void construct_hashmap(HashMap* hashmap);
void destruct_hashmap(HashMap* hashmap);
HashMap* new_hashmap();
void delete_hashmap();

#endif