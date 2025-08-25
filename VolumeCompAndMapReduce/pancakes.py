# Nicolas Urrea
# FSUID: nu22c
# Due Date: July 17th 2025
# The program in this file is the individual work of Nicolas Urrea

import numpy as np

# Read number of boxes and accuracy, then read and normalize each box
def read_input():
    print("Enter Input:")
    n, degacc = input().strip().split()
    n, degacc = int(n), float(degacc)
    boxes = []

    for _ in range(n):
        x1, y1, z1, x2, y2, z2 = map(float, input().strip().split())
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        z1, z2 = sorted([z1, z2])
        boxes.append((x1, x2, y1, y2, z1, z2))

    return boxes, degacc

# Calculate union area of overlapping YZ rectangles using sweep line
def compute_union_area(rects):
    events = []
    for y1, y2, z1, z2 in rects:
        events.append((y1, 1, z1, z2))  # entering 
        events.append((y2, -1, z1, z2)) # leaving 
    events.sort()

    active = []
    last_y = None
    area = 0

     # typ == 1 means we're starting a rectangle, typ == -1 means we're ending one
    for y, typ, z1, z2 in events:
        if last_y is not None and active:
            dy = y - last_y
            merged = merge_intervals(active)
            total_z = sum(z2 - z1 for z1, z2 in merged)
            area += dy * total_z
        if typ == 1:
            active.append((z1, z2))
        else:
            active.remove((z1, z2))
        last_y = y
    return area

# Merge overlapping z-intervals into a union set
def merge_intervals(intervals):
    intervals.sort()
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

# Use a sweep line along the X-axis to compute union volume
def compute_union_volume(boxes):
    events = []
    for x1, x2, y1, y2, z1, z2 in boxes:
        events.append((x1, 1, y1, y2, z1, z2))
        events.append((x2, -1, y1, y2, z1, z2))
    events.sort()

    active = []
    last_x = None
    volume = 0

    for x, typ, y1, y2, z1, z2 in events:
        if last_x is not None and active:
            dx = x - last_x
            union_area = compute_union_area(active)
            volume += dx * union_area
        if typ == 1:
            active.append((y1, y2, z1, z2))
        else:
            active.remove((y1, y2, z1, z2))
        last_x = x
    return volume

# reads input, computes volume, and prints result rounded down to DegAcc
def main():
    boxes, degacc = read_input()
    raw_volume = compute_union_volume(boxes)
    rounded = (raw_volume // degacc) * degacc
    print(f"{rounded:.3f}")

main()