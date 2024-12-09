from io import TextIOWrapper


def get_line(file):
    
    for line in file.readlines():
        yield line
    
    return ""


def get_nr(line : str):
    first = ""
    for letter in line:
        if not first and letter.isnumeric(): 
            first = letter
            break
        
    for letter in line[::-1]:
        if letter.isnumeric(): return f"{first}{letter}"
        
    
def get_answer():
    acc = 0
    with open("Advent/1a/input.txt", 'r') as f:
        for line in get_line(f):
            acc += int(get_nr(line))
            
        return acc
        

if __name__ == "__main__":
    print(get_answer())