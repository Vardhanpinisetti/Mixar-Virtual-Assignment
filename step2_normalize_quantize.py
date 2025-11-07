import os
import numpy as np
import trimesh

INPUT_DIR = "meshes_original"
OUT_NORM_MINMAX = "outputs/normalized_minmax"
OUT_NORM_UNITSPHERE = "outputs/normalized_unitsphere"
OUT_QUANT_MINMAX = "outputs/quantized_minmax"
OUT_QUANT_UNITSPHERE = "outputs/quantized_unitsphere"

os.makedirs(OUT_NORM_MINMAX, exist_ok=True)
os.makedirs(OUT_NORM_UNITSPHERE, exist_ok=True)
os.makedirs(OUT_QUANT_MINMAX, exist_ok=True)
os.makedirs(OUT_QUANT_UNITSPHERE, exist_ok=True)

bins = 1024

mesh_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".obj")]

for fname in mesh_files:
    path = os.path.join(INPUT_DIR, fname)
    mesh = trimesh.load(path, force='mesh')
    V = np.asarray(mesh.vertices)

    # ----- Method 1: Min-Max Normalization -----
    vmin = V.min(axis=0)
    vmax = V.max(axis=0)
    norm_minmax = (V - vmin) / (vmax - vmin)

    mesh_norm1 = trimesh.Trimesh(vertices=norm_minmax, faces=mesh.faces)
    mesh_norm1.export(os.path.join(OUT_NORM_MINMAX, fname.replace(".obj", "_minmax.obj")))

    q1 = np.floor(norm_minmax * (bins - 1)).astype(np.int32)
    np.save(os.path.join(OUT_QUANT_MINMAX, fname.replace(".obj", "_quant.npy")), q1)

    # ----- Method 2: Unit Sphere Normalization -----
    mean = V.mean(axis=0)
    centered = V - mean
    max_radius = np.max(np.linalg.norm(centered, axis=1))
    norm_us = centered / max_radius

    mesh_norm2 = trimesh.Trimesh(vertices=norm_us, faces=mesh.faces)
    mesh_norm2.export(os.path.join(OUT_NORM_UNITSPHERE, fname.replace(".obj", "_unitsphere.obj")))

    norm_us_01 = (norm_us + 1) / 2
    q2 = np.floor(norm_us_01 * (bins - 1)).astype(np.int32)
    np.save(os.path.join(OUT_QUANT_UNITSPHERE, fname.replace(".obj", "_quant.npy")), q2)

print("✅ Step 2 completed: Normalized & Quantized meshes saved.")
