import numpy as np

with open('inputs/day15.txt') as f:
    input_string = f.read()

### Part 1
robot_map, moves = input_string.split('\n\n')
robot_map = [list(line) for line in robot_map.split()]
moves = list(moves.replace('\n', ''))
robot_map = np.array(robot_map)
print(robot_map, moves)

def push(direction):
    robot_location = np.argwhere(robot_map == '@')[0]
    
    to_move = []
    loc = robot_location.copy()

    # Get pushable blocks in front of robot
    while robot_map[loc[0],loc[1]] == '@' or robot_map[loc[0],loc[1]] == 'O':
        new_loc = loc.copy()
        if direction == '<':
            new_loc[1] -= 1
        elif direction == '>':
            new_loc[1] += 1
        elif direction == '^':
            new_loc[0] -= 1
        elif direction == 'v':
            new_loc[0] += 1

        # Can it be moved or is it connected to something movable?
        if robot_map[*new_loc] == '.' or robot_map[*new_loc] == 'O':
            to_move.append((loc, new_loc))
        else:
            return
        loc = new_loc.copy()

    # Now move the items
    for item_loc, new_item_loc in to_move[::-1]:
        robot_map[*new_item_loc] = robot_map[*item_loc]

        # Remove old
        robot_map[*item_loc] = '.'

for move in moves:
    push(move)

# Calculate GPS coordinate
total_gps_coord = 0
for row_idx, row in enumerate(robot_map):
    for col_idx, val in enumerate(row):
        if val == 'O':
            gps_coord = 100*row_idx + col_idx
            total_gps_coord += gps_coord

print(f'{total_gps_coord=}')


### Part 2
robot_map, moves = input_string.split('\n\n')
robot_map = [list(line) for line in robot_map.split()]
moves = list(moves.replace('\n', ''))
robot_map = np.array(robot_map)

# Update robot map
new_robot_map = []
for row_idx, row in enumerate(robot_map):
    new_row = []
    for col_idx, tile in enumerate(row):
        if tile == '#':
            new_row.extend(['#','#'])
        elif tile == 'O':
            new_row.extend(['[',']'])
        elif tile == '.':
            new_row.extend(['.','.'])
        elif tile == '@':
            new_row.extend(['@','.'])
    new_robot_map.append(new_row)

robot_map = np.array(new_robot_map)
print(robot_map)

def push(direction):
    robot_location = np.argwhere(robot_map == '@')[0]
    
    to_visit = [robot_location]
    to_move = []

    # Iterate through indices to visit, adding to to_visit if we have [ or ]
    while len(to_visit) > 0:
        loc = to_visit.pop(0)
        new_loc = loc.copy()
        if direction == '<':
            new_loc[1] -= 1
        elif direction == '>':
            new_loc[1] += 1
        elif direction == '^':
            new_loc[0] -= 1
        elif direction == 'v':
            new_loc[0] += 1

        # Is it blocked?
        if robot_map[*new_loc] == '#':
            to_move = []
            break
        # Can we move and there's nothing else in the way?
        elif robot_map[*new_loc] == '.':
            to_move.append((loc, new_loc))
        # Is there another movable item in the way?
        elif robot_map[*new_loc] == '[' or robot_map[*new_loc] == ']':
            to_move.append((loc, new_loc))

            if not any(np.array_equal(new_loc, arr) for arr in to_visit):
                to_visit.append(new_loc)


            if direction == '^' or direction == 'v':
                if robot_map[*new_loc] == '[':
                    next_visit = np.array([new_loc[0],new_loc[1]+1])
                else:
                    next_visit = np.array([new_loc[0],new_loc[1]-1])
                # Only add if we aren't going to visit it
                if not any(np.array_equal(next_visit, arr) for arr in to_visit):
                    to_visit.append(next_visit)


    # Now move the items
    for item_loc, new_item_loc in to_move[::-1]:
        robot_map[*new_item_loc] = robot_map[*item_loc]

        # Remove old
        robot_map[*item_loc] = '.'

for move in moves:
    push(move)

# Calculate GPS coordinate
total_gps_coord = 0
for row_idx, row in enumerate(robot_map):
    for col_idx, val in enumerate(row):
        if col_idx < len(row) // 2:
            if val == '[':
                gps_coord = 100*row_idx + col_idx
                total_gps_coord += gps_coord 
        elif col_idx > len(row) // 2:
            if val == ']':
                gps_coord = 100*row_idx + col_idx-1
                total_gps_coord += gps_coord

print(f'{total_gps_coord=}')