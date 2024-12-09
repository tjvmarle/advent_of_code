import Util.input as fl
from functools import reduce

class Set:
    def __init__(self, set_str: str) -> None:
        self.red = self.green = self.blue = 0
        
        if not set_str:
            return
        
        for entry in set_str.split(','):
            count, color = entry.split()
            match color:
                case "red":
                    self.red = int(count)
                case "green":
                    self.green = int(count)
                case "blue":
                    self.blue = int(count)
                case _:
                    print(f"Error entry: {entry}")
                    
        
    def __le__(self, other):
        return all([self.red <= other.red, 
                    self.green <= other.green, 
                    self.blue <= other.blue])
        
    def power(self) -> int:
        return self.red * self.green * self.blue
    
    @staticmethod
    def max(lh: 'Set', rh: 'Set') -> 'Set':
        max_set: Set = Set("")
        max_set.red = max((lh.red, rh.red))
        max_set.green = max((lh.green, rh.green))
        max_set.blue = max((lh.blue, rh.blue))
        
        return max_set


class Game:
    def __init__(self, line: str) -> None:
        game_str, sets_str = line.split(':')
        self.game = int(game_str.split()[1])
        self.sets = [Set(game_set) for game_set in sets_str.split(';')]
        
    def possible(self, reference_set: Set) -> bool:
        return all([cube_set <= reference_set for cube_set in self.sets])
    
    def minimum_power(self):
        return reduce(Set.max, self.sets).power()
        

def solve() -> int:
    acc: int = 0
    for line in fl.get_lines():
        acc += Game(line).minimum_power()
    
    return acc


if __name__ == "__main__":
    print(solve())
