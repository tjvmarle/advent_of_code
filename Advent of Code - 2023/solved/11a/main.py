from Util.input import get_lines
from typing import Tuple, Dict, List, Set

GALAXY_CHAR = '#'
EMPTY_CHAR = "."


def parse_file():
    gen = get_lines()
    galaxy_chart: List[List[str]] = []
    filled_x = set()
    for line in gen:
        if not GALAXY_CHAR in line:
            galaxy_chart.append(["." for _ in line])
            galaxy_chart.append(["." for _ in line])  # Directly inflate in y-direction
            continue

        curr_row = []
        for col_nr, char in enumerate(line):
            curr_row.append(char)

            if char == GALAXY_CHAR:
                filled_x.add(col_nr)
        galaxy_chart.append(curr_row)

    # Inflate in x-direction.
    for col in range(len(galaxy_chart[0]) - 1, -1, -1):
        if col in filled_x:
            continue

        for row in galaxy_chart:
            row.insert(col, EMPTY_CHAR)

    # for row in galaxy_chart:  # pipe to file for a print of the inflated galaxy
    #     print("".join(row))

    return galaxy_chart


def solve() -> int:
    galaxy_chart = parse_file()
    galaxies: List[Tuple[int, int]] = []
    for row_nr, row in enumerate(galaxy_chart):
        for char_nr, char in enumerate(row):
            if char == GALAXY_CHAR:
                galaxies.append((char_nr, row_nr))

    acc: int = 0
    for index, galaxy in enumerate(galaxies):
        for other_gal in galaxies[index:]:  # Only count downwards to avoid duplicates
            acc += abs(other_gal[0] - galaxy[0])
            acc += abs(other_gal[1] - galaxy[1])

    return acc


if __name__ == "__main__":
    print(solve())
