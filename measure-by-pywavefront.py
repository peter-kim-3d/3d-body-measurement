import numpy as np
import pywavefront

def load_obj_file(file_path):
    """
    Load an OBJ file and return its vertices.
    """
    scene = pywavefront.Wavefront(file_path, collect_faces=True)
    vertices = np.array([scene.vertices[i] for i in scene.mesh_list[0].faces[0]])
    return vertices

def get_model_height(vertices):
    """
    Determine the height of the model from the OBJ file vertices.
    """
    min_z = np.min(vertices[:, 2])  # Assuming Z is the vertical axis
    max_z = np.max(vertices[:, 2])
    return max_z - min_z

def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two 3D points.
    """
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)

def scale_point(point, scaling_factor):
    """
    Apply the scaling factor to a 3D point.
    """
    return np.array(point) * scaling_factor

# Load the OBJ file
obj_file_path = 'result_test_512.obj' 
vertices = load_obj_file(obj_file_path)

# Calculate the model's height
model_height = get_model_height(vertices)


# # Define the real-world height (in the same units as the OBJ file)
# real_world_height = 170  # Replace with the known real-world height

# # Calculate scaling factor
# scaling_factor = real_world_height / model_height

# # Define the points you got from MeshLab
# point1 = (-0.20678, 0.13695, 0.0754229)  
# point2 = (0.072486, 0.145478, -0.00224643)  

# # Scale the points
# scaled_point1 = scale_point(point1, scaling_factor)
# scaled_point2 = scale_point(point2, scaling_factor)

# # Calculate the scaled distance
# scaled_distance = calculate_distance(scaled_point1, scaled_point2)

# print("Scaled Distance:", scaled_distance)
