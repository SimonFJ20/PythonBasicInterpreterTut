#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

typedef struct List {
    void (*delete)(struct List* self);
    size_t (*length)(struct List* self);
    void* (*get)(struct List* self, int index);
    void (*add)(struct List* self, void* element);
    void (*free_all)(struct List* self);
    void (*delete_all)(struct List* self, void (*)(void*));
} List;

void list_free_all_and_self(List* list);
void list_delete_all_and_self(List* list, void (*deletor)(void*));

typedef struct ArrayList {
    void (*delete)(struct ArrayList* self);
    size_t (*length)(struct ArrayList* self);
    void* (*get)(struct ArrayList* self, int index);
    void (*add)(struct ArrayList* self, void* element);
    void (*free_all)(struct ArrayList* self);
    void (*delete_all)(struct ArrayList* self, void (*)(void*));
    size_t m_length;
    void** m_elements;
} ArrayList;

ArrayList* new_array_list();
void delete_array_list(ArrayList* self);
size_t array_list_length(ArrayList* self);
void* array_list_get(ArrayList* self, int index);
void array_list_add(ArrayList* self, void* element);
void array_list_free_all(ArrayList* self);
void array_list_delete_all(ArrayList* self, void (*)(void*));

typedef struct Map {
    void (*delete)(struct Map* self);
    size_t (*length)(struct Map* self);
    void* (*get)(struct Map* self, const char* string);
    void (*set)(struct Map* self, const char* string, void* value);
    bool (*contains_key)(struct Map* self, const char* string);
} Map;

uint64_t hash_string(const char* value);

typedef struct StringHashMapElement {
    char* key;
    uint64_t hash;
    void* value;
} StringHashMapElement;

StringHashMapElement* new_string_hash_map_element(char* key, uint64_t hash, void* value);
void delete_string_hash_map_element(StringHashMapElement* self);

typedef struct StringHashMap {
    void (*delete)(struct StringHashMap* self);
    size_t (*length)(struct StringHashMap* self);
    void* (*get)(struct StringHashMap* self, const char* string);
    void (*set)(struct StringHashMap* self, const char* string, void* value);
    bool (*contains_key)(struct StringHashMap* self, const char* string);
    size_t m_length;
    List* m_elements;
} StringHashMap;

StringHashMap* new_string_hash_map();
void delete_string_hash_map(StringHashMap* self);
size_t string_hash_map_length(StringHashMap* self);
void* string_hash_map_get(StringHashMap* self, const char* string);
void string_hash_map_set(StringHashMap* self, const char* string, void* value);
bool string_hash_map_contains_key(StringHashMap* self, const char* string);

typedef struct FileReader {
    FILE* fp;
} FileReader;

FileReader* new_file_reader(const char* path);
void delete_file_reader(FileReader* self);
size_t file_reader_length(FileReader* self);
char* file_reader_read(FileReader* self);

typedef struct FileWriter {
    FILE* fp;
} FileWriter;

FileWriter* new_file_writer(const char* path);
void delete_file_writer(FileWriter* self);
void file_writer_write(FileWriter* self, char* string);

typedef struct StringBuilder {
    size_t m_length;
    char* m_buffer;
} StringBuilder;

StringBuilder* new_string_builder();
void delete_string_builder(StringBuilder* self);
size_t string_builder_length(StringBuilder* self);
char* string_builder_c_string(StringBuilder* self);
char* string_builder_buffer(StringBuilder* self);
void string_builder_write(StringBuilder* self, char* string);
void string_builder_write_fmt(StringBuilder* self, const char* fmt, ...);

char* chars_to_string(const char* chars, size_t amount);
char* copy_string(const char* string);
void println_and_free(char* string);
void list_delete_all_and_self(List* list, void (*)(void*));
char* read_file(const char* path);
void write_file(const char* path, char* string);
