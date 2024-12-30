from collections import defaultdict, deque

# Example input file
# Part 1 should return 143
# Part 2 should return 123
with open('example', 'r') as f:
    lines = f.readlines()

# Real input file (provided on advent of code site)
with open('input', 'r') as f:
    lines = f.readlines()

# Parse the two parts of the input file
rules = [line for line in lines if "|" in line]
updates = [line for line in lines if "," in line]


"""
Part 1:
The input file consists of two sections:
    1. page ordering rules, one per line
       A|B means A must come before B in the updates
    2. page update sequences, one per line
       X,Y,Z must conform to the page ordering rules
Identify which updates are in valid order.
Determine the middle number of each valid order sequence.
Sum them up, and return the sum.
"""

# Procedure:
# - create fwd/rev mappings A|B A->B and B->A
# - iterate over each update sequence
# - iterate over each item in update sequence
# - use index() to get index of item in list
# - use index of item to split list into pre and ant
# - turn pre/ant into sets
# - check which fwd/rev rules apply to item

# Create fwd A|B mapping
# Create rev B|A mapping

map_fwd = defaultdict(set)
map_rev = defaultdict(set)
for rule in rules:

    a, b = [int(j.strip()) for j in rule.split("|")]
    map_fwd[a].add(b)
    map_rev[b].add(a)

accumulator = 0
invalid_sequences = []
for update in updates:
    update_valid = True
    seq = [int(j) for j in update.split(",")]

    for ix,item in enumerate(seq):
        pre = set(seq[:ix])
        ant = set(seq[ix+1:])

        # Check if preceding numbers show up in ant rules
        for p in pre:
            if p in map_rev:
                if item in map_rev[p]:
                    update_valid = False

        # Check if anteceding numbers show up in pre rules
        for a in ant:
            if a in map_fwd:
                if item in map_fwd[a]:
                    update_valid = False

    if update_valid:
        accumulator += seq[len(seq)//2]
    else:
        invalid_sequences.append(seq)

print(f"Part 1: sum of middle numbers: {accumulator}")


"""
Part 2:
For each sequence in Part 1 that is not in valid order,
rearrange the elements so they are in correct order,
then return the sum of the middle numbers.
"""

def swap_items(a, b, lst):
    if a not in lst:
        raise Exception(f"Asked to remove {a} from {', '.join(lst)}, but item not found")
    if b not in lst:
        return lst
    ixa = lst.index(a)
    ixb = lst.index(b)
    tmp = lst[ixa]
    lst[ixa] = lst[ixb]
    lst[ixb] = tmp
    return lst

# This was difficult to troubleshoot b/c example provided
# did not require topological sort or show how multiple
# mappings should be handled.
accumulator2 = 0
for seq in invalid_sequences:
    valid_sequence = []
    d = {j: len(map_fwd[j] & set(seq)) for j in seq}
    q = deque([])

    for j in seq:
        if d[j]==0:
            q.append(j)
    while q:
        a = q.popleft()
        valid_sequence.append(a)
        for b in map_rev[a]:
            if b in d:
                d[b] -= 1
                if d[b] == 0:
                    q.append(b)

    # should be 6305
    accumulator2 += valid_sequence[len(valid_sequence)//2]

print(f"Part 2: sum of middle numbers: {accumulator2}")
