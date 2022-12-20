from __future__ import annotations
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
    exclusion_zone: Box

    def __init__(self, x: int, y: int, beacon_x: int, beacon_y: int):
        self.x = x
        self.y = y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y

        dist = mdist(x, y, beacon_x, beacon_y)
        self.exclusion_dist = dist
        self.exclusion_zone = Box(x - dist, y - dist, x + dist, y + dist)

    def within_zone(self, x: int, y: int) -> bool:
        return mdist(self.x, self.y, x, y) <= self.exclusion_dist

    def exclusion_zone_on_line(self, y: int) -> Optional[tuple[int, int]]:
        # whats the min and max x values?
        maximum_x_delta = self.exclusion_dist - abs(self.y - y)
        if maximum_x_delta < 0:
            return None
        return self.x - maximum_x_delta, self.x + maximum_x_delta


@dataclass
class Box:
    minx: int
    miny: int
    maxx: int
    maxy: int

    def union(a: Box, b: Box) -> Box:
        return Box(
            min(a.minx, b.minx),
            min(a.miny, b.miny),
            max(a.maxx, b.maxx),
            max(a.maxy, b.maxy),
        )


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
    # first, figure out the maximum zone where things could be excluded
    exclusion_zone = Box(0, 0, 0, 0)
    for sensor in sensors:
        exclusion_zone = Box.union(exclusion_zone, sensor.exclusion_zone)

    # next, construct a list of all existing beacons
    beacons = set()
    for sensor in sensors:
        beacons.add((sensor.beacon_x, sensor.beacon_y))
    print("maximum exclusion zone", exclusion_zone)

    # now, lets check the possible exclusion zone, accounting
    # for places where there are already beacons as well
    # i think this is checking _way_ more than it needs to.
    # for each sensor, once the point gets further away we should stop checking it but
    # i don't wanna do that right now
    count = 0
    for x in range(exclusion_zone.minx, exclusion_zone.maxx + 1):
        # if its a beacon, continue
        if (x, line_to_check) in beacons:
            continue

        # otherwise, if its blocked by any sensor then count it
        for sensor in sensors:
            if sensor.within_zone(x, line_to_check):
                count += 1
                break

    return count


START = 1
END = 2


@dataclass(order=True)
class Point:
    val: int
    type: int

    def __str__(self) -> str:
        if self.type == START:
            return f"S{self.val}"
        else:
            return f"E{self.val}"

    def __repr__(self) -> str:
        return str(self)


def part_2(sensors: list[Sensor], min_pos: int, max_pos: int) -> int:
    # first, figure out the maximum zone where things could be excluded
    exclusion_zone = Box(min_pos, min_pos, max_pos, max_pos)

    # next, construct a list of all existing beacons
    beacons = set()
    for sensor in sensors:
        beacons.add(f"X{sensor.beacon_x}Y{sensor.beacon_y}")
    print("maximum exclusion zone", exclusion_zone)

    # now, lets check the entire exclusion zone
    for y in range(exclusion_zone.miny, exclusion_zone.maxy + 1):
        points = []
        for sensor in sensors:
            res = sensor.exclusion_zone_on_line(y)
            if res is None:
                continue
            start, end = res
            points.append(Point(start, START))
            points.append(Point(end, END))

        points.sort()

        open_stack = [points[0].val]
        prev_end = points[0].val

        empty_spots = False
        for p in points[1:]:
            if p.type == END:
                open_stack.pop()
                prev_end = p.val
            else:
                # in case we have an empty stack
                if len(open_stack) == 0:
                    # we can only open a new interval if we start
                    # where the old one left off
                    if p.val > prev_end + 1:
                        empty_spots = True
                        break
                open_stack.append(p.val)

        if y % 10000 == 0:
            print(y)
        if not empty_spots:
            continue

        print(points, y, "trying")
        for x in range(exclusion_zone.minx, exclusion_zone.maxx + 1):
            if f"X{x}Y{y}" in beacons:
                continue

            possible = True
            # otherwise, if its blocked by any sensor then count it
            for sensor in sensors:
                if sensor.within_zone(x, y):
                    possible = False
                    break

            if possible:
                return x * 4000000 + y

    return -1


def main():
    with open("day_15_input.txt", "r") as f:
        contents = f.read().strip()
        lines = parse_lines(contents)
        # result_1 = part_1(lines, 2000000)
        result_2 = part_2(lines, 0, 4000000)
        # print(f"part 1: {result_1}")
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

    # def test_part1(self):
    #     lines = parse_lines(self.input)
    #     self.assertEqual(26, part_1(lines, 10))

    def test_part2(self):
        lines = parse_lines(self.input)
        self.assertEqual(56000011, part_2(lines, 0, 20))


if __name__ == "__main__":
    # unittest.main()
    main()
