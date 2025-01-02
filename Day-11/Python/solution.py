import time
from functools import lru_cache

# Example input file
# Part 1: after 25 blinks, 55312 stones
# Part 2: after 75 blinks: 65601038650482 stones
with open("example", "r") as f:
    lines = f.readlines()

# Real input file
# from AoC website
with open("input", "r") as f:
    lines = f.readlines()

line = lines[0].strip()
original_stones = [int(j) for j in line.split(" ")]

"""
Part 1:
Given a set of stones with numbers on them,
at each step, the numbers change simultaneously
according to the first applicable rule in this list:

1. if stone has 0, replaced by stone with 1
2. if stone has even number of digits, replaced by two stones:
     - left stone: left half of digits
     - right stone: right half of digits
3. if no other rules apply, stone replaced by new stone,
   new stone number is old stone number times 2024

order of stones is always preserved.
Figure out how many stones you will have after 25 rounds.
"""

stones = original_stones[:]
def transform(stones):
    new_stones = []
    for stone in stones:
        if stone==0:
            new_stones.append(1)
        elif len(str(stone))%2==0:
            ss = str(stone)
            left_stone  = int(ss[:len(str(stone))//2])
            right_stone = int(ss[len(str(stone))//2:])
            new_stones.append(left_stone)
            new_stones.append(right_stone)
        else:
            new_stones.append(2024*stone)
    return new_stones

nblinks = 25

for i in range(nblinks):
    new_stones = transform(stones)
    stones = new_stones

print(f"Part 1: 25 blinks: {len(stones)} stones")



"""
Part 2:
Repeat Part 1, but this time, use nblinks = 75.

Note: If you try to use the Part 1 solution,
it will really start to slow down around 45 blinks.
No way it would make it to 75 blinks in less than
a day or two of compute time, maybe more.

Instead, use the fact that stones don't interact
to conduct a depth-first search. We can also
memoize the combinations of stone value and depth
to skip significant amounts of calculation time.
"""

stones = original_stones[:]

@lru_cache(maxsize=10000)
def depth_search(stone_value, blinks_left):
    """
    Recursive depth-first search.

    Base case: no blinks left, return how many stones you have.

    Recursive case: Decrement blinks_left,
    apply any rules to the stone value you have,
    and call depth_search() on the resulting stones.
    Sum the results from those calls and return it.
    """
    nstones = 0
    if blinks_left==0:
        # Base case: no blinks left
        nstones = 1
    else:
        # Recursive case: apply rules, decrement blinks, call ourselves
        slen = len(str(stone_value))
        if stone_value==0:
            # Rule 1: if stone has 0, replaced by stone with 1
            nstones += depth_search(1, blinks_left-1)
        elif slen%2==0:
            # Rule 2: if stone has even number of digits,
            # replace it with two stones:
            # left stone = left half of digits
            # right stone = right half of digits
            lh = int(str(stone_value)[:slen//2])
            rh = int(str(stone_value)[slen//2:])
            nstones += depth_search(lh, blinks_left-1)
            nstones += depth_search(rh, blinks_left-1)
        else:
            # Rule 3: if no other rules apply,
            # replace with new stone that is
            # old stone number times 2024
            nstones += depth_search(stone_value*2024, blinks_left-1)
    return nstones

blinks = 75

n = 0
for stone in stones:
    n += depth_search(stone, blinks)

print(f"Part 2: 75 blinks: {n} stones")
