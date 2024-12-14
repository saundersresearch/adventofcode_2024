from itertools import batched
import re

input_string = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
"""
with open('inputs/day13.txt') as f:
    input_string = f.read()

### Part 1
total_tokens = 0
for line_group in batched(input_string.splitlines(), n=4):
    a_x = int(re.findall(r'X\+[0-9]+', line_group[0])[0][2:])
    a_y = int(re.findall(r'Y\+[0-9]+', line_group[0])[0][2:])
    b_x = int(re.findall(r'X\+[0-9]+', line_group[1])[0][2:])
    b_y = int(re.findall(r'Y\+[0-9]+', line_group[1])[0][2:])
    c_x = int(re.findall(r'X=[0-9]+', line_group[2])[0][2:])
    c_y = int(re.findall(r'Y=[0-9]+', line_group[2])[0][2:])

    # Standard linear equation that we can invert
    m = (b_y * c_x - b_x * c_y) / (a_x * b_y - b_x * a_y)
    n = (a_x * c_y - a_y * c_x) / (a_x * b_y - b_x * a_y)
    
    # Are m and n ints? If so, we can win!
    if m.is_integer() and n.is_integer() and m < 100 and n < 100:
        total_tokens += 3*m + n

print(f'{total_tokens=}')

### Part 2
total_tokens = 0
for line_group in batched(input_string.splitlines(), n=4):
    a_x = int(re.findall(r'X\+[0-9]+', line_group[0])[0][2:])
    a_y = int(re.findall(r'Y\+[0-9]+', line_group[0])[0][2:])
    b_x = int(re.findall(r'X\+[0-9]+', line_group[1])[0][2:])
    b_y = int(re.findall(r'Y\+[0-9]+', line_group[1])[0][2:])
    c_x = int(re.findall(r'X=[0-9]+', line_group[2])[0][2:]) + 10000000000000
    c_y = int(re.findall(r'Y=[0-9]+', line_group[2])[0][2:]) + 10000000000000

    # Standard linear equation that we can invert
    m = (b_y * c_x - b_x * c_y) / (a_x * b_y - b_x * a_y)
    n = (a_x * c_y - a_y * c_x) / (a_x * b_y - b_x * a_y)
    
    # Are m and n ints? If so, we can win!
    if m.is_integer() and n.is_integer():
        total_tokens += 3*m + n

print(f'{total_tokens=}')