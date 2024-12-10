from itertools import combinations

import numpy as np

test_string = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
input_string = test_string
with open("inputs/day8.txt") as f:
    input_string = f.read()

antenna_map = np.array([list(line) for line in input_string.splitlines()])
print(antenna_map)

### Part 1
# Loop through unique non '.' characters
antinode_indices = set()
for frequency in np.unique(antenna_map):
    if frequency == ".":
        continue

    freq_rows, freq_cols = np.where(antenna_map == frequency)
    for (freq1_row, freq1_col), (freq2_row, freq2_col) in combinations(
        zip(freq_rows, freq_cols), 2
    ):
        # Get distances
        height = freq1_row - freq2_row
        width = freq1_col - freq2_col

        # Should we add height/width to freq1 or freq2?
        add_to_first = True if freq1_row + height != freq2_row else False
        antinode1_row = freq1_row + height if add_to_first else freq1_row - height
        antinode1_col = freq1_col + width if add_to_first else freq1_col - width

        antinode2_row = freq2_row - height if add_to_first else freq2_row + height
        antinode2_col = freq2_col - width if add_to_first else freq2_col + width

        # Is it within map
        if (
            0 <= antinode1_row < antenna_map.shape[0]
            and 0 <= antinode1_col < antenna_map.shape[1]
        ):
            antinode_indices.add((antinode1_row, antinode1_col))
        if (
            0 <= antinode2_row < antenna_map.shape[0]
            and 0 <= antinode2_col < antenna_map.shape[1]
        ):
            antinode_indices.add((antinode2_row, antinode2_col))

print(f"There are {len(antinode_indices)} antinodes on the map for Part 1.")

### Part 2
# Loop through unique non '.' characters
antinode_indices = set()
for frequency in np.unique(antenna_map):
    if frequency == ".":
        continue

    freq_rows, freq_cols = np.where(antenna_map == frequency)
    for (freq1_row, freq1_col), (freq2_row, freq2_col) in combinations(
        zip(freq_rows, freq_cols), 2
    ):
        # Get distances
        height = freq1_row - freq2_row
        width = freq1_col - freq2_col

        # If height/width is 0, just repeat the row/col
        # Otherwise, repeat from -antenna_map size to +antenna_map size by height/width, starting off at freq1
        if height == 0:
            antinode_rows = np.repeat(freq1_row, antenna_map.shape[0])
        else:
            antinode_rows = np.arange(-antenna_map.shape[0], antenna_map.shape[0])
            antinode_rows *= height
            antinode_rows += freq1_row
        if width == 0:
            antinode_cols = np.repeat(freq1_col, antenna_map.shape[1])
        else:
            antinode_cols = np.arange(-antenna_map.shape[1], antenna_map.shape[1])
            antinode_cols *= width
            antinode_cols += freq1_col

        for antinode_row, antinode_col in zip(antinode_rows, antinode_cols):
            if (
                0 <= antinode_row < antenna_map.shape[0]
                and 0 <= antinode_col < antenna_map.shape[1]
            ):
                antinode_indices.add((antinode_row, antinode_col))

print(f"There are {len(antinode_indices)} antinodes on the map for Part 2.")
