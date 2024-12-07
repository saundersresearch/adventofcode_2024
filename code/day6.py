import numpy as np
from tqdm import tqdm

test_string = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
input_string = test_string
with open("inputs/day6.txt") as f:
    input_string = f.read()

input_array = input_string.splitlines()
input_array = [list(line) for line in input_array]
input_array = np.array(input_array)

### Part 1
# Set up map
init_map = input_array

print(init_map)

guard_char_list = ["^", ">", "v", "<"]

visited_indices = set()
current_map = init_map.copy()
guard_indices = np.where(np.isin(current_map, guard_char_list))
guard_row, guard_col = guard_indices[0][0], guard_indices[1][0]
while True:
    # Find ^, >, < or v character
    direction = current_map[guard_row, guard_col]

    # Reset at index and add to visited set
    current_map[guard_row, guard_col] = "X"
    visited_indices.add((guard_row, guard_col))

    # Move forward according to direction
    if direction == "^":
        update_index = (guard_row - 1, guard_col)
    elif direction == "v":
        update_index = (guard_row + 1, guard_col)
    elif direction == ">":
        update_index = (guard_row, guard_col + 1)
    elif direction == "<":
        update_index = (guard_row, guard_col - 1)

    # Check if still in frame
    if (
        update_index[0] < 0
        or update_index[1] < 0
        or update_index[0] >= current_map.shape[0]
        or update_index[1] >= current_map.shape[1]
    ):
        break

    # Check if next one is a block
    if current_map[*update_index] == "#":
        # Turn to the right
        current_dir_idx = guard_char_list.index(direction)
        direction = guard_char_list[(current_dir_idx + 1) % 4]
        update_index = (guard_row, guard_col)

    # Update
    current_map[*update_index] = direction
    guard_row, guard_col = update_index

print(f"Visited {len(visited_indices)} squares.")

### Part 2
potential_block_indices = visited_indices
cycle_indices = set()
print(current_map)
for potential_block in tqdm(potential_block_indices):
    visited_indices = set()

    current_map = init_map.copy()
    guard_indices = np.where(np.isin(current_map, guard_char_list))
    guard_row, guard_col = guard_indices[0][0], guard_indices[1][0]

    if potential_block == (guard_row, guard_col):
        continue

    # Add block
    current_map[potential_block[0], potential_block[1]] = "#"

    while True:
        # Find ^, >, < or v character
        direction = current_map[guard_row, guard_col]

        # Reset at index and add to visited set
        current_map[guard_row, guard_col] = "X"

        # Have we been here before?
        if (guard_row, guard_col, direction) in visited_indices:
            cycle_indices.add((potential_block))
            break
        else:
            visited_indices.add((guard_row, guard_col, direction))
        # Move forward according to direction
        if direction == "^":
            update_index = (guard_row - 1, guard_col)
        elif direction == "v":
            update_index = (guard_row + 1, guard_col)
        elif direction == ">":
            update_index = (guard_row, guard_col + 1)
        elif direction == "<":
            update_index = (guard_row, guard_col - 1)

        # Check if still in frame
        if (
            update_index[0] < 0
            or update_index[1] < 0
            or update_index[0] >= current_map.shape[0]
            or update_index[1] >= current_map.shape[1]
        ):
            break

        # Check if next one is a block
        if current_map[*update_index] == "#":
            # Turn to the right
            current_dir_idx = guard_char_list.index(direction)
            direction = guard_char_list[(current_dir_idx + 1) % 4]
            update_index = (guard_row, guard_col)

        # Update
        current_map[*update_index] = direction
        guard_row, guard_col = update_index

print(f"There are {len(cycle_indices)} places to put a cycle")
