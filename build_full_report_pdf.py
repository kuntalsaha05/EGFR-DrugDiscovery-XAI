"""
Generates the Complete Academic Project Report PDF adhering to
Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune guidelines
for the AI Systems and Applications course under the guidance of Dr. Devendra Joshi.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(CURRENT_DIR, "ACADEMIC_PROJECT_REPORT.pdf")
LOGO_PNG = os.path.join(CURRENT_DIR, "mit_wpu_logo.png")

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Don't draw headers/footers on title page (page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#475569"))
            
            # Running Header
            self.drawString(54, 800, "MIT-WPU PUNE · AI SYSTEMS & APPLICATIONS · EGFR VIRTUAL SCREENING")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 794, 541, 794)
            
            # Running Footer
            self.line(54, 45, 541, 45)
            self.drawString(54, 34, "Dr. Vishwanath Karad MIT World Peace University, Pune — Guide: Dr. Devendra Joshi")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(541, 34, page_text)
            self.restoreState()


def generate_full_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom typography styles
    title_univ = ParagraphStyle(
        "UnivTitle",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#800000")  # MIT-WPU Maroon
    )
    title_sub = ParagraphStyle(
        "SubTitle",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=14
    )
    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )
    h1_style = ParagraphStyle(
        "H1Heading",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "H2Heading",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=9,
        spaceAfter=3,
        keepWithNext=True
    )
    center_p = ParagraphStyle(
        "CenterP",
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#1e293b")
    )
    
    story = []

    # =========================================================================
    # 1. TITLE PAGE (MIT-WPU PUNE)
    # =========================================================================
    story.append(Spacer(1, 10))
    if os.path.exists(LOGO_PNG):
        story.append(Image(LOGO_PNG, width=280, height=84))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<b>Dr. Vishwanath Karad MIT WORLD PEACE UNIVERSITY, PUNE</b>", title_univ))
    story.append(Spacer(1, 14))
    story.append(Paragraph("A MINI PROJECT REPORT ON", ParagraphStyle("Cap", fontName="Helvetica-Bold", fontSize=10, alignment=1, spaceAfter=6, textColor=colors.HexColor("#475569"))))
    story.append(Paragraph("<b>EXPLAINABLE AI-BASED DRUG DISCOVERY ASSISTANT FOR EARLY MOLECULAR SCREENING</b>", title_sub))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>Submitted in partial fulfillment of the requirements for the course</i><br/><b>AI SYSTEMS AND APPLICATIONS</b>", center_p))
    story.append(Spacer(1, 24))
    
    cand_info = [
        [Paragraph("<b>Submitted by:</b>", body_style), Paragraph("<b>Under the Guidance of:</b>", body_style)],
        [Paragraph("<b>Kuntal Saha</b> (PRN / Roll No: _____________) <br/>[Team Member 2 Name] (PRN: _____________) <br/>[Team Member 3 Name] (PRN: _____________)", body_style),
         Paragraph("<b>Dr. Devendra Joshi</b><br/>Department of Artificial Intelligence & Data Science,<br/>School of Computer Science & Engineering", body_style)]
    ]
    t_cand = Table(cand_info, colWidths=[240, 240])
    t_cand.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0)
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 35))
    
    story.append(Paragraph("<b>Department of Artificial Intelligence and Data Science<br/>Dr. Vishwanath Karad MIT World Peace University</b><br/>Paud Road, Kothrud, Pune, Maharashtra – 411 038, India<br/><b>Academic Year: 2026–2027</b>", center_p))
    story.append(PageBreak())

    # =========================================================================
    # 2. ABSTRACT & INTRODUCTION (>250 WORDS)
    # =========================================================================
    story.append(Paragraph("ABSTRACT & INTRODUCTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("Traditional pharmaceutical drug discovery is an extraordinarily costly, labor-intensive, and protracted endeavor, typically spanning 10 to 15 years and requiring capital investments exceeding $2 billion per approved therapeutic entity. A predominant cause of this severe developmental attrition is the late-stage failure of candidate chemical compounds during preclinical animal trials and human clinical phases, largely attributable to inadequate target binding affinity, off-target cellular toxicity, or poor oral pharmacokinetics. In classical High-Throughput Screening (HTS), pharmaceutical laboratories empirically assay millions of physical chemical compounds against disease proteins, consuming vast quantities of expensive biological reagents and technician hours.", body_style))
    story.append(Paragraph("This mini-project for <b>AI Systems and Applications</b>, developed under the mentorship of <b>Dr. Devendra Joshi</b> at <b>MIT World Peace University (MIT-WPU), Pune</b>, introduces <b>EGFR Molecular Intelligence</b>—an end-to-end, interpretable computational framework for early-stage Virtual High-Throughput Screening (vHTS). The application specifically targets <b>Human Epidermal Growth Factor Receptor (EGFR / ErbB-1, ChEMBL ID: CHEMBL203)</b>, a transmembrane receptor tyrosine kinase whose hyper-activation drives oncogenic proliferation in Non-Small Cell Lung Cancer (NSCLC) and Glioblastoma.", body_style))
    story.append(Paragraph("By training on a curated benchmark of 881 small-molecule bioactivity assays extracted from the EMBL-EBI ChEMBL database, the platform translates raw chemical representations (SMILES notation) into composite 2,056-dimensional numerical feature spaces combining <b>2048-bit Extended Connectivity Circular Fingerprints (ECFP4)</b> with 8 physicochemical property descriptors. Supervised ensemble models—<b>Random Forest (RF)</b> and <b>Gradient Boosted Decision Trees (GBDT)</b>—achieved exceptional predictive performance on a holdout test set with test accuracies of <b>90.96%</b> and <b>91.53%</b>, and Area Under the ROC Curve (<b>ROC-AUC</b>) metrics of <b>0.978</b> and <b>0.968</b>, respectively.", body_style))
    story.append(Paragraph("To resolve the opaque 'black-box' dilemma that historically impedes clinician and chemist trust in biomedical AI, the platform incorporates <b>Explainable AI (XAI)</b> based on <b>TreeSHAP (SHapley Additive exPlanations)</b> cooperative game theory. The system computes exact polynomial-time Shapley attributions and projects them directly onto 2D molecular graphs, highlighting favorable binding anchors in fluorescent chartreuse and unfavorable steric penalties in crimson. The platform additionally assesses oral drug-likeness via <b>Lipinski’s Rule of Five</b> and <b>Veber’s rules</b>, computes <b>Tanimoto structural similarity</b> against FDA-approved cancer drugs (Gefitinib, Erlotinib, Osimertinib), embeds an offline <b>Ollama Large Language Model (LLM)</b> chemoinformatics tutor, and compiles automated vector PDF screening dossiers via ReportLab.", body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>KEYWORDS:</b> Explainable AI (XAI), Artificial Intelligence Systems, Virtual Screening, Epidermal Growth Factor Receptor (EGFR), Human ChEMBL203, SHAP TreeExplainer, RDKit, Random Forest, Gradient Boosting, Morgan Fingerprints (ECFP4), Lipinski Rule of Five, MIT-WPU Pune.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 3. SECTION 1: MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("SECTION 1: MOTIVATION & PROBLEM STATEMENT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("1.1 The Pharmaceutical Discovery Bottleneck", h2_style))
    story.append(Paragraph("Pharmaceutical development faces steep attrition: only 1 in 10,000 synthesized compounds ultimately gains regulatory approval. Traditional High-Throughput Screening (HTS) requires hundreds of thousands of robotic wet-lab enzymatic assays, incurring substantial costs. Deploying <b>Narrow Artificial Intelligence as an intelligent pre-filter</b> enables rapid <i>in silico</i> digital evaluation, discarding non-viable chemical structures before physical synthesis occurs.", body_style))
    
    story.append(Paragraph("1.2 Target Biology: Oncogenic Human EGFR (CHEMBL203)", h2_style))
    story.append(Paragraph("The Epidermal Growth Factor Receptor (EGFR / ErbB-1) is a transmembrane tyrosine kinase receptor. Somatic activating mutations—specifically exon 19 deletions and the L858R point mutation—drive uncontrolled proliferation in Non-Small Cell Lung Cancer (NSCLC). While 1st-generation ATP-competitive inhibitors (Gefitinib) provide clinical benefits, acquired secondary mutations (T790M) necessitate continuous discovery of diverse chemical scaffolds capable of kinase inhibition.", body_style))
    
    story.append(Paragraph("1.3 Key Project Objectives", h2_style))
    story.append(Paragraph("• Build an end-to-end Python pipeline parsing SMILES strings into energy-minimized 3D conformers.<br/>• Curate 881 bioactivity assays from ChEMBL (CHEMBL203) with a verified IC₅₀ ≤ 1,000 nM active threshold.<br/>• Formulate 2,056-dimensional feature spaces (2,048 ECFP4 bits + 8 RDKit descriptors).<br/>• Train Random Forest and GBDT ensembles achieving ROC-AUC > 0.96.<br/>• Provide atom-level TreeSHAP game-theoretic explainability on 2D diagrams.<br/>• Profile oral bioavailability (Lipinski/Veber) and clinical Tanimoto similarity.<br/>• Deliver an interactive Streamlit UI, an offline Ollama LLM tutor, and automated PDF reporting.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 4. SECTION 2: END-TO-END WORKFLOW
    # =========================================================================
    story.append(Paragraph("SECTION 2: END-TO-END SYSTEM WORKFLOW", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("2.1 Pipeline Flowchart & Architectural Workflow", h2_style))
    story.append(Paragraph("The system operates as an integrated multi-stage inference and explainability engine:", body_style))
    
    workflow_box = [
        [Paragraph("<b>STAGE 1: Chemical Ingestion & Geometry Optimization</b><br/>User SMILES ──► RDKit Validation ──► 2D Planar SVG ──► ETKDGv3 MMFF94 3D Conformer", body_style)],
        [Paragraph("<b>STAGE 2: Multi-Scale Molecular Featurization</b><br/>2048-bit Morgan Fingerprints (ECFP4, r=2) + 8 Scaled Physicochemical Descriptors ──► Feature Vector x in R^2056", body_style)],
        [Paragraph("<b>STAGE 3: Supervised Ensemble Inference & Probability Calibration</b><br/>Random Forest (100 Trees) & GBDT (100 Estimators) ──► P(Active) ──► Decision Threshold (0.50)", body_style)],
        [Paragraph("<b>STAGE 4: Game-Theoretic Explainability (TreeSHAP)</b><br/>Exact Polynomial TreeSHAP ──► RDKit bitInfo Coordinate Mapping ──► 2D Atom Highlight Map", body_style)],
        [Paragraph("<b>STAGE 5: Translational Intelligence & Automated Reporting</b><br/>Lipinski/Veber Radar Chart ──► Tanimoto Similarity vs FDA Drugs ──► Ollama LLM Tutor ──► PDF Export", body_style)]
    ]
    t_wf = Table(workflow_box, colWidths=[480])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_wf)
    story.append(PageBreak())

    # =========================================================================
    # 5. SECTION 3: SYSTEM METHODOLOGY
    # =========================================================================
    story.append(Paragraph("SECTION 3: SYSTEM METHODOLOGY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("3.1 ChEMBL Data Curation & Logarithmic Transformation", h2_style))
    story.append(Paragraph("Bioactivity records for target CHEMBL203 were filtered for IC₅₀ measurements in nM and transformed to logarithmic potency: <b>pIC₅₀ = 9 - log₁₀(IC₅₀)</b>. Compounds with IC₅₀ ≤ 1,000 nM (pIC₅₀ ≥ 6.0) were labeled Active (y=1), and IC₅₀ ≥ 10,000 nM were labeled Inactive (y=0). Ambiguous intermediates were excluded, yielding 881 curated compounds.", body_style))
    
    story.append(Paragraph("3.2 Featurization & Physicochemical Descriptors", h2_style))
    story.append(Paragraph("Each molecule is transformed into 2048-bit circular Morgan fingerprints (ECFP4, radius 2) and 8 standardized bulk descriptors:", body_style))
    
    desc_data = [
        [Paragraph("<b>Descriptor</b>", body_style), Paragraph("<b>Physical Property</b>", body_style), Paragraph("<b>Clinical Role in Drug Discovery</b>", body_style)],
        [Paragraph("MolWt", body_style), Paragraph("Molecular Weight (Da)", body_style), Paragraph("Cavity fit, passive transcellular diffusion", body_style)],
        [Paragraph("MolLogP", body_style), Paragraph("Octanol-water partition", body_style), Paragraph("Lipophilicity, gut absorption, membrane permeability", body_style)],
        [Paragraph("TPSA", body_style), Paragraph("Polar Surface Area (Å²)", body_style), Paragraph("Epithelial permeability, blood-brain barrier transport", body_style)],
        [Paragraph("HBD / HBA", body_style), Paragraph("H-Bond Donors & Acceptors", body_style), Paragraph("Directional binding capability with ATP-pocket residues", body_style)],
        [Paragraph("NumRotBonds", body_style), Paragraph("Rotatable Bond Count", body_style), Paragraph("Conformational flexibility; high counts penalize entropy", body_style)],
        [Paragraph("QED", body_style), Paragraph("Drug-likeness desirability", body_style), Paragraph("Desirability metric combining 8 properties (0.0 to 1.0)", body_style)]
    ]
    t_desc = Table(desc_data, colWidths=[75, 145, 260])
    t_desc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_desc)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("3.3 TreeSHAP Game-Theoretic Explainability", h2_style))
    story.append(Paragraph("Model predictions are decomposed into additive Shapley contributions: <b>f(x) = φ₀ + Σ φᵢ(x)</b>. Active fingerprint bits are mapped to central atoms and neighborhood radii via RDKit bitInfo, yielding color-coded 2D atomic highlights (Chartreuse = Favorable binding anchor, Crimson = Steric penalty).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 6. SECTION 4: EXPERIMENTAL RESULTS
    # =========================================================================
    story.append(Paragraph("SECTION 4: EXPERIMENTAL RESULTS & DISCUSSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("4.1 Holdout Test Set Performance Metrics", h2_style))
    story.append(Paragraph("Evaluated on 177 holdout compounds (20% stratified test split from 881 curated ChEMBL molecules):", body_style))
    
    res_data = [
        [Paragraph("<b>Model Classifier</b>", body_style), Paragraph("<b>Test Accuracy</b>", body_style), Paragraph("<b>Precision</b>", body_style), Paragraph("<b>Recall</b>", body_style), Paragraph("<b>F1-Score</b>", body_style), Paragraph("<b>Test ROC-AUC</b>", body_style)],
        [Paragraph("Random Forest (RF)", body_style), Paragraph("<b>90.96%</b>", body_style), Paragraph("90.62%", body_style), Paragraph("92.55%", body_style), Paragraph("0.9158", body_style), Paragraph("<b>0.9784</b>", body_style)],
        [Paragraph("Gradient Boosting (GBDT)", body_style), Paragraph("<b>91.53%</b>", body_style), Paragraph("91.67%", body_style), Paragraph("92.55%", body_style), Paragraph("0.9206", body_style), Paragraph("<b>0.9678</b>", body_style)]
    ]
    t_res = Table(res_data, colWidths=[130, 70, 70, 70, 70, 70])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_res)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("4.2 Explainable AI Case Studies (Gefitinib vs. Aspirin Control)", h2_style))
    story.append(Paragraph("• <b>Gefitinib (Approved Active):</b> Predicted Active with <b>99.8% probability</b>. Top positive SHAP drivers identified the 4-anilinoquinazoline core and the 3-chloro-4-fluoroaniline moiety, matching crystallographic hinge-binding anchors with Met793.<br/>• <b>Aspirin (Negative Control):</b> Predicted Inactive with <b>7.7% probability</b>. SHAP identified low molecular weight (180 Da) and the negatively charged carboxylate group as severe penalties (-SHAP), causing electrostatic repulsion with the hydrophobic ATP pocket.", body_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("4.3 Oral Bioavailability & Clinical Similarity Benchmarks", h2_style))
    story.append(Paragraph("Gefitinib and Erlotinib pass all Lipinski and Veber criteria with 0 violations. Tanimoto similarity against clinical drugs correctly identified Gefitinib at 100%, Erlotinib at 100%, and Canertinib at 78.4% homology.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 7. SECTION 5: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("SECTION 5: CONCLUSION & FUTURE SCOPE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("5.1 Conclusion", h2_style))
    story.append(Paragraph("This mini-project for <b>AI Systems and Applications</b> at <b>MIT World Peace University (MIT-WPU), Pune</b>, conducted under the guidance of <b>Dr. Devendra Joshi</b>, successfully established an explainable virtual screening platform for Human EGFR inhibitors. Combining 2048-bit Morgan circular fingerprints with tree ensembles yielded <b>90.96% accuracy and 0.978 ROC-AUC</b>, while TreeSHAP provided actionable atom-level structural rationales.", body_style))
    
    story.append(Paragraph("5.2 Key Technical Advantages", h2_style))
    story.append(Paragraph("• <b>Sub-Second Throughput:</b> Screens molecules <i>in silico</i> in < 50 ms, saving months of wet-lab screening.<br/>• <b>Actionable Interpretability:</b> Decomposes black-box predictions into atom-level highlights for lead optimization.<br/>• <b>Dual Affinity & Bioavailability Filtering:</b> Concurrently evaluates binding and Lipinski/Veber oral absorption.<br/>• <b>Offline Privacy:</b> Local Ollama LLM and Python inference ensure zero external cloud data exposure.", body_style))
    
    story.append(Paragraph("5.3 Future Scope", h2_style))
    story.append(Paragraph("• Extend featurization to 3D Equivariant Graph Neural Networks (EGNN).<br/>• Expand models across the multi-target human kinome (HER2, HER4, VEGFR2).<br/>• Couple with reinforcement learning for <i>de novo</i> drug design.<br/>• Incorporate quantitative hERG cardiac and CYP450 toxicity predictors.", body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 8. SECTION 6: REFERENCES (24 CITATIONS)
    # =========================================================================
    story.append(Paragraph("SECTION 6: REFERENCES (24 ACADEMIC CITATIONS)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=8))
    refs = [
        "[1] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' <i>NeurIPS</i>, vol. 30, pp. 4765–4774, 2017.",
        "[2] S. M. Lundberg et al., 'From local explanations to global understanding with explainable AI for trees,' <i>Nature Machine Intelligence</i>, vol. 2, pp. 56–67, 2020.",
        "[3] S. Bandyopadhyay and S. Saha, <i>Unsupervised Classification: Similarity Measures and Applications</i>. Springer, 2013.",
        "[4] C. A. Lipinski et al., 'Experimental approaches to estimate solubility and permeability in drug discovery,' <i>Adv. Drug Deliv. Rev.</i>, vol. 46, pp. 3–26, 2001.",
        "[5] D. F. Veber et al., 'Molecular properties that influence the oral bioavailability of drug candidates,' <i>J. Med. Chem.</i>, vol. 45, pp. 2615–2623, 2002.",
        "[6] D. Rogers and M. Hahn, 'Extended-connectivity fingerprints,' <i>J. Chem. Inf. Model.</i>, vol. 50, no. 5, pp. 742–754, 2010.",
        "[7] G. Landrum et al., 'RDKit: Open-source cheminformatics,' <i>GitHub repository</i>, https://github.com/rdkit/rdkit, 2023.",
        "[8] A. Gaulton et al., 'ChEMBL: a large-scale bioactivity database for drug discovery,' <i>Nucleic Acids Res.</i>, vol. 40, pp. D1100–D1107, 2012.",
        "[9] L. Breiman, 'Random Forests,' <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, 2001.",
        "[10] J. H. Friedman, 'Greedy function approximation: A gradient boosting machine,' <i>Annals of Statistics</i>, vol. 29, pp. 1189–1232, 2001.",
        "[11] R. Sordella et al., 'Gefitinib-sensitizing EGFR mutations in lung cancer activate selective apoptotic pathways,' <i>Science</i>, vol. 305, pp. 1163–1167, 2004.",
        "[12] D. A. Cross et al., 'AZD9291, an irreversible EGFR TKI, overcomes T790M-mediated resistance,' <i>Cancer Discovery</i>, vol. 4, pp. 1046–1061, 2014.",
        "[13] G. R. Bickerton et al., 'Quantifying the chemical beauty of drugs,' <i>Nature Chemistry</i>, vol. 4, no. 2, pp. 90–98, 2012.",
        "[14] F. Pedregosa et al., 'Scikit-learn: Machine learning in Python,' <i>J. Machine Learning Research</i>, vol. 12, pp. 2825–2830, 2011.",
        "[15] S. A. Wildman and G. M. Crippen, 'Prediction of physicochemical parameters by atomic contributions,' <i>J. Chem. Inf. Comput. Sci.</i>, vol. 39, pp. 868–873, 1999.",
        "[16] P. Ertl et al., 'Fast calculation of molecular polar surface area as a sum of fragment contributions,' <i>J. Med. Chem.</i>, vol. 43, pp. 3714–3717, 2000.",
        "[17] F. Lovering et al., 'Escape from Flatland: increasing saturation as an approach to improving clinical success,' <i>J. Med. Chem.</i>, vol. 52, pp. 6752–6756, 2009.",
        "[18] S. Riniker and G. A. Landrum, 'Better informed distance geometry: using knowledge-based torsion angle potentials,' <i>J. Chem. Inf. Model.</i>, vol. 55, pp. 2562–2574, 2015.",
        "[19] T. A. Halgren, 'Merck molecular force field. I. Basis, form, scope, and performance of MMFF94,' <i>J. Comput. Chem.</i>, vol. 17, pp. 490–519, 1996.",
        "[20] J. Bajorath, 'Integration of virtual and high-throughput screening,' <i>Nature Reviews Drug Discovery</i>, vol. 1, no. 11, pp. 882–894, 2002.",
        "[21] J. Vamathevan et al., 'Applications of machine learning in drug discovery and development,' <i>Nature Reviews Drug Discovery</i>, vol. 18, pp. 463–477, 2019.",
        "[22] M. T. Ribeiro, S. Singh, and C. Guestrin, ''Why should I trust you?': Explaining the predictions of any classifier,' <i>ACM SIGKDD</i>, pp. 1135–1144, 2016.",
        "[23] L. S. Shapley, 'A value for n-person games,' <i>Contributions to the Theory of Games</i>, vol. 2, no. 28, pp. 307–317, 1953.",
        "[24] S. V. Sharma, D. W. Bell, J. Settleman, and D. A. Haber, 'Epidermal growth factor receptor mutations in lung cancer,' <i>Nature Reviews Cancer</i>, vol. 7, pp. 169–181, 2007."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle("RefStyle", fontName="Helvetica", fontSize=7.8, leading=10.5, textColor=colors.HexColor("#1e293b"), spaceAfter=3.5)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Updated Academic Project Report PDF generated at: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_full_pdf()
