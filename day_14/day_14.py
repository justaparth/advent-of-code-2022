from __future__ import annotations
import unittest


class AdjustedMatrix:
    minx: int
    maxx: int
    miny: int
    maxy: int
    mat: dict[tuple[int, int], str]

    def __init__(self, minx: int, miny: int, maxx: int, maxy: int):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.mat = {}

    # def __str__(self) -> str:
    #     buf = []
    #     for r in range(len(self.mat)):
    #         line = ""
    #         for c in range(len(self.mat[r])):
    #             line += self.mat[r][c]
    #         buf.append(line)
    #     return "\n".join(buf)

    def get(self, x: int, y: int) -> str:
        return self.mat.get((x - self.minx, y - self.miny), ".")

    def set(self, x: int, y: int, val: str):
        self.mat[(x - self.minx, y - self.miny)] = val

    def valid(self, x: int, y: int) -> bool:
        newx = x - self.minx
        newy = y - self.miny
        return (
            newx >= 0
            and newy >= 0
            and newx <= self.maxx - self.minx
            and newy <= self.maxy - self.miny
        )


def part_1(contents: str) -> int:
    pathstrings = contents.split("\n")
    paths: list[list[list[int]]] = []

    for path in pathstrings:
        coords: list[list[int]] = [
            [int(y) for y in x.split(",")] for x in path.split(" -> ")
        ]
        paths.append(coords)

    # we have 1 point definitely at 0, 500
    minx = 500
    miny = 0
    maxx = 500
    maxy = 0
    for arr in paths:
        for x, y in arr:
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)

    mat = AdjustedMatrix(minx, miny, maxx, maxy)

    for arr in paths:
        for i in range(len(arr) - 1):
            curr_x, curr_y = arr[i]
            next_x, next_y = arr[i + 1]
            if curr_x == next_x:
                step = 1 if next_y > curr_y else -1
                for y in range(curr_y, next_y + step, step):
                    mat.set(curr_x, y, "#")
            else:
                step = 1 if next_x > curr_x else -1
                for x in range(curr_x, next_x + step, step):
                    mat.set(x, curr_y, "#")

    sand = 0
    abyss = False
    while True:
        # lets simulate sand
        x = 500
        y = 0
        while True:
            if not mat.valid(x, y + 1):
                abyss = True
                break
            elif mat.get(x, y + 1) == ".":
                y += 1
            else:
                # try to go left
                if not mat.valid(x - 1, y + 1):
                    abyss = True
                    break
                elif mat.get(x - 1, y + 1) == ".":
                    x -= 1
                    y += 1
                else:
                    # try to go right
                    if not mat.valid(x + 1, y + 1):
                        abyss = True
                        break
                    elif mat.get(x + 1, y + 1) == ".":
                        x += 1
                        y += 1
                    else:
                        # no movement
                        break
        if abyss:
            break
        mat.set(x, y, "o")
        sand += 1

    print(mat)
    return sand


def part_2(contents: str) -> int:
    pathstrings = contents.split("\n")
    paths: list[list[list[int]]] = []

    for path in pathstrings:
        coords: list[list[int]] = [
            [int(y) for y in x.split(",")] for x in path.split(" -> ")
        ]
        paths.append(coords)

    # we have 1 point definitely at 0, 500
    minx = 500
    miny = 0
    maxx = 500
    maxy = 0
    for arr in paths:
        for x, y in arr:
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)

    mat = AdjustedMatrix(minx, miny, maxx, maxy)
    # we know for sure we have 2 extra rows
    mat.maxy += 2

    for arr in paths:
        for i in range(len(arr) - 1):
            curr_x, curr_y = arr[i]
            next_x, next_y = arr[i + 1]
            if curr_x == next_x:
                step = 1 if next_y > curr_y else -1
                for y in range(curr_y, next_y + step, step):
                    mat.set(curr_x, y, "#")
            else:
                step = 1 if next_x > curr_x else -1
                for x in range(curr_x, next_x + step, step):
                    mat.set(x, curr_y, "#")

    sand = 0
    while True:
        # lets simulate sand
        x = 500
        y = 0
        while True:
            if y + 1 == mat.maxy - mat.miny:
                break
            if mat.get(x, y + 1) == ".":
                y += 1
            elif mat.get(x - 1, y + 1) == ".":
                x -= 1
                y += 1
            elif mat.get(x + 1, y + 1) == ".":
                x += 1
                y += 1
            else:
                break

        if x == 500 and y == 0:
            sand += 1
            break
        sand += 1
        mat.set(x, y, "o")

    print(mat)
    return sand


def main():
    with open("day_14_input.txt", "r") as f:
        contents = f.read().strip()
        result_1 = part_1(contents)
        result_2 = part_2(contents)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day14Test(unittest.TestCase):
    input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

    def test_part1(self):
        self.assertEqual(24, part_1(self.input))

    def test_part2(self):
        self.assertEqual(93, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
