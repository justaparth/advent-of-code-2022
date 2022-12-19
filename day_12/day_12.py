from __future__ import annotations
import unittest
from dataclasses import dataclass, field
from queue import PriorityQueue


@dataclass(order=True)
class PRoute:
    length: int
    r: int = field(compare=False)
    c: int = field(compare=False)

    def __init__(self, priority: int, r: int, c: int):
        self.length = priority
        self.r = r
        self.c = c

    def __str__(self):
        return f"[{self.length}] ({self.r},{self.c})"


def parse_matrix(contents: str) -> list[list[str]]:
    return [[x for x in line.strip()] for line in contents.strip().split("\n")]


def part_1(mat: list[list[str]]) -> int:
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            if mat[r][c] == "S":
                return dijkstras(mat, r, c)
    return -1


def part_2(mat: list[list[str]]) -> int:
    min = len(mat) * len(mat[0]) + 1
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            if mat[r][c] == "S" or mat[r][c] == "a":
                path = dijkstras(mat, r, c)
                if path != -1 and path < min:
                    min = path

    return min


def dijkstras(mat: list[list[str]], start_r: int, start_c: int) -> int:
    visited = [[False for x in mat[0]] for y in mat]
    q: PriorityQueue = PriorityQueue()
    q.put(PRoute(0, start_r, start_c))
    while not q.empty():
        next = q.get()
        if visited[next.r][next.c]:
            continue
        visited[next.r][next.c] = True

        r = next.r
        c = next.c

        if mat[r][c] == "E":
            return next.length

        # go all 4 directions
        for rdelta in range(-1, 2, 1):
            for cdelta in range(-1, 2, 1):
                if (rdelta == 0) != (cdelta == 0):
                    newr = r + rdelta
                    newc = c + cdelta
                    if valid(mat, r, c, newr, newc):
                        q.put(PRoute(next.length + 1, newr, newc))

    # this indicates we can't find a path
    # could imagine a grid where `a` is locked behind `z`s or something
    return -1


def valid(mat: list[list[str]], r: int, c: int, newr: int, newc: int) -> bool:
    if not (newr >= 0 and newr < len(mat) and newc >= 0 and newc < len(mat[0])):
        return False

    old = mat[r][c]
    new = mat[newr][newc]

    # start and end are treated as a and z for checking validity
    if old == "S":
        old = "a"
    if new == "E":
        new = "z"

    return ord(new) <= ord(old) + 1


def main():
    with open("day_12_input.txt", "r") as f:
        contents = f.read().strip()
        mat = parse_matrix(contents)
        result_1 = part_1(mat)
        result_2 = part_2(mat)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day12Test(unittest.TestCase):
    input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()

    def test_part1(self):
        mat = parse_matrix(self.input)
        self.assertEqual(31, part_1(mat))

    def test_part2(self):
        mat = parse_matrix(self.input)
        self.assertEqual(29, part_2(mat))


if __name__ == "__main__":
    # unittest.main()
    main()
