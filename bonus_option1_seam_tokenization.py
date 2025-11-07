# BONUS OPTION 1 – Seam Tokenization Prototype (version-safe for trimesh)

import os, json, math
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from collections import defaultdict

MESH_PATH = "meshes_original/cube.obj"
OUT_DIR   = "Bonus Task/option1_seams"
ANGLE_DEG = 45.0

os.makedirs(OUT_DIR, exist_ok=True)

mesh = trimesh.load(MESH_PATH, force='mesh')
V = np.asarray(mesh.vertices)
F = np.asarray(mesh.faces)

def has_attr(obj, name):
    try:
        return hasattr(obj, name) and getattr(obj, name) is not None
    except Exception:
        return False

# ---------- seam edges ----------
# sharp (by dihedral angle)
sharp_edges = np.empty((0, 2), dtype=int)
if has_attr(mesh, "face_adjacency_angles") and has_attr(mesh, "face_adjacency_edges"):
    angles = mesh.face_adjacency_angles
    shared_edges = mesh.face_adjacency_edges
    if angles is not None and shared_edges is not None and len(shared_edges) > 0:
        sharp_mask = angles > math.radians(ANGLE_DEG)
        sharp_edges = shared_edges[sharp_mask] if np.any(sharp_mask) else np.empty((0, 2), dtype=int)

# boundary (API differs by version)  <<< THIS IS THE FIX
boundary_edges = np.empty((0, 2), dtype=int)
if has_attr(mesh, "edges_unique_boundary"):
    boundary_edges = mesh.edges_unique_boundary
elif has_attr(mesh, "edges_boundary"):     # very old trimesh
    boundary_edges = mesh.edges_boundary
# if a closed mesh, boundary may be empty – that’s fine

parts = []
if sharp_edges.size > 0: parts.append(sharp_edges)
if boundary_edges.size > 0: parts.append(boundary_edges)
if parts:
    seams = np.vstack(parts)
else:
    # fallback so the prototype still shows something
    seams = mesh.edges_unique

seams = np.unique(np.sort(seams, axis=1), axis=0)

# ---------- build seam graph ----------
G = defaultdict(list)
for u, v in seams:
    G[u].append(v); G[v].append(u)

def extract_chains(graph):
    visited_e = set()
    chains = []
    deg = {n: len(nei) for n, nei in graph.items()}
    endpoints = [n for n, d in deg.items() if d != 2]

    # open chains
    for s in endpoints:
        for nb in graph[s]:
            e = tuple(sorted((s, nb)))
            if e in visited_e: 
                continue
            chain = [s, nb]
            visited_e.add(e)
            prev, cur = s, nb
            while True:
                nxts = [x for x in graph[cur] if x != prev and tuple(sorted((cur, x))) not in visited_e]
                if not nxts: break
                nxt = nxts[0]
                visited_e.add(tuple(sorted((cur, nxt))))
                chain.append(nxt)
                prev, cur = cur, nxt
                if deg.get(cur, 0) != 2: break
            chains.append(chain)

    # cycles
    for n in list(graph.keys()):
        for nb in graph[n]:
            e = tuple(sorted((n, nb)))
            if e in visited_e: 
                continue
            cycle = [n, nb]
            visited_e.add(e)
            prev, cur = n, nb
            while True:
                nxts = [x for x in graph[cur] if x != prev and tuple(sorted((cur, x))) not in visited_e]
                if not nxts: break
                nxt = nxts[0]
                visited_e.add(tuple(sorted((cur, nxt))))
                cycle.append(nxt)
                prev, cur = cur, nxt
                if len(cycle) > 2 and cycle[-1] == cycle[0]:
                    break
            chains.append(cycle)
    return chains

chains = extract_chains(G)

# ---------- tokenization ----------
token_chains = []
for chain in chains:
    tokens = ["BOS"]
    for i in range(len(chain)-1):
        u, v = chain[i], chain[i+1]
        tokens.append(f"E {u} {v}")
    tokens.append("EOS")
    token_chains.append(tokens)

with open(os.path.join(OUT_DIR, "seam_tokens.json"), "w") as f:
    json.dump(token_chains, f, indent=2)

with open(os.path.join(OUT_DIR, "seam_chains.txt"), "w") as f:
    for t in token_chains:
        f.write(" ".join(t) + "\n")

# ---------- sanity: reconstruct from tokens ----------
re_edges = set()
for tks in token_chains:
    for tok in tks:
        if tok.startswith("E "):
            _, a, b = tok.split()
            re_edges.add(tuple(sorted((int(a), int(b)))))

orig = {tuple(sorted(e)) for e in seams}
miss = orig - re_edges
extra = re_edges - orig

# ---------- visualize ----------
from mpl_toolkits.mplot3d import Axes3D  # noqa
fig = plt.figure(figsize=(7,6))
ax = fig.add_subplot(111, projection='3d')

for tri in V[F]:
    xs, ys, zs = tri[:,0], tri[:,1], tri[:,2]
    xs = np.append(xs, xs[0]); ys = np.append(ys, ys[0]); zs = np.append(zs, zs[0])
    ax.plot(xs, ys, zs, color="gray", linewidth=0.5, alpha=0.4)

for (u, v) in seams:
    p, q = V[u], V[v]
    ax.plot([p[0], q[0]],[p[1], q[1]],[p[2], q[2]], color="red", linewidth=2)

ax.set_title("Seam Overlay (red) – boundary/dihedral")
ax.set_box_aspect([1,1,1])
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "seam_overlay.png"), dpi=160)

# ---------- report ----------
report = {
    "mesh": MESH_PATH,
    "n_vertices": int(V.shape[0]),
    "n_faces": int(F.shape[0]),
    "n_seam_edges": int(len(seams)),
    "n_chains": int(len(token_chains)),
    "angle_deg": ANGLE_DEG,
    "reconstruction_missed_edges": len(miss),
    "reconstruction_extra_edges": len(extra)
}
with open(os.path.join(OUT_DIR, "seam_report.json"), "w") as f:
    json.dump(report, f, indent=2)

print("\n===== OPTION 1: Seam Tokenization Prototype =====")
print(f"Seam edges: {report['n_seam_edges']}, chains: {report['n_chains']}")
print(f"Reconstruction missed: {report['reconstruction_missed_edges']}, extra: {report['reconstruction_extra_edges']}")
print("Saved:")
print(" -", os.path.join(OUT_DIR, "seam_tokens.json"))
print(" -", os.path.join(OUT_DIR, "seam_chains.txt"))
print(" -", os.path.join(OUT_DIR, "seam_overlay.png"))
print(" -", os.path.join(OUT_DIR, "seam_report.json"))
