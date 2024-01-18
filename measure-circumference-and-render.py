import numpy as np
import trimesh
import pyvista as pv

def load_obj_file(file_path):
    return trimesh.load(file_path)

def extract_contour(mesh, left_point, right_point, tolerance=0.01):
    # Extract vertices between the left and right points, considering a tolerance around the Y-value
    y_value = np.mean([left_point[1], right_point[1]])
    x_min, x_max = sorted([left_point[0], right_point[0]])
    vertices = mesh.vertices
    return vertices[(np.abs(vertices[:, 1] - y_value) < tolerance) &
                    (vertices[:, 0] >= x_min) & (vertices[:, 0] <= x_max)]

def sort_vertices(vertices, center):
    # This is a simplified version. For complex models, more sophisticated methods might be required.
    angles = np.arctan2(vertices[:, 2] - center[2], vertices[:, 0] - center[0])
    return vertices[np.argsort(angles)]

def calculate_circumference(vertices):
    distances = np.linalg.norm(np.diff(vertices, axis=0, append=vertices[0:1]), axis=1)
    return np.sum(distances)

# Load the OBJ file
obj_file_path = 'result_test_512.obj'
mesh = load_obj_file(obj_file_path)

# Define your wrist points (left and right)
left_point = np.array([-0.21978, 0.182487, 0.0553705])  # Replace with your actual left point
right_point = np.array([0.071312, 0.205991, 0.00683572])  # Replace with your actual right point

# Extract and sort the contour vertices
contour_vertices = extract_contour(mesh, left_point, right_point)
wrist_center = np.mean(contour_vertices, axis=0)
sorted_contour = sort_vertices(contour_vertices, wrist_center)

# Calculate the circumference
wrist_circumference = calculate_circumference(sorted_contour)
print("Wrist Circumference:", wrist_circumference)

# Convert Trimesh object to PyVista mesh for rendering
pv_mesh = pv.wrap(mesh)

# Convert the sorted contour vertices to PyVista PolyData
contour_poly = pv.PolyData(sorted_contour)

# Plot using PyVista's plotter
plotter = pv.Plotter()
plotter.add_mesh(pv_mesh, color='white')
plotter.add_mesh(contour_poly, color='red', point_size=10, render_points_as_spheres=True)
plotter.view_vector((1, 0, 0), (0, 0, 0))
plotter.show()
