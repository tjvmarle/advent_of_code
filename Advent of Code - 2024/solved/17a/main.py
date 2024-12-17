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
    global RAX, RBX, RCX

    RAX = int(re.findall(r"\d+", next(lines))[0])
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
    OUT.append(str(get_combo(operand) % 8))


def opcode_6(operand: int):
    """bdv"""
    global RAX, RBX
    RBX = RAX // (2**get_combo(operand))


def opcode_7(operand: int):
    """cdv"""
    global RAX, RCX
    RCX = RAX // (2**get_combo(operand))


opcodes = {0: opcode_0, 1: opcode_1, 2: opcode_2, 3: opcode_3, 4: opcode_4, 5: opcode_5, 6: opcode_6, 7: opcode_7}


# Nothing too difficult. Just implement the operations and run the program.
def solve() -> str:
    lines = get_lines()
    # lines = get_lines(True)
    program = read_input(lines)

    try:
        global ISP
        while True:
            opcode, operand = program[ISP], program[ISP + 1]
            opcodes[opcode](operand)
            ISP += 2

    except IndexError:
        return ','.join(OUT)  # 1,5,0,1,7,4,1,0,3


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
