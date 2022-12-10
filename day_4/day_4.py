import unittest


def main():
    f = open("day_4_input.txt", "r")
    # total = part_1(f.read().strip())
    total = part_2(f.read().strip())
    print(total)


def fully_overlap(a: int, b: int, x: int, y: int) -> bool:
    return a <= x and b >= y or x <= a and y >= b


def overlap(a: int, b: int, x: int, y: int) -> bool:
    return a <= x <= b or x <= a <= y


def part_1(contents: str) -> int:
    total = 0
    for line in contents.split("\n"):
        first, second = line.split(",")
        a, b = [int(x) for x in first.split("-")]
        x, y = [int(x) for x in second.split("-")]
        if fully_overlap(a, b, x, y):
            total += 1

    return total


def part_2(contents: str) -> int:
    total = 0
    for line in contents.split("\n"):
        first, second = line.split(",")
        a, b = [int(x) for x in first.split("-")]
        x, y = [int(x) for x in second.split("-")]
        print(a, b, x, y)
        if overlap(a, b, x, y):
            total += 1

    return total


class Day4Test(unittest.TestCase):
    input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()

    def test_part1(self):
        self.assertEqual(2, part_1(self.input))

    def test_overlap(self):
        # no overlap
        self.assertEqual(False, fully_overlap(1, 2, 3, 4))
        self.assertEqual(False, fully_overlap(1, 10, 2, 11))
        self.assertEqual(False, fully_overlap(8, 17, 16, 49))

        # full overlap
        self.assertEqual(True, fully_overlap(1, 2, 1, 2))
        self.assertEqual(True, fully_overlap(1, 10, 2, 5))
        self.assertEqual(True, fully_overlap(1, 99, 1, 1))

    def test_part2(self):
        self.assertEqual(4, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
