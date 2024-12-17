from util.input import *  # Yeah yeah, blah blah
from typing import List, Tuple, Set, Dict
import cProfile
import re

RAX = 0
RBX = 0
RCX = 0
ISP = 0
OUT = []


def get_combo(operand) -> int:
    if 0 <= operand <= 3:
        return operand

    match operand:
        case 4:
            return RAX
        case 5:
            return RBX
        case 6:
            return RCX
        case _:
            raise NotImplementedError


def read_input(lines):
    global OUT, ISP, RAX, RBX, RCX

    OUT = []
    ISP = 0

    RAX = int(re.findall(r"\d+", next(lines))[0])  # Will be overwritten.
    RBX = int(re.findall(r"\d+", next(lines))[0])
    RCX = int(re.findall(r"\d+", next(lines))[0])
    next(lines)
    return [int(asm) for asm in re.findall(r"\d+", next(lines))]


def opcode_0(operand: int):
    """adv"""
    global RAX
    RAX = RAX // (2**get_combo(operand))


def opcode_1(operand: int):
    """bxl"""
    global RBX
    RBX = RBX ^ operand


def opcode_2(operand: int):
    """bst"""
    global RBX
    RBX = get_combo(operand) % 8


def opcode_3(operand: int):
    """jnz"""
    if RAX == 0:
        return

    global ISP
    ISP = operand
    ISP -= 2


def opcode_4(_: int):
    """bxc"""
    global RBX, RCX
    RBX = RBX ^ RCX


def opcode_5(operand: int):
    """out"""
    global OUT
    OUT.append(get_combo(operand) % 8)


def opcode_6(operand: int):
    """bdv"""
    global RAX, RBX
    RBX = RAX // (2**get_combo(operand))


def opcode_7(operand: int):
    """cdv"""
    global RAX, RCX
    RCX = RAX // (2**get_combo(operand))


opcodes = {0: opcode_0, 1: opcode_1, 2: opcode_2, 3: opcode_3, 4: opcode_4, 5: opcode_5, 6: opcode_6, 7: opcode_7}


def run_program(rax_value: int):
    global ISP, RAX
    lines = get_lines()
    program = read_input(lines)
    RAX = rax_value

    while True:
        try:
            opcode, operand = program[ISP], program[ISP + 1]
            opcodes[opcode](operand)
            ISP += 2

        except IndexError:
            return


def get_next_multis(exponent: int, previous_values: int, target_digit: int, location: int):

    # Multiple answers could lead to the correct current digit, but might result in a dead end later on.
    multis = []
    for multiplier in range(0, 8):
        next_rax = 8**exponent * multiplier + previous_values

        if next_rax == 0:  # Stupid first entry.
            continue

        run_program(next_rax)

        if OUT[location] == target_digit:
            multis.append(multiplier)

    return multis


# Although I haven't fully dissected the underlying logic, analyzing the data shows that each position corresponds to
# 8**n. For example, increments of 8**5 * i will change the 5th digit for i = range(0,8). Using a backwards search it
# should be possible to brute force each digit with a max of 8 attempts per digit.
def solve() -> int:

    global OUT, ISP
    target_output = [2, 4, 1, 6, 7, 5, 4, 4, 1, 7, 0, 3, 5, 5, 3, 0]
    possible_solutions: List[List[int]] = [[]]
    curr_exponent = len(target_output)

    while target_output:
        curr_exponent -= 1
        target_digit = target_output.pop(-1)

        new_solutions: List[List[int]] = []
        for solution in possible_solutions:
            next_multis = get_next_multis(curr_exponent, sum(solution), target_digit, len(target_output))

            # Lets take the clean appraoch of not modifying a list while iterating over it.
            for multi in next_multis:
                new_solution = list(solution)
                new_solution.append(8**curr_exponent * multi)
                new_solutions.append(new_solution)

        possible_solutions = new_solutions

    return min([sum(sol) for sol in possible_solutions])  # 47910079998866


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
