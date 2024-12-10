from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from typing import List, Tuple, Dict, Set


PEAK = 9


# Lol, 10b literally just requires changing the sets to a list.
def solve() -> int:
    acc: int = 0

    grid = Grid(get_lines_as_grid(), True)
    # grid = Grid(get_lines_as_grid(True), True)  # 81

    cell_bases: List[Cell] = []

    # Collect all 0's.
    for row in grid:
        for cell in row:
            if cell.get_value() == 0:
                cell_bases.append(cell)

    for cell in cell_bases:
        curr_lvl: List[Cell] = [cell]

        while True:
            next_level: List[Cell] = []

            for curr_lvl_cell in curr_lvl:
                for neighbour in curr_lvl_cell.get_adjacent_neighbours():
                    if neighbour.value == curr_lvl_cell.value + 1:

                        # Now we're adding duplicates. This is correct, since each entry represents a unique path.
                        next_level.append(neighbour)

            if next_level and next(iter(next_level)).value == PEAK:
                acc += len(next_level)
                break

            curr_lvl = next_level

    return acc  # 1619


if __name__ == "__main__":
    print(solve())
