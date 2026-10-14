"""
Explainable AI-Based Drug Discovery Assistant for Human EGFR (CHEMBL203) Virtual Screening.
Interactive Streamlit Application featuring 3-Part Presentation Milestones:
  Part 1: Molecular Profiling & Chemoinformatics (SMILES validation, 2D/3D conformers, Lipinski/Veber rules)
  Part 2: AI Virtual Screening & Benchmark (Random Forest & Gradient Boosting, ROC-AUC > 0.80)
  Part 3: Explainable AI & Full Platform (SHAP TreeExplainer, atom-level highlights, PDF reports)
"""

import os
import sys
import json
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import py3Dmol

# Ensure current directory is on path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from chem_engine import (
    validate_smiles,
    canonicalize_smiles,
    calculate_descriptors,
    evaluate_drug_likeness,
    draw_molecule_2d_svg,
    generate_3d_conformer_block
)
from ai_model import get_predictor
from explainability import SHAPExplainerEngine
from similarity_engine import get_similarity_engine
from report_generator import generate_screening_pdf
from chatbot import check_ollama_status, build_system_context, stream_ollama_chat

# Page configuration
st.set_page_config(
    page_title="EGFR Drug Discovery Assistant",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern biotech styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .milestone-banner {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    .active-badge {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.3rem;
        text-align: center;
        letter-spacing: 0.5px;
    }
    .inactive-badge {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.3rem;
        text-align: center;
        letter-spacing: 0.5px;
    }
    /* Hide Streamlit top-right menu, deploy button, status, and footer */
    #MainMenu {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    .stDeployButton {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0px 0px;
        padding: 10px 18px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Presets database
PRESET_MOLECULES = {
    "Gefitinib (Iressa) - 1st Gen EGFR Inhibitor": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1",
    "Erlotinib (Tarceva) - 1st Gen EGFR Inhibitor": "COCCOc1cc2c(Nc3cccc(c3)C#C)ncnc2cc1OCCOC",
    "Afatinib (Gilotrif) - 2nd Gen Covalent Inhibitor": "CN(C)C/C=C/C(=O)Nc1cc2c(Nc3ccc(Cl)c(F)c3)ncnc2cc1O[C@H]1CCOC1",
    "Osimertinib (Tagrisso) - 3rd Gen Mutant-Selective": "CN(C)CC=CC(=O)Nc1cc(Nc2ncc(c(n2)C(F)(F)F)Nc3ccccc3N(C)C)c(OC)cc1NC(=O)C=C",
    "Lapatinib (Tykerb) - Dual EGFR/HER2 Inhibitor": "CS(=O)(=O)CCNCc1ccc(o1)c2ccc3c(c2)c(ncn3)Nc4ccc(c(c4)Cl)OCc5cccc(c5)F",
    "Aspirin (Negative Control / Inactive)": "CC(=O)Oc1ccccc1C(=O)O",
    "Caffeine (Negative Control / Inactive)": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Custom SMILES": ""
}

def render_3dmol_viewer(mol_block: str, style_name: str = "stick", spin: bool = False, height: int = 400):
    """Renders 3D Py3Dmol interactive canvas inside Streamlit."""
    viewer = py3Dmol.view(width=None, height=height)
    viewer.addModel(mol_block, "mol")
    
    if style_name == "stick":
        viewer.setStyle({"stick": {"radius": 0.22, "colorscheme": "greenCarbon"}})
    elif style_name == "sphere":
        viewer.setStyle({"sphere": {"scale": 0.32}})
    elif style_name == "surface":
        viewer.setStyle({"stick": {}})
        viewer.addSurface(py3Dmol.VDW, {"opacity": 0.65, "color": "skyblue"})
    else:
        viewer.setStyle({"line": {}})
        
    viewer.zoomTo()
    if spin:
        viewer.spin(True)
        
    html_content = viewer._make_html()
    components.html(html_content, height=height + 20)

# Main App Layout
st.markdown("<div class='main-title'>🧬 Explainable AI-Based Drug Discovery Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Early Molecular Screening & Interpretability for <b>Human EGFR (CHEMBL203)</b> Virtual Screening</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔬 Screening Configuration")

# Silent stage detection: Part 1 vs Final System.
# Controlled via DEMO_PART environment variable or URL query param ?part=1 or ?part=final
raw_part = str(st.query_params.get("part", os.environ.get("DEMO_PART", "final"))).strip().lower()
if raw_part in ["1", "part1"]:
    demo_stage = "Part 1"
else:
    demo_stage = "Final"

selected_preset_key = st.sidebar.selectbox(
    "Select Molecule Preset:",
    list(PRESET_MOLECULES.keys()),
    index=0
)

preset_val = PRESET_MOLECULES[selected_preset_key]
if selected_preset_key == "Custom SMILES":
    input_smiles = st.sidebar.text_area(
        "Enter SMILES string:",
        value="COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1",
        height=100
    )
else:
    input_smiles = st.sidebar.text_area(
        "SMILES string:",
        value=preset_val,
        height=90
    )

# Only show classifier controls in Final Platform
if demo_stage == "Final":
    model_type = st.sidebar.selectbox(
        "Machine Learning Classifier:",
        ["Random Forest", "Gradient Boosting"],
        index=0
    )
    threshold = st.sidebar.slider(
        "Classification Threshold [P(Active)]:",
        min_value=0.10,
        max_value=0.90,
        value=0.50,
        step=0.05,
        help="Compounds with predicted probability >= threshold are classified as Active."
    )
else:
    model_type = "Random Forest"
    threshold = 0.50

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Target Information:**
- **Receptor:** Human EGFR (CHEMBL203)
- **Pathway:** ErbB Signaling / RTK
- **Disease Focus:** NSCLC, Glioblastoma, Colorectal
- **Benchmark Goal:** ROC-AUC > 0.80
""")

# Validate input
if not input_smiles.strip():
    st.info("👈 Enter a SMILES string or choose a preset molecule from the sidebar to begin.")
    st.stop()

valid_smiles, mol, can_smiles = validate_smiles(input_smiles)
if not valid_smiles or mol is None:
    st.error(f"❌ **Invalid SMILES String:** {can_smiles}")
    st.stop()

# Load Predictor
predictor = get_predictor()
pred_res = predictor.predict(can_smiles, model_type=model_type, threshold=threshold) if predictor.is_loaded else {}
descriptors = calculate_descriptors(mol)
drug_likeness = evaluate_drug_likeness(mol)
similarity_engine = get_similarity_engine()
sim_matches = similarity_engine.search_similar_drugs(mol, top_k=6)

# Modular Tab Renderers
def render_tab_overview():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("2D Chemical Architecture")
        svg_code = draw_molecule_2d_svg(mol, size=(480, 320))
        st.markdown(svg_code, unsafe_allow_html=True)
        st.caption(f"**Canonical SMILES:** `{can_smiles}`")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mol. Wt", f"{descriptors.get('MolWt', 0):.1f} Da")
        m2.metric("LogP", f"{descriptors.get('MolLogP', 0):.2f}")
        m3.metric("TPSA", f"{descriptors.get('TPSA', 0):.1f} Å²")
        m4.metric("QED", f"{descriptors.get('QED', 0):.2f}")
    with col2:
        st.subheader("Interactive 3D Conformer")
        style_choice = st.selectbox("3D Rendering Style:", ["stick", "sphere", "surface", "line"], index=0, key="style_select")
        spin_choice = st.checkbox("Auto-Spin Conformer", value=False, key="spin_select")
        success, mol_block, _ = generate_3d_conformer_block(mol)
        if success:
            render_3dmol_viewer(mol_block, style_name=style_choice, spin=spin_choice, height=360)
            st.caption("Energy-minimized 3D conformer generated via RDKit ETKDGv3 + MMFF94 force field.")
        else:
            st.warning(f"Could not generate 3D conformer: {mol_block}")

def render_tab_druglikeness():
    st.subheader("Oral Bioavailability & Drug-Likeness Profiling")
    dl_lip = drug_likeness.get("lipinski", {})
    dl_veb = drug_likeness.get("veber", {})
    desc = drug_likeness.get("descriptors", {})
    d_col1, d_col2 = st.columns([1.2, 1.8])
    with d_col1:
        st.markdown("#### Lipinski's Rule of Five")
        lip_status = dl_lip.get("status", "Pass")
        lip_viol = dl_lip.get("violations_count", 0)
        if lip_status == "Pass":
            st.success(f"**Lipinski Status: PASS** ({lip_viol} violations, max permitted 1)")
        else:
            st.error(f"**Lipinski Status: FAIL** ({lip_viol} violations)")
        lip_rules = dl_lip.get("rules", {})
        lip_df = pd.DataFrame([
            {"Criterion": k, "Value": v["value"], "Threshold": v["threshold"], "Pass": "✅" if v["pass"] else "❌"}
            for k, v in lip_rules.items()
        ])
        st.table(lip_df)
        st.markdown("#### Veber's Rule")
        veb_status = dl_veb.get("status", "Pass")
        veb_viol = dl_veb.get("violations_count", 0)
        if veb_status == "Pass":
            st.success(f"**Veber Status: PASS** ({veb_viol} violations)")
        else:
            st.error(f"**Veber Status: FAIL** ({veb_viol} violations)")
    with d_col2:
        st.markdown("#### Bioavailability Radar Profiling")
        categories = ["Molecular Weight", "LogP", "TPSA", "HBD", "HBA", "Rot. Bonds"]
        mw_norm = min(2.0, desc.get("MolWt", 0) / 500.0)
        logp_norm = max(0.0, min(2.0, (desc.get("MolLogP", 0) + 1.0) / 6.0))
        tpsa_norm = min(2.0, desc.get("TPSA", 0) / 140.0)
        hbd_norm = min(2.0, desc.get("NumHDonors", 0) / 5.0)
        hba_norm = min(2.0, desc.get("NumHAcceptors", 0) / 10.0)
        rb_norm = min(2.0, desc.get("NumRotatableBonds", 0) / 10.0)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            theta=categories + [categories[0]],
            fill="toself",
            name="Lipinski / Veber Limit",
            fillcolor="rgba(37, 99, 235, 0.12)",
            line=dict(color="#2563eb", dash="dash")
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[mw_norm, logp_norm, tpsa_norm, hbd_norm, hba_norm, rb_norm, mw_norm],
            theta=categories + [categories[0]],
            fill="toself",
            name="Query Molecule",
            fillcolor="rgba(16, 185, 129, 0.28)",
            line=dict(color="#10b981", width=2.5)
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1.5])),
            showlegend=True,
            height=380,
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

def render_tab_prediction():
    st.subheader(f"Virtual Screening Outcome ({model_type})")
    if not pred_res or not pred_res.get("success", False):
        st.warning("Please train the models to view predictions.")
    else:
        is_active = pred_res["is_active"]
        prob_active = pred_res["prob_active"]
        prob_inactive = pred_res["prob_inactive"]
        conf_tier = pred_res["confidence"]
        p_col1, p_col2 = st.columns([1.2, 1.8])
        with p_col1:
            st.markdown("<br>", unsafe_allow_html=True)
            if is_active:
                st.markdown(f"<div class='active-badge'>✅ ACTIVE (EGFR Inhibitor)<br><span style='font-size:0.9rem; font-weight:normal;'>{conf_tier}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='inactive-badge'>⛔ INACTIVE (Non-Inhibitor)<br><span style='font-size:0.9rem; font-weight:normal;'>{conf_tier}</span></div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Inhibition Probability P(Active)", f"{prob_active * 100:.1f}%")
            st.metric("Non-Inhibition Probability P(Inactive)", f"{prob_inactive * 100:.1f}%")
            st.caption(f"Decision Threshold: {threshold:.2f}")
        with p_col2:
            st.markdown("#### Probability Distribution")
            prob_df = pd.DataFrame({
                "Class": ["Active (EGFR Inhibitor)", "Inactive (Non-Inhibitor)"],
                "Probability": [prob_active, prob_inactive],
                "Color": ["#10b981", "#ef4444"]
            })
            fig_bar = px.bar(
                prob_df,
                x="Probability",
                y="Class",
                orientation="h",
                color="Class",
                color_discrete_map={"Active (EGFR Inhibitor)": "#10b981", "Inactive (Non-Inhibitor)": "#ef4444"},
                text=prob_df["Probability"].apply(lambda p: f"{p*100:.1f}%"),
                range_x=[0, 1.0]
            )
            fig_bar.update_layout(height=260, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("---")
        st.markdown("#### Molecular Screening Interpretation")
        if is_active:
            st.success(
                f"**High EGFR Binding Affinity Anticipated:** The molecule exhibits structural and electronic features consistent with established EGFR tyrosine kinase inhibitors ($IC_{{50}} \\le 1000\\text{{ nM}}$)."
            )
        else:
            st.info(
                f"**Low or Negligible EGFR Binding Predicted:** The molecular features, aromatic core, or hydrogen-bonding arrangement do not meet the affinity requirements for EGFR kinase inhibition at micromolar thresholds."
            )

def render_tab_benchmark():
    st.subheader("Model Validation & ChEMBL Bioactivity Benchmark")
    meta_path = os.path.join(CURRENT_DIR, "models", "model_meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            bench_meta = json.load(f)
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Target", bench_meta.get("target", "CHEMBL203"))
        m_col2.metric("Total Compounds", bench_meta.get("num_samples_total", 0))
        m_col3.metric("Actives in Dataset", bench_meta.get("class_distribution", {}).get("Active", 0))
        m_col4.metric("Inactives in Dataset", bench_meta.get("class_distribution", {}).get("Inactive", 0))
        st.markdown("---")
        st.markdown("#### Test Set Performance Metrics (Target ROC-AUC > 0.80)")
        metrics = bench_meta.get("metrics", {})
        metric_rows = []
        for m_name, m_vals in metrics.items():
            metric_rows.append({
                "Model": m_name,
                "Accuracy": f"{m_vals.get('accuracy', 0)*100:.2f}%",
                "Precision": f"{m_vals.get('precision', 0)*100:.2f}%",
                "Recall": f"{m_vals.get('recall', 0)*100:.2f}%",
                "F1-Score": f"{m_vals.get('f1_score', 0):.4f}",
                "ROC-AUC": f"{m_vals.get('roc_auc', 0):.4f}"
            })
        st.table(pd.DataFrame(metric_rows))
        fig_roc = go.Figure()
        fig_roc.add_shape(
            type="line", line=dict(dash="dash", color="#94a3b8"),
            x0=0, x1=1, y0=0, y1=1
        )
        for m_name, m_vals in metrics.items():
            rc = m_vals.get("roc_curve", {})
            fpr = rc.get("fpr", [])
            tpr = rc.get("tpr", [])
            auc = m_vals.get("roc_auc", 0.0)
            if fpr and tpr:
                fig_roc.add_trace(go.Scatter(
                    x=fpr, y=tpr, mode="lines",
                    name=f"{m_name} (AUC = {auc:.3f})"
                ))
        fig_roc.update_layout(
            title="Receiver Operating Characteristic (ROC) Curves",
            xaxis_title="False Positive Rate (1 - Specificity)",
            yaxis_title="True Positive Rate (Sensitivity)",
            height=400,
            margin=dict(l=30, r=30, t=40, b=30)
        )
        st.plotly_chart(fig_roc, use_container_width=True)
    else:
        st.warning("Model benchmark metadata not found. Train the models to view performance charts.")

def render_tab_target_overview():
    st.subheader("Human EGFR Target & ChEMBL Bioactivity Foundation")
    st.markdown("""
    ### Why Target Human EGFR (CHEMBL203)?
    The **Epidermal Growth Factor Receptor (EGFR)** is a transmembrane receptor tyrosine kinase (RTK) of the ErbB family. 
    Upon ligand binding, EGFR undergoes dimerization and transphosphorylation, triggering the downstream **MAPK/ERK** and **PI3K/AKT** oncogenic cascades.
    - **Clinical Relevance:** Overexpression or activating mutations (such as *Exon 19 deletions* and *L858R*) drive **Non-Small Cell Lung Cancer (NSCLC)** and Glioblastoma.
    - **Approved Therapeutics:** Gefitinib, Erlotinib, Afatinib, and Osimertinib were developed to target this specific binding pocket.
    
    ---
    ### Data Harvesting from ChEMBL
    Bioactivity data was queried directly from the **EMBL-EBI ChEMBL REST API** for target ID `CHEMBL203`:
    1. Filtered for standard measurement type **$IC_{50}$** in nanomolar (**$\text{nM}$**).
    2. Converted raw potency into logarithmic scale:
       $$pIC_{50} = 9 - \\log_{10}(IC_{50})$$
    3. Classified into standard binary screening labels:
       - **Active (1):** $IC_{50} \\le 1,000\\text{ nM}$ ($pIC_{50} \\ge 6.0$)
       - **Inactive (0):** $IC_{50} \\ge 10,000\\text{ nM}$ ($pIC_{50} \\le 5.0$)

    ---
    ### 🎓 Academic AI Curriculum Alignment (Units I - V)
    This project applies key concepts across the Artificial Intelligence syllabus:
    - **UNIT-I (Key Components of AI Systems):** Implementation of a domain-specific **Narrow AI** for automated problem solving in oncology. Evaluates the perception $\\to$ representation $\\to$ prediction loop and addresses ethical considerations in medical AI.
    - **UNIT-II (ML Applications, Tools & Frameworks):** Data wrangling via **Pandas** and **NumPy**; supervised ensemble learning using **Random Forest** and **Gradient Boosting** with rigorous train/test stratification.
    - **UNIT-III (Graph Theory, LLMs & Explainable AI - XAI):**
      - **Graph Theory:** Molecules represented as mathematical graphs $G=(V,E)$ where vertices are atoms and edges are covalent bonds, mapped via 2048-bit Morgan circular graph traversal (ECFP4).
      - **Large Language Models (LLMs):** Local **Ollama** chatbot providing conversational explanations for students and evaluators.
      - **Explainable AI (XAI):** Game-theoretic **SHAP (SHapley Additive exPlanations)** decomposing predictions down to individual functional groups and atoms.
    - **UNIT-IV (AI Applications in Healthcare):** Direct application in targeted lung cancer therapeutics (EGFR virtual screening), drastically cutting down wet-lab testing cycles and laboratory costs.
    - **UNIT-V (Real-World AI Case Studies):** Parallels milestone AI applications like **IBM Watson Health**, **DeepMind's AlphaFold**, and predictive disease biomarker systems.
    """)

def render_tab_shap():
    st.subheader("Explainable AI: SHAP Model Interpretability")
    st.markdown("""
    SHAP (SHapley Additive exPlanations) attributes the contribution of each molecular descriptor and Morgan fingerprint fragment to the final prediction.
    - <span style='color:#10b981; font-weight:bold;'>Green Regions (+SHAP):</span> Substructures that **enhance** binding to EGFR.
    - <span style='color:#ef4444; font-weight:bold;'>Red Regions (-SHAP):</span> Substructures that **penalize** or hinder EGFR inhibition.
    """, unsafe_allow_html=True)
    if not pred_res or not pred_res.get("success", False):
        st.warning("Please train models to enable SHAP interpretability.")
    else:
        selected_model = predictor.rf_model if model_type == "Random Forest" else predictor.gb_model
        with st.spinner("Computing SHAP values and atom-level substructure mappings..."):
            explainer_engine = SHAPExplainerEngine(selected_model)
            shap_res = explainer_engine.explain_instance(
                pred_res["features"],
                mol,
                bit_info=pred_res["bit_info"],
                top_k=8
            )
        col_x1, col_x2 = st.columns([1.1, 1.4])
        with col_x1:
            st.markdown("#### Atom-Level Feature Attribution")
            st.markdown(shap_res["highlighted_svg"], unsafe_allow_html=True)
            st.caption("Atoms highlighted in **Green** provide favorable binding interactions; **Red** highlights indicate unfavorable steric or electronic features.")
        with col_x2:
            st.markdown("#### Key Feature Impact (SHAP Values)")
            drivers = shap_res["top_drivers"]
            df_drivers = pd.DataFrame(drivers)
            if not df_drivers.empty:
                df_drivers["Color"] = df_drivers["shap_value"].apply(lambda v: "#10b981" if v > 0 else "#ef4444")
                fig_shap = px.bar(
                    df_drivers,
                    x="shap_value",
                    y="feature",
                    orientation="h",
                    color="shap_value",
                    color_continuous_scale=["#ef4444", "#f1f5f9", "#10b981"],
                    text=df_drivers["shap_value"].apply(lambda v: f"{v:+.4f}")
                )
                fig_shap.update_layout(
                    height=360,
                    margin=dict(l=20, r=20, t=10, b=20),
                    yaxis=dict(autorange="reversed"),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_shap, use_container_width=True)
        st.markdown("#### Physicochemical Descriptors SHAP Breakdown")
        df_desc = pd.DataFrame(shap_res["descriptor_contributions"])
        st.dataframe(
            df_desc[["feature", "feature_value", "shap_value", "effect"]].rename(
                columns={
                    "feature": "Descriptor",
                    "feature_value": "Calculated Value",
                    "shap_value": "SHAP Contribution",
                    "effect": "Model Influence"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

def render_tab_similarity():
    st.subheader("Tanimoto Structural Similarity against FDA-Approved EGFR Inhibitors")
    st.markdown("""
    Evaluates 2048-bit Morgan Fingerprint (ECFP4) Tanimoto similarity against clinically approved cancer therapeutics targeting the EGFR tyrosine kinase.
    """)
    if sim_matches:
        top_match = sim_matches[0]
        st.info(f"🏆 **Highest Match:** **{top_match['name']}** with **{top_match['similarity_pct']}%** structural similarity.")
        sim_df = pd.DataFrame(sim_matches)
        fig_sim = px.bar(
            sim_df,
            x="similarity_pct",
            y="name",
            orientation="h",
            color="similarity_pct",
            color_continuous_scale="Blues",
            text=sim_df["similarity_pct"].apply(lambda v: f"{v:.1f}%"),
            labels={"similarity_pct": "Tanimoto Similarity (%)", "name": "Approved Drug"}
        )
        fig_sim.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_sim, use_container_width=True)
        st.markdown("#### Detailed Clinical Intelligence")
        for match in sim_matches:
            with st.expander(f"{match['name']} — {match['similarity_pct']}% Similarity ({match['generation']})"):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.write(f"**FDA Approval Year:** {match['fda_approval_year']}")
                    st.write(f"**Target Mutations:** {match['target_mutations']}")
                    st.write(f"**Primary Indication:** {match['clinical_indication']}")
                with c2:
                    st.write(f"**Mechanism of Action:** {match['mechanism']}")
                    st.code(match['smiles'], language="text")

def render_tab_report():
    st.subheader("Generate Publication-Grade Virtual Screening Dossier")
    st.markdown("""
    Export a PDF report complete with:
    - 2D Molecular Architecture & Canonical SMILES
    - AI Virtual Screening Outcome & Calibrated Probability
    - Physicochemical Profiling & Lipinski / Veber Rules
    - Top Contributing SHAP Features
    - FDA-Approved Drug Similarity Benchmarks
    """)
    if not pred_res or not pred_res.get("success", False):
        st.warning("Please train models and validate a molecule to generate a report.")
    else:
        selected_model = predictor.rf_model if model_type == "Random Forest" else predictor.gb_model
        explainer_engine = SHAPExplainerEngine(selected_model)
        shap_res = explainer_engine.explain_instance(
            pred_res["features"],
            mol,
            bit_info=pred_res["bit_info"],
            top_k=8
        )
        pdf_bytes = generate_screening_pdf(
            smiles=can_smiles,
            prediction_result=pred_res,
            shap_result=shap_res,
            similarity_matches=sim_matches
        )
        st.success("✅ PDF Screening Report successfully compiled!")
        st.download_button(
            label="📥 Download PDF Screening Dossier",
            data=pdf_bytes,
            file_name=f"EGFR_Screening_Report_{descriptors.get('MolWt', 0):.0f}Da.pdf",
            mime="application/pdf"
        )

def render_tab_chatbot():
    st.subheader("💬 AI Chemoinformatics Tutor (Ollama)")
    st.markdown("Ask questions in simple everyday language to understand this molecule, its descriptors, the AI prediction, or prepare talking points for your teacher!")

    ollama_info = check_ollama_status()
    c_status1, c_status2 = st.columns([2, 1])
    with c_status1:
        if ollama_info["available"]:
            st.success(f"🟢 **Local Ollama LLM Online** — Model: `{ollama_info['selected_model']}` (Running locally on your device, private & offline)")
        else:
            st.info("💡 **Local Ollama Offline** — Active with built-in instant Chemoinformatics Explainer")
    with c_status2:
        if ollama_info["available"] and len(ollama_info["models"]) > 1:
            active_model = st.selectbox("Ollama Model:", ollama_info["models"], index=0, key="ollama_model_select")
        else:
            active_model = ollama_info["selected_model"]

    # Pre-computed SHAP for context if available
    shap_data_for_chat = None
    if predictor.is_loaded and pred_res.get("success"):
        try:
            sel_model = predictor.rf_model if model_type == "Random Forest" else predictor.gb_model
            exp_engine = SHAPExplainerEngine(sel_model)
            shap_data_for_chat = exp_engine.explain_instance(
                pred_res["features"],
                mol,
                bit_info=pred_res["bit_info"],
                top_k=5
            )
        except Exception:
            pass

    system_context = build_system_context(
        can_smiles,
        descriptors,
        drug_likeness,
        prediction_result=pred_res if predictor.is_loaded else None,
        shap_result=shap_data_for_chat,
        similarity_matches=sim_matches
    )

    # Quick Question Buttons
    st.markdown("##### 💡 Quick Questions:")
    q_col1, q_col2, q_col3 = st.columns(3)
    quick_query = None
    with q_col1:
        if st.button("🎓 Explain this for my teacher", use_container_width=True, key="btn_teacher"):
            quick_query = "How can I explain this molecule, its descriptors, and its prediction to my teacher in simple words?"
        if st.button("❓ Why did the AI predict this?", use_container_width=True, key="btn_why_pred"):
            quick_query = "Why did the machine learning model make this prediction for this molecule?"
    with q_col2:
        if st.button("💊 Explain Lipinski Rule of 5", use_container_width=True, key="btn_lipinski"):
            quick_query = "What is Lipinski's Rule of 5 and what do the violations mean for this drug?"
        if st.button("🟢 Explain Green vs Red SHAP", use_container_width=True, key="btn_shap"):
            quick_query = "Explain what the green and red atom highlights mean in simple terms."
    with q_col3:
        if st.button("🔍 Compare with Approved Drugs", use_container_width=True, key="btn_sim"):
            quick_query = "How does this compound compare to approved cancer drugs like Gefitinib?"
        if st.button("🧹 Clear Chat History", use_container_width=True, key="btn_clear"):
            st.session_state.chat_history = []
            st.rerun()

    # Session state for chat
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "👋 **Hello!** I am your local AI Chemoinformatics Tutor. I can explain this molecule, translate complex pharmacology into simple concepts, or help you practice answers for your teacher. Click any button above or type your question below!"
            }
        ]

    # Render past chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input or button trigger
    user_input = st.chat_input("Ask a question about this molecule or project in simple terms...")
    prompt_to_send = quick_query or user_input

    if prompt_to_send:
        st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        with st.chat_message("assistant"):
            response_generator = stream_ollama_chat(
                prompt=prompt_to_send,
                system_context=system_context,
                model_name=active_model,
                conversation_history=st.session_state.chat_history[:-1]
            )
            full_response = st.write_stream(response_generator)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# Render Tabs dynamically based on demo_stage (Part 1 vs Final System)
if demo_stage == "Part 1":
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧬 Molecular Overview & 3D",
        "💊 Drug-Likeness (Lipinski & Veber)",
        "🎯 Target & Syllabus (CHEMBL203)",
        "💬 AI Tutor (Ollama)"
    ])
    with tab1:
        render_tab_overview()
    with tab2:
        render_tab_druglikeness()
    with tab3:
        render_tab_target_overview()
    with tab4:
        render_tab_chatbot()

else:
    # Final Full Platform
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🧬 Molecular Overview & 3D",
        "🎯 AI Virtual Screening",
        "💡 Explainable AI (SHAP)",
        "💊 Drug-Likeness (Lipinski)",
        "🔍 Approved Drug Similarity",
        "📊 Model Benchmark",
        "💬 AI Tutor (Ollama)",
        "📄 PDF Screening Report"
    ])
    with tab1:
        render_tab_overview()
    with tab2:
        render_tab_prediction()
    with tab3:
        render_tab_shap()
    with tab4:
        render_tab_druglikeness()
    with tab5:
        render_tab_similarity()
    with tab6:
        render_tab_benchmark()
    with tab7:
        render_tab_chatbot()
    with tab8:
        render_tab_report()
