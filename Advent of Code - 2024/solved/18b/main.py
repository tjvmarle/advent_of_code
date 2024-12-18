from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile


SIZE = 71
EMPTY = "."
BYTE = "#"


# Second half can still be easily brute forced. If it takes to long we can change the implementation to a binary
# approach instead:
# Drop 1024 bytes + remaining bytes / 2
#   If this blocks the end: half the 'remaining bytes' amount and repeat.
#     1024 bytes + remaining bytes / 4
#   If the end can still be reached: add the next half of remaining bytes (== 1/4):
#     1024 + remaining bytes / 2 + remaining bytes / 4
# Etc. untill answer is reached. Should be quite performant.
def solve() -> int:

    base_maze = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    lines = get_lines()

    for _ in range(1024):
        x, y = [int(pos) for pos in next(lines).split(",")]
        base_maze[y][x] = BYTE

    additional_bytes: List[Tuple[int, int]] = []

    while True:
        fresh_maze = Grid(list(base_maze))  # We'll skip the first 1024 bytes.
        next_x, next_y = [int(pos) for pos in next(lines).split(",")]
        additional_bytes.append((next_x, next_y))

        steps = 0
        start_pos = (0, 0)

        curr_layer: Set[Tuple[int, int]] = set()
        curr_layer.add(start_pos)

        for byte in additional_bytes:
            fresh_maze.set_val(*byte, BYTE)

        while curr_layer:
            steps += 1
            next_layer = set()
            for pos in curr_layer:
                neighbours = fresh_maze.get_adjacent_neighbours_with_value(*pos, EMPTY)

                for cell in neighbours:
                    cell.set_value(steps)
                    next_layer.add(cell.get_pos())

            curr_layer = next_layer

        if fresh_maze.get_cell(SIZE - 1, SIZE - 1).get_value() == EMPTY:
            return additional_bytes[-1]  # 39,40 - Took ~30+ seconds.


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
