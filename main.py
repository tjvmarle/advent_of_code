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


cache: Dict[str, int] = {}


def arrange_towels_all(remaining_design: str, towels: List[str], curr_count: int = 0) -> int:
    # Lets try something with a recursive sliding window.

    if remaining_design == "":
        return 1

    for towel in towels:
        if remaining_design.startswith(towel):
            curr_count += arrange_towels_all(remaining_design[len(towel):], towels)

    return curr_count


# # Python program for coin change problem using memoization
# def countRecur(coins, n, sum, memo):

#     # If sum is 0 then there is 1 solution
#     # (do not include any coin)
#     if sum == 0:
#         return 1

#     # 0 ways in the following two cases
#     if sum < 0 or n == 0:
#         return 0

#     # If the subproblem is previously calculated then
#     # simply return the result
#     if memo[n - 1][sum] != -1:
#         return memo[n - 1][sum]

#     # count is sum of solutions (i)
#     # including coins[n-1] (ii) excluding coins[n-1]
#     memo[n - 1][sum] = (countRecur(coins, n, sum - coins[n - 1], memo) +
#                         countRecur(coins, n - 1, sum, memo))
#     return memo[n - 1][sum]


# def count(coins, sum):
#     memo = [[-1 for _ in range(sum + 1)] for _ in range(len(coins))]
#     return countRecur(coins, len(coins), sum, memo)


# if __name__ == "__main__":
#     coins = [1, 2, 3]
#     sum = ""
#     print(count(coins, sum))


def consume(remaining_string: str, indexed_towels: Dict[int, List[str]]):

    for towel in indexed_towels.values():
        if not remaining_string.startswith(towel):
            continue

        ...  # Do stuff

    # If we reach this point we've check
    # consume the string bit by bit and cache string combinations


# Feels like some variant of the coin change problem? I'm pretty stuck here.
def solve() -> int:
    acc: int = 0

    # lines = get_lines()

    lines = get_lines(True)
    towels: List[str] = [towel.strip() for towel in next(lines).split(",")]

    indexed_towels: Dict[int, List[str]] = {}
    for towel in towels:
        sized_towels = indexed_towels.get(len(towel), [])
        sized_towels.append(towel)
        indexed_towels[len(towel)] = sized_towels

    next(lines)  # Empty line
    valid_designs = []
    for design in lines:
        if arrange_towels(design, towels):
            valid_designs.append(design)

    for valid_design in valid_designs:
        acc = arrange_towels_all(valid_design, towels)

    return acc  # 209


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
