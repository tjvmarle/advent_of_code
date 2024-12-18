from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile


SIZE = 71


# This can probably be done with some form of Dijkstra's algorithm from SciPy, but I've no idea how that module works.
# Luckily, it's relatively little effort to just check the cost to reach each cell from the start.
def solve() -> int:

    maze = Grid([["." for _ in range(SIZE)] for _ in range(SIZE)])
    lines = get_lines()

    for _ in range(1024):
        x, y = [int(pos) for pos in next(lines).split(",")]
        maze.set_val(x, y, "#")

    steps = 0
    start_pos = (0, 0)

    # We use a set, because it is possible to get duplicates when evaluating each layer.
    curr_layer: Set[Tuple[int, int]] = set()
    curr_layer.add(start_pos)

    while curr_layer:
        steps += 1
        next_layer = set()
        for pos in curr_layer:
            neighbours = maze.get_adjacent_neighbours_with_value(*pos, ".")

            for cell in neighbours:
                cell.set_value(steps)
                next_layer.add(cell.get_pos())

        curr_layer = next_layer

    return maze.get_cell(SIZE - 1, SIZE - 1).get_value()


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
