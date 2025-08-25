# Nicolas Urrea
# FSUID: nu22c
# Due Date: July 17th 2025
# The program in this file is the individual work of Nicolas Urrea

import sys
import csv

# check arguments
if len(sys.argv) != 3:
    print("Usage: python3 mapper.py input.csv output.csv")
    sys.exit(1)

# get filenames
input_file = sys.argv[1]
output_file = sys.argv[2]

# setup lists
row_means = []
col_sums = []

# read csv file
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

    if not rows:
        sys.exit("Empty file")

    num_cols = len(rows[0])
    col_sums = [0.0] * num_cols

    # process each row
    for row in rows:
        numbers = [float(x) for x in row]
        row_mean = sum(numbers) / len(numbers)
        row_means.append(row_mean)

        for i, val in enumerate(numbers):
            col_sums[i] += val

# write output
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow([round(mean, 4) for mean in row_means])
    writer.writerow([round(total, 4) for total in col_sums])