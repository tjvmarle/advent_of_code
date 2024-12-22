from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile


numpad = """
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

dirpad = """
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

# There's no need to solve any directional input. The only thing that matters is the distance between each buttonpress.

dist_matrix = [
    [8][4][8][12][8][12][16][12][16][4]  # 0 --> 1,2,3,4,5,6,7,8,9,A
    [8][4][8][4][8][12][8][12][16][12]  # 1 --> 0,2,3,4,5,6,7,8,9,A
]


def solve() -> int:
    acc: int = 0

    lines = get_lines()
    # lines = get_lines(True)

    for line in numpad.split("\n"):
        print(f"line: {line}")

    return acc


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
