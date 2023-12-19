from mayavi import mlab
import trimesh

# Load the OBJ file
mesh = trimesh.load('path_to_your_obj_file.obj')
x, y, z = mesh.vertices.T

# Create a 3D scatter plot
mlab.points3d(x, y, z, color=(1, 1, 1), scale_factor=0.05)

mlab.show()
