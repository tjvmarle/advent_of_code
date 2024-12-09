from Util.input import get_lines
from typing import Tuple, List


class DeltaList:
    def __init__(self, numList: List[int]) -> None:
        self.deltas = [numList[curr + 1] - numList[curr] for curr in range(0, len(numList) - 1)]

    def solve(self) -> Tuple[int, int]:
        if all((val == 0 for val in self.deltas)):  # Breakout condition
            return (0, 0)

        up, down = DeltaList(self.deltas).solve()
        val_a = self.deltas[-1] + up  # 9a, counting up
        val_b = self.deltas[0] - down  # 9b, counting down
        return val_a, val_b


def solve() -> str:
    acc_a = acc_b = 0
    for line in get_lines():
        numlist = [int(num_str) for num_str in line.split()]
        up, down = DeltaList(numlist).solve()
        acc_a += numlist[-1] + up
        acc_b += numlist[0] - down

    return f"a: {acc_a}, b: {acc_b}"


if __name__ == "__main__":
    print(solve())
