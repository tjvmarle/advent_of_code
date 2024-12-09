from Util.input import get_lines
from typing import Tuple, Dict, List, Set
from functools import reduce
import re

# MULTIPLIER = 5
cntr = 0
curr_spring = ""


# Create a right-most fit
# Move the left group one to the left. This gets a multiplier .
# Grab the remaining string and repeat the process

def fits(in_set: List[int], ref_set: List[int]) -> bool:
    # in:[1,1,1,1] fits in [1,3,1]

    ...


def fit_prefix(prefix: List[int], remainder: List[int]) -> bool:
    # TODO: We need the entire spring-string here to correctly match the prefix on the "#"
    # We can use the fits() function for the partial matches

    # Try to fit the prefix and check if the remaining string can still fit the remainder-sets

    # Fully regex the current prefix and unmodified remainder. If it doesn't match, then the prefix is invalid
    # return True
    rgx_lst = [f"[?#]{{{cnt}}}" for cnt in prefix]
    for rem in remainder:
        rgx_lst.append(f"[?#]{{{rem}}}")

    rgx_str = "[?.]+".join(rgx_lst)
    res_rgx = re.findall(rgx_str, curr_spring)

    return bool(res_rgx)


def permute_sets(setlist: List[int], ref_max) -> List[List[int]]:
    """Create all summation-permutation of a list of spring-groupings. E.g. 3,1,1,1 becomes 5,1,1; 3,3,1; 3,1,3; etc."""
    new_sets = []

    for sum_index in range(len(setlist) - 1):
        res = setlist[sum_index] + setlist[sum_index + 1] + 1
        if res > ref_max:
            continue

        # TODO: if the prefix leaves no room for the remainder there's no need to permute further on this prefix
        prefix = setlist[:sum_index]
        remainder = setlist[sum_index + 2:]
        if not fit_prefix(prefix + [res], remainder):
            continue

        new_sets.append(prefix + [res] + remainder)

        for suffix in permute_sets([res] + remainder, ref_max):
            new_sets.append(prefix + suffix)

    return new_sets


def find_right_most(pattern: List[int]):
    print(f"{curr_spring}")

    rgx_lst = [f"[?#]{{{cnt}}}" for cnt in pattern]
    regex_suffix = "[?.]+?".join(rgx_lst[1:])

    # TODO:
    # Only match a single group, but check if the remaining string can fit the remaining groups
    # Determine the remaining string and recursively call this function
    # Figure out how to add/calc the multipliers.

    filler_counter = 1
    matches_found = 0
    while True:
        regex_prefix = f"{rgx_lst[0]}[?.]{{{filler_counter}}}"
        re_match = re.search(regex_prefix, curr_spring)

        if not re_match:
            break

        start, end = re_match.span()
        remaining_start = curr_spring[:start]
        matched_str = curr_spring[start:end]
        remaining_end = curr_spring[end:]

        re_rest = re.search(regex_suffix, remaining_end)  # drop 1 char for the remaining part.
        if not re_rest:
            print(f"No remaining matches")
            break

        print(f"\tregex_prefix: {regex_prefix}\n\tmatch: {matched_str}\n\tremaining: {remaining_end}\n")
        # print(f"re.match(): {re_match}")
        # print(regex_prefix)

        matches_found += 1
        filler_counter += 1

    print(f"Found {matches_found} matches on {regex_prefix}.")


def solve() -> int:
    gen = get_lines(tst=True)
    MULTI = 5

    # line = next(gen)
    cntr = 0

    for line in gen:
        cntr += 1

        spring_base, sets = line.split()
        springs = "?".join([spring_base] * MULTI)

        global curr_spring
        curr_spring = springs
        # print(f"curr_spring: {curr_spring}")

        # spring_list = [spring_group for spring_group in springs.split(".") if spring_group]
        # ref_set = [len(entry) for entry in spring_list]

        group_list = [int(val_str) for val_str in sets.split(",")] * MULTI
        find_right_most(group_list)

        # all_sets = permute_sets(set_list, max(ref_set))

    acc: int = 0

    return acc


if __name__ == "__main__":
    print(solve())
