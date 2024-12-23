from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple, Set, Dict
import re
import cProfile


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""
789
456
123
 0A
"""

"""
 ^A
<v>
"""

Pos = Tuple[int, int]

A: Pos = (2, 0)
Offset = Pos
numpad_to_pos: Dict[str, Pos] = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
                                 '4': (0, 1), '5': (1, 1), '6': (2, 1),
                                 '1': (0, 2), '2': (1, 2), '3': (2, 2),
                                              '0': (1, 3), 'A': (2, 3)}

# E.g.: moving right is an offset of (1,0). This requires the '<' button, located at position (2,1)
direction_to_pos: Dict[Offset, Pos] = {UP: (1, 0),  # up
                                       LEFT: (0, 1),  # left
                                       DOWN: (1, 1),  # down
                                       RIGHT: (2, 1),  # right
                                       'A': (2, 0)}  # A

direction_to_char: Dict[Offset, str] = {UP: '^',  # up
                                        LEFT: '<',  # left
                                        DOWN: 'v',  # down
                                        'A': 'A',  # down
                                        RIGHT: '>'}  # right


def delta_pos(current_pos: Pos, target_pos: Pos) -> Pos:
    curr_x, curr_y = current_pos
    target_x, target_y = target_pos
    return target_x - curr_x, target_y - curr_y


def delta_to_moves(delta: Offset) -> List[Offset]:
    delta_x, delta_y = delta
    offset_x = 1 if delta_x > 0 else -1
    offset_y = 1 if delta_y > 0 else -1

    move_list: List[Offset] = []

    for _ in range(abs(delta_x)):
        move_list.append((offset_x, 0))

    for _ in range(abs(delta_y)):
        move_list.append((0, offset_y))

    return move_list


# Prioritize directions moving away from the empty space
move_prio_numpad: Dict[Offset, int] = {UP: 0, RIGHT: 0, DOWN: 1, LEFT: 1}
move_prio_dirpad: Dict[Offset, int] = {UP: 1, RIGHT: 0, DOWN: 0, LEFT: 1}


def sort_numpad_moves(movelist: List[Offset], current_pos: Pos) -> List[Offset]:

    current_pos_in_left_column = current_pos[0] == 0
    current_pos_in_bottom_row = current_pos[1] == 3

    # We'd still like to douple tap a move if possible.
    if current_pos_in_left_column or current_pos_in_bottom_row:
        return sorted(movelist, key=lambda move: move_prio_numpad[move])

    return movelist


def sort_moves(movelist: List[Offset], current_pos: Pos, sort_numpad: bool) -> List[Offset]:
    # TODO: The optimal order depends on the current position of the next robot. Preferably you hit the same button
    # multiple times if possible. However, this must still avoid the empty space, so you can't:
    # * double tap a left on the bottom numpad row
    # * double tap a left on the top dirpad row
    # * double tap a down on the left numpad column
    # Other than that the order of operation doesn't seem to matter that mucht (yet).
    # We'd still like to douple tap a move if possible.

    current_pos_in_left_column = (current_pos[0] == 0)

    if sort_numpad:
        current_pos_in_bottom_row = (current_pos[1] == 3)

        if current_pos_in_left_column or current_pos_in_bottom_row:
            return sorted(movelist, key=lambda move: move_prio_numpad[move])
    else:
        current_pos_in_top_row = (current_pos[1] == 0)
        if current_pos_in_top_row:
            return sorted(movelist, key=lambda move: move_prio_dirpad[move])

    return movelist

    # No need for any other sorting, since the move generator automatically appends doubles together.
    # print(f"***** curren_pos: {curren_pos}, before list: {movelist}, sorted_list: {sorted_list}")


def solve() -> int:
    acc: int = 0

    numpad_robot_pos = numpad_to_pos['A']
    directional_robot_a_pos = direction_to_pos['A']
    directional_robot_b_pos = direction_to_pos['A']

    lines = get_lines()
    # lines = get_lines(True)
    num_list: List[int] = []
    code_list: List[List[str]] = []

    for line in lines:
        num_list.append(int(*re.findall(r"\d+", line)))

        code = []
        for char in line:
            code.append(char)
            # code.append('A')
        code_list.append(code)

    for index, code in enumerate(code_list):
        self_press_list = []
        char_press_list = []
        dir_a_press_list = []
        dir_b_press_list = []
        for char in code:
            next_numpad_pos = numpad_to_pos[char]
            numpad_delta = delta_pos(numpad_robot_pos, next_numpad_pos)

            numpad_moves = sort_moves(delta_to_moves(numpad_delta), numpad_robot_pos, True)
            # print(
            #     f"numpad_robot_pos: {numpad_robot_pos}, next_numpad_pos:{next_numpad_pos}, numpad_delta: {
            #         numpad_delta}, numpad_moves: {numpad_moves}")
            numpad_moves.append('A')
            numpad_robot_pos = next_numpad_pos

            char_press_list.append(char)
            # print(f"Numpad, moving to: {char}, moves: {[direction_to_char[move] for move in numpad_moves]}")

            for dir_a_move in numpad_moves:
                # if dir_a_move == 'A':
                #     print(f"  Pressing 'A', current numpad button: {numpad_robot_pos}")

                next_dir_a_pos = direction_to_pos[dir_a_move]
                dir_a_delta = delta_pos(directional_robot_a_pos, next_dir_a_pos)
                # dir_a_moves = delta_to_moves(dir_a_delta)
                dir_a_moves = sort_moves(delta_to_moves(dir_a_delta), directional_robot_a_pos, False)
                dir_a_moves.append('A')

                # print(f"  Robot A, moving from {directional_robot_a_pos} to: {
                # direction_to_char[dir_a_move]}, numpad_moves: {[direction_to_char[move]
                # for move in dir_a_moves]}")

                directional_robot_a_pos = next_dir_a_pos

                dir_a_press_list.append(direction_to_char[dir_a_move])

                for dir_b_move in dir_a_moves:
                    next_dir_b_pos = direction_to_pos[dir_b_move]
                    dir_b_delta = delta_pos(directional_robot_b_pos, next_dir_b_pos)
                    dir_b_moves = delta_to_moves(dir_b_delta)
                    dir_b_moves = sort_moves(delta_to_moves(dir_b_delta), directional_robot_b_pos, False)
                    dir_b_moves.append('A')

                    # print(f"    Robot B, moving from {directional_robot_b_pos} to: {
                    # direction_to_char[dir_b_move]}, numpad_moves:{[direction_to_char[move] for move in dir_b_moves]}")

                    directional_robot_b_pos = next_dir_b_pos

                    dir_b_press_list.append(direction_to_char[dir_b_move])

                    for move_press in dir_b_moves:
                        # print(f"      Pressing {direction_to_char[move_press]}")
                        self_press_list.append(direction_to_char[move_press])

        acc += len(self_press_list) * num_list[index]
        print(f"{len(self_press_list)} * {num_list[index]}: {''.join(self_press_list)}")
        # print(f"{''.join(dir_b_press_list)}")
        # print(f"{''.join(dir_a_press_list)}")
        # print(f"{''.join(char_press_list)}")

        # print(f"\n")

    return acc
    # Too high: 184390


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
