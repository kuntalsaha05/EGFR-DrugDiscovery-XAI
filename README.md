# 🧬 Explainable AI-Based Drug Discovery Assistant for Early Molecular Screening
### Target: Human EGFR (*Epidermal Growth Factor Receptor* / ChEMBL ID: CHEMBL203) Virtual Screening

An end-to-end, interpretable AI system that predicts whether chemical compounds bind to and inhibit the **Human EGFR** kinase domain, explains predictions using **SHAP** with atom-level structural attribution, calculates **Lipinski & Veber drug-likeness**, benchmarks **Tanimoto similarity** against FDA-approved cancer therapeutics, and generates publication-grade **PDF screening dossiers**.

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

6. **Automated PDF Screening Dossier**:
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

### Option A: Double-Click Launcher (Windows)
Double-click [`run_app.bat`](file:///c:/Users/sahak/Documents/AIDS/DVP/Project/run_app.bat) to activate the virtual environment and start the Streamlit server automatically.

### Option B: Terminal Command
```powershell
# 1. Activate virtual environment
.\.venv\Scripts\activate

# 2. Run Streamlit web app
streamlit run DrugDiscoveryAI\app.py
```

The web application will open in your browser at `http://localhost:8501`.

---

## 🧪 Dataset Information

- **Target:** Human Epidermal Growth Factor Receptor (**CHEMBL203**).
- **Assay Type:** Biochemical $IC_{50}$ binding assays measured in nanomolar ($\text{nM}$).
- **Transformation:**
  $$pIC_{50} = -\log_{10}(IC_{50} \times 10^{-9}) = 9 - \log_{10}(IC_{50})$$
- **Classification Thresholds:**
  - **Active ($1$):** $IC_{50} \le 1,000\text{ nM}$ ($pIC_{50} \ge 6.0$)
  - **Inactive ($0$):** $IC_{50} \ge 10,000\text{ nM}$ ($pIC_{50} \le 5.0$)
- **Data Size:** 881 curated compounds (480 Actives, 401 Inactives).

---

## 📈 Model Performance Benchmark

| Model | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **90.96%** | **89.58%** | **93.48%** | **0.9167** | **0.9778** |
| **Gradient Boosting** | **91.53%** | **91.49%** | **92.39%** | **0.9206** | **0.9675** |

*Both models exceed the project requirement target of $\text{ROC-AUC} > 0.80$ with exceptional margin.*
