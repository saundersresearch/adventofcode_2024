import numpy as np

test_string1 = """..X...
.SAMX.
.A..A.
XMAS.S
.X....
"""
test_string2 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""
# input_string = test_string2
with open('inputs/day4.txt') as f:
    input_string = f.read()

### Part 1
# Convert to array
str_list = input_string.splitlines()
str_array = [list(line) for line in str_list]
str_array = np.array(str_array)
print(str_array)

str_rows = str_array.shape[0]
str_cols = str_array.shape[1]

# Where are X's?
x_indices = np.where(str_array == "X")

# Create mask of all possible directions we want to sample
sample_dirs = np.array(
    [
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # Down
        [(0, 0), (0, -1), (0, -2), (0, -3)],  # Up
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # Right
        [(0, 0), (-1, 0), (-2, 0), (-3, 0)],  # Left
        [(0, 0), (1, 1), (2, 2), (3, 3)],  # Down-Right
        [(0, 0), (-1, -1), (-2, -2), (-3, -3)],  # Up-Left
        [(0, 0), (1, -1), (2, -2), (3, -3)],  # Down-Left
        [(0, 0), (-1, 1), (-2, 2), (-3, 3)],  # Up-Right
    ]
)

xmas_indices = set()
for row, col in zip(*x_indices):
    sample_indices = np.repeat([[row, col]], sample_dirs.shape[1], axis=0).reshape(
        1, sample_dirs.shape[1], sample_dirs.shape[2]
    )
    sample_indices = np.repeat(sample_indices, sample_dirs.shape[0], axis=0)
    sample_indices = sample_indices + sample_dirs

    # Loop over indices to sample
    for indices in sample_indices:
        # Do not use ones that fall outside of grid
        if (
            np.any(indices < 0)
            or np.any(indices[:, 0] >= str_rows)
            or np.any(indices[:, 1] >= str_cols)
        ):
            continue

        str_sample = str_array[indices[:, 0], indices[:, 1]]
        str_sample = "".join(str_sample)

        if str_sample == "XMAS":
            flattened_indices = tuple(indices.ravel())
            xmas_indices.add(flattened_indices)

num_matches = len(xmas_indices)
print(f'{num_matches=}')

# Now search for X-shaped MAS
# Where are A's?
a_indices = np.where(str_array == "A")

# Create mask of all possible directions we want to sample
sample_dirs = np.array(
    [
        [(-1,-1),(1,1),(-1,1),(1,-1)]
    ]
)

xmas_indices = set()
for row, col in zip(*a_indices):
    sample_indices = np.repeat([[row, col]], sample_dirs.shape[1], axis=0).reshape(
        1, sample_dirs.shape[1], sample_dirs.shape[2]
    )
    sample_indices = np.repeat(sample_indices, sample_dirs.shape[0], axis=0)
    sample_indices = sample_indices + sample_dirs

    # Loop over indices to sample
    for indices in sample_indices:
        # Do not use ones that fall outside of grid
        if (
            np.any(indices < 0)
            or np.any(indices[:, 0] >= str_rows)
            or np.any(indices[:, 1] >= str_cols)
        ):
            continue

        str_sample = str_array[indices[:, 0], indices[:, 1]]
        if ((str_sample[0] == "M" and str_sample[1] == "S") or (str_sample[0] == "S" and str_sample[1] == "M")) \
            and ((str_sample[2] == "M" and str_sample[3] == "S") or (str_sample[2] == "S" and str_sample[3] == "M")):
            flattened_indices = tuple(indices.ravel())
            xmas_indices.add(flattened_indices)

num_matches = len(xmas_indices)
print(f'{num_matches=}')

