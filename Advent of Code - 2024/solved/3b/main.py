from util.input import *  # Eat me
from typing import List

import re


def solve() -> int:
    acc: int = 0

    lines = get_lines()

    enabled = True
    for line in lines:
        chunks = line.replace(")", ")\n").split("\n")

        for chunk in chunks:
            chunk = chunk.strip()
            if "do()" in chunk:
                enabled = True
                continue

            if "don't()" in chunk:
                enabled = False
                continue

            if not enabled:
                continue

            multi = re.search("mul\\(\\d{1,3},\\d{1,3}\\)", chunk)
            if multi:
                nr1, nr2 = multi[0].split(",")
                nr1 = re.findall("\\d+", nr1)[0]
                nr2 = re.findall("\\d+", nr2)[0]
                acc += (int(nr1) * int(nr2))

    return acc


if __name__ == "__main__":
    print(solve())
