from __future__ import annotations
import unittest


class VisibleTrees:
    def __init__(self):
        self.top = 0
        self.left = 0
        self.right = 0
        self.down = 0

    def total(self):
        return self.top * self.right * self.down * self.left


def main():
    f = open("day_8_input.txt", "r")
    mat = parse_matrix(f.read().strip())
    # result = part_1(mat)
    result = part_2(mat)
    print(result)


def parse_matrix(contents: str) -> list[list[int]]:
    return [[int(x) for x in list(line.strip())] for line in contents.split("\n")]


# kind of basic, just computes for each tree if it can be seen from any direction
# we touch every row 4 times which isn't ideal but i am not sure how to reduce
def part_1(mat: list[list[int]]) -> int:
    visible = [[False for c in range(len(mat[0]))] for r in range(len(mat))]

    # horizontal
    for r in range(len(mat)):
        max = -1
        for c in range(len(mat[r])):
            if mat[r][c] > max:
                visible[r][c] = True
            if mat[r][c] > max:
                max = mat[r][c]

        max = -1
        for c in range(len(mat[r]) - 1, -1, -1):
            if mat[r][c] > max:
                visible[r][c] = True
            if mat[r][c] > max:
                max = mat[r][c]

    # vertical
    for c in range(len(mat[0])):
        max = -1
        for r in range(len(mat)):
            if mat[r][c] > max:
                visible[r][c] = True
            if mat[r][c] > max:
                max = mat[r][c]

        max = -1
        for r in range(len(mat) - 1, -1, -1):
            if mat[r][c] > max:
                visible[r][c] = True
            if mat[r][c] > max:
                max = mat[r][c]

    total = 0
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            if visible[r][c]:
                total += 1

    print(visible)
    return total


# dumbest way possible.
# i'm trying to think of a better way but having trouble, so will come back.
# dp approach seems hard or seem like it won't change big o
# (e.g. keep track of visibility in each direction at each tree, but that is
# still maybe not that different...)
def part_2(mat: list[list[int]]) -> int:
    max = 1
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            # now we search in every direction
            val = compute_visibility(mat, r, c)
            if val > max:
                print(r, c, val)
                max = val
    return max


def compute_visibility(mat: list[list[int]], start_r: int, start_c: int) -> int:
    if (
        start_r == 0
        or start_r == len(mat) - 1
        or start_c == 0
        or start_c == len(mat[start_r]) - 1
    ):
        return 0

    pos = mat[start_r][start_c]
    total = 1

    # up
    r = start_r - 1
    while r > 0 and mat[r][start_c] < pos:
        r -= 1
    total *= start_r - r

    # down
    r = start_r + 1
    while r < len(mat) - 1 and mat[r][start_c] < pos:
        r += 1
    total *= r - start_r

    # left
    c = start_c - 1
    while c > 0 and mat[start_r][c] < pos:
        c -= 1
    total *= start_c - c

    # right
    c = start_c + 1
    while c < len(mat[start_r]) - 1 and mat[start_r][c] < pos:
        c += 1
    total *= c - start_c

    return total


class Day8Test(unittest.TestCase):
    input = """
30373
25512
65332
33549
35390
""".strip()

    def test_part1(self):
        mat = parse_matrix(self.input)
        self.assertEqual(21, part_1(mat))

    def test_part2(self):
        mat = parse_matrix(self.input)
        self.assertEqual(8, part_2(mat))


if __name__ == "__main__":
    # unittest.main()
    main()
