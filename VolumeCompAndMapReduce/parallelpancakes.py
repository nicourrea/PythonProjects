# Nicolas Urrea
# FSUID: nu22c
# Due Date: July 17th 2025
# The program in this file is the individual work of Nicolas Urrea

import multiprocessing as mp
import random

# Function to count hits in chunk of points
def chunked_hits(start, end, shapes, xmin, xmax, ymin, ymax, zmin, zmax):
    count = 0
    for _ in range(start, end):
        x = random.uniform(xmin, xmax)
        y = random.uniform(ymin, ymax)
        z = random.uniform(zmin, zmax)
        for x1, x2, y1, y2, z1, z2 in shapes:
            if x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2:
                count += 1
                break
    return count

if __name__ == "__main__":
    mp.set_start_method("fork")  

    print("Enter Input:")
    n, DegAcc = input().strip().split()  # Read number and accuracy
    n = int(n)
    DegAcc = float(DegAcc)

    shapes = []  # List of prisms
    xmin = ymin = zmin = float('inf')    # Min bounds
    xmax = ymax = zmax = float('-inf')   # Max bounds

    # Read prism data and update bounds
    for _ in range(n):
        x1, y1, z1, x2, y2, z2 = map(float, input().split())
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        z1, z2 = sorted([z1, z2])
        shapes.append((x1, x2, y1, y2, z1, z2))
        xmin = min(xmin, x1)
        xmax = max(xmax, x2)
        ymin = min(ymin, y1)
        ymax = max(ymax, y2)
        zmin = min(zmin, z1)
        zmax = max(zmax, z2)

    num_processes = 150  # Number of parallel processes
    points_total = 10000 * num_processes  # Total random points
    step = points_total // num_processes  # Points per process

    # Start parallel jobs
    with mp.Pool(num_processes) as pool:
        jobs = [
            pool.apply_async(chunked_hits, args=(
                i * step, (i + 1) * step, shapes,
                xmin, xmax, ymin, ymax, zmin, zmax
            )) for i in range(num_processes)
        ]

        hits = sum(job.get() for job in jobs)  # Count total hits

    # Compute volume estimate
    box_volume = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)
    estimated_volume = (hits / points_total) * box_volume
    rounded_volume = (estimated_volume // DegAcc) * DegAcc
    print(f"{rounded_volume:.3f}")  # Print final volume