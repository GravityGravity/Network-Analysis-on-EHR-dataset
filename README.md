<p align="center">
  <img src="Screenshots/Graph Banner.png" alt="Network Visualization Banner">
</p>

# 🧠 Network-Analysis-on-EHR-dataset

#### 👥 Authors
###### - **Author 1** — GravityGravity *(http://github.com/GravityGravity)*
###### - **Author 2** — Starman4xz *(http://github.com/Starman4xz)*

## 📘 Project Description

This project explores how medical procedures relate to subsequent drug exposures using a subset of the **EHRShot dataset** from the first six months of 2020.  
> **"If a medical procedure was performed in the first half of 2020, what was the likelihood of specific drug exposure?"**

This research was conducted as part of a broader effort to **learn about network graph structure generation** and to develop hands-on experience in data preprocessing, graph modeling, and metric computation using real-world healthcare data. 

Through this project, our team gained practical experience in building bipartite networks, applying Python libraries such as NetworkX for structural analysis, and interpreting how statistical and graphical properties can uncover meaningful patterns in complex clinical datasets.

## 📊 Visual Highlights
<p align="center">
  <img src="Screenshots/Filtered graph without P-0.png" alt="Filtered graph with labels">
</p>
<p align="center">
  <img src="Screenshots/Unfiltered Graph.png" alt="Unfiltered graph">
</p>

## 🧠 Key Findings

- Medication exposure patterns are **highly centralized**, with a small number of procedures driving the majority of prescriptions.  
- Network metrics reveal that **high-frequency procedures** form the structural core of healthcare activity.  
- These findings highlight how **procedural workflows** shape overall prescribing behavior within clinical systems.

## ⚙️ Tools and Libraries Used

- **Python 3.10+**
- **pandas** — data manipulation and filtering  
- **NetworkX** — graph creation and network metric computation  
- **matplotlib** — visualizations and scatter plots  
- **tqdm** — progress tracking for large file operations  
