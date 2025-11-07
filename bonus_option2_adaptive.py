import trimesh
import numpy as np
import matplotlib.pyplot as plt
import os

input_file = "meshes_original/cube.obj"  # Use your input mesh
mesh = trimesh.load(input_file)
vertices = np.array(mesh.vertices)

# ------------------- UNIFORM QUANTIZATION -------------------
v_min = vertices.min(axis=0)
v_max = vertices.max(axis=0)
v_norm_uniform = (vertices - v_min) / (v_max - v_min)
q_uniform = np.round(v_norm_uniform * 1023).astype(np.int32)
v_recon_uniform = q_uniform / 1023 * (v_max - v_min) + v_min

# ------------------- ADAPTIVE QUANTIZATION -------------------
v_std = vertices.std(axis=0)
weights = 1 / (v_std + 1e-6)
v_norm_adaptive = (vertices * weights - (vertices * weights).min(axis=0)) / \
                  ((vertices * weights).max(axis=0) - (vertices * weights).min(axis=0))

q_adaptive = np.round(v_norm_adaptive * 1023).astype(np.int32)
v_recon_adaptive = q_adaptive / 1023
v_recon_adaptive = v_recon_adaptive / weights

# ------------------- ERROR CALCULATION -----------------------
mse_uniform = np.mean((vertices - v_recon_uniform) ** 2)
mse_adaptive = np.mean((vertices - v_recon_adaptive) ** 2)

print("\n===== BONUS ERROR RESULTS =====")
print(f"Uniform Quantization MSE     : {mse_uniform:.10f}")
print(f"Adaptive Quantization MSE    : {mse_adaptive:.10f}")

# ------------------- PLOT COMPARISON -------------------------
plt.figure(figsize=(6,4))
methods = ["Uniform", "Adaptive"]
errors = [mse_uniform, mse_adaptive]
plt.bar(methods, errors)
plt.ylabel("MSE Error")
plt.title("Uniform vs Adaptive Quantization Error")
plt.savefig("Bonus Task/bonus_error_barplot.png")
plt.close()

print("\n✅ Bonus Task Completed: Results saved in 'Bonus Task' folder.\n")
