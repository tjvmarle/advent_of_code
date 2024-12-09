from util.input import *  # Eat me
from typing import List
from random import shuffle


rules_map: dict[int, List[int]] = {}


def parse_rule(line: str):
    global rules_map
    before, after = [int(val) for val in line.split("|")]
    all_after = rules_map.get(before, [])
    all_after.append(after)

    rules_map[before] = all_after


def parse_update(line: str) -> tuple[bool, int]:
    global rules_map
    vals = [int(val) for val in line.split(",")]
    vals.reverse()

    middle = vals[(len(vals) - 1) // 2]
    while vals:
        val = vals.pop(0)
        all_after = rules_map.get(val, None)

        if not all_after:
            continue

        # Since we're checking in reverse. If any of the all_after-values is found in any of the remaining vals-list the
        # update is invalid.
        if len(set(all_after + vals)) < len(set(all_after)) + len(vals):
            return False, 0

    return True, middle


recursive_depth = 0
max_depth = 0


def fix_invalid_updates(update: List[int]):
    # For this part we can create our own bubble sort. Just check each value if they're in a correct position. If not,
    # move it to a valid position and restart the entire verification.

    # Validate each value from back to front, but check them against the list from front to back up to their own position.
    # If there is any clash, move the value in front of the first clashing value.

    global recursive_depth
    for rev_val in update[::-1]:
        for pos, val in enumerate(update):

            if rev_val == val:
                break  # We've reached our own position without any issues.

            if val in rules_map.get(rev_val, []):

                update.remove(rev_val)
                update.insert(pos, rev_val)

                recursive_depth += 1

                # We could just modify the list in a loop en try again, but recursion is more fun.
                return fix_invalid_updates(update)

    global max_depth
    max_depth = max(max_depth, recursive_depth)
    recursive_depth = 0

    return update


def solve() -> int:
    acc: int = 0

    lines = get_lines()
    invalid_lines = []
    for line in lines:
        if "|" in line:
            parse_rule(line)

        if "," in line:
            is_valid, _ = parse_update(line)

            if not is_valid:
                invalid_lines.append(line)

    for inv_line in invalid_lines:
        vals = [int(val) for val in inv_line.split(",")]

        fixed_vals = fix_invalid_updates(vals)
        acc += fixed_vals[(len(vals) - 1) // 2]

    print(f"Reached a maximum recursion of: {max_depth}")  # 22
    return acc  # 5479


if __name__ == "__main__":
    print(solve())
