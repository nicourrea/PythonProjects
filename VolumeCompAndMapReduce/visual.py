# Nicolas Urrea
# FSUID: nu22c
# Due Date: July 17th 2025
# The program in this file is the individual work of Nicolas Urrea


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import random

# Make 10 random pancake cuboids
num_pancakes = 10
pancakes = []
for _ in range(num_pancakes):
    x0 = random.uniform(0, 80)
    y0 = random.uniform(0, 80)
    z0 = random.uniform(0, 80)
    dx = random.uniform(5, 20)
    dy = random.uniform(5, 20)
    dz = random.uniform(5, 20)
    pancakes.append(((x0, y0, z0), (x0 + dx, y0 + dy, z0 + dz)))

# Make all 8 corners of the box
def get_box_vertices(xmin, xmax, ymin, ymax, zmin, zmax):
    return [
        [xmin, ymin, zmin],
        [xmin, ymax, zmin],
        [xmax, ymax, zmin],
        [xmax, ymin, zmin],
        [xmin, ymin, zmax],
        [xmin, ymax, zmax],
        [xmax, ymax, zmax],
        [xmax, ymin, zmax]
    ]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("3D Pancake Visualization with Bounding Boxes")

# Draw each pancake (blue transparent box)
for (min_corner, max_corner) in pancakes:
    verts = get_box_vertices(min_corner[0], max_corner[0],
                             min_corner[1], max_corner[1],
                             min_corner[2], max_corner[2])

    # 6 faces of the box
    faces = [
        [verts[0], verts[1], verts[2], verts[3]],
        [verts[4], verts[5], verts[6], verts[7]],
        [verts[0], verts[1], verts[5], verts[4]],
        [verts[2], verts[3], verts[7], verts[6]],
        [verts[1], verts[2], verts[6], verts[5]],
        [verts[4], verts[7], verts[3], verts[0]],
    ]

    box = Poly3DCollection(faces, facecolors='blue', linewidths=1, edgecolors='black', alpha=0.3)
    ax.add_collection3d(box)

# Set limits of the cube
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
ax.set_zlim([0, 100])
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()