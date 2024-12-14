from util.input import *  # Yeah yeah, blah blah
from util.grid import Grid, Cell
from typing import List, Tuple
import cProfile
from operator import itemgetter
import re

import numpy as np
from PIL import Image


X_MAX = 101
X_HALF = X_MAX // 2
Y_MAX = 103
Y_HALF = Y_MAX // 2
ROBOT = 'O'
EMPTY = ' '


def solve() -> int:
    time = 0

    plain_grid = []
    for _ in range(Y_MAX):
        row = []
        for _ in range(X_MAX):
            row.append(EMPTY)
        plain_grid.append(row)

    starting_robots = []
    for line in get_lines():
        robot_start = tuple(int(pos) for pos in re.findall(r"-?\d+", line))
        starting_robots.append(robot_start)

    starting_robots = sorted(starting_robots, key=itemgetter(0))

    frame = [[None for x in range(10)] for y in range(10)]

    while True:
        grid = set()
        data = np.zeros((X_MAX, Y_MAX, 3), dtype=np.uint8)

        for px, py, vx, vy in starting_robots:
            final_x = (px + vx * time) % X_MAX
            final_y = (py + vy * time) % Y_MAX
            grid.add((final_x, final_y))
            data[final_x][final_y] = [0, 255, 0]

        # This allows us to inspect 100 images at once.
        image = Image.fromarray(data)
        x = time % 10
        y = time % 100 // 10
        frame[y][x] = image

        if time % 100 == 99:
            composite = Image.new('RGB', (X_MAX * 10, Y_MAX * 10))
            for y, row in enumerate(frame):
                for x, img in enumerate(row):
                    composite.paste(img, (x * img.width, y * img.height))

            composite.save(f"pics/tree_{time}.bmp")
        time += 1

        # This limit is arbitrarily. Will generate 100 images, each containing a 100 results.
        if time > 10000:
            print(f"Failed!")
            return 0  # It was hidden at 8087.


if __name__ == "__main__":
    # cProfile.run("print(solve())", "performance_data")
    print(solve())
