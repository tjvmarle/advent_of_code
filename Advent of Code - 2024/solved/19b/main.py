from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import cProfile


SIZE = 71
EMPTY = "."
BYTE = "#"


def validate_design(remaining_design: str, towels: List[str]) -> bool:

    if remaining_design == "":
        return True

    for towel in towels:
        if remaining_design.startswith(towel):

            if validate_design(remaining_design[len(towel):], towels):
                return True

    return False


cache: Dict[str, int] = {"": 1}


def arrange_towel_all_combinations(remaining_design: str, towels: List[str]) -> int:
    global cache

    if remaining_design in cache:
        return cache[remaining_design]

    curr_remaining_count = 0
    for towel in towels:
        if remaining_design.startswith(towel):
            curr_remaining_count += arrange_towel_all_combinations(remaining_design[len(towel):], towels)

    cache[remaining_design] = curr_remaining_count
    return curr_remaining_count


# Feels like some variant of the coin change problem?
def solve() -> int:
    acc: int = 0

    lines = get_lines()
    # lines = get_lines(True)

    towels: List[str] = [towel.strip() for towel in next(lines).split(",")]

    indexed_towels: Dict[int, List[str]] = {}
    for towel in towels:
        sized_towels = indexed_towels.get(len(towel), [])
        sized_towels.append(towel)
        indexed_towels[len(towel)] = sized_towels

    next(lines)  # Empty line
    valid_designs = []
    for design in lines:
        if validate_design(design, towels):
            valid_designs.append(design)

    for valid_design in valid_designs:
        acc += arrange_towel_all_combinations(valid_design, towels)

    return acc  # 777669668613191


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
