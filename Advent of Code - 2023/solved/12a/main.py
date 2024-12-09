from Util.input import get_lines
from typing import Tuple, Dict, List, Set

import re

MULTIPLIER = 5


class RegexChecker:
    """Creates and checks regex-strings for a given input"""

    def __init__(self, line: str) -> None:
        self.spring_str, dmg_set = line.split()
        self.dmg_lst = [int(spring) for spring in dmg_set.split(",")]

    def permute(self, digits: int, remaining: int):
        """
        Find all possible combinations to divide 'remaining' over 'digits' positions.
        E.g.: 4, 6 --> divide '6' over 4 position: 0006, 0015, 0105, 1005, etc. Order matters, 1005 != 5001
        """
        # Yoinked straight from SO.
        # Credits to https://mathoverflow.net/questions/9477/

        if remaining < 0 or digits < 0:
            return "Error"
        if not remaining:
            return [[0] * digits]
        if not digits:
            return []
        if digits == 1:
            return [[remaining]]
        return [[0] + val for val in self.permute(digits - 1, remaining)] + \
            [[val[0] + 1] + val[1:] for val in self.permute(digits, remaining - 1)]

    def get_regex(self) -> str:
        # Create regex strings to exhaustively match every possible combination based purely on the dmg_lst.

        def ops(cnt): return f"[?.]{{{cnt}}}"   # Operational springs, for which we'll try all combinations.
        def dmg(cnt): return f"[?#]{{{cnt}}}"   # These counts are the given values, the damaged springs.

        # Any given input set needs to be alternated with an entry for possible ops
        # E.g. 6,4,3 --> 0,6,1,4,1,3,0 as a base. Matching ops and dmg alternatingly.
        # Edge-ops can start at 0, but the in-between ops need to be at least 1.
        # Count total nr of chars. Divide remaining number over ops.
        rgx_mask = [1 for _ in range(len(self.dmg_lst))]
        rgx_mask.append(0)
        rgx_mask[0] = 0   # First and last are now 0, rest is 1.

        # This count needs to be divided over the rgx_mask, for all possible solutions.
        remaining = len(self.spring_str) - sum(self.dmg_lst) - sum(rgx_mask)

        masks = self.permute(len(rgx_mask), remaining)

        for mask in masks:
            for index, _ in enumerate(mask):
                mask[index] += rgx_mask[index]

        acc: int = 0
        dmg_rgxs = [dmg(cnt) for cnt in self.dmg_lst]  # This is a constant for the object.
        for mask in masks:
            ops_rgxs = [ops(cnt) for cnt in mask]
            rgx_list = [None] * (len(dmg_rgxs) + len(ops_rgxs))
            rgx_list[::2] = ops_rgxs
            rgx_list[1::2] = dmg_rgxs

            regex_try = "".join([str(rgx) for rgx in rgx_list])
            if re.search(regex_try, self.spring_str):
                acc += 1

        return acc


def solve() -> int:
    gen = get_lines(tst=True)
    acc: int = 0

    for entry in gen:
        acc += RegexChecker(entry).get_regex()

    return acc


if __name__ == "__main__":
    print(solve())
