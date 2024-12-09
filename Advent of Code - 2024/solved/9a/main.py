from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from typing import List, Tuple, Dict


# Easy solution: expand the entire thing, defragment and evaluate from left to right.
# More fun: consume the line from both ends and calculate the checksum in a single pass.
def solve() -> int:
    acc: int = 0

    # I've padded both with a single trailing 0
    line = [int(char) for char in get_lines()]
    # line = [int(char) for char in get_lines(True)]  # 1928

    # No need to calculate the entire disk. We can just consume both sides and accumulate the checksum.
    id_cntr = 0
    pos_cntr = 0
    top_id = (len(line) // 2) - 1

    def fill_back_file_blocks():
        nonlocal line
        if len(line) > 1:
            line.pop(-1)  # Back end empty space
            return [top_id for _ in range(line.pop(-1))] if line else None

    def accumulate(left: int, right: int):
        nonlocal acc, pos_cntr
        acc += left * right
        pos_cntr += 1

    back_file_blocks = []

    while line:
        # We can accumulate the checksum going forward as long as we're evaluating file blocks
        file = line.pop(0)
        for _ in range(file):
            accumulate(pos_cntr, id_cntr)
        id_cntr += 1

        # When we encounter free space we can do more or less the same, except we'll consume blocks from the back.
        free_space = line.pop(0)
        for _ in range(free_space):
            if not back_file_blocks:
                back_file_blocks = fill_back_file_blocks()
                top_id -= 1

                if not back_file_blocks:
                    break  # If it's still empty we've consumed all of it.

            accumulate(pos_cntr, back_file_blocks.pop())

    # This can happen when there is some buffer left from the back while we were filling empty space from the front.
    if back_file_blocks:
        for leftover in back_file_blocks:
            accumulate(pos_cntr, leftover)

    return acc  # 6461289671426


if __name__ == "__main__":
    print(solve())
