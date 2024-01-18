import numpy as np
import trimesh
import pyvista as pv

def load_obj_file(file_path):
    return trimesh.load(file_path)

def extract_wrist_contour(mesh, left_point, right_point):
    # Assuming the wrist is aligned with the Z-axis and X-axis
    z_range = [min(left_point[2], right_point[2]), max(left_point[2], right_point[2])]
    x_range = [min(left_point[0], right_point[0]), max(left_point[0], right_point[0])]
    vertices = mesh.vertices
    # Filter vertices that fall within the specified ranges for x and z
    return vertices[(vertices[:, 0] >= x_range[0]) & (vertices[:, 0] <= x_range[1]) & 
                    (vertices[:, 2] >= z_range[0]) & (vertices[:, 2] <= z_range[1])]

# Load the OBJ file
obj_file_path = 'result_test_512.obj'
mesh = load_obj_file(obj_file_path)

# Define your wrist points (left and right)
left_point = np.array([-0.207575, 0.182487, 0.0553705])  # Replace with actual left point coordinates
right_point = np.array([0.070312, 0.205991, 0.00683572])  # Replace with actual right point coordinates

# Extract the contour vertices
wrist_contour = extract_wrist_contour(mesh, left_point, right_point)


def sort_vertices(vertices, center):
    # Simplified sorting. May need a more complex method for non-planar contours.
    angles = np.arctan2(vertices[:, 2] - center[2], vertices[:, 0] - center[0])
    return vertices[np.argsort(angles)]

def calculate_circumference(vertices):
    distances = np.linalg.norm(np.diff(vertices, axis=0, append=vertices[0:1]), axis=1)
    return np.sum(distances)

# Estimate the center for sorting
wrist_center = np.mean([left_point, right_point], axis=0)

# Sort vertices to form a loop
sorted_wrist_contour = sort_vertices(wrist_contour, wrist_center)

# Calculate circumference
wrist_circumference = calculate_circumference(sorted_wrist_contour)
print("Wrist Circumference:", wrist_circumference)


# Convert to PyVista mesh for rendering
pv_mesh = pv.wrap(mesh)
contour_poly = pv.PolyData(sorted_wrist_contour)

# Plot using PyVista's plotter
plotter = pv.Plotter()
plotter.add_mesh(pv_mesh, color='white')
plotter.add_mesh(contour_poly, color='red', point_size=10, render_points_as_spheres=True)
plotter.show()
