Title: Mesh Normalization, Quantization, and Error Analysis
Author: Pinisetti Govardhan (Govii)

1. Context & Goal
We prepare 3D meshes for AI by normalizing to consistent ranges and quantizing to discrete bins. We compare Min–Max vs Unit-Sphere normalization, quantize at 1024 bins, then reconstruct and measure error.

2. Data & Tools
Meshes: OBJ (sample: unit cube)
Libraries: NumPy, Trimesh, Matplotlib
Scripts: step1_inspect.py, step2_normalize_quantize.py, step3_reconstruct_error.py

3. Methods
- Min–Max: x'=(x−xmin)/(xmax−xmin); quantize q=⌊x'·1023⌋; dequantize x̂'=q/1023; denormalize inverse.
- Unit-Sphere: center by mean; scale by max radius to fit inside radius 1; map to [0,1] before quantization, inverse on reconstruction.
- Metric: Mean Squared Error (MSE); plus axis-wise error plots.

4. Results
Task 1: Stats saved to outputs/step1_vertex_stats.csv.
Task 2: Normalized .obj and quantized .npy saved.
Task 3: Reconstruction and errors:
- MSE (Min–Max): 0.0000000000
- MSE (Unit-Sphere): 0.0000010005
Plots saved as: outputs/error_minmax.png, outputs/error_unitsphere.png.

5. Analysis
Min–Max matches the [0,1] quantizer range, giving zero error on the cube. Unit-Sphere adds an extra scaling step, causing tiny rounding error (~1e-6). In general: higher bins → less error; aligning normalization range to the quantizer reduces loss; extra rescaling increases rounding sensitivity.

6. Conclusion
Least error on this mesh: Min–Max + 1024 bins. Unit-Sphere is still excellent and useful for scale invariance. Next steps: test diverse meshes and explore adaptive quantization.

7. References
Assignment brief; Trimesh documentation; standard normalization/quantization formulas.
