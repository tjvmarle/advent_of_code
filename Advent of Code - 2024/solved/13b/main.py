from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from enum import Enum, auto
import re


OFFSET = 10000000000000


class ClawGame():
    """Contains a parser, the data and a solver."""
    COST_A = 3
    COST_B = 1

    def __init__(self, a_button_line, b_button_line, prize_line) -> None:
        """Does some basic regex parsing of the input to retrieve the relevant data for the clawgame."""

        self.a_x, self.a_y = [int(val) for val in re.findall(r'\d+', a_button_line)]
        self.b_x, self.b_y = [int(val) for val in re.findall(r'\d+', b_button_line)]
        self.prize_x, self.prize_y = [int(val) + OFFSET for val in re.findall(r'\d+', prize_line)]

    def __repr__(self) -> str:
        return f"self.a: {self.a_x},{self.a_y}, self.b: {self.b_x},{self.b_y}, prize: {self.prize_x},{self.prize_y}"

    def play_game(self):
        """Solves the required steps (if possible) and cost to win the claw game.

        Basic assumption is that every game with a solution only has a single solution. This isn't guaranteed if the
        button vectors align exactly with eachother (e.g. (2,5) and (60,150)). This could invalidate our attempt, as
        this could skew the cost. If that turns out to be the case we can easily fix that in the constructor.
        --> turns out we didn't need to do that."""

        # Values are too high to brute force. However, we have two equations with two unknowns, which can be solved.
        #   prize_x = but_a_x * press_a + but_b_x * press_b
        #   prize_y = but_a_y * press_a + but_b_y * press_b

        # After some quick maths. We need to round due to induced floating-point conversions.
        a_presses = round((self.prize_x - (self.b_x * self.prize_y) / self.b_y) /
                          (self.a_x - (self.a_y * self.b_x) / self.b_y))

        # Just invert all the constants of the previous equation.
        b_presses = round((self.prize_y - (self.a_y * self.prize_x) / self.a_x) /
                          (self.b_y - (self.b_x * self.a_y) / self.a_x))

        if a_presses < 0 or b_presses < 0:
            return 0  # We can't 'unpress' a button.

        # We re-check the calculated presses against the prize value just in case rounding induced some error.
        if a_presses * self.a_x + b_presses * self.b_x == self.prize_x and \
           a_presses * self.a_y + b_presses * self.b_y == self.prize_y:
            return a_presses * ClawGame.COST_A + b_presses * ClawGame.COST_B

        return 0  # No solution or perhaps a rounding error, which we'll fix if our solution gets rejected.


def get_game(lines) -> ClawGame | None:
    """Reads the input file and converts it into a clawgame."""
    game = []
    for line in lines:
        if not line:
            continue

        game.append(line)
        if 'Prize' in line:
            break

    if not game:
        return None

    button_a, button_b, prize = game

    return ClawGame(button_a, button_b, prize)


def solve() -> int:
    lines = get_lines()
    # lines = get_lines(True)

    acc: int = 0

    while game := get_game(lines):
        acc += game.play_game()

    return acc  # 89013607072065


if __name__ == "__main__":
    cProfile.run("print(solve())", "performance_data")
    # print(solve())
