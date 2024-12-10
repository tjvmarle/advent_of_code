from typing import List, Any, Optional, Generator, Callable


class Cell():
    def __init__(self, val: Any, x_pos: int, y_pos: int, grid: 'Grid') -> None:
        """Cells should not be created outside the Grid class. Type hinting them is fine."""
        self.value: Any = val
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Each cell keeps a reference to the entire grid. This simplifies traversing the grid from a cell reference.
        self._grid = grid

    def get_value(self) -> Any:
        return self.value

    def set_value(self, value: Any) -> Any:
        self.value = value

    def get_adjacent_neighbours(self) -> List['Cell']:
        """Returns all cells within bounds that are directly up, down, left and right of this cell."""
        neighbours: List['Cell'] = []

        for position in [(self.x_pos - 1, self.y_pos),  # Left
                         (self.x_pos + 1, self.y_pos),  # Right
                         (self.x_pos, self.y_pos - 1),  # Up
                         (self.x_pos, self.y_pos + 1)   # Down
                         ]:
            if cell := self._grid.get_cell(*position):
                neighbours.append(cell)

        return neighbours

    def get_surrounding_neighbours(self) -> List['Cell']:
        """Returns all adjacent cells (within bounds), including diagonals."""
        neighbours: List['Cell'] = []

        for position in [(self.x_pos - 1, self.y_pos),  # Left
                         (self.x_pos + 1, self.y_pos),  # Right
                         (self.x_pos, self.y_pos - 1),  # Up
                         (self.x_pos, self.y_pos + 1),  # Down
                         (self.x_pos - 1, self.y_pos - 1),  # Top-left
                         (self.x_pos + 1, self.y_pos - 1),  # Top-right
                         (self.x_pos - 1, self.y_pos + 1),  # Down-left
                         (self.x_pos + 1, self.y_pos + 1),  # Down-right
                         ]:
            if cell := self._grid.get_cell(*position):
                neighbours.append(cell)

        return neighbours

    def __repr__(self) -> str:
        return f"Cell: ({self.x_pos},{self.y_pos}): {self.value}"


Grid_input = List[List[Any]] | Generator
Cell_Grid = List[List[Cell]]


class Grid():
    def __init__(self, grid: Grid_input, cell_values_as_integers: bool = False) -> None:
        self.grid = self._parse_grid(grid, cell_values_as_integers)
        self.max_x = len(self.grid[0]) - 1
        self.max_y = len(self.grid) - 1

    def _parse_grid(self, grid: Grid_input, is_integer: bool = False) -> Cell_Grid:
        grid_list: Grid_input = []

        for y_pos, line in enumerate(grid):
            grid_list.append([])

            for x_pos, val in enumerate(line):
                grid_list[y_pos].append(Cell(val if not is_integer else int(val), x_pos, y_pos, self))

        return grid_list

    def _in_bounds(self, x_pos, y_pos) -> bool:
        return 0 <= x_pos <= self.max_x and 0 <= y_pos <= self.max_y

    def print(self, spacer: str = " ", to_string: Callable = str):
        for line in self.grid:
            print(f"{spacer}".join([to_string(cell.get_value()) for cell in line]))

    def get_cell(self, x_pos: int, y_pos: int) -> Optional[Cell]:
        if not self._in_bounds(x_pos, y_pos):
            return None

        return self.grid[y_pos][x_pos]

    def get_val(self, x_pos: int, y_pos: int) -> Optional[Any]:
        if cell := self.get_cell(x_pos, y_pos):
            return cell.get_value()

        return None

    def set_val(self, x_pos: int, y_pos: int, val: Any) -> bool:
        if cell := self.get_cell(x_pos, y_pos):
            cell.set_value(val)
            return True
        return False

    def __iter__(self):
        return (row for row in self.grid)
