from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from util.logger import *
from typing import List, Tuple, Dict, Set


# Even at 990 the solution takes just a few seconds. Anything (much) higher will hit Python's maximum recursion depth.
MAX_BLINKS = 75

# Yay, dynamic programming! 🎉 Keep a map of all in-between results, otherwise we'll end up recalculating the same
# input value over and over again. The key has to be a tuple since you can't hash a list.
blink_results = {}  # (nr, blink_count) : stone_count_at_max_blinks


# Technically you could modify the function to also keep the progressive results for a certain input for all remaining
# blink-levels. This, however, would eat a lot of additional memory with, for now, unneeded performance improvements.
# The blink_o_plier(...) will only ever return when hitting the blink limit, so each return value is guaranteed to be
# the final result for that particular nr and blink level. Cache all of them, so we don't have to repeat the effort.
def blink_o_plier(nr: int, blink_count: int) -> int:
    """Increases blink_count by one and applies the blink rule to the number. Recursively calls itself until blink
    limit is reached."""

    if blink_count == MAX_BLINKS:
        return 1

    global blink_results
    if cached_val := blink_results.get((nr, blink_count), None):
        return cached_val

    blink_count += 1

    local_acc = 0
    orig_nr = nr
    if nr == 0:
        nr = 1

    elif len(nr_str := str(nr)) % 2 == 0:
        half = len(nr_str) // 2
        local_acc += blink_o_plier(int(nr_str[:half]), blink_count)
        local_acc += blink_o_plier(int(nr_str[half:]), blink_count)

        # We can save 'nr' since we haven't changed it.
        blink_results[(nr, blink_count - 1)] = local_acc
        return local_acc

    else:
        nr *= 2024

    local_acc += blink_o_plier(nr, blink_count)

    # Save agains't the original number, since we've changed it for the next input.
    blink_results[(orig_nr, blink_count - 1)] = local_acc

    return local_acc


# We can evaluate each number one-by-one as long as we keep track of their individual blink count.
def solve() -> int:
    # marked_nrs = [[nr, 0] for nr in get_lines_as_nrs(True)]  # type: ignore - 55312
    marked_nrs = [[nr, 0] for nr in get_lines_as_nrs()]

    acc = 0
    for nr, blink_count in marked_nrs:
        acc += blink_o_plier(nr, blink_count)

    return acc  # 223767210249237, took ~ 0.25s


if __name__ == "__main__":
    print(solve())
