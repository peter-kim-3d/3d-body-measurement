import numpy as np
import trimesh

def load_obj_file(file_path):
    """
    Load an OBJ file using trimesh and return the mesh object.
    """
    return trimesh.load(file_path)

def get_model_height(mesh):
    """
    Determine the height of the model from the trimesh object, using the Y-axis for height.
    """
    # Use Y-axis (index 1) for height
    bounding_box = mesh.bounds
    min_y = bounding_box[0][1]
    max_y = bounding_box[1][1]
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
mesh = load_obj_file(obj_file_path)

# Calculate the model's height using the Y-axis
model_height = get_model_height(mesh)

# Real-world desired height (170 cm)
real_world_height = 170  # Assuming the height is in cm

# Calculate scaling factor
scaling_factor = real_world_height / model_height

# The points you got from MeshLab
meshlab_point1 = (-0.0609601, 0.874205, 0.113864)
meshlab_point2 = (-0.0609601, -0.793804, 0.113864)

# Calculate the distance between the two points from MeshLab
meshlab_points_distance = calculate_distance(meshlab_point1, meshlab_point2)

# Scale this distance to the real-world size
scaled_meshlab_distance = scale_measurement(meshlab_points_distance, scaling_factor)

print("Model Height (from OBJ file):", model_height)
print("real_world_height:", real_world_height)
print("meshlab_points_distance:", meshlab_points_distance)
print("Scaled Distance Between Points:", scaled_meshlab_distance)
