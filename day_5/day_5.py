import unittest

from typing import Tuple
import re


command_pattern = "move (\d+) from (\d+) to (\d+)"


def main():
    f = open("day_5_input.txt", "r")
    # total = part_1(f.read())
    total = part_2(f.read().strip())
    print(total)


def parse_input(contents: str) -> Tuple[list[str], list[str]]:
    setup_string, command_string = contents.split("\n\n")

    # setup is in part 1
    # hack: get rid of any newlines if they exist at the beginning
    setup_string = setup_string.lstrip("\n")
    setup = []
    first = True
    for line in reversed(setup_string.split("\n")):
        if first:
            first = False
            for i in range(0, len(line), 4):
                setup.append([])

        else:
            for i in range(0, len(line), 4):
                char = line[i + 1 : i + 2]
                if char == " ":
                    continue
                setup[i // 4].append(line[i + 1 : i + 2])

    return (setup, command_string.strip().split("\n"))


def part_1(contents: str) -> str:
    setup, commands = parse_input(contents)
    for command in commands:
        res = re.search(command_pattern, command)
        amount = int(res.group(1))
        source = int(res.group(2)) - 1
        dest = int(res.group(3)) - 1

        for i in range(amount):
            setup[dest].append(setup[source].pop())

    result = ""
    for list in setup:
        if len(list) > 0:
            result += list.pop()
        else:
            result += " "

    return result


def part_2(contents: str) -> str:
    setup, commands = parse_input(contents)
    for command in commands:
        res = re.search(command_pattern, command)
        amount = int(res.group(1))
        source = int(res.group(2)) - 1
        dest = int(res.group(3)) - 1

        temp_stack = []
        for i in range(amount):
            temp_stack.append(setup[source].pop())
        for i in range(amount):
            setup[dest].append(temp_stack.pop())

    result = ""
    for list in setup:
        if len(list) > 0:
            result += list.pop()
        else:
            result += " "

    return result


class Day5Test(unittest.TestCase):
    input = """
    [D]    
[N] [C]    
[Z] [M] [P]
1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

    def test_parse_input(self):
        setup, commands = parse_input(self.input)
        self.assertEqual([["Z", "N"], ["M", "C", "D"], ["P"]], setup)
        self.assertEqual(
            [
                "move 1 from 2 to 1",
                "move 3 from 1 to 3",
                "move 2 from 2 to 1",
                "move 1 from 1 to 2",
            ],
            commands,
        )

    def test_part1(self):
        self.assertEqual("CMZ", part_1(self.input))

    def test_part2(self):
        self.assertEqual("MCD", part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
