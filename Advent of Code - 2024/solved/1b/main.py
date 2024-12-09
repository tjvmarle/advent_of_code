from util.input import get_lines


def solve() -> int:
    left, right = zip(*[line.split('   ') for line in get_lines()])
    
    scoremap = {}
    
    for val in right:
        val = int(val)
        count = scoremap.get(val, 0)
        count += val
        scoremap[val] = count
        
    acc: int = 0
    
    for val in left:
        val = int(val)
        acc += scoremap.get(val, 0)
    
    return acc

if __name__ == "__main__":
    print(solve())