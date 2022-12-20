from __future__ import annotations
from enum import IntEnum
import unittest
from dataclasses import dataclass
import re
from typing import Optional

NUM_REGEX = "([+-]?\d+)"


def mdist(x: int, y: int, x2: int, y2: int) -> int:
    return abs(x - x2) + abs(y - y2)


@dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int
    exclusion_dist: int

    def __init__(self, x: int, y: int, beacon_x: int, beacon_y: int):
        self.x = x
        self.y = y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y

        dist = mdist(x, y, beacon_x, beacon_y)
        self.exclusion_dist = dist

    def within_zone(self, x: int, y: int) -> bool:
        return mdist(self.x, self.y, x, y) <= self.exclusion_dist

    def exclusion_zone_on_line(self, y: int) -> Optional[tuple[int, int]]:
        # whats the min and max x values?
        maximum_x_delta = self.exclusion_dist - abs(self.y - y)
        if maximum_x_delta < 0:
            return None
        return self.x - maximum_x_delta, self.x + maximum_x_delta


class RangeType(IntEnum):
    START = 1
    END = 2


class LineRanges:
    elems: list[tuple[int, RangeType]]

    def __init__(self, sensors: list[Sensor], y: int):
        elems = []
        for sensor in sensors:
            res = sensor.exclusion_zone_on_line(y)
            if res is not None:
                elems.append((res[0], RangeType.START))
                elems.append((res[1], RangeType.END))
        elems.sort()
        self.elems = elems

    def interval_covered(self) -> tuple[int, int]:
        return self.elems[0][0], self.elems[-1][0]

    def find_gap(self) -> list[tuple[int, int]]:
        open_ranges: list[tuple[int, int]] = []
        if len(self.elems) == 0:
            return open_ranges

        open_stack = [self.elems[0][0]]
        prev_end = self.elems[0][0]

        for p in self.elems[1:]:
            val, type = p
            if type == RangeType.END:
                open_stack.pop()
                prev_end = val
            else:
                # if we are starting a new interval with no
                # existing open interval, check if the interval
                # starts where the last one left off.
                # if not, we know where the opening is
                if len(open_stack) == 0:
                    if val > prev_end + 1:
                        open_ranges.append((prev_end + 1, val - 1))
                open_stack.append(val)

        return open_ranges


def parse_lines(contents: str) -> list[Sensor]:
    sensors = []
    for line in contents.split("\n"):
        result = re.match(
            f"Sensor at x={NUM_REGEX}, y={NUM_REGEX}: closest beacon is at x={NUM_REGEX}, y={NUM_REGEX}",
            line,
        )
        if result is None:
            raise Exception("shouldn't happen")
        x, y, beacon_x, beacon_y = [int(x) for x in result.groups()]
        sensors.append(Sensor(x, y, beacon_x, beacon_y))

    return sensors


def part_1(sensors: list[Sensor], line_to_check: int) -> int:
    line = LineRanges(sensors, line_to_check)
    open_ranges = line.find_gap()
    start, end = line.interval_covered()
    print(open_ranges, start, end)

    count = end - start
    for range in open_ranges:
        count -= range[1] - range[0]

    return count


def part_2(sensors: list[Sensor], min_pos: int, max_pos: int) -> int:
    for y in range(min_pos, max_pos + 1):
        line = LineRanges(sensors, y)
        open_ranges = line.find_gap()
        if len(open_ranges) > 0:
            # we know by the problem statement there should be exactly one range
            print(open_ranges)
            return open_ranges[0][0] * 4000000 + y

    return -1


def main():
    with open("day_15_input.txt", "r") as f:
        contents = f.read().strip()
        lines = parse_lines(contents)
        result_1 = part_1(lines, 2000000)
        result_2 = part_2(lines, 0, 4000000)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day15Test(unittest.TestCase):
    input = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()

    def test_part1(self):
        lines = parse_lines(self.input)
        self.assertEqual(26, part_1(lines, 10))

    def test_part2(self):
        lines = parse_lines(self.input)
        self.assertEqual(56000011, part_2(lines, 0, 20))


if __name__ == "__main__":
    # unittest.main()
    main()
