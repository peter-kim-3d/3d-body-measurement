import numpy as np
import trimesh
import pyvista as pv

def load_obj_file(file_path):
    """Load a 3D OBJ file and return as a Trimesh object."""
    return trimesh.load(file_path)

def extract_contour(mesh, y_value, side=None, tolerance=0.005, x_threshold=0.01):
    """Extract contour vertices based on y-value, potentially considering side."""
    vertices = mesh.vertices
    potential_vertices = vertices[np.abs(vertices[:, 1] - y_value) < tolerance]

    if len(potential_vertices) == 0:
        return np.array([])  # Return empty array if no vertices are found.

    sorted_vertices = potential_vertices[np.argsort(potential_vertices[:, 0])]
    gaps = np.diff(sorted_vertices[:, 0]) > x_threshold
    gap_indices = np.where(gaps)[0]

    min_x_index = np.argmin(sorted_vertices[:, 0])
    max_x_index = np.argmax(sorted_vertices[:, 0])
    
    # Handling sides
    if side == 'left':
        return sorted_vertices[:gap_indices[0]+1] if gap_indices.size > 0 else sorted_vertices[:min_x_index+1]
    elif side == 'right':
        return sorted_vertices[gap_indices[-1]+1:] if gap_indices.size > 0 else sorted_vertices[max_x_index:]
    else:  # side is None or not specified
        if gap_indices.size >= 2:
            return sorted_vertices[gap_indices[0]+1:gap_indices[1]]
        elif gap_indices.size == 1:
            return sorted_vertices[gap_indices[0]+1:]
        else:
            return sorted_vertices

def project_contour_to_y(contour_vertices, y_value):
    """Project contour vertices onto a plane with a specific y-value."""
    projected_vertices = np.copy(contour_vertices)
    projected_vertices[:, 1] = y_value
    return projected_vertices

def sort_vertices(vertices, center):
    """Sort vertices around a center point based on angles."""
    angles = np.arctan2(vertices[:, 2] - center[2], vertices[:, 0] - center[0])
    return vertices[np.argsort(angles)]

def calculate_circumference(vertices):
    """Calculate the circumference of a closed loop of vertices."""
    if vertices.size == 0:
        return 0
    distances = np.linalg.norm(np.diff(vertices, axis=0, append=vertices[0:1]), axis=1)
    return np.sum(distances)

# Define body parts, points, and colors
body_parts = {
    "head": {"point": [0, 0.820129, 0], "color": "red", "side": None},
    "neck": {"point": [0, 0.630778, 0], "color": "green", "side": None},
    "chest": {"point": [0, 0.33848, 0], "color": "blue", "side": None},
    "left_arm": {"point": [0, 0.258622, 0], "color": "yellow", "side": "left"},
    "right_arm": {"point": [0, 0.258622, 0], "color": "yellow", "side": "right"},
    "wrist": {"point": [0, 0.214794, 0], "color": "purple", "side": None},
    "hip": {"point": [0, 0.0270495, 0], "color": "cyan", "side": None},
    "left_thigh": {"point": [0, -0.170023, 0], "color": "orange", "side": "left"},
    "right_thigh": {"point": [0, -0.170023, 0], "color": "orange", "side": "right"},
}

# Load the OBJ file
obj_file_path = 'generated/sub04.obj'
mesh = load_obj_file(obj_file_path)

# Visualization setup
pv_mesh = pv.wrap(mesh)
plotter = pv.Plotter()

for part, info in body_parts.items():
    y_value = info["point"][1]
    side = info.get("side")
    contour_vertices = extract_contour(mesh, y_value, side)
    projected_contour = project_contour_to_y(contour_vertices, y_value)
    center = np.mean(projected_contour, axis=0) if projected_contour.size > 0 else np.array([0, 0, 0])
    sorted_contour = sort_vertices(projected_contour, center)
    circumference = calculate_circumference(sorted_contour)
    print(f"{part.capitalize()} Circumference: {circumference:.2f}")

    # Add to visualization
    contour_poly = pv.PolyData(sorted_contour)
    plotter.add_mesh(contour_poly, color=info["color"], line_width=5, render_lines_as_tubes=True)

# Add the full mesh to visualization
plotter.add_mesh(pv_mesh, color='white', opacity=0.5)

# Set view vector for visualization
plotter.view_vector((0, 0, 1), (0, 0, 0))
plotter.show()
