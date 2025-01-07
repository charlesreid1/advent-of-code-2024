# Example input file
# Should return 5 separate regions with total perimeter 32, price is 140
# (Prices are: A = 40, B = 32, C = 40, D = 4, E = 24)
# Part 2 price is 80
# (Prices are: A = 16, B = 16, C = 32, D = 4, E = 12)
with open("example", "r") as f:
    lines = f.readlines()

# Non-contiguous regions example
# Should return 5 separate regions with total perimeter 36, price is 772
# (4 plots of price 4, 1 plot of price 756)
# Part 2 price is 436
with open("example2", "r") as f:
    lines = f.readlines()

# Part 2 example: snake region
# E shaped region should have area of 17, 12 sides
# Total price 236
with open("example3", "r") as f:
    lines = f.readlines()

# Another Part 2 example
# Total price: 368
# (two regions of B, 4 sides each, one region of A, 12 sides)
with open("example4", "r") as f:
    lines = f.readlines()

with open("input", "r") as f:
    lines = f.readlines()

NROWS = len(lines)
NCOLS = len(lines[0].strip())

grid = [list(j.upper()) for j in lines]


"""
Part 1:
2D grid of different plant types represented
by letters/numbers. 

Determine the number of distinct regions of the garden.

Find the area and perimeter of each distinct region.

Multiply the area of the garden by the perimeter of the garden
to get the price of the fence for that region of the garden.

Return the sum of the price of fence for each region.
"""

# Approach:
# - keep track of unvisited squares (visit all squares)
# - recursive method to visit a square:
#    - base case: neighbor cell is not same plant type, increment perimeter and area
#    - recursive case: neighbor cell is same plant type, visit it
#    - (are we going to have 4 base/recursive cases??)


def visit(row, col):
    plant_type = grid[row][col]

    # Check N E S W cell location
    # - is it on the grid?
    # - is it the same plant type?
    # - is it unvisited?
    # - if so, remove them from unvisited and call visit()
    # - otherwise, accumulate perimeter

    nesw_locs = [
        (row-1, col),
        (row, col+1),
        (row+1, col),
        (row, col-1),
    ]

    area = 1
    perimeter = 0

    for loc in nesw_locs:

        in_bounds = loc[0]>=0 and loc[0]<NROWS and loc[1]>=0 and loc[1]<NCOLS
        if not in_bounds:
            # Increment perimeter b/c this is the edge of the grid
            perimeter += 1

        else:
            is_sametype = grid[loc[0]][loc[1]] == plant_type
            if is_sametype:

                is_unvisited = loc in unvisited
                if is_unvisited:

                    unvisited.remove(loc)
                    _, child_area, child_perimeter = visit(*loc)
                    area += child_area
                    perimeter += child_perimeter

            else:
                # Neighbor is def on the grid, but different type
                perimeter += 1

    return plant_type, area, perimeter


unvisited = set()
for row in range(NROWS):
    for col in range(NCOLS):
        unvisited.add((row, col))

# Start visiting all squares
regions = []

while len(unvisited)>0:
    start = unvisited.pop()
    plant_type, area, perimeter = visit(*start)
    regions.append((plant_type, area, perimeter))

price = 0
for _, area, perimeter in regions:
    price += area*perimeter

print(f"Part 1: price: {price}")


"""
Part 2:
Same grid/scenario as Part 1, but this time, price is calculated
by multiplying area by number of sides, not by perimeter.

For example, this shape has 8 sides:
+-+
| |
| +-+
|   |
+-+ |
  | |
  +-+

Return the sum of the price of fence for each region.
"""

# Approach:
# - new corners can only be created at each + junction
# - revamp the recursive method to look for corners
# - if N-E, and/or E-S, and/or S-W, and/or W-N, then accumulate corners

def visit_part2(row, col):
    plant_type = grid[row][col]

    nesw_locs = [
        (row-1, col),
        (row, col+1),
        (row+1, col),
        (row, col-1),
    ]

    area = 1
    ncorners = 0

    corner_cycles = [0, 0, 0, 0]
    labels = list("NESW")

    for i, loc in enumerate(nesw_locs):
        lab = labels[i]

        in_bounds = loc[0]>=0 and loc[0]<NROWS and loc[1]>=0 and loc[1]<NCOLS
        if not in_bounds:
            # This is a boundary (edge of the grid)
            corner_cycles[i] = 1
        else:
            is_sametype = grid[loc[0]][loc[1]] == plant_type
            if is_sametype:
                is_unvisited = loc in unvisited
                if is_unvisited:
                    #print(f"About to visit {lab} neighbor for cell {row}, {col}")
                    unvisited.remove(loc)
                    _, child_area, child_ncorners = visit_part2(*loc)
                    area += child_area
                    ncorners += child_ncorners
                    #print(f"Found {ncorners} in visit to {lab} neighbor for cell {row}, {col}")
            else:
                # This is a boundary (neighbor is on the grid, but different type)
                corner_cycles[i] = 1

    pre_ncorners = ncorners

    # Must match NESW loc order
    diag_locs = [
        (row-1, col+1),
        (row+1, col+1),
        (row+1, col-1),
        (row-1, col-1),
    ]

    # Accumulate corners (one or more adjacent pairs of N-E, E-S, S-W, W-N combinations)
    for j in range(len(corner_cycles)):
        if corner_cycles[j]==1 and corner_cycles[(j+1)%len(corner_cycles)]==1:
            # Two adjacent directions both have boundaries,
            # forming an external corner
            #print(f"Accumulating 1 external corner (ncorners={ncorners}, corner_cycles={corner_cycles}) for cell {row}, {col}")
            ncorners += 1
        elif corner_cycles[j]==0 and corner_cycles[(j+1)%len(corner_cycles)]==0:
            # Two adjacent directions both lack boundaries,
            # check if the corresponding diagonal is the same type,
            # if it is not, it forms an internal corner.
            diag_loc = diag_locs[j]
            in_bounds = diag_loc[0]>=0 and diag_loc[0]<NROWS and diag_loc[1]>=0 and diag_loc[1]<NCOLS
            if in_bounds:
                is_sametype = grid[diag_loc[0]][diag_loc[1]] == plant_type
                if not is_sametype:
                    # Different diagonal type makes an internal corner
                    #print(f"Accumulating 1 internal corner (ncorners={ncorners}, corner_cycles={corner_cycles}) for cell {row}, {col}")
                    ncorners += 1

    post_ncorners = ncorners
    #print(f"Accumulating {post_ncorners-pre_ncorners} corners (ncorners={ncorners}, corner_cycles={corner_cycles}) for cell {row}, {col}")

    return plant_type, area, ncorners


unvisited = set()
for row in range(NROWS):
    for col in range(NCOLS):
        unvisited.add((row, col))

# Start visiting all squares
regions = []

while len(unvisited)>0:
    start = unvisited.pop()
    #print(f"Starting at {start[0]}, {start[1]}")
    plant_type, area, ncorners = visit_part2(*start)
    regions.append((plant_type, area, ncorners))

price = 0
for _, area, ncorners in regions:
    price += area*ncorners

print(f"Part 2: price: {price}")
