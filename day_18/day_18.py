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


class Lava:
    shape: set[tuple[int, int, int]]
    maxx: int
    maxy: int
    maxz: int

    def __init__(self, shape: set[tuple[int, int, int]]):
        self.shape = shape
        maxx = -1
        maxy = -1
        maxz = -1

        # figure out bounds of the shape
        for pt in shape:
            maxx = max(maxx, pt[0])
            maxy = max(maxy, pt[1])
            maxz = max(maxz, pt[2])

        self.maxx = maxx
        self.maxy = maxy
        self.maxz = maxz

    def total_surface_area(self) -> int:
        return surface_area(self.shape)

    def in_bounds(self, x: int, y: int, z: int) -> bool:
        return (
            x >= 0
            and x <= self.maxx
            and y >= 0
            and y <= self.maxy
            and z >= 0
            and z <= self.maxz
        )

    def accessible_surface_area(self) -> int:
        base = self.total_surface_area()

        visited: set[tuple[int, int, int]] = set()
        for x in range(0, self.maxx + 1):
            for y in range(0, self.maxy + 1):
                for z in range(0, self.maxz + 1):
                    if (x, y, z) in self.shape:
                        continue

                    # don't re-do calculations unnecessarily
                    if (x, y, z) in visited:
                        continue

                    # do dfs which mutates state jesus
                    amt = self.dfs(x, y, z, visited)
                    print("found to remove ", amt)
                    base -= amt
        return base

    def dfs(
        self,
        sx: int,
        sy: int,
        sz: int,
        visited: set[tuple[int, int, int]],
    ) -> int:

        total = 0

        # bfs into empty point
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

            if (
                x <= 0
                or x >= self.maxx
                or y <= 0
                or y >= self.maxy
                or z <= 0
                or z >= self.maxz
            ):
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
                if not self.in_bounds(c[0], c[1], c[2]):
                    continue
                if c not in self.shape:
                    q.append(c)

        if found_air:
            return 0
        else:
            surf = surface_area(space)
            print(f"surface area of {space} is {surf}")
            return surf


def part_1(contents: str) -> int:
    lines: list[list[int]] = []
    for line in contents.split("\n"):
        lines.append([int(x) for x in line.strip().split(",")])

    shape: set[tuple[int, int, int]] = set()
    for x, y, z in lines:
        shape.add((x, y, z))

    return Lava(shape).total_surface_area()


def part_2(contents: str) -> int:
    lines: list[list[int]] = []
    for line in contents.split("\n"):
        lines.append([int(x) for x in line.strip().split(",")])

    shape: set[tuple[int, int, int]] = set()
    for x, y, z in lines:
        shape.add((x, y, z))
    return Lava(shape).accessible_surface_area()


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
