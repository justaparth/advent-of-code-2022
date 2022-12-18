from __future__ import annotations
import unittest


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def move_toward(self, other: Point):
        # if they're touching, we're done.
        if abs(self.y - other.y) <= 1 and abs(self.x - other.x) <= 1:
            return

        # if they're on the same row or col, advance
        # one in the direction of the other one.
        # note: i think we can do this with less comparisons?
        if self.x == other.x:
            self.y = self.y + direction(self.y, other.y)
        elif self.y == other.y:
            self.x = self.x + direction(self.x, other.x)
        # otherwise, move diagonally towards the head
        else:
            self.y = self.y + direction(self.y, other.y)
            self.x = self.x + direction(self.x, other.x)


def direction(start: int, end: int) -> int:
    if end > start:
        return 1
    return -1


def parse_commands(contents: str) -> list[tuple[str, int]]:
    items = []
    for line in contents.strip().split("\n"):
        op, amt = line.strip().split(" ")
        items.append((op, int(amt)))
    return items


def rope_snake(commands: list[tuple[str, int]], length: int) -> int:
    knots: list[Point] = []
    for i in range(length):
        knots.append(Point())
    visited = {"X0Y0": ""}

    # convenience ptrs to head and tail
    head = knots[0]
    tail = knots[-1]
    for op, times in commands:
        for time in range(times):
            if op == "U":
                head.y += 1
            elif op == "D":
                head.y -= 1
            elif op == "L":
                head.x -= 1
            elif op == "R":
                head.x += 1

            for i in range(1, len(knots)):
                knots[i].move_toward(knots[i - 1])
            visited[f"X{tail.x}Y{tail.y}"] = ""

    return len(visited)


def part_1(commands: list[tuple[str, int]]) -> int:
    return rope_snake(commands, 2)


def part_2(commands: list[tuple[str, int]]) -> int:
    return rope_snake(commands, 10)


def main():
    f = open("day_9_input.txt", "r")
    commands = parse_commands(f.read().strip())
    result_1 = part_1(commands)
    result_2 = part_2(commands)
    print(f"part 1: {result_1}")
    print(f"part 2: {result_2}")


class Day9Test(unittest.TestCase):
    input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip()

    input2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

    def test_part1(self):
        commands = parse_commands(self.input)
        self.assertEqual(13, part_1(commands))

    def test_part2(self):
        commands = parse_commands(self.input)
        self.assertEqual(1, part_2(commands))
        commands = parse_commands(self.input2)
        self.assertEqual(36, part_2(commands))


if __name__ == "__main__":
    # unittest.main()
    main()
