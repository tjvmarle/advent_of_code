from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from typing import List, Tuple, Dict

EMPTY = '.'

antenna_map = Dict[str, List[Cell]]


def get_all_positions(grid: Grid) -> antenna_map:
    radio_map: antenna_map = {}

    for row in grid:
        for cell in row:
            if cell.get_value() == EMPTY:
                continue

            # Create the list if none exist, otherwise append to existing.
            if antenna_list := radio_map.get(cell.get_value(), []):
                antenna_list.append(cell)  # This is a reference to the list in the dict.
            else:
                radio_map[cell.get_value()] = [cell]  # Fresh list needs to be inserted first.

    return radio_map


def get_all_resonances(antenna_cells: antenna_map, grid: Grid):

    resonance_points = set()
    for _, cell_list in antenna_cells.items():
        positions = [(cell.x_pos, cell.y_pos) for cell in cell_list]

        if len(positions) == 1:  # Lone antenna, can be ignored.
            continue

        # We'll compare every position against every other position including itself, hence the double loop.
        for base_x, base_y in positions:
            for other_x, other_y in positions:

                # Antennas resonate with itself if they're in line with another one.
                if base_x == other_x and base_y == other_y:
                    resonance_points.add((base_x, base_y))
                    continue  # This also prevents an infinite loop due to offset (0,0).

                # We'll only move the offset in one direction, since the other direction will be done in some next
                # iteration.
                offset_x, offset_y = (base_x - other_x, base_y - other_y)
                next_x, next_y = (base_x + offset_x, base_y + offset_y)

                # Minor change from 8a. We'll just repeat the offsets as long as they're on the grid.
                while grid.get_cell(next_x, next_y):
                    resonance_points.add((next_x, next_y))
                    next_x += offset_x
                    next_y += offset_y

    return resonance_points


def solve() -> int:
    acc: int = 0

    grid = Grid(get_lines_as_grid())
    # grid = Grid(get_lines_as_grid(True))
    antenna_positions = get_all_positions(grid)
    resonance_locations = get_all_resonances(antenna_positions, grid)

    for x, y in resonance_locations:
        if grid.get_val(x, y) == ".":
            grid.set_val(x, y, "#")
    grid.print()

    acc = len(resonance_locations)
    return acc  # 1115


if __name__ == "__main__":
    print(solve())
