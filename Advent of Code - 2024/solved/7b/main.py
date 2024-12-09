from util.input import *  # Eat me
from typing import List, Tuple


def add(left, right): return left + right
def multi(left, right): return left * right
def concat(left, right): return int(f"{left}{right}")


def print_equation(nrs, ops, expected):
    msg = [str(nrs[0])]

    for index, op in enumerate(ops):
        msg.append('+' if op == add else '*' if op == multi else '||')
        msg.append(str(nrs[index + 1]))

    curr_result = nrs[0]
    for index, operation in enumerate(ops):
        curr_result = operation(curr_result, nrs[index + 1])

    print(f"Calculating: {''.join(msg)}; {curr_result}, expecting {expected}")


def decimal_to_trinary(decimal) -> str:

    digits = []
    while decimal:
        digits.append(decimal % 3)  # First iteration will give you 'n x 3**0'
        decimal //= 3

    # Reverse the list, since the first entry was 3**0, the second 3**1, etc.
    return "".join(str(digit) for digit in digits[::-1])


ops_map = {'0': add,
           '1': multi,
           '2': concat}


def calc_ops(result, nrs) -> bool:
    ops_count = len(nrs) - 1

    for permutation in range(3**ops_count):
        ops_mask = decimal_to_trinary(permutation).rjust(len(nrs) - 1, '0')
        ops_list = [ops_map[ops] for ops in ops_mask]

        curr_result = nrs[0]
        for index, operation in enumerate(ops_list):
            curr_result = operation(curr_result, nrs[index + 1])

            if curr_result > result:  # Minor optimization
                break

        if result == curr_result:
            # print_equation(nrs, ops_list, result)
            return True

    return False


# Yay, tristates.
def solve() -> int:
    acc: int = 0

    # lines = get_lines(True)
    lines = get_lines()

    cntr = 1
    for line in lines:
        print(f"Calculating line {cntr}.")
        cntr += 1
        result, nrs = line.split(":")
        result = int(result)
        nrs = [int(nr) for nr in nrs.split()]

        acc += result if calc_ops(result, nrs) else 0

    return acc  # 150077710195188, took a minute or so


if __name__ == "__main__":
    print(solve())
