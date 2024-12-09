from Util.input import get_lines
from typing import Dict, List, Generator, Any, Tuple


def get_pattern() -> Generator[List[str], Any, Any]:
    """Returns a generator yielding the patterns one by one. Filters out the empty lines between them."""
    gen = get_lines(tst=False)

    pattern = []
    for line in gen:

        if line == "":
            yield pattern
            pattern = []
            continue

        pattern.append(line)

    yield pattern


def search_reflection(pattern, old_reflection, log=False):
    """Tries to find a reflection that reaches an edge."""
    for line_index in range(0, len(pattern) - 1):
        if pattern[line_index] != pattern[line_index + 1]:
            continue

        if old_reflection and line_index + 1 == old_reflection[0]:
            continue

        offset: int = 1
        while True:  # Reflection found, keep checking until you hit an edge or find two unequal lines.
            if line_index - offset < 0 or line_index + 1 + offset > len(pattern) - 1:
                return (line_index + 1, line_index + 2)  # Edge hit, full reflection found.

            if pattern[line_index - offset] != pattern[line_index + 1 + offset]:
                break  # No reflection, continue search

            offset += 1

    return False


def find_reflection(pattern: List[str], old_reflection: Tuple[int, str]):
    if res := search_reflection(pattern, old_reflection if old_reflection[1] == "row" else None, True):
        return res[0], "row"
    else:
        res = search_reflection(transpose_pattern(pattern), old_reflection if old_reflection[1] == "col" else None)
        return False if not res else (res[0], "col")


def transpose_pattern(pattern: List[str]):
    """First line becomes first column, etc. Assumes the pattern is rectangular."""
    return ["".join(line) for line in zip(*pattern)]  # No need to write a column-based reflection search this way.


def brute_force_pattern(pattern: List[str]):
    """Creates all permutations of the patterns with a single field inverted."""

    x = y = 0
    x_max, y_max = len(pattern[0]), len(pattern) - 1
    while x != x_max or y != y_max:

        if x == x_max:  # Move to beginning of next line
            x = 0
            y += 1

        new_pattern = []

        for row, line in enumerate(pattern):
            if row != y:
                new_pattern.append(line)
                continue

            new_char = "." if line[x] == "#" else "#"
            new_pattern.append(f"{line[:x]}{new_char}{line[x+1:]}")

        yield new_pattern

        x += 1


def print_pattern(pattern):
    for line in pattern:
        print(line)
    print()


def solve() -> int:
    pttrn_gen = get_pattern()

    acc: int = 0
    for pattern in pttrn_gen:

        old_reflection = find_reflection(pattern, (-1, ""))
        brute_gen = brute_force_pattern(pattern)

        for invert_pattern in brute_gen:
            reflection_found = find_reflection(invert_pattern, old_reflection)
            if not reflection_found:  # or reflection_found == old_reflection:
                continue

            val, res_type = reflection_found
            if res_type == "row":
                val *= 100

            acc += val
            break

    return acc  # Anser: 34224


if __name__ == "__main__":
    print(solve())
