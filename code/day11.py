from tqdm import tqdm
from collections import Counter, defaultdict

with open('inputs/day11.txt') as f:
    input_string = f.read()

### Part 1
stones = input_string.split(" ")
stones = [int(stone) for stone in stones]
print(stones)

# Blink
def blink(stones, n_blinks=1):
    for n in tqdm(range(n_blinks)):
        to_insert = dict()
        for idx, stone in enumerate(stones):
            if stone == 0:
                stones[idx] = 1
            elif len(str(stone)) % 2 == 0:
                stone = str(stone)
                to_insert[idx] = (int(stone[:len(stone)//2]), int(stone[len(stone)//2:]))
            else:
                stones[idx] = stone*2024

        for i, (idx, (left_stone, right_stone)) in enumerate(sorted(to_insert.items())):
            stones[idx+i] = right_stone
            stones.insert(idx+i, left_stone)

    return stones

stones_after_blink = blink(stones, n_blinks=25)
print(f'There are {len(stones_after_blink)} stones.')

### Part 2 
stones = input_string.split(" ")
stones = [int(stone) for stone in stones]
stones = defaultdict(lambda: 0, Counter(stones).items())
print(stones.items())

# Blink
def blink(stones, n_blinks=1):
    for n in range(n_blinks):
        to_insert = defaultdict(lambda: 0)
        for (stone, count) in stones.items():
            if stone == 0:
                # Remove 0 stone and add 1
                to_insert[0] -= count
                to_insert[1] += count
            elif len(str(stone)) % 2 == 0:
                # Remove old stone and split
                to_insert[stone] -= count
                stone = str(stone)
                to_insert[int(stone[:len(stone)//2])] += count
                to_insert[int(stone[len(stone)//2:])] += count
            else:
                # Replace stone with stone*2024
                to_insert[stone] -= count
                to_insert[stone*2024] += count

        for idx, count_update in to_insert.items():
            stones[idx] += count_update

    return stones

stones_after_blink = blink(stones, n_blinks=75)
n_stones = sum(stones_after_blink.values())
print(f'There are {n_stones} stones.')