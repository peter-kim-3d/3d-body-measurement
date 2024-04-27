import numpy as np
import trimesh
import pyvista as pv

def load_obj_file(file_path):
    return trimesh.load(file_path)

def extract_chest_contour(mesh, y_value, tolerance=0.005):
    vertices = mesh.vertices
    return vertices[np.abs(vertices[:, 1] - y_value) < tolerance]

def sort_vertices(vertices, center):
    angles = np.arctan2(vertices[:, 2] - center[2], vertices[:, 0] - center[0])
    return vertices[np.argsort(angles)]

def calculate_circumference(vertices):
    distances = np.linalg.norm(np.diff(vertices, axis=0, append=vertices[0:1]), axis=1)
    return np.sum(distances)

# Load the OBJ file
obj_file_path = 'sub04.obj'
mesh = load_obj_file(obj_file_path)

# Define a point on the head and determine the Y-value for the cross-section
known_point = np.array([-0.375, 0.03125, 0])  # Replace with your actual known point 4. 팔 좌측
y_value = known_point[1]  # or z, depending on your model's orientation

# Extract and sort the contour vertices
contour_vertices = extract_chest_contour(mesh, y_value)
head_center = np.mean(contour_vertices, axis=0)
sorted_contour = sort_vertices(contour_vertices, head_center)

# Calculate the head circumference
head_circumference = calculate_circumference(sorted_contour)
print("Head Circumference:", head_circumference)

# Optional: Visualize
# Convert Trimesh object to PyVista mesh for rendering
pv_mesh = pv.wrap(mesh)
contour_poly = pv.PolyData(sorted_contour)
plotter = pv.Plotter()
plotter.add_mesh(pv_mesh, color='white')
plotter.add_mesh(contour_poly, color='red', point_size=10, render_points_as_spheres=True)
plotter.view_vector((0, 0, 1), (0, 0, 0))
plotter.show()
