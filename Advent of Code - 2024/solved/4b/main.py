from util.input import *  # Eat me
from typing import List

Grid = List[List[str]]


def square_to_diamond(square: Grid) -> Grid:
    """Rotates a square grid 1/8 clockwise, turning it into a diamond.

    Starting with:
                                       1                                    1
        1111                           21                                  2 1
        2222                           321                                3 2 1
        3333  --> expected result -->  4321  --> which is a diamond -->  4 3 2 1
        4444                           432                                4 3 2
                                       43                                  4 3
                                       4                                    4

    Strip the first column and append each value to a fresh list.

    Diamond:

        1 <-- start
        2
        3
        4
        []  <-- Empty lists (for now)
        []
        []

    Strip the next column from the input and append it to the diamond, but increase the row offset by one. Repeat.
    Every latest entry is enclosed in single quotes for clarity.

    Diamond:

        1                   1                    1
        2(1)  <-- start     2 1                  2 1
        3(2)                3 2(1)  <-- start    3 2 1
        4(3)                4 3(2)               4 3 2(1)  <-- start
       (4)    -->           4(3)   -->           4 3(2)
        []                 (4)                   4(3)
        []                  []                  (4)
    """

    diamond_length = len(square) * 2 - 1  # E.g. a 3x3 square creates a 5 row diamond.
    diamond = [[] for _ in range(diamond_length)]  # Since we'll only append, we need empty placeholders.

    quart_grid = list(zip(*square))  # This just changes columns to rows, since we'll need to strip the columns.
    for row_cnt, row in enumerate(quart_grid):
        for char_cnt, char in enumerate(row):
            diamond[row_cnt + char_cnt].append(char)

    return diamond


def diamond_to_square(diamond: Grid) -> Grid:
    """Rotates a diamond grid 1/8 clockwise, turning it into a square.

    Starting with:

        1                       1
        21                     2 1                             4321
        321                   3 2 1                            4321
        4321  --> equals --> 4 3 2 1  --> expected result -->  4321
        432                   4 3 2                            4321
        43                     4 3
        4                       4

    First calculate the size of the resulting square (4 x 4). Take the first value of this many rows, reverse them and
    throw them in the first list. Delete the (now empty) first slot of the diamond and repeat.

    The square is build line-by-line, so we'll show how we 'consume' the diamond. The square is going to be size 4, so
    strip the first value of the first 4 rows (highlighted between parentheses):

        (1)            [] <-- del  (1)         [] <-- del  (1)        []
        (2)1           1           (2)1        1           (2)1       1
        (3)2 1         2 1         (3)2 1      2 1         (3)2       2
        (4)3 2 1  -->  3 2 1  -->  (4)3 2 -->  3 2   -->   (4)3  -->  3  --> etc.
         4 3 2         4 3 2        4 3        4 3          4         4
         4 3           4 3          4          4
         4             4

    The removed values (1,2,3,4) need to be reversed and added as a list.
    """

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


def quarter_turn(grid: Grid) -> Grid:
    """Rotate the grid 1/4 clockwise."""
    return one_eight_turn(one_eight_turn(grid))


def scan_for_x_mas(diamond: List):
    """Checks the diamond for any 'MAS' or 'SAM' entries. Any 'A' encountered that isn't valid will be replaced by a '.'.
    """

    for char_row in diamond:
        line = "".join(char_row)

        for index in range(1, len(line) - 1):
            if line[index] == "A":
                if (line[index - 1] == "M" and line[index + 1] == "S") or \
                        (line[index - 1] == "S" and line[index + 1] == "M"):
                    continue  # Valid 'A'

                char_row[index] = "."  # Invalidate the 'A'


# Obvious solution: write a search algorithm and check for matches crosswise.
# More fun: rotate the block 1/8. Find all SAM and MAS, delete all invalid A's, turn 1/4, check all A's again.
def solve() -> int:
    acc: int = 0

    lines = get_lines()
    grid: Grid = []
    for cnt, line in enumerate(lines):
        charlist = [char for char in line]

        # Data cleanup, any edge-'A' is always invalid.
        if charlist[0] == "A":
            charlist[0] = "."

        if charlist[-1] == "A":
            charlist[-1] = "."

        grid.append(charlist)

    # First and last line also need all their A's removed.
    for line in (grid[0], grid[-1]):
        for cnt, char in enumerate(line):
            if char == "A":
                line[cnt] = "."

    grid = one_eight_turn(grid)

    scan_for_x_mas(grid)
    grid = quarter_turn(grid)

    # Second iteration. Any 'A' that's still valid after this must be an X-MAS.
    scan_for_x_mas(grid)

    flatlist = [char for charlist in grid for char in charlist]
    acc = "".join(flatlist).count("A")

    return acc  # 1912


if __name__ == "__main__":
    print(solve())
