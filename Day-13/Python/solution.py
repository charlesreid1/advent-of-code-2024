import re

# Example input file
with open("example", "r") as f:
    lines = f.readlines()

# Real input file
with open("input", "r") as f:
    lines = f.readlines()

A_COST = 3
B_COST = 1

"""
Part 1:
The input is a list of claw machines, where
there are three pieces of information given:

* number of steps to the right and up for
  button A (cost = 3), in the format
  Button A: X+123, Y+123

* number of steps to the right and up for
  button B (cost = 1), in the format
  Button B: X+123, Y+123

* prize location (X, Y), in the format
  Prize: X=12345, Y=12345

Find the cheapest way to win the prize,
if the prize can even be reached, and
add up the minimum total cost for each
machine (if no solution, 0).
"""

# Approach:
# - function to parse input
# - determine a cap on number of A, B button presses
# - double for loop over number of A, B button presses
# - have a boolean (prize reached) and minimum cost var
# 
# Caveat:
# - this approach will break down if the numbers get big
# - (if this chokes on the real input, replace the double for loop)

def parse_input(lines_):
    """
    Return a list of tuples with information about each claw machine:
    (A X+, A Y+, B X+, B Y+, Prize X Loc, Prize Y Loc)
    """
    machines = []
    nmachines = (len(lines_)//4)+1
    for i in range(nmachines):
        linea = lines_[4*i]
        lineb = lines_[4*i+1]
        linep = lines_[4*i+2]
        ax, ay = re.findall(r'\d+', linea)
        bx, by = re.findall(r'\d+', lineb)
        px, py = re.findall(r'\d+', linep)
        machines.append((int(ax), int(ay), int(bx), int(by), int(px), int(py)))
    return machines

# Machines is a list of tuples with info about claw machine:
# (A X+, A Y+, B X+, B Y+, Prize X Loc, Prize Y Loc)
machines = parse_input(lines)

solution = 0
for m, (ax, ay, bx, by, px, py) in enumerate(machines):

    # Determine maximum number of A or B button presses
    # (how many take it past the prize X or Y)
    max_a = min((px//ax)+1, (py//ay)+1)
    max_b = min((px//bx)+1, (py//by)+1)
    
    prize_reached = False
    min_cost = 0
    min_a, min_b = -1, -1

    for ia in range(max_a):
        for ib in range(max_b):
            # We have pressed A button ia times,
            # We have pressed B button ib times,
            # Now see where we ended up
            x = ia*ax + ib*bx
            y = ia*ay + ib*by
            if x==px and y==py:
                if prize_reached is False:
                    prize_reached = True
                    min_cost = ia*A_COST + ib*B_COST
                    min_a, min_b = ia, ib
                else:
                    min_cost = min(min_cost, ia*A_COST + ib*B_COST)
                    min_a, min_b = ia, ib
    
    #if prize_reached:
    #    print(f"Claw Machine {m+1}: min cost = {min_cost}")
    #else:
    #    print(f"Claw Machine {m+1}: prize cannot be reached")

    solution += min_cost

print(f"Part 1: total min cost = {solution}")
