"""
Generates the Comprehensive Academic Research Monograph (>= 20 Pages)
Adhering to Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune guidelines
for the course: AI SYSTEMS AND APPLICATIONS
Guide: Dr. Devendra Joshi
Authors (from Approved Poster):
  - Kalpana Bishnoi (PRN: 1262242386)
  - Kuntal Saha (PRN: 1262242342)
  - Saloni Bhongle (PRN: 1262242338)

Formatted strictly as an academic research paper following journal guidelines:
- Title from approved poster: "AI-POWERED DRUG DISCOVERY FOR EGFR INHIBITORS IN LUNG CANCER"
- Formatted Abstract callout box with cyan accent bar
- Abstract content directly synthesizes the approved poster
- Student names and index terms removed from abstract
- Keywords formatted per journal sample
- Comprehensive in-text citations ([1] to [24]) integrated throughout all sections
- Exact metrics, SHAP bits, and approved drug similarities from poster
- Pure RGB figures with pure white backgrounds (zero black boxes)
- Exactly 22 pages in compiled output.
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

# Image assets (all validated 100% RGB with pure white background)
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
            
            # Running Header (Academic Journal Style)
            self.drawString(54, 802, "MIT-WPU PUNE | AI SYSTEMS & APPLICATIONS | EGFR INHIBITOR DRUG DISCOVERY RESEARCH REPORT")
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
        fontSize=13.5,
        leading=18.5,
        alignment=1,
        textColor=colors.HexColor("#0369a1"),
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=8.9,
        leading=13.3,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5
    )
    body_bold = ParagraphStyle(
        "BodyDarkBold",
        fontName="Helvetica-Bold",
        fontSize=8.9,
        leading=13.3,
        textColor=colors.HexColor("#0f172a")
    )
    h1_style = ParagraphStyle(
        "H1Heading",
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "H2Heading",
        fontName="Helvetica-Bold",
        fontSize=9.6,
        leading=13.2,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    caption_style = ParagraphStyle(
        "CaptionStyle",
        fontName="Helvetica-Oblique",
        fontSize=7.8,
        leading=10.8,
        alignment=1,
        textColor=colors.HexColor("#475569"),
        spaceBefore=3,
        spaceAfter=5
    )
    center_p = ParagraphStyle(
        "CenterP",
        fontName="Helvetica",
        fontSize=8.9,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#1e293b")
    )
    code_p = ParagraphStyle(
        "CodeP",
        fontName="Courier",
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    
    # Abstract Specific Styles
    abstract_heading = ParagraphStyle(
        "AbstractHead",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=6
    )
    abstract_text_style = ParagraphStyle(
        "AbstractText",
        fontName="Helvetica",
        fontSize=8.6,
        leading=12.8,
        alignment=4, # Justified
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )
    keywords_style = ParagraphStyle(
        "KeywordsText",
        fontName="Helvetica",
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor("#0f172a")
    )
    
    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE (OFFICIAL MIT-WPU LOGO & TEAM DETAILS)
    # =========================================================================
    story.append(Spacer(1, 15))
    if os.path.exists(LOGO_PNG):
        story.append(Image(LOGO_PNG, width=330, height=88))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<b>Dr. Vishwanath Karad MIT WORLD PEACE UNIVERSITY, PUNE</b>", title_univ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("A MINI PROJECT REPORT ON", ParagraphStyle("Cap", fontName="Helvetica-Bold", fontSize=9.5, alignment=1, spaceAfter=5, textColor=colors.HexColor("#475569"))))
    story.append(Paragraph("<b>AI-POWERED DRUG DISCOVERY FOR EGFR INHIBITORS IN LUNG CANCER</b><br/><font size=10 color='#475569'>Integrating Cheminformatics, Machine Learning and Explainable AI to Identify Potential Anticancer Compounds</font>", title_sub))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>Submitted in partial fulfillment of the requirements for the course</i><br/><b>AI SYSTEMS AND APPLICATIONS</b>", center_p))
    story.append(Spacer(1, 22))
    
    cand_info = [
        [Paragraph("<b>Submitted by:</b>", body_style), Paragraph("<b>Under the Guidance of:</b>", body_style)],
        [Paragraph("<b>Kalpana Bishnoi</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(PRN: <b>1262242386</b>)<br/><b>Kuntal Saha</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(PRN: <b>1262242342</b>)<br/><b>Saloni Bhongle</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(PRN: <b>1262242338</b>)", body_style),
         Paragraph("<b>Dr. Devendra Joshi</b><br/>Department of Computer Science and Engineering,<br/>Department of Artificial Intelligence & Data Science,<br/>Dr. Vishwanath Karad MIT World Peace University", body_style)]
    ]
    t_cand = Table(cand_info, colWidths=[240, 240])
    t_cand.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0)
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 40))
    
    story.append(Paragraph("<b>Department of Computer Science and Engineering<br/>Department of Artificial Intelligence and Data Science<br/>School of Computer Science and Engineering<br/>Dr. Vishwanath Karad MIT World Peace University</b><br/>Paud Road, Kothrud, Pune, Maharashtra - 411 038, India<br/><b>Academic Year: 2026-2027</b>", center_p))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & RESEARCH SUMMARY
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    
    toc_data = [
        [Paragraph("<b>Section</b>", body_style), Paragraph("<b>Research Topic / Chapter Title</b>", body_style), Paragraph("<b>Page</b>", body_style)],
        [Paragraph("-", body_style), Paragraph("Title Page (Authors, Affiliations, MIT-WPU Pune)", body_style), Paragraph("1", body_style)],
        [Paragraph("-", body_style), Paragraph("Table of Contents & Research Outline", body_style), Paragraph("2", body_style)],
        [Paragraph("-", body_style), Paragraph("Abstract & Keywords (Poster Synthesis & Scope)", body_style), Paragraph("3", body_style)],
        [Paragraph("Section I", body_style), Paragraph("Background & Motivation: Oncogenic EGFR & Drug Discovery Economics", body_style), Paragraph("4", body_style)],
        [Paragraph("Section I (cont.)", body_style), Paragraph("System Pipeline Architecture & Figure 1 Workflow Block Diagram", body_style), Paragraph("5", body_style)],
        [Paragraph("Section II", body_style), Paragraph("Related Work & Literature Review: QSAR, Soft Computing & XAI", body_style), Paragraph("6", body_style)],
        [Paragraph("Section III", body_style), Paragraph("Biological Target Anatomy & ChEMBL203 Bioactivity Curation Protocol", body_style), Paragraph("7", body_style)],
        [Paragraph("Section IV", body_style), Paragraph("Multi-Scale Molecular Featurization: ECFP4 Fingerprints & Descriptors", body_style), Paragraph("8", body_style)],
        [Paragraph("Section IV (cont.)", body_style), Paragraph("2D/3D Molecular Geometry, MMFF94 & Figure 2 Gefitinib Architecture", body_style), Paragraph("9", body_style)],
        [Paragraph("Section V", body_style), Paragraph("Supervised Ensemble Classifiers: Random Forest & Gradient Boosting", body_style), Paragraph("10", body_style)],
        [Paragraph("Section VI", body_style), Paragraph("Game-Theoretic Explainability: TreeSHAP Mathematical Formulation", body_style), Paragraph("11", body_style)],
        [Paragraph("Section VI (cont.)", body_style), Paragraph("Atom-Level Attribution Algorithm & Figure 3 SHAP Highlight Map", body_style), Paragraph("12", body_style)],
        [Paragraph("Section VII", body_style), Paragraph("Oral Drug-Likeness & Bioavailability: Lipinski and Veber Profiles", body_style), Paragraph("13", body_style)],
        [Paragraph("Section VII (cont.)", body_style), Paragraph("Bioavailability Radar Profile & Figure 5 Polar Radar Boundary Plot", body_style), Paragraph("14", body_style)],
        [Paragraph("Section VIII", body_style), Paragraph("Approved Drug Similarity Benchmarking & Figure 6 Tanimoto Analysis", body_style), Paragraph("15", body_style)],
        [Paragraph("Section IX", body_style), Paragraph("Software Implementation: Herbarium UI System & Local Ollama LLM", body_style), Paragraph("16", body_style)],
        [Paragraph("Section X", body_style), Paragraph("Experimental Results & Empirical Holdout Test Set Benchmark Metrics", body_style), Paragraph("17", body_style)],
        [Paragraph("Section X (cont.)", body_style), Paragraph("Figure 4 Holdout ROC Curves & Comparative Oncological Case Studies", body_style), Paragraph("18", body_style)],
        [Paragraph("Section XI", body_style), Paragraph("University AI Syllabus Alignment: Units I to V Curriculum Mapping", body_style), Paragraph("19", body_style)],
        [Paragraph("Section XII", body_style), Paragraph("Discussion, Computational Speedup & Critical Biological Limitations", body_style), Paragraph("20", body_style)],
        [Paragraph("Section XIII", body_style), Paragraph("Conclusion & Future Work: Geometric GNNs & De Novo Design", body_style), Paragraph("21", body_style)],
        [Paragraph("Section XIV", body_style), Paragraph("References (24 Peer-Reviewed Academic Citations in IEEE Format)", body_style), Paragraph("22", body_style)]
    ]
    t_toc = Table(toc_data, colWidths=[65, 360, 40])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.1)
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ABSTRACT & KEYWORDS (POSTER SYNTHESIS, NO NAMES, NO INDEX TERMS)
    # =========================================================================
    story.append(Paragraph("RESEARCH ABSTRACT & SCOPE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=10))
    
    abstract_p1 = "Lung cancer, predominantly Non-Small Cell Lung Cancer (NSCLC), represents a leading cause of cancer-related mortality worldwide, frequently driven by dysregulated overexpression or activating somatic mutations in the Epidermal Growth Factor Receptor (EGFR / ErbB-1). Ligand binding induces receptor dimerization and tyrosine autophosphorylation, hyperactivating downstream MAPK/ERK and PI3K/AKT signaling cascades that promote uncontrolled malignant cell proliferation and evade programmed apoptosis. In traditional wet-lab High-Throughput Screening (HTS), pharmaceutical laboratories empirically assay millions of physical chemical compounds against target proteins, incurring prohibitive reagent expenditures exceeding $2 billion per approved molecule and requiring developmental timelines spanning over a decade [20], [21]."
    abstract_p2 = "To drastically accelerate early-stage therapeutic discovery while mitigating developmental attrition, this research develops an end-to-end, interpretable computational framework for early virtual high-throughput screening against Human EGFR (ChEMBL ID: CHEMBL203). Chemical structures in SMILES format are ingested through the ChEMBL REST API [8] and preprocessed by converting biochemical IC50 binding values into logarithmic potency (pIC50 = 9 - log10(IC50)), establishing rigorous active (IC50 &lt;= 1,000 nM) and inactive (IC50 &gt;= 10,000 nM) classification boundaries. Molecules are featurized using 2,048-bit Extended Connectivity Circular Fingerprints (ECFP4) [6] coupled with 8 physicochemical descriptors computed via RDKit [7]."
    abstract_p3 = "Supervised ensemble classifiers achieve robust predictive performance on held-out experimental assays, with Random Forest achieving 90.96% accuracy, 91.67% precision, 91.67% recall, and 0.9778 ROC-AUC, and Gradient Boosted Decision Trees achieving 91.53% accuracy, 93.55% precision, 90.62% recall, and 0.9675 ROC-AUC. To resolve the black-box dilemma in biomedical AI, the architecture incorporates cooperative game-theoretic Explainable AI (TreeSHAP) [1], [2], projecting exact polynomial feature attributions back onto 2D molecular graphs to delineate favorable hinge-binding pharmacophores in chartreuse and steric penalties in crimson. Candidate compounds are concurrently assessed for oral bioavailability via Lipinski's Rule of Five [4] and Veber's rules [5], benchmarked for structural similarity against approved clinical EGFR therapeutics (Gefitinib, Dacomitinib, Erlotinib, Afatinib, Lapatinib, Osimertinib), and reasoned through an offline local Large Language Model. This integrated workflow delivers an actionable, transparent screening pipeline that substantially reduces experimental costs in precision oncology."

    abstract_content = [
        [Paragraph("<b>ABSTRACT</b>", abstract_heading)],
        [Paragraph(abstract_p1, abstract_text_style)],
        [Paragraph(abstract_p2, abstract_text_style)],
        [Paragraph(abstract_p3, abstract_text_style)],
        [Spacer(1, 4)],
        [Paragraph("<b>Keywords:</b> Cheminformatics; Machine Learning; Explainable AI (XAI); EGFR Tyrosine Kinase; Non-Small Cell Lung Cancer (NSCLC); TreeSHAP; Morgan Fingerprints (ECFP4); Random Forest; Gradient Boosting; Drug Discovery; Virtual Screening.", keywords_style)]
    ]
    
    t_abstract = Table(abstract_content, colWidths=[485])
    t_abstract.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#cbd5e1")),
        ('LINELEFT', (0,0), (0,-1), 3.5, colors.HexColor("#0284c7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 13),
        ('RIGHTPADDING', (0,0), (-1,-1), 13),
    ]))
    story.append(t_abstract)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SECTION I: INTRODUCTION & RESEARCH MOTIVATION
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION & RESEARCH MOTIVATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("1.1 The Economics and Attrition of Modern Drug Discovery", h2_style))
    story.append(Paragraph("The synthesis and commercial translation of a novel chemical entity into an approved therapeutic drug typically spans 10 to 15 years and demands capital investments exceeding $2.6 billion per clinical success [20], [21]. In conventional wet-lab High-Throughput Screening (HTS), microtiter assay plates are robotically filled with purified target enzymes and candidate small molecules, testing compounds blindly across vast chemical spaces. The empirical cost per biological assay ranges from $10 to $500 per compound, consuming millions of dollars in early exploratory phases while suffering a staggering clinical attrition rate exceeding 90% [21]. The primary culprits behind this attrition are poor pharmacokinetics, unanticipated off-target toxicities, or insufficient on-target binding affinity [4], [5]. Virtual High-Throughput Screening (vHTS) through machine learning acts as an intelligent computational sieve, ranking millions of molecules <i>in silico</i> within milliseconds to prioritize high-affinity leads prior to physical synthesis [20].", body_style))
    
    story.append(Paragraph("1.2 Oncogenic EGFR Kinase Signaling in Lung Cancer", h2_style))
    story.append(Paragraph("Lung cancer, particularly Non-Small Cell Lung Cancer (NSCLC), is the leading cause of oncological mortality worldwide, accounting for over 1.8 million deaths annually [24]. Approximately 15% to 50% of NSCLC patients exhibit somatic activating mutations within the intracellular tyrosine kinase domain of the Epidermal Growth Factor Receptor (EGFR / ErbB-1), such as the exon 19 in-frame deletion (delE746-A750) or the exon 21 L858R point substitution [11], [24]. Under physiological conditions, ligand binding by Epidermal Growth Factor (EGF) stimulates receptor dimerization and autophosphorylation of key regulatory tyrosine residues [24]. This autophosphorylation hyperactivates two principal downstream signal transduction pathways:<br/>1. <b>MAPK/ERK Cascade:</b> Governs transcriptional activation, driving unchecked cellular proliferation.<br/>2. <b>PI3K/AKT Cascade:</b> Inhibits pro-apoptotic bad/caspase pathways, conferring malignant cellular survival.", body_style))
    story.append(Paragraph("While first-generation Tyrosine Kinase Inhibitors (TKIs) like Gefitinib (Iressa) and Erlotinib (Tarceva) demonstrated notable initial clinical remission, secondary resistance mutations (most prominently the gatekeeper T790M substitution and tertiary C797S mutations) inevitably cause therapeutic relapse [11], [12]. Consequently, discovering structurally novel, patentable chemotypes that inhibit wild-type and mutant EGFR variants remains an urgent therapeutic priority [12].", body_style))
    
    story.append(Paragraph("1.3 The Black-Box Challenge in Biomedical Artificial Intelligence", h2_style))
    story.append(Paragraph("Although advanced deep neural networks and ensemble learning algorithms deliver formidable statistical accuracy in bioactivity classification [9], [10], their translation into medicinal chemistry has been severely hindered by model opacity [22]. Medicinal chemists cannot rationally optimize a chemical scaffold based on an uninterpretable probability score alone. Without localized structural rationale delineating which specific pharmacophoric rings or substituents govern target binding, researchers cannot make informed chemical modifications [1], [2]. This investigation directly resolves this challenge by wedding predictive machine learning ensembles with cooperative game-theoretic explainability (TreeSHAP) [1], [2], projecting model decisions directly onto physical 2D chemical topologies.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SECTION I (CONT.): FIGURE 1 & RESEARCH CONTRIBUTIONS
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION (CONT.): PIPELINE ARCHITECTURE & CONTRIBUTIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("1.4 End-to-End System Architecture", h2_style))
    story.append(Paragraph("The platform is engineered as a modular, six-stage pipeline spanning chemical ingestion, featurization, ensemble classification, game-theoretic explainability, and multi-objective lead reporting [7], [8], [9], [14]:", body_style))
    
    if os.path.exists(FIG1_PNG):
        story.append(Image(FIG1_PNG, width=460, height=184))
        story.append(Paragraph("<b>Fig 1:</b> End-to-End Explainable Virtual Screening Architecture for Human EGFR (CHEMBL203).", caption_style))
    
    story.append(Paragraph("1.5 Summary of Key Technical Contributions", h2_style))
    story.append(Paragraph("1. <b>Curated ChEMBL203 Benchmark:</b> Harvested, cleaned, and standardized bioactivity assays from the EMBL-EBI ChEMBL database [8], enforcing a rigorous IC50 &lt;= 1,000 nM active boundary with removal of ambiguous boundary noise.<br/>2. <b>High-Performance Supervised Ensembles:</b> Formulated Random Forest (RF) [9] and Gradient Boosted Decision Tree (GBDT) [10] models achieving 90.96% and 91.53% test accuracy with 0.978 and 0.968 ROC-AUC on unseen held-out validation sets.<br/>3. <b>Topological Atom-Level TreeSHAP Mapping:</b> Developed a spatial deconvolution algorithm that maps computed polynomial Shapley values [1], [2] to physical 2D atom coordinates using RDKit bitInfo [6], [7], illuminating favorable hinge-binding anchors in chartreuse and steric penalties in crimson.<br/>4. <b>Multi-Parameter Oral Bioavailability Screening:</b> Integrated Lipinski's Rule of Five [4] and Veber's oral absorption scorecards [5] with normalized polar radar profiling.<br/>5. <b>Clinical Drug Homology Benchmarking:</b> Engineered a comparative Tanimoto similarity index [6] against 6 FDA-approved EGFR inhibitors (Gefitinib, Dacomitinib, Erlotinib, Afatinib, Lapatinib, Osimertinib) [11], [12].<br/>6. <b>Offline Edge AI Reasoning & Automated Dossier:</b> Embedded a local Ollama LLM chemoinformatics tutor and ReportLab PDF reporting engine wrapped in a dark editorial UI.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SECTION II: RELATED WORK & LITERATURE REVIEW
    # =========================================================================
    story.append(Paragraph("2. RELATED WORK & LITERATURE REVIEW", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("2.1 Evolution of Quantitative Structure-Activity Relationships (QSAR)", h2_style))
    story.append(Paragraph("The quantitative correlation of chemical structure with biological efficacy was pioneered by Corwin Hansch in 1962, utilizing linear regression over octanol-water partition coefficients (LogP) and Hammett electronic constants [15]. As computational power expanded in the 1990s, Structure-Based Drug Design (SBDD) gained prominence through molecular docking algorithms such as AutoDock and Glide [20]. Although molecular docking simulates explicit physical binding poses within protein crystallographic coordinates, it remains computationally demanding, prone to false-positive free energy estimates, and sensitive to rigid receptor assumptions [20]. Conversely, Ligand-Based Virtual Screening (LBVS) leverages empirical bioactivity databases [8] to learn complex, non-linear decision boundaries directly from molecular topology, enabling the rapid screening of millions of molecules in seconds [21].", body_style))
    
    story.append(Paragraph("2.2 Soft Computing and Ensemble Methods in Bioinformatics", h2_style))
    story.append(Paragraph("The application of soft computing, genetic algorithms, and supervised ensemble learning to biomedical data science has been extensively championed by pioneering researchers such as <b>Prof. Sanghamitra Bandyopadhyay</b> (Director, Indian Statistical Institute, Kolkata) [3]. Her foundational research demonstrated that biological datasets (distinguished by extreme feature dimensionality, inherent assay noise, and complex epistatic interactions) cannot be adequately captured by simplistic linear models [3]. Bandyopadhyay and Saha established that ensemble clustering and multi-objective optimization techniques robustly circumvent local optima, providing superior generalization across high-dimensional genomic and proteomic landscapes [3]. Supervised decision tree ensembles like Random Forests [9] and Gradient Boosting [10] build directly on these paradigms, providing robust variance reduction over high-dimensional sparse molecular spaces [14].", body_style))
    
    story.append(Paragraph("2.3 Explainable Artificial Intelligence (XAI) in Clinical Decision-Making", h2_style))
    story.append(Paragraph("To address the critical deficit of interpretability in healthcare AI, Ribeiro et al. introduced LIME (Local Interpretable Model-agnostic Explanations) [22], which approximates local decision boundaries using perturbed linear surrogates. In 2017, Scott Lundberg and Su-In Lee proposed SHAP (SHapley Additive exPlanations) [1], uniting cooperative game theory [23] with additive feature attributions to provide mathematically unique, locally accurate, and globally consistent feature importance values. Lundberg et al. subsequently developed TreeSHAP in 2020 [2], enabling exact polynomial-time calculation of Shapley values for tree ensembles. While TreeSHAP has seen wide adoption in tabular clinical domains, prevailing chemoinformatics literature rarely projects abstract circular fingerprint bit contributions back onto physical chemical graph topologies [1], [6], [7].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: SECTION III: BIOLOGICAL TARGET & DATASET CURATION
    # =========================================================================
    story.append(Paragraph("3. BIOLOGICAL TARGET ANATOMY & DATASET CURATION PROTOCOL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("3.1 Anatomy of Human EGFR Tyrosine Kinase Domain", h2_style))
    story.append(Paragraph("Human EGFR (erbB-1 / HER1) is a 170 kDa transmembrane glycoprotein belonging to the ErbB family of receptor tyrosine kinases [24]. The intracellular catalytic domain (residues 690-953) adopts a canonical bi-lobed architecture: a smaller N-terminal lobe primarily composed of five-stranded beta-sheets and the regulatory alphaC-helix, and a larger C-terminal lobe consisting predominantly of alpha-helices [11], [24]. Adenosine triphosphate (ATP) binds in the deep inter-lobar cleft between the two lobes [11]. Competitive Tyrosine Kinase Inhibitors (TKIs) insert directly into this nucleotide cleft, mimicking the purine ring of ATP and establishing critical directional hydrogen bonds with the backbone amide and carbonyl atoms of hinge region residue <b>Met793</b> [11], [12].", body_style))
    
    story.append(Paragraph("3.2 ChEMBL203 Bioactivity Extraction and Normalization Protocol", h2_style))
    story.append(Paragraph("Experimental bioactivity assays for the target identifier <b>CHEMBL203</b> (Human Epidermal Growth Factor Receptor) were extracted from the EMBL-EBI ChEMBL repository (Version 33) [8] via its official REST API. The curation and standardization protocol enforced the following criteria [8], [20]:<br/>1. <b>Bioactivity Assay Filter:</b> Retained only biochemical binding affinity assays where the standard measurement type is strictly equal to half-maximal inhibitory concentration (IC50) measured in nanomolar (nM) [8].<br/>2. <b>Logarithmic Transformation (pIC50):</b> Absolute IC50 concentrations were transformed into standard negative logarithmic potency: <b>pIC<sub>50</sub> = 9 - log<sub>10</sub>(IC<sub>50</sub>)</b> [20].<br/>3. <b>Binary Classification Discretization:</b> Compounds with IC50 &lt;= 1,000 nM (pIC50 &gt;= 6.0) were designated as Active (y = 1), representing potent micromolar inhibitors. Compounds with IC50 &gt;= 10,000 nM (pIC50 &lt;= 5.0) were designated as Inactive (y = 0). Intermediate compounds with ambiguous affinity (1,000 nM &lt; IC50 &lt; 10,000 nM) were systematically excluded to eliminate boundary label noise [20].<br/>4. <b>Chemical Hygiene and De-duplication:</b> SMILES representations were canonicalized using RDKit [7]. Counter-ions, inorganic salts, and solvent fragments were stripped. Replicate SMILES records were collapsed by computing the geometric mean of replicate IC50 measurements.<br/>The curated benchmark contains <b>881 unique chemical entities</b> (472 Actives, 409 Inactives).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SECTION IV: MULTI-SCALE CHEMOINFORMATICS FEATURIZATION
    # =========================================================================
    story.append(Paragraph("4. MULTI-SCALE MOLECULAR FEATURIZATION & CONFORMATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("4.1 Extended Connectivity Circular Fingerprints (ECFP4)", h2_style))
    story.append(Paragraph("To represent small molecules numerically, compounds are treated as undirected topological graphs G = (V, E), where vertices V correspond to heavy atoms and edges E correspond to covalent bonds [6], [7]. The Morgan circular fingerprint algorithm iteratively computes radial neighborhoods up to radius r = 2 (ECFP4, capturing chemical substructures across diameters of up to 4 bonds) [6]:", body_style))
    story.append(Paragraph("<b>ID_v^(r) = Hash( ID_v^(r-1), SUM [ BondOrder(v, u), ID_u^(r-1) ] )</b>", code_p))
    story.append(Paragraph("Atomic identifiers are initialized with Daylight invariant properties (atomic number, valence, ring membership, aromaticity) [6]. The hashed integer identifiers across all atoms and radii are folded into a dense binary bit vector of fixed length <b>2,048 bits</b> using modulo arithmetic [6]. A bit value of 1 denotes the presence of a specific pharmacophoric motif.", body_style))
    
    story.append(Paragraph("4.2 Physicochemical Molecular Property Descriptors", h2_style))
    story.append(Paragraph("To capture global molecular properties not explicitly encoded by localized circular fingerprints, 8 standardized physicochemical descriptors are extracted via RDKit [7], [13], [15], [16], [17]:", body_style))
    
    desc_tbl = [
        [Paragraph("<b>Descriptor</b>", body_style), Paragraph("<b>Property & Units</b>", body_style), Paragraph("<b>Clinical Role in Virtual Screening</b>", body_style)],
        [Paragraph("MolWt [4]", body_style), Paragraph("Molecular Weight (Da)", body_style), Paragraph("Controls steric cavity fit and passive membrane diffusion", body_style)],
        [Paragraph("MolLogP [15]", body_style), Paragraph("Wildman-Crippen LogP", body_style), Paragraph("Lipophilicity metric; governs intestinal absorption and clearance", body_style)],
        [Paragraph("TPSA [16]", body_style), Paragraph("Polar Surface Area (A<sup>2</sup>)", body_style), Paragraph("Predicts cell permeability and blood-brain barrier penetration", body_style)],
        [Paragraph("NumHDonors [4]", body_style), Paragraph("Count of -OH / -NH groups", body_style), Paragraph("Directional hydrogen-bond donors targeting hinge residues", body_style)],
        [Paragraph("NumHAcceptors [4]", body_style), Paragraph("Count of -O- / -N- atoms", body_style), Paragraph("Hydrogen-bond acceptors stabilizing ATP binding pocket", body_style)],
        [Paragraph("NumRotBonds [5]", body_style), Paragraph("Rotatable Single Bonds", body_style), Paragraph("Conformational flexibility; excess entropy penalizes binding", body_style)],
        [Paragraph("QED [13]", body_style), Paragraph("Quantitative Drug-Likeness [0, 1]", body_style), Paragraph("Composite desirability index reflecting oral clinical success", body_style)],
        [Paragraph("FractionCSP3 [17]", body_style), Paragraph("Ratio of sp<sup>3</sup> Carbons", body_style), Paragraph("3D complexity; higher saturation correlates with clinical safety", body_style)]
    ]
    t_d = Table(desc_tbl, colWidths=[85, 135, 260])
    t_d.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5)
    ]))
    story.append(t_d)
    story.append(Spacer(1, 6))
    story.append(Paragraph("The 8 continuous descriptors are standardized via StandardScaler (zero mean, unit variance) [14] and concatenated with the 2,048 Morgan bits, yielding a comprehensive composite feature vector <b>x in R<sup>2056</sup></b>.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SECTION IV (CONT.): 3D CONFORMATION & FIGURE 2
    # =========================================================================
    story.append(Paragraph("4. MOLECULAR CONFORMATION (CONT.): 3D GEOMETRY & MMFF94", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("4.3 Energy-Minimized 3D Conformation Engine", h2_style))
    story.append(Paragraph("Because planar 2D representations cannot convey spatial steric clashes within the ATP binding cleft, our framework embeds molecules in 3D Euclidean space using the ETKDGv3 (Experimental-Torsion Knowledge-based Distance Geometry) algorithm [18]. Initial distance-geometry conformations are subsequently relaxed to their lowest energy state using the <b>Merck Molecular Force Field 1994 (MMFF94)</b> [19]:", body_style))
    story.append(Paragraph("<b>E_total = E_stretch + E_angle + E_torsion + E_oop + E_van_der_Waals + E_electrostatic</b>", code_p))
    story.append(Paragraph("The optimized Cartesian coordinates are serialized into standard `.mol` blocks [7] and rendered in real-time WebGL via `py3Dmol` within the application interface.", body_style))
    
    if os.path.exists(FIG2_PNG):
        story.append(Image(FIG2_PNG, width=380, height=253))
        story.append(Paragraph("<b>Fig 2:</b> 2D Vector Chemical Architecture of Gefitinib (Iressa) generated via RDKit [7].", caption_style))
    
    story.append(Paragraph("As illustrated in Figure 2, the chemical scaffold of Gefitinib features the planar 4-anilinoquinazoline bicyclic core that mimics the purine ring of ATP [11], a 3-chloro-4-fluoroaniline pharmacophore that inserts into the hydrophobic selectivity pocket [11], and a flexible morpholine propoxy side-chain extending into solvent to enhance aqueous solubility [4], [5].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SECTION V: SUPERVISED ENSEMBLE CLASSIFIERS
    # =========================================================================
    story.append(Paragraph("5. SUPERVISED MACHINE LEARNING ENSEMBLE FORMULATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("5.1 Random Forest (RF) Bagging Formulation", h2_style))
    story.append(Paragraph("Random Forest [9] constructs an ensemble of B = 100 decorrelated decision trees using bootstrap aggregating (bagging). At each candidate split, a random subset of m = sqrt(M) features is evaluated [9], [14]. For classification into active (y=1) versus inactive (y=0) inhibitors, the final predicted binding probability is the consensus expectation:", body_style))
    story.append(Paragraph("<b>P(y = 1 | x) = (1 / B) * SUM[ T_b(x) ]</b>", code_p))
    story.append(Paragraph("Random Forests exhibit exceptional resistance against overfitting on sparse binary Morgan bit vectors [6], reducing generalization variance without inflating bias [9].", body_style))
    
    story.append(Paragraph("5.2 Gradient Boosted Decision Trees (GBDT) Formulation", h2_style))
    story.append(Paragraph("Gradient Boosting [10] constructs an additive ensemble model in a forward stage-wise manner by minimizing binary cross-entropy loss over the training distribution [10], [14]:", body_style))
    story.append(Paragraph("<b>L(y, p) = - [ y * log(p) + (1 - y) * log(1 - p) ]</b>", code_p))
    story.append(Paragraph("At each iteration m, a shallow regression tree h_m(x) is fit to the pseudo-residuals of the existing ensemble. The updated model is formulated as:", body_style))
    story.append(Paragraph("<b>F_m(x) = F_{m-1}(x) + eta * h_m(x)</b>", code_p))
    story.append(Paragraph("where eta = 0.1 is the shrinkage learning rate [10]. GBDT excels at discovering complex non-linear interaction thresholds between continuous physicochemical descriptors and topological fingerprints [10], [14].", body_style))
    
    story.append(Paragraph("5.3 Stratified Training & Validation Protocol", h2_style))
    story.append(Paragraph("The curated dataset of 881 compounds was partitioned into an 80% training set (704 compounds) and a 20% holdout test set (177 compounds) using stratified sampling on label y to preserve empirical class proportions [14]. Feature scalers were fit strictly on training partitions to prevent data leakage [14]. Model hyper-parameters were tuned via 5-fold stratified cross-validation.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: SECTION VI: GAME-THEORETIC EXPLAINABILITY (TREESHAP)
    # =========================================================================
    story.append(Paragraph("6. COOPERATIVE GAME-THEORETIC EXPLAINABILITY (TREESHAP)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("6.1 Shapley Value Axiomatic Foundation", h2_style))
    story.append(Paragraph("Rooted in Lloyd Shapley's cooperative game theory (1953) [23], Shapley values represent the unique feature attribution method that simultaneously satisfies four fundamental mathematical axioms: Efficiency, Symmetry, Dummy (Null player), and Additivity [1], [23]. The marginal contribution of feature i across all possible feature subsets S subset N \\ {i} is defined as:", body_style))
    story.append(Paragraph("<b>phi_i(v) = SUM [ |S|! (|N| - |S| - 1)! / |N|! ] * [ v(S U {i}) - v(S) ]</b>", code_p))
    story.append(Paragraph("In this virtual screening framework, players N correspond to the 2,056 input molecular variables [6], the game payout v(S) represents the ensemble's predicted probability of EGFR inhibition P(Active) [9], [10], and phi_i quantifies the exact directional influence of feature i toward the final prediction [1].", body_style))
    
    story.append(Paragraph("6.2 Polynomial-Time TreeSHAP Algorithm", h2_style))
    story.append(Paragraph("While model-agnostic KernelSHAP requires exponential computational sampling O(2^|N|) [1], the TreeSHAP algorithm formulated by Lundberg et al. (2020) [2] evaluates exact conditional expectations by recursively tracking feature split paths through decision tree branches in polynomial time O(T * L * D<sup>2</sup>), where T is tree count, L is maximum leaf count, and D is maximum tree depth [2]. This algorithmic efficiency enables instantaneous, sub-second explainability in interactive web screening applications [2].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: SECTION VI (CONT.): ATOM ATTRIBUTION ALGORITHM & FIG 3
    # =========================================================================
    story.append(Paragraph("6. EXPLAINABLE AI (CONT.): ATOM ATTRIBUTION & FIGURE 3", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("6.3 Topological Substructure Deconvolution Algorithm", h2_style))
    story.append(Paragraph("Because Morgan circular fingerprints represent localized concentric atomic neighborhoods [6], our framework maps computed Shapley values back to physical 2D atom coordinates using RDKit's bitInfo dictionary [7]:<br/>1. For each active fingerprint bit j with Shapley attribution phi_j, the central atom index v and radius r are retrieved [6], [7].<br/>2. The attribution is distributed across constituent atomic coordinates: <b>AtomScore(v) = SUM[ phi_j * w(r) ]</b>.<br/>3. Normalized atom scores are mapped to RGB visual highlights on the molecular graph [7]:", body_style))
    story.append(Paragraph("- <b>Chartreuse Highlights (phi &gt; 0):</b> Positive pharmacophores shifting prediction toward EGFR inhibition.<br/>- <b>Crimson Highlights (phi &lt; 0):</b> Unfavorable substituents penalizing predicted binding affinity.", body_style))
    
    if os.path.exists(FIG3_PNG):
        story.append(Image(FIG3_PNG, width=380, height=253))
        story.append(Paragraph("<b>Fig 3:</b> Atom-Level SHAP Highlight Map for Gefitinib. Chartreuse regions identify primary hinge-binding pharmacophores.", caption_style))
    
    story.append(Paragraph("As documented in the project poster, the top positive SHAP feature drivers for EGFR inhibition include:<br/>- <b>ECFP4_Bit_489 (+0.0299):</b> Quinazoline nitrogen heteroatom participating in hinge hydrogen bonding [11].<br/>- <b>ECFP4_Bit_708 (+0.0248):</b> Halogenated aniline aromatic ring mediating hydrophobic pocket packing [11].<br/>- <b>ECFP4_Bit_491 (+0.0243):</b> Secondary amine linker anchoring the core scaffold with Met793 [11].<br/>- Additional key drivers: Bit 1226 (+0.0234), Bit 1367 (+0.0234), Bit 794 (+0.0218), Bit 1157 (+0.0213), Bit 329 (+0.0186).", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: SECTION VII: ORAL DRUG-LIKENESS & ADMET PROFILING
    # =========================================================================
    story.append(Paragraph("7. ORAL DRUG-LIKENESS & ADMET BIOAVAILABILITY PROFILING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("7.1 Lipinski's Rule of Five Heuristic", h2_style))
    story.append(Paragraph("Christopher Lipinski et al. (2001) demonstrated that poor oral absorption and low gastrointestinal permeability are significantly more prevalent when a drug candidate violates more than one of the following four criteria [4]:", body_style))
    story.append(Paragraph("1. <b>Molecular Weight (MolWt) &lt;= 500 Da:</b> Bulky molecules suffer reduced aqueous diffusion and poor membrane transport [4].<br/>2. <b>Lipophilicity (MolLogP) &lt;= 5.0:</b> Excessive hydrophobicity leads to poor aqueous solubility, non-specific binding, and rapid metabolic clearance [4], [15].<br/>3. <b>Hydrogen Bond Donors (HBD) &lt;= 5:</b> Excessive -OH and -NH groups incur steep desolvation penalties when crossing lipid bilayers [4].<br/>4. <b>Hydrogen Bond Acceptors (HBA) &lt;= 10:</b> Abundant electronegative nitrogen and oxygen atoms hinder passive membrane transit [4].", body_style))
    
    story.append(Paragraph("7.2 Veber's Permeability & Flexibility Criteria", h2_style))
    story.append(Paragraph("Daniel Veber et al. (2002) established that molecular flexibility and polar surface area are superior predictors of oral bioavailability in rats and humans [5]:", body_style))
    story.append(Paragraph("- <b>Rotatable Bonds &lt;= 10:</b> High conformational flexibility imposes conformational entropic penalties upon receptor binding [5].<br/>- <b>Topological Polar Surface Area (TPSA) &lt;= 140 A<sup>2</sup>:</b> Polar surface area exceeding 140 A<sup>2</sup> severely diminishes passive oral bioavailability [5], [16].", body_style))
    
    story.append(Paragraph("7.3 Multi-Parameter Evaluation Matrix", h2_style))
    dl_tab = [
        [Paragraph("<b>Compound</b>", body_style), Paragraph("<b>MolWt</b>", body_style), Paragraph("<b>LogP</b>", body_style), Paragraph("<b>HBD</b>", body_style), Paragraph("<b>HBA</b>", body_style), Paragraph("<b>TPSA</b>", body_style), Paragraph("<b>RotB</b>", body_style), Paragraph("<b>Rule Compliance</b>", body_style)],
        [Paragraph("Gefitinib [11]", body_style), Paragraph("446.91", body_style), Paragraph("4.28", body_style), Paragraph("1", body_style), Paragraph("7", body_style), Paragraph("68.7", body_style), Paragraph("8", body_style), Paragraph("<b>PASS (0 violations)</b>", body_style)],
        [Paragraph("Dacomitinib", body_style), Paragraph("469.95", body_style), Paragraph("4.35", body_style), Paragraph("1", body_style), Paragraph("7", body_style), Paragraph("70.9", body_style), Paragraph("6", body_style), Paragraph("<b>PASS (0 violations)</b>", body_style)],
        [Paragraph("Erlotinib [24]", body_style), Paragraph("393.44", body_style), Paragraph("3.41", body_style), Paragraph("1", body_style), Paragraph("6", body_style), Paragraph("74.7", body_style), Paragraph("8", body_style), Paragraph("<b>PASS (0 violations)</b>", body_style)],
        [Paragraph("Afatinib [12]", body_style), Paragraph("485.94", body_style), Paragraph("3.92", body_style), Paragraph("2", body_style), Paragraph("8", body_style), Paragraph("81.8", body_style), Paragraph("8", body_style), Paragraph("<b>PASS (0 violations)</b>", body_style)],
        [Paragraph("Lapatinib [24]", body_style), Paragraph("581.06", body_style), Paragraph("5.38", body_style), Paragraph("2", body_style), Paragraph("7", body_style), Paragraph("114.3", body_style), Paragraph("9", body_style), Paragraph("<b>FAIL (2 violations)</b>", body_style)]
    ]
    t_dl = Table(dl_tab, colWidths=[70, 50, 50, 45, 45, 55, 45, 120])
    t_dl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2)
    ]))
    story.append(t_dl)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: SECTION VII (CONT.): POLAR RADAR PROFILE & FIGURE 5
    # =========================================================================
    story.append(Paragraph("7. DRUG-LIKENESS (CONT.): BIOAVAILABILITY RADAR & FIGURE 5", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("7.4 Normalized Bioavailability Radar Profiling", h2_style))
    story.append(Paragraph("To enable immediate visual evaluation of multi-parameter drug-likeness, the 6 core oral bioavailability descriptors are normalized against their standard upper threshold boundaries (Boundary = 1.0) [4], [5]:", body_style))
    
    if os.path.exists(FIG5_PNG):
        story.append(Image(FIG5_PNG, width=340, height=340))
        story.append(Paragraph("<b>Fig 5:</b> Polar Bioavailability Radar Profile. Green polygon depicts Gefitinib within the red dashed oral boundary.", caption_style))
    
    story.append(Paragraph("As depicted in Figure 5, the query molecule Gefitinib produces a polygon that resides entirely within the red dashed threshold boundary across all 6 axes, confirming favorable oral pharmacokinetic bioavailability without necessitating structural modification [4], [5].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: SECTION VIII: CLINICAL HOMOLOGY & FIGURE 6
    # =========================================================================
    story.append(Paragraph("8. APPROVED DRUG SIMILARITY BENCHMARKING (TANIMOTO)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("8.1 Tanimoto Coefficient Formulation", h2_style))
    story.append(Paragraph("The Tanimoto (Jaccard) similarity coefficient [3], [6] between a query molecule's 2,048-bit ECFP4 fingerprint vector A and a reference clinical drug vector B is calculated as:", body_style))
    story.append(Paragraph("<b>T_c(A, B) = |A INTERSECT B| / |A UNION B| = c / (a + b - c)</b>", code_p))
    story.append(Paragraph("where c is the count of coincident active bits, and a, b are the total bit counts for vectors A and B, respectively [6]. Queries are benchmarked against 6 clinically approved EGFR cancer therapeutics [11], [12]:", body_style))
    
    if os.path.exists(FIG6_PNG):
        story.append(Image(FIG6_PNG, width=430, height=240))
        story.append(Paragraph("<b>Fig 6:</b> Tanimoto Structural Similarity Index (%) against FDA-Approved EGFR Tyrosine Kinase Inhibitors (matching poster).", caption_style))
    
    story.append(Paragraph("The empirical Tanimoto alignment reflects precise pharmacological relationships:<br/>- <b>Gefitinib (Iressa):</b> 100.0% identity against itself [11].<br/>- <b>Dacomitinib (Vizimpro):</b> 44.1% similarity, sharing the 4-anilinoquinazoline core with an acrylamide warhead [12].<br/>- <b>Erlotinib (Tarceva):</b> 40.8% similarity, retaining the quinazoline core with bis-alkoxy sidechains [24].<br/>- <b>Afatinib (Gilotrif):</b> 38.1% similarity, reflecting second-generation irreversible quinazoline conservation [12].<br/>- <b>Lapatinib (Tykerb):</b> 31.7% similarity, reflecting dual EGFR/HER2 inhibition with bulkier fluorobenzyloxy substituents.<br/>- <b>Osimertinib (Tagrisso):</b> 15.0% similarity, structurally diverging into a third-generation indole-pyrimidine covalent scaffold [12].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: SECTION IX: SYSTEM IMPLEMENTATION & OLLAMA LLM
    # =========================================================================
    story.append(Paragraph("9. SYSTEM IMPLEMENTATION, HERBARIUM UI & OLLAMA LLM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("9.1 Herbarium Alpinum Editorial Design System", h2_style))
    story.append(Paragraph("The web interface is implemented in Streamlit, styled under the <b>HERBARIUM ALPINUM - The Edelweiss Folio</b> design specification. It departs from generic commercial dashboards in favor of an authoritative scientific workspace [22]:<br/>- <b>Base Surfaces:</b> Deep technical surfaces (#000000, #080e0a) with dark botanical card panels (#101811) and muted forest-green borders (#35402f).<br/>- <b>Typography:</b> Pale botanical chalk (#e6e9d9) adhering to WCAG 2.2 AA contrast standards (&gt; 4.5:1 ratio).<br/>- <b>Interactive Accent:</b> Fluorescent chartreuse (#99ff00) reserved exclusively for active predictions, positive SHAP anchors, and primary CTA actions.", body_style))
    
    story.append(Paragraph("9.2 Local Offline Ollama LLM Chemoinformatics Tutor", h2_style))
    story.append(Paragraph("To assist students and non-specialist evaluators in interpreting complex pharmacology, the application integrates a local offline LLM daemon via Ollama (`http://127.0.0.1:11434/api/generate`) running `gemma3:1b`. The daemon dynamically ingests calculated descriptors, predicted probabilities, and top SHAP feature drivers into a structured prompt context, outputting clear, plain-language mechanistic explanations without exposing sensitive chemical data to cloud servers.", body_style))
    
    story.append(Paragraph("9.3 Automated Vector PDF Reporting Engine", h2_style))
    story.append(Paragraph("The platform compiles comprehensive publication-ready PDF screening dossiers on demand in under 2 seconds via ReportLab, encapsulating vector 2D structures [7], calibrated ensemble probabilities [9], [10], Lipinski rule evaluations [4], and clinical homology benchmarks [6].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: SECTION X: EXPERIMENTAL RESULTS & BENCHMARKS
    # =========================================================================
    story.append(Paragraph("10. EXPERIMENTAL RESULTS & BENCHMARK DISCUSSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("10.1 Empirical Holdout Test Set Performance Metrics", h2_style))
    story.append(Paragraph("Models were trained on 704 curated compounds and evaluated on a holdout test set of 177 unseen chemical compounds from ChEMBL203 [8] (matching the approved poster metrics):", body_style))
    
    res_table = [
        [Paragraph("<b>Model Classifier</b>", body_style), Paragraph("<b>Accuracy</b>", body_style), Paragraph("<b>Precision</b>", body_style), Paragraph("<b>Recall</b>", body_style), Paragraph("<b>F1-Score</b>", body_style), Paragraph("<b>ROC-AUC</b>", body_style)],
        [Paragraph("Random Forest (RF) [9]", body_style), Paragraph("<b>90.96%</b>", body_style), Paragraph("91.67%", body_style), Paragraph("91.67%", body_style), Paragraph("0.9167", body_style), Paragraph("<b>0.9778</b>", body_style)],
        [Paragraph("Gradient Boosting (GBDT) [10]", body_style), Paragraph("<b>91.53%</b>", body_style), Paragraph("93.55%", body_style), Paragraph("90.62%", body_style), Paragraph("0.9206", body_style), Paragraph("<b>0.9675</b>", body_style)]
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
    
    story.append(Paragraph("10.2 Empirical Metric Analysis & Calibration", h2_style))
    story.append(Paragraph("Both ensemble classifiers decisively exceed our initial project target of 0.80 ROC-AUC [20]. Gradient Boosting achieved slightly higher test accuracy (91.53%) and precision (93.55%), effectively minimizing false-positive lead classifications [10]. Conversely, Random Forest delivered superior discrimination across the full threshold spectrum with an outstanding <b>ROC-AUC of 0.9778</b> [9]. The balanced recall rates (91.67% and 90.62%) verify that the models reliably capture true active kinase inhibitors while maintaining a low false-alarm rate under 8.5% [9], [10].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: SECTION X (CONT.): FIGURE 4 ROC CURVES & CASE STUDIES
    # =========================================================================
    story.append(Paragraph("10. RESULTS (CONT.): ROC CURVES & COMPARATIVE CASE STUDIES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    
    if os.path.exists(FIG4_PNG):
        story.append(Image(FIG4_PNG, width=320, height=266))
        story.append(Paragraph("<b>Fig 4:</b> Holdout ROC Curves for Random Forest (AUC = 0.978) and Gradient Boosting (AUC = 0.968).", caption_style))
    
    story.append(Paragraph("10.3 Comparative Case Studies: Active Lead vs. Negative Control", h2_style))
    story.append(Paragraph("- <b>Gefitinib (Approved EGFR TKI) [11]:</b> Classified Active with <b>P(Active) = 99.8%</b>. SHAP feature attribution identified the 4-anilinoquinazoline core (ECFP4_Bit_489, phi = +0.0299) and 3-chloro-4-fluoroaniline moiety (ECFP4_Bit_708, phi = +0.0248) as top positive drivers, matching crystallographic hinge-binding interactions with Met793 [11].<br/>- <b>Aspirin (Negative Control):</b> Classified Inactive with <b>P(Active) = 7.7%</b>. SHAP identified low molecular weight (180 Da) and the charged carboxylate group (phi = -0.0982) as severe penalties, producing electrostatic repulsion within the hydrophobic ATP pocket.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: SECTION XI: UNIVERSITY SYLLABUS ALIGNMENT
    # =========================================================================
    story.append(Paragraph("11. UNIVERSITY CURRICULUM ALIGNMENT (UNITS I TO V)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("This mini-project directly maps to the university <b>AI Systems and Applications</b> curriculum:", body_style))
    
    syl_table = [
        [Paragraph("<b>Syllabus Unit</b>", body_style), Paragraph("<b>Curriculum Concept</b>", body_style), Paragraph("<b>Implementation in Proposed Project</b>", body_style)],
        [Paragraph("<b>UNIT-I</b>", body_style), Paragraph("Key Components of AI Systems & Narrow AI", body_style), Paragraph("Domain-specific Narrow AI for oncology problem solving; observes bioethics against clinical over-extrapolation [20].", body_style)],
        [Paragraph("<b>UNIT-II</b>", body_style), Paragraph("ML Frameworks & Supervised Learning", body_style), Paragraph("End-to-end data pipeline using Pandas, NumPy, and Scikit-learn [14]; trained Random Forest [9] and GBDT [10] ensembles.", body_style)],
        [Paragraph("<b>UNIT-III</b>", body_style), Paragraph("Graph Theory, LLMs & Explainable AI", body_style), Paragraph("Molecules as graphs G=(V,E) via 2048-bit ECFP4 [6]; local Ollama LLM tutor; game-theoretic SHAP TreeExplainer [1], [2].", body_style)],
        [Paragraph("<b>UNIT-IV</b>", body_style), Paragraph("AI Applications in Healthcare", body_style), Paragraph("Direct precision oncology application targeting EGFR in NSCLC [24], drastically reducing wet-lab screening costs [21].", body_style)],
        [Paragraph("<b>UNIT-V</b>", body_style), Paragraph("Historical AI Milestones & Case Studies", body_style), Paragraph("Modern parallel to IBM Watson Health, DeepMind AlphaFold, and predictive disease biomarker systems [3], [21].", body_style)]
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
    story.append(Paragraph("12. DISCUSSION, TECHNOLOGICAL ADVANTAGES & LIMITATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("12.1 Key Technological Advantages", h2_style))
    story.append(Paragraph("1. <b>High-Throughput Acceleration:</b> Evaluates compounds <i>in silico</i> in under 50 milliseconds, bypassing months of physical assay preparation [20].<br/>2. <b>Transparent Lead Optimization:</b> Atom-level TreeSHAP highlights provide chemists with actionable feedback on which functional groups enhance or penalize binding [1], [2].<br/>3. <b>Concurrent Bioavailability Screening:</b> Evaluates target binding affinity alongside Lipinski and Veber oral absorption heuristics to reject insoluble hits [4], [5].<br/>4. <b>Complete On-Premise Privacy:</b> The local Ollama LLM and Python inference run entirely offline with zero third-party cloud data exposure.", body_style))
    
    story.append(Paragraph("12.2 Critical Methodological Limitations", h2_style))
    story.append(Paragraph("1. <b>2D Graph Topological Invariance:</b> Morgan fingerprints encode 2D circular connectivity but do not explicitly account for flexible protein backbone induced-fit dynamics or quantum mechanical polarization [6], [20].<br/>2. <b>Binary Potency Discretization:</b> Continuous affinity is binarized (IC50 &lt;= 1,000 nM vs &gt;= 10,000 nM), omitting weakly active molecules (1,000-10,000 nM) [20].<br/>3. <b>Target Selectivity Boundary:</b> The model is trained on Human EGFR (CHEMBL203) [8] and does not predict broader off-target kinome selectivity across related kinases (HER2, HER4, VEGFR2) [24].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: SECTION XIII: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("13. CONCLUSION & FUTURE RESEARCH DIRECTIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
    story.append(Paragraph("13.1 Research Conclusions", h2_style))
    story.append(Paragraph("In this mini-project for <b>AI Systems and Applications</b> at <b>MIT World Peace University (MIT-WPU), Pune</b>, conducted under the mentorship of <b>Dr. Devendra Joshi</b>, an end-to-end, interpretable computational screening platform, <b>EGFR Molecular Intelligence</b>, was successfully formulated, implemented, and empirically validated.", body_style))
    story.append(Paragraph("By combining RDKit chemoinformatics [7], 2,048-bit Morgan circular graph representations [6], and supervised tree ensemble models [9], [10], the system achieved <b>90.96% accuracy and 0.978 ROC-AUC</b> on a curated benchmark of 881 ChEMBL compounds [8]. Integrating polynomial TreeSHAP game theory [1], [2] resolved the black-box dilemma by projecting atom-level binding explanations directly onto 2D molecular graphs [7]. Supported by Lipinski oral bioavailability radar charts [4], clinical Tanimoto similarity indexing [6], an embedded local Ollama LLM tutor, and automated PDF reporting, this platform demonstrates the transformative power of Explainable AI in precision oncology [21].", body_style))
    
    story.append(Paragraph("13.2 Future Scope & Research Roadmap (from Approved Poster)", h2_style))
    story.append(Paragraph("- <b>Screen Larger & Diverse Libraries:</b> Expand virtual screening across multi-million compound repositories (ZINC20, Enamine REAL) [20].<br/>- <b>3D Equivariant Graph Neural Networks (EGNN):</b> Incorporate geometric deep learning directly on 3D Cartesian coordinates to capture flexible induced-fit docking dynamics [21].<br/>- <b>Predict Selectivity & ADMET Properties:</b> Build multi-target kinome selectivity models (HER2, HER4, MET) and quantitative toxicity predictors (hERG, Ames, CYP450) [21], [24].<br/>- <b>Wet-Lab Experimental Validation:</b> Validate top computational candidates through molecular docking and <i>in-vitro</i> cell viability assays [20].<br/>- <b>Interactive Web Platform:</b> Deploy a scalable cloud web platform for real-time drug screening and explanation [22].", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 22: SECTION XIV: REFERENCES (24 CITATIONS IN IEEE FORMAT)
    # =========================================================================
    story.append(Paragraph("14. REFERENCES (24 PEER-REVIEWED ACADEMIC CITATIONS)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
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
