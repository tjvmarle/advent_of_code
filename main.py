from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from typing import List, Tuple, Dict


class Block():
    def __init__(self, address: int, size: int, free: bool) -> None:
        self.address = address
        self.size = size
        self.free = free


def solve() -> int:
    acc: int = 0

    # line = [int(char) for char in get_lines()]
    line = [int(char) for char in get_lines(True)]  # 2858

    # TODO: I'm sure this could me a one-liner in Python. Map/reduce?
    file_list, free_list = [], []
    is_file = True
    start_index = 0

    block_list: List[Block] = []
    for entry in line:
        if is_file:
            file_list.append((start_index, entry))
            block_list.append(Block(start_index, entry, False))
            is_file = False
        else:
            free_list.append((start_index, entry))
            block_list.append(Block(start_index, entry, True))
            is_file = True

        start_index += entry

    for block in block_list[::-1]:
        ...
        # Don't forget to remove empty space from the back!

    #
    print(f"File list: {file_list}")
    print(f"Free list: {free_list}")

    return acc  # 6461289671426


if __name__ == "__main__":
    print(solve())
