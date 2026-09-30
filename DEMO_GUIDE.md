# 🎯 Presentation & Demo Guide: 3-Part Walkthrough
### Explainable AI-Based Drug Discovery Assistant for Human EGFR (CHEMBL203)

This guide provides an exact, step-by-step roadmap to present your project in **3 distinct parts/milestones** during tomorrow's demo.

---

## ⚡ Quick Start: How to Present Tomorrow

1. **Launch the Web App:**
   - Double-click [`run_app.bat`](run_app.bat) or run in terminal:
     ```powershell
     .\.venv\Scripts\activate
     streamlit run DrugDiscoveryAI\app.py
     ```
2. **Switching Between Parts:**
   - In the sidebar, look for **`🎯 Presentation Stage`**:
     - Select **Part 1** to show only the Chemoinformatics & Data foundation.
     - Select **Part 2** to unlock the AI Virtual Screening & Benchmark curves.
     - Select **Part 3** to unveil Explainable AI (SHAP), Approved Drug Similarity, and PDF Export.

---

## 📍 PART 1: Molecular Profiling & Chemoinformatics Foundation
> **Focus:** *Data acquisition from ChEMBL, chemical structure representation, 3D conformer energetics, and oral bioavailability rules.*

### 🖥️ What to Show in the App:
1. Set **Presentation Stage** to **`Part 1: Molecular Profiling & Chemoinformatics`**.
2. Select **Gefitinib (Iressa)** from the preset dropdown.
3. Show **Tab 1 (🧬 Molecular Overview & 3D)**:
   - Point out the clean 2D chemical structure, canonical SMILES, and basic descriptors (MW, LogP, TPSA, QED).
   - Interact with the **3D Py3Dmol viewer**: rotate the molecule, toggle from *stick* to *surface* mode, and turn on *Auto-Spin*.
4. Show **Tab 2 (💊 Drug-Likeness & Bioavailability)**:
   - Walk through the **Lipinski Rule of Five** scorecard: Molecular Weight $\le 500$, LogP $\le 5$, H-Bond Donors $\le 5$, H-Bond Acceptors $\le 10$ (Status: **PASS**, 0 violations).
   - Show the **Veber's Rule** scorecard (Rotatable Bonds $\le 10$, TPSA $\le 140$ Å²).
   - Explain the **Interactive Polar Radar Chart**: the blue dashed perimeter represents drug-like boundaries, and the green filled area shows the molecule fitting comfortably inside oral bioavailability space.
5. Show **Tab 3 (🎯 Target & Dataset - CHEMBL203)**:
   - Explain the biology of Human EGFR in cancer (NSCLC) and how 881 bioactivity records ($IC_{50} \to pIC_{50}$) were harvested from the ChEMBL API.

### 🎙️ Talking Points for Part 1:
> *"In Part 1, we establish the computational chemistry foundation. Before passing a chemical to AI, we must validate its structure, model its 3D geometry, and assess its oral drug-likeness. We extracted real bioactivity data from the ChEMBL database for Human EGFR (CHEMBL203), an oncogenic receptor tyrosine kinase responsible for non-small cell lung cancer. Using RDKit, we validate canonical SMILES, generate energy-minimized 3D conformers with MMFF94 force-fields, and evaluate Lipinski's Rule of Five and Veber's bioavailability rules."*

---

## 📍 PART 2: Machine Learning Virtual Screening Pipeline
> **Focus:** *Molecular featurization (ECFP4 fingerprints + descriptors), model training, classification accuracy, and ROC-AUC benchmark.*

### 🖥️ What to Show in the App:
1. Switch **Presentation Stage** to **`Part 2: AI Virtual Screening & Benchmark`**.
   *(Notice how the AI prediction tab and Model Benchmark tab appear smoothly!)*
2. In **Tab 2 (🎯 AI Virtual Screening)**:
   - Test **Gefitinib**: Shows a bright green **`✅ ACTIVE (EGFR Inhibitor)`** card with **99.8% probability**.
   - Switch preset to **Aspirin (Negative Control)**: Shows a red **`⛔ INACTIVE (Non-Inhibitor)`** card with only **7.7% probability**.
   - Switch between **Random Forest** and **Gradient Boosting** models in the sidebar to show consensus predictions.
3. In **Tab 4 (📊 Model Benchmark & ROC Curves)**:
   - Highlight the test set benchmark metrics table:
     - **Random Forest:** Accuracy: **90.96%**, Precision: **89.58%**, Recall: **93.48%**, F1: **0.9167**, **ROC-AUC: 0.9778**.
     - **Gradient Boosting:** Accuracy: **91.53%**, Precision: **91.49%**, Recall: **92.39%**, F1: **0.9206**, **ROC-AUC: 0.9675**.
   - Show the interactive **ROC curves**: both curves hug the top-left corner, far exceeding the project target of $\text{ROC-AUC} > 0.80$.

### 🎙️ Talking Points for Part 2:
> *"In Part 2, we formulated the virtual screening AI. Molecules are featurized into 2048-bit Morgan Fingerprints (ECFP4) capturing atomic neighborhoods up to radius 2, combined with 10 standardized physicochemical descriptors. To prevent data leakage, we strictly split our ChEMBL dataset into stratified train and test sets before fitting any scalers. We trained and compared both Random Forest and Gradient Boosting classifiers. On unseen test data, our Random Forest achieves an outstanding ROC-AUC of 0.978 and 91.0% accuracy, far surpassing our target benchmark of 0.80."*

---

## 📍 PART 3: Explainable AI (SHAP) & Clinical Decision Support
> **Focus:** *Model interpretability, atom-level fragment attribution, similarity to approved drugs, and automated reporting.*

### 🖥️ What to Show in the App:
1. Switch **Presentation Stage** to **`Part 3: Explainable AI & Full Platform`**.
   *(The full 7-tab platform is now unlocked!)*
2. Select **Gefitinib** and open **Tab 3 (💡 Explainable AI - SHAP)**:
   - Show the **Atom-Level 2D Highlight diagram**:
     - 🟢 **Green Atoms:** Point to the quinazoline core and anilino group — explain that SHAP identified these as primary positive drivers that anchor into the ATP-binding pocket.
     - 🔴 **Red Atoms:** Explain how steric clashes or unfavorable substituents are flagged by SHAP in red.
   - Show the **Key Feature Impact bar chart** and **Physicochemical Descriptors Breakdown table** (how LogP, MW, and specific ECFP4 bits pushed the score).
3. Open **Tab 5 (🔍 Approved Drug Similarity)**:
   - Point out the **Tanimoto similarity ranking**: Gefitinib matches 100%, Erlotinib matches 60%+, etc.
   - Expand an approved drug card to show its generation, FDA approval year, mutation coverage (L858R, T790M), and mechanism of action.
4. Open **Tab 7 (📄 PDF Screening Report)**:
   - Click the **`📥 Download PDF Screening Dossier`** button.
   - Open the generated PDF to show the professional summary: embedded molecular diagram, prediction badge, Lipinski table, top SHAP features, and similarity benchmarks ready for clinical review.

### 🎙️ Talking Points for Part 3:
> *"In Part 3, we solve the critical 'black-box' dilemma in computational drug discovery. Medicinal chemists cannot trust an AI prediction without knowing why. Using SHAP TreeExplainer, we compute Shapley values for every molecular feature and map them back to the 2D chemical structure. Favorable binding fragments are highlighted in green, while unfavorable steric penalties are in red. Furthermore, our similarity engine benchmarks candidate molecules against clinical therapeutics like Gefitinib and Osimertinib, and compiles a comprehensive PDF dossier with a single click."*

---

## 💡 Anticipated Questions & How to Answer

| Question | Recommended Answer |
| :--- | :--- |
| **Q1: Why did you choose Human EGFR (CHEMBL203)?** | *"EGFR is one of the most clinically validated cancer targets in modern oncology, with multiple generations of FDA-approved TKIs (Gefitinib, Erlotinib, Osimertinib). This provides rich, high-quality ChEMBL bioactivity data for rigorous benchmarking."* |
| **Q2: What is the difference between $IC_{50}$ and $pIC_{50}$?** | *"$IC_{50}$ is the concentration required for 50% inhibition in nanomolar ($nM$). Because $IC_{50}$ spans multiple orders of magnitude, we convert it to $pIC_{50} = 9 - \log_{10}(IC_{50})$. Lower $IC_{50}$ means stronger potency, which translates to a higher $pIC_{50}$ value."* |
| **Q3: What are Morgan fingerprints (ECFP4)?** | *"Extended-Connectivity Fingerprints (ECFP4) represent circular atom environments within a 2-bond radius hashed into a 2048-bit binary vector. They capture functional groups and topological pharmacophores essential for machine learning."* |
| **Q4: How did you prevent data leakage during training?** | *"We strictly performed stratified train-test splits on the raw molecules BEFORE fitting any scalers. The descriptor scaler was fit solely on the training partition and only applied as a transform on the test partition."* |
| **Q5: How does SHAP map to individual atoms?** | *"During fingerprint generation, RDKit tracks which atoms and bond radii activated each Morgan bit. By matching active bits to their respective SHAP values, we aggregate feature contributions across the central and neighboring atoms to render intuitive green and red gradients."* |
