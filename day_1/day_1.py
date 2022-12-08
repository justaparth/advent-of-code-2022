import unittest


def main():
    f = open("day_1_input.txt", "r")
    # best = part_1(f.read().strip())
    best = part_2(f.read().strip())
    print(best)


def part_1(contents: str) -> int:
    best = -1
    for group in contents.split("\n\n"):
        total = sum([int(x) for x in group.split("\n")])
        if total > best:
            best = total
    return best


def part_2(contents: str) -> int:
    best = []
    for group in contents.split("\n\n"):
        total = sum([int(x) for x in group.split("\n")])
        best.append(total)
    best.sort(reverse=True)
    return sum(best[0:3])


class Day1Test(unittest.TestCase):
    input = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".strip()

    def test_part1(self):
        self.assertEqual(24000, part_1(self.input))

    def test_part2(self):
        self.assertEqual(45000, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
