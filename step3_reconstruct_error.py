import os
import numpy as np
import trimesh
import matplotlib.pyplot as plt

INPUT_ORIGINAL = "meshes_original/cube.obj"

# Normalized outputs
NORM_MINMAX = "outputs/normalized_minmax/cube_minmax.obj"
NORM_UNITSPHERE = "outputs/normalized_unitsphere/cube_unitsphere.obj"

# Quantized numpy arrays
Q_MINMAX = "outputs/quantized_minmax/cube_quant.npy"
Q_UNITSPHERE = "outputs/quantized_unitsphere/cube_quant.npy"

# Load original mesh
orig_mesh = trimesh.load(INPUT_ORIGINAL, force='mesh')
orig = np.asarray(orig_mesh.vertices)

bins = 1024

# ----- Method 1 Reconstruction: Min-Max -----
quant_minmax = np.load(Q_MINMAX)
norm_minmax_recon = quant_minmax / (bins - 1)

# load min-max bounds
vmin = orig.min(axis=0)
vmax = orig.max(axis=0)
recon_minmax = norm_minmax_recon * (vmax - vmin) + vmin

# Save reconstructed mesh
mesh_rec1 = trimesh.Trimesh(vertices=recon_minmax, faces=orig_mesh.faces)
mesh_rec1.export("outputs/reconstructed_minmax.obj")

mse_minmax = np.mean((orig - recon_minmax) ** 2)

# ----- Method 2 Reconstruction: Unit Sphere -----
quant_us = np.load(Q_UNITSPHERE)
norm_us_recon = quant_us / (bins - 1)
norm_us_recon = norm_us_recon * 2 - 1

mean = orig.mean(axis=0)
centered = orig - mean
max_radius = np.max(np.linalg.norm(centered, axis=1))
recon_us = norm_us_recon * max_radius + mean

mesh_rec2 = trimesh.Trimesh(vertices=recon_us, faces=orig_mesh.faces)
mesh_rec2.export("outputs/reconstructed_unitsphere.obj")

mse_unitsphere = np.mean((orig - recon_us) ** 2)

print("\n===== ERROR RESULTS =====")
print(f"MSE (Min-Max): {mse_minmax:.10f}")
print(f"MSE (Unit Sphere): {mse_unitsphere:.10f}")

# Plot error per axis
err_minmax = orig - recon_minmax
err_us = orig - recon_us

plt.figure()
plt.plot(err_minmax[:,0], label="X Error (MinMax)")
plt.plot(err_minmax[:,1], label="Y Error (MinMax)")
plt.plot(err_minmax[:,2], label="Z Error (MinMax)")
plt.legend()
plt.title("Reconstruction Error - MinMax")
plt.savefig("outputs/error_minmax.png")

plt.figure()
plt.plot(err_us[:,0], label="X Error (UnitSphere)")
plt.plot(err_us[:,1], label="Y Error (UnitSphere)")
plt.plot(err_us[:,2], label="Z Error (UnitSphere)")
plt.legend()
plt.title("Reconstruction Error - UnitSphere")
plt.savefig("outputs/error_unitsphere.png")

print("\n✅ Step 3 Completed — Reconstruction + Error Analysis Done.")
