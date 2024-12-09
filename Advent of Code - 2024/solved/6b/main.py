from util.input import *  # Eat me
from typing import List, Tuple

Grid = List[List[str]]

rules_map: dict[int, List[int]] = {}


def quarter_turn_clockwise(grid: Grid) -> Grid:
    return [list(tup)[::-1] for tup in zip(*grid)]


def quarter_turn_counter_clockwise(grid: Grid) -> Grid:
    return [list(tup) for tup in zip(*grid)][::-1]


GUARD = "^"
OBSTACLE = ["#", "O"]
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

            if curr_position not in OBSTACLE:
                grid[y][x] = MARKED  # This includes the current guard position.

            if curr_position in OBSTACLE:
                grid[y][x - 1] = GUARD
                return grid, False

        if guard_on_the_move:
            return grid, True  # This means the guard has moved off the grid. We're done.

    # It should be impossible to reach this line.
    raise NotImplementedError


def mark_all(grid: Grid) -> Tuple[Grid, bool]:
    """This is just the answer from 6a."""
    grid = quarter_turn_clockwise(grid)
    nr_of_turns = -1

    grid, done = move_guard(grid)

    grid_hashes = []
    loop_found = False
    while not done:
        grid = quarter_turn_counter_clockwise(grid)
        nr_of_turns += 1

        grid, done = move_guard(grid)

        if hash(str(grid)) in grid_hashes:
            loop_found = True
            break  # Loop detected

        grid_hashes.append(hash(str(grid)))

    # Re-arrange the grid to its' original position
    for _ in range(nr_of_turns % 4):
        grid = quarter_turn_clockwise(grid)

    return grid, loop_found


# Same as before: just rotate the input. Makes it easy to just scan the guard to the right.
def solve() -> int:

    acc: int = 0
    # Use a grid for easy replacement of visited cells.
    grid = [line for line in get_lines_as_grid()]
    # grid = [line for line in get_lines_as_grid(True)]
    def fresh_grid(): return [line for line in get_lines_as_grid()]

    marked_grid, _ = mark_all(grid)

    cntr = 0
    for y, line in enumerate(marked_grid):
        for x, char in enumerate(line):
            if char == MARKED:  # Possible location for a new obstacle.

                print(f"Analyzing entry {cntr}")
                # Replace this location with an obstacle and check if this grid will loop.
                new_grid = fresh_grid()

                if new_grid[y][x] == GUARD:
                    continue  # The only position in the entire grid we're not allowed to touch.
                else:
                    new_grid[y][x] = OBSTACLE[1]

                _, looped = mark_all(new_grid)

                acc += 1 if looped else 0

                if looped:
                    print(f"\t Entry {cntr} looped!")

                cntr += 1

    return acc  # 1602. This took 15 minutes!!


if __name__ == "__main__":
    print(solve())
