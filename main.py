from util.input import *  # # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set
import cProfile
from operator import itemgetter, attrgetter
import numpy as np
from functools import reduce

rules_map: dict[int, List[int]] = {}

WALL = '#'
EMPTY = '.'
BLOCK = 'O'
BLOCKS = ['[', ']']
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
        if we_ve_got_the_moves:
            moves.append([char for char in line])
        else:
            row = []
            for char in line:
                if char == BLOCK:
                    row.append('[')
                    row.append(']')
                elif char == ROBOT:
                    row.append(ROBOT)
                    row.append(EMPTY)
                else:
                    row.append(char)
                    row.append(char)
            grid.append(row)

        if ROBOT in grid[-1]:
            x_index = grid[-1].index(ROBOT)
            robo_start = (x_index, y_index)

        y_index += 1

    flat_moves = []
    for movelist in moves:
        for move in movelist:
            flat_moves.append(move)
    return grid, flat_moves, robo_start


def get_other_half(warehouse: Grid, current_block_half: Cell) -> Cell | None:
    offset_x, _ = move_map['>' if current_block_half.get_value() == BLOCKS[0] else '<']
    return warehouse.get_cell(current_block_half.x_pos + offset_x, current_block_half.y_pos)  # y-pos doesn't change


move_failed = set(), False


def check_next_for_blocks(warehouse: Grid, curr_block_cell: Cell, direction: Tuple[int, int]) -> Tuple[Set[Cell], bool]:
    # This is only for detecting when moving up or down.

    #       #
    #      []
    #   [][]
    #    []
    #   []
    #   []
    #    @  ^

    moveable_cells = set([curr_block_cell])

    # if next is block, check both for the next layer. If any hit a wall, the entire stack won't move.
    move_x, move_y = direction
    next_layer_cell = warehouse.get_cell(curr_block_cell.x_pos, curr_block_cell.y_pos + move_y)

    if (next_layer_cell_val := next_layer_cell.get_value()) == WALL:
        # No movement possible.
        return move_failed

    if next_layer_cell_val == EMPTY:
        # Possible candidate to move current cell value into.
        # moveable_cells.add(next_layer_cell)
        return moveable_cells, True

    if next_layer_cell_val in BLOCKS:
        next_layer_moveable_cells, move_possible = check_next_for_blocks(warehouse, next_layer_cell, direction)

        if not move_possible:
            return move_failed
        moveable_cells.update(next_layer_moveable_cells)

        next_layer_other_half = get_other_half(warehouse, next_layer_cell)
        if next_layer_other_half not in moveable_cells:
            # This saves a bunch of duplicate searching due to the branching nature of the search.
            next_layer_moveable_cells, move_possible = check_next_for_blocks(warehouse,
                                                                             next_layer_other_half,
                                                                             direction)

        if not move_possible:
            return move_failed

        moveable_cells.update(next_layer_moveable_cells)

    return moveable_cells, True


def move_stack(warehouse: Grid, stack: Set[Cell], move_down: bool):
    # Move the stack of movable blocks.
    # Convert to list. Order top/bottom or other way around, depending on the direction moved.

    move_steps = sorted(list(stack), key=attrgetter('y_pos', 'x_pos'), reverse=move_down)
    # print(f"Sorted step list: {move_steps}")

    # Every item in this list is guaranteed to be able to move up/down one cell.
    move_offset = 1 if move_down else -1

    for cell_to_move in move_steps:
        next_x, next_y = cell_to_move.x_pos, cell_to_move.y_pos + move_offset

        # print(f"moving {cell_to_move} to {next_x, next_y}")
        warehouse.set_val(next_x, next_y, cell_to_move.get_value())

    # This is the block directly adjacent to the robot. One of these will be filled by the robot later.
    warehouse.set_val(*move_steps[-1].get_pos(), EMPTY)
    warehouse.set_val(*move_steps[-2].get_pos(), EMPTY)


def move_blocks(warehouse: Grid, robo_cell: Cell, direction: Tuple[int, int]):

    move_x, move_y = direction
    next_cell = warehouse.get_cell(robo_cell.x_pos + move_x, robo_cell.y_pos + move_y)

    while next_cell.get_value() != EMPTY:
        if next_cell.get_value() == WALL:
            # Blocks all the way to the wall.
            return robo_cell

        if (block_half := next_cell.get_value()) in BLOCKS:

            if up_down := (direction in (move_map['^'], move_map['v'])):
                # Moving up or down
                offset_x, offset_y = move_map['>' if block_half == BLOCKS[0] else '<']
                other_block_half = warehouse.get_cell(next_cell.x_pos + offset_x, next_cell.y_pos + offset_y)
                moveable_cells, move_possible = check_next_for_blocks(warehouse, next_cell, direction)

                if not move_possible:
                    # print(f"1: Move failed due to hitting a wall.")
                    return robo_cell

                if other_block_half not in moveable_cells:
                    more_moveable_cells, move_possible = check_next_for_blocks(warehouse, other_block_half, direction)

                    if not move_possible:
                        # print(f"2: Move failed due to hitting a wall.")
                        return robo_cell
                    moveable_cells.update(more_moveable_cells)

                    # TODO: This only moves the blocks. Don't forget to move the robot.
                    move_stack(warehouse, moveable_cells, direction == (0, 1))
                    break

            else:
                # Moving left/right
                next_cell = warehouse.get_cell(next_cell.x_pos + move_x, next_cell.y_pos + move_y)

    if not up_down:
        # We need to walk back and invert all the blocks.
        raise NotImplementedError
        ...

    # TODO: correctly move blocks sideways
    # next_cell.set_value(BLOCK)
    robo_cell.set_value(EMPTY)
    next_robo_cell = warehouse.get_cell(robo_cell.x_pos + move_x, robo_cell.y_pos + move_y)
    next_robo_cell.set_value(ROBOT)
    return next_robo_cell


def solve() -> int:
    acc: int = 0

    # lines = get_lines_as_grid()
    lines = get_lines_as_grid(True)

    grid, moves, robo_pos = get_grid_and_moves(lines)
    warehouse = Grid(grid)
    robo_cell = warehouse.get_cell(*robo_pos)

    while moves:
        robo_x, robo_y = robo_cell.get_pos()
        curr_move = moves.pop(0)
        print(f"curr_move: {curr_move}")
        warehouse.print()
        move_x, move_y = move_map[curr_move]

        if (next_cell := warehouse.get_cell(robo_x + move_x, robo_y + move_y)).get_value() == WALL:
            continue

        if next_cell.get_value() == EMPTY:
            next_cell.set_value(ROBOT)
            robo_cell.set_value(EMPTY)
            robo_cell = next_cell
            continue

        if next_cell.get_value() in BLOCKS:
            # Move blocks in the direction if possible
            robo_cell = move_blocks(warehouse, robo_cell, (move_x, move_y))
            continue

    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell.get_value() not in BLOCKS:
                continue

            acc += y * 100 + x

    print(f"\nFinal state:")
    warehouse.print()

    print(f"\n Don't forget you've changed the testdata. Both grid and input moves.")

    return acc  # 1461806


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
