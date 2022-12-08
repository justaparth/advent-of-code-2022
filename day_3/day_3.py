import unittest


def main():
    f = open("day_3_input.txt", "r")
    # total = part_1(f.read().strip())
    total = part_2(f.read().strip())
    print(total)


def find_duplicate(rucksack: str) -> str:
    seen = {}
    for i in range(len(rucksack) // 2):
        seen[rucksack[i]] = 1
    for i in range(len(rucksack) // 2, len(rucksack)):
        if rucksack[i] in seen:
            return rucksack[i]
    return "lol"


def score(char: str) -> int:
    code = ord(char)
    if code >= ord("a"):
        return code - ord("a") + 1
    return code - ord("A") + 1 + 26


def part_1(contents: str) -> int:
    total = 0
    for rucksack in contents.split("\n"):
        duplicate = find_duplicate(rucksack)
        code = ord(duplicate)
        if code >= ord("a"):
            total += code - ord("a") + 1
        else:
            total += code - ord("A") + 1 + 26

    return total


def part_2(contents: str) -> int:
    total = 0
    rucksacks = contents.split("\n")
    for i in range(0, len(rucksacks), 3):
        first = {}
        second = {}

        badge = ""

        for char in rucksacks[i]:
            first[char] = 1
        for char in rucksacks[i + 1]:
            second[char] = 1
        for char in rucksacks[i + 2]:
            if char in first and char in second:
                badge = char
                break

        total += score(badge)

    return total


class Day3Test(unittest.TestCase):
    input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()

    def test_part1(self):
        self.assertEqual(157, part_1(self.input))

    def test_part2(self):
        self.assertEqual(70, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
