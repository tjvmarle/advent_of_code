from util.input import *  # Yeah yeah, blah blah
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
    # Not sure if it helps, but this will remove any dead ends except roundabouts.

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


# Setting these bounds saves a lot of calculations and makes it easier to count the paths.
path_value_limit = 99460
# path_value_limit = 11048
# path_value_limit = 7036

best_path_cells: Set[Cell] = set()
best_paths: List[List[Cell]] = []
node_limit_map: Dict[Tuple[int, int], int] = {}


def search_to_end(grid: Grid, curr_cell: Cell, curr_path: List[Cell], curr_path_val: int):

    curr_path.append(curr_cell)
    neighbours = grid.get_adjacent_neighbours_with(*curr_cell.get_pos(), is_empty_or_goal)

    # We save the path value at T-junctions. If we encounter it again with a higher value we can skip that attempt. We
    # skip crossroads, since they're more complex to properly cache.
    if len(neighbours) == 3:

        # If the next straight move would be a wall, this node costs an additional turn. Otherwise we'll end up caching
        # incorrect values, since from one direction you'll be forced to turn and from the other you won't.
        prev_x, prev_y = curr_path[-2].get_pos()
        curr_x, curr_y = curr_cell.get_pos()
        delta_x, delta_y = curr_x - prev_x, curr_y - prev_y
        actual_path_val = curr_path_val
        if grid.get_val(curr_x + delta_x, curr_y + delta_y) == WALL:
            # Next move would be into a wall. So the proper node value costs an additional turn.
            actual_path_val += 1000

        global node_limit_map
        if (pos := curr_cell.get_pos()) in node_limit_map:

            if node_limit_map[pos] < actual_path_val:
                return  # This path is already too long.

            else:  # Current path is shorter/faster or at least equivalent.
                node_limit_map[pos] = actual_path_val
        else:
            node_limit_map[pos] = actual_path_val

    global path_value_limit
    if curr_path_val >= path_value_limit:
        return

    for next_cell in neighbours:

        if next_cell in curr_path:
            continue  # Dead end.

        if next_cell.get_value() == END:
            curr_path_val += 1
            curr_path.append(next_cell)

            global best_path_cells, best_paths
            best_path_cells.update(curr_path)
            best_paths.append(list(curr_path))

            curr_path.pop()  # We've saved the current path, now we need to clean up until we reach another branch.
            curr_path_val -= 1
            return

        prev_x, prev_y = curr_path[-2].get_pos()
        path_val_increase = 1 if next_cell.x_pos == prev_x or next_cell.y_pos == prev_y else 1001
        curr_path_val += path_val_increase

        search_to_end(grid, next_cell, curr_path, curr_path_val)

        curr_path.pop()  # Otherwise we'll block ourselves
        curr_path_val -= path_val_increase

    return


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

    # Due to the high recursive nature of the solution we need a bit more stack space.
    sys.setrecursionlimit(5000)
    start_search(maze)

    fresh_maze = Grid(get_lines_as_grid())
    # fresh_maze = Grid(get_lines_as_grid(True))

    global best_path_cells, best_paths
    for path in best_paths:
        print(f"  Path: {path}")

    for cell in best_path_cells:
        fresh_maze.set_val(*cell.get_pos(), "X")

    print(f"\nSolution:\n")
    fresh_maze.print()

    return len(best_path_cells)  # 500


# Our lesson of the day: be careful with so many returns in a recursive solution.
if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
