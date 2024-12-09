import Util.input as fl

class Scratchcard:
    def __init__(self, card_line: str) -> None:
        ref_line, my_line = card_line.split(":")[1].split("|")
        self.win_ref = set([int(num) for num in ref_line.split()])
        self.my_num = set([int(num) for num in my_line.split()])
        self.copies = 1  # self-inclusion
        
    def points(self) -> int:
        return int(2**(len(self.win_ref.intersection(self.my_num)) - 1))
    
    def wins(self) -> int:
        return len(self.win_ref.intersection(self.my_num))
        

def solve() -> int:
    # 4a
    # return sum([Scratchcard(line).points() for line in fl.get_lines()])

    #4b
    acc: int = 0
    card_list = [Scratchcard(line) for line in fl.get_lines()]
    for nr, card in enumerate(card_list):
        acc += card.copies
        for win in range(0, card.wins()):
            card_list[nr + win + 1].copies += card.copies
    return acc

if __name__ == "__main__":
    print(solve())