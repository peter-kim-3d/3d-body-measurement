import numpy as np
import trimesh
import pyvista as pv

def load_obj_file(file_path):
    return trimesh.load(file_path)

def extract_cylindrical_section(mesh, center_point, radius, height):
    # Calculate distances from the center point along the XY plane and Z axis
    distances_xy = np.linalg.norm(mesh.vertices[:, :2] - center_point[:2], axis=1)
    distances_z = np.abs(mesh.vertices[:, 2] - center_point[2])
    
    # Identify vertices within the specified radius and height
    cylinder_mask = (distances_xy < radius) & (distances_z < height / 2)
    return mesh.vertices[cylinder_mask]

def sort_vertices(vertices, center):
    # Sort vertices around the center point in the XY plane
    angles = np.arctan2(vertices[:, 1] - center[1], vertices[:, 0] - center[0])
    return vertices[np.argsort(angles)]

def calculate_circumference(vertices):
    # Calculate the circumference by summing the distances between sorted vertices
    distances = np.linalg.norm(np.diff(vertices, axis=0, append=vertices[0:1]), axis=1)
    return np.sum(distances)

# Load the OBJ file
obj_file_path = 'sub04.obj'  # Replace with your actual file path
mesh = load_obj_file(obj_file_path)

# Define a point on the wrist and the expected radius and height of the wrist section
wrist_point = np.array([-0.00306554, 0.212611, 0.12693])  # Replace with your actual wrist point
wrist_radius = 0.05  # Replace with an estimated radius for the wrist
wrist_height = 0.05  # Replace with an estimated height for the wrist section

# Extract the cylindrical section around the wrist point
wrist_section = extract_cylindrical_section(mesh, wrist_point, wrist_radius, wrist_height)

# Sort the vertices to form a loop around the center point
wrist_center = np.mean(wrist_section, axis=0)
sorted_wrist_section = sort_vertices(wrist_section, wrist_center)

# Calculate the wrist circumference
wrist_circumference = calculate_circumference(sorted_wrist_section)
print("Wrist Circumference:", wrist_circumference)

# Optional: Visualize
pv_mesh = pv.wrap(mesh)
wrist_section_poly = pv.PolyData(sorted_wrist_section)
plotter = pv.Plotter()
plotter.add_mesh(pv_mesh, color='white')
plotter.add_mesh(wrist_section_poly, color='red', line_width=5, render_lines_as_tubes=True)
plotter.view_vector((0, 0, 1), (0, 0, 0))  # Adjust the viewing vector as needed
plotter.show()

