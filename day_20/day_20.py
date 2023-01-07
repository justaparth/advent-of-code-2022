from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import unittest
from collections import deque


def wrap(idx: int, elem: int, length: int) -> int:

    if elem == 0:
        return idx

    backwards = False
    if elem < 0:
        backwards = True

    adjustment = abs(elem) % (length - 1)

    for i in range(adjustment):
        if backwards:
            if idx == 0:
                idx = length - 1
            idx -= 1
            if idx == 0:
                idx = length - 1
        else:
            if idx == length - 1:
                idx = 0
            idx += 1
            if idx == length - 1:
                idx = 0

    return idx


def part_1(contents: str) -> int:
    nums = [int(x) for x in contents.replace("\n", " ").strip().split(" ")]
    mixed = nums.copy()

    for elem in nums:
        idx = mixed.index(elem)
        new_idx = wrap(idx, elem, len(mixed))

        # this is so awful
        # first, remove it, then add it back
        mixed = mixed[0:idx] + mixed[idx + 1 :]
        mixed = mixed[0:new_idx] + [elem] + mixed[new_idx:]

    print("state of mixed at the end", mixed)
    idx = mixed.index(0)
    a = mixed[(idx + 1000) % len(mixed)]
    b = mixed[(idx + 2000) % len(mixed)]
    c = mixed[(idx + 3000) % len(mixed)]

    return a + b + c


def part_2(contents: str) -> int:
    return -1


def main():
    with open("day_20_input.txt", "r") as f:
        contents = f.read().strip()
        result_1 = part_1(contents)
        result_2 = part_2(contents)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day20Test(unittest.TestCase):
    input = """
1
2
-3
3
-2
0
4
""".strip()

    # def test_part1(self):
    #     self.assertEqual(3, part_1(self.input))

    # def test_part2(self):
    #     self.assertEqual(58, part_2(self.input))

    def test_wrap(self):
        self.assertEqual(1, wrap(0, 1, 7))
        self.assertEqual(2, wrap(0, 2, 7))
        self.assertEqual(4, wrap(1, -3, 7))

        # test 0
        for i in range(0, 6):
            self.assertEqual(i, wrap(i, 0, 7))

        # test moving negative thing back its exact amount
        for i in range(1, 6):
            self.assertEqual(6, wrap(i, -1 * i, 7))
            self.assertEqual(6, wrap(i, -1 * (i + 6), 7))
            self.assertEqual(6, wrap(i, -1 * (i + 36), 7))


if __name__ == "__main__":
    unittest.main()
    # main()
