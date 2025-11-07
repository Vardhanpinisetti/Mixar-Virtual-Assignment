import open3d as o3d

def show(title, path, color):
    mesh = o3d.io.read_triangle_mesh(path)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color(color)

    axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5)
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=title, width=1200, height=800)

    vis.add_geometry(mesh)
    vis.add_geometry(axes)

    # Auto zoom out
    view_ctrl = vis.get_view_control()
    view_ctrl.set_zoom(0.6)        # zoom out
    view_ctrl.set_front([1, -1, 1])
    view_ctrl.set_up([0, 1, 0])
    view_ctrl.set_lookat(mesh.get_center())

    vis.run()
    vis.destroy_window()

show("Min-Max Normalized Mesh", "outputs/normalized_minmax/cube_minmax.obj", [0.2, 0.7, 1.0])
show("Unit Sphere Normalized Mesh", "outputs/normalized_unitsphere/cube_unitsphere.obj", [1.0, 0.6, 0.1])
