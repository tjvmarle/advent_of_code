from util.input import *  # Eat me
from typing import List

import re

def solve() -> int:
    acc: int = 0
    
    lines = get_lines()
    
    for line in lines:
        matches = re.findall("mul\(\d+,\d+\)", line)
        
        for match in matches:
            nr1, nr2 = match.split(",")
            nr1 = re.findall("\d+", nr1)[0]
            nr2 = re.findall("\d+", nr2)[0]
            acc += (int(nr1) * int(nr2))
    
    return acc

if __name__ == "__main__":
    print(solve())