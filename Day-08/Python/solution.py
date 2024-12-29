from collections import defaultdict


# Example input file
# Should return 14 unique antinode locations for part 1
with open('example', 'r') as f:
    lines = f.readlines()

# Part 1 simple example input file
# Should return 2 unique antinode locations for part 1
with open('example2', 'r') as f:
    lines = f.readlines()

# Part 2 simple example input file
# Should return 9 unique antinode locations for part 2
with open('example3', 'r') as f:
    lines = f.readlines()

# Real input file (provided on advent of code site)
with open('input', 'r') as f:
    lines = f.readlines()

NROWS = len(lines)
NCOLS = len(lines[0].strip())


"""
Part 1:
The input file contains a grid with . (empty)
and various characters representing antennas
at various frequencies. The task is to iterate
pairwise through antennas of a given frequency,
and count the number of antinodes they create
on the grid.
"""

# Solution procedure:
# - create dictionary mapping of frequencies to antenna locations
# - write function to determine antinode locations given two
#   antenna locations (r1, c1) and (r2, c2)
# - create the set of antinode locations
# - filter antinode locations not on the grid


def antinode_locations(p1, p2):
    r1, c1 = p1
    r2, c2 = p2

    dy = r2 - r1
    dx = c2 - c1

    anti1 = (r1 - dy, c1 - dx)
    anti2 = (r2 + dy, c2 + dx)

    return (anti1, anti2)


def draw_grid(locs):
    # Debug utility, draw grid and fill in given locs
    # with a "#" unless already occupied by antenna
    for i in range(len(lines)):
        line = lines[i].strip()
        newline = ""
        for j in range(len(line)):
            if line[j]=='.':
                if (i, j) in locs:
                    newline += "#"
                else:
                    newline += "."
            else:
                newline += line[j]
        print("".join(newline))


def eliminate_invalid_antinodes(all_locs):
    valid_locs = set()
    for loc in all_antinode_locs:
        c1 = loc[0] >= 0 and loc[0] <= NROWS-1
        c2 = loc[1] >= 0 and loc[1] <= NCOLS-1
        if c1 and c2:
            valid_locs.add(loc)
    valid_locs = list(valid_locs)
    valid_locs.sort(key = lambda x: x[0])
    return valid_locs


antenna_map = defaultdict(list)
for i, line in enumerate(lines):
    for j, c in enumerate(line.strip()):
        if c != ".":
            antenna_map[c].append((i, j))

# Iterate over each frequency
all_antinode_locs = set()
for frequency in antenna_map.keys():
    # Iterate pairwise over each antenna location
    antenna_locs = antenna_map[frequency]
    for i in range(len(antenna_locs)):
        for j in range(i+1, len(antenna_locs)):
            if antenna_locs[i]==antenna_locs[j]:
                continue
            anti1, anti2 = antinode_locations(antenna_locs[i], antenna_locs[j])
            all_antinode_locs.update([anti1, anti2])

# Eliminate antinode locs outside the grid
valid_antinode_locs = eliminate_invalid_antinodes(all_antinode_locs)

print(f"Part 1: antinodes found: {len(valid_antinode_locs)}")


"""
Part 2:
Take into account the effects of resonant harmonics.
Antinodes can now occur at any grid position that is
exactly in line with at least two antennas of the
same frequency, regardless of distance.
"""

def extended_antinode_locations(p1, p2):
    r1, c1 = p1
    r2, c2 = p2

    dy = r2 - r1
    dx = c2 - c1

    antis = []
    for i in range(0, max(NROWS//dy, NCOLS//dx) + 1):
        antis.append((r1 - i*dy, c1 - i*dx))
        antis.append((r2 + i*dy, c2 + i*dx))

    return antis

# Iterate over each frequency
all_antinode_locs = set()
for frequency in antenna_map.keys():
    # Iterate pairwise over each antenna location
    antenna_locs = antenna_map[frequency]
    for i in range(len(antenna_locs)):
        for j in range(i+1, len(antenna_locs)):
            if antenna_locs[i]==antenna_locs[j]:
                continue
            antis = extended_antinode_locations(antenna_locs[i], antenna_locs[j])
            all_antinode_locs.update(antis)

# Eliminate antinode locs outside the grid
valid_antinode_locs = eliminate_invalid_antinodes(all_antinode_locs)

print(f"Part 2: antinodes found: {len(valid_antinode_locs)}")
