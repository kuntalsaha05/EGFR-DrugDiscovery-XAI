"""
Generates the Comprehensive Academic Research Monograph (>= 20 Pages)
Adhering to Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune guidelines
for the course: AI SYSTEMS AND APPLICATIONS
Guide: Dr. Devendra Joshi
Authors:
  - Kuntal Saha (PRN: 1262242342)
  - Kalpana Bishnoi (PRN: 1262242386)
  - Saloni Bhongle (PRN: 1262242338)

Formatted for pure academic presentation with zero tofu glyphs, zero black boxes,
clean RGB figures, and crisp typography across all 22 pages.
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

# Image assets
LOGO_PNG = os.path.join(CURRENT_DIR, "mit_wpu_logo.png")
FIG1_PNG = os.path.join(CURRENT_DIR, "fig1_pipeline_architecture.png")
FIG2_PNG = os.path.join(CURRENT_DIR, "fig2_gefitinib_structure.png")
FIG3_PNG = os.path.join(CURRENT_DIR, "fig3_shap_highlight_map.png")
FIG4_PNG = os.path.join(CURRENT_DIR, "fig4_roc_curves.png")
FIG5_PNG = os.path.join(CURRENT_DIR, "fig5_radar_druglikeness.png")
FIG6_PNG = os.path.join(CURRENT_DIR, "fig6_similarity_benchmark.png")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw running headers and total page numbers."""
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
        # Suppress running header on title page
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#475569"))
            
            # Running Header
            self.drawString(54, 802, "MIT-WPU PUNE | AI SYSTEMS & APPLICATIONS | EGFR VIRTUAL SCREENING RESEARCH REPORT")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 796, 541, 796)
            
            # Running Footer
            self.line(54, 46, 541, 46)
            self.drawString(54, 34, "Dr. Vishwanath Karad MIT World Peace University - Guide: Dr. Devendra Joshi")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(541, 34, page_text)
            self.restoreState()


def generate_monograph_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    # Custom Typography Styles
    title_univ = ParagraphStyle(
        "UnivTitle",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0f172a")
    )
    title_sub = ParagraphStyle(
        "SubTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=19,
        alignment=1,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=12
    )
    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5
    )
    body_bold = ParagraphStyle(
        "BodyDarkBold",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#0f172a")
    )
    h1_style = ParagraphStyle(
        "H1Heading",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "H2Heading",
        fontName="Helvetica-Bold",
        fontSize=9.8,
        leading=13.5,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    caption_style = ParagraphStyle(
        "CaptionStyle",
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#475569"),
        spaceBefore=3,
        spaceAfter=6
    )
    center_p = ParagraphStyle(
        "CenterP",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#1e293b")
    )
    code_p = ParagraphStyle(
        "CodeP",
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    
    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE (OFFICIAL MIT-WPU LOGO & TEAM DETAILS)
    # =========================================================================
    story.append(Spacer(1, 15))
    if os.path.exists(LOGO_PNG):
        story.append(Image(LOGO_PNG, width=330, height=88))
        story.append(Spacer(1, 16))
    
    story.append(Paragraph("<b>Dr. Vishwanath Karad MIT WORLD PEACE UNIVERSITY, PUNE</b>", title_univ))
    story.append(Spacer(1, 14))
    story.append(Paragraph("A MINI PROJECT REPORT ON", ParagraphStyle("Cap", fontName="Helvetica-Bold", fontSize=10, alignment=1, spaceAfter=6, textColor=colors.HexColor("#475569"))))
    story.append(Paragraph("<b>EXPLAINABLE AI-BASED DRUG DISCOVERY ASSISTANT FOR EARLY MOLECULAR SCREENING</b>", title_sub))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>Submitted in partial fulfillment of the requirements for the course</i><br/><b>AI SYSTEMS AND APPLICATIONS</b>", center_p))
    story.append(Spacer(1, 26))
    
    cand_info = [
        [Paragraph("<b>Submitted by:</b>", body_style), Paragraph("<b>Under the Guidance of:</b>", body_style)],
        [Paragraph("<b>Kuntal Saha</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(PRN: <b>1262242342</b>)<br/><b>Kalpana Bishnoi</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(PRN: <b>1262242386</b>)<br/><b>Saloni Bhongle</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(PRN: <b>1262242338</b>)", body_style),
         Paragraph("<b>Dr. Devendra Joshi</b><br/>Department of Artificial Intelligence & Data Science,<br/>School of Computer Science & Engineering,<br/>Dr. Vishwanath Karad MIT World Peace University", body_style)]
    ]
    t_cand = Table(cand_info, colWidths=[240, 240])
    t_cand.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0)
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 45))
    
    story.append(Paragraph("<b>Department of Artificial Intelligence and Data Science<br/>School of Computer Science and Engineering<br/>Dr. Vishwanath Karad MIT World Peace University</b><br/>Paud Road, Kothrud, Pune, Maharashtra - 411 038, India<br/><b>Academic Year: 2026-2027</b>", center_p))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & RESEARCH SUMMARY
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    
    toc_data = [
        [Paragraph("<b>Section</b>", body_style), Paragraph("<b>Research Topic / Chapter Title</b>", body_style), Paragraph("<b>Page</b>", body_style)],
        [Paragraph("-", body_style), Paragraph("Title Page (Authors, Affiliations, MIT-WPU Pune)", body_style), Paragraph("1", body_style)],
        [Paragraph("-", body_style), Paragraph("Table of Contents & Research Summary", body_style), Paragraph("2", body_style)],
        [Paragraph("-", body_style), Paragraph("Abstract & Index Terms (Comprehensive Summary)", body_style), Paragraph("3", body_style)],
        [Paragraph("Section I", body_style), Paragraph("Introduction & Research Motivation (Drug Discovery Economics)", body_style), Paragraph("4", body_style)],
        [Paragraph("Section I (cont.)", body_style), Paragraph("System Pipeline Architecture & Figure 1 Block Diagram", body_style), Paragraph("5", body_style)],
        [Paragraph("Section II", body_style), Paragraph("Related Work & Literature Review (QSAR, Soft Computing & XAI)", body_style), Paragraph("6", body_style)],
        [Paragraph("Section III", body_style), Paragraph("Biological Target & ChEMBL203 Bioactivity Curation Protocol", body_style), Paragraph("7", body_style)],
        [Paragraph("Section IV", body_style), Paragraph("Multi-Scale Chemoinformatics Featurization (ECFP4 & Descriptors)", body_style), Paragraph("8", body_style)],
        [Paragraph("Section IV (cont.)", body_style), Paragraph("3D Conformation via MMFF94 & Figure 2 (Gefitinib Structure)", body_style), Paragraph("9", body_style)],
        [Paragraph("Section V", body_style), Paragraph("Supervised Ensemble Classifier Formulation (RF & GBDT)", body_style), Paragraph("10", body_style)],
        [Paragraph("Section VI", body_style), Paragraph("Game-Theoretic Explainability (TreeSHAP Mathematical Formulation)", body_style), Paragraph("11", body_style)],
        [Paragraph("Section VI (cont.)", body_style), Paragraph("Atom-Level Attribution Algorithm & Figure 3 (SHAP Map)", body_style), Paragraph("12", body_style)],
        [Paragraph("Section VII", body_style), Paragraph("Oral Drug-Likeness Profiling (Lipinski's Rule of 5 & Veber Rules)", body_style), Paragraph("13", body_style)],
        [Paragraph("Section VII (cont.)", body_style), Paragraph("Bioavailability Radar Profile & Figure 5 (Polar Radar Plot)", body_style), Paragraph("14", body_style)],
        [Paragraph("Section VIII", body_style), Paragraph("Clinical Homology Benchmarking & Figure 6 (Tanimoto Similarity)", body_style), Paragraph("15", body_style)],
        [Paragraph("Section IX", body_style), Paragraph("Software Implementation, Herbarium UI & Local Ollama LLM Tutor", body_style), Paragraph("16", body_style)],
        [Paragraph("Section X", body_style), Paragraph("Experimental Results & Empirical Test Set Benchmark Metrics", body_style), Paragraph("17", body_style)],
        [Paragraph("Section X (cont.)", body_style), Paragraph("Figure 4 (Holdout ROC Curves) & In-Depth Case Studies", body_style), Paragraph("18", body_style)],
        [Paragraph("Section XI", body_style), Paragraph("University AI Syllabus Alignment (Units I to V Comprehensive Mapping)", body_style), Paragraph("19", body_style)],
        [Paragraph("Section XII", body_style), Paragraph("Discussion, Computational Speedup & Critical Limitations", body_style), Paragraph("20", body_style)],
        [Paragraph("Section XIII", body_style), Paragraph("Conclusion & Future Scope (3D GNNs & De Novo Design)", body_style), Paragraph("21", body_style)],
        [Paragraph("Section XIV", body_style), Paragraph("References (24 Peer-Reviewed Academic Citations in IEEE Format)", body_style), Paragraph("22", body_style)]
    ]
    t_toc = Table(toc_data, colWidths=[65, 360, 40])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2)
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ABSTRACT & INDEX TERMS (> 350 WORDS)
    # =========================================================================
    story.append(Paragraph("ABSTRACT & INDEX TERMS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=10))
    story.append(Paragraph("Traditional pharmaceutical drug discovery is an extraordinarily costly, labor-intensive, and protracted endeavor, typically spanning 10 to 15 years and requiring capital investments exceeding $2 billion per approved therapeutic entity. A predominant cause of this severe developmental attrition is the late-stage failure of candidate chemical compounds during preclinical animal trials and human clinical phases, largely attributable to inadequate target binding affinity, off-target cellular toxicity, or poor oral pharmacokinetics. In classical High-Throughput Screening (HTS), pharmaceutical laboratories empirically assay millions of physical chemical compounds against disease proteins, consuming vast quantities of expensive biological reagents and technician hours.", body_style))
    story.append(Paragraph("This mini-project for <b>AI Systems and Applications</b>, conducted under the guidance of <b>Dr. Devendra Joshi</b> at <b>MIT World Peace University (MIT-WPU), Pune</b> by <b>Kuntal Saha (1262242342), Kalpana Bishnoi (1262242386), and Saloni Bhongle (1262242338)</b>, introduces <b>EGFR Molecular Intelligence</b>, an end-to-end, interpretable computational framework for early-stage Virtual High-Throughput Screening (vHTS). The application specifically targets <b>Human Epidermal Growth Factor Receptor (EGFR / ErbB-1, ChEMBL ID: CHEMBL203)</b>, a transmembrane receptor tyrosine kinase whose hyper-activation drives oncogenic proliferation in Non-Small Cell Lung Cancer (NSCLC) and Glioblastoma.", body_style))
    story.append(Paragraph("By training on a curated benchmark of 881 small-molecule bioactivity assays extracted from the EMBL-EBI ChEMBL database, the platform translates raw chemical representations (SMILES notation) into composite 2,056-dimensional numerical feature spaces combining <b>2048-bit Extended Connectivity Circular Fingerprints (ECFP4)</b> with 8 physicochemical property descriptors. Supervised ensemble models (Random Forest and Gradient Boosted Decision Trees) achieved exceptional predictive performance on a holdout test set with test accuracies of <b>90.96%</b> and <b>91.53%</b>, and Area Under the ROC Curve (<b>ROC-AUC</b>) metrics of <b>0.978</b> and <b>0.968</b>, respectively.", body_style))
    story.append(Paragraph("To resolve the opaque 'black-box' dilemma that historically impedes clinician and chemist trust in biomedical AI, the platform incorporates <b>Explainable AI (XAI)</b> based on <b>TreeSHAP (SHapley Additive exPlanations)</b> cooperative game theory. The system computes exact polynomial-time Shapley attributions and projects them directly onto 2D molecular graphs, highlighting favorable binding anchors in fluorescent chartreuse and unfavorable steric penalties in crimson. The platform additionally assesses oral drug-likeness via <b>Lipinski's Rule of Five</b> and <b>Veber's rules</b>, computes <b>Tanimoto structural similarity</b> against FDA-approved cancer drugs (Gefitinib, Erlotinib, Osimertinib), embeds an offline <b>Ollama Large Language Model (LLM)</b> chemoinformatics tutor, and compiles automated vector PDF screening dossiers via ReportLab.", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>INDEX TERMS:</b> Explainable AI (XAI), Artificial Intelligence Systems, Virtual Screening, Epidermal Growth Factor Receptor (EGFR), Human ChEMBL203, TreeSHAP, RDKit, Random Forest, Gradient Boosting, Morgan Fingerprints (ECFP4), Lipinski Rule of Five, MIT-WPU Pune.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SECTION I: INTRODUCTION & RESEARCH MOTIVATION
    # =========================================================================
    story.append(Paragraph("SECTION I: INTRODUCTION & RESEARCH MOTIVATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("1.1 The Economics of Modern Drug Discovery", h2_style))
    story.append(Paragraph("The translation of a novel chemical entity into an FDA-approved medicine requires synthesizing thousands of structural analogues. In wet-lab High-Throughput Screening (HTS), microtiter plates are filled with biological enzymes and candidate ligands, testing compounds blindly. The cost per assay ranges from $10 to $500 per compound, accumulating millions in early exploratory budgets with an overall clinical attrition rate exceeding 90%. Virtual screening through Machine Learning acts as an intelligent computational filter: by analyzing structural features <i>in silico</i>, AI models rank chemical libraries within milliseconds, eliminating non-binding molecules before physical laboratory synthesis.", body_style))
    
    story.append(Paragraph("1.2 Oncogenic EGFR Kinase in Lung Cancer", h2_style))
    story.append(Paragraph("The Epidermal Growth Factor Receptor (EGFR) is an established therapeutic oncogene. In Non-Small Cell Lung Cancer (NSCLC), which represents 85% of all lung cancer occurrences, somatic in-frame deletions in exon 19 and the L858R point mutation in exon 21 constitutively activate the receptor kinase domain, driving the pro-survival MAPK and PI3K/Akt signaling cascades. Small-molecule Tyrosine Kinase Inhibitors (TKIs) such as Gefitinib bind reversibly to the adenosine triphosphate (ATP) cleft. However, secondary gatekeeper mutations like T790M and tertiary resistance mutations like C797S emerge, necessitating continuous computational screening for novel inhibitory chemotypes.", body_style))
    
    story.append(Paragraph("1.3 The Black-Box Challenge in Biomedical AI", h2_style))
    story.append(Paragraph("Although modern deep neural networks and ensemble classifiers produce high predictive accuracy on chemoinformatics benchmarks, their clinical adoption has been stalled by opacity. A medicinal chemist cannot utilize an uninterpretable score of '98% probability' without knowing which specific functional groups or atomic clusters mediate the interaction. Without rational structural explanation, researchers cannot perform guided lead optimization. This research resolves this fundamental challenge by embedding cooperative game-theoretic explainability directly into the inference pipeline.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SECTION I (CONT.): FIGURE 1 & RESEARCH CONTRIBUTIONS
    # =========================================================================
    story.append(Paragraph("SECTION I (CONT.): SYSTEM ARCHITECTURE & CONTRIBUTIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("1.4 End-to-End Architectural Pipeline", h2_style))
    story.append(Paragraph("The platform is engineered as a unified five-tier pipeline executing chemical input ingestion, 3D conformation, multi-scale featurization, supervised ensemble classification, TreeSHAP attribution, and clinical dossier compilation:", body_style))
    
    if os.path.exists(FIG1_PNG):
        story.append(Image(FIG1_PNG, width=460, height=184))
        story.append(Paragraph("<b>Fig 1:</b> End-to-End Explainable Virtual Screening Architecture for Human EGFR (CHEMBL203).", caption_style))
    
    story.append(Paragraph("1.5 Summary of Key Contributions", h2_style))
    story.append(Paragraph("1. <b>Curated Benchmark Dataset:</b> Harvested and curated 881 bioactivity assays for Human EGFR from ChEMBL203, establishing an empirical IC<sub>50</sub> &lt;= 1,000 nM active boundary.<br/>2. <b>High-Performance Ensembles:</b> Trained Random Forest and Gradient Boosting classifiers achieving 90.96% accuracy and 0.978 ROC-AUC with zero synthetic data leakage.<br/>3. <b>Atom-Level XAI Mapping:</b> Formulated an algorithm mapping TreeSHAP polynomial feature attributions to 2D chemical graphs, displaying favorable anchors and steric penalties.<br/>4. <b>Multi-Property Oral Bioavailability:</b> Integrated Lipinski Rule of Five and Veber scorecards with interactive polar radar profiling.<br/>5. <b>Offline Conversational Tutor & PDF Engine:</b> Deployed a local Ollama LLM tutor and ReportLab automated dossier compiler within an editorial dark UI.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SECTION II: RELATED WORK & LITERATURE REVIEW
    # =========================================================================
    story.append(Paragraph("SECTION II: RELATED WORK & LITERATURE REVIEW", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("2.1 Evolution of Quantitative Structure-Activity Relationships", h2_style))
    story.append(Paragraph("Classical QSAR models, introduced by Corwin Hansch in 1962, correlated biological activity with linear combinations of lipophilicity (LogP) and electronic parameters. During the 1990s, Structure-Based Drug Design (SBDD) emerged with molecular docking programs such as AutoDock and Glide. However, physical docking simulations require extensive compute time, are sensitive to receptor flexibility, and struggle to estimate solvent entropy accurately. Machine learning-driven Ligand-Based Virtual Screening (LBVS) offers a compelling alternative by learning complex non-linear decision boundaries directly from empirical bioactivity repositories.", body_style))
    
    story.append(Paragraph("2.2 Soft Computing in Bioinformatics: Prof. Sanghamitra Bandyopadhyay", h2_style))
    story.append(Paragraph("The application of soft computing, genetic algorithms, and supervised ensemble learning to bioinformatics has been extensively championed by computational pioneers such as <b>Prof. Sanghamitra Bandyopadhyay</b> (Director, Indian Statistical Institute, Kolkata). Her research demonstrated that biological datasets (characterized by high dimensionality, severe noise, and complex non-linear feature interactions) cannot be modeled by rigid parametric assumptions. Her work on multi-objective optimization laid the mathematical framework for handling structural uncertainty in biological sequence analysis and biomarker discovery.", body_style))
    
    story.append(Paragraph("2.3 Explainable Artificial Intelligence in Healthcare", h2_style))
    story.append(Paragraph("In response to model opacity, Explainable AI has emerged as an indispensable requirement in biomedical systems. Ribeiro et al. (KDD 2016) proposed LIME (Local Interpretable Model-agnostic Explanations), which fits local surrogate linear models around individual predictions. In 2017, Scott Lundberg and Su-In Lee proposed SHAP, uniting cooperative game theory with additive feature attribution. In 2020, Lundberg et al. published TreeSHAP, enabling exact polynomial-time evaluation for tree ensembles. However, prevailing literature rarely projects abstract fingerprint bits back onto physical 2D chemical structures.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: SECTION III: BIOLOGICAL TARGET & DATASET CURATION
    # =========================================================================
    story.append(Paragraph("SECTION III: BIOLOGICAL TARGET & DATASET CURATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("3.1 Human EGFR Tyrosine Kinase Anatomy", h2_style))
    story.append(Paragraph("Human EGFR (erbB-1) is a 170 kDa transmembrane glycoprotein. The intracellular kinase domain (residues 690-953) contains an N-terminal lobe primarily consisting of five-stranded beta-sheets and the regulatory alphaC-helix, and a larger C-terminal lobe consisting mainly of alpha-helices. Adenosine triphosphate (ATP) binds in the deep cleft between the two lobes. Tyrosine kinase inhibitors (TKIs) act by mimicking the adenine ring of ATP, inserting into the nucleotide cleft and forming hydrogen bonds with the hinge region backbone residue <b>Met793</b>.", body_style))
    
    story.append(Paragraph("3.2 ChEMBL203 Bioactivity Extraction & Normalization", h2_style))
    story.append(Paragraph("Bioactivity records for target identifier <b>CHEMBL203</b> were harvested using the official EMBL-EBI REST API. The curation workflow enforces the following criteria:<br/>1. <b>Assay Filter:</b> Retained only biochemical binding affinity assays where the standard measurement type is strictly equal to half-maximal inhibitory concentration (IC<sub>50</sub>) measured in nanomolar (nM).<br/>2. <b>Logarithmic Conversion (pIC<sub>50</sub>):</b> Converted absolute concentrations into standard logarithmic potency: <b>pIC<sub>50</sub> = 9 - log<sub>10</sub>(IC<sub>50</sub>)</b>.<br/>3. <b>Binary Classification Threshold:</b> Compounds with IC<sub>50</sub> &lt;= 1,000 nM (pIC<sub>50</sub> &gt;= 6.0) are classified as Active (y=1), denoting micromolar potency. Compounds with IC<sub>50</sub> &gt;= 10,000 nM (pIC<sub>50</sub> &lt;= 5.0) are classified as Inactive (y=0). Compounds in the ambiguous boundary zone (1,000 nM &lt; IC<sub>50</sub> &lt; 10,000 nM) were removed to eliminate label noise.<br/>4. <b>Chemical Hygiene:</b> SMILES were canonicalized in RDKit. Inorganic salts, counter-ions, and solvent fragments were stripped. Duplicate canonical SMILES were resolved by averaging replicate pIC<sub>50</sub> values.<br/>The final benchmark contains <b>881 curated chemical compounds</b> (472 Actives, 409 Inactives).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SECTION IV: MULTI-SCALE CHEMOINFORMATICS FEATURIZATION
    # =========================================================================
    story.append(Paragraph("SECTION IV: MULTI-SCALE CHEMOINFORMATICS FEATURIZATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("4.1 Extended Connectivity Circular Fingerprints (ECFP4)", h2_style))
    story.append(Paragraph("Molecules are modeled as undirected topological graphs G = (V, E), where vertices V represent heavy atoms and edges E represent covalent bonds. The Morgan algorithm applies iterative circular neighborhood hashing up to radius r = 2 (representing chemical path diameters of 4 bonds):", body_style))
    story.append(Paragraph("<b>ID_v^(r) = Hash( ID_v^(r-1), SUM [ BondOrder(v, u), ID_u^(r-1) ] )</b>", center_p))
    story.append(Paragraph("The resulting integer identifiers are folded into a sparse binary bit vector of length <b>2,048 bits</b> using modulo arithmetic. Bit j = 1 signifies the presence of a specific pharmacophoric substructure.", body_style))
    
    story.append(Paragraph("4.2 Physicochemical Molecular Descriptors", h2_style))
    story.append(Paragraph("To complement topological fingerprints with whole-molecule bulk properties, 8 standardized physicochemical descriptors are calculated via RDKit:", body_style))
    
    desc_tbl = [
        [Paragraph("<b>Descriptor</b>", body_style), Paragraph("<b>Property & Units</b>", body_style), Paragraph("<b>Clinical Role in Drug Discovery</b>", body_style)],
        [Paragraph("MolWt", body_style), Paragraph("Molecular Weight (Da)", body_style), Paragraph("Steric cavity fit, passive membrane diffusion", body_style)],
        [Paragraph("MolLogP", body_style), Paragraph("Wildman-Crippen LogP", body_style), Paragraph("Lipophilicity, gut absorption, membrane partition", body_style)],
        [Paragraph("TPSA", body_style), Paragraph("Polar Surface Area (A<sup>2</sup>)", body_style), Paragraph("Transcellular permeability, blood-brain barrier transport", body_style)],
        [Paragraph("NumHDonors", body_style), Paragraph("Count of -OH / -NH", body_style), Paragraph("Directional hydrogen-bond donors with kinase residues", body_style)],
        [Paragraph("NumHAcceptors", body_style), Paragraph("Count of -O- / -N-", body_style), Paragraph("Hydrogen-bond acceptors interacting in ATP pocket", body_style)],
        [Paragraph("NumRotBonds", body_style), Paragraph("Rotatable Single Bonds", body_style), Paragraph("Conformational flexibility; excess flexibility penalizes entropy", body_style)],
        [Paragraph("QED", body_style), Paragraph("Drug-likeness score [0, 1]", body_style), Paragraph("Desirability index combining 8 physical properties", body_style)],
        [Paragraph("FractionCSP3", body_style), Paragraph("Ratio of sp<sup>3</sup> carbons", body_style), Paragraph("Molecular 3D saturation; correlates with clinical success", body_style)]
    ]
    t_d = Table(desc_tbl, colWidths=[80, 140, 260])
    t_d.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5)
    ]))
    story.append(t_d)
    story.append(Spacer(1, 6))
    story.append(Paragraph("The 8 descriptors are scaled using StandardScaler (mean=0, variance=1) and concatenated with the 2048-bit fingerprint vector, yielding a comprehensive composite feature vector <b>x in R<sup>2056</sup></b>.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SECTION IV (CONT.): 3D CONFORMATION & FIGURE 2
    # =========================================================================
    story.append(Paragraph("SECTION IV (CONT.): 2D/3D GEOMETRY & MMFF94 MINIMIZATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("4.3 Energy-Minimized 3D Conformation Engine", h2_style))
    story.append(Paragraph("Planar 2D representations cannot illustrate spatial steric constraints within the ATP pocket. The platform employs the ETKDGv3 (Experimental-Torsion Knowledge-based Distance Geometry) algorithm to embed atoms in 3D Euclidean space. Initial coordinates undergo iterative energy minimization using the <b>Merck Molecular Force Field 1994 (MMFF94)</b>:", body_style))
    story.append(Paragraph("<b>E_total = E_str + E_ang + E_tor + E_oop + E_vdW + E_elec</b>", center_p))
    story.append(Paragraph("Minimized atomic Cartesian coordinates are serialized into standard `.mol` blocks and rendered in real-time WebGL via `py3Dmol`.", body_style))
    
    if os.path.exists(FIG2_PNG):
        story.append(Image(FIG2_PNG, width=380, height=253))
        story.append(Paragraph("<b>Fig 2:</b> 2D Vector Chemical Architecture of Gefitinib (Iressa) generated via RDKit.", caption_style))
    
    story.append(Paragraph("The molecular framework reveals the 4-anilinoquinazoline core, the 3-chloro-4-fluoroaniline pharmacophore, and the flexible morpholine ether side-chain responsible for high water solubility.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SECTION V: SUPERVISED ENSEMBLE CLASSIFIERS
    # =========================================================================
    story.append(Paragraph("SECTION V: SUPERVISED ENSEMBLE CLASSIFIERS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("5.1 Random Forest Classifier Formulation", h2_style))
    story.append(Paragraph("Random Forest builds an ensemble of B = 100 decorrelated decision trees using bootstrap aggregating (bagging). At each candidate split, a random subset of m = sqrt(M) features is sampled. For classification, the final binding probability is the consensus average:", body_style))
    story.append(Paragraph("<b>P(y = 1 | x) = (1 / B) * SUM[ T_b(x) ]</b>", center_p))
    story.append(Paragraph("Random Forests are exceptionally resilient against overfitting on high-dimensional sparse binary vectors like Morgan fingerprints, providing stable variance reduction.", body_style))
    
    story.append(Paragraph("5.2 Gradient Boosted Decision Trees (GBDT) Formulation", h2_style))
    story.append(Paragraph("Gradient Boosting constructs an additive model in a forward stage-wise manner by minimizing binary cross-entropy loss:", body_style))
    story.append(Paragraph("<b>L(y, p) = - [ y * log(p) + (1 - y) * log(1 - p) ]</b>", center_p))
    story.append(Paragraph("At step m, a shallow regression tree h_m(x) is fit to the pseudo-residuals of the existing ensemble. The updated model is:", body_style))
    story.append(Paragraph("<b>F_m(x) = F_{m-1}(x) + eta * h_m(x)</b>", center_p))
    story.append(Paragraph("where eta = 0.1 is the learning rate (shrinkage parameter). GBDT excels at discovering complex non-linear interaction thresholds between continuous descriptors.", body_style))
    
    story.append(Paragraph("5.3 Stratified Training & Validation Setup", h2_style))
    story.append(Paragraph("The 881 curated compounds are split into an 80% training set (704 compounds) and a 20% holdout test set (177 compounds) using stratified sampling on label y. Feature scalers are fit strictly on training samples to prevent information leakage.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: SECTION VI: GAME-THEORETIC EXPLAINABILITY (TREESHAP)
    # =========================================================================
    story.append(Paragraph("SECTION VI: GAME-THEORETIC EXPLAINABILITY (TREESHAP)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("6.1 Shapley Value Axiomatic Foundation", h2_style))
    story.append(Paragraph("Originating from Lloyd Shapley's cooperative game theory (1953), Shapley values represent the unique payout allocation method that satisfies four fundamental mathematical axioms: Efficiency, Symmetry, Dummy (Null player), and Additivity. The marginal contribution of feature i across all possible feature subsets S is:", body_style))
    story.append(Paragraph("<b>phi_i(v) = SUM [ |S|! (|N| - |S| - 1)! / |N|! ] * [ v(S U {i}) - v(S) ]</b>", center_p))
    story.append(Paragraph("In our virtual screening framework, players N correspond to the 2,056 input molecular variables, the game payout v(S) is the model's predicted probability P(Active), and phi_i quantifies the positive or negative contribution of feature i toward the classification decision.", body_style))
    
    story.append(Paragraph("6.2 Polynomial-Time TreeSHAP Algorithm", h2_style))
    story.append(Paragraph("While model-agnostic KernelSHAP requires exponential sampling O(2^|N|), Lundberg's TreeSHAP algorithm evaluates exact conditional expectations by tracking feature paths through decision tree branches in polynomial time O(T * L * D<sup>2</sup>), where T is tree count, L is maximum leaves, and D is maximum depth. This enables instantaneous sub-second explainability in interactive clinical web applications.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: SECTION VI (CONT.): ATOM ATTRIBUTION ALGORITHM & FIG 3
    # =========================================================================
    story.append(Paragraph("SECTION VI (CONT.): ATOM-LEVEL ATTRIBUTION & FIGURE 3", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("6.3 Spatial Substructure Projection Algorithm", h2_style))
    story.append(Paragraph("Because Morgan fingerprints represent localized atomic neighborhoods, our platform maps computed Shapley values back to physical atom coordinates using RDKit's bitInfo dictionary:<br/>1. For each active fingerprint bit j with Shapley value phi_j, the central atom index v and radius r are retrieved.<br/>2. The attribution is allocated across spatial coordinates: <b>AtomScore(v) = SUM[ phi_j * w(r) ]</b>.<br/>3. Normalized atom scores are mapped to visual highlights:<br/>- <b>Chartreuse Highlights (phi &gt; 0):</b> Positive binding anchors enhancing EGFR inhibition.<br/>- <b>Crimson Highlights (phi &lt; 0):</b> Unfavorable steric or electrostatic penalties.", body_style))
    
    if os.path.exists(FIG3_PNG):
        story.append(Image(FIG3_PNG, width=380, height=253))
        story.append(Paragraph("<b>Fig 3:</b> Atom-Level SHAP Highlight Map for Gefitinib. Chartreuse regions denote favorable hinge-binding pharmacophores.", caption_style))
    
    story.append(Paragraph("This spatial visualization immediately confirms that the quinazoline ring and aniline nitrogen function as primary binding anchors, matching known structural biology.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: SECTION VII: ORAL DRUG-LIKENESS & ADMET PROFILING
    # =========================================================================
    story.append(Paragraph("SECTION VII: ORAL DRUG-LIKENESS & ADMET PROFILING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("7.1 Lipinski's Rule of Five Heuristic", h2_style))
    story.append(Paragraph("Christopher Lipinski (2001) established that poor oral absorption is significantly more likely when a molecule violates more than one of the following four physicochemical parameters:", body_style))
    story.append(Paragraph("1. <b>Molecular Weight (MolWt) &lt;= 500 Da:</b> Bulky molecules cannot passively cross intestinal epithelial membranes.<br/>2. <b>Lipophilicity (MolLogP) &lt;= 5.0:</b> Highly lipophilic molecules exhibit poor aqueous solubility and high metabolic clearance.<br/>3. <b>Hydrogen Bond Donors (HBD) &lt;= 5:</b> Excessive -OH and -NH groups incur high desolvation energy penalties when entering lipid bilayers.<br/>4. <b>Hydrogen Bond Acceptors (HBA) &lt;= 10:</b> Excessive electronegative atoms hinder passive membrane permeability.", body_style))
    
    story.append(Paragraph("7.2 Veber's Oral Bioavailability Rules", h2_style))
    story.append(Paragraph("Daniel Veber (2002) identified that molecular flexibility and polar surface area dictate oral bioavailability in rats and humans:", body_style))
    story.append(Paragraph("- <b>Rotatable Bonds &lt;= 10:</b> Highly flexible molecules suffer entropic penalties upon target binding and show reduced intestinal permeation.<br/>- <b>Topological Polar Surface Area (TPSA) &lt;= 140 A<sup>2</sup>:</b> Polar surface areas exceeding 140 A<sup>2</sup> correlate with poor cellular permeability.", body_style))
    
    story.append(Paragraph("7.3 Multi-Parameter Evaluation Table", h2_style))
    dl_tab = [
        [Paragraph("<b>Compound</b>", body_style), Paragraph("<b>MolWt</b>", body_style), Paragraph("<b>LogP</b>", body_style), Paragraph("<b>HBD</b>", body_style), Paragraph("<b>HBA</b>", body_style), Paragraph("<b>TPSA</b>", body_style), Paragraph("<b>RotB</b>", body_style), Paragraph("<b>Rule Status</b>", body_style)],
        [Paragraph("Gefitinib", body_style), Paragraph("446.9", body_style), Paragraph("4.28", body_style), Paragraph("1", body_style), Paragraph("7", body_style), Paragraph("68.7", body_style), Paragraph("7", body_style), Paragraph("<b>PASS (0 viol)</b>", body_style)],
        [Paragraph("Erlotinib", body_style), Paragraph("393.4", body_style), Paragraph("3.41", body_style), Paragraph("1", body_style), Paragraph("6", body_style), Paragraph("74.7", body_style), Paragraph("8", body_style), Paragraph("<b>PASS (0 viol)</b>", body_style)],
        [Paragraph("Osimertinib", body_style), Paragraph("499.6", body_style), Paragraph("4.62", body_style), Paragraph("1", body_style), Paragraph("8", body_style), Paragraph("87.3", body_style), Paragraph("9", body_style), Paragraph("<b>PASS (0 viol)</b>", body_style)],
        [Paragraph("Lapatinib", body_style), Paragraph("581.1", body_style), Paragraph("5.38", body_style), Paragraph("2", body_style), Paragraph("7", body_style), Paragraph("114.3", body_style), Paragraph("9", body_style), Paragraph("<b>FAIL (2 viol)</b>", body_style)]
    ]
    t_dl = Table(dl_tab, colWidths=[70, 50, 50, 45, 45, 55, 45, 120])
    t_dl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5)
    ]))
    story.append(t_dl)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: SECTION VII (CONT.): POLAR RADAR PROFILE & FIGURE 5
    # =========================================================================
    story.append(Paragraph("SECTION VII (CONT.): BIOAVAILABILITY RADAR & FIGURE 5", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("7.4 Normalized Bioavailability Radar Profiling", h2_style))
    story.append(Paragraph("To enable immediate visual comprehension, the 6 key oral bioavailability parameters are normalized against their standard upper threshold boundaries (Boundary = 1.0). The query molecule's polygon is superimposed over the threshold limit:", body_style))
    
    if os.path.exists(FIG5_PNG):
        story.append(Image(FIG5_PNG, width=340, height=340))
        story.append(Paragraph("<b>Fig 5:</b> Polar Bioavailability Radar Profile. Green polygon depicts Gefitinib within the red dashed oral boundary.", caption_style))
    
    story.append(Paragraph("Molecules whose green polygon stays completely inside the red boundary satisfy all oral absorption rules without structural modification.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: SECTION VIII: CLINICAL HOMOLOGY & FIGURE 6
    # =========================================================================
    story.append(Paragraph("SECTION VIII: CLINICAL HOMOLOGY & FIGURE 6", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("8.1 Tanimoto Coefficient Formulation", h2_style))
    story.append(Paragraph("The Tanimoto (Jaccard) similarity index between query fingerprint vector A and reference drug vector B is calculated as:", body_style))
    story.append(Paragraph("<b>T_c(A, B) = |A INTERSECT B| / |A UNION B| = c / (a + b - c)</b>", center_p))
    story.append(Paragraph("where c is the number of common bits, and a, b are the active bit counts. Queries are benchmarked against 6 clinically approved EGFR cancer therapeutics:", body_style))
    
    if os.path.exists(FIG6_PNG):
        story.append(Image(FIG6_PNG, width=420, height=245))
        story.append(Paragraph("<b>Fig 6:</b> Tanimoto Similarity Index (%) against FDA-Approved EGFR Tyrosine Kinase Inhibitors.", caption_style))
    
    story.append(Paragraph("Gefitinib matches itself at 100%, exhibits high homology with Erlotinib (52.4%), and diverges from third-generation covalent drugs like Osimertinib (39.2%), while the negative control Aspirin displays only 13.3% background similarity.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: SECTION IX: SYSTEM IMPLEMENTATION & OLLAMA LLM
    # =========================================================================
    story.append(Paragraph("SECTION IX: IMPLEMENTATION, HERBARIUM UI & OLLAMA LLM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("9.1 Herbarium Alpinum Editorial Design System", h2_style))
    story.append(Paragraph("The user interface implements the <b>HERBARIUM ALPINUM - The Edelweiss Folio</b> design system. Built with Streamlit, it abandons generic SaaS aesthetics in favor of a specialized research instrument:<br/>- <b>Base Palette:</b> Near-black base surfaces (#000000, #080e0a) with dark botanical card panels (#101811) and muted forest green borders (#35402f).<br/>- <b>Typography:</b> Pale botanical chalk (#e6e9d9) meeting WCAG 2.2 AA contrast standards (minimum 4.5:1 ratio).<br/>- <b>Interactive Accent:</b> Fluorescent chartreuse (#99ff00) reserved exclusively for active predictions, positive SHAP anchors, and primary actions.", body_style))
    
    story.append(Paragraph("9.2 Local Offline Ollama LLM Chemoinformatics Tutor", h2_style))
    story.append(Paragraph("To democratize chemoinformatics understanding, the system integrates a local offline LLM daemon via Ollama (http://127.0.0.1:11434/api/generate) running gemma3:1b. It ingests real-time descriptors, predictions, and top SHAP drivers into a prompt context, translating complex pharmacology into intuitive explanations for students and non-specialist evaluators.", body_style))
    
    story.append(Paragraph("9.3 Automated ReportLab Vector PDF Engine", h2_style))
    story.append(Paragraph("The platform compiles publication-ready PDF dossiers on demand in under 2 seconds, embedding vector chemical structures, calibrated probabilities, Lipinski rule matrices, and clinical similarity indices.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: SECTION X: EXPERIMENTAL RESULTS & BENCHMARKS
    # =========================================================================
    story.append(Paragraph("SECTION X: EXPERIMENTAL RESULTS & BENCHMARK DISCUSSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("10.1 Empirical Holdout Test Set Performance Metrics", h2_style))
    story.append(Paragraph("Models were trained on 704 compounds and evaluated on a holdout test set of 177 unseen compounds from ChEMBL203:", body_style))
    
    res_table = [
        [Paragraph("<b>Model Classifier</b>", body_style), Paragraph("<b>Accuracy</b>", body_style), Paragraph("<b>Precision</b>", body_style), Paragraph("<b>Recall</b>", body_style), Paragraph("<b>F1-Score</b>", body_style), Paragraph("<b>ROC-AUC</b>", body_style)],
        [Paragraph("Random Forest (RF)", body_style), Paragraph("<b>90.96%</b>", body_style), Paragraph("90.62%", body_style), Paragraph("92.55%", body_style), Paragraph("0.9158", body_style), Paragraph("<b>0.9784</b>", body_style)],
        [Paragraph("Gradient Boosting (GBDT)", body_style), Paragraph("<b>91.53%</b>", body_style), Paragraph("91.67%", body_style), Paragraph("92.55%", body_style), Paragraph("0.9206", body_style), Paragraph("<b>0.9678</b>", body_style)]
    ]
    t_res = Table(res_table, colWidths=[130, 70, 70, 70, 70, 70])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_res)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("10.2 Discussion of Empirical Performance", h2_style))
    story.append(Paragraph("Both classifiers significantly exceed our project target of 0.80 ROC-AUC. Gradient Boosting achieved a slightly higher test accuracy (91.53%) and precision (91.67%), while Random Forest yielded superior discrimination across the full threshold spectrum with an outstanding <b>ROC-AUC of 0.9784</b>. The balanced recall (92.55%) confirms that the models successfully identify active inhibitors while maintaining a very low false-positive rate (&lt; 9.4%).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: SECTION X (CONT.): FIGURE 4 ROC CURVES & CASE STUDIES
    # =========================================================================
    story.append(Paragraph("SECTION X (CONT.): ROC CURVES & IN-DEPTH CASE STUDIES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    
    if os.path.exists(FIG4_PNG):
        story.append(Image(FIG4_PNG, width=320, height=266))
        story.append(Paragraph("<b>Fig 4:</b> Holdout ROC Curves for Random Forest (AUC = 0.978) and Gradient Boosting (AUC = 0.968).", caption_style))
    
    story.append(Paragraph("10.3 Comparative Case Studies: Gefitinib vs. Aspirin", h2_style))
    story.append(Paragraph("- <b>Gefitinib (Approved TKI):</b> Classified Active with <b>P(Active) = 99.8%</b>. Top positive SHAP drivers identified the 4-anilinoquinazoline core (phi = +0.0712) and 3-chloro-4-fluoroaniline moiety (phi = +0.0489), directly matching crystallographic hinge-binding anchors with Met793.<br/>- <b>Aspirin (Negative Control):</b> Classified Inactive with <b>P(Active) = 7.7%</b>. SHAP identified low molecular weight (180 Da) and the negatively charged carboxylate group (phi = -0.0982) as severe penalties, causing electrostatic repulsion with the hydrophobic ATP pocket.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: SECTION XI: UNIVERSITY SYLLABUS ALIGNMENT
    # =========================================================================
    story.append(Paragraph("SECTION XI: AI SYLLABUS ALIGNMENT (UNITS I TO V)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("This mini-project directly maps to the university <b>AI Systems and Applications</b> curriculum:", body_style))
    
    syl_table = [
        [Paragraph("<b>Syllabus Unit</b>", body_style), Paragraph("<b>Curriculum Concept</b>", body_style), Paragraph("<b>Implementation in Proposed Project</b>", body_style)],
        [Paragraph("<b>UNIT-I</b>", body_style), Paragraph("Key Components of AI Systems & Narrow AI", body_style), Paragraph("Implements domain-specific Narrow AI for oncology problem solving; observes bioethics against clinical over-extrapolation.", body_style)],
        [Paragraph("<b>UNIT-II</b>", body_style), Paragraph("ML Frameworks & Supervised Learning", body_style), Paragraph("End-to-end data pipeline using Pandas, NumPy, and Scikit-learn; trained Random Forest and Gradient Boosting ensembles.", body_style)],
        [Paragraph("<b>UNIT-III</b>", body_style), Paragraph("Graph Theory, LLMs & Explainable AI", body_style), Paragraph("Molecules as graphs G=(V,E) via 2048-bit ECFP4 traversal; local Ollama LLM tutor; game-theoretic SHAP TreeExplainer.", body_style)],
        [Paragraph("<b>UNIT-IV</b>", body_style), Paragraph("AI Applications in Healthcare", body_style), Paragraph("Direct precision oncology application targeting EGFR in Non-Small Cell Lung Cancer, drastically reducing wet-lab reagent costs.", body_style)],
        [Paragraph("<b>UNIT-V</b>", body_style), Paragraph("Historical AI Milestones & Case Studies", body_style), Paragraph("Modern parallel to IBM Watson Health, DeepMind AlphaFold, and predictive disease biomarker systems.", body_style)]
    ]
    t_syl = Table(syl_table, colWidths=[65, 145, 270])
    t_syl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5)
    ]))
    story.append(t_syl)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: SECTION XII: DISCUSSION & LIMITATIONS
    # =========================================================================
    story.append(Paragraph("SECTION XII: DISCUSSION, ADVANTAGES & LIMITATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("12.1 Key Technological Advantages", h2_style))
    story.append(Paragraph("1. <b>High Throughput Acceleration:</b> Evaluates compounds <i>in silico</i> in under 50 milliseconds, bypassing months of physical assay preparation.<br/>2. <b>Transparent Lead Optimization:</b> Atom-level SHAP highlights provide chemists with actionable feedback on which functional groups enhance or penalize binding.<br/>3. <b>Concurrent Bioavailability Screening:</b> Evaluates target binding affinity alongside Lipinski and Veber oral absorption heuristics to reject insoluble hits.<br/>4. <b>Complete On-Premise Privacy:</b> The local Ollama LLM and Python inference run entirely offline with zero third-party cloud data exposure.", body_style))
    
    story.append(Paragraph("12.2 Critical Limitations", h2_style))
    story.append(Paragraph("1. <b>2D Graph Topological Invariance:</b> Morgan fingerprints encode 2D circular connectivity but do not explicitly account for flexible protein backbone induced-fit dynamics or quantum mechanical polarization.<br/>2. <b>Binary Potency Discretization:</b> Continuous affinity is binarized (IC<sub>50</sub> &lt;= 1,000 nM vs &gt;= 10,000 nM), omitting weakly active molecules (1,000-10,000 nM).<br/>3. <b>Target Selectivity Boundary:</b> The model is trained on Human EGFR (CHEMBL203) and does not predict broader off-target kinome selectivity across related kinases (HER2, HER4, VEGFR2).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: SECTION XIII: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("SECTION XIII: CONCLUSION & FUTURE SCOPE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    story.append(Paragraph("13.1 Conclusion", h2_style))
    story.append(Paragraph("In this mini-project for <b>AI Systems and Applications</b> at <b>MIT World Peace University (MIT-WPU), Pune</b>, conducted by <b>Kuntal Saha (1262242342), Kalpana Bishnoi (1262242386), and Saloni Bhongle (1262242338)</b> under the mentorship of <b>Dr. Devendra Joshi</b>, an end-to-end, interpretable computational screening assistant, <b>EGFR Molecular Intelligence</b>, was successfully conceptualized, implemented, and empirically verified.", body_style))
    story.append(Paragraph("By combining RDKit chemoinformatics, 2048-bit Morgan circular graph representations, and supervised tree ensemble models, the system achieved <b>90.96% accuracy and 0.978 ROC-AUC</b> on a curated benchmark of 881 ChEMBL compounds. Integrating polynomial TreeSHAP game theory resolved the black-box dilemma by projecting atom-level binding explanations directly onto 2D molecular graphs. Supported by Lipinski oral bioavailability radar charts, clinical Tanimoto similarity indexing, an embedded local Ollama LLM tutor, and automated PDF reporting, this platform demonstrates the transformative power of Explainable AI in precision oncology.", body_style))
    
    story.append(Paragraph("13.2 Future Scope & Research Roadmap", h2_style))
    story.append(Paragraph("- <b>3D Equivariant Graph Neural Networks (EGNN):</b> Incorporate geometric deep learning directly on 3D Cartesian coordinates to capture flexible induced-fit docking dynamics.<br/>- <b>Multi-Target Kinome Selectivity:</b> Expand classifiers across related kinases (HER2, HER4, MET, ALK) to predict polypharmacological safety profiles.<br/>- <b>De Novo Generative Design:</b> Interface the predictive model with Generative Adversarial Networks (GANs) or Reinforcement Learning (RL) for automated de novo hit synthesis.<br/>- <b>Quantitative ADMET Toxicity Models:</b> Integrate predictive models for hERG cardiac channel liability, Ames mutagenicity, and cytochrome P450 clearance.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 22: SECTION XIV: REFERENCES (24 CITATIONS)
    # =========================================================================
    story.append(Paragraph("SECTION XIV: REFERENCES (24 ACADEMIC CITATIONS)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=8))
    refs = [
        "[1] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' <i>NeurIPS</i>, vol. 30, pp. 4765-4774, 2017.",
        "[2] S. M. Lundberg et al., 'From local explanations to global understanding with explainable AI for trees,' <i>Nature Machine Intelligence</i>, vol. 2, pp. 56-67, 2020.",
        "[3] S. Bandyopadhyay and S. Saha, <i>Unsupervised Classification: Similarity Measures and Applications</i>. Springer, 2013.",
        "[4] C. A. Lipinski et al., 'Experimental approaches to estimate solubility and permeability in drug discovery,' <i>Adv. Drug Deliv. Rev.</i>, vol. 46, pp. 3-26, 2001.",
        "[5] D. F. Veber et al., 'Molecular properties that influence the oral bioavailability of drug candidates,' <i>J. Med. Chem.</i>, vol. 45, pp. 2615-2623, 2002.",
        "[6] D. Rogers and M. Hahn, 'Extended-connectivity fingerprints,' <i>J. Chem. Inf. Model.</i>, vol. 50, no. 5, pp. 742-754, 2010.",
        "[7] G. Landrum et al., 'RDKit: Open-source cheminformatics,' <i>GitHub repository</i>, https://github.com/rdkit/rdkit, 2023.",
        "[8] A. Gaulton et al., 'ChEMBL: a large-scale bioactivity database for drug discovery,' <i>Nucleic Acids Res.</i>, vol. 40, pp. D1100-D1107, 2012.",
        "[9] L. Breiman, 'Random Forests,' <i>Machine Learning</i>, vol. 45, no. 1, pp. 5-32, 2001.",
        "[10] J. H. Friedman, 'Greedy function approximation: A gradient boosting machine,' <i>Annals of Statistics</i>, vol. 29, pp. 1189-1232, 2001.",
        "[11] R. Sordella et al., 'Gefitinib-sensitizing EGFR mutations in lung cancer activate selective apoptotic pathways,' <i>Science</i>, vol. 305, pp. 1163-1167, 2004.",
        "[12] D. A. Cross et al., 'AZD9291, an irreversible EGFR TKI, overcomes T790M-mediated resistance,' <i>Cancer Discovery</i>, vol. 4, pp. 1046-1061, 2014.",
        "[13] G. R. Bickerton et al., 'Quantifying the chemical beauty of drugs,' <i>Nature Chemistry</i>, vol. 4, no. 2, pp. 90-98, 2012.",
        "[14] F. Pedregosa et al., 'Scikit-learn: Machine learning in Python,' <i>J. Machine Learning Research</i>, vol. 12, pp. 2825-2830, 2011.",
        "[15] S. A. Wildman and G. M. Crippen, 'Prediction of physicochemical parameters by atomic contributions,' <i>J. Chem. Inf. Comput. Sci.</i>, vol. 39, pp. 868-873, 1999.",
        "[16] P. Ertl et al., 'Fast calculation of molecular polar surface area as a sum of fragment contributions,' <i>J. Med. Chem.</i>, vol. 43, pp. 3714-3717, 2000.",
        "[17] F. Lovering et al., 'Escape from Flatland: increasing saturation as an approach to improving clinical success,' <i>J. Med. Chem.</i>, vol. 52, pp. 6752-6756, 2009.",
        "[18] S. Riniker and G. A. Landrum, 'Better informed distance geometry: using knowledge-based torsion angle potentials,' <i>J. Chem. Inf. Model.</i>, vol. 55, pp. 2562-2574, 2015.",
        "[19] T. A. Halgren, 'Merck molecular force field. I. Basis, form, scope, and performance of MMFF94,' <i>J. Comput. Chem.</i>, vol. 17, pp. 490-519, 1996.",
        "[20] J. Bajorath, 'Integration of virtual and high-throughput screening,' <i>Nature Reviews Drug Discovery</i>, vol. 1, no. 11, pp. 882-894, 2002.",
        "[21] J. Vamathevan et al., 'Applications of machine learning in drug discovery and development,' <i>Nature Reviews Drug Discovery</i>, vol. 18, pp. 463-477, 2019.",
        "[22] M. T. Ribeiro, S. Singh, and C. Guestrin, ''Why should I trust you?': Explaining the predictions of any classifier,' <i>ACM SIGKDD</i>, pp. 1135-1144, 2016.",
        "[23] L. S. Shapley, 'A value for n-person games,' <i>Contributions to the Theory of Games</i>, vol. 2, no. 28, pp. 307-317, 1953.",
        "[24] S. V. Sharma, D. W. Bell, J. Settleman, and D. A. Haber, 'Epidermal growth factor receptor mutations in lung cancer,' <i>Nature Reviews Cancer</i>, vol. 7, pp. 169-181, 2007."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle("RefStyle", fontName="Helvetica", fontSize=7.6, leading=10.2, textColor=colors.HexColor("#1e293b"), spaceAfter=3.2)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Research Monograph PDF generated successfully at: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_monograph_pdf()
