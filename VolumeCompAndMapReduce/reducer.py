# Nicolas Urrea
# FSUID: nu22c
# Due Date: July 17th 2025
# The program in this file is the individual work of Nicolas Urrea

import sys
import csv

# check arguments
if len(sys.argv) < 2:
    print("Usage: python3 reducer.py file1.csv file2.csv ...")
    sys.exit(1)

# setup variables
all_row_means = []
total_sum = 0.0
total_count = 0
column_sums = []
column_counts = []

# read each file
for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)

        if len(lines) < 2:
            continue

        row_means = [float(x) for x in lines[0]]
        col_sums = [float(x) for x in lines[1]]

        all_row_means.extend(row_means)
        total_sum += sum(col_sums)
        total_count += len(col_sums) * len(row_means)

        if not column_sums:
            column_sums = col_sums
            column_counts = [len(row_means)] * len(col_sums)
        else:
            for i in range(len(col_sums)):
                column_sums[i] += col_sums[i]
                column_counts[i] += len(row_means)

# compute stats
overall_mean = total_sum / total_count if total_count else 0
median_row_mean = 0
sorted_means = sorted(all_row_means)

# get median
if sorted_means:
    mid = len(sorted_means) // 2
    if len(sorted_means) % 2 == 0:
        median_row_mean = (sorted_means[mid - 1] + sorted_means[mid]) / 2
    else:
        median_row_mean = sorted_means[mid]

# compute column means
column_means = [
    column_sums[i] / column_counts[i]
    for i in range(len(column_sums))
] if column_sums else []

# print result
print(f"{overall_mean:.4f}")
print(f"{median_row_mean:.4f}")
print(",".join(f"{mean:.4f}" for mean in column_means))