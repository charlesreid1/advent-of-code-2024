import re

# Example input file
# Should return 161 when evaluated
with open("example", "r") as f:
    lines = f.readlines()

# Real input file (provided on advent of code site)
with open("input", "r") as f:
    lines = f.readlines()

# Mash everything into one line
oneline = "".join(lines).strip()


"""
Part 1: 
Extract instructions of the form "mult(M,N)"
where M and N are integers. Compute and return
the sum of all products M*N.
"""

p = re.compile(r"mul\((\d+),(\d+)\)")

sum_product = 0

# for line in lines:
results = p.findall(oneline)
for result in results:
    sum_product += int(result[0]) * int(result[1])

print(f"Part 1: sum product: {sum_product}")


"""
Part 2:
Similar to part 1, extract instructions of form "mult(M,N)",
but this time, ignore any instructions occurring after a
"dont()" instruction and before a "do()" instruction.
"""

# # Example input file
# # Should return 48 when evaluated
# with open('example2', 'r') as f:
#     lines = f.readlines()
# oneline = "".join(lines).strip()

# First try:
# - at the beginning of the program, mul is enabled
# - find opening don't() and closing do()
# - erase everything between them
# - evaluate remainder with same funciton as before

# Change .* to (.*?) to be non-greedy...
oneline2 = re.sub("don't\(\)(.*?)do\(\)", "", oneline)

sum_product = 0
results = p.findall(oneline2)
for result in results:
    sum_product += int(result[0]) * int(result[1])

# This gives an incorrect result.

# Second try:
# - use findall to iterate over occurrences of mult(M,N), do(), don't()
# - turn the multiplication operation on/off if encountering do() or don't()
# - accumulate sum product if multiplication operation is on

sum_product = 0
active = True
for op, x, y in re.findall("(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", oneline2):
    if op == "don't()":
        active = False
    elif op == "do()":
        active = True
    elif active:
        sum_product += int(x) * int(y)

print(f"Part 2: sum product with do()/don't(): {sum_product}")
