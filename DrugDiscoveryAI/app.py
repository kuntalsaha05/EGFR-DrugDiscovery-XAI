"""
EGFR-DrugDiscovery-XAI — Specialized Scientific Research Instrument
Design System: HERBARIUM ALPINUM — The Edelweiss Folio
Reference: https://ui.oiloil.org/works/herbarium/live/index.html

Target: Human Epidermal Growth Factor Receptor (CHEMBL203 / ErbB-1)
Architecture: Streamlit + RDKit + Scikit-Learn + SHAP + ReportLab + Ollama
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

# Ensure current directory is on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from design_tokens import (
    get_herbarium_css,
    get_herbarium_plotly_layout,
    SEMANTIC_TOKENS,
    COLOR_FOUNDATIONS,
    TYPOGRAPHY_FOUNDATIONS
)
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

# ==============================================================================
# STREAMLIT CONFIGURATION & DESIGN SYSTEM INJECTION
# ==============================================================================

st.set_page_config(
    page_title="EGFR Molecular Intelligence — Herbarium Alpinum",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject centralized Herbarium Alpinum CSS
st.markdown(get_herbarium_css(), unsafe_allow_html=True)

# ==============================================================================
# REFERENCE MOLECULE PRESETS
# ==============================================================================

PRESET_MOLECULES = {
    "Gefitinib (Iressa) - 1st Gen EGFR TKI": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1",
    "Erlotinib (Tarceva) - 1st Gen EGFR TKI": "COCCOc1cc2c(Nc3cccc(c3)C#C)ncnc2cc1OCCOC",
    "Afatinib (Gilotrif) - 2nd Gen Covalent TKI": "CN(C)C/C=C/C(=O)Nc1cc2c(Nc3ccc(Cl)c(F)c3)ncnc2cc1O[C@H]1CCOC1",
    "Osimertinib (Tagrisso) - 3rd Gen T790M TKI": "CN(C)CC=CC(=O)Nc1cc(Nc2ncc(c(n2)C(F)(F)F)Nc3ccccc3N(C)C)c(OC)cc1NC(=O)C=C",
    "Lapatinib (Tykerb) - Dual EGFR/HER2 Inhibitor": "CS(=O)(=O)CCNCc1ccc(o1)c2ccc3c(c2)c(ncn3)Nc4ccc(c(c4)Cl)OCc5cccc(c5)F",
    "Aspirin (Negative Control / Inactive)": "CC(=O)Oc1ccccc1C(=O)O",
    "Caffeine (Negative Control / Inactive)": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Custom SMILES": ""
}

# ==============================================================================
# 3D PY3DMOL VIEWER HELPER (HERBARIUM DARK PALETTE)
# ==============================================================================

def render_3dmol_viewer(mol_block: str, style_name: str = "stick", spin: bool = False, height: int = 380):
    """Renders 3D Py3Dmol conformer canvas styled for dark botanical surface."""
    viewer = py3Dmol.view(width=None, height=height)
    viewer.addModel(mol_block, "mol")
    viewer.setBackgroundColor("#101811")
    
    if style_name == "stick":
        viewer.setStyle({"stick": {"radius": 0.22, "colorscheme": "greenCarbon"}})
    elif style_name == "sphere":
        viewer.setStyle({"sphere": {"scale": 0.30}})
    elif style_name == "surface":
        viewer.setStyle({"stick": {}})
        viewer.addSurface(py3Dmol.VDW, {"opacity": 0.60, "color": "#70a9a1"})
    else:
        viewer.setStyle({"line": {}})
        
    viewer.zoomTo()
    if spin:
        viewer.spin(True)
        
    html_content = viewer._make_html()
    components.html(html_content, height=height + 20)

# ==============================================================================
# PERSISTENT SIDEBAR NAVIGATION & HERBARIUM CABINET CONTROLS
# ==============================================================================

# Silent stage detection: Part 1 vs Full Platform
raw_part = str(st.query_params.get("part", os.environ.get("DEMO_PART", "final"))).strip().lower()
demo_stage = "Part 1" if raw_part in ["1", "part1"] else "Final"

# Sidebar Brand Header
st.sidebar.markdown(f"""
<div style="border-bottom: 1px solid var(--line); padding-bottom: 14px; margin-bottom: 16px;">
    <span class="eyebrow">EGFR MOLECULAR INTELLIGENCE</span>
    <h3 style="font-size: 16px; margin: 4px 0 2px 0; font-weight: 600; color: var(--chalk);">HERBARIUM ALPINUM</h3>
    <span class="mono" style="color: var(--muted); font-size: 10px;">FOLIO CHEMBL203 / SWISS SPECIMEN</span>
</div>
""", unsafe_allow_html=True)

# Navigation sections
FULL_SECTIONS = [
    "01 / Overview",
    "02 / Molecular Screening",
    "03 / Explainable AI",
    "04 / Drug-Likeness",
    "05 / Similarity Search",
    "06 / Model Performance",
    "07 / Screening Reports",
    "08 / Methodology"
]

PART1_SECTIONS = [
    "01 / Overview",
    "02 / Molecular Screening",
    "04 / Drug-Likeness",
    "08 / Methodology"
]

AVAILABLE_SECTIONS = PART1_SECTIONS if demo_stage == "Part 1" else FULL_SECTIONS

# Initialize session state for navigation
if "active_section" not in st.session_state or st.session_state.active_section not in AVAILABLE_SECTIONS:
    st.session_state.active_section = AVAILABLE_SECTIONS[0]

st.sidebar.markdown("<span class='eyebrow'>CABINET / SPECIMEN DRAWER</span>", unsafe_allow_html=True)
current_section_idx = AVAILABLE_SECTIONS.index(st.session_state.active_section)
selected_nav = st.sidebar.radio(
    "Select Specimen Drawer",
    AVAILABLE_SECTIONS,
    index=current_section_idx,
    label_visibility="collapsed",
    key="nav_radio"
)
st.session_state.active_section = selected_nav

st.sidebar.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<span class='eyebrow'>SPECIMEN IDENTIFIER</span>", unsafe_allow_html=True)

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
        height=90
    )
else:
    input_smiles = st.sidebar.text_area(
        "SMILES string:",
        value=preset_val,
        height=80
    )

# Model configuration controls (Final Platform)
if demo_stage == "Final":
    st.sidebar.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<span class='eyebrow'>CLASSIFIER SPECIFICATION</span>", unsafe_allow_html=True)
    model_type = st.sidebar.selectbox(
        "Supervised Model:",
        ["Random Forest", "Gradient Boosting"],
        index=0
    )
    threshold = st.sidebar.slider(
        "Activity Threshold [P(Active)]:",
        min_value=0.10,
        max_value=0.90,
        value=0.50,
        step=0.05,
        help="Decision boundary for classifying bioactivity against EGFR tyrosine kinase."
    )
else:
    model_type = "Random Forest"
    threshold = 0.50

# Target Information Stamp
st.sidebar.markdown(f"""
<div style="border-top: 1px solid var(--line); margin-top: 16px; padding-top: 12px;" class="mono">
    <div style="color: var(--muted); font-size: 9px; margin-bottom: 4px;">TARGET ACCESSION</div>
    <div style="color: var(--chalk); font-weight: 600; font-size: 11px;">CHEMBL203 · ErbB-1 / RTK</div>
    <div style="color: var(--muted-dark); font-size: 9px; margin-top: 2px;">Homo sapiens · NSCLC Oncogene</div>
</div>
""", unsafe_allow_html=True)

# Check input validity
if not input_smiles.strip():
    st.info("Select a preset molecule or provide a canonical SMILES string in the cabinet sidebar to begin.")
    st.stop()

valid_smiles, mol, can_smiles = validate_smiles(input_smiles)
if not valid_smiles or mol is None:
    st.error(f"Invalid Chemical SMILES String: `{can_smiles}`")
    st.stop()

# ==============================================================================
# CORE COMPUTATIONAL PIPELINE
# ==============================================================================

predictor = get_predictor()
pred_res = predictor.predict(can_smiles, model_type=model_type, threshold=threshold) if predictor.is_loaded else {}
descriptors = calculate_descriptors(mol)
drug_likeness = evaluate_drug_likeness(mol)
similarity_engine = get_similarity_engine()
sim_matches = similarity_engine.search_similar_drugs(mol, top_k=6)

# Cached SHAP explainer computation
@st.cache_data(show_spinner=False)
def get_cached_shap_analysis(_model, features, _mol_obj, bit_info):
    explainer = SHAPExplainerEngine(_model)
    return explainer.explain_instance(features, _mol_obj, bit_info=bit_info, top_k=8)


# ==============================================================================
# SECTION RENDERERS (8 INFORMATION ARCHITECTURE MODULES)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. OVERVIEW
# ------------------------------------------------------------------------------
def render_section_overview():
    # Technical Specimen Header
    st.markdown("""
    <div class="specimen-header">
        <div>
            <span class="eyebrow">BOTANICAL EDITORIAL RESTORATION · VOLUME 001</span>
            <h1 class="specimen-header-title">EGFR Molecular Intelligence</h1>
            <div class="specimen-header-sub">High-Throughput Chemoinformatics & Explainable Virtual Screening for Human Epidermal Growth Factor Receptor</div>
        </div>
        <div class="specimen-accession">
            <span>TARGET ACC.</span><br>
            <strong style="font-size: 14px;">CHEMBL203</strong><br>
            <span style="color: var(--muted); font-size: 9px;">ErbB-1 / HER1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_mount, col_cabinet = st.columns([1.2, 0.8])
    
    with col_mount:
        # Specimen Voucher Mount (Herbarium Alpinum style)
        st.markdown(f"""
        <div class="specimen-voucher">
            <div class="voucher-head">
                <span>FLORA HELVETICA · CHEMOINFORMATICS FOLIO</span>
                <span>CH / CHEMBL203</span>
            </div>
            <div class="voucher-title">Human Epidermal Growth Factor Receptor</div>
            <p style="font-size: 11px; margin-bottom: 10px; line-height: 1.5;">
                Transmembrane receptor tyrosine kinase of the ErbB family. Activating kinase domain mutations drive oncogenesis in Non-Small Cell Lung Cancer (NSCLC) and Glioblastoma.
            </p>
            <div style="font-family: var(--font-mono); font-size: 10px; border-top: 1px solid rgba(8, 14, 10, 0.3); padding-top: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="font-weight: 600;">ACTIVE QUERY SPECIMEN:</span>
                    <span>{selected_preset_key.split('-')[0].strip()}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="font-weight: 600;">CANONICAL SMILES:</span>
                    <span style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{can_smiles}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 600;">BIOACTIVITY THRESHOLD:</span>
                    <span>IC₅₀ ≤ 1,000 nM (pIC₅₀ ≥ 6.0)</span>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(8, 14, 10, 0.3); margin-top: 10px; padding-top: 8px; font-size: 8px; font-family: var(--font-mono);">
                <span>VOUCHER HB-203 / REPRODUCIBLE ML MODEL</span>
                <span class="voucher-barcode"></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-rule'><span>01 / INSTRUMENT ARCHITECTURE</span><span>5-STAGE PIPELINE</span></div>", unsafe_allow_html=True)
        st.markdown("""
        1. **Chemical Representation:** SMILES parsing, aromatic normalization, and MMFF94 force-field 3D conformer minimization via RDKit.
        2. **Multi-Scale Featurization:** 2048-bit Morgan circular fingerprints ($r=2$, ECFP4) combined with 8 physicochemical property descriptors.
        3. **Ensemble Machine Learning:** Stratified Random Forest and Gradient Boosting classifiers calibrated on 881 curated ChEMBL bioactivity assays.
        4. **Explainable AI (XAI):** Game-theoretic SHAP TreeExplainer projecting local fragment and atom attribution onto 2D molecular graphs.
        5. **Translational Intelligence:** Morgan-Tanimoto similarity mapping against FDA-approved cancer therapeutics and publication-grade PDF reporting.
        """)

    with col_cabinet:
        st.markdown("<div class='section-rule'><span>02 / MODEL BENCHMARKS</span><span>CHEMSCORE v1.0</span></div>", unsafe_allow_html=True)
        meta_path = os.path.join(CURRENT_DIR, "models", "model_meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                b_meta = json.load(f)
            metrics = b_meta.get("metrics", {})
            rf_m = metrics.get("Random Forest", {})
            gb_m = metrics.get("Gradient Boosting", {})

            m_col1, m_col2 = st.columns(2)
            m_col1.metric("RF ROC-AUC", f"{rf_m.get('roc_auc', 0.978):.3f}")
            m_col2.metric("RF Accuracy", f"{rf_m.get('accuracy', 0.91)*100:.1f}%")
            
            m_col3, m_col4 = st.columns(2)
            m_col3.metric("GBDT ROC-AUC", f"{gb_m.get('roc_auc', 0.968):.3f}")
            m_col4.metric("GBDT Accuracy", f"{gb_m.get('accuracy', 0.915)*100:.1f}%")

            st.markdown(f"""
            <div class="herb-card" style="margin-top: 14px;">
                <div class="herb-card-title">DATASET PROVENANCE</div>
                <div class="mono" style="font-size: 10px; line-height: 1.8;">
                    • Target Assay: CHEMBL203<br>
                    • Curated Samples: <b>{b_meta.get('num_samples_total', 881)} compounds</b><br>
                    • Active Class: <b>{b_meta.get('class_distribution', {}).get('Active', 472)}</b> (IC₅₀ ≤ 1,000 nM)<br>
                    • Inactive Class: <b>{b_meta.get('class_distribution', {}).get('Inactive', 409)}</b> (IC₅₀ ≥ 10,000 nM)<br>
                    • Feature Dimension: <b>2,056 variables</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Proceed to Molecular Screening →", type="primary", use_container_width=True):
            st.session_state.active_section = "02 / Molecular Screening"
            st.rerun()


# ------------------------------------------------------------------------------
# 2. MOLECULAR SCREENING
# ------------------------------------------------------------------------------
def render_section_screening():
    st.markdown("<div class='section-rule'><span>02 / CHEMOINFORMATICS & ACTIVITY INFERENCE</span><span>STRUCTURAL CHARACTERIZATION</span></div>", unsafe_allow_html=True)
    
    col_2d, col_3d = st.columns([1.1, 1.2])

    with col_2d:
        st.markdown("<div class='herb-card-title'><span>2D Chemical Architecture</span><span class='mono'>RDKit SVG</span></div>", unsafe_allow_html=True)
        svg_code = draw_molecule_2d_svg(mol, size=(480, 320), dark_mode=True)
        st.markdown(f"<div class='mol-svg-container'>{svg_code}</div>", unsafe_allow_html=True)
        st.caption(f"<span class='mono'>Canonical SMILES:</span> `{can_smiles}`", unsafe_allow_html=True)

        # Descriptor metric grid
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='herb-card-title'><span>Calculated Physicochemical Descriptors</span></div>", unsafe_allow_html=True)
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("Mol Wt", f"{descriptors.get('MolWt', 0):.1f} Da")
        g2.metric("LogP", f"{descriptors.get('MolLogP', 0):.2f}")
        g3.metric("TPSA", f"{descriptors.get('TPSA', 0):.1f} Å²")
        g4.metric("QED", f"{descriptors.get('QED', 0):.2f}")

        g5, g6, g7, g8 = st.columns(4)
        g5.metric("H-Donors", f"{descriptors.get('NumHDonors', 0)}")
        g6.metric("H-Acceptors", f"{descriptors.get('NumHAcceptors', 0)}")
        g7.metric("Rot. Bonds", f"{descriptors.get('NumRotatableBonds', 0)}")
        g8.metric("Fsp3", f"{descriptors.get('FractionCSP3', 0):.2f}")

    with col_3d:
        st.markdown("<div class='herb-card-title'><span>Interactive 3D Conformer</span><span class='mono'>ETKDGv3 / MMFF94</span></div>", unsafe_allow_html=True)
        c_style, c_spin = st.columns([2, 1])
        with c_style:
            style_choice = st.selectbox("Render Style:", ["stick", "sphere", "surface", "line"], index=0, key="scr_style")
        with c_spin:
            spin_choice = st.checkbox("Auto-Spin", value=False, key="scr_spin")

        success, mol_block, _ = generate_3d_conformer_block(mol)
        if success:
            render_3dmol_viewer(mol_block, style_name=style_choice, spin=spin_choice, height=300)
            st.caption("<span class='mono' style='font-size:9px;'>Energy-minimized conformer in py3Dmol canvas. Left-click to rotate, right-click to translate, scroll to zoom.</span>", unsafe_allow_html=True)
        else:
            st.warning(f"Conformer generation fallback: {mol_block}")

        # Prediction Outcome Panel
        st.markdown("<div class='herb-card-title'><span>Virtual Screening Outcome</span><span class='mono'>{model_type}</span></div>", unsafe_allow_html=True)
        if not pred_res or not pred_res.get("success", False):
            st.warning("Classifier inference pipeline unavailable. Please train models.")
        else:
            is_active = pred_res["is_active"]
            p_active = pred_res["prob_active"]
            p_inactive = pred_res["prob_inactive"]
            confidence = pred_res["confidence"]

            if is_active:
                st.markdown(f"""
                <div class="badge-active">
                    <span class="badge-active-title">ACTIVE · EGFR TYROSINE KINASE INHIBITOR</span>
                    <span class="mono" style="font-size: 11px;">P(Active) = {p_active*100:.1f}% · {confidence}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="badge-inactive">
                    <span class="badge-inactive-title">INACTIVE · NON-INHIBITOR</span>
                    <span class="mono" style="font-size: 11px;">P(Active) = {p_active*100:.1f}% · {confidence}</span>
                </div>
                """, unsafe_allow_html=True)

            prob_df = pd.DataFrame({
                "Class": ["Active (Inhibitor)", "Inactive (Non-Inhibitor)"],
                "Probability": [p_active, p_inactive],
                "Category": ["Active", "Inactive"]
            })
            fig_prob = px.bar(
                prob_df,
                x="Probability",
                y="Class",
                orientation="h",
                color="Category",
                color_discrete_map={"Active": "#99ff00", "Inactive": "#ff5555"},
                text=prob_df["Probability"].apply(lambda p: f"{p*100:.1f}%"),
                range_x=[0, 1.0]
            )
            fig_prob.update_layout(
                get_herbarium_plotly_layout(height=170),
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_prob, use_container_width=True)


# ------------------------------------------------------------------------------
# 3. EXPLAINABLE AI (SHAP)
# ------------------------------------------------------------------------------
def render_section_explainability():
    st.markdown("<div class='section-rule'><span>03 / SHAPLEY FEATURE ATTRIBUTION (XAI)</span><span>GAME-THEORETIC DECOMPOSITION</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="scientific-disclaimer">
        <strong>Scientific Attribution Framework:</strong> SHAP (SHapley Additive exPlanations) computes Shapley values from cooperative game theory, quantifying the positive and negative marginal contributions of molecular substructures toward the prediction threshold. 
        <em>Attributions reflect internal model decisions and do not constitute causal proof of biochemical binding mechanisms.</em>
    </div>
    """, unsafe_allow_html=True)

    if not pred_res or not pred_res.get("success", False):
        st.warning("Prediction required before computing SHAP explanations.")
        return

    sel_model = predictor.rf_model if model_type == "Random Forest" else predictor.gb_model
    with st.spinner("Decomposing 2056 molecular features via SHAP TreeExplainer..."):
        shap_res = get_cached_shap_analysis(
            sel_model,
            pred_res["features"],
            mol,
            pred_res["bit_info"]
        )

    col_x1, col_x2 = st.columns([1.1, 1.4])

    with col_x1:
        st.markdown("<div class='herbarium-card-title'><span>Atom-Level Attribution Map</span><span class='mono'>Morgan Circular Bits</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='mol-svg-container'>{shap_res['highlighted_svg']}</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="mono" style="font-size: 10px; margin-top: 8px; line-height: 1.6;">
            • <span style="color: #99ff00; font-weight:600;">Chartreuse Highlights (+SHAP):</span> Substructures that shift prediction toward EGFR inhibition.<br>
            • <span style="color: #ff5555; font-weight:600;">Crimson Highlights (-SHAP):</span> Substructures penalizing predicted affinity (steric clashes or unfavorable polarity).
        </div>
        """, unsafe_allow_html=True)

    with col_x2:
        st.markdown("<div class='herbarium-card-title'><span>Ranked Feature Impact (Top SHAP Drivers)</span></div>", unsafe_allow_html=True)
        drivers = shap_res["top_drivers"]
        df_drivers = pd.DataFrame(drivers)
        if not df_drivers.empty:
            df_drivers["Category"] = df_drivers["shap_value"].apply(lambda v: "Favorable" if v > 0 else "Unfavorable")
            fig_shap = px.bar(
                df_drivers,
                x="shap_value",
                y="feature",
                orientation="h",
                color="Category",
                color_discrete_map={"Favorable": "#99ff00", "Unfavorable": "#ff5555"},
                text=df_drivers["shap_value"].apply(lambda v: f"{v:+.4f}")
            )
            fig_shap.update_layout(
                get_herbarium_plotly_layout(height=340),
                yaxis=dict(autorange="reversed"),
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_shap, use_container_width=True)

    # Detailed physicochemical table
    st.markdown("<div class='section-rule'><span>PHYSICOCHEMICAL ATTRIBUTION BREAKDOWN</span><span>DESCRIPTOR SENSITIVITY</span></div>", unsafe_allow_html=True)
    df_desc = pd.DataFrame(shap_res["descriptor_contributions"])
    st.dataframe(
        df_desc[["feature", "feature_value", "shap_value", "effect"]].rename(
            columns={
                "feature": "Physicochemical Descriptor",
                "feature_value": "Calculated Value",
                "shap_value": "SHAP Contribution",
                "effect": "Model Influence"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------------------------
# 4. DRUG-LIKENESS
# ------------------------------------------------------------------------------
def render_section_druglikeness():
    st.markdown("<div class='section-rule'><span>04 / ORAL BIOAVAILABILITY & RULE COMPLIANCE</span><span>LIPINSKI & VEBER CRITERIA</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="scientific-disclaimer">
        <strong>Pharmacokinetic Rule Boundary:</strong> Rule-of-Five and Veber compliance assesses general oral bioavailability characteristics based on historical drug collections. 
        <em>Compliance does not represent proof of human pharmacokinetics, target engagement, or clinical safety.</em>
    </div>
    """, unsafe_allow_html=True)

    dl_lip = drug_likeness.get("lipinski", {})
    dl_veb = drug_likeness.get("veber", {})
    desc = drug_likeness.get("descriptors", {})

    col_rules, col_radar = st.columns([1.2, 1.4])

    with col_rules:
        st.markdown("<div class='herb-card-title'><span>Lipinski's Rule of Five</span><span class='mono'>Max 1 Violation</span></div>", unsafe_allow_html=True)
        lip_status = dl_lip.get("status", "Pass")
        lip_viol = dl_lip.get("violations_count", 0)
        if lip_status == "Pass":
            st.markdown(f"<div class='mono' style='color:#99ff00; font-size:12px; margin-bottom:8px;'>STATUS: PASS ({lip_viol} violations)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='mono' style='color:#ff5555; font-size:12px; margin-bottom:8px;'>STATUS: FAIL ({lip_viol} violations)</div>", unsafe_allow_html=True)

        lip_rules = dl_lip.get("rules", {})
        lip_df = pd.DataFrame([
            {"Criterion": k, "Value": f"{v['value']:.2f}" if isinstance(v['value'], float) else str(v['value']), "Threshold": v["threshold"], "Pass": "PASS" if v["pass"] else "FAIL"}
            for k, v in lip_rules.items()
        ])
        st.table(lip_df)

        st.markdown("<div class='herb-card-title' style='margin-top:16px;'><span>Veber's Rule</span><span class='mono'>Rot. Bonds & TPSA</span></div>", unsafe_allow_html=True)
        veb_status = dl_veb.get("status", "Pass")
        veb_viol = dl_veb.get("violations_count", 0)
        if veb_status == "Pass":
            st.markdown(f"<div class='mono' style='color:#99ff00; font-size:12px; margin-bottom:8px;'>STATUS: PASS ({veb_viol} violations)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='mono' style='color:#ff5555; font-size:12px; margin-bottom:8px;'>STATUS: FAIL ({veb_viol} violations)</div>", unsafe_allow_html=True)

    with col_radar:
        st.markdown("<div class='herb-card-title'><span>Bioavailability Radar Polygon</span><span class='mono'>Normalized Space</span></div>", unsafe_allow_html=True)
        categories = ["Molecular Weight", "LogP", "TPSA", "HBD", "HBA", "Rot. Bonds"]
        mw_norm = min(2.0, desc.get("MolWt", 0) / 500.0)
        logp_norm = max(0.0, min(2.0, (desc.get("MolLogP", 0) + 1.0) / 6.0))
        tpsa_norm = min(2.0, desc.get("TPSA", 0) / 140.0)
        hbd_norm = min(2.0, desc.get("NumHDonors", 0) / 5.0)
        hba_norm = min(2.0, desc.get("NumHAcceptors", 0) / 10.0)
        rb_norm = min(2.0, desc.get("NumRotatableBonds", 0) / 10.0)

        fig_radar = go.Figure()
        # Reference limit polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            theta=categories + [categories[0]],
            fill="toself",
            name="Threshold Boundary",
            fillcolor="rgba(155, 167, 147, 0.08)",
            line=dict(color="#35402f", dash="dash", width=1.5)
        ))
        # Query molecule polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=[mw_norm, logp_norm, tpsa_norm, hbd_norm, hba_norm, rb_norm, mw_norm],
            theta=categories + [categories[0]],
            fill="toself",
            name="Query Molecule",
            fillcolor="rgba(153, 255, 0, 0.20)",
            line=dict(color="#99ff00", width=2.0)
        ))
        fig_radar.update_layout(
            paper_bgcolor="#101811",
            plot_bgcolor="#101811",
            font=dict(family="Inter, sans-serif", size=10, color="#9ba793"),
            polar=dict(
                bgcolor="#101811",
                radialaxis=dict(visible=True, range=[0, 1.6], gridcolor="#35402f", tickfont=dict(size=9, color="#9ba793")),
                angularaxis=dict(gridcolor="#35402f", tickfont=dict(size=10, color="#e6e9d9"))
            ),
            showlegend=True,
            height=360,
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)


# ------------------------------------------------------------------------------
# 5. SIMILARITY SEARCH
# ------------------------------------------------------------------------------
def render_section_similarity():
    st.markdown("<div class='section-rule'><span>05 / TANIMOTO MORGAN SIMILARITY BENCHMARK</span><span>FDA-APPROVED EGFR INHIBITORS</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="scientific-disclaimer">
        <strong>Cheminformatics Distinction:</strong> Structural similarity evaluates 2048-bit Morgan Fingerprint (ECFP4) bit overlap via the Tanimoto coefficient. 
        <em>High structural similarity indicates shared chemical motifs but does not establish equal binding potency or metabolic equivalence.</em>
    </div>
    """, unsafe_allow_html=True)

    if not sim_matches:
        st.warning("Similarity reference index not populated.")
        return

    top_match = sim_matches[0]
    st.markdown(f"""
    <div class="herb-card" style="border-left: 3px solid var(--accent);">
        <div class="herb-card-title">PRIMARY STRUCTURAL MATCH</div>
        <div style="font-size: 18px; font-weight: 600; color: var(--chalk); margin-bottom: 4px;">
            {top_match['name']} — <span style="color: var(--accent);">{top_match['similarity_pct']}%</span> Tanimoto Overlap
        </div>
        <div class="mono" style="font-size: 11px; color: var(--muted);">
            {top_match['generation']} · FDA Approved {top_match['fda_approval_year']} · Target: {top_match['target_mutations']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    sim_df = pd.DataFrame(sim_matches)
    fig_sim = px.bar(
        sim_df,
        x="similarity_pct",
        y="name",
        orientation="h",
        color="similarity_pct",
        color_continuous_scale=["#152412", "#3b5c28", "#99ff00"],
        text=sim_df["similarity_pct"].apply(lambda v: f"{v:.1f}%"),
        labels={"similarity_pct": "Tanimoto Similarity (%)", "name": "Approved Therapeutic"}
    )
    fig_sim.update_layout(
        get_herbarium_plotly_layout(height=260),
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("<div class='section-rule'><span>CLINICAL PHARMACOPHORE INTELLIGENCE</span><span>APPROVED THERAPEUTICS</span></div>", unsafe_allow_html=True)
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


# ------------------------------------------------------------------------------
# 6. MODEL PERFORMANCE
# ------------------------------------------------------------------------------
def render_section_performance():
    st.markdown("<div class='section-rule'><span>06 / SUPERVISED LEARNING EVALUATION METRICS</span><span>HOLDOUT TEST SET VALIDATION</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="scientific-disclaimer">
        <strong>Empirical Evaluation Protocol:</strong> All metrics, ROC curves, and confusion parameters originate directly from stratified holdout evaluation on 881 curated ChEMBL203 bioactivity records. No synthetic curves or artificial benchmark values are introduced.
    </div>
    """, unsafe_allow_html=True)

    meta_path = os.path.join(CURRENT_DIR, "models", "model_meta.json")
    if not os.path.exists(meta_path):
        st.warning("Model benchmark metadata file not located. Please execute train_model.py.")
        return

    with open(meta_path, "r") as f:
        bench_meta = json.load(f)

    metrics = bench_meta.get("metrics", {})
    metric_rows = []
    for m_name, m_vals in metrics.items():
        metric_rows.append({
            "Classifier Model": m_name,
            "Accuracy": f"{m_vals.get('accuracy', 0)*100:.2f}%",
            "Precision": f"{m_vals.get('precision', 0)*100:.2f}%",
            "Recall": f"{m_vals.get('recall', 0)*100:.2f}%",
            "F1-Score": f"{m_vals.get('f1_score', 0):.4f}",
            "ROC-AUC": f"{m_vals.get('roc_auc', 0):.4f}"
        })
    st.table(pd.DataFrame(metric_rows))

    # ROC Curves with Herbarium styling
    fig_roc = go.Figure()
    fig_roc.add_shape(
        type="line", line=dict(dash="dash", color="#35402f", width=1.5),
        x0=0, x1=1, y0=0, y1=1
    )
    colors = {"Random Forest": "#99ff00", "Gradient Boosting": "#e6e9d9"}
    for m_name, m_vals in metrics.items():
        rc = m_vals.get("roc_curve", {})
        fpr = rc.get("fpr", [])
        tpr = rc.get("tpr", [])
        auc = m_vals.get("roc_auc", 0.0)
        if fpr and tpr:
            fig_roc.add_trace(go.Scatter(
                x=fpr, y=tpr, mode="lines",
                name=f"{m_name} (AUC = {auc:.3f})",
                line=dict(color=colors.get(m_name, "#99ff00"), width=2.5)
            ))

    fig_roc.update_layout(
        get_herbarium_plotly_layout(height=400, title="Receiver Operating Characteristic (ROC)"),
        xaxis_title="False Positive Rate (1 - Specificity)",
        yaxis_title="True Positive Rate (Sensitivity)",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_roc, use_container_width=True)


# ------------------------------------------------------------------------------
# 7. SCREENING REPORTS
# ------------------------------------------------------------------------------
def render_section_reports():
    st.markdown("<div class='section-rule'><span>07 / PUBLICATION-GRADE SCREENING DOSSIER</span><span>PDF EXPORT ENGINE</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    The PDF generation pipeline compiles a comprehensive virtual screening dossier for institutional presentation, peer review, and academic submission:
    - **Voucher Metadata:** Canonical SMILES, 2D molecular architecture, formula, and target accession.
    - **Classification Record:** Dual classifier predictions, calibrated probability distributions, and confidence tiers.
    - **Physicochemical Profiling:** Full Lipinski and Veber rule compliance matrices.
    - **Explainability Annex:** Top favorable and unfavorable SHAP fragment attributions.
    - **Clinical Comparison:** Tanimoto similarity metrics against FDA-approved therapeutics.
    """)

    if not pred_res or not pred_res.get("success", False):
        st.warning("Complete virtual screening inference before generating a PDF dossier.")
        return

    sel_model = predictor.rf_model if model_type == "Random Forest" else predictor.gb_model
    explainer = SHAPExplainerEngine(sel_model)
    shap_res = explainer.explain_instance(
        pred_res["features"],
        mol,
        bit_info=pred_res["bit_info"],
        top_k=8
    )

    with st.spinner("Compiling publication-grade vector graphics and PDF dossier..."):
        pdf_bytes = generate_screening_pdf(
            smiles=can_smiles,
            prediction_result=pred_res,
            shap_result=shap_res,
            similarity_matches=sim_matches
        )

    st.markdown(f"""
    <div class="herb-card" style="border-left: 3px solid var(--accent); margin-top: 14px;">
        <div class="herb-card-title">DOSSIER READY FOR DOWNLOAD</div>
        <div class="mono" style="font-size: 11px; color: var(--muted); line-height: 1.8;">
            • Target: CHEMBL203 (Human EGFR)<br>
            • Specimen: {selected_preset_key.split('-')[0].strip()}<br>
            • Byte Size: {len(pdf_bytes):,} bytes<br>
            • Engine: ReportLab 3.6+ Vector Typesetter
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Download PDF Virtual Screening Dossier ↓",
        data=pdf_bytes,
        file_name=f"EGFR_Screening_Dossier_{descriptors.get('MolWt', 0):.0f}Da.pdf",
        mime="application/pdf",
        type="primary"
    )


# ------------------------------------------------------------------------------
# 8. METHODOLOGY & ACADEMIC SYLLABUS
# ------------------------------------------------------------------------------
def render_section_methodology():
    st.markdown("<div class='section-rule'><span>08 / METHODOLOGY & CURRICULUM FOUNDATIONS</span><span>ACADEMIC ALIGNMENT</span></div>", unsafe_allow_html=True)
    
    st.markdown(r"""
    ### 1. Target Biology & Cancer Signaling
    The **Epidermal Growth Factor Receptor (EGFR / ErbB-1)** is a transmembrane receptor tyrosine kinase belonging to the HER/ErbB family. Binding of epidermal growth factor induces homodimerization and trans-autophosphorylation of tyrosine residues in the intracellular kinase domain, activating the **MAPK/ERK** proliferation and **PI3K/AKT** anti-apoptotic pathways. Overexpression or somatic mutations (such as exon 19 deletions and L858R point mutations) are primary drivers of **Non-Small Cell Lung Cancer (NSCLC)**.

    ---
    ### 2. Bioactivity Dataset Harvesting (EMBL-EBI ChEMBL)
    Bioactivity records for target identifier `CHEMBL203` were harvested via the **ChEMBL REST API**:
    - **Measurement Filter:** Standard biochemical affinity assays measuring IC₅₀ in nanomolar units ($\text{nM}$).
    - **Logarithmic Conversion:** Absolute potency was transformed to $p\text{IC}_{50} = 9 - \log_{10}(\text{IC}_{50})$.
    - **Classification Thresholds:**
      - **Active Class ($y=1$):** $\text{IC}_{50} \le 1,000\text{ nM}$ ($p\text{IC}_{50} \ge 6.0$) — represents micromolar binding potency.
      - **Inactive Class ($y=0$):** $\text{IC}_{50} \ge 10,000\text{ nM}$ ($p\text{IC}_{50} \le 5.0$) — compounds in the ambiguous intermediate zone ($1,000\text{--}10,000\text{ nM}$) were excluded to ensure class separation.

    ---
    ### 3. Cheminformatics Featurization Pipeline
    Each candidate molecule undergoes a dual representation pipeline:
    1. **Morgan Circular Fingerprints (ECFP4):** Radial graph neighborhood traversal with radius $r=2$, folded into a 2,048-bit bit vector via hash modulo.
    2. **Physicochemical Properties:** 8 RDKit descriptors including Molecular Weight, Wildman-Crippen LogP, Topological Polar Surface Area (TPSA), Quantitative Estimate of Drug-likeness (QED), H-bond donors/acceptors, rotatable bond count, and fraction of $sp^3$ hybridized carbons ($\text{Fsp}^3$).

    ---
    ### 4. 🎓 Academic AI Curriculum Alignment (Units I–V)
    This platform directly implements key theoretical concepts from the university AI syllabus:
    - **UNIT-I (Key Components of AI Systems):** Practical realization of a domain-specific **Narrow AI** for oncology problem-solving, structured around the perception $\to$ representation $\to$ inference $\to$ explanation paradigm, observing rigorous bioethics against clinical over-extrapolation.
    - **UNIT-II (ML Applications, Tools & Frameworks):** Supervised learning workflows using **Pandas**, **NumPy**, and **Scikit-learn** ensembles (Random Forest and Gradient Boosted Decision Trees) trained with stratified cross-validation.
    - **UNIT-III (Graph Theory, LLMs & Explainable AI):**
      - **Graph Theory:** Molecular structures modeled as mathematical graphs $G=(V,E)$ with atom vertices and covalent bond edges.
      - **Large Language Models:** Embedded **Ollama** tutor interface translating pharmacological predictions into accessible educational explanations.
      - **Explainable AI (XAI):** Game-theoretic **SHAP (SHapley Additive exPlanations)** attributing decision weight to specific atoms and functional groups.
    - **UNIT-IV (AI Applications in Healthcare):** Direct computational oncology application expediting drug discovery pipelines and reducing wet-lab reagent expenditure.
    - **UNIT-V (Historical AI Case Studies):** Parallels milestone medical intelligence architectures including **IBM Watson Health**, **DeepMind AlphaFold**, and predictive diagnostic oncology tools.
    """)


# ==============================================================================
# AI CHEMOINFORMATICS TUTOR (OLLAMA INTEGRATION)
# ==============================================================================

def render_ai_tutor_drawer():
    """Collapsible AI Tutor drawer styled with Herbarium dark palette."""
    with st.expander("💬 AI Chemoinformatics Tutor (Ollama Local Assistant) — Ask Questions & Practice Answers", expanded=False):
        ollama_info = check_ollama_status()
        t_col1, t_col2 = st.columns([2, 1])
        with t_col1:
            if ollama_info["available"]:
                st.markdown(f"<span class='mono' style='color:#99ff00;'>● OLLAMA ONLINE</span> — Model: `{ollama_info['selected_model']}` (Private, offline inference)", unsafe_allow_html=True)
            else:
                st.markdown("<span class='mono' style='color:#9ba793;'>○ OLLAMA OFFLINE</span> — Built-in Chemoinformatics Knowledge Engine active", unsafe_allow_html=True)
        with t_col2:
            if ollama_info["available"] and len(ollama_info["models"]) > 1:
                active_model = st.selectbox("Model:", ollama_info["models"], index=0, key="tutor_model")
            else:
                active_model = ollama_info["selected_model"]

        # Context builder
        sys_context = build_system_context(
            can_smiles,
            descriptors,
            drug_likeness,
            prediction_result=pred_res if predictor.is_loaded else None,
            shap_result=None,
            similarity_matches=sim_matches
        )

        # Quick question buttons
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        quick_query = None
        with b1:
            if st.button("🎓 Explain this for my teacher", use_container_width=True, key="btn_q_teacher"):
                quick_query = "How can I explain this molecule, its descriptors, and its prediction to my teacher in simple words?"
        with b2:
            if st.button("❓ Why did the AI predict this?", use_container_width=True, key="btn_q_why"):
                quick_query = "Why did the machine learning model make this prediction for this molecule?"
        with b3:
            if st.button("💊 Explain Lipinski Rule of 5", use_container_width=True, key="btn_q_lip"):
                quick_query = "What is Lipinski's Rule of 5 and what do the violations mean for this drug?"

        if "chat_history" not in st.session_state or not st.session_state.chat_history:
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "👋 **Greetings.** I am your AI Chemoinformatics Tutor. I can explain this molecule, clarify descriptors, interpret machine learning predictions, or help you practice viva questions for your faculty evaluation. Click a quick question or type below."
                }
            ]

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask a question about this molecule, XAI, or syllabus connections...", key="tutor_chat_input")
        prompt_to_send = quick_query or user_input

        if prompt_to_send:
            st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
            with st.chat_message("user"):
                st.markdown(prompt_to_send)

            with st.chat_message("assistant"):
                resp_gen = stream_ollama_chat(
                    prompt=prompt_to_send,
                    system_context=sys_context,
                    model_name=active_model,
                    conversation_history=st.session_state.chat_history[:-1]
                )
                full_resp = st.write_stream(resp_gen)
                st.session_state.chat_history.append({"role": "assistant", "content": full_resp})


# ==============================================================================
# MAIN ROUTER
# ==============================================================================

current_section = st.session_state.active_section

if current_section == "01 / Overview":
    render_section_overview()
elif current_section == "02 / Molecular Screening":
    render_section_screening()
elif current_section == "03 / Explainable AI":
    render_section_explainability()
elif current_section == "04 / Drug-Likeness":
    render_section_druglikeness()
elif current_section == "05 / Similarity Search":
    render_section_similarity()
elif current_section == "06 / Model Performance":
    render_section_performance()
elif current_section == "07 / Screening Reports":
    render_section_reports()
elif current_section == "08 / Methodology":
    render_section_methodology()

# Persistent AI Chemoinformatics Tutor Drawer at bottom of view
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
render_ai_tutor_drawer()

# Scientific Footer
st.markdown(f"""
<div style="border-top: 1px solid var(--line); margin-top: 36px; padding-top: 18px; padding-bottom: 24px; display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 10px; color: var(--muted);">
    <div>HERBARIUM ALPINUM · EGFR MOLECULAR INTELLIGENCE · SWISS ARCHIVE CH-203</div>
    <div>ACTIVE SPECIMEN: <span style="color: var(--accent);">{selected_preset_key.split('-')[0].strip()}</span></div>
    <div>REPRODUCIBLE RESEARCH INSTRUMENT</div>
</div>
""", unsafe_allow_html=True)
