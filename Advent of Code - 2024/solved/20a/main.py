from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile

START = "S"
PATH = "."
END = "E"
SHORTCUT_THRESHOLD = 100


def get_start(grid: Grid) -> Tuple[int, int]:
    """Retrieves the start position."""
    # I won't deny I lost some time because I left the start position of the example in my script somewhere...
    for row in grid:
        for cell in row:
            if cell.get_value() == START:
                return cell.get_pos()
    raise ValueError("Start not found")


def set_path_values(racetrack: Grid) -> Dict[Tuple[int, int], int]:
    """Same as one of the earlier questsions, just assign a step count to each cell."""

    start = get_start(racetrack)
    curr_cell = start
    step_value = 0
    racetrack.set_val(*start, step_value)

    def path_or_end(cell: Cell): return cell.get_value() in (PATH, END)

    cell_path: Dict[Tuple[int, int], int] = {start: step_value}
    while True:
        step_value += 1

        if not (nb := racetrack.get_adjacent_neighbours_with(*curr_cell, path_or_end)):
            return cell_path

        nb[0].set_value(step_value)
        cell_path[nb[0].get_pos()] = step_value
        curr_cell = nb[0].get_pos()


def get_shortcuts(cell_path: Dict[Tuple[int, int], int]) -> List[int]:
    """Traverse the path and offset by 2 in each direction. If the offset exists and has a delta greater than 2 it is a
    shortcut."""

    offsets = ((2, 0), (0, 2), (-2, 0), (0, -2))

    shortcuts: List[int] = []
    for pos, curr_path_cost in cell_path.items():
        cell_x, cell_y = pos

        for offset_x, offset_y in offsets:
            other_path_cost = cell_path.get((cell_x + offset_x, cell_y + offset_y), -1)

            if other_path_cost != -1 and (time_saved := other_path_cost - curr_path_cost - 2) >= SHORTCUT_THRESHOLD:
                shortcuts.append(time_saved)

    return sorted(shortcuts)


def solve() -> int:

    racetrack = Grid(get_lines_as_grid())
    # racetrack = Grid(get_lines_as_grid(True))  # 44

    path_cells = set_path_values(racetrack)
    shortcut_values = get_shortcuts(path_cells)

    return len(shortcut_values)


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
