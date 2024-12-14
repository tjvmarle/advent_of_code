from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from enum import Enum, auto
import re


X_MAX = 101
# X_MAX = 11
X_HALF = X_MAX // 2
Y_MAX = 103
# Y_MAX = 7
Y_HALF = Y_MAX // 2
TIME = 100
# ROBOT = 'X'
ROBOT = 'O'
EMPTY = ' '
WALL = '+'


# Lists in python wrap automatically
def solve() -> int:
    lines = get_lines()
    # lines = get_lines(True)

    plain_grid = []
    for y in range(Y_MAX):
        row = []
        for x in range(X_MAX):
            if x == X_HALF and y == Y_HALF or x == X_HALF or y == Y_HALF:
                row.append(WALL)
                continue

            row.append(EMPTY)
        plain_grid.append(row)

    grid = Grid(plain_grid)

    q1, q2, q3, q4 = [0, 0, 0, 0]
    for line in lines:
        px, py, vx, vy = [int(pos) for pos in re.findall(r"-?\d+", line)]
        final_x = (px + vx * TIME) % X_MAX
        final_y = (py + vy * TIME) % Y_MAX

        if final_x == X_HALF or final_y == Y_HALF:
            continue  # Position at the quadrant divider

        grid.set_val(final_x, final_y, ROBOT)

        if final_x < X_HALF:
            if final_y < Y_HALF:
                q1 += 1
            else:
                q3 += 1
        else:
            if final_y < Y_HALF:
                q2 += 1
            else:
                q4 += 1

    # grid.print()
    return q1 * q2 * q3 * q4


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
