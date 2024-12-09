import Util.input as fl
from typing import List, Optional, Tuple, Set
from itertools import islice

class RangedValue:
    def __init__(self, val: int, range: int) -> None:
        """Representation of a value range instead of a single value."""
        self.min = val
        self.max = val + range - 1
        self.range = range
        
    def offset(self, offset: int) -> None:
        self.min += offset
        self.max += offset
        
class RangeCollection:
    def __init__(self, ranges: List[RangedValue]) -> None:
        self.ranges = ranges
        self._overlapping = []
        
    def add_non_overlapping(self, range: RangedValue):
        self.ranges.append(range)
        
    def add_overlapping(self, range: RangedValue):
        # Put these somewhere else temporarily or they'll be reused on the current map
        self._overlapping.append(range)
        
    def finalize(self) -> None:
        # Just add everything back to a single list so it can be used for the next map
        self.ranges += self._overlapping
        self._overlapping = []
        
    def min(self) -> int:
        return min(range.min for range in self.ranges)

class Src2DestRange:
    def __init__(self, line: str) -> None:
        dest_start, source_start, range = line.split()
        self.dest = int(dest_start)
        self.min = int(source_start)
        self.range = int(range)
        self.max = self.min + self.range - 1
        self.offset = self.dest - self.min
        
    def __getitem__(self, in_coll: RangeCollection):
        # Checks for a given collection of ranges the ones that overlap (and offsets them). Non-overlapping ranges will 
        # also be returned, without the offset. A single range could be split into up to three smaller ranges.
        
        result = RangeCollection([])
        result._overlapping = in_coll._overlapping  # Otherwise we'll lose the values we filtered out earlier
        
        # Since the range of a RangedValue can partially overlap with this, it might need to be split up into multiple 
        # result ranges.
        for range in in_coll.ranges:
            if range.min > self.max or range.max < self.min:
                result.add_non_overlapping(range) # input value entirely out of range
                continue
            
            # Overlapping part
            lower = max(range.min, self.min)
            upper = min(range.max, self.max)
            overlapping_range = RangedValue(lower, (upper - lower + 1))
            overlapping_range.offset(self.offset)  # This is the part that needs to be converted to new values
            result.add_overlapping(overlapping_range)
            
            # Non-overlapping lower part
            if range.min < lower:
                result.add_non_overlapping(RangedValue(range.min, lower - range.min))
            
            # Non-overlapping upper part
            if range.max > upper:
                result.add_non_overlapping(RangedValue(upper + 1, range.max - upper))
        
        return result
        
def parseInputToMaps():
    line_generator = fl.get_lines()
    seeds = [int(seed_str) for seed_str in next(line_generator).split(":")[1].split()]
    seed_ranges = list(zip(islice(seeds, 0, None, 2), islice(seeds, 1, None, 2)))
    
    mapList: List[List[Src2DestRange]] = []
    
    for line in line_generator:
        if line[0].isalpha():
            mapList.append([])  # Start the next maplist
            continue
        
        if not line[0].isdigit(): continue  # ignore empty/newlines
        
        mapList[-1].append(Src2DestRange(line))
        
    return seed_ranges, mapList

    
def solve() -> int:
    seedList, mapList = parseInputToMaps()
    ranged_seeds = [RangedValue(*seed) for seed in seedList]
    location: int = 1_000_000_000_000
    
    for seed in ranged_seeds:
        dest_val = RangeCollection([seed])
            
        for map in mapList:    
            for range in map:
                dest_val = range[dest_val]  # This 'filters' out overlapping values
            dest_val.finalize()
                
        location = min(dest_val.min(), location)
    
    return location

if __name__ == "__main__":
    print(solve())