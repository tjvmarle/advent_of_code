from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
from collections import Counter
import cProfile

START = "S"
PATH = "."
END = "E"
MIN_SHORTCUT_GAIN = 100
MAX_SHORTCUT_STEPS = 20


def get_start(grid: Grid) -> Tuple[int, int]:
    """Retrieves the start position."""
    for row in grid:
        for cell in row:
            if cell.get_value() == START:
                return cell.get_pos()
    raise ValueError("Start not found")


def set_path_values(racetrack: Grid) -> List[Tuple[Tuple[int, int], int]]:
    """Same as one of the earlier questsions, just assign a step count to each cell."""

    start = get_start(racetrack)
    curr_cell = start
    step_value = 0
    racetrack.set_val(*start, step_value)

    def path_or_end(cell: Cell): return cell.get_value() in (PATH, END)

    # We'll use a list now because it is sorted.
    cell_path: List[Tuple[Tuple[int, int], int]] = [(start, step_value)]
    while True:
        step_value += 1

        if not (nb := racetrack.get_adjacent_neighbours_with(*curr_cell, path_or_end)):
            return cell_path

        next_cell = nb[0]

        next_cell.set_value(step_value)
        cell_path.append((next_cell.get_pos(), step_value))
        curr_cell = next_cell.get_pos()


def get_shortcuts(cell_path: List[Tuple[Tuple[int, int], int]]) -> int:
    """
       We can work the list downwards and compare against all other remaining positions. If the delta_x + delta_y <= 76
       both cells can reach eachother. Here we again compare their path values.
    """

    shortcuts: Counter[int] = Counter()
    print(f"Cell path size: {len(cell_path)}")
    for curr_path_index, ((curr_x, curr_y), curr_path_cost) in enumerate(cell_path):

        if curr_path_index > len(cell_path) - MIN_SHORTCUT_GAIN:
            # We can skip the bottom group of cells, since the delta will never be larger than the threshold.
            return shortcuts.total()

        # And we can also skip the first bunch of remaining cells since any possible shortcut will be too short.
        for (other_x, other_y), other_path_cost in cell_path[(curr_path_index + MIN_SHORTCUT_GAIN):]:

            delta_steps = abs(other_x - curr_x) + abs(other_y - curr_y)
            if delta_steps > MAX_SHORTCUT_STEPS:
                continue

            shortcut_gain = other_path_cost - curr_path_cost - delta_steps
            if shortcut_gain < MIN_SHORTCUT_GAIN:
                continue

            shortcuts[shortcut_gain] += 1

    raise ValueError("You shouldn't be ably to reach this.")


# Second half is quite similar, we just change how we determine the shortcut a bit.
def solve() -> int:

    racetrack = Grid(get_lines_as_grid())
    # racetrack = Grid(get_lines_as_grid(True))  # 285

    path_cells = set_path_values(racetrack)
    shortcut_values = get_shortcuts(path_cells)

    return shortcut_values  # 997879


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
