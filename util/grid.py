from typing import List, Any, Optional, Generator, Callable


class Cell():
    def __init__(self, val: Any, x_pos: int, y_pos: int) -> None:
        self.value: Any = val
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_value(self) -> Any:
        return self.value

    def set_value(self, value: Any) -> Any:
        self.value = value

    def __repr__(self) -> str:
        return f"Cell: ({self.x_pos},{self.y_pos}): {self.value}"


Grid_input = List[List[Any]] | Generator
Cell_Grid = List[List[Cell]]

# TODO
# * What if input has rows of differing lengths? --> Pad with None's?


class Grid():
    def __init__(self, grid: Grid_input) -> None:
        self.grid = self._parse_grid(grid)
        self.max_x = len(self.grid[0]) - 1
        self.max_y = len(self.grid) - 1

    def _parse_grid(self, grid: Grid_input) -> Cell_Grid:
        grid_list: Grid_input = []

        for y_pos, line in enumerate(grid):
            grid_list.append([])

            for x_pos, val in enumerate(line):
                grid_list[y_pos].append(Cell(val, x_pos, y_pos))

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
