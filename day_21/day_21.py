from __future__ import annotations

import unittest
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# it might have been better to do an ADT between 2 node types
# but maybe will follow up in the future or something
@dataclass(frozen=True)
class Node:
    name: str
    val: str | int
    left: Optional[Node] = None
    right: Optional[Node] = None

    def inorder(self) -> str:
        strs = []
        if self.left is not None and self.right is not None:
            strs.append(self.left.inorder())
            strs.append(str(self.val))
            strs.append(self.right.inorder())
            return "(" + " ".join(strs) + ")"
        else:
            if self.name == "humn":
                return f"{self.val}[human]"
            else:
                return str(self.val)

    def compute(self) -> int:
        if isinstance(self.val, int):
            return self.val

        if self.left is None or self.right is None:
            raise Exception("cant happen")

        left = self.left.compute()
        right = self.right.compute()
        if self.val == "+":
            return left + right
        elif self.val == "-":
            return left - right
        elif self.val == "*":
            return left * right
        else:
            return left // right

    def contains_node(self, name: str) -> bool:
        if self.name == name:
            return True

        if self.left is None or self.right is None:
            return False

        return self.left.contains_node(name) or self.right.contains_node(name)


def build_tree(graph: dict[str, Formula | int], node: str) -> Node:
    elem = graph[node]
    if isinstance(elem, int):
        return Node(node, elem)

    else:
        return Node(
            node, elem.op, build_tree(graph, elem.left), build_tree(graph, elem.right)
        )


@dataclass
class Formula:
    left: str
    right: str
    op: str


def parsed_contents(contents: str) -> dict[str, Formula | int]:
    graph: dict[str, Formula | int] = {}

    for line in contents.split("\n"):
        monkey, formula = line.split(": ")
        parts = formula.strip().split(" ")
        if len(parts) == 1:
            graph[monkey] = int(parts[0])
        else:
            graph[monkey] = Formula(parts[0], parts[2], parts[1])

    return graph


def part_1(contents: str) -> int:
    graph = parsed_contents(contents)
    tree = build_tree(graph, "root")
    return tree.compute()


def part_2(contents: str) -> int:
    graph = parsed_contents(contents)

    root = graph["root"]
    if isinstance(root, int):
        raise Exception("root found to have a value, this isn't right for part 2")

    search = build_tree(graph, root.left)
    soln = build_tree(graph, root.right)

    # do a quick swap just to make sure that "search" has humn and "soln" doesn't
    if soln.contains_node("humn"):
        temp = search
        search = soln
        soln = temp

    # traverse the tree trying to find humn, and reversing operations
    while True:
        if search.name == "humn":
            break

        if search.left is None or search.right is None:
            raise Exception("you messed up")

        op: str = str(search.val)
        newop = flip(op)  # it'll be a string don't worry

        # the left case is easy, we just move stuff over to the other side
        if search.left.contains_node("humn"):
            newnode = Node(search.name, newop, left=soln, right=search.right)
            soln = newnode
            search = search.left

        # the right case is hard because we need to undo some of the signs / division
        # e.g. 10 - x = 5, you have to subtract 10 and then also multiply by negative one
        # to fully get x by itself
        elif search.right.contains_node("humn"):
            if op == "+":
                soln = Node(search.name, "-", left=soln, right=search.left)
            elif op == "*":
                soln = Node(search.name, "/", left=soln, right=search.left)
            elif op == "-":
                soln = Node(search.name, "-", left=soln, right=search.left)
                soln = Node(
                    search.name, "*", left=soln, right=Node("", -1)
                )  # transfer sign over
            elif op == "/":
                print("does this really happen cuz it can't work with integer division")
                soln = Node(search.name, "/", left=soln, right=search.left)
                soln = Node(search.name, "/", left=Node("", 1), right=soln)

            search = search.right
        else:
            raise Exception("we lost humn")

    return soln.compute()


def flip(op: str) -> str:
    if op == "+":
        return "-"
    elif op == "-":
        return "+"
    elif op == "*":
        return "/"
    elif op == "/":
        return "*"
    else:
        raise Exception("hmm")


def main():
    with open("day_21_input.txt", "r") as f:
        contents = f.read().strip()
        result_1 = part_1(contents)
        result_2 = part_2(contents)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day21Test(unittest.TestCase):
    input = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()

    def test_part1(self):
        self.assertEqual(152, part_1(self.input))

    def test_part2(self):
        self.assertEqual(301, part_2(self.input))


if __name__ == "__main__":
    # unittest.main()
    main()
