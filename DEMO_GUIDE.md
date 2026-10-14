# 🎯 Presentation & Demo Guide: Part 1 & Final System
### Explainable AI-Based Drug Discovery Assistant for Human EGFR (CHEMBL203)

This guide provides an exact, step-by-step roadmap to present your project in **2 clean milestones**:
- **Part 1 (Milestone 1):** Molecular Representation, Chemoinformatics & 3D Conformer Foundation
- **Final System (Complete Platform):** AI Virtual Screening, Explainable AI (SHAP), Ollama Chatbot & PDF Reports

---

## ⚡ Quick Launch: 1-Click Launchers

| Launcher File | What It Opens |
| :--- | :--- |
| **[`run_part1.bat`](run_part1.bat)** | **Part 1 Only:** Molecular profiling, 3D Py3Dmol viewer, Lipinski/Veber drug-likeness rules, target overview with AI syllabus alignment, and the Ollama AI tutor. *(No ML prediction tabs shown).* |
| **[`run_final_app.bat`](run_final_app.bat)** *(or `run_app.bat`)* | **Final Complete Platform:** All 8 tabs unlocked including Virtual Screening AI, SHAP atom highlights, approved drug similarity search, Ollama chatbot, and ReportLab PDF downloads. |

---

## 📍 MILESTONE 1: Molecular Profiling & Chemoinformatics Foundation
> **Focus:** *Data harvesting from ChEMBL, chemical graph representations, 3D conformer energetics, oral bioavailability rules, and the AI Chemoinformatics Tutor.*

### 🖥️ What to Show in the App:
1. Double-click [`run_part1.bat`](run_part1.bat).
2. Select **Gefitinib (Iressa)** from the preset dropdown.
3. Show **Tab 1 (🧬 Molecular Overview & 3D)**:
   - Point out the clean 2D chemical structure, canonical SMILES, and basic descriptors (MW, LogP, TPSA, QED).
   - Interact with the **3D Py3Dmol viewer**: rotate the molecule, switch between *stick* and *surface* modes, and turn on *Auto-Spin*.
4. Show **Tab 2 (💊 Drug-Likeness & Bioavailability)**:
   - Walk through the **Lipinski Rule of Five** scorecard: Molecular Weight $\le 500$, LogP $\le 5$, H-Bond Donors $\le 5$, H-Bond Acceptors $\le 10$ (Status: **PASS**, 0 violations).
   - Show the **Veber's Rule** scorecard (Rotatable Bonds $\le 10$, TPSA $\le 140$ Å²).
   - Explain the **Interactive Polar Radar Chart**: the blue dashed perimeter represents drug-like boundaries, and the green filled area shows the molecule fitting comfortably inside oral bioavailability space.
5. Show **Tab 3 (🎯 Target & Syllabus - CHEMBL203)**:
   - Explain the biology of Human EGFR in cancer (NSCLC) and how 881 bioactivity records ($IC_{50} \to pIC_{50}$) were harvested from ChEMBL.
   - Point to the **Academic AI Curriculum Alignment (Units I - V)** section mapping to your college syllabus.
6. Show **Tab 4 (💬 AI Tutor - Ollama)**:
   - Click the button: **`🎓 Explain this for my teacher`** to watch the local Ollama LLM stream an explanation of the molecule in simple English!

### 🎙️ Talking Points for Milestone 1:
> *"In Milestone 1, we establish our computational chemistry foundation. Before feeding chemicals into machine learning models, we must validate their structure, model their 3D geometry, and assess their oral drug-likeness. We extracted real bioactivity data from the ChEMBL database for Human EGFR (CHEMBL203), an oncogenic receptor tyrosine kinase responsible for non-small cell lung cancer. Using RDKit, we validate canonical SMILES, generate energy-minimized 3D conformers with MMFF94 force-fields, and evaluate Lipinski's Rule of Five and Veber's bioavailability rules. We have also embedded a local Ollama AI tutor to translate these findings into plain English."*

---

## 📍 FINAL SYSTEM: Full AI Virtual Screening & Explainability Platform
> **Focus:** *Molecular featurization (ECFP4 fingerprints + descriptors), Random Forest vs Gradient Boosting models, SHAP atom-level attribution, and automated PDF dossiers.*

### 🖥️ What to Show in the App:
1. Double-click [`run_final_app.bat`](run_final_app.bat) (or [`run_app.bat`](run_app.bat)).
2. In **Tab 2 (🎯 AI Virtual Screening)**:
   - Test **Gefitinib**: Shows a bright green **`✅ ACTIVE (EGFR Inhibitor)`** card with **99.8% probability**.
   - Switch preset to **Aspirin (Negative Control)**: Shows a red **`⛔ INACTIVE (Non-Inhibitor)`** card with only **7.7% probability**.
   - Switch between **Random Forest** and **Gradient Boosting** models in the sidebar to demonstrate consensus predictions.
3. In **Tab 3 (💡 Explainable AI - SHAP)**:
   - Show the **Atom-Level 2D Highlight diagram**:
     - 🟢 **Green Atoms:** Point to the quinazoline core and anilino group — explain that SHAP identified these as primary positive drivers that anchor into the ATP-binding pocket.
     - 🔴 **Red Atoms:** Explain how steric clashes or unfavorable substituents are flagged by SHAP in red.
   - Show the **Key Feature Impact bar chart** and **Physicochemical Descriptors Breakdown table**.
4. In **Tab 5 (🔍 Approved Drug Similarity)**:
   - Point out the **Tanimoto similarity ranking**: Gefitinib matches 100%, Erlotinib matches 60%+, etc.
   - Expand an approved drug card to show its generation, FDA approval year, mutation coverage, and mechanism of action.
5. In **Tab 6 (📊 Model Benchmark & ROC Curves)**:
   - Highlight the test set benchmark metrics table:
     - **Random Forest:** Accuracy: **90.96%**, Precision: **89.58%**, Recall: **93.48%**, F1: **0.9167**, **ROC-AUC: 0.9778**.
     - **Gradient Boosting:** Accuracy: **91.53%**, Precision: **91.49%**, Recall: **92.39%**, F1: **0.9206**, **ROC-AUC: 0.9675**.
   - Show the interactive **ROC curves**: both curves hug the top-left corner, far exceeding the project target of $\text{ROC-AUC} > 0.80$.
6. In **Tab 7 (💬 AI Tutor - Ollama)**:
   - Click **`❓ Why did the AI predict this?`** or **`🟢 Explain Green vs Red SHAP`** to demonstrate conversational AI interpretability.
7. In **Tab 8 (📄 PDF Screening Report)**:
   - Click **`📥 Download PDF Screening Dossier`** to generate and open the publication-grade PDF report.

### 🎙️ Talking Points for the Final System:
> *"In our Final System, we solve the critical 'black-box' dilemma in computational drug discovery. We featurized compounds into 2048-bit Morgan Fingerprints (ECFP4) and standardized descriptors. After strict train-test splitting to prevent data leakage, we trained Random Forest and Gradient Boosting models, achieving over 91% accuracy and an ROC-AUC of 0.978 on unseen test data. Using SHAP TreeExplainer, we trace predictions down to individual atoms and fragments on the 2D molecule. Furthermore, our similarity engine benchmarks candidate molecules against clinical therapeutics like Gefitinib and Osimertinib, and compiles a comprehensive PDF dossier with a single click."*

---

## 🎓 Syllabus Alignment Defense (Quick Reference)

- **UNIT-I (Key Components of AI Systems):** Narrow AI for oncology virtual screening; heuristic problem solving; algorithmic ethics and patient safety.
- **UNIT-II (ML Applications, Tools & Frameworks):** Data wrangling via Pandas/NumPy; Supervised Random Forest and Gradient Boosting classification.
- **UNIT-III (Graph Theory, LLMs & Explainable AI):** Chemical compounds represented as molecular graphs $G=(V, E)$; local Ollama LLMs for interactive tutoring; game-theoretic SHAP TreeExplainer for atom attribution.
- **UNIT-IV (AI Applications in Healthcare):** Direct application in computational oncology and targeted cancer drug discovery.
- **UNIT-V (Real-World AI Case Studies):** Mirrors industry breakthroughs like DeepMind's AlphaFold, IBM Watson Health, and AI-driven disease prediction.
