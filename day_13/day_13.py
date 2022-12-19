from __future__ import annotations
import unittest
from dataclasses import dataclass
from functools import cmp_to_key


@dataclass
class Pair:
    left: str
    right: str

    def __str__(self) -> str:
        return f"{self.left}\n{self.right}"


@dataclass
class SignalList:
    elements: list[SignalList | int]

    # todo: clean this up
    def lessthan(self, other: SignalList) -> bool:
        i = 0
        while i < len(self.elements) and i < len(other.elements):
            left = self.elements[i]
            right = other.elements[i]

            if isinstance(left, int) and isinstance(right, int):
                # base case of 2 ints
                if left < right:
                    return True
                elif left > right:
                    return False
            else:
                # otherwise, coerce types and go forward
                if isinstance(left, int):
                    left = SignalList([left])
                if isinstance(right, int):
                    right = SignalList([right])
                if left.lessthan(right):
                    return True
                elif right.lessthan(left):
                    return False

            i += 1

        # if we get here, we should have processed everything in 1 list.
        # the left list must be less than the right one
        return len(self.elements) < len(other.elements)

    def __str__(self) -> str:
        parts = []
        for elem in self.elements:
            if isinstance(elem, int):
                parts.append(str(elem))
            else:
                parts.append(elem.__str__())
        return "[" + ",".join(parts) + "]"

    def __repr__(self) -> str:
        return str(self)


def parse_pairs(contents: str) -> list[Pair]:
    items: list[Pair] = []
    pairs = contents.split("\n\n")
    for pair in pairs:
        parts = pair.split("\n")
        items.append(Pair(parts[0].strip(), parts[1].strip()))

    return items


def part_1(pairs: list[Pair]) -> int:
    total = 0
    for i, pair in enumerate(pairs):
        left = make_list(pair.left)
        right = make_list(pair.right)
        if left.lessthan(right):
            total += i + 1

    return total


def part_2(pairs: list[Pair]) -> int:
    all: list[SignalList] = []

    marker2 = make_list("[[2]]")
    marker6 = make_list("[[6]]")

    for pair in pairs:
        all.append(make_list(pair.left))
        all.append(make_list(pair.right))
    all.append(marker2)
    all.append(marker6)

    def cmp(left: SignalList, right: SignalList) -> int:
        if left.lessthan(right):
            return -1
        elif right.lessthan(left):
            return 1
        return 0

    sortedlist = sorted(all, key=cmp_to_key(cmp))

    total = 1
    for i, item in enumerate(sortedlist):
        print(item)
        if item == marker2:
            total *= i + 1
        elif item == marker6:
            total *= i + 1
    return total


def make_list(thing: str) -> SignalList:
    # in this, we need to have a stack len of 1 and see a comma
    # for a split to happen
    parts = SignalList([])
    prev = 0
    stack = 1
    i = 1

    # HACK:
    if thing == "[]":
        return parts

    while i < len(thing) - 1:
        if stack == 1 and thing[i] == ",":
            to_add = thing[prev + 1 : i]
            if to_add.startswith("["):
                parts.elements.append(make_list(to_add))
            else:
                parts.elements.append(int(to_add))
            prev = i
        elif thing[i] == "[":
            stack += 1
        elif thing[i] == "]":
            stack -= 1
        i += 1

    to_add = thing[prev + 1 : len(thing) - 1]
    if to_add.startswith("["):
        parts.elements.append(make_list(to_add))
    else:
        parts.elements.append(int(to_add))
    return parts


def main():
    with open("day_13_input.txt", "r") as f:
        contents = f.read().strip()
        pairs = parse_pairs(contents)
        result_1 = part_1(pairs)
        result_2 = part_2(pairs)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day12Test(unittest.TestCase):
    input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

    def test_part1(self):
        pairs = parse_pairs(self.input)
        self.assertEqual(13, part_1(pairs))

    def test_part2(self):
        pairs = parse_pairs(self.input)
        self.assertEqual(140, part_2(pairs))

    def test_make_list(self):
        self.assertEqual(SignalList([]), make_list("[]"))
        self.assertEqual(SignalList([1, 1, 31, 1]), make_list("[1,1,31,1]"))
        self.assertEqual(SignalList([1, 1, 31, 1]), make_list("[1,1,31,1]"))
        self.assertEqual(
            SignalList([1, SignalList([1, 2]), SignalList([1]), 2]),
            make_list("[1,[1,2],[1],2]"),
        )

    def test_less_than(self):
        a = make_list("[[6],[8,3]]")
        b = make_list("[[6]]")
        self.assertTrue(a.lessthan(b))


if __name__ == "__main__":
    # unittest.main()
    main()
