from Util.input import get_lines
from typing import Tuple, Dict, List, Set

import re

# TODO: Implement a way to efficiently manage columns instead of rows.


def solve() -> int:
    gen = get_lines(tst=False)

    rock_list = []
    for line in gen:
        rock_list.append([char for char in line])

    # Ugly, but it works
    rolled = True
    while rolled:
        rolled = False

        for index_line, line in enumerate(rock_list):

            if index_line + 1 == len(rock_list):  # Last line
                continue

            # Check if char below is rock and if current one is empty.
            for index, char in enumerate(line):
                if char == "." and rock_list[index_line + 1][index] == "O":
                    line[index] = "O"
                    rock_list[index_line + 1][index] = "."
                    rolled = True

    for line in rock_list:
        print("".join(line))

    acc: int = 0
    rock_list.reverse()
    for multi, line in enumerate(rock_list):
        acc += "".join(line).count("O") * (multi + 1)
        # line_str = "".join(line)
        # val = (line_str.count("0") + 1) * multi

    return acc


if __name__ == "__main__":
    print(solve())
