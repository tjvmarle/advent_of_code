from Util.input import get_lines
from typing import Tuple, Dict
from enum import Enum, auto


class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)
    # b, a, select, start...


dir = Direction
exits: Dict[str, Tuple[Direction, Direction]] = {
    "|": (dir.up, dir.down),
    "-": (dir.left, dir.right),
    "F": (dir.down, dir.right),
    "7": (dir.left, dir.down),
    "L": (dir.up, dir.right),
    "J": (dir.up, dir.left)
}
out2in = {dir.up: dir.down, dir.down: dir.up, dir.left: dir.right, dir.right: dir.left}


def solve() -> int:
    grid = []
    for line in get_lines():
        grid.append([char for char in line])

    nextChar = ""
    currPt = (101, 96)   # S-location, no logic applied for this except 'ctrl+f'
    currDir = dir.right  # Initial move direction. Just read the grid.
    acc: int = 0

    while True:
        acc += 1

        curr_x, curr_y = currPt
        move_x, move_y = currDir.value

        next_x = curr_x + move_x
        next_y = curr_y + move_y

        nextChar = grid[next_y][next_x]
        if nextChar == "S":
            break

        exit_a, exit_b = exits[nextChar]
        nextDir = exit_a if out2in[currDir] == exit_b else exit_b

        currPt = (next_x, next_y)
        currDir = nextDir

    return int(acc / 2)


if __name__ == "__main__":
    print(solve())
