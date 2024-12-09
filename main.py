from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from typing import List, Tuple, Dict


class Block():
    def __init__(self, address: int, size: int, file_id: int, free: bool) -> None:
        self.address = address
        self.size = size
        self.free = free
        self.file_id = file_id if not free else '.'
        self.alread_moved = False

    def fits(self, other_block: 'Block') -> bool:
        return self.free and other_block.size <= self.size

    def fill(self, other_block: 'Block') -> 'Block':
        """Fills the current empty block with data. Returns a new block with remaining free space, which could be zero."""
        if not self.free:
            raise ValueError(f"Block {self} contains file, not free space.")

        if other_block.size > self.size:
            raise ValueError(f"Cannot fit block of size {other_block.size} in memory of size {self.size}.")

        remaining_block = Block(self.address + other_block.size, self.size - other_block.size, 0, True)
        self.size = other_block.size
        self.free = other_block.free  # Which should be False
        self.file_id = other_block.file_id
        self.alread_moved = True
        other_block.erase()

        return remaining_block

    def erase(self):
        self.file_id = '.'
        self.free = True

    def empty(self) -> bool:
        return self.size == 0

    def checksum(self) -> int:
        if self.free:
            return 0

        total = 0
        for offset in range(self.size):
            total += self.file_id * (self.address + offset)  # type: ignore - This is guaranteed an int.

        return total

    def __repr__(self) -> str:
        return f"{self.address}:{self.size}:{self.file_id}"

    def __str__(self) -> str:
        return f"{str(self.file_id) * self.size}"


def defragment(partition: List[Block]):

    base_partition_index_max = len(partition) - 1
    for back_counter, back_block in enumerate(partition[::-1]):
        back_index = base_partition_index_max - back_counter

        if back_block.free or back_block.alread_moved:
            continue

        for before_index, before_block in enumerate(partition):
            if before_index == back_index:
                break  # We've searched up to our initial position. If we move further we risk moving data backwards.

            if not before_block.free or before_block.empty():
                continue

            if not before_block.fits(back_block):
                continue

            remaining_block = before_block.fill(back_block)
            if not remaining_block.empty():
                partition.insert(before_index + 1, remaining_block)
            break

    return sum([block.checksum() for block in partition])


def solve() -> int:
    acc: int = 0

    line = [int(char) for char in get_lines()]
    # line = [int(char) for char in get_lines(True)]  # 2858

    is_free_toggle = False
    curr_address = 0
    block_list: List[Block] = []

    for file_id, block_size in enumerate(line):
        block_list.append(Block(curr_address, block_size, file_id // 2, is_free_toggle))
        is_free_toggle = not is_free_toggle
        curr_address += block_size

    acc = defragment(block_list)

    return acc
# 9a:       6461289671426
# Too high: 6490561614794


if __name__ == "__main__":
    print(solve())
