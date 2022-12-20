from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import unittest
from collections import deque


def surface_area(shape: set[tuple[int, int, int]]) -> int:
    maxx = -1
    maxy = -1
    maxz = -1

    # figure out bounds of the shape
    for pt in shape:
        maxx = max(maxx, pt[0])
        maxy = max(maxy, pt[1])
        maxz = max(maxz, pt[2])

    total = 0
    for x in range(0, maxx + 1):
        for y in range(0, maxy + 1):
            for z in range(0, maxz + 1):
                if (x, y, z) not in shape:
                    continue

                # look every direction
                candidates = [
                    (x, y, z + 1),
                    (x, y, z - 1),
                    (x, y + 1, z),
                    (x, y - 1, z),
                    (x + 1, y, z),
                    (x - 1, y, z),
                ]
                for c in candidates:
                    if c not in shape:
                        total += 1

    return total


# class Lava:
#     shape: set[tuple[int, int, int]]
#     maxx: int
#     maxy: int
#     maxz: int

#     def __init__(self, shape: set[tuple[int, int, int]]):
#         self.shape = shape
#         maxx = -1
#         maxy = -1
#         maxz = -1

#         # figure out bounds of the shape
#         for pt in shape:
#             maxx = max(maxx, pt[0])
#             maxy = max(maxy, pt[1])
#             maxz = max(maxz, pt[2])

#         self.maxx = maxx
#         self.maxy = maxy
#         self.maxz = maxz


def part_1(contents: str) -> int:
    lines: list[list[int]] = []
    for line in contents.split("\n"):
        lines.append([int(x) for x in line.strip().split(",")])

    shape: set[tuple[int, int, int]] = set()
    for x, y, z in lines:
        shape.add((x, y, z))

    return surface_area(shape)


def part_2(contents: str) -> int:
    lines: list[list[int]] = []
    for line in contents.split("\n"):
        lines.append([int(x) for x in line.strip().split(",")])

    shape: set[tuple[int, int, int]] = set()
    for x, y, z in lines:
        shape.add((x, y, z))
    total = surface_area(shape)

    maxx = -1
    maxy = -1
    maxz = -1

    # figure out bounds of the shape
    for pt in shape:
        maxx = max(maxx, pt[0])
        maxy = max(maxy, pt[1])
        maxz = max(maxz, pt[2])

    # adjust for empty pockets
    visited: set[tuple[int, int, int]] = set()
    for x in range(0, maxx + 1):
        for y in range(0, maxy + 1):
            for z in range(0, maxz + 1):
                if (x, y, z) in shape:
                    continue

                # don't re-do calculations unnecessarily
                if (x, y, z) in visited:
                    continue

                # do dfs which mutates state jesus
                amt = dfs(x, y, z, maxx, maxy, maxz, shape, visited)
                print("found ", amt)
                total -= amt

    return total


def dfs(
    sx: int,
    sy: int,
    sz: int,
    maxx: int,
    maxy: int,
    maxz: int,
    shape: set[tuple[int, int, int]],
    visited: set[tuple[int, int, int]],
) -> int:

    total = 0

    # we found an empty point
    # now, let's bfs
    space: set[tuple[int, int, int]] = set()
    found_air = False
    q = deque([(sx, sy, sz)])
    while len(q) != 0:
        # get next
        elem = q.popleft()
        x, y, z = elem

        # skip seen elements
        if elem in visited:
            continue

        # add to current shape and also leave off visited
        space.add(elem)
        visited.add(elem)

        if x <= 0 or x >= maxx or y <= 0 or y >= maxy or z <= 0 or z >= maxz:
            found_air = True

        # look every direction we can
        candidates = [
            (x, y, z + 1),
            (x, y, z - 1),
            (x, y + 1, z),
            (x, y - 1, z),
            (x + 1, y, z),
            (x - 1, y, z),
        ]

        for c in candidates:
            if (
                c[0] < 0
                or c[0] > maxx
                or c[1] < 0
                or c[1] > maxy
                or c[2] < 0
                or c[2] > maxz
            ):
                continue
            if c not in shape:
                q.append(c)

    if found_air:
        return 0
    else:
        surf = surface_area(space)
        print(f"surface area of {space} is {surf}")
        return surf


def main():
    with open("day_18_input.txt", "r") as f:
        contents = f.read().strip()
        result_1 = part_1(contents)
        result_2 = part_2(contents)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day18Test(unittest.TestCase):
    input = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip()

    def test_part1(self):
        self.assertEqual(64, part_1(self.input))

    def test_part2(self):
        self.assertEqual(58, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
