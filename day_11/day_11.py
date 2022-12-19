from __future__ import annotations
import unittest
from enum import Enum
import re
from collections import deque
import math
from typing import Generator


class Monkey:
    def __init__(
        self,
        items: list[int],
        op: str,
        test: int,
        true_monkey: int,
        false_monkey: int,
    ):
        self.items = deque(items)
        self.op = op
        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

    # TODO: not sure how to do types for generator functions
    # return worry, and value to pass
    def pass_to_monkey(self, lcm: int, should_divide: bool):
        for i in range(len(self.items)):
            item = self.items.popleft()

            worry = self.evaluate_item(item, lcm, should_divide)
            if worry % self.test == 0:
                yield (worry, self.true_monkey)
            else:
                yield (worry, self.false_monkey)

    # its possible the operation balloons the value. we don't need
    # the true value, we just need it % the lcm of all the test values
    # of all the monkeys, since they'll all end up checking mod anyways
    # we're taking advantage of rule that
    # a * b (mod c) = (a%c) * (b%c) (mod c)
    # same with addition
    def evaluate_item(self, item: int, lcm: int, should_divide: bool) -> int:
        left, mid, right = self.op.split(" ")

        l = item % lcm
        if not "old" in left:
            l = int(left) % lcm

        r = item % lcm
        if not "old" in right:
            l = int(right) % lcm

        worry = l + r
        if mid == "*":
            worry = l * r

        if should_divide:
            worry = worry // (3 % lcm)

        return worry % lcm


def parse_monkeys(contents: str) -> list[Monkey]:
    # assume monkeys are provided in order
    monkeys: list[Monkey] = []
    specs = contents.split("\n\n")
    for spec in specs:
        lines = [x.strip() for x in spec.strip().split("\n")]
        if len(lines) != 6:
            raise Exception("bro")

        # we can do this without regex, but i want to practice writing them
        itemstr = help_regex("Starting items:\s*([\d\s,]+)", lines[1])
        items = [int(x) for x in re.split(",?\s", itemstr)]
        opstr = help_regex("Operation: new = (.*)", lines[2])
        testdivis = int(help_regex("Test: divisible by (\d+)", lines[3]))
        true_monkey = int(help_regex("If true: throw to monkey (\d+)", lines[4]))
        false_monkey = int(help_regex("If false: throw to monkey (\d+)", lines[5]))

        monkeys.append(Monkey(items, opstr, testdivis, true_monkey, false_monkey))

    return monkeys


def help_regex(regex: str, target: str) -> str:
    result = re.search(regex, target)
    if result is None:
        raise Exception
    return result.group(1)


def solve(monkeys: list[Monkey], rounds: int, should_divide: bool) -> int:
    lcm = math.lcm(*[x.test for x in monkeys])
    inspections = [0 for i in range(len(monkeys))]
    for round in range(rounds):
        for monkey_num, monkey in enumerate(monkeys):
            for worry, dest in monkey.pass_to_monkey(lcm, should_divide):
                inspections[monkey_num] += 1
                monkeys[dest].items.append(worry)

    # theres a better way to find top 2, i'll look up after
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def part_1(monkeys: list[Monkey]) -> int:
    return solve(monkeys, 20, True)


def part_2(monkeys: list[Monkey]) -> int:
    return solve(monkeys, 10000, False)


def main():
    with open("day_11_input.txt", "r") as f:
        monkeys = parse_monkeys(f.read().strip())
        result_1 = part_1(monkeys)
        print(f"part 1: {result_1}")
    with open("day_11_input.txt", "r") as f:
        monkeys = parse_monkeys(f.read().strip())
        result_2 = part_2(monkeys)
        print(f"part 2: {result_2}")


class Day11Test(unittest.TestCase):
    input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()

    def test_part1(self):
        monkeys = parse_monkeys(self.input)
        self.assertEqual(10605, part_1(monkeys))

    def test_part2(self):
        monkeys = parse_monkeys(self.input)
        self.assertEqual(2713310158, part_2(monkeys))


if __name__ == "__main__":
    # unittest.main()
    main()
