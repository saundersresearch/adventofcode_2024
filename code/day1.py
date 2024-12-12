# https://adventofcode.com/2024/day/1
from collections import Counter
from pathlib import Path

import numpy as np

### Part 1
input_path = Path("inputs/day1.txt")
with open(input_path, "r") as f:
    input_data = np.loadtxt(input_path, dtype=int)
    list1 = input_data[:, 0]
    list2 = input_data[:, 1]

# Sort and get index
list1_sorted = sorted(list1)
list2_sorted = sorted(list2)

# Calculate distance
dist = [abs(l1 - l2) for l1, l2 in zip(list1_sorted, list2_sorted)]

# Get total
total_dist = sum(dist)
print(f"{total_dist=}")

### Part 2
unique_elem_count1 = Counter(list1)
unique_elem_count2 = Counter(list2)

similarity_score = 0
for elem in unique_elem_count1.keys():
    similarity_score += elem * unique_elem_count2[elem]
print(f"{similarity_score=}")
