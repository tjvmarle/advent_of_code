from Util.input import get_lines
from typing import Tuple, Dict, List, Set
from enum import Enum


MARKED_PIPE = "0"
MARKED_OUTSIDE = " "
GRID_FILLER = '+'


class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)
    # b, a, select, start...


dir = Direction
exits: Dict[str, Tuple[Direction, Direction]] = {
    "|": (dir.up, dir.down),
    "-": (dir.left, dir.right),
    "F": (dir.down, dir.right),
    "7": (dir.left, dir.down),
    "L": (dir.up, dir.right),
    "J": (dir.up, dir.left),
}
out2in = {dir.up: dir.down, dir.down: dir.up, dir.left: dir.right, dir.right: dir.left}


def get_adjacent(cell_x: int, cell_y: int, min: int, max: int) -> List[Tuple[int, int]]:
    neighbours = []

    # This assumes a square grid
    if cell_x - 1 >= min:
        neighbours.append((cell_x - 1, cell_y))

    if cell_x + 1 <= max:
        neighbours.append((cell_x + 1, cell_y))

    if cell_y - 1 >= min:
        neighbours.append((cell_x, cell_y - 1))

    if cell_y + 1 <= max:
        neighbours.append((cell_x, cell_y + 1))

    return neighbours


def get_next_cells(grid: List[List[str]], cell_list: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # Return a new list of unmarked, non-pipe cells
    valid_neighbours: Set[Tuple[int, int]] = set()  # Avoid duplicates
    for cell_x, cell_y in cell_list:
        grid[cell_y][cell_x] = MARKED_OUTSIDE

        adj_cells = get_adjacent(cell_x, cell_y, 0, len(grid[0]) - 1)
        for next_x, next_y in adj_cells:
            if (adj := grid[next_y][next_x]) != MARKED_OUTSIDE and adj != MARKED_PIPE:
                valid_neighbours.add((next_x, next_y))

    return list(valid_neighbours)


def solve() -> int:

    # Inflate grid with filler-chars, '+'
    grid: List[List[str]] = []
    for line in get_lines():
        grid.append([GRID_FILLER for _ in range(len(line) * 2 + 1)])  # Filler line first.

        lst = []
        for char in line:  # Alternating '+' and char
            lst.append(GRID_FILLER)
            lst.append(char)
        lst.append(GRID_FILLER)  # One more at the end
        grid.append(lst)

    grid.append([GRID_FILLER for _ in range(len(grid[0]))])  # And one at the end

    nextChar = ""
    currPt = (102 * 2 - 1, 97 * 2 - 1)   # S-location of inflated grid
    currDir = dir.right  # Initial move direction, same as previous.

    pipe_size: int = 0
    while True:  # Traverse the pipe system. Move forward on a '+' and mark off all elements.
        pipe_size += 1
        curr_x, curr_y = currPt
        move_x, move_y = currDir.value

        next_x = curr_x + move_x
        next_y = curr_y + move_y

        nextChar = grid[next_y][next_x]
        grid[curr_y][curr_x] = MARKED_PIPE  # Mark element as 'done'
        if nextChar == MARKED_PIPE:
            break

        if nextChar == GRID_FILLER:
            # Move to next element and retry loop
            nextDir = currDir
        else:
            exit_a, exit_b = exits[nextChar]
            nextDir = exit_a if out2in[currDir] == exit_b else exit_b

        currPt = (next_x, next_y)
        currDir = nextDir

    outside_count: int = 0
    curr_cells: List[Tuple[int, int]] = [(0, 0)]
    while curr_cells:
        outside_count += len(curr_cells)
        curr_cells = get_next_cells(grid, curr_cells)

    # for row in grid:  # Pipe output to file for a nice visualization
    #     print("".join(row))

    # Just count everything --> 453
    acc: int = 0
    for row in grid:
        for char in row:
            # if char != MARKED_PIPE and char != MARKED_OUTSIDE and char != GRID_FILLER:
            if char not in (MARKED_PIPE, MARKED_OUTSIDE, GRID_FILLER):
                acc += 1

    return acc


if __name__ == "__main__":
    print(solve())
