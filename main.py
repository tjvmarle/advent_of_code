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


def edge_crawl(grid: Grid, start) -> int:
    start_x, start_y = start
    start_cell = grid.get_cell(start_x, start_y)
    next_cell = grid.get_cell(start_x + 1, start_y)

    side_count = 1

    # Move one to the right.

    def same_val(neighbour_cell: Cell):
        return neighbour_cell.get_value() == FIELD

    while next_cell != start_cell:
        neighbours = grid.get_surrounding_neighbours_with(next_cell.x_pos, next_cell.y_pos, same_val)
        print(f"curr_cell: {next_cell}, neighbours: {neighbours}")

        # ...  .xx  ... ..x
        # xXx  xXx  xX. xX.
        # xxx  xxx  xx. xx.
        #  5    7    3   4

        match(len(neighbours)):
            case 5:
                # Regular case, keep moving right
                print(f"  Regular case")

            case 7:
                print(f"  Upside corner")
                side_count += 1
                # Rotate clockwise
                ...

            case 3 | 4:
                print(f"  Downside corner")  # Possibly with a diagonal field.
                # Rotate counter-clockwise
                side_count += 1
                ...

            case _:
                # This should be impossible
                print(f"  Impossibru: {next_cell}")
                ...

        next_cell = grid.get_cell(next_cell.x_pos + 1, next_cell.y_pos)

    return 0


def my_sides(subfield: List[Cell]) -> int:
    # To determine the number of sides we can scan the edge for corners. We need to repeat that for any nested fields.
    max_x, max_y = 0, 0
    max_x = reduce(max, [cell.x_pos for cell in subfield], 0)
    max_y = reduce(max, [cell.y_pos for cell in subfield], 0)

    # We multiply the field in size so it's easier to scan the edges without interference.
    field_holder = np.full(shape=((max_y + 1) * FIELD_MULTI + 2,
                                  (max_x + 1) * FIELD_MULTI + 2), fill_value=EMPTY, dtype=str)

    for cell in subfield:
        for y_offset in range(FIELD_MULTI):
            for x_offset in range(FIELD_MULTI):
                curr_x = (cell.x_pos * FIELD_MULTI) + x_offset + 1
                curr_y = (cell.y_pos * FIELD_MULTI) + y_offset + 1

                field_holder[curr_y][curr_x] = FIELD

    start_position = []
    for y, row in enumerate(field_holder):
        if start_position:
            break
        for x, cell_val in enumerate(row):
            if cell_val == EMPTY:
                continue

            start_position = [x, y]
            break

    for row in field_holder:
        print("".join(row))

    sides = edge_crawl(Grid(field_holder.tolist()), start_position)

    return 0


def solve() -> int:
    acc: int = 0

    # grid = get_lines_as_grid()
    grid = get_lines_as_grid(True)
    total_field = Grid(grid)

    field_holder = np.full(shape=(len(grid[0]), len(grid)), fill_value=EMPTY, dtype=str)

    # First find the fields' area and save its'exact shape. Determine the perimeter seperately.
    for y, line in enumerate(grid):
        for x, curr_char in enumerate(line):
            if total_field.get_val(x, y) == EMPTY:
                continue

            curr_area = 1

            # This keeps track of the entire field we're currently evaluating, while wiping the total field.
            acc_curr_field: List[Cell] = [start_cell := total_field.get_cell(x, y)]

            # This is a growing frontline to detect the current field.
            curr_char_fields = [start_cell]

            while curr_char_fields:
                print(f"Working through {curr_char_fields}, curr_char: {curr_char}")
                if len(curr_char_fields) > 6:
                    return 0

                curr_cell = curr_char_fields.pop(0)
                if curr_cell.get_value() == EMPTY:
                    continue

                def same_val(cell: Cell):
                    nonlocal curr_cell
                    print(f"  Checking: {curr_cell} vs {cell}")
                    return cell.get_value() == curr_cell.get_value()

                neighbours = total_field.get_adjacent_neighbours_with(curr_cell.x_pos, curr_cell.y_pos, same_val)
                print(f"    From {total_field.get_cell(curr_cell.x_pos, curr_cell.y_pos)}, got back {neighbours}")
                total_field.set_val(curr_cell.x_pos, curr_cell.y_pos, EMPTY)

                for neighbour in neighbours:
                    curr_area += 1

                    # We've 'consumed' the current cell.
                    acc_curr_field.append(neighbour)
                    curr_char_fields.append(neighbour)
            else:
                # curr_char_field consumed. We should now have the area and perimeter of curr_char, that started at x,y
                curr_perimeter = my_sides(acc_curr_field)
                acc += curr_area * curr_perimeter
                return 10

    return acc  # 1461806


if __name__ == "__main__":
    cProfile.run("print(solve())", "performance_data")
    # print(solve())
