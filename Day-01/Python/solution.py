# Example input file
# Should return distance = 11 and similarity = 31
with open("example", "r") as f:
    lines = f.readlines()

# Real input file (provided on advent of code site)
with open("input", "r") as f:
    lines = f.readlines()

left, right = [], []
for line in lines:
    a = int(line.split()[0])
    b = int(line.split()[1])
    left.append(a)
    right.append(b)

"""
Part 1: Compute the distance between two lists.
Start with the smallest numbers in the left and right,
calculate their distance, then move on to next largest
and repeat. Both lists are the same size.
"""

sorted_left, sorted_right = sorted(left), sorted(right)

distance = 0
for a, b in zip(sorted_left, sorted_right):
    d = abs(b - a)
    distance += d

print(f"Part 1: Distance: {distance}")

"""
Part 2: Compute the similarity between two lists.
Similarity calculation is performed by taking
each element that appears in the left list,
and multiplying it by the number of times it
appears in the right list. If an element appears
N times in the left list, its similarity contribution
is added N times.
"""

from collections import Counter

counter_left = Counter(left)
counter_right = Counter(right)

similarity = 0
for key_left in counter_left:
    s = key_left * counter_right[key_left] * counter_left[key_left]
    similarity += s

print(f"Part 2: Similarity: {similarity}")
