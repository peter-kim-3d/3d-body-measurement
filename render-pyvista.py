import pyvista as pv

# Load the OBJ file
mesh = pv.read('result_test_512.obj')

# Plot using PyVista's plotter
plotter = pv.Plotter()
plotter.add_mesh(mesh, color='white')

# Set camera position
# The format is (camera_position, focus_point, view_up)
plotter.view_vector((1, 0, 0), (0, 0, 0))

plotter.show()
