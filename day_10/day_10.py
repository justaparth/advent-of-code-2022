from __future__ import annotations
import unittest


def parse_commands(contents: str) -> list[tuple[str, int]]:
    items = []
    for line in contents.strip().split("\n"):
        parts = line.strip().split(" ")
        if len(parts) == 1:
            items.append((parts[0], 0))
        else:
            items.append((parts[0], int(parts[1])))
    return items


def both_parts(commands: list[tuple[str, int]]) -> int:
    cycle = 1
    x = 1

    # im trying out inner functions...
    # kind of weird but cool i guess too
    def advance_cycle() -> int:
        nonlocal cycle, x

        toreturn = 0
        if cycle in [20, 60, 100, 140, 180, 220]:
            toreturn = cycle * x

        # print out whether the sprite is visible

        # advance every 40th cycle
        if (cycle - 1) % 40 == 0:
            print()
        # print X if the position within 1 of
        # the cycle (mod 40)
        # i'm like 100% sure something is off by one here
        if abs(x - (cycle % 40 - 1)) <= 1:
            print("#", end="")
        else:
            print(".", end="")
        cycle += 1
        return toreturn

    total = 0
    for op, amt in commands:
        if op == "noop":
            total += advance_cycle()
        elif op == "addx":
            total += advance_cycle()
            total += advance_cycle()
            x += amt

    total += advance_cycle()
    return total


def part_2(commands: list[tuple[str, int]]) -> int:
    return -1


def main():
    f = open("day_10_input.txt", "r")
    commands = parse_commands(f.read().strip())
    result_1 = both_parts(commands)
    print(f"part 1: {result_1}")


class Day10Test(unittest.TestCase):
    input = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip()

    def test_part1(self):
        commands = parse_commands(self.input)
        self.assertEqual(13140, both_parts(commands))


if __name__ == "__main__":
    # unittest.main()
    main()
