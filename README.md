# 🧬 Explainable AI-Based Drug Discovery Assistant for Early Molecular Screening
### Target: Human EGFR (*Epidermal Growth Factor Receptor* / ChEMBL ID: CHEMBL203) Virtual Screening

An end-to-end, interpretable AI system that predicts whether chemical compounds bind to and inhibit the **Human EGFR** kinase domain, explains predictions using **SHAP** with atom-level structural attribution, calculates **Lipinski & Veber drug-likeness**, benchmarks **Tanimoto similarity** against FDA-approved cancer therapeutics, provides a local **Ollama AI Chemoinformatics Tutor**, and generates publication-grade **PDF screening dossiers**.

---

## 🌟 Key Capabilities

1. **SMILES Processing & 2D/3D Molecular Visualization**:
   - SMILES validation, sanitization, and canonicalization via RDKit.
   - High-resolution 2D structural diagram generation.
   - Interactive 3D conformer generation using ETKDGv3 and MMFF94 force-field energy minimization rendered via Py3Dmol.

2. **Dual-Model Virtual Screening Ensemble**:
   - **Random Forest Classifier**: Test Accuracy: **91.0%**, F1-Score: **0.917**, ROC-AUC: **0.978**.
   - **Gradient Boosting Classifier**: Test Accuracy: **91.5%**, F1-Score: **0.921**, ROC-AUC: **0.968**.
   - Strict train-test separation before preprocessing with standardized descriptors and 2048-bit Morgan (ECFP4) fingerprints.

3. **Explainable AI (SHAP) with Atom-Level Highlighting**:
   - `TreeExplainer` decomposes predictions into individual feature contributions.
   - Traces top Morgan fingerprint bits back to molecular substructures.
   - Color-coded 2D atomic highlights:
     - 🟢 **Green**: Favorable pharmacophoric fragments enhancing EGFR binding.
     - 🔴 **Red**: Unfavorable steric or electronic features penalizing inhibition.

4. **Oral Drug-Likeness & Bioavailability Scorecard**:
   - **Lipinski's Rule of Five**: Molecular Weight ($\le 500$ Da), LogP ($\le 5$), HBD ($\le 5$), HBA ($\le 10$).
   - **Veber's Rule**: Rotatable Bonds ($\le 10$), TPSA ($\le 140$ Å²).
   - Interactive Plotly polar radar chart comparing query properties to oral drug-like boundaries.

5. **FDA-Approved Cancer Drug Similarity Search**:
   - Morgan fingerprint (ECFP4) Tanimoto similarity against clinical EGFR TKIs:
     - **Gefitinib (Iressa)** (1st Gen)
     - **Erlotinib (Tarceva)** (1st Gen)
     - **Afatinib (Gilotrif)** (2nd Gen Covalent)
     - **Osimertinib (Tagrisso)** (3rd Gen Mutant-Selective)
     - **Lapatinib (Tykerb)** (Dual EGFR/HER2)
     - **Dacomitinib (Vizimpro)** (2nd Gen Pan-HER)

6. **Local Ollama AI Chemoinformatics Tutor**:
   - Powered by local models (`gemma3:1b`, `phi4-mini`) for conversational explanations.
   - Translates complex pharmacology into simple analogies (locks and keys, coffee filters, oral pill absorption) for student and evaluator questions.

7. **Automated PDF Screening Dossier**:
   - Publication-grade PDF report compiled with ReportLab containing structure diagrams, predictions, confidence meters, drug-likeness scorecards, SHAP feature rankings, and clinical similarity tables.

---

## 📁 Project Architecture

```
DrugDiscoveryAI/
├── app.py                  # Streamlit Multi-Tab Web Application
├── chem_engine.py          # RDKit Chemoinformatics Engine (2D/3D, Descriptors, ECFP4)
├── fetch_data.py           # ChEMBL REST API Data Harvester & Bioactivity Preprocessor
├── train_model.py          # ML Training Pipeline (RF & GBDT, Metrics, ROC-AUC > 0.80)
├── ai_model.py             # Inference Wrapper & Calibrated Probability Engine
├── explainability.py       # SHAP TreeExplainer & Atom-Level Highlight Mapper
├── similarity_engine.py    # Approved EGFR Drug Tanimoto Similarity Engine
├── chatbot.py              # Local Ollama AI Chemoinformatics Tutor & Explainer
├── report_generator.py     # Publication-Grade ReportLab PDF Generator
├── data/
│   └── egfr_chembl203_bioactivity.csv   # Curated & Processed EGFR ChEMBL Dataset
├── models/
│   ├── rf_model.pkl        # Serialized Random Forest Classifier
│   ├── gb_model.pkl        # Serialized Gradient Boosting Classifier
│   ├── scaler.pkl          # Standardized Descriptor Scaler
│   ├── background_samples.pkl # Baseline Data for SHAP Explainer
│   └── model_meta.json     # Benchmark Metrics & Evaluation Curves
└── requirements.txt        # Python Dependencies
```

---

## 🚀 How to Run the Application

| Launcher | Description |
| :--- | :--- |
| **[`run_part1.bat`](run_part1.bat)** | **Part 1 (Milestone 1):** Molecular profiling, 3D conformers, Lipinski/Veber rules, EGFR target overview, and the Ollama AI tutor. |
| **[`run_final_app.bat`](run_final_app.bat)** *(or `run_app.bat`)* | **Final Complete Platform:** All features unlocked including ML virtual screening, SHAP explainability, drug similarity search, Ollama chatbot, and PDF dossier generation. |

---

## 🎓 Academic AI Syllabus Alignment (Units I - V)

This project directly aligns with college Artificial Intelligence and Applications curricula. See the complete viva guide in **[`SYLLABUS_ALIGNMENT.md`](SYLLABUS_ALIGNMENT.md)**.

- **UNIT-I (Key Components of AI Systems):** Domain-specific **Narrow AI** for automated problem solving in oncology; heuristic search spaces; algorithmic ethics.
- **UNIT-II (ML Applications, Tools & Frameworks):** Data wrangling via **Pandas** and **NumPy**; supervised ensemble learning using **Random Forest** and **Gradient Boosting**.
- **UNIT-III (Graph Theory, LLMs & Explainable AI):** Chemical compounds represented as **molecular graphs** $G=(V, E)$; local **Ollama** LLMs for conversational tutoring; game-theoretic **SHAP (XAI)** for atom attribution.
- **UNIT-IV (AI Applications in Healthcare):** Direct application in computational oncology and early virtual high-throughput screening for lung cancer therapeutics.
- **UNIT-V (Real-World AI Case Studies):** Parallels industry milestones like **IBM Watson Health**, **DeepMind's AlphaFold**, and predictive disease biomarker systems.

---

## 📈 Model Performance Benchmark

| Model | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **90.96%** | **89.58%** | **93.48%** | **0.9167** | **0.9778** |
| **Gradient Boosting** | **91.53%** | **91.49%** | **92.39%** | **0.9206** | **0.9675** |

*Both models exceed the project requirement target of $\text{ROC-AUC} > 0.80$ with exceptional margin.*
