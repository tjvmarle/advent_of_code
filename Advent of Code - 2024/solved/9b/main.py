from util.input import *  # Yeah yeah, blah blah
from util.grid import *
from typing import List, Tuple, Dict


class Block():
    def __init__(self, address: int, size: int, file_id: int, free: bool) -> None:
        self.address = address
        self.size = size
        self.free = free
        self.file_id = file_id if not free else '.'  # Makes it easier to print the test-data.
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
        self.alread_moved = False

    def empty(self) -> bool:
        return self.size == 0

    def checksum(self) -> int:
        """Calculate this blocks' checksum."""
        if self.free:
            return 0

        total = 0
        for offset in range(self.size):
            total += self.file_id * (self.address + offset)  # type: ignore - This is guaranteed an int.

        return total

    def __repr__(self) -> str:
        return f"{self.address}:{self.size}:{self.file_id}"

    def __str__(self) -> str:
        return f"{str(self.file_id) * self.size}" if self.size else '-'


def defragment(partition: List[Block]) -> int:
    """Checking back-to-front, check if a file block can be moved forward (this check is performed fron-to-back).
    Returns the checksum of the entire partition."""

    msg = []
    for block in partition:
        msg.append(str(block))

    back_counter = -1
    curr_block = partition[back_counter]
    while curr_block is not partition[0]:  # While-loop makes it safe to mutate len(partition) while iterating.

        # This skips the last block, which is empty anyway. Having the decrement here simplifies the code.
        back_counter -= 1

        if curr_block.free or curr_block.alread_moved:
            curr_block = partition[back_counter]
            continue

        for before_index, before_block in enumerate(partition):

            if partition[before_index] is partition[back_counter + 1]:
                break  # We've searched up to our initial position. If we move further we risk moving data backwards.

            if not before_block.free or before_block.empty():
                continue

            if not before_block.fits(curr_block):
                continue

            remaining_block = before_block.fill(curr_block)
            if not remaining_block.empty():
                # Inserting while iterating would usually be dangerous, but we have a guaranteed break after this.
                partition.insert(before_index + 1, remaining_block)
            break

        curr_block = partition[back_counter]

    return sum([block.checksum() for block in partition])


def solve() -> int:
    acc: int = 0

    # Both datasets have been padded with a trailing 0 for easier processing.
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

    return acc  # 6488291456470, to ~5s


if __name__ == "__main__":
    print(solve())
