# 🎓 AI & Data Science Syllabus Alignment & Academic Defense Guide
### Project Title: Explainable AI-Based Drug Discovery Assistant for Human EGFR (CHEMBL203) Virtual Screening

This document maps the project to each unit of the Artificial Intelligence syllabus. Use this during evaluations, lab presentations, and project vivas to prove academic alignment and earn top marks.

---

## 📑 Syllabus Mapping Matrix

| Unit | Syllabus Topics | Project Implementation & Evidence |
| :--- | :--- | :--- |
| **UNIT-I** | **Key Components of AI Systems**<br>• Narrow AI vs General AI vs Super AI<br>• AI for Problem Solving<br>• Ethical Considerations in AI<br>• How AI Systems Work | • **Narrow AI Application:** Domain-specific virtual screening system for EGFR inhibition.<br>• **Heuristic Problem Solving:** Transforming chemical search spaces into optimized binary classification.<br>• **Ethical Considerations:** Algorithmic transparency in healthcare, dataset bias mitigation, and human-in-the-loop laboratory validation before clinical trials.<br>• **AI Architecture Loop:** Perception (SMILES) $\to$ Graph Featurization $\to$ Inference $\to$ SHAP Explanation $\to$ Clinical Reporting. |
| **UNIT-II** | **ML/DL Applications & Frameworks**<br>• AI Tools & Frameworks<br>• Supervised Machine Learning<br>• Feature Engineering & Preprocessing<br>• Pandas, NumPy, Scikit-Learn | • **Tools Used:** Scikit-learn, Pandas, NumPy, Torch, RDKit, Plotly, ReportLab.<br>• **Algorithms:** Random Forest (bagging ensemble) and Gradient Boosting (boosting ensemble).<br>• **Rigorous Data Science:** Strict stratified train-test splitting before fitting any scalers to prevent data leakage.<br>• **Metrics:** Accuracy (91.0%), Precision, Recall, F1-Score, and ROC-AUC (0.978). |
| **UNIT-III** | **Graph Theory, LLMs & Explainable AI (XAI)**<br>• Graph Theory<br>• Large Language Models (LLMs)<br>• Generative AI & Conversational Agents<br>• Explainable AI (XAI) & AI Ethics | • **Graph Theory:** Molecules represented as mathematical graphs $G=(V, E)$ where vertices are atoms and edges are bonds. Topological circular traversal generates 2048-bit Morgan Fingerprints (ECFP4).<br>• **LLMs & Generative AI:** Integrated local **Ollama** chatbot (`gemma3:1b` / `phi4-mini`) serving as an interactive Chemoinformatics Tutor explaining findings in plain English.<br>• **Explainable AI (XAI):** Game-theoretic **SHAP TreeExplainer** decomposing black-box predictions into atom-level favorable (green) and unfavorable (red) heatmaps.<br>• **AI Ethics:** Transparency, auditability, and removing the black box in medical decision support. |
| **UNIT-IV** | **AI Applications in Healthcare**<br>• Healthcare Innovations<br>• Business & Laboratory Optimization<br>• Translational Medicine | • **Primary Application Domain:** Computational Oncology & Virtual High-Throughput Screening.<br>• **Impact:** Replaces expensive, slow laboratory brute-force screening, reducing drug discovery timelines (traditionally 10–15 years and millions of dollars) to seconds.<br>• **Target:** Human Epidermal Growth Factor Receptor (EGFR) implicated in Non-Small Cell Lung Cancer (NSCLC) and Glioblastoma. |
| **UNIT-V** | **Real-World AI Case Studies**<br>• IBM Watson Health<br>• AlphaFold / DeepMind Biotech AI<br>• Parkinson's Disease Prediction<br>• Historic AI Milestones | • **Industrial Parallels:** Directly builds on AI biotech milestones like **AlphaFold** (protein structure prediction) and **IBM Watson for Drug Discovery**.<br>• **Benchmarking:** Evaluates predictions against FDA-approved cancer therapeutics (Gefitinib, Erlotinib, Afatinib, Osimertinib). |

---

## 🎙️ Viva / Oral Defense: Unit-by-Unit Teacher Talking Points

### 🔹 UNIT-I: "What kind of AI system is this?"
> *"Our project is a **Narrow AI (Applied AI)** system designed for molecular virtual screening. Rather than relying on brute-force laboratory trials, it uses heuristic chemical representations to predict EGFR inhibition. From an ethical standpoint, healthcare AI cannot afford to be an untrusted black-box, which is why we incorporated explainability (SHAP) and clear disclaimers that computational findings must be verified via in vitro assays."*

### 🔹 UNIT-II: "Explain your Machine Learning pipeline and tools."
> *"We utilized **Pandas** and **NumPy** for bioactivity data ingestion from ChEMBL. We trained **Random Forest** and **Gradient Boosting** classifiers in **Scikit-learn**. To enforce strict ML best practices, we performed an 80/20 stratified split **before** fitting our standard scaler on descriptors, completely eliminating data leakage. Our Random Forest model achieves a test accuracy of **90.96%** and an ROC-AUC of **0.9778**, far exceeding the 0.80 benchmark."*

### 🔹 UNIT-III: "How does your project relate to Graph Theory and LLMs?"
> *"1. **Graph Theory:** Every chemical compound is fundamentally a molecular graph $G=(V,E)$ where atoms are vertices and chemical bonds are edges. We use Morgan circular graph traversal (ECFP4) to hash 2-bond atomic neighborhoods into a 2048-bit numerical vector.*
> *2. **Explainable AI (XAI):** We implemented **SHAP (SHapley Additive exPlanations)** based on cooperative game theory to attribute prediction weights back to individual graph nodes (atoms), rendering 🟢 green favorable binding anchors and 🔴 red steric clashing regions.*
> *3. **Generative AI & LLMs:** We connected local **Ollama** models (`gemma3:1b` / `phi4-mini`) to provide an interactive natural language tutor that translates complex pharmacological data into plain English for students and clinicians."*

### 🔹 UNIT-IV: "What is the healthcare and real-world significance?"
> *"Traditional drug discovery takes over 10 to 15 years and billions of dollars testing thousands of inactive molecules in wet labs. Our system performs early **virtual screening** for Human EGFR—the primary kinase target for non-small cell lung cancer—in seconds, allowing research teams to prioritize only the most viable, orally bioavailable drug candidates."*

### 🔹 UNIT-V: "How does this compare to real-world AI systems like IBM Watson or AlphaFold?"
> *"While **AlphaFold** predicts 3D protein structures and **IBM Watson** mined medical literature, our platform focuses on **ligand-target interaction screening and explainability**. It directly compares candidate compounds against clinical benchmark drugs like Gefitinib and Osimertinib using Tanimoto similarity metrics."*
