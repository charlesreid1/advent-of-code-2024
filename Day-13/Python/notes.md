# Notes on Part 2

For part 2, needed to take a step back from
the brute force approach using nested for loops
and figure out a better approach.

## First Approach

My first approach was to split the problem into two parts:

1. Figure out a cost effective way to cross
   the square expanse of 100000000 x 100000000
2. Once you have the cost of crossing that expanse,
   use that new starting point and repeat part 1.

The method to do this turned out to work on the example
but not on the real input.

The examples all had X and Y changes for Button A and Button B
that could form a perfect square in some combination.
Some of the inputs, however, had X and Y changes that could
never be combined to form a perfect square.

Without a working example, I could not figure out a way around
that issue, so I abandoned that approach. Code is given below.

```
"""
Part 2:
Modify the input such that the old prize location (X,Y)
is now at (10000000000000+X, 10000000000000+Y)

Find the same answer as Part 1, but with the new
prize locations. If the prize can be reached,
determine the cheapest way, and the minimum cost.
"""

OFFSET = 10000000000000

def convert_input_part2(part1):
    new_input = []
    for m in part1:
        new_input.append((m[0], m[1], m[2], m[3], m[4]+OFFSET, m[5]+OFFSET))
    return new_input

machines = convert_input_part2(parse_input(lines))

# Approach:
# - replace the for loop with something smarter...
# - prior approach incremented A, B button presses from 0 to max
# - this approach needs to figure out a way to cross the endless expanse
#   of the 10000000000 x 1000000000 square, which requires figuring out
#   the cheapest way to make a perfect square.
#   Constraint:
#   p X_A + q X_B = p Y_A + q Y_B

solution = 0
for m, (ax, ay, bx, by, px, py) in enumerate(machines):

    # Split this calculation into two parts:
    # 1. cheapest way to cross the OFFSET x OFFSET square desert
    # 2. cheapest way to get from that point to the prize

    #print(f"Machine {m+1}: ({ax}, {ay}, {bx}, {by}, {px}, {py})")

    # --------------------------------
    # 1. OFFSET X OFFSET square desert

    # Start by determining the ratio of A:B presses
    # required to form a perfect square
    found = False
    perfect_p, perfect_q = -1, -1
    for p in range(1,1000):
        if found:
            break
        for q in range(1,1000):
            left = p*ax + q*bx
            right = p*ay + q*by
            if left==right:
                perfect_p, perfect_q = p, q
                found = True
            if found:
                break

    if perfect_p==-1:
        #print(f"Warning: machine {m+1} could not find a square ratio")
        continue

    # Determine size/cost of square
    square_cost = perfect_p*A_COST + perfect_q*B_COST
    square_size = perfect_p*ax + perfect_q*bx

    # Determine number of squares in OFFSET x OFFSET
    nsq = OFFSET//square_size

    # This puts us close to OFFSET, but maybe not quite
    start_loc = square_size*nsq

    # ---------------------------------
    # 2. Go from OFFSETxOFFSET to prize

    # Traveling FROM start_loc (just near the OFFSET)
    #           TO end_loc (where the prize is located)

    # Use the same principle as Part 1
    max_a = min(((px - start_loc)//ax)+1, ((py - start_loc)//ay)+1)
    max_b = min(((px - start_loc)//bx)+1, ((py - start_loc)//by)+1)

    prize_reached = False
    min_cost = 0

    # Start by pressing the buttons nsq*perfect_{p,q} times,
    square_x = nsq*perfect_p*ax + nsq*perfect_q*bx
    square_y = nsq*perfect_p*ay + nsq*perfect_q*by

    for ia in range(max_a):
        for ib in range(max_b):

            # Then we pressed A button ia times,
            # Then we pressed B button ib times,
            # Now see where we ended up
            x = square_x + ia*ax + ib*bx
            y = square_y + ia*ay + ib*by
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

print(f"Part 2: total min cost = {solution}")
```

## Second Approach

In the process of implementing the loop to find number of
button presses to form a perfect square, I wrote an equation
relating changes in x and y and button pressses. 

I reworked the equation to cover the entire problem,
and realized it's just a system of two equations and
two unknowns (duh):

```
A = number of A button presses
X_A = x change for button A press
Y_A = y change for button A press

B = number of B button presses
X_B = x change for button B press
Y_B = y change for button B press

X_P = x location of prize
Y_P = y locaiton of prize

-----------------

A * X_A + B * X_B = X_P
A * Y_A + B * Y_B = Y_P
```

