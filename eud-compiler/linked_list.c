#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#include "utils.h"

LinkedListNode* new_linked_list_node(LinkedListNode* prev, LinkedListNode* next, void* value)
{
    LinkedListNode* self = calloc(1, sizeof (LinkedListNode));
    *self = (LinkedListNode) {
        .prev = prev,
        .next = next,
        .value = value,
    };
    return self;
}

void delete_linked_list_node(LinkedListNode* self)
{
    free(self);
}

void linked_list_node_short_circuit_child_and_parent(LinkedListNode* self)
{
    assert(self->prev);
    self->prev->next = self->next;
    if (self->next)
        self->next->prev = self->prev;
}

LinkedList* new_linked_list()
{
    LinkedList* self = calloc(1, sizeof (LinkedList));
    *self = (LinkedList) {
        .head = NULL,
        .length = 0,
    };
    return self;
}

void linked_list_add(LinkedList* self, void* value)
{
    self->length++;
    if (self->head == NULL) {
        self->head = new_linked_list_node(NULL, NULL, value);
    } else {
        LinkedListNode* node = self->head;
        while (node->next)
            node = node->next;
        node->next = new_linked_list_node(node, NULL, value);
    }
}

LinkedListNode* linked_list_node_at(LinkedList* self, int index)
{
    if (index >= 0) {
        assert(index < self->length);
        LinkedListNode* node = self->head;
        for (int i = 0; i < index; i++)
            node = node->next;
        return node;
    } else {
        return linked_list_at(self, self->length - index);
    }
}

void* linked_list_at(LinkedList* self, int index)
{
    return linked_list_node_at(self, index)->value;
}

void linked_list_delete_node(LinkedList* self, LinkedListNode* node, bool is_head)
{
    node->next->prev = NULL;
    if (is_head)
        self->head = node->next;
    else
        linked_list_node_short_circuit_child_and_parent(node);
    delete_linked_list_node(node);
}

void* linked_list_remove_at(LinkedList* self, int index)
{
    assert(index < self->length);
    LinkedListNode* node = index == 0 ? self->head : linked_list_node_at(self, index);
    void* value = node->value;
    linked_list_delete_node(self, node, index == 0);
    self->length--;
    return value;
}

int linked_list_remove(LinkedList* self, void* value)
{
    int removed = 0;
    LinkedListNode* node = self->head;
    while (node) {
        if (node->value == value) {
            linked_list_delete_node(self, node, node == self->head);
            removed++;
        }
        node = node->next;
    }
    return removed;
}

size_t linked_list_length(LinkedList* self)
{
    return self->length;
}

void** linked_list_to_array(LinkedList* self)
{
    void** array = calloc(self->length, sizeof (void*));
    int i = 0;
    for (LinkedListNode* node = self->head; node; node = node->next)
        array[i++] = node->value;
    return array;
}

