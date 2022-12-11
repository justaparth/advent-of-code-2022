import unittest


def main():
    f = open("day_6_input.txt", "r")
    # total = part_1(f.read().strip())
    total = part_2(f.read().strip())
    print(total)


def part_1(line: str) -> int:
    return gen(line, 4)


def part_2(line: str) -> int:
    return gen(line, 14)


def gen(line: str, sequence_length: int) -> int:
    charset = {}

    # initialize
    if len(line) < sequence_length:
        return -1

    i = 0
    while i < sequence_length:
        charset[line[i]] = charset.get(line[i], 0) + 1
        i += 1

    if check(charset):
        return 4

    while i < len(line):
        charset[line[i]] = charset.get(line[i], 0) + 1
        charset[line[i - sequence_length]] = (
            charset.get(line[i - sequence_length], 1) - 1
        )
        if check(charset):
            return i + 1
        i += 1


def check(charset: dict) -> bool:
    for key, val in charset.items():
        if val > 1:
            return False

    return True


class Day6Test(unittest.TestCase):
    inputs = [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
    ]

    part1_results = [7, 5, 6, 10, 11]
    part2_results = [19, 23, 23, 29, 26]

    def test_part1(self):
        for i in range(len(self.inputs)):
            with self.subTest(i):
                self.assertEqual(self.part1_results[i], part_1(self.inputs[i]))

    def test_part2(self):
        for i in range(len(self.inputs)):
            with self.subTest(i):
                self.assertEqual(self.part2_results[i], part_2(self.inputs[i]))


if __name__ == "__main__":
    # unittest.main()
    main()
