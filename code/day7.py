from itertools import batched, chain, product, zip_longest
from tqdm import tqdm

test_string = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
input_string = test_string
with open('inputs/day7.txt') as f:
    input_string = f.read()

### Part 1
# Let's just brute force search the 2^n space
total_result = 0
for equation in tqdm(input_string.splitlines()):
    total, operands = equation.split(": ")
    total = int(total)
    operands = [int(operand) for operand in operands.split(" ")]
    operators = ["*", "+"]

    n_spaces = len(operands) - 1

    # Loop through potential spaces
    for operator_combination in product(operators, repeat=n_spaces):
        merged_expression = [
            pair
            for pair in chain(*zip_longest(operands, operator_combination))
            if pair is not None
        ]

        # Evalue merged expression from left to right (not regular order!)
        result = merged_expression.pop(0)
        for operator, operand in batched(merged_expression, n=2):
            if operator == "+":
                result += operand
            elif operator == "*":
                result *= operand

        if result == total:
            total_result += result
            break

print(f"{total_result=}")

### Part 2
total_result = 0
for equation in tqdm(input_string.splitlines()):
    total, operands = equation.split(": ")
    total = int(total)
    operands = [int(operand) for operand in operands.split(" ")]
    operators = ["*", "+", "||"]

    n_spaces = len(operands) - 1

    # Loop through potential spaces
    for operator_combination in product(operators, repeat=n_spaces):
        merged_expression = [
            pair
            for pair in chain(*zip_longest(operands, operator_combination))
            if pair is not None
        ]

        # Evalue merged expression from left to right (not regular order!)
        result = merged_expression.pop(0)
        for operator, operand in batched(merged_expression, n=2):
            if operator == "+":
                result += operand
            elif operator == "*":
                result *= operand
            elif operator == '||':
                # Concatenate
                result = int(str(result) + str(operand))

        if result == total:
            total_result += result
            break

print(f"{total_result=}")
