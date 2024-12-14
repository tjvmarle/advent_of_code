from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from enum import Enum, auto
import re


class ClawGame():
    COST_A = 3
    COST_B = 1
    MAX_PRESSES = 100

    def __init__(self, a, b, prize) -> None:
        self.a_x, self.a_y = [int(val) for val in re.findall(r'\d+', a)]
        self.b_x, self.b_y = [int(val) for val in re.findall(r'\d+', b)]
        self.prize_x, self.prize_y = [int(val) for val in re.findall(r'\d+', prize)]

    def __repr__(self) -> str:
        return f"self.a: {self.a_x},{self.a_y}, self.b: {self.b_x},{self.b_y}, prize: {self.prize_x},{self.prize_y}"

    def play_game(self):
        if (self.a_x + self.b_x) * ClawGame.MAX_PRESSES < self.prize_x or \
                (self.a_y + self.b_y) * ClawGame.MAX_PRESSES < self.prize_y:
            # Unwinnable, prize is out of range within 100 presses.
            return []

        # You can first check all combinations of x, then check if any of those will fit y.
        possible_x = []
        for counter_x in range(ClawGame.MAX_PRESSES):
            remaining_x = self.prize_x - self.a_x * counter_x
            if remaining_x % self.b_x == 0:
                # possible x solution!
                possible_x.append((counter_x, remaining_x // self.b_x))

        costs = []
        for a_counter_y, b_counter_y in possible_x:
            if a_counter_y * self.a_y + b_counter_y * self.b_y == self.prize_y:
                # Solution!
                costs.append(a_counter_y * ClawGame.COST_A + b_counter_y * ClawGame.COST_B)

        return costs


def get_game(lines) -> ClawGame | None:
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
        if solutions := game.play_game():
            acc += min(solutions)

    return acc  # 32026


if __name__ == "__main__":
    cProfile.run("print(solve())", "performance_data")
    # print(solve())
