from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from util.logger import *
from typing import List, Tuple, Dict, Set


acc = 0
MAX_BLINKS = 25


def blink_o_plier(nr: int, blink_count: int):
    """Applies the blink rule to the number and increases blink_count by one. Recursively calls itself until blink
    limit is reached."""

    if blink_count == MAX_BLINKS:
        global acc  # Could've been a parameter, but this is easier for now.
        acc += 1
        return

    blink_count += 1

    if nr == 0:
        nr = 1

    elif len(nr_str := str(nr)) % 2 == 0:
        half = len(nr_str) // 2
        blink_o_plier(int(nr_str[:half]), blink_count)
        blink_o_plier(int(nr_str[half:]), blink_count)
        return

    else:
        nr *= 2024

    blink_o_plier(nr, blink_count)


# We can evaluate each number one-by-one as long as we keep track of their blink count.
def solve() -> int:
    # marked_nrs = [[nr, 0] for nr in get_lines_as_nrs(True)]  # type: ignore
    marked_nrs = [[nr, 0] for nr in get_lines_as_nrs()]  # 55312

    for nr, blink_count in marked_nrs:
        blink_o_plier(nr, blink_count)

    return acc  # 187738


if __name__ == "__main__":
    print(solve())
