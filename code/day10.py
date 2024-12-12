with open("inputs/day10.txt") as f:
    input_string = f.read()

topographic_map = [list(line) for line in input_string.splitlines()]
print("\n".join(["".join(row) for row in topographic_map]))

### Part 1
# Find zeros
zeros = [
    (row_idx, col_idx)
    for row_idx, row in enumerate(topographic_map)
    for col_idx, col in enumerate(row)
    if col == "0"
]
# print(zeros)


def get_neighbors(array, idx, n):
    """Look for cardinal direction neighbors of value n at idx"""
    neighbors = [
        (idx[0] + 1, idx[1]),
        (idx[0] - 1, idx[1]),
        (idx[0], idx[1] + 1),
        (idx[0], idx[1] - 1),
    ]
    neighbors = [
        neighbor
        for neighbor in neighbors
        if neighbor[0] >= 0
        and neighbor[0] < len(array)
        and neighbor[1] >= 0
        and neighbor[1] < len(array[0])
        and array[neighbor[0]][neighbor[1]] == n
    ]
    return neighbors


def find_paths(array, idx, final_val):
    """Find paths from value at idx to final_val"""
    value = array[idx[0]][idx[1]]
    neighbors = set([idx])
    while int(value) < final_val:
        update = []
        for neighbor_idx in neighbors:
            update.extend(get_neighbors(array, neighbor_idx, str(int(value) + 1)))
        neighbors = set(update)
        value = str(int(value) + 1)

    return neighbors


trail_scores = [len(find_paths(topographic_map, zero, 9)) for zero in zeros]
print(f"Sum of trail scores: {sum(trail_scores)}")

### Part 2
# Find zeros
zeros = [
    (row_idx, col_idx)
    for row_idx, row in enumerate(topographic_map)
    for col_idx, col in enumerate(row)
    if col == "0"
]


def find_n_paths(array, idx, final_val):
    """Find paths from value at idx to final_val"""
    value = array[idx[0]][idx[1]]
    neighbors = [idx]
    while int(value) < final_val:
        update = []
        for neighbor_idx in neighbors:
            update.extend(get_neighbors(array, neighbor_idx, str(int(value) + 1)))
        neighbors = update.copy()
        value = str(int(value) + 1)

    return len(neighbors)


trail_ratings = [find_n_paths(topographic_map, zero, 9) for zero in zeros]
print(f"Sum of trailhead ratings: {sum(trail_ratings)}")
