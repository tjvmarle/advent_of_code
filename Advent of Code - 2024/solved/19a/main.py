from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile


SIZE = 71
EMPTY = "."
BYTE = "#"


def arrange_towels(remaining_design: str, towels: List[str]) -> bool:

    if remaining_design == "":
        return True

    for towel in towels:
        if remaining_design.startswith(towel):

            if arrange_towels(remaining_design[len(towel):], towels):
                return True

    return False


# Seems doable with a depth-first approach. Recursion seems an option here. Can probably be optimized further by sorting
# the towels and only select relevant ones for further analysis.
def solve() -> int:
    acc: int = 0

    lines = get_lines()
    towels: List[str] = [towel.strip() for towel in next(lines).split(",")]
    next(lines)  # Empty line

    for design in lines:
        acc += 1 if arrange_towels(design, towels) else 0

    return acc  # 209


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
