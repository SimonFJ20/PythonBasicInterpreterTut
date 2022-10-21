#include "dstring.h"
#include "hashmap.h"
#include "panic.h"
#include <stdint.h>
#include <stdio.h>

int main()
{
    int a = 4, b = 7;
    HashMap* map = new_hashmap();
    hashmap_set(map, string_from("a"), &a);
    int* pa = hashmap_get_maybe(map, string_from("a"));
    printf("*pa = %d\n", *pa);
    hashmap_set(map, string_from("b"), &b);
    int* pb = hashmap_get_maybe(map, string_from("b"));
    if (pb == NULL)
        PANIC("pb = NULL");
    printf("*pb = %d\n", *pb);
    hashmap_delete(map, string_from("b"));
    int* pb1 = hashmap_get_maybe(map, string_from("b"));
    printf("pb1 = %p\n", pb1);
    int* pa1 = hashmap_get_maybe(map, string_from("a"));
    printf("pa1 = %p\n", pa1);
}
