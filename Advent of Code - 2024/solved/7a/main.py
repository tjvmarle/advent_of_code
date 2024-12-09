from util.input import *  # Eat me
from typing import List, Tuple


def add(left, right): return left + right
def multi(left, right): return left * right


def print_equation(nrs, ops, expected):
    msg = [str(nrs[0])]

    for index, op in enumerate(ops):
        msg.append('+' if op == add else '*')
        msg.append(str(nrs[index + 1]))

    curr_result = nrs[0]
    for index, operation in enumerate(ops):
        curr_result = operation(curr_result, nrs[index + 1])

    print(f"Calculating: {''.join(msg)} - {curr_result}, expecting {expected}")


def calc_ops(result, nrs) -> bool:
    ops_count = len(nrs) - 1

    for permutation in range(2**ops_count):
        ops_mask = f"{f'{permutation:b}':0>{ops_count}}"  # Decimal to '0'-leftpadded binary string.
        ops_list = [add if ops == '0' else multi for ops in ops_mask]  # Yay, functions are also objects.

        curr_result = nrs[0]
        for index, operation in enumerate(ops_list):
            curr_result = operation(curr_result, nrs[index + 1])

        # print_equation(nrs, ops_list, result)
        if result == curr_result:
            return True

    return False


# Brute forcing it again. Just bitmask the operations and exhaust all options. If it gets too slow, eary break when the
# current answer > expected answer.
def solve() -> int:
    acc: int = 0

    # lines = get_lines(True)
    lines = get_lines()

    for line in lines:
        result, nrs = line.split(":")
        result = int(result)
        nrs = [int(nr) for nr in nrs.split()]

        acc += result if calc_ops(result, nrs) else 0

    return acc  # 1985268524462


if __name__ == "__main__":
    print(solve())
