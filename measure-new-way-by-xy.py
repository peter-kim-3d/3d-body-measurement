import numpy as np
import trimesh
import pyvista as pv

def load_obj_file(file_path):
    return trimesh.load(file_path)

def extract_contour(mesh, y_value, side=None, tolerance=0.01, x_threshold=0.01):
    vertices = mesh.vertices
    # Extract vertices that are within the tolerance along the y-axis
    potential_vertices = vertices[np.abs(vertices[:, 1] - y_value) < tolerance]
    
    # Sort the potential vertices by their x-coordinate
    sorted_vertices = potential_vertices[np.argsort(potential_vertices[:, 0])]
    
    # Find gaps in the x-coordinates that are larger than the threshold
    gaps = np.diff(sorted_vertices[:, 0]) > x_threshold
    gap_indices = np.where(gaps)[0]
    
    # Find the farthest left and right vertices within the potential vertices
    min_x_index = np.argmin(sorted_vertices[:, 0])
    max_x_index = np.argmax(sorted_vertices[:, 0])
    
    if side is None:
        # If 'side' is None, return vertices between the first and second gap if there are more than one gap
        if len(gap_indices) > 1:
            contour_vertices = sorted_vertices[gap_indices[0]+1:gap_indices[1]]
        else:
            # If there are no clear gaps, return all potential vertices
            contour_vertices = potential_vertices
    elif side == 'right':
        # If 'side' is 'left', return vertices from the minimum x up to the first gap
        contour_vertices = sorted_vertices[:gap_indices[0]+1] if len(gap_indices) > 0 else sorted_vertices[:min_x_index+1]
    elif side == 'left':
        # If 'side' is 'right', return vertices from the first gap to the maximum x
        contour_vertices = sorted_vertices[gap_indices[0]+1:] if len(gap_indices) > 0 else sorted_vertices[max_x_index:]
    
    return contour_vertices


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
known_point = np.array([0.0981951, -0.130103, 0])  # Replace with your actual known point 
y_value = known_point[1]  # or z, depending on your model's orientation

# Extract and sort the contour vertices
contour_vertices = extract_contour(mesh, y_value,'left')
center = np.mean(contour_vertices, axis=0)
sorted_contour = sort_vertices(contour_vertices, center)

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


##find general way.
# if gap_indices is 2 -> just filter btw gaps 
# if gap_indices is 1 
#    if gap_indices[0] is less than half