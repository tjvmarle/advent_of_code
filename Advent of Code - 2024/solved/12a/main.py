from util.input import *  # # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from enum import Enum, auto


rules_map: dict[int, List[int]] = {}

EMPTY = '.'


# Just use a grid. Every cell has area 1 and perimeter 4. Subtract 2 perimeter for each identical neighbour.
def solve() -> int:
    acc: int = 0

    grid = get_lines_as_grid()
    # grid = get_lines_as_grid(True)
    total_field = Grid(grid)

    curr_area = 0
    curr_perimeter = 0

    # We'll consume the grid letter for letter, line by line.
    for y, line in enumerate(grid):
        for x, curr_char in enumerate(line):
            if total_field.get_val(x, y) == EMPTY:
                continue

            curr_area = 1
            curr_perimeter = 4

            # This keeps track of the entire field we're currently evaluating, while wiping the total field.
            acc_curr_field: List[Cell] = [start_cell := total_field.get_cell(x, y)]

            # This is a growing frontline to detect the current field.
            curr_char_fields = [start_cell]

            while curr_char_fields:
                curr_cell = curr_char_fields.pop(0)

                def same_val(cell: Cell):
                    nonlocal curr_cell
                    return cell.get_value() == curr_cell.get_value()

                neigbours = total_field.get_adjacent_neighbours_with(curr_cell.x_pos, curr_cell.y_pos, same_val)
                total_field.set_val(curr_cell.x_pos, curr_cell.y_pos, EMPTY)

                for neighbour in neigbours:

                    if neighbour in acc_curr_field:

                        # We've hit this cell from a different direction before. This costs 2 perimeters.
                        curr_perimeter -= 2
                        continue

                    curr_area += 1
                    curr_perimeter += 2

                    # We've 'consumed' the current cell.
                    acc_curr_field.append(neighbour)
                    curr_char_fields.append(neighbour)
            else:
                # curr_char_field consumed. We should now have the area and perimeter of curr_char, that started at x,y
                acc += curr_area * curr_perimeter

    return acc  # 1461806


if __name__ == "__main__":
    cProfile.run("print(solve())", "performance_data")
    # print(solve())
