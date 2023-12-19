import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import trimesh

# Load the OBJ file
mesh = trimesh.load('result_test_512.obj')
vertices = mesh.vertices
faces = mesh.faces

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the model vertices
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], alpha=0.1)

# Set labels
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

plt.show()
