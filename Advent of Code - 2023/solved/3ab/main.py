import Util.input as fl
from typing import List, Optional, Tuple, Set

class GridNumber:
    def __init__(self) -> None:
        self.points: List['Point'] = []  # A GridNumber can have multiple Points
        self.value = 0
        self.val_str = []
    
    def add(self, pt: 'Point'):
        self.points.append(pt)
        self.val_str.append(pt.char)
        
    def finalize(self):
        self.value = int("".join(self.val_str))
        for pt in self.points:
            pt.grnr = self  # Cross-reference a point with it's GridNumber
        
    def empty(self) -> bool:
        return len(self.points) == 0
        

class Point:
    def __init__(self, x: int, y: int, char: str) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.grnr: Optional[GridNumber] = None    # A Point can have at max one GridNumber
        
        
        
MAX_X = 140
MAX_Y = 140

class Grid:
    def __init__(self) -> None:
        self.grid : List[List[Point|None]]= [[None for _ in range(0, MAX_X)] for _ in range(0, MAX_Y)] # Empty grid
        self.symbols: List[Point] = []
    
    def add_point(self, pt : Point) -> None:
        self.grid[pt.y][pt.x] = pt
        if not pt.char.isnumeric() and not pt.char == ".":
            self.symbols.append(pt)  # Save all symbols for easy access later
            
    def __getitem__(self, xy: Tuple[int, int]) -> Point|None:
        x, y = xy
        return self.grid[y][x]
        
    def adjacent(self, pt: Point):
        """Return a list of all surrounding Points"""
        offsets = [(-1, -1), (0, -1), (1, -1), 
                   (-1,  0),          (1,  0), 
                   (-1,  1), (0,  1), (1,  1)]
        
        coordinates = [(pt.x + x, pt.y + y) for x, y in offsets]
        def check_in_bounds(xy: Tuple[int, int]):
            for val, upper in zip(xy, (MAX_X, MAX_Y)):
                if val < 0 or val >= upper:
                    return False
            return True
        return [self[xy] for xy in filter(check_in_bounds, coordinates)]
        
def buildGrid():
    grd = Grid()
    curr_nr = [GridNumber()]
    
    def finalize_nr():
        """Check if a GridNumber was being built and finalize it."""
        nonlocal curr_nr 
        if not curr_nr[-1].empty(): # Previous entry was a nr
            curr_nr[-1].finalize()
            curr_nr.append(GridNumber())  #FIXME: This overwrites all references with an empty instance
            
    for y, line in enumerate(fl.get_lines()):
        for x, char in enumerate(line):
            if char == '\n':
                continue
            
            pt = Point(x, y, char)
            
            if char.isnumeric():    # Start or continue building a GridNumber
                curr_nr[-1].add(pt)
            else:  # Finalize when current char is not a number and the previous one was
                finalize_nr()
                
            grd.add_point(pt)
            
        finalize_nr() # Always finalize when starting a new line
    
    return grd

def solve() -> int:
    grd = buildGrid()
    
    # 3a
    # all_adjacent = set() 
    # for symbol_point in grd.symbols:
    #     for adjacent_point in grd.adjacent(symbol_point):
    #         if adjacent_point and adjacent_point.nr:
    #             all_adjacent.add(adjacent_point.nr)
    # return sum([gr_nr.value for gr_nr in all_adjacent])
    
    # 3b
    acc: int = 0
    all_asterisks = filter(lambda pt : pt.char == "*", grd.symbols)
    for asterisk in all_asterisks:
        adjacent_parts: Set[GridNumber] = set()
        for adjacent in grd.adjacent(asterisk):
            if adjacent and adjacent.grnr:
                adjacent_parts.add(adjacent.grnr)
        
        if len(adjacent_parts) == 2:
            acc += (adjacent_parts.pop().value * adjacent_parts.pop().value)
    return acc

if __name__ == "__main__":
    print(solve())
