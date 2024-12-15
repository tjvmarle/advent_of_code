from util.input import *  # # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from enum import Enum, auto
import numpy as np
from functools import reduce

rules_map: dict[int, List[int]] = {}

WALL = '#'
EMPTY = '.'
BLOCK = 'O'
ROBOT = '@'

move_map = {'<': (-1, 0), 'v': (0, 1), '>': (1, 0), '^': (0, -1)}


def get_grid_and_moves(lines):

    grid = []
    moves = []
    we_ve_got_the_moves = False  # Let's do it again ⚡📞👦🏼!

    y_index = 0
    robo_start = ()
    for line in lines:

        if line == []:
            we_ve_got_the_moves = True
            continue

        # Lol, I can't believe this works, although I'm also not suprised it does.
        (moves if we_ve_got_the_moves else grid).append([char for char in line])

        if ROBOT in grid[-1]:
            x_index = grid[-1].index(ROBOT)
            robo_start = (x_index, y_index)

        y_index += 1

    flat_moves = []
    for movelist in moves:
        for move in movelist:
            flat_moves.append(move)
    return grid, flat_moves, robo_start


def move_blocks(warehouse: Grid, robo_cell: Cell, direction: Tuple[int, int]):

    move_x, move_y = direction
    next_cell = warehouse.get_cell(robo_cell.x_pos + move_x, robo_cell.y_pos + move_y)

    while next_cell.get_value() != EMPTY:
        if next_cell.get_value() == WALL:
            # Blocks all the way to the wall.
            return robo_cell

        if next_cell.get_value() == BLOCK:
            next_cell = warehouse.get_cell(next_cell.x_pos + move_x, next_cell.y_pos + move_y)
            continue

    # We've hit an empty space. We don't need to rewalk the entire line:
    # * This function is only called if we've hit at least one block.
    # * We only need to fill the current empty space with a block and move the robot one cell.

    next_cell.set_value(BLOCK)
    robo_cell.set_value(EMPTY)
    next_robo_cell = warehouse.get_cell(robo_cell.x_pos + move_x, robo_cell.y_pos + move_y)
    next_robo_cell.set_value(ROBOT)
    return next_robo_cell


def solve() -> int:
    acc: int = 0

    lines = get_lines_as_grid()
    # lines = get_lines_as_grid(True)

    grid, moves, robo_pos = get_grid_and_moves(lines)
    warehouse = Grid(grid)
    robo_cell = warehouse.get_cell(*robo_pos)

    while moves:
        robo_x, robo_y = robo_cell.get_pos()
        move_x, move_y = move_map[moves.pop(0)]

        if (next_cell := warehouse.get_cell(robo_x + move_x, robo_y + move_y)).get_value() == WALL:
            continue

        if next_cell.get_value() == EMPTY:
            next_cell.set_value(ROBOT)
            robo_cell.set_value(EMPTY)
            robo_cell = next_cell
            continue

        if next_cell.get_value() == BLOCK:
            # Move blocks in the direction if possible
            robo_cell = move_blocks(warehouse, robo_cell, (move_x, move_y))
            continue

    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell.get_value() != BLOCK:
                continue

            acc += y * 100 + x

    return acc  # 1461806


if __name__ == "__main__":
    cProfile.run("print(solve())", "performance_data")
    # print(solve())
