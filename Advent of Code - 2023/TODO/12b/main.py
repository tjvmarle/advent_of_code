from Util.input import get_lines
from typing import Tuple, Dict, List, Set


def solve() -> int:
    gen = get_lines(tst=True)
    acc: int = 0

    # Approach 1
    # First get the minimum, valid match (left-to-right) for the given sequence.
    # Then start iterating to the right towards other valid locations.
    # E.g.: move the right-most term 1 (valid) step. With the space created,
    # try to move the 2nd-to-right 1 step. Then 3rd-to-right.

    # Approach 2
    # Find some mathematical approach to calculate all legal options.
    # Perhaps it's possitble to calculte all valid position of a term, given the constraints of the set.

    # Maybe do a left-most and right-most match of the set. For every entry in the set, check the matching position of
    # that entry in the left/right matches and check the number of valid alternatives inbetween.
    # Do this for all possible entry and multiply the results together.

    return acc


if __name__ == "__main__":
    print(solve())
