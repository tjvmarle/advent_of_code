from Util.input import get_lines
import time
from typing import Dict, List, Tuple
from enum import Enum, auto


dirmap = {"R": (0, -1),
          "L": (0, 1),
          "U": (-1, 0),
          "D": (1, 0), }


nr2dir = {"0": "R",
          "1": "D",
          "2": "L",
          "3": "U",
          }


class Line:
    def __init__(self, begin, end, position) -> None:
        self.begin = begin
        self.end = end
        self.position = position  # x for vert lines, y for horiz lines
        pass


def traverse(norm_coordinates: List[Tuple[int, int]], horiz_lines: List[Line], vert_lines: List[Line]):
    # we need all coordinates (normalized) and all horiz/vert lines.

    norm_coordinates.append((-1, -1))
    any_x, curr_row = norm_coordinates.pop(0)
    x_points = [any_x]
    while norm_coordinates[0][1] == curr_row:
        x_points.append(norm_coordinates.pop()[0])

    # TODO:
    # Grab all horizontal lines for the current row.
    # Check if we cross any vertical ones

    while True:
        #
        next_x, any_y = norm_coordinates[1]

        while curr_row == any_y:
            ...
        ...
    ...


def solve() -> int:
    # gen = get_lines(tst=False)
    gen = get_lines(tst=True)

    # First save all coördinates
    coord_list = [[0, 0]]
    min_x = 0
    min_y = 0
    for line in gen:
        _, nr = line.split("#")
        dir_char = nr2dir[nr[-2]]
        dir = dirmap[dir_char]

        steps = int(nr[:-2], 16)
        curr_x, curr_y = coord_list[-1]
        move_x, move_y = dir[0], dir[1]
        new_x, new_y = curr_x + move_x * steps, curr_y + move_y * steps
        min_x = min(min_x, new_x)
        min_y = min(min_y, new_y)

        coord_list.append([new_x, new_y])
    coord_list.pop()  # Otherwise start and end will be duplicate

    # Normalize them for easy calculations
    normalized_list = []
    for x, y in coord_list:
        norm_x, norm_y = x - min_x, y - min_y
        normalized_list.append([norm_x, norm_y])
    normalized_list = sorted(normalized_list, key=lambda pt: pt[1])

    vert_lines, horiz_lines = [], []
    prev_x, prev_y = normalized_list[0]
    for curr_x, curr_y in normalized_list[1:]:
        if prev_x == curr_x:
            vert_lines.append(Line(min(prev_y, curr_y), max(prev_y, curr_y), prev_x))
        else:
            horiz_lines.append(Line(min(prev_x, curr_x), max(prev_x, curr_x), prev_y))
        prev_x = curr_x
        prev_y = curr_y

    sorted_horizon = sorted(horiz_lines, key=lambda line: line.position)
    sorted_vertic = sorted(vert_lines, key=lambda line: line.position)

    # x_to_y_map, y_to_x_map = {}, {}
    # for k in x_to_y_map.keys():
    #     x_to_y_map[k] = sorted(x_to_y_map[k])

    # for k in y_to_x_map.keys():
    #     y_to_x_map[k] = sorted(y_to_x_map[k])

    # # Map every vertical line to their x-position
    # for key, value in x_to_y_map.items():
    #     for index in range(0, len(value), 2):
    #         vert_lines.append((value[index], value[index + 1], key))

    # # Map every horizontal  line to their y-position
    # for key, value in y_to_x_map.items():
    #     for index in range(0, len(value), 2):
    #         horiz_lines.append((value[index], value[index + 1], key))

    # TODO:
    # We can move top-down through the coördinates (sort them by y value, then by x)
    # If we hit a coördinate while also having crossed a line we can ignore the cöordinate and continue traversing
    # Every position will have an equal amount of points
    # We can also cross a line, but never between two connecting points (probably).
    # --> line-point, line-line, point-line

    # WARN:
    # There's a chance lines overlap. For safety reasons, calc the lines when normalizing the coordinates.
    # There could be a possibility that lines cross, although we assume they won't

    print(f"min_x: {min_x}, min_y: {min_y}")
    # print(f"coord_list: {coord_list}")
    print(f"normalized_list: {normalized_list}")
    # print(f"sorted_horizon: {sorted_horizon}")
    # print(f"x_to_y_map: {x_to_y_map}")
    # print(f"y_to_x_map: {y_to_x_map}")
    # print(f"horiz_lines: {horiz_lines}")
    for line in sorted_horizon:
        print(f"{line.begin} - {line.end} at row {line.position}.")

    acc: int = 0
    return acc


if __name__ == "__main__":
    now = time.time()
    print(f"Answer: {solve()}")
    delta = time.time() - now

    mins, secs = int(delta / 60), delta % 60
    time_str = ["Runtime: "]
    if mins:
        time_str.append(f"{mins}m ")
    time_str.append(f"{secs:.1f}s.")
    print("".join(time_str))
