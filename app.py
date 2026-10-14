"""
Explainable AI-Based Drug Discovery Assistant for Human EGFR (CHEMBL203) Virtual Screening.
Interactive Streamlit Application featuring:
- SMILES validation & canonicalization
- 2D structure rendering & interactive 3D Py3Dmol conformers
- Random Forest & Gradient Boosting virtual screening predictions
- SHAP TreeExplainer with atom-level favorable/unfavorable substructure highlights
- Lipinski Rule of Five & Veber oral bioavailability radar charts
- Tanimoto similarity search against FDA-approved cancer therapeutics
- Automated ReportLab PDF report generation
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

# Page configuration
st.set_page_config(
    page_title="EGFR Drug Discovery Assistant",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern biotech theme
# Custom CSS for dark biotech theme
st.markdown("""
<style>
    /* Main background and font styling */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: #F8FAFC !important;
    }
    
    /* Metric Cards styling */
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
    }
    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
    }
    
    /* Prediction badges */
    .active-badge {
        background: linear-gradient(135deg, #047857, #0D9488);
        color: #FFFFFF;
        padding: 22px 18px;
        border-radius: 14px;
        font-weight: 750;
        font-size: 1.2rem;
        text-align: center;
        box-shadow: 0 6px 18px rgba(13, 148, 136, 0.25);
    }
    .inactive-badge {
        background: linear-gradient(135deg, #B91C1C, #E05252);
        color: #FFFFFF;
        padding: 22px 18px;
        border-radius: 14px;
        font-weight: 750;
        font-size: 1.2rem;
        text-align: center;
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.25);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 6px;
        padding: 8px 16px;
        color: #94A3B8 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0D9488 !important;
        color: #FFFFFF !important;
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


# Modern Header Banner
st.markdown("""
    <div style="padding: 1.5rem 0rem; border-bottom: 1px solid #E2E8F0; margin-bottom: 2rem;">
        <h1 style="color: #0F172A; font-weight: 800; font-size: 2.25rem; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 10px;">
            🧬 EGFR Drug Discovery <span style="color: #0D9488; font-size: 1.5rem; background: #F0FDFA; padding: 2px 10px; border-radius: 20px; border: 1px solid #CCFBF1;">AI</span>
        </h1>
        <p style="color: #64748B; font-size: 1.05rem; font-weight: 500; margin: 0;">
            Explainable molecular screening platform &nbsp;•&nbsp; Human EGFR / CHEMBL203 &nbsp;•&nbsp; Molecular analysis and virtual screening
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔬 Screening Configuration")

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
if not predictor.is_loaded:
    st.warning("⚠️ Machine learning models are not yet trained. Run `train_model.py` or trigger training from the Model Benchmark tab.")
    
# Compute Prediction
pred_res = predictor.predict(can_smiles, model_type=model_type, threshold=threshold) if predictor.is_loaded else {}
descriptors = calculate_descriptors(mol)
drug_likeness = evaluate_drug_likeness(mol)
similarity_engine = get_similarity_engine()
sim_matches = similarity_engine.search_similar_drugs(mol, top_k=6)

# Main Multi-Tab Interface
tab_overview, tab_pred, tab_shap, tab_druglikeness, tab_similarity, tab_benchmark, tab_report = st.tabs([
    "🧬 Molecular Overview & 3D",
    "🎯 AI Prediction",
    "💡 Explainable AI (SHAP)",
    "💊 Drug-Likeness (Lipinski)",
    "🔍 Approved Drug Similarity",
    "📊 Model Benchmark",
    "📄 PDF Screening Report"
])

# ----------------- TAB 1: MOLECULAR OVERVIEW -----------------
with tab_overview:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("2D Chemical Architecture")

        svg_code = draw_molecule_2d_svg(mol, size=(480, 320))

        if svg_code and "<svg" in svg_code:
            svg_display = svg_code[svg_code.find("<svg"):]
            components.html(
                svg_display,
                height=350,
                scrolling=False
            )
        else:
            st.error("Could not generate the 2D molecular structure.")

        st.caption(f"Canonical SMILES: {can_smiles}")

        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mol. Wt", f"{descriptors.get('MolWt', 0):.1f} Da")
        m2.metric("LogP", f"{descriptors.get('MolLogP', 0):.2f}")
        m3.metric("TPSA", f"{descriptors.get('TPSA', 0):.1f} Å²")
        m4.metric("QED", f"{descriptors.get('QED', 0):.2f}")

    with col2:
        st.subheader("Interactive 3D Conformer")

        style_choice = st.selectbox(
            "3D Rendering Style:",
            ["stick", "sphere", "surface", "line"],
            index=0
        )
        spin_choice = st.checkbox("Auto-Spin Conformer", value=False)

        success, mol_block, _ = generate_3d_conformer_block(mol)

        if success:
            render_3dmol_viewer(
                mol_block,
                style_name=style_choice,
                spin=spin_choice,
                height=360
            )
            st.caption(
                "Energy-minimized 3D conformer generated via "
                "RDKit ETKDGv3 + MMFF94 force field."
            )
        else:
            st.warning(f"Could not generate 3D conformer: {mol_block}")


# ----------------- TAB 2: AI PREDICTION -----------------
with tab_pred:
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
                f"**High EGFR Binding Affinity Anticipated:** The molecule exhibits structural and electronic features consistent with established EGFR tyrosine kinase inhibitors ($IC_{{50}} \\le 1000\\text{{ nM}}$). Proceed to explainability tab for fragment drivers."
            )
        else:
            st.info(
                f"**Low or Negligible EGFR Binding Predicted:** The molecular features, aromatic core, or hydrogen-bonding arrangement do not meet the affinity requirements for EGFR kinase inhibition at micromolar thresholds."
            )

# ----------------- TAB 3: EXPLAINABLE AI (SHAP) -----------------
with tab_shap:
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
            shap_svg = shap_res.get("highlighted_svg", "")

            if shap_svg and "<svg" in shap_svg:
                shap_svg_display = shap_svg[shap_svg.find("<svg"):]
                components.html(
                    shap_svg_display,
                    height=370,
                    scrolling=False
                )
            else:
                st.warning(
                    "The SHAP molecule structure could not be rendered. "
                    "Check the terminal for RDKit or SHAP errors."
                )

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

# ----------------- TAB 4: DRUG-LIKENESS & BIOAVAILABILITY -----------------
with tab_druglikeness:
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

# ----------------- TAB 5: APPROVED DRUG SIMILARITY -----------------
with tab_similarity:
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

# ----------------- TAB 6: MODEL BENCHMARK -----------------
with tab_benchmark:
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

# ----------------- TAB 7: PDF SCREENING REPORT -----------------
with tab_report:
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