from Util.input import get_lines
from typing import Tuple, Dict, List, Set

GALAXY_CHAR = '#'
EMPTY_CHAR = "."
MILLION_CHAR = "M"
M_SPACE = int(1e6 - 1)


def parse_file():
    gen = get_lines()
    galaxy_chart: List[List[str]] = []
    filled_x = set()
    for line in gen:
        if not GALAXY_CHAR in line:
            galaxy_chart.append([MILLION_CHAR for _ in line])
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
            row[col] = MILLION_CHAR

    # for row in galaxy_chart:  # pipe to file for a print of the inflated galaxy
    #     print("".join(row))

    return galaxy_chart


def solve() -> int:
    galaxy_chart = parse_file()
    galaxies: List[Tuple[int, int]] = []
    for row_nr, row in enumerate(galaxy_chart):  # Map out all galaxies
        for char_nr, char in enumerate(row):
            if char == GALAXY_CHAR:
                galaxies.append((char_nr, row_nr))

    acc: int = 0
    m_rows, m_cols = set(), set()
    for index, char in enumerate(galaxy_chart[0]):
        if char == MILLION_CHAR:
            m_cols.add(index)

    for index, row in enumerate(galaxy_chart):
        if row[0] == MILLION_CHAR:
            m_rows.add(index)

    for index, galaxy in enumerate(galaxies):
        for other_gal in galaxies[index + 1:]:  # Only count downwards to avoid duplicates
            self_x, self_y = galaxy[0], galaxy[1]
            other_x, other_y = other_gal[0], other_gal[1]
            acc += abs(self_x - other_x)
            acc += abs(self_y - other_y)

            # 1M for every M between the coördinates
            for space_x in m_cols:
                if min(self_x, other_x) < space_x < max(self_x, other_x):
                    acc += M_SPACE

            for space_y in m_rows:
                if min(self_y, other_y) < space_y < max(self_y, other_y):
                    acc += M_SPACE

    return acc


if __name__ == "__main__":
    print(solve())
