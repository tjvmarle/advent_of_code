from util.input import get_lines


def solve() -> int:
    left, right = zip(*[line.split('   ') for line in get_lines()])
    sorted_left, sorted_right = sorted(left), sorted(right)
    acc: int = 0
    
    for index, item in enumerate(sorted_left):
        acc += abs(int(sorted_left[index]) - int(sorted_right[index]))
    
    return acc

if __name__ == "__main__":
    print(solve())