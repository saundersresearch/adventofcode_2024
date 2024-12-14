import re
from functools import reduce
from operator import mul
import numpy as np
from scipy.stats import entropy 

n_seconds = 100
n_cols = 101
n_rows = 103
with open('inputs/day14.txt') as f:
    input_string = f.read()

### Part 1
# Loop through to create  
robots = [] # List of [(pos_x, pos_y), (vel_x, vel_y)]
for line in input_string.splitlines():
    numbers = re.findall(r'\-?\d+', line)
    numbers = [int(n) for n in numbers]
    robots.append([(numbers[1],numbers[0]), (numbers[3],numbers[2])])

print(robots)

# Now loop through and update 
for second in range(n_seconds):
    for idx, robot in enumerate(robots):
        (pos_y, pos_x), (vel_y, vel_x) = robot
        pos_x = pos_x + vel_x
        pos_y = pos_y + vel_y

        # Wrap around
        if pos_x >= n_cols or pos_x < 0:
            pos_x = pos_x % n_cols
        if pos_y >= n_rows or pos_y < 0:
            pos_y = pos_y % n_rows

        # Reassign
        robots[idx][0] = (pos_y, pos_x)

# Count how many are in each quadrant
sum_quadrants = [0,0,0,0]
for robot in robots:
    (pos_y, pos_x), _ = robot
    if pos_y < n_rows // 2 and pos_x < n_cols // 2:
        sum_quadrants[0] += 1
    elif pos_y < n_rows // 2 and pos_x > n_cols // 2:
        sum_quadrants[1] += 1
    elif pos_y > n_rows // 2 and pos_x > n_cols // 2:
        sum_quadrants[2] += 1
    elif pos_y > n_rows // 2 and pos_x < n_cols // 2:
        sum_quadrants[3] += 1

safety_factor = reduce(mul, sum_quadrants)
print(f'{safety_factor=}')

### Part 2
n_seconds = 10000

# Loop through to create  
robots = [] # List of [(pos_x, pos_y), (vel_x, vel_y)]
for line in input_string.splitlines():
    numbers = re.findall(r'\-?\d+', line)
    numbers = [int(n) for n in numbers]
    robots.append([(numbers[1],numbers[0]), (numbers[3],numbers[2])])

# Now loop through and update 
mutual_infos = []
for second in range(n_seconds):
    positions_x = []
    positions_y = []
    for idx, robot in enumerate(robots):
        (pos_y, pos_x), (vel_y, vel_x) = robot
        pos_x = pos_x + vel_x
        pos_y = pos_y + vel_y

        # Wrap around
        if pos_x >= n_cols or pos_x < 0:
            pos_x = pos_x % n_cols
        if pos_y >= n_rows or pos_y < 0:
            pos_y = pos_y % n_rows

        # Reassign
        robots[idx][0] = (pos_y, pos_x)
        
        positions_x.append(pos_x)
        positions_y.append(pos_y)

    # Get distribution of pos_x and pos_y to calculate mutual information
    hist = np.histogram2d(positions_x, positions_y, bins=20, density=True)[0]
    x_prob = hist.sum(axis=1)
    y_prob = hist.sum(axis=0)
    x_entropy = entropy(x_prob)
    y_entropy = entropy(y_prob)
    joint_entropy = entropy(hist.ravel())
    mutual_info = x_entropy + y_entropy - joint_entropy

    mutual_infos.append(mutual_info)
    print(f'MI at {second+1}: {mutual_info}')

min_mi = max(mutual_infos)
min_mi_time = mutual_infos.index(min_mi)
print(f'{min_mi=} at {min_mi_time+1} seconds')