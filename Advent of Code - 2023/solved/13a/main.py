from Util.input import get_lines
from typing import Dict, List


def get_pattern():
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


def find_reflection(pattern):
    for line_index in range(0, len(pattern) - 1):
        if pattern[line_index] != pattern[line_index + 1]:
            continue

        offset: int = 1
        while True:  # Reflection found, keep checking until you hit an edge or find two unequal lines.
            if line_index - offset < 0 or line_index + 1 + offset > len(pattern) - 1:
                return (line_index + 1, line_index + 2)  # Edge hit, full reflection found.

            if pattern[line_index - offset] != pattern[line_index + 1 + offset]:
                break  # No reflection, continue search

            offset += 1

    return False


def transpose_pattern(pattern):
    """First line becomes first column, etc. Assumes the pattern is rectangular."""
    return ["".join(line) for line in zip(*pattern)]


def solve() -> int:
    pttrn_gen = get_pattern()

    acc: int = 0
    for pattern in pttrn_gen:

        if res := find_reflection(pattern):
            row_a, _ = res
            acc += row_a * 100
        else:
            row_a, _ = find_reflection(transpose_pattern(pattern))
            acc += row_a

    return acc


if __name__ == "__main__":
    print(solve())
