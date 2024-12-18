import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

input_string = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
with open('/Users/adamsaunders/Developer/GitHub/adventofcode_2024/code/inputs/day17.txt') as f:
    input_string = f.read()

### Part 1
class Computer():
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
        self.pointer = 0
        self.output = []

        # Create opcode dict
        def combo_operand(operand):
            if operand == 4:
                operand = self.A
            elif operand == 5:
                operand = self.B
            elif operand == 6:
                operand = self.C
            return operand

        def adv(operand):
            operand = combo_operand(operand)
            self.A = int(self.A / (2**operand))
            self.pointer += 2

        def bxl(operand):
            self.B = self.B ^ operand
            self.pointer += 2

        def bst(operand):
            operand = combo_operand(operand)
            self.B = operand % 8
            self.pointer += 2

        def jnz(operand):
            if self.A > 0:
                self.pointer = operand
            else:
                self.pointer += 2

        def bxc(operand):
            self.B = self.B ^ self.C
            self.pointer += 2

        def out(operand):
            operand = combo_operand(operand)
            self.output.append(operand % 8)
            self.pointer += 2

        def bdv(operand):
            operand = combo_operand(operand)
            self.B = int(self.A / (2**operand))
            self.pointer += 2

        def cdv(operand):
            operand = combo_operand(operand)
            self.C = int(self.A / (2**operand))
            self.pointer += 2

        self.opcode_dict = {
            0: adv,
            1: bxl,
            2: bst,
            3: jnz,
            4: bxc,
            5: out,
            6: bdv,
            7: cdv
        }
    
    def run(self, program):
        pointer_end  = len(program)
        while self.pointer < pointer_end:
            opcode, operand = program[self.pointer], program[self.pointer+1]
            self.opcode_dict[opcode](operand)
        
        return self.output
    
# Read inputs
lines = input_string.splitlines()
A = int(re.findall(r'\d+', lines[0])[0])
B = int(re.findall(r'\d+', lines[1])[0])
C = int(re.findall(r'\d+', lines[2])[0])
program = [int(r) for r in re.findall(r'\d+', lines[4])]

computer = Computer(A, B, C)
output = computer.run(program)
print('Part 1:', ','.join([str(out) for out in output]))

### Part 2
lines = input_string.splitlines()
A = int(re.findall(r'\d+', lines[0])[0])
B = int(re.findall(r'\d+', lines[1])[0])
C = int(re.findall(r'\d+', lines[2])[0])
program = [int(r) for r in re.findall(r'\d+', lines[4])]

print(f'{program=}')

def single_run(A):
    B = A % 8
    B = B ^ 3
    C = A // (2 ** B)
    B = B ^ 5
    A = A // 8
    B = B ^ C
    return B % 8

# Only relies on the last 3 digits (IDK why), so make a lookup table. It has to be 1024 digits.
lookup = dict()
for i in range(1024):

    lookup[i] = single_run(i)

# To convert to output, pop off final 3 and lookup, remove last digit and iterate
print(A)
A_list = [int(a) for a in str(A)]
print(A_list)
for digits_list in [A_list[i:i+3] for i in range(len(A_list)-2)]:
    digits_str = [str(d) for d in digits_list]
    digits_int = int("".join(digits_str))
    print(digits_int)
    output = lookup[digits_int]
    print(output)

# for A in tqdm(range(10, 20, 8)):
#     computer = Computer(A, B, C)
#     output = computer.run(program)
#     print(A, output, program)
#     print(octal_program(A))

#     # Is output equal to program
#     if output == program:
#         print(f'{A=}')
#         break

# # print(f'{output=}')
# # print(f'{program=}')
