from Util.input import get_lines
import time
from typing import Dict, List, Tuple
from enum import Enum, auto


class Hole:
    def __init__(self, x: int, y: int, rgb: str) -> None:
        self.x = x
        self.y = y
        self.color = rgb


dirmap = {"R": (0, -1),
          "L": (0, 1),
          "U": (-1, 0),
          "D": (1, 0), }


BUFFER = 300 - 59
LAGOON_SIZE = 476


def get_adjacent(x: int, y: int) -> List[Tuple[int, int]]:
    left_x, right_x = x - 1, x + 1
    up_y, down_y = y - 1, y + 1

    tuplist = []

    if left_x >= 0:
        tuplist.append((left_x, y))

    if right_x < LAGOON_SIZE:
        tuplist.append((right_x, y))

    if up_y >= 0:
        tuplist.append((x, up_y))

    if down_y < LAGOON_SIZE:
        tuplist.append((x, down_y))

    return tuplist


def solve() -> int:
    gen = get_lines(tst=False)

    lagoon = []
    for _ in range(0, LAGOON_SIZE):
        lagoon.append([" " for _ in range(0, LAGOON_SIZE)])

    curr_pt = [BUFFER, BUFFER]
    lagoon[BUFFER][BUFFER] = Hole(BUFFER, BUFFER, "(#6248a0)")

    for line in gen:
        dir, steps, clr = line.split()
        curr_x, curr_y = curr_pt

        dir = dirmap[dir]
        move_x, move_y = dir[0], dir[1]
        for index in range(1, int(steps) + 1):
            new_x = curr_x + move_x * index
            new_y = curr_y + move_y * index
            lagoon[new_y][new_x] = Hole(new_x, new_y, clr)

        curr_pt = [curr_x + move_x * int(steps), curr_y + move_y * int(steps)]

    # Fill up the outside
    curr_cells = [(0, 0)]
    while curr_cells:
        next_cells = []
        for cell in curr_cells:
            neigbours = get_adjacent(*cell)
            neigbours.append(cell)
            # print(f"neigbours: {neigbours}")
            # return 0

            for adj_x, adj_y in neigbours:
                lagoon_entry = lagoon[adj_y][adj_x]
                if lagoon_entry == " ":
                    lagoon[adj_y][adj_x] = "."
                    next_cells.append((adj_x, adj_y))
        curr_cells = next_cells

    # Print out to out.txt
    acc: int = 0
    for line in lagoon:
        line_str = []
        for char in line:
            if char != ".":
                acc += 1
            line_str.append(" " if char == "." else "#")
        # print("".join(line_str))

    return acc


if __name__ == "__main__":
    now = time.time()
    print(f"Answer: {solve()}")
    delta = time.time() - now

    mins, secs = int(delta / 60), delta % 60
    time_str = ["Runtime: "]
    if mins:
        time_str.append(f"{mins}m ")
    time_str.append(f"{secs:.1f}s.")
    print("".join(time_str))
