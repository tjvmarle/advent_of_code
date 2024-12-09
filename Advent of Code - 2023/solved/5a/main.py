import Util.input as fl
from typing import List, Optional, Tuple, Set

class Src2DestRange:
    def __init__(self, line: str) -> None:
        dest_start, source_start, range = line.split()
        self.dest = int(dest_start)
        self.src = int(source_start)
        self.range = int(range)
        
    def __getitem__(self, src_val: int):
        if not self.src <= src_val < (self.src + self.range):
            return src_val
        
        return src_val - self.src + self.dest
        
    
def parseInputToMaps():
    line_generator = fl.get_lines()
    seedList = [int(seed_str) for seed_str in next(line_generator).split(":")[1].split()]
    
    mapList: List[List[Src2DestRange]] = []
    
    for line in line_generator:
        if line[0].isalpha():
            mapList.append([])  # Start the next maplist
            continue
        
        if not line[0].isdigit(): continue  # ignore empty/newlines
        
        mapList[-1].append(Src2DestRange(line))
        
    return seedList, mapList
    

def solve() -> int:
    seedList, mapList = parseInputToMaps()
    location: int = 1_000_000_000_000
    
    for seed in seedList:
        src_val = seed
        dest_val = seed
        
        for map in mapList:
            src_val = dest_val  # dest val of previous iteration becomes src for the next one
            
            for range in map:
                dest_val = range[src_val]
                
                if dest_val != src_val:
                    break  # Aanname: Een dest-waarde komt maar binnen 1 range voor per map
                
        location = min(dest_val, location)
    
    return location

if __name__ == "__main__":
    print(solve())