from Util.input import get_lines
from typing import Dict, List

# We 'nest' these characters so we can copy them by reference instead of by value.
ROCK = ["O"]
EMPTY = ["."]
BLOCK = ["#"]


# We only need to implement for one direction, since we can just use different views of the same grid to move in
# alternate directions
def tilt_right(rock_list: List[List[List[str]]]) -> None:
    """Moves all rocks on the current line completely to the right. Although it works in a single pass, it does require
    inspecting each character on the line.
    """

    for line in rock_list:
        rock_indices: List[int] = []
        space_available = False

        for curr_pos, curr_char in enumerate(line):

            end_of_line_hit = len(line) - 1 == curr_pos
            if curr_char == ROCK:
                rock_indices.append(curr_pos)
                if not end_of_line_hit:
                    continue

            if curr_char == EMPTY and rock_indices:
                space_available = True
                if not end_of_line_hit:
                    continue

            if curr_char == BLOCK or end_of_line_hit:

                if rock_indices and space_available:  # Rocks found and empty space in between them. Time to roll!
                    rock_indices.reverse()  # This prevents overwrites in the wrong order

                    for offset, rock_index in enumerate(rock_indices, 1 if curr_char == BLOCK else 0):  # eol correction
                        # Write the char instead of list to avoid breaking the reference between views.
                        line[rock_index][0] = EMPTY[0]

                        # No checking if current position already contains a rock.
                        line[curr_pos - offset][0] = ROCK[0]

                # Reset whether or not rocks have moved.
                rock_indices.clear()
                space_available = False


def rotate_minus_90(grid: List[List[List[str]]]) -> List[List[List[str]]]:
    """Creates a copy of the grid, rotated 90 degrees counter-clockwise. Since lists are copied  by reference, this
    creates a rotated 'view' of the original."""
    new_grid = []
    for index in range(len(grid) - 1, -1, -1):  # Just moving backwards.
        line = []
        for entry in grid:
            line.append(entry[index])

        new_grid.append(line)
    return new_grid


def hash_grid(grid: List[List[List[str]]]) -> int:
    """Concat all chars and hash the resulting string."""
    row_str = []
    for row in grid:
        row_str.append("".join([char[0] for char in row]))

    hash_str = "".join(row_str)
    return hash(hash_str)


def print_grid(grid):
    """Debugging tool."""
    for row in grid:
        print("".join(char[0] for char in row))
    print("")


def solve() -> int:
    gen = get_lines(tst=False)
    rock_grid_0: List[List[List[str]]] = []  # Default view. Rows --> cols --> chars

    for line in gen:
        rock_grid_0.append([[char] for char in line])

    # Because all characters are nested in their own list, we can copy their list-objects by reference and create
    # 'views' that are rotated in different directions. Replacing a char will replace it in all views.
    # Wrapping in a custom class would've achieved the same result, but a list will suffice.
    rock_grid_270 = rotate_minus_90(rock_grid_0)
    rock_grid_180 = rotate_minus_90(rock_grid_270)
    rock_grid_90 = rotate_minus_90(rock_grid_180)

    def cycle_grid():
        """Full rotation of the grid. Yes, this will take 40k list-lookups total."""
        tilt_right(rock_grid_90)    # North
        tilt_right(rock_grid_180)   # West
        tilt_right(rock_grid_270)   # South
        tilt_right(rock_grid_0)     # East

    curr_cycle: int = 0
    step_map: Dict[int, int] = {}  # This is how we track every state of the board.

    while True:  # Holy shit the performance is terrible.
        curr_cycle += 1  # Since the assignment start counting at 1.

        cycle_grid()
        grid_hash = hash_grid(rock_grid_0)

        if not step_map.get(grid_hash):
            step_map[grid_hash] = curr_cycle  # Unique board state found
            continue

        # When we find a duplicate board state it is guaranteed it will repeat this state every # nr of cycles.
        rep_size = curr_cycle - step_map[grid_hash]

        # Now we just need to find the board state that will match up to 1e9 in rep_size increments
        remaining_steps = int((1e9 - curr_cycle) % rep_size)
        while remaining_steps > 0:
            cycle_grid()
            remaining_steps -= 1

        # print(f"Exit loop after {curr_cycle} cycles. rep_size: {rep_size}.")  # We need <200 cycles
        # print_grid(rock_grid_0)
        break

    acc: int = 0
    rock_grid_0.reverse()  # Since the scoring is descending.
    for multi, line in enumerate(rock_grid_0, 1):
        acc += "".join((char[0] for char in line)).count("O") * multi

    return acc


if __name__ == "__main__":
    print(solve())
