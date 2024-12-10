import heapq
from itertools import groupby
from collections import defaultdict

import line_profiler
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


# Create a heap of all the gaps, sorted by gap length
def create_blank_heaps(disk_blocks):
    blank_heaps = [[] for i in range(10)]
    for is_blank, sequence in groupby(enumerate(disk_blocks), lambda x: x[1] == -1):
        if is_blank:
            sequence = list(sequence)
            start_index = sequence[0][0]
            sequence_length = len(sequence)
            blank_heaps[sequence_length].append(start_index)

    # Heapify
    [heapq.heapify(blank_heap) for blank_heap in blank_heaps]
    return blank_heaps


blank_heaps = create_blank_heaps(disk_blocks)
print(blank_heaps, "".join([str(d) for d in disk_blocks]).replace("-1", "."))
print(disk_blocks)

# Create locations of each file id and store in dict file_id: (index, length)
file_loc_dict = defaultdict(lambda: {"start": None, "size": 0})
for idx, file_id in enumerate(disk_blocks):
    if file_id != -1:
        if file_loc_dict[file_id]["start"] is None:
            file_loc_dict[file_id]["start"] = idx  # Set start index
        file_loc_dict[file_id]["size"] += 1     # Increment size

# @line_profiler.profile
def get_new_seq():
    # Compress sequence by iterating down files and moving whole file IDs that fit into blank spaces
    for file_id in tqdm(range(max(disk_blocks), -1, -1)):
        # Where is file?
        file_start = file_loc_dict[file_id]["start"]
        file_size = file_loc_dict[file_id]["size"]

        # Is there a spot that fits this?
        # Get a list of smallest index for each
        leftmost_indices = [
            heap[0] if len(heap) > 0 and i >= file_size else len(disk_blocks)
            for i, heap in enumerate(blank_heaps)
        ]

        # Find min that fits
        min_index = min(leftmost_indices)
        min_heap_index = leftmost_indices.index(min_index)

        if min_index < len(disk_blocks) and min_index < file_start:
            new_idx = heapq.heappop(blank_heaps[min_heap_index])

            # Put into space
            disk_blocks[new_idx : new_idx + file_size] = [file_id] * file_size

            # Remove from old space
            disk_blocks[file_start : file_start + file_size] = [-1] * file_size

            # Update heap
            new_size = min_heap_index - file_size
            if new_size > 0:
                heapq.heappush(blank_heaps[new_size], new_idx + file_size)

            # Update dict
            file_loc_dict[file_id]["start"] = new_idx
            file_loc_dict[file_id]["size"] = file_size

        # print(blank_heaps, "".join([str(d) for d in disk_blocks]).replace("-1", "."))

# Checksum is sum of id * location
checksum = 0
for idx, id in enumerate(disk_blocks):
    if id > 0:
        checksum += idx * int(id)

print(f"{checksum=}")
