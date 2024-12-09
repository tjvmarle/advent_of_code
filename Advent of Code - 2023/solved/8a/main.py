from Util.input import get_lines
from itertools import cycle
import re
from typing import List, Tuple


class Node:
    def __init__(self, line: str) -> None:
        self.node, self.left_str, self.right_str = re.findall("[A-Z]{3}", line)
        self.right: Node
        self.left: Node


def parseFile() -> Tuple['cycle[str]', dict[str, Node]]:
    gen = get_lines()
    route = cycle([step for step in next(gen) if step != '\n'])
    next(gen)  # Empty line

    nodeMap = {line.split(" = ")[0]: Node(line) for line in gen}  # "AAA" : Node("AAA")
    for node in nodeMap.values():   # Cross-reference all nodes
        node.left = nodeMap[node.left_str]
        node.right = nodeMap[node.right_str]

    return route, nodeMap


def solve() -> int:
    route, nodeMap = parseFile()
    curr_node = nodeMap["AAA"]
    acc: int = 0

    while curr_node != nodeMap["ZZZ"]:
        acc += 1
        curr_node = nodeMap[curr_node.left_str] if next(route) == 'L' else nodeMap[curr_node.right_str]

    return acc


if __name__ == "__main__":
    print(solve())
