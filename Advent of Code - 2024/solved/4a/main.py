from util.input import *  # Eat me
from typing import List

SUBSTRING = "XMAS"

Grid = List[List[str]]


def square_to_diamond(square: Grid) -> Grid:
    """Rotates a square grid 1/8 clockwise, turning it into a diamond."""

    diamond_length = len(square) * 2 - 1  # E.g. a 3x3 square creates a 5 row diamond.
    diamond = [[] for _ in range(diamond_length)]

    # We'll append each row to a new list of rows, then move the starting row by one and repeat.
    quart_grid = list(zip(*square))  # Columns to rows
    for row_cnt, row in enumerate(quart_grid):
        for char_cnt, char in enumerate(row):
            diamond[row_cnt + char_cnt].append(char)

    return diamond


def diamond_to_square(diamond: Grid) -> Grid:
    """Rotates a diamond grid 1/8 clockwise, turning it into a square."""

    square_length = (len(diamond) + 1) // 2
    square = []

    # We can just keep stripping the first entry of the first 'square_length' nr of rows.
    while any(diamond):
        row = list()
        for index in range(square_length):
            row.append(diamond[index].pop(0))
        row.reverse()
        square.append(row)
        del diamond[0]  # Should be empty now

    return square


def one_eight_turn(grid: Grid) -> Grid:
    """Rotate the grid 1/8 clockwise."""
    return square_to_diamond(grid) if len(grid[0]) == len(grid) else diamond_to_square(grid)


# Obvious solution: write a search algorithm
# More fun: rotate the text in 1/8 turns and scan for the string
def solve() -> int:
    acc: int = 0

    lines = get_lines()

    grid: Grid = []
    for line in lines:
        grid.append([char for char in line])

    curr_grid = grid
    for _ in range(8):
        curr_grid = one_eight_turn(curr_grid)
        str_grid = ["".join(char_row) for char_row in curr_grid]

        for row_str in str_grid:
            acc += row_str.count(SUBSTRING)

    return acc


if __name__ == "__main__":
    print(solve())
