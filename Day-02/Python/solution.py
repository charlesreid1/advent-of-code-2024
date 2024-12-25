import time

# Example input file
# Should return distance = 11 and similarity = 31
with open('example', 'r') as f:
    lines = f.readlines()

# Real input file (provided on advent of code site)
with open('input', 'r') as f:
    lines = f.readlines()


"""
Part 1:
You are provided with data consisting of a matrix of numbers,
each row is a report, each column is a level of a nuclear reactor.
Safe reports are monotonically increasing/decreasing by between 1 and 3.
Return a count of safe reports.
"""

def is_safe(row):
    rowint = [int(j) for j in row.split()]
    diffs = [rowint[j] - rowint[j-1] for j in range(1,len(rowint))]

    sign_ok = [(diffs[j]>0)==(diffs[j-1]>0) for j in range(1,len(diffs))]
    value_ok = [(abs(diffs[j]) >= 1) and (abs(diffs[j]) <= 3) for j in range(len(diffs))]

    if all(sign_ok):
        if all(value_ok):
            return True

    return False

safe = 0
for row in lines:
    if is_safe(row):
        safe += 1

print(f"Part 1: Safe reports: {safe}")


"""
Part 2:
Modify Part 1 to allow for a single bad level in the
increase/decrease between levels.
"""

def is_safe_with_problem_dampener(row):

    if is_safe(row):
        return True

    # Try removing each column of the report
    # to see if any make the report safe.
    rowint = [int(j) for j in row.split()]
    for i in range(len(rowint)):
        if i==len(rowint)-1:
            new_rowint = rowint[:i]
        else:
            new_rowint = rowint[:i] + rowint[i+1:]
        # Convert list of integers to a string row for is_safe()
        new_row = " ".join([str(j) for j in new_rowint])
        if is_safe(new_row):
            # We have SOME way to make report safe
            return True

    # There is no way to make the report safe
    return False

safe = 0
for row in lines:
    if is_safe_with_problem_dampener(row):
        safe += 1

print(f"Part 2: Safe reports with problem dampener: {safe}")

