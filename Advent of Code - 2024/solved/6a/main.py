from util.input import *  # Eat me
from typing import List, Tuple

Grid = List[List[str]]

rules_map: dict[int, List[int]] = {}


def quarter_turn_clockwise(grid: Grid) -> Grid:
    return [list(tup)[::-1] for tup in zip(*grid)]


def quarter_turn_counter_clockwise(grid: Grid) -> Grid:
    return [list(tup) for tup in zip(*grid)][::-1]


GUARD = "^"
OBSTACLE = "#"
MARKED = "X"


def move_guard(grid: Grid) -> Tuple[Grid, bool]:
    """Move the guard forwards. Replace al visited cells with an 'X'."""
    guard_on_the_move = False
    for y, line in enumerate(grid):
        for x, curr_position in enumerate(line):

            if curr_position != GUARD and not guard_on_the_move:
                continue  # Haven't found the guard for this line yet.
            else:
                guard_on_the_move = True

            if curr_position != OBSTACLE:
                grid[y][x] = MARKED  # This includes the current guard position.

            if curr_position == OBSTACLE:
                grid[y][x - 1] = GUARD
                return grid, False

        if guard_on_the_move:
            return grid, True  # This means the guard has moved off the grid. We're done.

    return  # type: ignore - It should be impossible to reach this line.


# Same as before: just rotate the input. Makes it easy to just scan the guard to the right.
def solve() -> int:

    acc: int = 0
    # Use a grid for easy replacement of visited cells.
    grid = [line for line in get_lines_as_grid()]

    grid = quarter_turn_clockwise(grid)
    grid, done = move_guard(grid)

    while not done:
        grid = quarter_turn_counter_clockwise(grid)
        grid, done = move_guard(grid)

    for line in grid:
        acc += "".join(line).count(MARKED)

    return acc


if __name__ == "__main__":
    print(solve())
