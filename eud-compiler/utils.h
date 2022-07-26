#ifndef UTILS_H
#define UTILS_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    void** values;
    size_t length;
} List;

List* new_list();
void delete_list(List* self);

void list_add(List* self, void* value);
void* list_at(List* self, int index);
void* list_remove_at(List* self, int index);
int list_remove(List* self, void* value);
size_t list_length(List* self);
void** list_to_array(List* self);

typedef struct LinkedListNodeStruct {
    struct LinkedListNodeStruct* prev;
    struct LinkedListNodeStruct* next;
    void* value;
} LinkedListNode;

LinkedListNode* new_linked_list_node(LinkedListNode* prev, LinkedListNode* next, void* value);
void delete_linked_list_node(LinkedListNode* self);

void linked_list_node_short_circuit_child_and_parent(LinkedListNode* self);

typedef struct {
    LinkedListNode* head;
    size_t length;
} LinkedList;

LinkedList* new_linked_list();
void delete_linked_list();

void linked_list_add(LinkedList* self, void* value);
LinkedListNode* linked_list_node_at(LinkedList* self, int index);
void* linked_list_at(LinkedList* self, int index);
void linked_list_delete_node(LinkedList* self, LinkedListNode* node, bool is_head);
void* linked_list_remove_at(LinkedList* self, int index);
int linked_list_remove(LinkedList* self, void* value);
size_t linked_list_length(LinkedList* self);
void** linked_list_to_array(LinkedList* self);

typedef struct ReaderStruct {
    char (*getc)(struct ReaderStruct* self);
    void (*delete)(struct ReaderStruct* self);
} Reader;

typedef struct FileReaderStruct {
    char (*getc)(struct FileReaderStruct* self);
    void (*delete)(struct FileReaderStruct* self);
    FILE* fp;
} FileReader;

FileReader* new_file_reader(FILE* fp);
void delete_file_reader(FileReader* self);

char file_reader_getc(FileReader* self);

#endif
