#include "hashmap.h"
#include "array.h"
#include "dstring.h"
#include "object.h"
#include "panic.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

void construct_hashmap(HashMap* hashmap)
{
    *hashmap = (HashMap) {
        .pairs = new_array(),
    };
}

void destruct_hashmap(HashMap* hashmap)
{
    array_destruct_values(hashmap->pairs, free);
    delete_array(hashmap->pairs);
}

HashMap* new_hashmap()
{
    HashMap* hashmap = calloc(1, sizeof(HashMap));
    construct_hashmap(hashmap);
    return hashmap;
}

void delete_hashmap(HashMap* hashmap)
{
    destruct_hashmap(hashmap);
    free(hashmap);
}

HashMapPair* hashmap_pair_at(const HashMap* hashmap, size_t index)
{
    return array_at(hashmap->pairs, index);
}

size_t find_pair_in_range_maybe(const HashMap* hashmap, uint64_t key_hash, size_t first, size_t last)
{
    size_t pairs_size = array_size(hashmap->pairs);
    if (pairs_size == 0 || first >= pairs_size)
        return -1;
    size_t middle = (first + last) / 2;
    HashMapPair* pair = array_at(hashmap->pairs, middle);
    if (key_hash < pair->key) {
        return find_pair_in_range_maybe(hashmap, key_hash, first, middle - 1);
    } else if (key_hash > pair->key) {
        return find_pair_in_range_maybe(hashmap, key_hash, middle + 1, last);
    } else {
        assert(pair->key == key_hash);
        return middle;
    }
}

size_t find_unique_sorted_index(const HashMap* hashmap, uint64_t key_hash)
{
    for (size_t i = 0; i < array_size(hashmap->pairs); i++) {
        uint64_t pair_hash = hashmap_pair_at(hashmap, i)->key;
        if (pair_hash == key_hash)
            PANIC("duplicate keys");
        else if (pair_hash > key_hash)
            return i;
    }
    return array_size(hashmap->pairs);
}

void hashmap_set(HashMap* hashmap, const String* key, void* value)
{
    uint64_t key_hash = string_hash(key);
    size_t hashmap_size = array_size(hashmap->pairs);
    if (array_size(hashmap->pairs) > 0) {
        size_t index = find_pair_in_range_maybe(hashmap, key_hash, 0, hashmap_size);
        if (index != -1) {
            HashMapPair* pair = hashmap_pair_at(hashmap, index);
            pair->value = value;
        } else {
            HashMapPair* pair = calloc(1, sizeof(HashMapPair));
            *pair = (HashMapPair) {
                .key = key_hash,
                .value = value,
            };
            size_t unique_index = find_unique_sorted_index(hashmap, key_hash);
            array_insert_at(hashmap->pairs, pair, unique_index);
        }
    } else {
        HashMapPair* pair = calloc(1, sizeof(HashMapPair));
        *pair = (HashMapPair) {
            .key = key_hash,
            .value = value,
        };
        size_t unique_index = find_unique_sorted_index(hashmap, key_hash);
        array_insert_at(hashmap->pairs, pair, unique_index);
    }
}

void* hashmap_get_maybe(const HashMap* hashmap, const String* key)
{
    size_t index = find_pair_in_range_maybe(hashmap, string_hash(key), 0, array_size(hashmap->pairs));
    if (index != -1)
        return hashmap_pair_at(hashmap, index)->value;
    else
        return NULL;
}

void hashmap_delete(HashMap* hashmap, const String* key)
{
    size_t index = find_pair_in_range_maybe(hashmap, string_hash(key), 0, array_size(hashmap->pairs));
    if (index != -1)
        array_remove_and_shift_at(hashmap->pairs, index);
}
