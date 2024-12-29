# Example input file
# Should return accumulated value of 3749 (part 1)
# Should return accumulated value of 11387 (part 2)
with open('example', 'r') as f:
    lines = f.readlines()

# # Simpler example input file
# # Should return accumulated value of 3267 (part 1)
# with open('example2', 'r') as f:
#     lines = f.readlines()

# Real input file from AoC website
with open('input', 'r') as f:
    lines = f.readlines()


"""
Part 1:
Each line of the input file is of the form

<test_value>: <int1> <int2> <int3>

Your job is to find a valid combination of operators
(*) and (+) to insert between the given numbers.

If you can find a valid combination of operators,
add that test value to the final sum. Otherwise, don't.
"""

# Convert list of strings "<test_val>: <int1> <int2>" to mapping
test_map = {}
for line in lines:
    if line=="":
        continue
    a, b = line.strip().split(":")
    right_values = [int(j) for j in b.strip().split(" ")]
    test_value = int(a)
    test_map[a] = right_values


def find_valid_operators(target_value, sum_nums, operator_list, part2):

    if len(operator_list) == len(sum_nums)-1:
        # Base case, picked all operators, now check if they yield target value
        accumulator = sum_nums[0]
        #opstr = f"{accumulator}"
        for i, op in enumerate(operator_list):
            if op=="*":
                accumulator *= sum_nums[i+1]
            elif op=="+":
                accumulator += sum_nums[i+1]
            elif op=="||" and part2 is True:
                accumulator = int(str(accumulator) + str(sum_nums[i+1]))
            else:
                raise Exception(f"Unknown operator {op}")
            #opstr += op + str(sum_nums[i+1])

        if accumulator == target_value:
            #print(f"Checking operator list: {target_value} = {accumulator} = {opstr} (success)")
            return True
        else:
            #print(f"Checking operator list: {target_value} != {accumulator} = {opstr} (failure)")
            return False

    else:
        # Recursive case
        if part2:
            return \
                find_valid_operators(target_value, sum_nums, operator_list+["+"], part2) \
                or find_valid_operators(target_value, sum_nums, operator_list+["*"], part2) \
                or find_valid_operators(target_value, sum_nums, operator_list+["||"], part2)
        else:
            return \
                find_valid_operators(target_value, sum_nums, operator_list+["+"], part2) \
                or find_valid_operators(target_value, sum_nums, operator_list+["*"], part2)

accumulator = 0
for k, right_values in test_map.items():
    test_value = int(k)
    valid_operators = find_valid_operators(test_value, right_values, [], False)
    if valid_operators is True:
        accumulator += test_value

print(f"Part 1: accumulated value: {accumulator}")



"""
Part 2:
Repeat Part 1, but include a third concatenation operator.

<int1> || <int2> will concatenate the two together like a string.

For example, 15 || 10 becomes 1510
"""

accumulator2 = 0
for k, right_values in test_map.items():
    test_value = int(k)
    valid_operators = find_valid_operators(test_value, right_values, [], True)
    if valid_operators is True:
        accumulator2 += test_value

print(f"Part 2: accumulated value: {accumulator2}")

