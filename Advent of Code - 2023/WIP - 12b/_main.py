from Util.input import get_lines
from typing import Dict, List
import time


def solve() -> int:
    gen = get_lines(tst=True)
    for line in gen:
        springs_1, groups_1 = line.split()
        springs_5 = "?".join([springs_1] * 5)
        groups_5 = ",".join([groups_1] * 5)
        print(f"{springs_5} {groups_5}")

    acc: int = 0
    return acc


if __name__ == "__main__":
    now = time.time()
    print(f"Answer: {solve()}")
    delta = time.time() - now

    mins, secs = int(delta / 60), delta % 60
    time_str = ["Runtime: "]
    if mins:
        time_str.append(f"{mins}m ")
    time_str.append(f"{secs:.1f}s.")
    print("".join(time_str))
