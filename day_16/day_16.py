from __future__ import annotations
from enum import IntEnum
import unittest
from dataclasses import dataclass
import re
from typing import Optional
from collections import deque


@dataclass
class Valve:
    name: str
    flow: int
    links: list[str]
    open: bool = False

    def __init__(self, name: str, flow: int, links: list[str]):
        self.name = name
        self.flow = flow
        self.links = links
        self.open = flow == 0


class Network:
    graph: dict[str, Valve]
    min_dist: dict[tuple[str, str], int]

    def __init__(self, graph: dict[str, Valve]):
        self.graph = graph
        self.min_dist = {}

        # lets figure out min distance
        for elem in graph:
            visited = set()
            q = deque([(elem, 0)])
            while len(q) > 0:
                next, dist = q.popleft()
                if next in visited:
                    continue
                self.min_dist[(elem, next)] = dist
                self.min_dist[(next, elem)] = dist
                for neighbor in graph[next].links:
                    q.append((neighbor, dist + 1))
                visited.add(next)
        print(self.min_dist)


def parse_graph(contents: str) -> dict[str, Valve]:
    graph = {}
    for line in contents.split("\n"):
        matches = re.match(
            "Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line
        )
        if matches is None or len(matches.groups()) != 3:
            raise Exception("shouldn't happen)")

        valve, flowstr, links = matches.groups()
        graph[valve] = Valve(valve, int(flowstr), links.split(", "))

    return graph


def part_1(graph: dict[str, Valve]) -> int:
    network = Network(graph)
    visited: dict[str, list[set[str]]] = {}
    for valvename in graph:
        visited[valvename] = []
    return recurse(graph, "AA", 1, visited)
    # return recurse2(network, "AA", 1, visited)


def recurse2(
    network: Network, valve: str, turn_num: int, visited: dict[str, list[set[str]]]
) -> int:
    print(f"valve: {network.graph[valve]}")
    graph = network.graph
    # base
    if turn_num >= 31:
        return 0

    openable = set()
    for node in graph.values():
        if not node.open:
            openable.add(node.name)

    if len(openable) == 0:
        return 0

    # check if we've already visited this in this exact position
    for prevstate in visited[valve]:
        if openable == prevstate:
            return 0

    # otherwise, let's add ourselves
    visited[valve].append(openable)
    best = -1

    # if the current valve isn't open, see what opening it would give us
    if not graph[valve].open:
        graph[valve].open = True
        print(f"just set {valve} open")
        value = ((30 - turn_num) * graph[valve].flow) + recurse2(
            network, valve, turn_num + 1, visited
        )
        best = max(value, best)
        graph[valve].open = False

    # we only really need to explore openable next options
    for elem in graph.values():
        if not elem.open and elem.name != valve:
            best = max(
                recurse2(
                    network,
                    elem.name,
                    turn_num + network.min_dist[(valve, elem.name)],
                    visited,
                ),
                best,
            )

    visited[valve].pop()
    return best


def recurse(
    graph: dict[str, Valve],
    valve: str,
    turn_num: int,
    visited: dict[str, list[set[str]]],
) -> int:
    # base
    if turn_num == 31:
        return 0

    openable = set()
    for node in graph.values():
        if not node.open:
            openable.add(node.name)

    if len(openable) == 0:
        return 0

    # check if we've already visited this in this exact position
    for prevstate in visited[valve]:
        if openable == prevstate:
            return 0

    # otherwise, let's add ourselves
    visited[valve].append(openable)
    best = -1

    # if the current valve isn't open, see what opening it would give us
    if not graph[valve].open:
        graph[valve].open = True
        value = ((30 - turn_num) * graph[valve].flow) + recurse(
            graph, valve, turn_num + 1, visited
        )
        best = max(value, best)
        graph[valve].open = False

    # check what going down every path would give us
    for link in graph[valve].links:
        best = max(recurse(graph, link, turn_num + 1, visited), best)

    visited[valve].pop()
    return best


def part_2(graph: dict[str, Valve]) -> int:
    return -1


def main():
    with open("day_16_input.txt", "r") as f:
        contents = f.read().strip()
        graph = parse_graph(contents)
        result_1 = part_1(graph)
        result_2 = part_2(graph)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day16Test(unittest.TestCase):
    input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()

    def test_part1(self):
        graph = parse_graph(self.input)
        self.assertEqual(1651, part_1(graph))


if __name__ == "__main__":
    # unittest.main()
    main()
