from util.input import get_lines
from typing import List


def validate_report(report, up: bool) -> bool:
    
    for index in range(len(report) - 1):
        diff = report[index + 1] - report[index]
        
        if diff == 0 or abs(diff) > 3 or (diff > 0) != up:
            return False
    
    return True
    

def solve() -> int:
    acc: int = 0
    lines: List[str] = get_lines()
    
    for line in lines:
        
        nrs = [int(val) for val in line.split()]
        
        # Regular check
        if validate_report(nrs, True) or validate_report(nrs, False):
            acc += 1
            continue
        
        # Just try every possible list by deleting 1 entry
        for index in range(len(nrs)):
            
            copy_list = list(nrs)
            del copy_list[index]
            
            if validate_report(copy_list, True) or validate_report(copy_list, False):
                acc += 1
                break
    
    return acc

if __name__ == "__main__":
    print(solve())