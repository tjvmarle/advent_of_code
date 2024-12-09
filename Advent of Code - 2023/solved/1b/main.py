import re

FILE = "Advent/1b/input.txt"
nrs = [str(nr) for nr in range(1, 10)] # '1', '2'
txt = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
total_rgx = ("|").join(nrs + txt)
txt2nr = {nr_str : nr for nr_str, nr in zip(txt, nrs)}
print(total_rgx)

def get_line():
    with open(FILE, 'r') as file:
    
        for line in file.readlines():
            yield line
        
        return ""
        

def get_answer():
    acc = 0
    for line in get_line():
        acc += int(get_nr(line))
        
    return acc


def get_nr(line : str):
    matched = re.findall(f"(?=({total_rgx}))", line)
    parse = lambda nr : txt2nr.get(nr, nr)
    
    return f"{parse(matched[0])}{parse(matched[-1])}"


if __name__ == "__main__":
    print(get_answer())