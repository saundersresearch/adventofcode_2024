from pathlib import Path

import numpy as np

### Part 1
input_path = Path("inputs/day2.txt")
with open(input_path, "r") as f:
    num_safe = 0
    for line in f.readlines():
        line = line.strip()
        line_list = line.split(" ")
        report = [int(l) for l in line_list]

        report = np.array(report)
        report_diff = np.diff(report)

        # Needs to be solely increasing or decreasing
        if not np.all(report_diff > 0) and not np.all(report_diff < 0):
            continue

        # Are adjacent levels differing by at least 1 and at most 3
        if np.any(np.abs(report_diff) > 3) or np.any(np.abs(report_diff) < 1):
            continue

        # It's safe
        num_safe += 1

    print(f"{num_safe=}")


### Part 2: tolerate a single bad level
# I think the key is that each of these needs to be true for at least two
def check_report(report):
    report_diff = np.diff(report)
    if not np.all(report_diff > 0) and not np.all(report_diff < 0):
        return False

        # Are adjacent levels differing by at least 1 and at most 3
    if np.any(np.abs(report_diff) > 3) or np.any(np.abs(report_diff) < 1):
        return False

    return True


with open(input_path, "r") as f:
    num_safe = 0
    for line in f:
        line = line.strip()
        line_list = line.split(" ")
        report = [int(l) for l in line_list]

        report = np.array(report)
        report_diff = np.diff(report)

        if check_report(report):
            num_safe += 1
        else:
            # Loop through and remove each index
            for index in range(0, len(report)):
                mask = np.ones(report.shape, dtype=bool)
                mask[index] = False
                new_report = report[mask]

                if check_report(new_report):
                    num_safe += 1
                    break

    print(f"{num_safe=}")
