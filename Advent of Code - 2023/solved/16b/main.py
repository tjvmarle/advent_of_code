from Util.input import get_lines
from typing import Dict, List, Tuple
from enum import Enum, auto
import time


class Direction(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()


dir = Direction
dirmap = {
    (dir.up, "|"): (dir.up,),
    (dir.down, "|"): (dir.down,),
    (dir.left, "|"): (dir.up, dir.down),
    (dir.right, "|"): (dir.up, dir.down),

    (dir.up, "-"): (dir.left, dir.right),
    (dir.down, "-"): (dir.left, dir.right),
    (dir.right, "-"): (dir.right,),
    (dir.left, "-"): (dir.left,),

    (dir.up, "\\"): (dir.left,),
    (dir.down, "\\"): (dir.right,),
    (dir.right, "\\"): (dir.down,),
    (dir.left, "\\"): (dir.up,),

    (dir.up, "/"): (dir.right, ),
    (dir.down, "/"): (dir.left, ),
    (dir.right, "/"): (dir.up,),
    (dir.left, "/"): (dir.down,),

    (dir.up, "."): (dir.up, ),
    (dir.down, "."): (dir.down, ),
    (dir.right, "."): (dir.right,),
    (dir.left, "."): (dir.left,),
}


class Point:
    def __init__(self, char: str) -> None:
        self.char = char
        self.energized = False
        self.enery_direction = []

    def enter(self, dir: Direction) -> Tuple[Direction] | None:
        if self.energized and dir in self.enery_direction:
            return None  # Prevent infinite loops

        self.energized = True
        self.enery_direction.append(dir)
        return dirmap[(dir, self.char)]


move_map = {dir.up: (0, -1),
            dir.down: (0, 1),
            dir.left: (-1, 0),
            dir.right: (1, 0),
            }

MAX_X = 0
MAX_Y = 0


def move(x: int, y: int, dir: Direction) -> Tuple[int, int, Direction] | None:
    move_x, move_y = move_map[dir]
    x += move_x
    y += move_y
    if x < 0 or x > MAX_X or y < 0 or y > MAX_X:
        return None
    return (x, y, dir)


def get_mirror_maze():
    # gen = get_lines(tst=True)
    gen = get_lines(tst=False)
    grid = []
    for line in gen:
        grid.append([Point(char) for char in line])

    global MAX_X
    global MAX_Y
    MAX_X = len(grid[0]) - 1
    MAX_Y = len(grid) - 1
    return grid


def solve() -> int:
    maze = get_mirror_maze()

    all_directions = []
    for val in range(0, 100):
        all_directions.append((0, val, dir.right))
        all_directions.append((99, val, dir.left))
        all_directions.append((val, 0, dir.down))
        all_directions.append((val, 99, dir.up))

    res: int = 0
    for start_dir in all_directions:

        # Reset the maze - this eats most of the performance
        for line in maze:
            for pt in line:
                pt.energized = False
                pt.enery_direction = []

        curr_beams = [start_dir]

        while curr_beams:
            new_beams = []

            for beam in curr_beams:
                x, y, curr_dir = beam
                new_dirs = maze[y][x].enter(curr_dir)

                if not new_dirs:  # Dead end or loop
                    continue

                for new_dir in new_dirs:
                    if moved_beam := move(x, y, new_dir):
                        new_beams.append(moved_beam)
            curr_beams = new_beams

        acc: int = 0
        for line in maze:
            for pt in line:
                acc += 1 if pt.energized else 0

        res = max(res, acc)
        # Pipe this to an out.txt file
        # chars = ["X" if pt.energized else " " for pt in line]
        # print("".join(chars))

    return res


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
