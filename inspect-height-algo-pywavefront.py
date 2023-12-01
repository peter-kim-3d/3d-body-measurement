import numpy as np
import pywavefront

def load_obj_file(file_path):
    """
    Load an OBJ file and return its vertices as a 2D array.
    """
    scene = pywavefront.Wavefront(file_path, collect_faces=True)
    # Collect all vertices into a 2D list
    vertices_list = []
    for mesh in scene.mesh_list:
        for face in mesh.faces:
            for vertex_i in face:
                vertices_list.append(scene.vertices[vertex_i])
    return np.array(vertices_list)

def get_model_height(vertices):
    """
    Determine the height of the model from the OBJ file vertices, using the Y-axis for height.
    """
    # Use Y-axis for height
    min_y = np.min(vertices[:, 1])
    max_y = np.max(vertices[:, 1])
    return max_y - min_y

def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two 3D points.
    """
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)

def scale_measurement(measured_distance, scaling_factor):
    """
    Scale the measured distance by the scaling factor.
    """
    return measured_distance * scaling_factor

# Load the OBJ file
obj_file_path = 'result_test_512.obj'  # Your specified OBJ file path
vertices = load_obj_file(obj_file_path)

# Calculate the model's height using the Y-axis
model_height = get_model_height(vertices)

# Real-world desired height (170 cm)
real_world_height = 170  # Converted to meters to match the units of model_height

# Calculate scaling factor
scaling_factor = real_world_height / model_height

# The points you got from MeshLab
meshlab_point1 = (-0.070083238, 0.88559955, 0.097375318) 
meshlab_point2 = (-0.070083238, -0.732373, 0.097375318)

# Calculate the distance between the two points from MeshLab
meshlab_points_distance = calculate_distance(meshlab_point1, meshlab_point2)

# Scale this distance to the real-world size
scaled_meshlab_distance = scale_measurement(meshlab_points_distance, scaling_factor)

print("Model Height (from OBJ file):", model_height)
print("real_world_height:", real_world_height)
print("meshlab_points_distance:", meshlab_points_distance)
print("Scaled Distance Between Points:", scaled_meshlab_distance)
