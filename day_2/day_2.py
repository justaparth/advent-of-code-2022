import unittest

# x = rock, y = paper, z = scissors
scores = {"X": 0, "Y": 1, "Z": 2}
opponent_map = {"A": "X", "B": "Y", "C": "Z"}
order = ["X", "Y", "Z"]


def main():
    f = open("day_2_input.txt", "r")
    # best = part_1(f.read().strip())
    best = part_2(f.read().strip())
    print(best)


def score(opponent: str, us: str) -> int:
    total = 0
    if opponent == us:
        total += 3
    elif (
        opponent == "X"
        and us == "Y"
        or opponent == "Y"
        and us == "Z"
        or opponent == "Z"
        and us == "X"
    ):
        total += 6

    total += scores[us] + 1
    return total


def part_1(contents: str) -> int:
    total = 0
    for row in contents.split("\n"):
        parts = row.strip().split(" ")
        opponent = opponent_map[parts[0]]
        us = parts[1]
        total += score(opponent, us)

    return total


def part_2(contents: str) -> int:
    total = 0
    for row in contents.split("\n"):
        parts = row.strip().split(" ")
        opponent = opponent_map[parts[0]]
        idx = scores[opponent]
        result = parts[1]

        us = "X"
        if result == "X":
            us = order[(idx + 2) % 3]
        elif result == "Y":
            us = opponent
        else:
            us = order[(idx + 1) % 3]

        total += score(opponent, us)

    return total


class Day2Test(unittest.TestCase):
    input = """
A Y
B X
C Z
""".strip()

    def test_part1(self):
        self.assertEqual(15, part_1(self.input))

    def test_part2(self):
        self.assertEqual(12, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
