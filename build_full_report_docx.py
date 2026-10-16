"""
Generates the Comprehensive Academic Research Monograph in DOCX format (Word Document).
Adhering to Dr. Vishwanath Karad MIT World Peace University (MIT-WPU), Pune guidelines
for the course: AI SYSTEMS AND APPLICATIONS
Guide: Dr. Devendra Joshi
Authors (from Approved Poster):
  - Kalpana Bishnoi (PRN: 1262242386)
  - Kuntal Saha (PRN: 1262242342)
  - Saloni Bhongle (PRN: 1262242338)

Includes:
- Title page with embedded MIT-WPU logo
- Table of Contents
- Abstract callout box with cyan accent bar (no student names, no index terms)
- Comprehensive in-text citations ([1] to [24]) throughout
- All 6 embedded publication figures with captions
- All data tables, mathematical formulations, and complete 14-section monograph
- Professional typography, headers, footers, and margins
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DOCX = os.path.join(CURRENT_DIR, "ACADEMIC_PROJECT_REPORT.docx")

# Asset paths
LOGO_PNG = os.path.join(CURRENT_DIR, "mit_wpu_logo.png")
FIG1_PNG = os.path.join(CURRENT_DIR, "fig1_pipeline_architecture.png")
FIG2_PNG = os.path.join(CURRENT_DIR, "fig2_gefitinib_structure.png")
FIG3_PNG = os.path.join(CURRENT_DIR, "fig3_shap_highlight_map.png")
FIG4_PNG = os.path.join(CURRENT_DIR, "fig4_roc_curves.png")
FIG5_PNG = os.path.join(CURRENT_DIR, "fig5_radar_druglikeness.png")
FIG6_PNG = os.path.join(CURRENT_DIR, "fig6_similarity_benchmark.png")


def set_cell_shading(cell, color_hex):
    """Sets cell background fill color."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_left_border(cell, color_hex="0284C7", size="36"):
    """Adds a thick accent border on the left of a callout cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="{size}" w:space="0" w:color="{color_hex}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)


def set_table_borders(table, color_hex="CBD5E1"):
    """Sets subtle academic horizontal borders for tables."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="0369A1"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="0369A1"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color_hex}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_callout_box(doc, title, paragraphs, keywords=""):
    """Creates a research paper styled Abstract callout box with a cyan left bar."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    set_cell_shading(cell, "F8FAFC")
    set_cell_left_border(cell, "0284C7", size="36")
    
    # Internal cell margins
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="160" w:type="dxa"/>'
        f'<w:bottom w:w="160" w:type="dxa"/>'
        f'<w:left w:w="220" w:type="dxa"/>'
        f'<w:right w:w="200" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)
    
    p_head = cell.paragraphs[0]
    p_head.paragraph_format.space_before = Pt(4)
    p_head.paragraph_format.space_after = Pt(6)
    r_head = p_head.add_run(title)
    r_head.bold = True
    r_head.font.size = Pt(11)
    r_head.font.color.rgb = RGBColor(2, 132, 199) # Cyan/Blue
    
    for text in paragraphs:
        p = cell.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        
    if keywords:
        p_kw = cell.add_paragraph()
        p_kw.paragraph_format.space_before = Pt(4)
        p_kw.paragraph_format.space_after = Pt(4)
        r_lbl = p_kw.add_run("Keywords: ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.color.rgb = RGBColor(15, 23, 42)
        r_val = p_kw.add_run(keywords)
        r_val.font.size = Pt(9.5)
        r_val.font.color.rgb = RGBColor(51, 65, 85)


def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p


def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(3, 105, 161) # Academic Blue
    return p


def add_body_p(doc, text, bold_prefix="", italic_suffix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_bp = p.add_run(bold_prefix)
        r_bp.bold = True
        r_bp.font.size = Pt(10)
        r_bp.font.color.rgb = RGBColor(15, 23, 42)
        
    r_body = p.add_run(text)
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = RGBColor(30, 41, 59)
    
    if italic_suffix:
        r_is = p.add_run(italic_suffix)
        r_is.italic = True
        r_is.font.size = Pt(10)
        r_is.font.color.rgb = RGBColor(51, 65, 85)
        
    return p


def add_formula_block(doc, formula_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(formula_text)
    run.bold = True
    run.font.name = "Cambria Math"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p


def add_figure(doc, img_path, caption_text, width_inches=5.5):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run(caption_text)
        run_cap.italic = True
        run_cap.font.size = Pt(8.5)
        run_cap.font.color.rgb = RGBColor(71, 85, 105)


def build_docx_monograph():
    print("Generating Academic Research Monograph in DOCX format...")
    doc = Document()
    
    # Page setup: Standard A4 with 1-inch margins
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69) # A4 height
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        
        # Configure Header
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("MIT-WPU PUNE | AI SYSTEMS & APPLICATIONS | EGFR DRUG DISCOVERY RESEARCH REPORT")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(8)
        r_hdr.font.color.rgb = RGBColor(100, 116, 139)
        
        # Configure Footer
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_ftr = p_ftr.add_run("Dr. Vishwanath Karad MIT World Peace University, Pune - Guide: Dr. Devendra Joshi")
        r_ftr.font.name = "Calibri"
        r_ftr.font.size = Pt(8)
        r_ftr.font.color.rgb = RGBColor(100, 116, 139)

    # Set default style to Calibri
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10)
    font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # PAGE 1: TITLE PAGE (OFFICIAL MIT-WPU LOGO & TEAM DETAILS)
    # =========================================================================
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(10)
    p_logo.paragraph_format.space_after = Pt(12)
    if os.path.exists(LOGO_PNG):
        p_logo.add_run().add_picture(LOGO_PNG, width=Inches(3.8))
        
    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_after = Pt(14)
    r_univ = p_univ.add_run("Dr. Vishwanath Karad MIT WORLD PEACE UNIVERSITY, PUNE")
    r_univ.bold = True
    r_univ.font.size = Pt(12)
    r_univ.font.color.rgb = RGBColor(15, 23, 42)

    p_min = doc.add_paragraph()
    p_min.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_min.paragraph_format.space_after = Pt(6)
    r_min = p_min.add_run("A MINI PROJECT REPORT ON")
    r_min.bold = True
    r_min.font.size = Pt(10)
    r_min.font.color.rgb = RGBColor(71, 85, 105)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("AI-POWERED DRUG DISCOVERY FOR EGFR INHIBITORS IN LUNG CANCER")
    r_title.bold = True
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = RGBColor(3, 105, 161)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Integrating Cheminformatics, Machine Learning and Explainable AI to Identify Potential Anticancer Compounds")
    r_sub.italic = True
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_after = Pt(24)
    r_req1 = p_req.add_run("Submitted in partial fulfillment of the requirements for the course\n")
    r_req1.italic = True
    r_req1.font.size = Pt(9.5)
    r_req2 = p_req.add_run("AI SYSTEMS AND APPLICATIONS")
    r_req2.bold = True
    r_req2.font.size = Pt(10.5)

    # Authors & Guide Table
    tbl_cand = doc.add_table(rows=1, cols=2)
    tbl_cand.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_cand.cell(0, 0)
    c_right = tbl_cand.cell(0, 1)
    c_left.width = Inches(3.2)
    c_right.width = Inches(3.2)

    p_cl = c_left.paragraphs[0]
    p_cl.paragraph_format.space_after = Pt(4)
    r1 = p_cl.add_run("Submitted by:\n")
    r1.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)
    r2 = p_cl.add_run("Kalpana Bishnoi  (PRN: 1262242386)\nKuntal Saha  (PRN: 1262242342)\nSaloni Bhongle  (PRN: 1262242338)")
    r2.font.size = Pt(9.5)

    p_cr = c_right.paragraphs[0]
    p_cr.paragraph_format.space_after = Pt(4)
    r3 = p_cr.add_run("Under the Guidance of:\n")
    r3.bold = True
    r3.font.color.rgb = RGBColor(15, 23, 42)
    r4 = p_cr.add_run("Dr. Devendra Joshi\nDepartment of Computer Science & Engineering,\nDepartment of Artificial Intelligence & Data Science,\nDr. Vishwanath Karad MIT World Peace University")
    r4.font.size = Pt(9.5)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(36)
    p_dept.paragraph_format.space_after = Pt(0)
    r_dept = p_dept.add_run(
        "Department of Computer Science and Engineering\n"
        "Department of Artificial Intelligence and Data Science\n"
        "School of Computer Science and Engineering\n"
        "Dr. Vishwanath Karad MIT World Peace University\n"
        "Paud Road, Kothrud, Pune, Maharashtra - 411 038, India\n"
        "Academic Year: 2026-2027"
    )
    r_dept.font.size = Pt(9.5)
    r_dept.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================================
    add_heading_1(doc, "TABLE OF CONTENTS & RESEARCH OUTLINE")
    
    toc_data = [
        ("Section", "Research Chapter / Content Outline", "Page"),
        ("-", "Title Page (Authors, Affiliations, MIT-WPU Pune)", "1"),
        ("-", "Table of Contents & Research Outline", "2"),
        ("-", "Abstract & Keywords (Poster Synthesis & Scope)", "3"),
        ("Section 1", "Background & Motivation: Oncogenic EGFR & Drug Discovery Economics", "4"),
        ("Section 1 (cont.)", "System Pipeline Architecture & Figure 1 Workflow Block Diagram", "5"),
        ("Section 2", "Related Work & Literature Review: QSAR, Soft Computing & XAI", "6"),
        ("Section 3", "Biological Target Anatomy & ChEMBL203 Bioactivity Curation Protocol", "7"),
        ("Section 4", "Multi-Scale Molecular Featurization: ECFP4 Fingerprints & Descriptors", "8"),
        ("Section 4 (cont.)", "2D/3D Molecular Geometry, MMFF94 & Figure 2 Gefitinib Architecture", "9"),
        ("Section 5", "Supervised Ensemble Classifiers: Random Forest & Gradient Boosting", "10"),
        ("Section 6", "Game-Theoretic Explainability: TreeSHAP Mathematical Formulation", "11"),
        ("Section 6 (cont.)", "Atom-Level Attribution Algorithm & Figure 3 SHAP Highlight Map", "12"),
        ("Section 7", "Oral Drug-Likeness & Bioavailability: Lipinski and Veber Profiles", "13"),
        ("Section 7 (cont.)", "Bioavailability Radar Profile & Figure 5 Polar Radar Boundary Plot", "14"),
        ("Section 8", "Approved Drug Similarity Benchmarking & Figure 6 Tanimoto Analysis", "15"),
        ("Section 9", "Software Implementation: Herbarium UI System & Local Ollama LLM", "16"),
        ("Section 10", "Experimental Results & Empirical Holdout Test Set Benchmark Metrics", "17"),
        ("Section 10 (cont.)", "Figure 4 Holdout ROC Curves & Comparative Oncological Case Studies", "18"),
        ("Section 11", "University AI Syllabus Alignment: Units I to V Curriculum Mapping", "19"),
        ("Section 12", "Discussion, Technological Advantages & Critical Biological Limitations", "20"),
        ("Section 13", "Conclusion & Future Work: Geometric GNNs & De Novo Design", "21"),
        ("Section 14", "References (24 Peer-Reviewed Academic Citations in IEEE Format)", "22")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_data), cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc)
    
    for row_idx, (col1, col2, col3) in enumerate(toc_data):
        row = tbl_toc.rows[row_idx]
        row.cells[0].width = Inches(1.2)
        row.cells[1].width = Inches(4.5)
        row.cells[2].width = Inches(0.8)
        
        row.cells[0].text = col1
        row.cells[1].text = col2
        row.cells[2].text = col3
        
        if row_idx == 0:
            set_cell_shading(row.cells[0], "F1F5F9")
            set_cell_shading(row.cells[1], "F1F5F9")
            set_cell_shading(row.cells[2], "F1F5F9")
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(9.5)
        else:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        r.font.size = Pt(9)
                        
    doc.add_page_break()

    # =========================================================================
    # PAGE 3: ABSTRACT & KEYWORDS (POSTER SYNTHESIS)
    # =========================================================================
    add_heading_1(doc, "RESEARCH ABSTRACT & SCOPE")
    
    ab_p1 = (
        "Lung cancer, predominantly Non-Small Cell Lung Cancer (NSCLC), represents a leading cause of "
        "cancer-related mortality worldwide, frequently driven by dysregulated overexpression or activating "
        "somatic mutations in the Epidermal Growth Factor Receptor (EGFR / ErbB-1). Ligand binding induces "
        "receptor dimerization and tyrosine autophosphorylation, hyperactivating downstream MAPK/ERK and "
        "PI3K/AKT signaling cascades that promote uncontrolled malignant cell proliferation and evade programmed "
        "apoptosis. In traditional wet-lab High-Throughput Screening (HTS), pharmaceutical laboratories empirically "
        "assay millions of physical chemical compounds against target proteins, incurring prohibitive reagent "
        "expenditures exceeding $2 billion per approved molecule and requiring developmental timelines spanning over "
        "a decade [20], [21]."
    )
    ab_p2 = (
        "To drastically accelerate early-stage therapeutic discovery while mitigating developmental attrition, this "
        "research develops an end-to-end, interpretable computational framework for early virtual high-throughput "
        "screening against Human EGFR (ChEMBL ID: CHEMBL203). Chemical structures in SMILES format are ingested through "
        "the ChEMBL REST API [8] and preprocessed by converting biochemical IC50 binding values into logarithmic potency "
        "(pIC50 = 9 - log10(IC50)), establishing rigorous active (IC50 <= 1,000 nM) and inactive (IC50 >= 10,000 nM) "
        "classification boundaries. Molecules are featurized using 2,048-bit Extended Connectivity Circular Fingerprints "
        "(ECFP4) [6] coupled with 8 physicochemical descriptors computed via RDKit [7]."
    )
    ab_p3 = (
        "Supervised ensemble classifiers achieve robust predictive performance on held-out experimental assays, with "
        "Random Forest achieving 90.96% accuracy, 91.67% precision, 91.67% recall, and 0.9778 ROC-AUC, and Gradient "
        "Boosted Decision Trees achieving 91.53% accuracy, 93.55% precision, 90.62% recall, and 0.9675 ROC-AUC. To "
        "resolve the black-box dilemma in biomedical AI, the architecture incorporates cooperative game-theoretic "
        "Explainable AI (TreeSHAP) [1], [2], projecting exact polynomial feature attributions back onto 2D molecular "
        "graphs to delineate favorable hinge-binding pharmacophores in chartreuse and steric penalties in crimson. "
        "Candidate compounds are concurrently assessed for oral bioavailability via Lipinski's Rule of Five [4] and "
        "Veber's rules [5], benchmarked for structural similarity against approved clinical EGFR therapeutics (Gefitinib, "
        "Dacomitinib, Erlotinib, Afatinib, Lapatinib, Osimertinib), and reasoned through an offline local Large Language "
        "Model. This integrated workflow delivers an actionable, transparent screening pipeline that substantially reduces "
        "experimental costs in precision oncology."
    )
    keywords_str = (
        "Cheminformatics; Machine Learning; Explainable AI (XAI); EGFR Tyrosine Kinase; Non-Small Cell Lung "
        "Cancer (NSCLC); TreeSHAP; Morgan Fingerprints (ECFP4); Random Forest; Gradient Boosting; Drug Discovery; "
        "Virtual Screening."
    )
    
    add_callout_box(doc, "ABSTRACT", [ab_p1, ab_p2, ab_p3], keywords_str)
    doc.add_page_break()

    # =========================================================================
    # SECTION 1: INTRODUCTION & RESEARCH MOTIVATION
    # =========================================================================
    add_heading_1(doc, "1. INTRODUCTION & RESEARCH MOTIVATION")
    
    add_heading_2(doc, "1.1 The Economics and Attrition of Modern Drug Discovery")
    add_body_p(
        doc,
        "The translation of a novel chemical entity into an approved therapeutic drug typically spans 10 to 15 years "
        "and demands capital investments exceeding $2.6 billion per clinical success [20], [21]. In conventional wet-lab "
        "High-Throughput Screening (HTS), microtiter assay plates are robotically filled with purified target enzymes and "
        "candidate small molecules, testing compounds blindly across vast chemical spaces. The empirical cost per biological "
        "assay ranges from $10 to $500 per compound, consuming millions of dollars in early exploratory phases while suffering "
        "a staggering clinical attrition rate exceeding 90% [21]. The primary culprits behind this attrition are poor "
        "pharmacokinetics, unanticipated off-target toxicities, or insufficient on-target binding affinity [4], [5]. Virtual "
        "High-Throughput Screening (vHTS) through machine learning acts as an intelligent computational sieve, ranking millions "
        "of molecules in silico within milliseconds to prioritize high-affinity leads prior to physical synthesis [20]."
    )
    
    add_heading_2(doc, "1.2 Oncogenic EGFR Kinase Signaling in Lung Cancer")
    add_body_p(
        doc,
        "Lung cancer, particularly Non-Small Cell Lung Cancer (NSCLC), is the leading cause of oncological mortality worldwide, "
        "accounting for over 1.8 million deaths annually [24]. Approximately 15% to 50% of NSCLC patients exhibit somatic "
        "activating mutations within the intracellular tyrosine kinase domain of the Epidermal Growth Factor Receptor (EGFR / "
        "ErbB-1), such as the exon 19 in-frame deletion (delE746-A750) or the exon 21 L858R point substitution [11], [24]. "
        "Under physiological conditions, ligand binding by Epidermal Growth Factor (EGF) stimulates receptor dimerization and "
        "autophosphorylation of key regulatory tyrosine residues [24]. This autophosphorylation hyperactivates two principal "
        "downstream signal transduction pathways:\n"
        "1. MAPK/ERK Cascade: Governs transcriptional activation, driving unchecked cellular proliferation.\n"
        "2. PI3K/AKT Cascade: Inhibits pro-apoptotic bad/caspase pathways, conferring malignant cellular survival."
    )
    add_body_p(
        doc,
        "While first-generation Tyrosine Kinase Inhibitors (TKIs) like Gefitinib (Iressa) and Erlotinib (Tarceva) demonstrated "
        "notable initial clinical remission, secondary resistance mutations (most prominently the gatekeeper T790M substitution "
        "and tertiary C797S mutations) inevitably cause therapeutic relapse [11], [12]. Consequently, discovering structurally "
        "novel, patentable chemotypes that inhibit wild-type and mutant EGFR variants remains an urgent therapeutic priority [12]."
    )
    
    add_heading_2(doc, "1.3 The Black-Box Challenge in Biomedical Artificial Intelligence")
    add_body_p(
        doc,
        "Although advanced deep neural networks and ensemble learning algorithms deliver formidable statistical accuracy in "
        "bioactivity classification [9], [10], their translation into medicinal chemistry has been severely hindered by model "
        "opacity [22]. Medicinal chemists cannot rationally optimize a chemical scaffold based on an uninterpretable probability "
        "score alone. Without localized structural rationale delineating which specific pharmacophoric rings or substituents govern "
        "target binding, researchers cannot make informed chemical modifications [1], [2]. This investigation directly resolves "
        "this challenge by wedding predictive machine learning ensembles with cooperative game-theoretic explainability (TreeSHAP) "
        "[1], [2], projecting model decisions directly onto physical 2D chemical topologies."
    )
    
    add_heading_2(doc, "1.4 End-to-End System Pipeline Architecture")
    add_body_p(
        doc,
        "The platform is engineered as a modular, six-stage pipeline spanning chemical ingestion, featurization, ensemble "
        "classification, game-theoretic explainability, and multi-objective lead reporting [7], [8], [9], [14]:"
    )
    add_figure(doc, FIG1_PNG, "Fig 1: End-to-End Explainable Virtual Screening Architecture for Human EGFR (CHEMBL203).", width_inches=5.8)
    
    add_heading_2(doc, "1.5 Summary of Key Technical Contributions")
    add_body_p(
        doc,
        "1. Curated ChEMBL203 Benchmark: Harvested, cleaned, and standardized bioactivity assays from the EMBL-EBI ChEMBL "
        "database [8], enforcing a rigorous IC50 <= 1,000 nM active boundary with removal of ambiguous boundary noise.\n"
        "2. High-Performance Supervised Ensembles: Formulated Random Forest (RF) [9] and Gradient Boosted Decision Tree (GBDT) "
        "[10] models achieving 90.96% and 91.53% test accuracy with 0.978 and 0.968 ROC-AUC on unseen held-out validation sets.\n"
        "3. Topological Atom-Level TreeSHAP Mapping: Developed a spatial deconvolution algorithm that maps computed polynomial "
        "Shapley values [1], [2] to physical 2D atom coordinates using RDKit bitInfo [6], [7], illuminating favorable hinge-binding "
        "anchors in chartreuse and steric penalties in crimson.\n"
        "4. Multi-Parameter Oral Bioavailability Screening: Integrated Lipinski's Rule of Five [4] and Veber's oral absorption "
        "scorecards [5] with normalized polar radar profiling.\n"
        "5. Clinical Drug Homology Benchmarking: Engineered a comparative Tanimoto similarity index [6] against 6 FDA-approved "
        "EGFR inhibitors (Gefitinib, Dacomitinib, Erlotinib, Afatinib, Lapatinib, Osimertinib) [11], [12].\n"
        "6. Offline Edge AI Reasoning & Automated Dossier: Embedded a local Ollama LLM chemoinformatics tutor and ReportLab PDF "
        "reporting engine wrapped in a dark editorial UI."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 2: RELATED WORK & LITERATURE REVIEW
    # =========================================================================
    add_heading_1(doc, "2. RELATED WORK & LITERATURE REVIEW")
    
    add_heading_2(doc, "2.1 Evolution of Quantitative Structure-Activity Relationships (QSAR)")
    add_body_p(
        doc,
        "The quantitative correlation of chemical structure with biological efficacy was pioneered by Corwin Hansch in 1962, "
        "utilizing linear regression over octanol-water partition coefficients (LogP) and Hammett electronic constants [15]. As "
        "computational power expanded in the 1990s, Structure-Based Drug Design (SBDD) gained prominence through molecular docking "
        "algorithms such as AutoDock and Glide [20]. Although molecular docking simulates explicit physical binding poses within "
        "protein crystallographic coordinates, it remains computationally demanding, prone to false-positive free energy estimates, "
        "and sensitive to rigid receptor assumptions [20]. Conversely, Ligand-Based Virtual Screening (LBVS) leverages empirical "
        "bioactivity databases [8] to learn complex, non-linear decision boundaries directly from molecular topology, enabling "
        "the rapid screening of millions of molecules in seconds [21]."
    )
    
    add_heading_2(doc, "2.2 Soft Computing and Ensemble Methods in Bioinformatics")
    add_body_p(
        doc,
        "The application of soft computing, genetic algorithms, and supervised ensemble learning to biomedical data science has "
        "been extensively championed by pioneering researchers such as Prof. Sanghamitra Bandyopadhyay (Director, Indian Statistical "
        "Institute, Kolkata) [3]. Her foundational research demonstrated that biological datasets (distinguished by extreme feature "
        "dimensionality, inherent assay noise, and complex epistatic interactions) cannot be adequately captured by simplistic "
        "linear models [3]. Bandyopadhyay and Saha established that ensemble clustering and multi-objective optimization techniques "
        "robustly circumvent local optima, providing superior generalization across high-dimensional genomic and proteomic "
        "landscapes [3]. Supervised decision tree ensembles like Random Forests [9] and Gradient Boosting [10] build directly on "
        "these paradigms, providing robust variance reduction over high-dimensional sparse molecular spaces [14]."
    )
    
    add_heading_2(doc, "2.3 Explainable Artificial Intelligence (XAI) in Clinical Decision-Making")
    add_body_p(
        doc,
        "To address the critical deficit of interpretability in healthcare AI, Ribeiro et al. introduced LIME (Local Interpretable "
        "Model-agnostic Explanations) [22], which approximates local decision boundaries using perturbed linear surrogates. In 2017, "
        "Scott Lundberg and Su-In Lee proposed SHAP (SHapley Additive exPlanations) [1], uniting cooperative game theory [23] with "
        "additive feature attributions to provide mathematically unique, locally accurate, and globally consistent feature importance "
        "values. Lundberg et al. subsequently developed TreeSHAP in 2020 [2], enabling exact polynomial-time calculation of Shapley "
        "values for tree ensembles. While TreeSHAP has seen wide adoption in tabular clinical domains, prevailing chemoinformatics "
        "literature rarely projects abstract circular fingerprint bit contributions back onto physical chemical graph topologies [1], [6], [7]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 3: BIOLOGICAL TARGET & DATASET CURATION
    # =========================================================================
    add_heading_1(doc, "3. BIOLOGICAL TARGET ANATOMY & DATASET CURATION PROTOCOL")
    
    add_heading_2(doc, "3.1 Anatomy of Human EGFR Tyrosine Kinase Domain")
    add_body_p(
        doc,
        "Human EGFR (erbB-1 / HER1) is a 170 kDa transmembrane glycoprotein belonging to the ErbB family of receptor tyrosine kinases [24]. "
        "The intracellular catalytic domain (residues 690-953) adopts a canonical bi-lobed architecture: a smaller N-terminal lobe primarily "
        "composed of five-stranded beta-sheets and the regulatory alphaC-helix, and a larger C-terminal lobe consisting predominantly of "
        "alpha-helices [11], [24]. Adenosine triphosphate (ATP) binds in the deep inter-lobar cleft between the two lobes [11]. Competitive "
        "Tyrosine Kinase Inhibitors (TKIs) insert directly into this nucleotide cleft, mimicking the purine ring of ATP and establishing critical "
        "directional hydrogen bonds with the backbone amide and carbonyl atoms of hinge region residue Met793 [11], [12]."
    )
    
    add_heading_2(doc, "3.2 ChEMBL203 Bioactivity Extraction and Normalization Protocol")
    add_body_p(
        doc,
        "Experimental bioactivity assays for the target identifier CHEMBL203 (Human Epidermal Growth Factor Receptor) were extracted from the "
        "EMBL-EBI ChEMBL repository (Version 33) [8] via its official REST API. The curation and standardization protocol enforced the following criteria [8], [20]:\n"
        "1. Bioactivity Assay Filter: Retained only biochemical binding affinity assays where the standard measurement type is strictly equal to "
        "half-maximal inhibitory concentration (IC50) measured in nanomolar (nM) [8].\n"
        "2. Logarithmic Transformation (pIC50): Absolute IC50 concentrations were transformed into standard negative logarithmic potency:\n"
        "pIC50 = 9 - log10(IC50) [20].\n"
        "3. Binary Classification Discretization: Compounds with IC50 <= 1,000 nM (pIC50 >= 6.0) were designated as Active (y = 1), representing "
        "potent micromolar inhibitors. Compounds with IC50 >= 10,000 nM (pIC50 <= 5.0) were designated as Inactive (y = 0). Intermediate compounds "
        "with ambiguous affinity (1,000 nM < IC50 < 10,000 nM) were systematically excluded to eliminate boundary label noise [20].\n"
        "4. Chemical Hygiene and De-duplication: SMILES representations were canonicalized using RDKit [7]. Counter-ions, inorganic salts, and solvent "
        "fragments were stripped. Replicate SMILES records were collapsed by computing the geometric mean of replicate IC50 measurements.\n"
        "The curated benchmark contains 881 unique chemical entities (472 Actives, 409 Inactives)."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 4: MULTI-SCALE FEATURIZATION & CONFORMATION
    # =========================================================================
    add_heading_1(doc, "4. MULTI-SCALE MOLECULAR FEATURIZATION & CONFORMATION")
    
    add_heading_2(doc, "4.1 Extended Connectivity Circular Fingerprints (ECFP4)")
    add_body_p(
        doc,
        "To represent small molecules numerically, compounds are treated as undirected topological graphs G = (V, E), where vertices V "
        "correspond to heavy atoms and edges E correspond to covalent bonds [6], [7]. The Morgan circular fingerprint algorithm iteratively "
        "computes radial neighborhoods up to radius r = 2 (ECFP4, capturing chemical substructures across diameters of up to 4 bonds) [6]:"
    )
    add_formula_block(doc, "ID_v^(r) = Hash( ID_v^(r-1),  SUM [ BondOrder(v, u),  ID_u^(r-1) ] )")
    add_body_p(
        doc,
        "Atomic identifiers are initialized with Daylight invariant properties (atomic number, heavy valence, formal charge, hydrogen count, "
        "aromaticity) [6]. The hashed integer identifiers across all atoms and radii are folded into a dense binary bit vector of fixed length "
        "2,048 bits using modulo arithmetic [6]. A bit value of 1 denotes the presence of a specific pharmacophoric motif."
    )
    
    add_heading_2(doc, "4.2 Physicochemical Molecular Property Descriptors")
    add_body_p(
        doc,
        "To capture global molecular properties not explicitly encoded by localized circular fingerprints, 8 standardized physicochemical "
        "descriptors are extracted via RDKit [7], [13], [15], [16], [17]:"
    )
    
    desc_rows = [
        ("Descriptor", "Property & Units", "Clinical Role in Virtual Screening"),
        ("MolWt [4]", "Molecular Weight (Da)", "Controls steric cavity fit and passive membrane diffusion"),
        ("MolLogP [15]", "Wildman-Crippen LogP", "Lipophilicity metric; governs intestinal absorption and clearance"),
        ("TPSA [16]", "Polar Surface Area (A^2)", "Predicts cell permeability and blood-brain barrier penetration"),
        ("NumHDonors [4]", "Count of -OH / -NH groups", "Directional hydrogen-bond donors targeting hinge residues"),
        ("NumHAcceptors [4]", "Count of -O- / -N- atoms", "Hydrogen-bond acceptors stabilizing ATP binding pocket"),
        ("NumRotBonds [5]", "Rotatable Single Bonds", "Conformational flexibility; excess entropy penalizes binding"),
        ("QED [13]", "Quantitative Drug-Likeness [0, 1]", "Composite desirability index reflecting oral clinical success"),
        ("FractionCSP3 [17]", "Ratio of sp3 Carbons", "3D complexity; higher saturation correlates with clinical safety")
    ]
    tbl_desc = doc.add_table(rows=len(desc_rows), cols=3)
    tbl_desc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_desc)
    for r_idx, (c1, c2, c3) in enumerate(desc_rows):
        row = tbl_desc.rows[r_idx]
        row.cells[0].width = Inches(1.5)
        row.cells[1].width = Inches(1.8)
        row.cells[2].width = Inches(3.2)
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        if r_idx == 0:
            for c in row.cells:
                set_cell_shading(c, "F1F5F9")
                for p in c.paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(9.5)
        else:
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9)
                        
    add_body_p(
        doc,
        "The 8 continuous descriptors are standardized via StandardScaler (zero mean, unit variance) [14] and concatenated with the "
        "2,048 Morgan bits, yielding a comprehensive composite feature vector x in R^2056."
    )
    
    add_heading_2(doc, "4.3 Energy-Minimized 3D Conformation Engine")
    add_body_p(
        doc,
        "Because planar 2D representations cannot convey spatial steric clashes within the ATP binding cleft, our framework embeds "
        "molecules in 3D Euclidean space using the ETKDGv3 (Experimental-Torsion Knowledge-based Distance Geometry) algorithm [18]. Initial "
        "distance-geometry conformations are subsequently relaxed to their lowest energy state using the Merck Molecular Force Field 1994 (MMFF94) [19]:"
    )
    add_formula_block(doc, "E_total = E_stretch + E_angle + E_torsion + E_oop + E_van_der_Waals + E_electrostatic")
    add_figure(doc, FIG2_PNG, "Fig 2: 2D Vector Chemical Architecture of Gefitinib (Iressa) generated via RDKit [7].", width_inches=4.8)
    add_body_p(
        doc,
        "As illustrated in Figure 2, the chemical scaffold of Gefitinib features the planar 4-anilinoquinazoline bicyclic core that mimics "
        "the purine ring of ATP [11], a 3-chloro-4-fluoroaniline pharmacophore that inserts into the hydrophobic selectivity pocket [11], "
        "and a flexible morpholine propoxy side-chain extending into solvent to enhance aqueous solubility [4], [5]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 5: SUPERVISED ENSEMBLE CLASSIFIERS
    # =========================================================================
    add_heading_1(doc, "5. SUPERVISED MACHINE LEARNING ENSEMBLE FORMULATION")
    
    add_heading_2(doc, "5.1 Random Forest (RF) Bagging Formulation")
    add_body_p(
        doc,
        "Random Forest [9] constructs an ensemble of B = 100 decorrelated decision trees using bootstrap aggregating (bagging). At each candidate "
        "split, a random subset of m = sqrt(M) features is evaluated [9], [14]. For classification into active (y=1) versus inactive (y=0) inhibitors, "
        "the final predicted binding probability is the consensus expectation:"
    )
    add_formula_block(doc, "P(y = 1 | x) = (1 / B) * SUM[ T_b(x) ]")
    add_body_p(
        doc,
        "Random Forests exhibit exceptional resistance against overfitting on sparse binary Morgan bit vectors [6], reducing generalization "
        "variance without inflating bias [9]."
    )
    
    add_heading_2(doc, "5.2 Gradient Boosted Decision Trees (GBDT) Formulation")
    add_body_p(
        doc,
        "Gradient Boosting [10] constructs an additive ensemble model in a forward stage-wise manner by minimizing binary cross-entropy loss over "
        "the training distribution [10], [14]:"
    )
    add_formula_block(doc, "L(y, p) = - [ y * ln(p) + (1 - y) * ln(1 - p) ]")
    add_body_p(
        doc,
        "At each iteration m, a shallow regression tree h_m(x) is fit to the pseudo-residuals of the existing ensemble. The updated model is formulated as:"
    )
    add_formula_block(doc, "F_m(x) = F_{m-1}(x) + eta * h_m(x)")
    add_body_p(
        doc,
        "where eta = 0.1 is the shrinkage learning rate [10]. GBDT excels at discovering complex non-linear interaction thresholds between "
        "continuous physicochemical descriptors and topological fingerprints [10], [14]."
    )
    
    add_heading_2(doc, "5.3 Stratified Training & Validation Protocol")
    add_body_p(
        doc,
        "The curated dataset of 881 compounds was partitioned into an 80% training set (704 compounds) and a 20% holdout test set (177 compounds) "
        "using stratified sampling on label y to preserve empirical class proportions [14]. Feature scalers were fit strictly on training partitions "
        "to prevent data leakage [14]. Model hyper-parameters were tuned via 5-fold stratified cross-validation."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 6: GAME-THEORETIC EXPLAINABILITY (TREESHAP)
    # =========================================================================
    add_heading_1(doc, "6. COOPERATIVE GAME-THEORETIC EXPLAINABILITY (TREESHAP)")
    
    add_heading_2(doc, "6.1 Shapley Value Axiomatic Foundation")
    add_body_p(
        doc,
        "Rooted in Lloyd Shapley's cooperative game theory (1953) [23], Shapley values represent the unique feature attribution method that "
        "simultaneously satisfies four fundamental mathematical axioms: Efficiency, Symmetry, Dummy (Null player), and Additivity [1], [23]. "
        "The marginal contribution of feature i across all possible feature subsets S subset N \\ {i} is defined as:"
    )
    add_formula_block(doc, "phi_i(v) = SUM [ |S|! (|N| - |S| - 1)! / |N|! ] * [ v(S U {i}) - v(S) ]")
    add_body_p(
        doc,
        "In this virtual screening framework, players N correspond to the 2,056 input molecular variables [6], the game payout v(S) represents the "
        "ensemble's predicted probability of EGFR inhibition P(Active) [9], [10], and phi_i quantifies the exact directional influence of feature i "
        "toward the final prediction [1]."
    )
    
    add_heading_2(doc, "6.2 Polynomial-Time TreeSHAP Algorithm")
    add_body_p(
        doc,
        "While model-agnostic KernelSHAP requires exponential computational sampling O(2^|N|) [1], the TreeSHAP algorithm formulated by Lundberg et al. "
        "(2020) [2] evaluates exact conditional expectations by recursively tracking feature split paths through decision tree branches in polynomial "
        "time O(T * L * D^2), where T is tree count, L is maximum leaf count, and D is maximum tree depth [2]. This algorithmic efficiency enables "
        "instantaneous, sub-second explainability in interactive web screening applications [2]."
    )
    
    add_heading_2(doc, "6.3 Topological Substructure Deconvolution Algorithm")
    add_body_p(
        doc,
        "Because Morgan circular fingerprints represent localized concentric atomic neighborhoods [6], our framework maps computed Shapley values "
        "back to physical 2D atom coordinates using RDKit's bitInfo dictionary [7]:\n"
        "1. For each active fingerprint bit j with Shapley attribution phi_j, the central atom index v and radius r are retrieved [6], [7].\n"
        "2. The attribution is distributed across constituent atomic coordinates: AtomScore(v) = SUM[ phi_j * w(r) ].\n"
        "3. Normalized atom scores are mapped to RGB visual highlights on the molecular graph [7]:\n"
        "- Chartreuse Highlights (phi > 0): Positive pharmacophores shifting prediction toward EGFR inhibition.\n"
        "- Crimson Highlights (phi < 0): Unfavorable substituents penalizing predicted binding affinity."
    )
    add_figure(doc, FIG3_PNG, "Fig 3: Atom-Level SHAP Highlight Map for Gefitinib. Chartreuse regions identify primary hinge-binding pharmacophores.", width_inches=4.8)
    add_body_p(
        doc,
        "As documented in the project poster, the top positive SHAP feature drivers for EGFR inhibition include:\n"
        "- ECFP4_Bit_489 (+0.0299): Quinazoline nitrogen heteroatom participating in hinge hydrogen bonding with Met793 [11].\n"
        "- ECFP4_Bit_708 (+0.0248): Halogenated aniline aromatic ring mediating hydrophobic pocket packing [11].\n"
        "- ECFP4_Bit_491 (+0.0243): Secondary amine linker anchoring the core scaffold with Met793 [11].\n"
        "- Additional key drivers: Bit 1226 (+0.0234), Bit 1367 (+0.0234), Bit 794 (+0.0218), Bit 1157 (+0.0213), Bit 329 (+0.0186)."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 7: ORAL DRUG-LIKENESS & ADMET PROFILING
    # =========================================================================
    add_heading_1(doc, "7. ORAL DRUG-LIKENESS & ADMET BIOAVAILABILITY PROFILING")
    
    add_heading_2(doc, "7.1 Lipinski's Rule of Five Heuristic")
    add_body_p(
        doc,
        "Christopher Lipinski et al. (2001) demonstrated that poor oral absorption and low gastrointestinal permeability are significantly "
        "more prevalent when a drug candidate violates more than one of the following four criteria [4]:\n"
        "1. Molecular Weight (MolWt) <= 500 Da: Bulky molecules suffer reduced aqueous diffusion and poor membrane transport [4].\n"
        "2. Lipophilicity (MolLogP) <= 5.0: Excessive hydrophobicity leads to poor aqueous solubility, non-specific binding, and rapid metabolic clearance [4], [15].\n"
        "3. Hydrogen Bond Donors (HBD) <= 5: Excessive -OH and -NH groups incur steep desolvation penalties when crossing lipid bilayers [4].\n"
        "4. Hydrogen Bond Acceptors (HBA) <= 10: Abundant electronegative nitrogen and oxygen atoms hinder passive membrane transit [4]."
    )
    
    add_heading_2(doc, "7.2 Veber's Permeability & Flexibility Criteria")
    add_body_p(
        doc,
        "Daniel Veber et al. (2002) established that molecular flexibility and polar surface area are superior predictors of oral bioavailability "
        "in rats and humans [5]:\n"
        "- Rotatable Bonds <= 10: High conformational flexibility imposes conformational entropic penalties upon receptor binding [5].\n"
        "- Topological Polar Surface Area (TPSA) <= 140 A^2: Polar surface area exceeding 140 A^2 severely diminishes passive oral bioavailability [5], [16]."
    )
    
    add_heading_2(doc, "7.3 Multi-Parameter Evaluation Matrix")
    
    dl_rows = [
        ("Compound", "MolWt (Da)", "MolLogP", "HBD", "HBA", "TPSA (A^2)", "RotB", "Rule Compliance"),
        ("Gefitinib [11]", "446.91", "4.28", "1", "7", "68.7", "8", "PASS (0 violations)"),
        ("Dacomitinib", "469.95", "4.35", "1", "7", "70.9", "6", "PASS (0 violations)"),
        ("Erlotinib [24]", "393.44", "3.41", "1", "6", "74.7", "8", "PASS (0 violations)"),
        ("Afatinib [12]", "485.94", "3.92", "2", "8", "81.8", "8", "PASS (0 violations)"),
        ("Lapatinib [24]", "581.06", "5.38", "2", "7", "114.3", "9", "FAIL (2 violations)")
    ]
    tbl_dl = doc.add_table(rows=len(dl_rows), cols=8)
    tbl_dl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_dl)
    for r_idx, r_vals in enumerate(dl_rows):
        row = tbl_dl.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            row.cells[c_idx].text = val
            if r_idx == 0:
                set_cell_shading(row.cells[c_idx], "F1F5F9")
                for p in row.cells[c_idx].paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(8.5)
            else:
                for p in row.cells[c_idx].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(8.5)
                        
    add_heading_2(doc, "7.4 Normalized Bioavailability Radar Profiling")
    add_body_p(
        doc,
        "To enable immediate visual evaluation of multi-parameter drug-likeness, the 6 core oral bioavailability descriptors are normalized "
        "against their standard upper threshold boundaries (Boundary = 1.0) [4], [5]:"
    )
    add_figure(doc, FIG5_PNG, "Fig 5: Polar Bioavailability Radar Profile. Green polygon depicts Gefitinib within the red dashed oral boundary.", width_inches=4.4)
    add_body_p(
        doc,
        "As depicted in Figure 5, the query molecule Gefitinib produces a polygon that resides entirely within the red dashed threshold boundary "
        "across all 6 axes, confirming favorable oral pharmacokinetic bioavailability without necessitating structural modification [4], [5]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 8: APPROVED DRUG SIMILARITY BENCHMARKING (TANIMOTO)
    # =========================================================================
    add_heading_1(doc, "8. APPROVED DRUG SIMILARITY BENCHMARKING (TANIMOTO)")
    
    add_heading_2(doc, "8.1 Tanimoto Coefficient Formulation")
    add_body_p(
        doc,
        "The Tanimoto (Jaccard) similarity coefficient [3], [6] between a query molecule's 2,048-bit ECFP4 fingerprint vector A and a reference "
        "clinical drug vector B is calculated as:"
    )
    add_formula_block(doc, "T_c(A, B) = |A INTERSECT B| / |A UNION B| = c / (a + b - c)")
    add_body_p(
        doc,
        "where c is the count of coincident active bits, and a, b are the total bit counts for vectors A and B, respectively [6]. Queries are "
        "benchmarked against 6 clinically approved EGFR cancer therapeutics [11], [12]:"
    )
    add_figure(doc, FIG6_PNG, "Fig 6: Tanimoto Structural Similarity Index (%) against FDA-Approved EGFR Tyrosine Kinase Inhibitors (matching poster).", width_inches=5.2)
    add_body_p(
        doc,
        "The empirical Tanimoto alignment reflects precise pharmacological relationships:\n"
        "- Gefitinib (Iressa): 100.0% identity against itself [11].\n"
        "- Dacomitinib (Vizimpro): 44.1% similarity, sharing the 4-anilinoquinazoline core with an acrylamide warhead [12].\n"
        "- Erlotinib (Tarceva): 40.8% similarity, retaining the quinazoline core with bis-alkoxy sidechains [24].\n"
        "- Afatinib (Gilotrif): 38.1% similarity, reflecting second-generation irreversible quinazoline conservation [12].\n"
        "- Lapatinib (Tykerb): 31.7% similarity, reflecting dual EGFR/HER2 inhibition with bulkier fluorobenzyloxy substituents.\n"
        "- Osimertinib (Tagrisso): 15.0% similarity, structurally diverging into a third-generation indole-pyrimidine covalent scaffold [12]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 9: SYSTEM IMPLEMENTATION & OLLAMA LLM
    # =========================================================================
    add_heading_1(doc, "9. SYSTEM IMPLEMENTATION, HERBARIUM UI & OLLAMA LLM")
    
    add_heading_2(doc, "9.1 Herbarium Alpinum Editorial Design System")
    add_body_p(
        doc,
        "The web interface is implemented in Streamlit, styled under the HERBARIUM ALPINUM - The Edelweiss Folio design specification. It departs "
        "from generic commercial dashboards in favor of an authoritative scientific workspace [22]:\n"
        "- Base Surfaces: Deep technical surfaces (#000000, #080e0a) with dark botanical card panels (#101811) and muted forest-green borders (#35402f).\n"
        "- Typography: Pale botanical chalk (#e6e9d9) adhering to WCAG 2.2 AA contrast standards (> 4.5:1 ratio).\n"
        "- Interactive Accent: Fluorescent chartreuse (#99ff00) reserved exclusively for active predictions, positive SHAP anchors, and primary CTA actions."
    )
    
    add_heading_2(doc, "9.2 Local Offline Ollama LLM Chemoinformatics Tutor")
    add_body_p(
        doc,
        "To assist students and non-specialist evaluators in interpreting complex pharmacology, the application integrates a local offline LLM daemon "
        "via Ollama (http://127.0.0.1:11434/api/generate) running gemma3:1b. The daemon dynamically ingests calculated descriptors, predicted "
        "probabilities, and top SHAP feature drivers into a structured prompt context, outputting clear, plain-language mechanistic explanations "
        "without exposing sensitive chemical data to cloud servers."
    )
    
    add_heading_2(doc, "9.3 Automated Vector PDF Reporting Engine")
    add_body_p(
        doc,
        "The platform compiles comprehensive publication-ready PDF screening dossiers on demand in under 2 seconds via ReportLab, encapsulating vector "
        "2D structures [7], calibrated ensemble probabilities [9], [10], Lipinski rule evaluations [4], and clinical homology benchmarks [6]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 10: EXPERIMENTAL RESULTS & BENCHMARKS
    # =========================================================================
    add_heading_1(doc, "10. EXPERIMENTAL RESULTS & BENCHMARK DISCUSSION")
    
    add_heading_2(doc, "10.1 Empirical Holdout Test Set Performance Metrics")
    add_body_p(
        doc,
        "Models were trained on 704 curated compounds and evaluated on a holdout test set of 177 unseen chemical compounds from ChEMBL203 [8] "
        "(matching the approved poster metrics):"
    )
    
    res_rows = [
        ("Model Classifier", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"),
        ("Random Forest (RF) [9]", "90.96%", "91.67%", "91.67%", "0.9167", "0.9778"),
        ("Gradient Boosting (GBDT) [10]", "91.53%", "93.55%", "90.62%", "0.9206", "0.9675")
    ]
    tbl_res = doc.add_table(rows=len(res_rows), cols=6)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_res)
    for r_idx, r_vals in enumerate(res_rows):
        row = tbl_res.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            row.cells[c_idx].text = val
            if r_idx == 0:
                set_cell_shading(row.cells[c_idx], "F1F5F9")
                for p in row.cells[c_idx].paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(9)
            else:
                for p in row.cells[c_idx].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9)
                        
    add_heading_2(doc, "10.2 Empirical Metric Analysis & Calibration")
    add_body_p(
        doc,
        "Both ensemble classifiers decisively exceed our initial project target of 0.80 ROC-AUC [20]. Gradient Boosting achieved slightly higher "
        "test accuracy (91.53%) and precision (93.55%), effectively minimizing false-positive lead classifications [10]. Conversely, Random Forest "
        "delivered superior discrimination across the full threshold spectrum with an outstanding ROC-AUC of 0.9778 [9]. The balanced recall rates "
        "(91.67% and 90.62%) verify that the models reliably capture true active kinase inhibitors while maintaining a low false-alarm rate under 8.5% [9], [10]."
    )
    add_figure(doc, FIG4_PNG, "Fig 4: Holdout ROC Curves for Random Forest (AUC = 0.978) and Gradient Boosting (AUC = 0.968).", width_inches=4.4)
    
    add_heading_2(doc, "10.3 Comparative Case Studies: Active Lead vs. Negative Control")
    add_body_p(
        doc,
        "- Gefitinib (Approved EGFR TKI) [11]: Classified Active with P(Active) = 99.8%. SHAP feature attribution identified the 4-anilinoquinazoline "
        "core (ECFP4_Bit_489, phi = +0.0299) and 3-chloro-4-fluoroaniline moiety (ECFP4_Bit_708, phi = +0.0248) as top positive drivers, matching "
        "crystallographic hinge-binding interactions with Met793 [11].\n"
        "- Aspirin (Negative Control): Classified Inactive with P(Active) = 7.7%. SHAP identified low molecular weight (180 Da) and the charged carboxylate "
        "group (phi = -0.0982) as severe penalties, producing electrostatic repulsion within the hydrophobic ATP pocket."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 11: UNIVERSITY CURRICULUM ALIGNMENT
    # =========================================================================
    add_heading_1(doc, "11. UNIVERSITY CURRICULUM ALIGNMENT (UNITS I TO V)")
    add_body_p(doc, "This mini-project directly maps to the university AI Systems and Applications curriculum:")
    
    syl_rows = [
        ("Syllabus Unit", "Curriculum Concept", "Implementation in Proposed Project"),
        ("UNIT-I", "Key Components of AI Systems & Narrow AI", "Domain-specific Narrow AI for oncology problem solving; observes bioethics against clinical over-extrapolation [20]."),
        ("UNIT-II", "ML Frameworks & Supervised Learning", "End-to-end data pipeline using Pandas, NumPy, and Scikit-learn [14]; trained Random Forest [9] and GBDT [10] ensembles."),
        ("UNIT-III", "Graph Theory, LLMs & Explainable AI", "Molecules as graphs G=(V,E) via 2048-bit ECFP4 [6]; local Ollama LLM tutor; game-theoretic SHAP TreeExplainer [1], [2]."),
        ("UNIT-IV", "AI Applications in Healthcare", "Direct precision oncology application targeting EGFR in NSCLC [24], drastically reducing wet-lab screening costs [21]."),
        ("UNIT-V", "Historical AI Milestones & Case Studies", "Modern parallel to IBM Watson Health, DeepMind AlphaFold, and predictive disease biomarker systems [3], [21].")
    ]
    tbl_syl = doc.add_table(rows=len(syl_rows), cols=3)
    tbl_syl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_syl)
    for r_idx, (c1, c2, c3) in enumerate(syl_rows):
        row = tbl_syl.rows[r_idx]
        row.cells[0].width = Inches(1.2)
        row.cells[1].width = Inches(2.2)
        row.cells[2].width = Inches(3.1)
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        if r_idx == 0:
            for c in row.cells:
                set_cell_shading(c, "F1F5F9")
                for p in c.paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(9)
        else:
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9)
                        
    doc.add_page_break()

    # =========================================================================
    # SECTION 12: DISCUSSION, ADVANTAGES & LIMITATIONS
    # =========================================================================
    add_heading_1(doc, "12. DISCUSSION, TECHNOLOGICAL ADVANTAGES & LIMITATIONS")
    
    add_heading_2(doc, "12.1 Key Technological Advantages")
    add_body_p(
        doc,
        "1. High-Throughput Acceleration: Evaluates compounds in silico in under 50 milliseconds, bypassing months of physical assay preparation [20].\n"
        "2. Transparent Lead Optimization: Atom-level TreeSHAP highlights provide chemists with actionable feedback on which functional groups enhance or penalize binding [1], [2].\n"
        "3. Concurrent Bioavailability Screening: Evaluates target binding affinity alongside Lipinski and Veber oral absorption heuristics to reject insoluble hits [4], [5].\n"
        "4. Complete On-Premise Privacy: The local Ollama LLM and Python inference run entirely offline with zero third-party cloud data exposure."
    )
    
    add_heading_2(doc, "12.2 Critical Methodological Limitations")
    add_body_p(
        doc,
        "1. 2D Graph Topological Invariance: Morgan fingerprints encode 2D circular connectivity but do not explicitly account for flexible protein backbone induced-fit dynamics or quantum mechanical polarization [6], [20].\n"
        "2. Binary Potency Discretization: Continuous affinity is binarized (IC50 <= 1,000 nM vs >= 10,000 nM), omitting weakly active molecules (1,000-10,000 nM) [20].\n"
        "3. Target Selectivity Boundary: The model is trained on Human EGFR (CHEMBL203) [8] and does not predict broader off-target kinome selectivity across related kinases (HER2, HER4, VEGFR2) [24]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 13: CONCLUSION & FUTURE RESEARCH DIRECTIONS
    # =========================================================================
    add_heading_1(doc, "13. CONCLUSION & FUTURE RESEARCH DIRECTIONS")
    
    add_heading_2(doc, "13.1 Research Conclusions")
    add_body_p(
        doc,
        "In this mini-project for AI Systems and Applications at MIT World Peace University (MIT-WPU), Pune, conducted under the mentorship "
        "of Dr. Devendra Joshi, an end-to-end, interpretable computational screening platform, EGFR Molecular Intelligence, was successfully "
        "formulated, implemented, and empirically validated."
    )
    add_body_p(
        doc,
        "By combining RDKit chemoinformatics [7], 2,048-bit Morgan circular graph representations [6], and supervised tree ensemble models [9], [10], "
        "the system achieved 90.96% accuracy and 0.978 ROC-AUC on a curated benchmark of 881 ChEMBL compounds [8]. Integrating polynomial TreeSHAP "
        "game theory [1], [2] resolved the black-box dilemma by projecting atom-level binding explanations directly onto 2D molecular graphs [7]. "
        "Supported by Lipinski oral bioavailability radar charts [4], clinical Tanimoto similarity indexing [6], an embedded local Ollama LLM "
        "tutor, and automated PDF reporting, this platform demonstrates the transformative power of Explainable AI in precision oncology [21]."
    )
    
    add_heading_2(doc, "13.2 Future Scope & Research Roadmap (from Approved Poster)")
    add_body_p(
        doc,
        "- Screen Larger & Diverse Libraries: Expand virtual screening across multi-million compound repositories (ZINC20, Enamine REAL) [20].\n"
        "- 3D Equivariant Graph Neural Networks (EGNN): Incorporate geometric deep learning directly on 3D Cartesian coordinates to capture flexible induced-fit docking dynamics [21].\n"
        "- Predict Selectivity & ADMET Properties: Build multi-target kinome selectivity models (HER2, HER4, MET) and quantitative toxicity predictors (hERG, Ames, CYP450) [21], [24].\n"
        "- Wet-Lab Experimental Validation: Validate top computational candidates through molecular docking and in-vitro cell viability assays [20].\n"
        "- Interactive Web Platform: Deploy a scalable cloud web platform for real-time drug screening and explanation [22]."
    )
    doc.add_page_break()

    # =========================================================================
    # SECTION 14: REFERENCES (24 CITATIONS IN IEEE FORMAT)
    # =========================================================================
    add_heading_1(doc, "14. REFERENCES (24 PEER-REVIEWED ACADEMIC CITATIONS)")
    
    refs = [
        "[1] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 4765-4774, 2017.",
        "[2] S. M. Lundberg et al., 'From local explanations to global understanding with explainable AI for trees,' Nature Machine Intelligence, vol. 2, no. 1, pp. 56-67, 2020.",
        "[3] S. Bandyopadhyay and S. Saha, Unsupervised Classification: Similarity Measures and Applications. Springer-Verlag Berlin Heidelberg, 2013.",
        "[4] C. A. Lipinski, F. Lombardo, B. W. Dominy, and P. J. Feeney, 'Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings,' Advanced Drug Delivery Reviews, vol. 46, no. 1-3, pp. 3-26, 2001.",
        "[5] D. F. Veber et al., 'Molecular properties that influence the oral bioavailability of drug candidates,' Journal of Medicinal Chemistry, vol. 45, no. 12, pp. 2615-2623, 2002.",
        "[6] D. Rogers and M. Hahn, 'Extended-connectivity fingerprints,' Journal of Chemical Information and Modeling, vol. 50, no. 5, pp. 742-754, 2010.",
        "[7] G. Landrum et al., 'RDKit: Open-source cheminformatics,' GitHub repository, https://github.com/rdkit/rdkit, 2023.",
        "[8] A. Gaulton et al., 'ChEMBL: a large-scale bioactivity database for drug discovery,' Nucleic Acids Research, vol. 40, no. D1, pp. D1100-D1107, 2012.",
        "[9] L. Breiman, 'Random Forests,' Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.",
        "[10] J. H. Friedman, 'Greedy function approximation: A gradient boosting machine,' Annals of Statistics, vol. 29, no. 5, pp. 1189-1232, 2001.",
        "[11] R. Sordella, D. W. Bell, D. A. Haber, and J. Settleman, 'Gefitinib-sensitizing EGFR mutations in lung cancer activate selective apoptotic pathways,' Science, vol. 305, no. 5687, pp. 1163-1167, 2004.",
        "[12] D. A. Cross et al., 'AZD9291, an irreversible EGFR TKI, overcomes T790M-mediated resistance through selective inhibition of the mutant form of the epidermal growth factor receptor,' Cancer Discovery, vol. 4, no. 9, pp. 1046-1061, 2014.",
        "[13] G. R. Bickerton, G. V. Paolini, J. Besnard, S. Muresan, and A. L. Hopkins, 'Quantifying the chemical beauty of drugs,' Nature Chemistry, vol. 4, no. 2, pp. 90-98, 2012.",
        "[14] F. Pedregosa et al., 'Scikit-learn: Machine learning in Python,' Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.",
        "[15] S. A. Wildman and G. M. Crippen, 'Prediction of physicochemical parameters by atomic contributions,' Journal of Chemical Information and Computer Sciences, vol. 39, no. 5, pp. 868-873, 1999.",
        "[16] P. Ertl, B. Rohde, and P. Selzer, 'Fast calculation of molecular polar surface area as a sum of fragment-based contributions and its application to the prediction of drug transport properties,' Journal of Medicinal Chemistry, vol. 43, no. 20, pp. 3714-3717, 2000.",
        "[17] F. Lovering, J. Bikker, and C. Humblet, 'Escape from Flatland: increasing saturation as an approach to improving clinical success,' Journal of Medicinal Chemistry, vol. 52, no. 21, pp. 6752-6756, 2009.",
        "[18] S. Riniker and G. A. Landrum, 'Better informed distance geometry: using knowledge-based torsion angle potentials,' Journal of Chemical Information and Modeling, vol. 55, no. 12, pp. 2562-2574, 2015.",
        "[19] T. A. Halgren, 'Merck molecular force field. I. Basis, form, scope, parameterization, and performance of MMFF94,' Journal of Computational Chemistry, vol. 17, no. 5-6, pp. 490-519, 1996.",
        "[20] J. Bajorath, 'Integration of virtual and high-throughput screening,' Nature Reviews Drug Discovery, vol. 1, no. 11, pp. 882-894, 2002.",
        "[21] J. Vamathevan et al., 'Applications of machine learning in drug discovery and development,' Nature Reviews Drug Discovery, vol. 18, no. 6, pp. 463-477, 2019.",
        "[22] M. T. Ribeiro, S. Singh, and C. Guestrin, ''Why should I trust you?': Explaining the predictions of any classifier,' in Proc. 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 1135-1144, 2016.",
        "[23] L. S. Shapley, 'A value for n-person games,' Contributions to the Theory of Games, vol. 2, no. 28, pp. 307-317, 1953.",
        "[24] S. V. Sharma, D. W. Bell, J. Settleman, and D. A. Haber, 'Epidermal growth factor receptor mutations in lung cancer,' Nature Reviews Cancer, vol. 7, no. 3, pp. 169-181, 2007."
    ]
    
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.1
        r = p_ref.add_run(ref)
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        
    doc.save(OUTPUT_DOCX)
    print(f"[SUCCESS] Research Monograph DOCX generated successfully at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_docx_monograph()
