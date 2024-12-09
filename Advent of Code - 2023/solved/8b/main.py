from Util.input import get_lines
from itertools import cycle
import re
from typing import Tuple
import math


class Node:
    def __init__(self, line: str) -> None:
        self.node: str
        self.node, self.left_str, self.right_str = re.findall("[12A-Z]{3}", line)
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
    # Brute forcing is going to take ages. However, as long as each path is fully cyclic we can calculate their
    # individual step count and search for the Least Common Multiple among them.
    # E.g.: for 3 nodes taking 2, 7 and 12 steps this would be at most:
    # 2 * 7 * 12 = 168 steps
    # With some math (different approaches exist, most involving primes) we can bring that down to 84.

    route, nodeMap = parseFile()
    node_list = [node_obj for node_obj in nodeMap.values() if node_obj.node.endswith("A")]  # 6 nodes end in 'A'
    step_counts = []  # Answers: 20777, 18673, 13939, 17621, 19199, 12361
    # Hint: there's a reason each of these numbers is divisible bij 263 (len(route) and prime)

    for curr_node in node_list:
        route_copy = route
        curr_steps: int = 0

        while not curr_node.node.endswith("Z"):
            curr_steps += 1
            curr_node = nodeMap[curr_node.left_str] if next(route_copy) == "L" else nodeMap[curr_node.right_str]

        step_counts.append(curr_steps)

    # Some fancy math, Least Common Multiple.
    return math.lcm(*step_counts)


if __name__ == "__main__":
    print(solve())  # Answer: 17_972_669_116_327 or ~18 billion. That would've taken a while.
