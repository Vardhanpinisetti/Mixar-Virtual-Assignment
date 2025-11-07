### Mixar / Virtual Assignment ###
### Title: Mesh Normalization, Quantization, and Error Analysis ### 


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




Assignment Tasks (Total: 100 Marks) 
Task 1: Load and Inspect the Mesh (20 Marks) 
Goal: Understand and visualize 3D mesh data. 
Steps: 
1. Load .obj meshes using libraries such as trimesh or open3d. 
2. Extract vertex coordinates (x, y, z) as a NumPy array. 
3. Print basic statistics: 
- Number of vertices 
- Minimum, maximum, mean, and standard deviation per axis 
4. Visualize the original mesh (optional). 
Expected Output: 
Printed statistics and optionally a screenshot or rendered view of the mesh. 

Output Image: 


<img width="1920" height="991" alt="outputsoriginal_mesh_view" src="https://github.com/user-attachments/assets/b0bb9614-91ec-4a9f-9724-f02068b23a32" />












Task 2: Normalize and Quantize the Mesh (40 Marks) 
Goal: Convert the mesh into a standard numerical form. 
Steps: 
1. Implement two normalization methods of your choice (for example, Min–Max and 
Unit Sphere). 
2. For each method: 
- Normalize all vertex coordinates. 
- Quantize with a bin size of 1024. 
3. Save the quantized mesh as .ply or .obj. 
4. Visualize both the normalized and quantized meshes. 
Deliverables: 
● Two normalized meshes 
● Two quantized meshes 
● Short written comparison: which normalization method preserves the mesh structure 
better? 

Output Images: 


<img width="1920" height="991" alt="outputsminmax_view" src="https://github.com/user-attachments/assets/a79712dc-c21f-4eaa-bcbd-2080ae8fca8c" />





<img width="1920" height="991" alt="outputsunitsphere_view" src="https://github.com/user-attachments/assets/79b40225-f4a1-4a7b-bbbe-42d13170279b" />










Task 3: Dequantize, Denormalize, and Measure Error (40 Marks) 
Goal: Check how much information is lost after processing. 
Steps: 
1. For each normalization and quantization combination:
- Dequantize to recover normalized coordinates. 
- Denormalize to recover the original scale. 
2. Compute Mean Squared Error (MSE) or Mean Absolute Error (MAE) between: 
- Original mesh vertices 
- Reconstructed vertices 
3. Visualize reconstructed meshes. 
4. Plot reconstruction error per axis (x, y, z) using Matplotlib. 
5. Write a short conclusion (5–10 lines): 
- Which normalization and quantization combination gives the least error? 
- What pattern do you observe? 
Deliverables: 
● Plots of error metrics 
● Screenshots of reconstructed meshes 
● Written analysis

Output Images: 


<img width="640" height="480" alt="error_minmax" src="https://github.com/user-attachments/assets/3a698f2a-b2fe-4937-bc34-923f7e76a715" />




<img width="640" height="480" alt="error_unitsphere" src="https://github.com/user-attachments/assets/a671f532-5e7d-4083-8108-ef46fd9cb959" />










