import os
import numpy as np
import pandas as pd
import trimesh

INPUT_DIR = "meshes_original"
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

rows = []
mesh_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".obj")]
if not mesh_files:
    print("No .obj files found in 'meshes_original/'.")
    print("Tip: Copy sample_meshes/cube.obj into meshes_original/ and run again.")
    raise SystemExit(0)

for fname in mesh_files:
    path = os.path.join(INPUT_DIR, fname)
    mesh = trimesh.load(path, force='mesh')

    if not hasattr(mesh, "vertices") or mesh.vertices is None or len(mesh.vertices) == 0:
        print(f"[WARN] {fname} has no vertices; skipping.")
        continue

    V = np.asarray(mesh.vertices)
    n_vertices = V.shape[0]

    vmin = V.min(axis=0)
    vmax = V.max(axis=0)
    vmean = V.mean(axis=0)
    vstd = V.std(axis=0)
    bbox_diag = float(np.linalg.norm(vmax - vmin))

    rows.append({
        "file": fname,
        "n_vertices": n_vertices,
        "xmin": vmin[0], "ymin": vmin[1], "zmin": vmin[2],
        "xmax": vmax[0], "ymax": vmax[1], "zmax": vmax[2],
        "x_mean": vmean[0], "y_mean": vmean[1], "z_mean": vmean[2],
        "x_std": vstd[0], "y_std": vstd[1], "z_std": vstd[2],
        "bbox_diag": bbox_diag
    })

df = pd.DataFrame(rows)
csv_path = os.path.join(OUT_DIR, "step1_vertex_stats.csv")
df.to_csv(csv_path, index=False)

with pd.option_context("display.max_columns", None, "display.width", 120):
    print(df)
print(f"\nSaved stats to: {csv_path}")

import open3d as o3d

first = os.path.join(INPUT_DIR, df.iloc[0]['file'])
mesh_o3d = o3d.io.read_triangle_mesh(first)

mesh_o3d.compute_vertex_normals()

# Color the mesh so it's visible
mesh_o3d.paint_uniform_color([0.1, 0.8, 0.2])   # green color

# Add coordinate frame so orientation is visible
axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.8)

o3d.visualization.draw_geometries(
    [mesh_o3d, axes],
    window_name="Original Mesh View",
    width=1000,
    height=800,
    mesh_show_back_face=True
)

