import Util.input as fl
from enum import Enum
from typing import List

class HandType(Enum):
    FiveOfAKind = 6
    FourOfAKind = 5
    FullHouse = 4
    ThreeOfAKind = 3
    TwoPair = 2
    OnePair = 1
    HighCard = 0
    
cardStrength = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
cnts2Type = {(5,) : HandType.FiveOfAKind, (4,1) : HandType.FourOfAKind, (3,2) : HandType.FullHouse, 
             (3,1,1) : HandType.ThreeOfAKind, (2,2,1) : HandType.TwoPair, (2,1,1,1) : HandType.OnePair, 
             (1,1,1,1,1) : HandType.HighCard}

class Hand:
    def __init__(self, line: str) -> None:
        self.cards, bid_str = line.split()
        self.bid = int(bid_str)
        self.cards_nr: List[int] = [cardStrength[card] for card in self.cards]
        self.type: HandType = self._get_type()
        
    def _get_type(self) -> HandType:
        card_cnt = {}
        for card_nr in self.cards_nr:
            card_cnt[card_nr] = card_cnt.get(card_nr, 0) + 1
            
        cnt_list: List[int] = sorted([val for val in card_cnt.values()], reverse=True)
        return cnts2Type[tuple(cnt_list)]
    
    def __lt__(self, other: 'Hand') -> bool:
        if self.type == other.type:
            for index, card in enumerate(self.cards_nr):
                if card == other.cards_nr[index]:
                    continue
                return card < other.cards_nr[index]
        return self.type.value < other.type.value
    
    def __str__(self) -> str:
        return f"cards: {self.cards}, bid: {self.bid}, type: {self.type}"
        
        

def parseFile():
    return [Hand(line) for line in fl.get_lines()]  
    
def solve() -> int:
    hands = sorted(parseFile())
    
    for hand in hands:
        print(str(hand))
        
    return sum([hand.bid * rank for rank, hand in enumerate(hands, 1)])

if __name__ == "__main__":
    print(solve())