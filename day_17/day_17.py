from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import unittest


# i discovered frozen=True today, lets try it out
@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)


@dataclass(frozen=True)
class Piece:
    points: list[Point]

    # left/right we'll do as mutations
    def shift_left(self) -> Piece:
        pts = []
        for point in self.points:
            pts.append(Point(point.x - 1, point.y))
        return Piece(pts)

    def shift_right(self) -> Piece:
        pts = []
        for point in self.points:
            pts.append(Point(point.x + 1, point.y))
        return Piece(pts)

    # down we'll do as a copy for now.
    def shift_down(self) -> Piece:
        pts = []
        for point in self.points:
            pts.append(Point(point.x, point.y - 1))
        return Piece(pts)

    def valid(self) -> bool:
        for point in self.points:
            if not (point.x >= 0 and point.x <= 6 and point.y >= 0):
                return False
        return True


class Board:
    mat: set[Point]
    jets: str
    jet_idx: int = 0
    top: int = -1
    piece_idx: int = 0

    def __init__(self, jets: str):
        self.mat = set()
        self.jets = jets

    def next_wind(self) -> str:
        char = self.jets[self.jet_idx]
        self.jet_idx = (self.jet_idx + 1) % len(self.jets)
        return char

    def collides(self, piece: Piece) -> bool:
        for pt in piece.points:
            if pt in self.mat:
                return True
        return False

    def add(self, piece: Piece):
        for pt in piece.points:
            self.mat.add(pt)
            self.top = max(self.top, pt.y)

    def iter(self):
        piece = self.next_piece()

        while True:
            wind = self.next_wind()
            if wind == "<":
                lefted = piece.shift_left()
                if lefted.valid() and not self.collides(lefted):
                    piece = lefted
            else:
                righted = piece.shift_right()
                if righted.valid() and not self.collides(righted):
                    piece = righted

            # try to move it down
            candidate = piece.shift_down()
            if not candidate.valid() or self.collides(candidate):
                self.add(piece)
                break
            else:
                piece = candidate

    def next_piece(self) -> Piece:
        # 3 lines between piece and the top
        y = self.top + 4
        idx = self.piece_idx
        self.piece_idx = (self.piece_idx + 1) % 5

        # return the next piece at the correct height
        if idx == 0:
            # ####
            return Piece([Point(2, y), Point(3, y), Point(4, y), Point(5, y)])
        elif idx == 1:
            #  #
            # ###
            #  #
            return Piece(
                [
                    Point(3, y),
                    Point(2, y + 1),
                    Point(3, y + 1),
                    Point(4, y + 1),
                    Point(3, y + 2),
                ]
            )
        elif idx == 2:
            #   #
            #   #
            # ###
            return Piece(
                [
                    Point(2, y),
                    Point(3, y),
                    Point(4, y),
                    Point(4, y + 1),
                    Point(4, y + 2),
                ]
            )
        elif idx == 3:
            # #
            # #
            # #
            # #
            return Piece(
                [Point(2, y), Point(2, y + 1), Point(2, y + 2), Point(2, y + 3)]
            )
        else:
            # ##
            # ##
            return Piece([Point(2, y), Point(3, y), Point(2, y + 1), Point(3, y + 1)])

    def print_board(self):
        for y in range(self.top + 2, -1, -1):
            print("|", end="")
            for x in range(0, 7):
                if Point(x, y) in self.mat:
                    print("#", end="")
                else:
                    print(".", end="")
            print("|", end="")
            print()
        print("---------")


def solve(contents: str, iterations: int) -> int:
    board = Board(contents)
    for i in range(iterations):
        board.iter()
    board.print_board()
    return board.top + 1  # zero-indexed


def part_1(contents: str) -> int:
    return solve(contents, 2022)


def part_2(contents: str) -> int:
    # we can't do this the same way. SOMETHING will repeat but i don't know what yet.
    # lcm(length(input), 5) is the point at which we'll do the exact same motions again?
    # but its not guaranteed we'll just copy what we did because it could fit differently
    # into the new board.
    # maybe something about the jet itself?
    # maybe something more optimal with placing pieces?
    return -1


def main():
    with open("day_17_input.txt", "r") as f:
        contents = f.read().strip()
        print(len(contents))
        result_1 = part_1(contents)
        result_2 = part_2(contents)
        print(f"part 1: {result_1}")
        print(f"part 2: {result_2}")


class Day17Test(unittest.TestCase):
    input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

    # def test_part1(self):
    #     self.assertEqual(3068, part_1(self.input))

    def test_myself(self):
        input = "<><>>><>>>"
        self.assertEqual(100, solve(">>>>><<<<<>>>>><<<<<", len(input) * 5))


if __name__ == "__main__":
    unittest.main()
    # main()
