import { assertEquals } from "https://deno.land/std/testing/asserts.ts";

type Pair = {
    key: number;
    value: string;
};

const pair = (key: number, value: string): Pair => ({ key, value });

// const find = (
//     pairs: Pair[],
//     key: number,
//     first: number,
//     last: number,
// ): number => {
//     for (let i = first; i < last; i++) if (pairs[i].key === key) return i;
//     return -1;
// };

const find = (
    pairs: Pair[],
    key: number,
    first: number,
    last: number,
): number => {
    if (pairs.length === 0) return -1;
    const middle = Math.floor((first + last) / 2);
    if (pairs[middle].key === key) return middle;
    else if (first === last) return -1;
    else if (pairs[middle].key > key) return find(pairs, key, first, middle);
    else return find(pairs, key, middle, last);
};

Deno.test("0 elements", () => {
    assertEquals(find([], 0, 0, 0), -1);
});

Deno.test("1 elements", () => {
    assertEquals(find([pair(0, "a")], 0, 0, 1), 0);
});

Deno.test("2 elements", () => {
    assertEquals(find([pair(0, "a"), pair(1, "b")], 0, 0, 2), 0);
    assertEquals(find([pair(0, "a"), pair(1, "b")], 1, 0, 2), 1);
});

Deno.test("3 elements", () => {
    assertEquals(find([pair(0, "a"), pair(1, "b"), pair(2, "c")], 0, 0, 3), 0);
    assertEquals(find([pair(0, "a"), pair(1, "b"), pair(2, "c")], 1, 0, 3), 1);
    assertEquals(find([pair(0, "a"), pair(1, "b"), pair(2, "c")], 2, 0, 3), 2);
});

Deno.test("4 elements", () => {
    assertEquals(
        find([pair(0, "a"), pair(1, "b"), pair(2, "c"), pair(3, "d")], 0, 0, 4),
        0,
    );
    assertEquals(
        find([pair(0, "a"), pair(1, "b"), pair(2, "c"), pair(3, "d")], 1, 0, 4),
        1,
    );
    assertEquals(
        find([pair(0, "a"), pair(1, "b"), pair(2, "c"), pair(3, "d")], 2, 0, 4),
        2,
    );
    assertEquals(
        find([pair(0, "a"), pair(1, "b"), pair(2, "c"), pair(3, "d")], 3, 0, 4),
        3,
    );
});
