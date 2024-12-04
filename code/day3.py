import re

### Part 1
input_string = (
    "mul(1,1)don't()mul(1,1)don't()mul(1,100)do()mul(1,1)do()mul(1,1)don't()mul(1,1)"
)
with open("inputs/day3.txt") as f:
    input_string = f.read()

# Remove newlines
input_string = input_string.replace("\n", "")

# Regex for finding mul(#,#)
pattern = r"mul\([0-9]*,[0-9]*\)"
matches = re.findall(pattern, input_string)

total = 0
for match in matches:
    numbers = re.findall(r"[0-9]+", match)
    numbers = [int(n) for n in numbers]

    total += numbers[0] * numbers[1]

print(f"{total=}")

### Part 2
# Identify pattern don't()...do() or don't()...<END> and remove
disable_pattern = r"(?:don\'t\(\).*?do\(\)|don\'t\(\).*?(?!do\(\))$)"

new_string = input_string
match = re.search(disable_pattern, new_string)
while match is not None:
    print(new_string)
    new_string = new_string.replace(match.group(0), "")
    match = re.search(disable_pattern, new_string)

print(new_string)

pattern = r"mul\([0-9]*,[0-9]*\)"
matches = re.findall(pattern, new_string)

total = 0
for match in matches:
    numbers = re.findall(r"[0-9]+", match)
    numbers = [int(n) for n in numbers]
    total += numbers[0] * numbers[1]

print(f"{total=}")  # > 79842763