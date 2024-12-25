from collections import Counter

# Example input file
# Contains 18 occurrences of "XMAS"
with open('example', 'r') as f:
    lines = f.readlines()

# Example input file
# Contains 9 occurrences of X-MAS
with open('example2', 'r') as f:
    lines = f.readlines()

# Real input file (provided on advent of code site)
with open('input', 'r') as f:
    lines = f.readlines()

"""
Part 1:
Given an M x N block of letters,
find all occurrences of "XMAS"
occurring horizontally, vertically,
diagonally, backwards, or
(???) even overlapping other words.
"""

magic_word = "XMAS"

# First pass:
# - Iterate over every letter X in the grid
# - Use a stencil to get every 4-letter word
# - Put those 4-letter words into a counter
# - Return count of "XMAS" when done

# # Function to generate every 4-letter word
# # from a stencil applied to a location (i,j)
# def generate_all_words(irow, jcol, rows, cols):
#     words = []
#     # NORTH (vertical bottom-to-top)
#     # NORTHEAST (diagonal up-right)
#     # EAST (horizontal left-to-right)
#     # SOUTHEAST (diagonal down-right)
#     # SOUTH (vertical top-to-bottom)
#     # SOUTHWEST (diagonal down-left)
#     # WEST (horizontal right-to-left)
#     # NORTHWEST (diagonal up-left)
#     pass

# Second pass:
# - Yikes!! Simplify this a bit, reduce to just 4 stencils:
# - Diagonal up-left/down-right,
# - Diagonal up-right/down-left, 
# - Horizontal forwards/backwards,
# - Vertical up/down

def generate_all_words(grid, rows, cols):
    words = []

    # Diagonal up-left/down-right
    rowmin = 0
    rowmax = rows - (len(magic_word)-1)
    for i in range(rowmin, rowmax):
        colmin = 0
        colmax = cols - (len(magic_word)-1)
        for j in range(colmin, colmax):
            word = []
            for c in range(len(magic_word)):
                word.append(grid[i+c][j+c])
            word = "".join(word)
            words.append(word)
            words.append(word[::-1])

    # Diagonal up-right/down-left
    rowmin = len(magic_word)-1
    rowmax = rows
    for i in range(rowmin, rowmax):
        colmin = 0
        colmax = cols - (len(magic_word)-1)
        for j in range(colmin, colmax):
            word = []
            for c in range(len(magic_word)):
                word.append(grid[i-c][j+c])
            word = "".join(word)
            words.append(word)
            words.append(word[::-1])

    # Vertical
    rowmin = 0
    rowmax = rows - (len(magic_word)-1)
    for i in range(rowmin, rowmax):
        colmin = 0
        colmax = cols
        for j in range(colmin, colmax):
            word = []
            for c in range(len(magic_word)):
                word.append(grid[i+c][j])
            word = "".join(word)
            words.append(word)
            words.append(word[::-1])

    # Horizontal
    rowmin = 0
    rowmax = rows
    for i in range(rowmin, rowmax):
        colmin = 0
        colmax = cols - (len(magic_word)-1)
        for j in range(colmin, colmax):
            word = []
            for c in range(len(magic_word)):
                word.append(grid[i][j+c])
            word = "".join(word)
            words.append(word)
            words.append(word[::-1])
    
    return words

# The grid is the list of lists we will be using
grid = [list(j.upper()) for j in lines]
rows = len(grid)
cols = len(grid[0])

words = generate_all_words(grid, rows, cols)
counter = Counter(words)
count = counter[magic_word]

print(f"Part 1: number of XMAS strings found: {count}")

# Note: after finishing this part, I realized I could have
# used a single 4x4 moving window, and one for loop.

"""
Part 2:
Given an M x N block of letters,
find all occurrences of "MAS"
in the shape of an X:
    M . M
    . A .
    S . S
or
    M . S
    . A .
    M . S
"""

magic_word = "MAS"

# Implement an improved method:
# - Use one 3x3 stencil
# - Reduce everything to one for loop

rowmin = 0
rowmax = rows - (len(magic_word)-1)

colmin = 0
colmax = cols - (len(magic_word)-1)

xcount = 0
for i in range(rowmin, rowmax):
    for j in range(colmin, colmax):
        # Check if center of X is "A"
        if grid[i+1][j+1]==magic_word[1]:
            # Diagonal: upper left to lower right
            check1 = (grid[i][j]==magic_word[0] and grid[i+2][j+2]==magic_word[2]) \
                    or (grid[i][j]==magic_word[2] and grid[i+2][j+2]==magic_word[0])
            if check1:
                # Diagonal: lower left to upper right
                check2 = (grid[i][j+2]==magic_word[0] and grid[i+2][j]==magic_word[2]) \
                    or (grid[i][j+2]==magic_word[2] and grid[i+2][j]==magic_word[0])
                if check2:
                    xcount += 1

print(f"Part 2: number of X-MAS cocurrences: {xcount}")

