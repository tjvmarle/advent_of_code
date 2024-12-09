from util.input import *  # Eat me
from typing import List


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


def solve() -> int:
    acc: int = 0

    lines = get_lines()
    for line in lines:
        if "|" in line:
            parse_rule(line)

        if "," in line:
            is_valid, middle_val = parse_update(line)
            acc += middle_val if is_valid else 0

    return acc


if __name__ == "__main__":
    print(solve())
