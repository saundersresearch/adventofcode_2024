import numpy as np
import heapq
from adam_viz import Grid, Animation
from copy import deepcopy

input_string = """#####
#..E#
#...#
#...#
#S..#
#####
"""
# with open('inputs/day16.txt') as f:
#     input_string = f.read()

### Part 1
maze = [list(line) for line in input_string.split()]
maze = np.array(maze)
maze_width = maze.shape[1]
maze_height = maze.shape[0]
print(maze)

# Use Dijkstra's algorithm to find path
start_idx = tuple(np.argwhere(maze == 'S')[0])
end_idx = tuple(np.argwhere(maze == 'E')[0])

queue = [] # Tuples of distance, idx, direction
distances = dict()
predecessors = dict()

heapq.heappush(queue, (0, start_idx, 'E'))

distances[start_idx] = 0
predecessors[start_idx] = None

def calculate_dist(u, v, dir):
    """Calculate distance between neighbors u and v and new direction."""
    diff = (u[0]-v[0], u[1]-v[1])
    if diff[0] == 1 and diff[1] == 0:  
        new_dir = 'N'
    elif diff[0] == -1 and diff[1] == 0:  
        new_dir = 'S'
    elif diff[0] == 0 and diff[1] == 1: 
        new_dir = 'W' 
    elif diff[0] == 0 and diff[1] == -1:
        new_dir = 'E'
    
    dist = 1 if new_dir == dir else 1001
    return dist, new_dir 


while len(queue) > 0:
    _, u_idx, u_dir = heapq.heappop(queue)

    # Get neighbors
    neighbors = [
        (u_idx[0]-1, u_idx[1]), # North
        (u_idx[0]+1, u_idx[1]), # South
        (u_idx[0], u_idx[1]+1), # East
        (u_idx[0], u_idx[1]-1), # West
    ]
    neighbors = [n for n in neighbors if n[0] >= 0 and n[0] < maze.shape[0] and n[1] >= 0 and n[1] < maze.shape[1] and maze[*n] != '#']
    
    for v in neighbors:
        dist, new_dir = calculate_dist(u_idx, v, u_dir)
        alt = distances[u_idx] + dist
        if v not in distances.keys() or alt < distances[v]:
            predecessors[v] = u_idx
            distances[v] = alt
            heapq.heappush(queue, (alt, v, new_dir))

# Find path from end_idx
next_idx = predecessors[end_idx]
maze_map = maze.copy()
while next_idx is not None:
    maze_map[*next_idx] = 'X'
    next_idx = predecessors[next_idx]

print(maze_map)

# Best path score is distance at end_idx
best_path_score = distances[end_idx]
print(f'{best_path_score=}')
