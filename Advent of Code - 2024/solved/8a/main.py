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

            antenna_list = radio_map.get(cell.get_value(), [])
            antenna_list.append(cell)
            radio_map[cell.get_value()] = antenna_list

    return radio_map


def get_all_resonances(antenna_cells: antenna_map, grid: Grid):

    resonance_points = set()
    for _, cell_list in antenna_cells.items():
        positions = [(cell.x_pos, cell.y_pos) for cell in cell_list]

        for curr_x, curr_y in positions:
            for other_x, other_y in positions:
                if curr_x == other_x and curr_y == other_y:
                    continue

                offset_x, offset_y = (curr_x - other_x, curr_y - other_y)
                resonance_point = (curr_x + offset_x, curr_y + offset_y)
                if grid.get_cell(*resonance_point):
                    resonance_points.add(tuple([*resonance_point]))

    return resonance_points


def solve() -> int:
    acc: int = 0

    grid = Grid(get_lines_as_grid())
    # grid = Grid(get_lines_as_grid(True))
    antenna_positions = get_all_positions(grid)
    resonance_locations = get_all_resonances(antenna_positions, grid)

    for x, y in resonance_locations:
        grid.set_val(x, y, "#")

    acc = len(resonance_locations)

    return acc


if __name__ == "__main__":
    print(solve())
