# Example input file
# Should return 5 separate regions with total perimeter 32, price is 140
# (Prices are: A = 40, B = 32, C = 40, D = 4, E = 24)
with open("example", "r") as f:
    lines = f.readlines()

# Non-contiguous regions example
# Should return 5 separate regions with total perimeter 36, price is 772
# (4 plots of price 4, 1 plot of price 756)
with open("example2", "r") as f:
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

    nsew_locs = [
        (row-1, col),
        (row+1, col),
        (row, col+1),
        (row, col-1),
    ]

    area = 1
    perimeter = 0

    for loc in nsew_locs:

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


