import numpy as np
import heapq

with open('inputs/day16.txt') as f:
    input_string = f.read()

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
directions = dict()

heapq.heappush(queue, (0, start_idx, 'E'))

distances[start_idx] = 0
predecessors[start_idx] = None
directions[start_idx] = 'E'

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
        if v not in distances.keys() or alt <= distances[v]:
            predecessors[v] = u_idx
            distances[v] = alt
            directions[v] = u_dir
            heapq.heappush(queue, (alt, v, new_dir))

# Find path from end_idx
next_idx = predecessors[end_idx]
maze_map = maze.copy()
while next_idx is not None:
    maze_map[*next_idx] = 'X'
    next_idx = predecessors[next_idx]

# Best path score is distance at end_idx
best_path_score = distances[end_idx]
print(f'Best path score: {best_path_score}')


### Part 2
# Instead of Dijkstra's, run a BFS to get best_path_score so we can find all best paths
def dijkstra(start_idx, start_dir=None, revisit=True):
    """Get distances from start_idx to all others"""
    queue = [] # Tuples of distance, idx, direction
    visited = set()
    distances = dict()
    predecessors = dict()

    if start_dir is not None:
        heapq.heappush(queue, (0, start_idx, start_dir))
        distances[start_idx] = 0
    else:
        heapq.heappush(queue, (0, start_idx, 'N'))
        heapq.heappush(queue, (0, start_idx, 'S'))
        heapq.heappush(queue, (0, start_idx, 'E'))
        heapq.heappush(queue, (0, start_idx, 'W'))

        distances[start_idx] = 0
    predecessors[start_idx] = start_idx


    while len(queue) > 0:
        _, u_idx, u_dir = heapq.heappop(queue)
        if u_idx == (13,13):
            pass

        # Get neighbors
        neighbors = [
            (u_idx[0]-1, u_idx[1]), # North
            (u_idx[0]+1, u_idx[1]), # South
            (u_idx[0], u_idx[1]+1), # East
            (u_idx[0], u_idx[1]-1), # West
        ]
        neighbors = [n for n in neighbors if n[0] >= 0 and n[0] < maze.shape[0] and n[1] >= 0 and n[1] < maze.shape[1] and maze[*n] != '#']
        for v in neighbors:
            if v in visited:
                continue
            dist, new_dir = calculate_dist(u_idx, v, u_dir)
            alt = distances[u_idx] + dist
            if v not in distances.keys() or alt <= distances[v]:
                predecessors[v] = u_idx
                distances[v] = alt
                directions[v] = u_dir
                heapq.heappush(queue, (alt, v, new_dir))
                if not revisit:
                    visited.add(v) # Adding this reverses the problems

    return distances, predecessors, directions

distances_from_start, pred_start, dir_start = dijkstra(start_idx, start_dir='E')
distances_from_end, pred_end, dir_end = dijkstra(end_idx)

total = 0
on_best_path = []
for key in sorted(distances_from_end.keys()):
    if distances_from_start[key]+distances_from_end[key] == best_path_score:
        total += 1
        on_best_path.append(key)

# For some reason, need to repeat without revisiting to cover the "decision" tiles?
distances_from_start, pred_start, dir_start = dijkstra(start_idx, start_dir='E', revisit=False)
distances_from_end, pred_end, dir_end = dijkstra(end_idx, revisit=False)

for key in sorted(distances_from_end.keys()):
    if distances_from_start[key]+distances_from_end[key] == best_path_score:
        total += 1
        on_best_path.append(key)

# How many tiles are in a best path?x
maze_map = maze.copy()
best_path_tiles = set()
for idx in on_best_path:
    maze_map[*idx] = 'O'
    best_path_tiles.add(idx)
    
print(f'Total tiles along best paths: {len(best_path_tiles)}')