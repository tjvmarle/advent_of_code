import Util.input as fl
from functools import reduce

def parseFile():
    gen = fl.get_lines()
    # 6a
    # times =  [int(time) for time in next(gen).split(":")[1].split()]
    # dist = [int(dist) for dist in  next(gen).split(":")[1].split()]
    
    # 6b
    time = int("".join(next(gen).split(":")[1].split()))
    distance = int("".join(next(gen).split(":")[1].split()))
    
    # return zip(times, dist)  # 6a
    return (time, distance)

def correct_approach(time: int, distance: int) -> int:
    # Just solve for what combination of push-time * run-time you equate the distance. Then round up to nearest integers
    # and calculate the difference (+1)
    
    # Basic setup
    # time and distance are known values (constants). Two equations with two unknows, solvable.
    # time_c     = run_time + push_time
    # distance_c = run_time * push_time
    
    # Since
    # run_time = time_c - push_time
    # We can replace either run_time or push_time with the other
    # distance_c = (time_c - push_time) * push_time
    # distance_c = time_c * push_time - push_time^2
    # 0          = -push_time^2 + time_c * push_time - distance_c <-- classic quadratic equation: ax^2 + bx + c
    # push_time  = (-time_c +/- sqrt(time_c^2 - 4 * -1 * -distance)) / -2
    
    # Plug in the values, solve push_time (and run_time), round up the values and calculate delta.
    # Might have to check for correct rounding on the edges.
    ...
    
def count_winning_races(time: int, distance: int) -> int:
    wins: int = 0
    for val in range(0, time + 1):  # Just bruteforce this
        if (time - val) * val > distance:
            wins += 1
    return wins
    
def solve() -> int:
    races = parseFile()
    
    # 6b
    return count_winning_races(*races)
    
    # 6a
    # result = [count_winning_races(*race) for race in races]
    # return reduce(lambda x, y: x*y, result)

if __name__ == "__main__":
    print(solve())