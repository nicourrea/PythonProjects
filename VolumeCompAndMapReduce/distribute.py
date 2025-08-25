# Nicolas Urrea
# FSUID: nu22c
# Due Date: July 17th 2025
# The program in this file is the individual work of Nicolas Urrea

import os
import csv
import sys
import subprocess
from multiprocessing import Process

# Reads a CSV file and returns the rows
def read_csv_file(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

# Writes rows to a CSV file
def write_chunk(rows, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# Main program starts here
def main():
    # Ask the user for the input file and number of processes
    input_file = input("Enter the name of the CSV file: ").strip()
    num_procs = int(input("Enter the number of processes required: ").strip())

    # Stop if the file doesn’t exist
    if not os.path.exists(input_file):
        print("Error: file not found.")
        sys.exit(1)

    # Read all the rows from the file
    rows = read_csv_file(input_file)
    if not rows:
        print("Empty file.")
        sys.exit(1)

    # Print how many rows and columns are in the file
    num_rows = len(rows)
    num_cols = len(rows[0])
    print(f"Number of rows in the file: {num_rows}")
    print(f"Number of columns in the file: {num_cols}")

    # Figure out how many rows each chunk should have
    chunk_size = (num_rows + num_procs - 1) // num_procs
    mapper_outputs = []
    processes = []

    # Split the file into chunks and run mappers
    for i in range(num_procs):
        chunk_rows = rows[i * chunk_size: (i + 1) * chunk_size]
        if not chunk_rows:
            continue
        chunk_file = f"chunk_{i}.csv"
        output_file = f"map_out_{i}.csv"
        write_chunk(chunk_rows, chunk_file)
        mapper_outputs.append(output_file)
        p = Process(target=subprocess.run, args=(["python3", "mapper.py", chunk_file, output_file],))
        p.start()
        processes.append((p, chunk_file, output_file))

    # Wait for all mappers to finish
    for p, _, _ in processes:
        p.join()

    # Run the reducer
    reducer_process = subprocess.run(["python3", "reducer.py"] + mapper_outputs)

    # Delete all the temporary files
    for _, chunk_file, output_file in processes:
        if os.path.exists(chunk_file):
            os.remove(chunk_file)
        if os.path.exists(output_file):
            os.remove(output_file)

# Call main if this file is run
if __name__ == "__main__":
    main()