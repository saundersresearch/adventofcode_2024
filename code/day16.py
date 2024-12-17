import numpy as np
import heapq
from adam_viz import Grid, Animation
from queue import Queue

input_string = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
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

print(maze_map)

# Best path score is distance at end_idx
best_path_score = distances[end_idx]
print(f'{best_path_score=}')

print(directions)

### Part 2
# BFS on Djikstra distances
print(distances)

# How many tiles are in a best path?
maze_map = maze.copy()
best_path_tiles = set()
for idx, score in distances.items():
    if score <= best_path_score:
        maze_map[*idx] = 'O'

print('\n'.join(''.join(row) for row in maze_map))


# Instead of Dijkstra's, run a BFS to get best_path_score so we can find all best paths
queue = Queue()
queue.put([(0,end_idx,'N')])
queue.put([(0,end_idx,'S')])
queue.put([(0,end_idx,'E')])
queue.put([(0,end_idx,'W')])


best_paths = []
while not queue.empty():
    print(f'{queue.qsize()=}')
    path = queue.get()
    
    # Is path at start node and score is best_path_score?
    path_end_score, path_end_idx, path_end_dir = path[-1]

    if maze[*path_end_idx] == 'S':
        path_idxs = [p[1] for p in path]
        best_paths.append(path_idxs)
        continue
    
    print(path)
    path_scores = [p[0] for p in path]
    path_idxs = [p[1] for p in path]
#     path_dirs = [p[2] for p in path]

    # Get neighbors
    neighbors = [
        ((path_end_idx[0]-1, path_end_idx[1]), 'S'),
        ((path_end_idx[0]+1, path_end_idx[1]), 'N'),
        ((path_end_idx[0], path_end_idx[1]-1), 'W'),
        ((path_end_idx[0], path_end_idx[1]+1), 'E'),
    ]
    neighbors = [n for n in neighbors if n[0][0] >= 0 and n[0][0] < maze.shape[0] and n[0][1] >= 0 and n[0][1] < maze.shape[1] and maze[*n[0]] != '#']
    
    for v, dir in neighbors:
        if v not in path_idxs:
            # print(path_end_idx, v)
            # dist, new_dir = calculate_dist(path_end_idx, v, path_end_dir)
            # new_path_score = path_scores[len(path)-1] + dist            
            
            # Find distance from neighbor to path end and direction

            dist, new_dir = calculate_dist(v, path_end_idx, path_end_dir) 
            print(f'{v=}? {path_end_idx=}, {dir=}, {dist=}, {new_dir=}, {path_end_score=}')

            # Want to get current path score
            current_path_score = distances[*v]
            current_end_score = distances[*path_end_idx]
            total_dist = dist + path_end_score

            print(f'{current_path_score=}')
            print(f'{path_end_score=}')
            print(f'{current_end_score=}')
            print(f'{total_dist=}')

            # Is dist + current_path_score = best_path_score?
            if current_end_score + total_dist - 1 == best_path_score:
                print('YES!')
                new_path = path.copy()
                new_path.append((total_dist, v, new_dir))
                queue.put(new_path)

            # dist, new_dir = calculate_dist(v, path_end_idx, path_end_dir) # THIS IS THE MISTAKE - NOT THE RIGHT DIR? WHEN TURNING
            # new_path_score = distances[*v] if v in distances else np.inf
            # print(f'{v=} {new_dir=} {dist=}, {new_path_score=}, {path_end_score=} {new_path_score+dist+path_end_score}')
            # print(f'{distances[*path_end_idx] + path_end_score}')
            # if v == (np.int64(12), np.int64(13)):
            #     pass
            # if distances[*path_end_idx] + path_end_score == best_path_score:
            #     print(f'ADDING {(distances[*path_end_idx] - dist, v, new_dir)}')
            #     new_path = path.copy()
            #     new_path.append((distances[*path_end_idx] - dist, v, new_dir))
            #     queue.put(new_path)

# How many tiles are in a best path?
maze_map = maze.copy()
best_path_tiles = set()
for path in best_paths:
    # print(best_paths)
    for idx in path:
        maze_map[*idx] = 'O'
        best_path_tiles.add(idx)
    
print('\n'.join(''.join(row) for row in maze_map))
print(f'Total tiles along best paths: {len(best_path_tiles)}')