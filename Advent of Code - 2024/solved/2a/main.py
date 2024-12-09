from util.input import get_lines


def validate_report(report, up: bool) -> bool:
    
    for index in range(len(report) - 1):
        diff = report[index + 1] - report[index]
        
        if abs(diff) > 3 or (diff > 0) != up:
            return False
    
    return True
    

def solve() -> int:
    acc: int = 0
    lines = get_lines()
    
    for line in lines:
        nrs = [int(val) for val in line.split()]
        
        if len(nrs) != len(set(nrs)):
            continue  # Duplicates
        
        acc += 1 if validate_report(nrs, nrs[1] - nrs[0] > 0) else 0
    
    return acc

if __name__ == "__main__":
    print(solve())