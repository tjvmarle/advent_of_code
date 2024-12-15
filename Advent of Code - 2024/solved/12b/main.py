from util.input import *  # # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from enum import Enum, auto
import numpy as np
from functools import reduce

rules_map: dict[int, List[int]] = {}

EMPTY = '.'
FIELD = 'X'
FIELD_MULTI = 3


def my_sides(subfield: List[Cell], field_char: str) -> int:
    """Determines the number of sides of a field by counting the number of corners."""

    # To determine the number of sides we can scan each position for their neighbours. We also add an empty line around
    # the entire field to make scanning easier later. --> TODO: We don't need the edge anymore.
    max_x, max_y = 0, 0
    max_x = reduce(max, [cell.x_pos for cell in subfield], 0)
    max_y = reduce(max, [cell.y_pos for cell in subfield], 0)

    # We multiply the field in size so we'll reduce the number of possible situations we can find when counting the
    # number of neighbours.
    multi_field = np.full(shape=((max_y + 1) * FIELD_MULTI + 2,
                                 (max_x + 1) * FIELD_MULTI + 2), fill_value=EMPTY, dtype=str)

    for cell in subfield:
        for y_offset in range(FIELD_MULTI):
            for x_offset in range(FIELD_MULTI):
                curr_x = (cell.x_pos * FIELD_MULTI) + x_offset + 1
                curr_y = (cell.y_pos * FIELD_MULTI) + y_offset + 1

                multi_field[curr_y][curr_x] = field_char

    # We check every field cell and count its' neighbours. Certain counts correspond to it being a corner or not.
    # Because we've grown the field (increased resolution) only a few options are possible (in any rotation):
    #
    # Corner:           x    x    x
    #
    #             ...  .xx  ...  ..x  xxx
    #             xOx  xOx  xO.  xO.  xOx
    #             xxx  xxx  xx.  xx.  xxx
    #
    # Neigbours:   5    7    3    4    8
    #
    # No additional effort is required for situation 4, since we'll scan the diagonal corner also.

    # For example, these situations aren't possible anymore due to increasing the resolution, so we don't have to
    # perform any additional calculations for those.
    #
    #  ...  .x.  .xx
    #  xOx  xOx  xOx
    #  x.x  xxx  xx.
    #   4    5    6

    multi_grid = Grid(multi_field.tolist())
    def is_field(other: Cell): return other.get_value() == field_char

    side_count = 0
    for multi_row in multi_grid:
        for multi_cell in multi_row:
            if multi_cell.get_value() != FIELD_CHAR:
                # This way we also automatically skip the edges of the grid, since we've added an empty border.
                continue

            neighbours = multi_grid.get_surrounding_neighbours_with(multi_cell.x_pos, multi_cell.y_pos, is_field)

            match(len(neighbours)):
                case 5 | 6 | 8:
                    pass

                case 3 | 4 | 7:
                    side_count += 1

                case _:
                    raise NotImplementedError

    return side_count


def solve() -> int:
    acc: int = 0

    grid = get_lines_as_grid()
    # grid = get_lines_as_grid(True)
    total_field = Grid(grid)

    # First find the fields' area and save its' exact shape. Determine the perimeter seperately.
    for y, line in enumerate(grid):
        for x, curr_char in enumerate(line):
            if total_field.get_val(x, y) == EMPTY:
                continue

            # This keeps track of the entire field we're currently evaluating, while wiping the total field.
            acc_curr_field: List[Cell] = [start_cell := total_field.get_cell(x, y)]

            # This is a growing frontline to detect the current field.
            curr_char_fields = [start_cell]

            curr_area = 1
            while curr_char_fields:

                curr_cell = curr_char_fields.pop(0)
                if curr_cell.get_value() == EMPTY:
                    continue

                def same_val(cell: Cell):
                    nonlocal curr_cell
                    return cell.get_value() == curr_cell.get_value()

                neighbours = total_field.get_adjacent_neighbours_with(curr_cell.x_pos, curr_cell.y_pos, same_val)
                total_field.set_val(curr_cell.x_pos, curr_cell.y_pos, EMPTY)

                for neighbour in neighbours:
                    if neighbour in acc_curr_field:
                        continue
                    curr_area += 1

                    # We've 'consumed' the current cell.
                    acc_curr_field.append(neighbour)
                    curr_char_fields.append(neighbour)
            else:
                # curr_char_field consumed. Count corners to find number of sides.
                curr_perimeter = my_sides(acc_curr_field, curr_char)
                acc += curr_area * curr_perimeter

    return acc  # 1461806


if __name__ == "__main__":
    cProfile.run("print(solve())", "performance_data")
    # print(solve())
