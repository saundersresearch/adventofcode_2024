with open('inputs/day12.txt') as f:
    input_string = f.read()
input_array = [list(line) for line in input_string.splitlines()]
print("\n".join(["".join(row) for row in input_array]))

### Part 1
# Get unique elements
unique_chars = set("".join(["".join(row) for row in input_array]))
print(sorted(unique_chars))

n_rows = len(input_array)
n_cols = len(input_array[0])

# Run connected components to label 
components = [[0]*len(col) for col in input_array]
next_component_number = 1
for char in sorted(unique_chars):
    # Run connected components on this char
    for row_idx, row in enumerate(input_array):
        for col_idx, val in enumerate(row):
            if val == char:

                # What are neighbors?
                neighbors = [(row_idx-1,col_idx),
                            (row_idx+1,col_idx),
                            (row_idx,col_idx-1),
                            (row_idx,col_idx+1)]
                neighbors = [n for n in neighbors if n[0] >= 0 and n[0] < n_rows
                                and n[1] >= 0 and n[1] < n_cols]
                neighbors = [n for n in neighbors if input_array[n[0]][n[1]] == char]
                
                # What are values at neighbors?
                neighbor_vals = [input_array[n[0]][n[1]] for n in neighbors]

                # Are any marked and with what?
                neighbor_components = [components[n[0]][n[1]] for n in neighbors]

                # Case 1: all 4 are unmarked
                if all([c == 0 for c in neighbor_components]):
                    components[row_idx][col_idx] = next_component_number
                    next_component_number += 1
                # Case 2: 1/+ are marked with same
                elif sorted(set(neighbor_components))[0] == 0 and len(sorted(set(neighbor_components))) == 2:
                    components[row_idx][col_idx] = sorted(set(neighbor_components))[1]
                # Case 3: 1/+ are marked with different
                else:
                    equivalent_components = set(neighbor_components)
                    if 0 in equivalent_components:
                        equivalent_components.remove(0)
                    new_component_number = sorted(equivalent_components)[0]
                    components[row_idx][col_idx] = new_component_number
                    for comp_row_idx, comp_row in enumerate(components):
                        for comp_col_idx, comp_val in enumerate(row):
                            if components[comp_row_idx][comp_col_idx] in equivalent_components:
                                components[comp_row_idx][comp_col_idx] = new_component_number
                # print("\n".join(["".join([f'{r:3d}' for r in row]) for row in components]))
                # print("\n")

print("\n".join(["".join([f'{r:3d}' for r in row]) for row in components]))
max_component_number = next_component_number

# Now calculate area/perimeter of each 
total_price = 0
for component_number in range(1,max_component_number):
    component_area = 0
    component_sides = 0
    for row_idx, row in enumerate(components):
        for col_idx, val in enumerate(row):
            if val == component_number:
                component_area += 1

                # What are neighbors?
                neighbors = [(row_idx-1,col_idx),
                            (row_idx+1,col_idx),
                            (row_idx,col_idx-1),
                            (row_idx,col_idx+1)]
                border_neighbors = [n for n in neighbors if n[0] < 0 or n[0] >= n_rows or
                                     n[1] < 0 or n[1] >= n_cols or components[n[0]][n[1]] != val]

                # Sum up bordering neighbors to get perimeter
                component_sides += len(border_neighbors)
    
    total_price += component_area * component_sides 

    print(f'{component_number}: area {component_area}, perimeter: {component_sides}')

print(f'Total price: {total_price}')

### Part 2
# Now calculate area/num sides of each 
total_price = 0
for component_number in range(1,max_component_number):
    component_area = 0
    component_sides = 0
    for row_idx, row in enumerate(components):
        for col_idx, val in enumerate(row):
            if val == component_number:
                component_area += 1

                # Count corners instead of counting sides
                # Sample 8-connected neighbors
                neighbors = [(row_idx-1,col_idx-1),
                            (row_idx-1,col_idx),
                            (row_idx-1,col_idx+1),
                            (row_idx,col_idx-1),
                            (row_idx,col_idx+1),
                            (row_idx+1,col_idx-1),
                            (row_idx+1,col_idx),
                            (row_idx+1,col_idx+1)]
                
                neighbor_vals = [1 if n[0] >= 0 and n[0] < n_rows and n[1] >= 0 and n[1] < n_cols and components[n[0]][n[1]] == val else 0 for n in neighbors]
                cardinal_neighbors = [neighbor_vals[1], neighbor_vals[3], neighbor_vals[4], neighbor_vals[6]] # up, left, right, down
                diagonal_neighbors = [neighbor_vals[0], neighbor_vals[2], neighbor_vals[5], neighbor_vals[7]] # upper-left, upper-right, lower-left, lower-right

                # Corners have equal cardinal values along two directions
                # Interior corners have a 1's at cardinal directions, 0 at diagonal
                # Exterior corners have a 0's at cardinal directions
                # Upper-left
                if cardinal_neighbors[0] == cardinal_neighbors[1]:
                    if cardinal_neighbors[0] == 1 and diagonal_neighbors[0] == 0:
                        component_sides += 1
                    elif cardinal_neighbors[0] == 0:
                        component_sides += 1
                # Upper-right
                if cardinal_neighbors[0] == cardinal_neighbors[2]:
                    if cardinal_neighbors[0] == 1 and diagonal_neighbors[1] == 0:
                        component_sides += 1
                    elif cardinal_neighbors[0] == 0:
                        component_sides += 1                
                # Lower-left
                if cardinal_neighbors[1] == cardinal_neighbors[3]:
                    if cardinal_neighbors[1] == 1 and diagonal_neighbors[2] == 0:
                        component_sides += 1
                    elif cardinal_neighbors[1] == 0:
                        component_sides += 1
                # Lower-right
                if cardinal_neighbors[2] == cardinal_neighbors[3]:
                    if cardinal_neighbors[2] == 1 and diagonal_neighbors[3] == 0:
                        component_sides += 1
                    elif cardinal_neighbors[2] == 0:
                        component_sides += 1
    
    total_price += component_area * component_sides

    print(f'{component_number}: area {component_area}, number of sides: {component_sides}')

print(f'Total price: {total_price}')