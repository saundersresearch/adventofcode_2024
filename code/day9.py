from itertools import groupby

import numpy as np
from tqdm import tqdm

test_string = "2333133121414131402"
input_string = test_string
with open("inputs/day9.txt") as f:
    input_string = f.read()

input_string = input_string.replace("\n", "")

### Part 1
# Turn string into disk blocks
disk_blocks = []
for i, char in enumerate(input_string):
    # Number of blocks
    if i % 2 == 0:
        id = i // 2
        disk_blocks.extend([id] * int(char))
    # Free space
    else:
        blank = "."
        disk_blocks.extend([blank] * int(char))

disk_blocks = np.array(disk_blocks)

# Compress sequence by filling in blank spaces backwards
blank_spaces = np.where(disk_blocks == ".")[0]
blocks_alone = disk_blocks[disk_blocks != "."]

compressed_disk_blocks = disk_blocks.copy()
n_blanks = compressed_disk_blocks[blank_spaces].shape[0]
compressed_disk_blocks[blank_spaces] = blocks_alone[::-1][:n_blanks]

# Remove final ones we've replaced
compressed_disk_blocks = compressed_disk_blocks[: len(blocks_alone)]

# Checksum is sum of id * location
checksum = 0
for idx, id in enumerate(compressed_disk_blocks):
    checksum += idx * int(id)

print(f"{checksum=}")

### Part 2
# Turn string into disk blocks
disk_blocks = []
for i, char in enumerate(input_string):
    # Number of blocks
    if i % 2 == 0:
        id = i // 2
        disk_blocks.extend([id] * int(char))
    # Free space
    else:
        blank = "."
        disk_blocks.extend([-1] * int(char))

# disk_blocks = np.array(disk_blocks)
print(disk_blocks)


# Create dictionary of index: length for all blanks
def create_blank_dict(disk_blocks):
    blank_dict = dict()
    for is_blank, sequence in groupby(enumerate(disk_blocks), lambda x: x[1] == -1):
        if is_blank:
            sequence = list(sequence)
            start_index = sequence[0][0]
            sequence_length = len(sequence)
            blank_dict[start_index] = sequence_length
    return blank_dict


blank_dict = create_blank_dict(disk_blocks)
print(blank_dict)

# print(
#     "".join([str(d) for d in disk_blocks]).replace("-1", "."),
#     dict(sorted(blank_dict.items())),
# )

# Compress sequence by iterating down files and moving whole file IDs that fit into blank spaces
for file_id in tqdm(range(max(disk_blocks), -1, -1)):
    # Where is file?
    file_loc = [i for i, n in enumerate(disk_blocks) if n == file_id]
    file_start = min(file_loc)

    # How large?
    file_size = len(file_loc)

    for idx, seq_size in sorted(blank_dict.items()):
        if seq_size >= file_size and file_start > idx:
            # Put into space
            disk_blocks[idx : (idx + file_size)] = [file_id] * file_size

            # Remove from disk_blocks
            disk_blocks[file_start : (file_start + file_size)] = [-1] * file_size

            # Update dict (this is the major inefficiency)
            blank_dict = create_blank_dict(disk_blocks)

            break

    # tqdm.write(
    #     f"{''.join([str(d) for d in disk_blocks]).replace('-1', '.')},{dict(sorted(blank_dict.items()))}"
    # )

# Checksum is sum of id * location
checksum = 0
for idx, id in enumerate(disk_blocks):
    if id > 0:
        checksum += idx * int(id)

print(f"{checksum=}")
