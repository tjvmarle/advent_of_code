from util.input import *  # # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile
from operator import attrgetter
import sys

WALL = '#'
EMPTY = '.'
START = 'S'
END = 'E'
PATH = 'X'


def fill_dead_ends(grid: Grid):
    # Not sure if it helps, but this will remove any dead ends.

    cntr = 1

    while cntr < len(grid):
        dead_end_filled = False
        row = grid[cntr]

        for cell in row:
            if cell.get_value() != EMPTY:
                continue

            if len(grid.get_adjacent_neighbours_with_value(*cell.get_pos(), WALL)) == 3:
                cell.set_value(WALL)
                dead_end_filled = True

        cntr += -1 if dead_end_filled else 1


def get_neighbour_value():
    ...


def get_path_value(path: List[Cell], grid: Grid):
    # Convert the path to a value. Each corner adds a 1000. Each step adds 1.
    path_value = len(path) - 1

    # Just check for each cell if both adjacent cells are opposites.
    for cell in path[1:-1]:
        curr_x, curr_y = cell.get_pos()
        left, right = grid.get_cell(curr_x - 1, curr_y), grid.get_cell(curr_x + 1, curr_y)
        up, down = grid.get_cell(curr_x, curr_y - 1), grid.get_cell(curr_x, curr_y + 1)

        if not (left in path and right in path) and not (up in path and down in path):
            path_value += 1000  # Corner + step

    start_x, start_y = path[0].get_pos()
    if path[1].get_pos() == (start_x, start_y - 1):
        # Initial move was up, which adds a 1000
        path_value += 1000

    return path_value


def is_empty_or_goal(cell: Cell):
    return cell.get_value() in [EMPTY, END]


# path_value_limit = 99489
path_value_limit = 100_000
best_path: List[Cell] = []
node_limit_map: Dict[Tuple[int, int], int] = {}


def search_to_end(grid: Grid, curr_cell: Cell, curr_path: List[Cell], curr_path_val: int):
    curr_path.append(curr_cell)

    neighbours = grid.get_adjacent_neighbours_with(*curr_cell.get_pos(), is_empty_or_goal)

    if len(neighbours) > 2:
        # We've hit a node. If we've hit this node before with a lower value the current path is taking too long.
        global node_limit_map
        if (pos := curr_cell.get_pos()) in node_limit_map:

            if node_limit_map[pos] < curr_path_val:
                return False  # This path is already too long.
            else:  # Current path is shorter/faster.
                node_limit_map[pos] = curr_path_val
        else:
            node_limit_map[pos] = curr_path_val

    global path_value_limit
    if len(curr_path) > 2 and curr_path_val >= path_value_limit:
        return False

    for next_cell in neighbours:

        if next_cell in curr_path:
            continue  # Dead end.

        if next_cell.get_value() == END:
            curr_path_val += 1
            curr_path.append(next_cell)
            path_value_limit = get_path_value(curr_path, grid)

            if path_value_limit != curr_path_val:
                print(f"  ERROR! Calculated path: {path_value_limit}, curr_path_val: {curr_path_val}, path length: {
                    len(curr_path)}")
            else:
                print(f"Calculated path: {path_value_limit}, curr_path_val: {curr_path_val}, current path length: {
                    len(curr_path)}.")
            global best_path
            best_path = list(curr_path)

            curr_path.pop()  # We've saved the current path, now we need to clean up until we reach another branch.
            curr_path_val -= 1
            return True

        prev_x, prev_y = curr_path[-2].get_pos()
        path_val_increase = 1 if next_cell.x_pos == prev_x or next_cell.y_pos == prev_y else 1001
        curr_path_val += path_val_increase

        search_to_end(grid, next_cell, curr_path, curr_path_val)

        curr_path.pop()  # Otherwise we'll block ourselves
        curr_path_val -= path_val_increase

    return False


def start_search(grid: Grid):
    start_pos = (1, len(grid) - 2)
    start_cell = grid.get_cell(*start_pos)

    neighbours = grid.get_adjacent_neighbours_with_value(*start_cell.get_pos(), EMPTY)

    path_found: List[Cell] = [start_cell]
    for next_cell in neighbours:
        path_value = 1
        if next_cell.y_pos != start_cell.y_pos:
            path_value += 1000
        search_to_end(grid, next_cell, path_found, path_value)
        path_found.pop()


def solve() -> int:
    lines = get_lines_as_grid()
    # lines = get_lines_as_grid(True)

    maze = Grid(lines)
    fill_dead_ends(maze)

    # Initial brute force attempts reached the end in ~2600 steps.
    sys.setrecursionlimit(5000)
    start_search(maze)

    fresh_maze = Grid(get_lines_as_grid())
    # fresh_maze = Grid(get_lines_as_grid(True))
    global best_path

    print(f"\nBest path value:")
    val = get_path_value(best_path, maze)
    print(f"\t{val}")
    print("\n")
    print(f"Path: {best_path}\n")
    for cell in best_path:
        fresh_maze.set_val(*cell.get_pos(), "X")

    print(f"\nSolution:\n")
    fresh_maze.print()
    print("\n")

    return path_value_limit  # 99460


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
