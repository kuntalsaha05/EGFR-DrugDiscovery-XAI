"""
Generates the Complete Academic Project Report PDF adhering to the
Dr. Babasaheb Ambedkar Marathwada University & Maharashtra Institute of Technology template.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(CURRENT_DIR, "ACADEMIC_PROJECT_REPORT.pdf")

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
        # Don't draw headers/footers on cover page (page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#475569"))
            
            # Running Header
            self.drawString(54, 800, "EXPLAINABLE AI-BASED DRUG DISCOVERY ASSISTANT — EGFR VIRTUAL SCREENING")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 794, 541, 794)
            
            # Running Footer
            self.line(54, 45, 541, 45)
            self.drawString(54, 34, "Maharashtra Institute of Technology, Chhatrapati Sambhajinagar")
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
    
    # Custom styles
    title_univ = ParagraphStyle(
        "UnivTitle",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#0f172a")
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
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=7
    )
    body_bold = ParagraphStyle(
        "BodyDarkBold",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0f172a")
    )
    h1_style = ParagraphStyle(
        "H1Heading",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "H2Heading",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    center_p = ParagraphStyle(
        "CenterP",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#1e293b")
    )
    
    story = []

    # =========================================================================
    # 1. TITLE PAGE (COVER)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>“Dr. BABASAHEB AMBEDKAR MARATHWADA UNIVERSITY,<br/>Chhatrapati Sambhajinagar”</b>", title_univ))
    story.append(Spacer(1, 24))
    story.append(Paragraph("A MINOR PROJECT REPORT ON", ParagraphStyle("Cap", fontName="Helvetica", fontSize=11, alignment=1, spaceAfter=8)))
    story.append(Paragraph("<b>EXPLAINABLE AI-BASED DRUG DISCOVERY ASSISTANT FOR EARLY MOLECULAR SCREENING</b>", title_sub))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<i>Submitted in partial fulfillment of the requirements for the award of the degree of</i><br/><b>BACHELOR OF TECHNOLOGY</b><br/>(Artificial Intelligence and Data Science / Electrical Engineering)", center_p))
    story.append(Spacer(1, 25))
    
    cand_info = [
        [Paragraph("<b>Submitted by:</b>", body_style), Paragraph("<b>Under the Guidance of:</b>", body_style)],
        [Paragraph("<b>Kuntal Saha</b> (Roll No: _____________) <br/>[Student Name 2] (Roll No: _____________) <br/>[Student Name 3] (Roll No: _____________)", body_style),
         Paragraph("<b>[Project Guide Name]</b><br/>Assistant Professor,<br/>Department of Artificial Intelligence & Data Science", body_style)]
    ]
    t_cand = Table(cand_info, colWidths=[240, 240])
    t_cand.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0)
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 40))
    
    story.append(Paragraph("<b>Department of Artificial Intelligence and Data Science<br/>Maharashtra Institute of Technology</b><br/>Chhatrapati Sambhajinagar (Aurangabad), Maharashtra – 431 005<br/><b>Academic Year: 2026–2027</b>", center_p))
    story.append(PageBreak())

    # =========================================================================
    # 2. DECLARATION
    # =========================================================================
    story.append(Paragraph("DECLARATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=12))
    story.append(Paragraph("I / We hereby declare that the minor project report entitled <b>“EXPLAINABLE AI-BASED DRUG DISCOVERY ASSISTANT FOR EARLY MOLECULAR SCREENING”</b> has been completed and written by us.", body_style))
    story.append(Paragraph("To the best of our knowledge and belief, the work embodied in this thesis has not formed earlier the basis for the award of any Degree, Diploma, Associate-ship, or other similar title of this or any other University or examining body.", body_style))
    story.append(Paragraph("We give an undertaking that the material included in the thesis from other sources is duly acknowledged and cited. We have incorporated all changes as suggested by the Pre-submission Presentation Committee.", body_style))
    story.append(Spacer(1, 40))
    
    dec_table = [
        [Paragraph("<b>Date:</b> DD / MM / YYYY<br/><b>Place:</b> Chhatrapati Sambhajinagar", body_style),
         Paragraph("<b>Kuntal Saha</b><br/>[Student Name 2]<br/>[Student Name 3]<br/><i>Department of AI & Data Science,<br/>Maharashtra Institute of Technology</i>", body_style)]
    ]
    t_dec = Table(dec_table, colWidths=[240, 240])
    t_dec.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_dec)
    story.append(PageBreak())

    # =========================================================================
    # 3. CERTIFICATE
    # =========================================================================
    story.append(Paragraph("CERTIFICATE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=12))
    story.append(Paragraph("This is to certify that the minor project report entitled <b>“EXPLAINABLE AI-BASED DRUG DISCOVERY ASSISTANT FOR EARLY MOLECULAR SCREENING”</b>, submitted by <b>Kuntal Saha, [Student Name 2], and [Student Name 3]</b> is the bona fide work completed under my supervision and guidance in partial fulfillment for the award of Bachelor of Technology of <b>Dr. Babasaheb Ambedkar Marathwada University, Chhatrapati Sambhajinagar (M.S.)</b>.", body_style))
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Place:</b> Chhatrapati Sambhajinagar<br/><b>Date:</b> _____ / _____ / 2026", body_style))
    story.append(Spacer(1, 50))
    
    sign_table = [
        [Paragraph("_________________________<br/><b>[Project Guide Name]</b><br/>Project Guide", center_p),
         Paragraph("_________________________<br/><b>Dr. Shilpa Kodgire</b><br/>Project Co-ordinator", center_p),
         Paragraph("_________________________<br/><b>Dr. S. M. Badave</b><br/>Head of Department", center_p)]
    ]
    t_sign = Table(sign_table, colWidths=[160, 160, 160])
    story.append(t_sign)
    story.append(Spacer(1, 40))
    story.append(Paragraph("___________________________________<br/><b>Dr. S. P. Bhosle</b><br/>Director<br/>Maharashtra Institute of Technology, Chhatrapati Sambhajinagar", center_p))
    story.append(PageBreak())

    # =========================================================================
    # 4. ACKNOWLEDGEMENTS
    # =========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=12))
    story.append(Paragraph("The portion of success is brewed by the efforts put in by many individuals. It is constant support provided by people who give you the initiative, who inspire you at each step of your endeavor that eventually helps you in your goal.", body_style))
    story.append(Paragraph("We wish to express our deep gratitude and hearty appreciation for the invaluable guidance of our professors throughout the span of doing this project. We are deeply indebted to our college Director <b>Dr. S. P. Bhosle</b> for providing institutional infrastructure and academic resources.", body_style))
    story.append(Paragraph("We are also thankful to our HOD <b>Dr. S. M. Badave</b>, Project Co-Ordinator <b>Dr. Shilpa Kodgire</b>, and our Project Guide <b>[Guide Name]</b> for their invaluable and elaborate suggestions. Their mentorship guided us to complete this task successfully.", body_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>Kuntal Saha</b><br/>Roll No: _____________<br/>Division: ____________", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 5. ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=12))
    story.append(Paragraph("Pharmaceutical drug discovery takes 10 to 15 years and billions of dollars, with late-stage preclinical failures primarily driven by poor efficacy or adverse pharmacokinetics. This project implements <b>EGFR Molecular Intelligence</b>, an end-to-end, interpretable computational assistant for virtual screening targeting <b>Human Epidermal Growth Factor Receptor (EGFR / ErbB-1, CHEMBL203)</b>, a crucial oncogene in Non-Small Cell Lung Cancer (NSCLC).", body_style))
    story.append(Paragraph("Using 881 curated chemical assays from the EMBL-EBI ChEMBL database, molecules are converted into composite feature representations combining 2,048-bit Morgan Circular Fingerprints (ECFP4) and 8 physicochemical descriptors via RDKit. Supervised ensemble classifiers (Random Forest and Gradient Boosted Decision Trees) were trained with stratified holdout validation. Random Forest achieved <b>90.96% accuracy</b> and an <b>ROC-AUC of 0.978</b>, while Gradient Boosting attained <b>91.53% accuracy</b> and <b>0.968 ROC-AUC</b>.", body_style))
    story.append(Paragraph("To eliminate the 'black-box' barrier in clinical adoption, the system integrates <b>SHAP (SHapley Additive exPlanations)</b> cooperative game theory, projecting favorable binding fragments (in chartreuse) and unfavorable steric clashes (in crimson) directly onto 2D molecular structures. The platform additionally computes Lipinski Rule of Five oral drug-likeness radar charts, Tanimoto similarity against clinical drugs (Gefitinib, Erlotinib, Osimertinib), integrates a local Ollama LLM tutor for viva preparation, and compiles publication-grade PDF dossiers using ReportLab.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>KEYWORDS:</b> Explainable AI (XAI), Computer-Aided Drug Discovery, EGFR (CHEMBL203), Virtual Screening, SHAP, RDKit, Random Forest, Gradient Boosting, Lipinski Rule of Five, Morgan Fingerprints.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 6. CHAPTER 1: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("1.1 Introduction", h2_style))
    story.append(Paragraph("Traditional pharmaceutical discovery relies heavily on High-Throughput Screening (HTS) of physical chemical libraries against biological targets. This empirical paradigm requires multi-year wet-lab validation and incurs immense reagent costs. Machine learning has transformed early discovery into digital <i>in silico</i> virtual screening. By learning structural patterns from historical assays, AI algorithms rapidly prioritize candidate molecules that are likely to bind tightly to disease proteins.", body_style))
    story.append(Paragraph("However, high predictive accuracy alone is insufficient. Computational chemistry demands <b>interpretability</b>: medicinal chemists must know <i>why</i> a compound is predicted active to guide lead optimization and avoid toxic off-target interactions. This project bridges this gap for Human EGFR, a critical lung cancer target.", body_style))
    
    story.append(Paragraph("1.2 Need of Project", h2_style))
    story.append(Paragraph("Non-Small Cell Lung Cancer (NSCLC) accounts for 85% of global lung cancer mortalities. Overexpression and activating mutations in the EGFR kinase domain (e.g., exon 19 deletions and L858R) drive uncontrolled cellular proliferation. Although targeted tyrosine kinase inhibitors (TKIs) exist, acquired drug resistance inevitably arises. Consequently, fast, interpretable computational filters are urgently needed to screen novel chemical scaffolds with zero physical reagent waste.", body_style))
    
    story.append(Paragraph("1.3 Objectives of Project", h2_style))
    story.append(Paragraph("• Develop an automated chemoinformatics pipeline parsing SMILES strings into 2D diagrams and 3D MMFF94 energy-minimized conformers.<br/>• Harvest and curate 881 bioactivity records from ChEMBL (CHEMBL203), establishing a strict 1,000 nM active cutoff.<br/>• Featurize compounds using 2048-bit Morgan Fingerprints (ECFP4) and 8 RDKit physicochemical descriptors.<br/>• Train supervised Random Forest and GBDT ensembles achieving ROC-AUC > 0.90.<br/>• Integrate game-theoretic TreeSHAP for atom-level visual explanation.<br/>• Evaluate oral bioavailability via Lipinski and Veber rules and benchmark clinical similarity via Tanimoto metrics.<br/>• Deliver an interactive dark-themed web platform with local Ollama LLM tutoring and automated PDF dossier export.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 7. CHAPTER 2: LITERATURE REVIEW
    # =========================================================================
    story.append(Paragraph("CHAPTER 2: LITERATURE REVIEW", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("2.1 Literature Description", h2_style))
    story.append(Paragraph("<b>Computer-Aided Drug Discovery (CADD):</b> Originating from Hansch QSAR analysis in the 1960s, computational drug discovery progressed from simple linear regressions to molecular docking (AutoDock, Glide) and modern statistical learning. While docking models physical 3D lock-and-key physics, it is computationally expensive and sensitive to static crystal grid artifacts.", body_style))
    story.append(Paragraph("<b>Target Biology & EGFR Inhibitors:</b> Sordella et al. (Science, 2004) proved that kinase domain somatic mutations sensitize lung cancers to 4-anilinoquinazoline derivatives like Gefitinib and Erlotinib. Cross et al. (Cancer Discovery, 2014) detailed the emergence of the T790M resistance mutation, prompting the development of mutant-selective covalent inhibitors such as Osimertinib (AZD9291).", body_style))
    story.append(Paragraph("<b>Soft Computing in Bioinformatics:</b> The application of soft computing and evolutionary multi-objective optimization to biological sequences was pioneered by <b>Prof. Sanghamitra Bandyopadhyay</b> (ISI Kolkata), demonstrating that non-linear ensemble algorithms effectively model noisy biological feature landscapes.", body_style))
    story.append(Paragraph("<b>Explainable AI (XAI):</b> Lundberg and Lee (NeurIPS 2017) formalized SHAP based on cooperative game theory. Lundberg et al. (Nature Machine Intelligence 2020) demonstrated TreeSHAP, enabling polynomial-time exact Shapley calculation for tree ensembles. However, published literature rarely connects abstract fingerprint bits back to visual 2D atom diagrams.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 8. CHAPTER 3: SYSTEM MODELLING & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("CHAPTER 3: SYSTEM MODELLING & ARCHITECTURE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("3.1 Chemoinformatics Featurization", h2_style))
    story.append(Paragraph("Chemical compounds are represented as mathematical graphs G = (V, E). We apply Extended Connectivity Circular Fingerprints (ECFP4) with radius r = 2, capturing circular atomic environments up to 4 bonds and folding into 2,048 bits. Concurrently, 8 physicochemical descriptors are calculated:", body_style))
    
    desc_data = [
        [Paragraph("<b>Descriptor</b>", body_style), Paragraph("<b>Target Property</b>", body_style), Paragraph("<b>Clinical Drug Discovery Relevance</b>", body_style)],
        [Paragraph("MolWt", body_style), Paragraph("Molecular Weight (Da)", body_style), Paragraph("Governs steric cavity fit and passive membrane diffusion", body_style)],
        [Paragraph("MolLogP", body_style), Paragraph("Octanol-water partition", body_style), Paragraph("Lipophilicity, gut absorption, and membrane permeability", body_style)],
        [Paragraph("TPSA", body_style), Paragraph("Polar Surface Area (Å²)", body_style), Paragraph("Cellular permeability and blood-brain barrier transport", body_style)],
        [Paragraph("NumHBD / HBA", body_style), Paragraph("H-Bond Donors & Acceptors", body_style), Paragraph("Key directional bonding capabilities with kinase residues", body_style)],
        [Paragraph("NumRotBonds", body_style), Paragraph("Rotatable Bond Count", body_style), Paragraph("Molecular flexibility; high flexibility incurs entropic penalty", body_style)],
        [Paragraph("QED", body_style), Paragraph("Drug-likeness desirability", body_style), Paragraph("Multi-parameter optimization score between 0.0 and 1.0", body_style)]
    ]
    t_desc = Table(desc_data, colWidths=[80, 150, 250])
    t_desc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_desc)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("3.2 Supervised Ensembles & TreeSHAP Formulation", h2_style))
    story.append(Paragraph("Combined feature vectors x in R^2056 are classified via Random Forest and Gradient Boosting. Local explainability decomposes predictions into additive contributions:", body_style))
    story.append(Paragraph("<b>f(x) = φ₀ + Σ φᵢ(x)</b>", center_p))
    story.append(Paragraph("where φ₀ is the baseline dataset probability and φᵢ is the Shapley value of feature i. By tracing bits to their physical atomic coordinates via RDKit bitInfo, atom-level scores are mapped into green (+SHAP favorable binding) and red (-SHAP steric penalty) visual highlights.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 9. CHAPTER 4: IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 4: IMPLEMENTATION DETAILS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("4.1 Software Pipeline Architecture", h2_style))
    story.append(Paragraph("The software stack is organized into clean modular components in Python 3.11:<br/>• <b>chem_engine.py:</b> SMILES sanitization, descriptor extraction, and ETKDGv3 MMFF94 3D conformer minimization.<br/>• <b>ai_model.py:</b> Ensemble model loading, feature scaling, and calibrated inference.<br/>• <b>explainability.py:</b> TreeSHAP computation and atom-level color gradient generation.<br/>• <b>similarity_engine.py:</b> Morgan Tanimoto similarity against clinical EGFR inhibitors.<br/>• <b>chatbot.py:</b> Local Ollama LLM integration (gemma3:1b) with offline fallback.<br/>• <b>report_generator.py:</b> Vector PDF generation engine powered by ReportLab.<br/>• <b>app.py:</b> Multi-section Streamlit research instrument styled under the Herbarium Alpinum design system.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 10. CHAPTER 5: EXPERIMENTAL RESULTS
    # =========================================================================
    story.append(Paragraph("CHAPTER 5: EXPERIMENTAL RESULTS & DISCUSSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("5.1 Model Benchmark Evaluation", h2_style))
    story.append(Paragraph("Classifiers were evaluated on a 20% stratified holdout test set (177 compounds) from the curated ChEMBL203 dataset:", body_style))
    
    res_data = [
        [Paragraph("<b>Model Classifier</b>", body_style), Paragraph("<b>Accuracy</b>", body_style), Paragraph("<b>Precision</b>", body_style), Paragraph("<b>Recall</b>", body_style), Paragraph("<b>F1-Score</b>", body_style), Paragraph("<b>ROC-AUC</b>", body_style)],
        [Paragraph("Random Forest (RF)", body_style), Paragraph("<b>90.96%</b>", body_style), Paragraph("90.62%", body_style), Paragraph("92.55%", body_style), Paragraph("0.9158", body_style), Paragraph("<b>0.9784</b>", body_style)],
        [Paragraph("Gradient Boosting (GBDT)", body_style), Paragraph("<b>91.53%</b>", body_style), Paragraph("91.67%", body_style), Paragraph("92.55%", body_style), Paragraph("0.9206", body_style), Paragraph("<b>0.9678</b>", body_style)]
    ]
    t_res = Table(res_data, colWidths=[120, 70, 70, 70, 70, 80])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_res)
    story.append(Spacer(1, 14))
    
    story.append(Paragraph("5.2 XAI Validation: Gefitinib vs. Aspirin Control", h2_style))
    story.append(Paragraph("<b>Gefitinib (Approved TKI):</b> Model predicted Active with <b>99.8% probability</b>. Top positive SHAP drivers identified the 4-anilinoquinazoline bicyclic core and the 3-chloro-4-fluoroaniline moiety, corresponding precisely to the known crystallographic hinge-binding anchors with Met793.<br/><b>Aspirin (Negative Control):</b> Model predicted Inactive with <b>7.7% probability</b>. SHAP identified low molecular weight (180 Da) and the negatively charged carboxylate group as severe penalties (-SHAP), causing electrostatic repulsion with the hydrophobic ATP pocket.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # 11. CHAPTER 6: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    story.append(Paragraph("6.1 Conclusion", h2_style))
    story.append(Paragraph("This project successfully demonstrated that machine learning ensembles combined with game-theoretic explainability provide a powerful, transparent virtual screening platform for Human EGFR oncology targets. The system achieves <b>90.96% accuracy and 0.978 ROC-AUC</b>, bridges the black-box gap via atom-level SHAP visualization, checks oral bioavailability, and equips researchers with automated PDF dossiers and an interactive LLM tutor.", body_style))
    
    story.append(Paragraph("6.2 Advantages", h2_style))
    story.append(Paragraph("• Ultra-fast screening (< 50 ms per compound) with zero reagent costs.<br/>• Full interpretability: chemists can visualize exactly which functional groups drive binding.<br/>• Simultaneous assessment of binding probability and oral absorption rules.<br/>• Completely private, offline-capable architecture using local models.", body_style))
    
    story.append(Paragraph("6.3 Future Scope", h2_style))
    story.append(Paragraph("• Extend featurization to 3D Equivariant Graph Neural Networks (EGNN).<br/>• Expand screening to multi-target kinase selectivity panels (HER2, HER4, VEGFR).<br/>• Couple with deep generative reinforcement learning for <i>de novo</i> drug design.<br/>• Incorporate quantitative hERG and CYP450 toxicity predictors.", body_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # 12. REFERENCES
    # =========================================================================
    story.append(Paragraph("REFERENCES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f172a"), spaceAfter=10))
    refs = [
        "[1] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 30, pp. 4765–4774, 2017.",
        "[2] S. M. Lundberg et al., 'From local explanations to global understanding with explainable AI for trees,' <i>Nature Machine Intelligence</i>, vol. 2, no. 1, pp. 56–67, 2020.",
        "[3] S. Bandyopadhyay and S. Saha, <i>Unsupervised Classification: Similarity Measures, Classical and Metaheuristic Approaches, and Applications</i>. Springer Science & Business Media, 2013.",
        "[4] C. A. Lipinski et al., 'Experimental and computational approaches to estimate solubility and permeability in drug discovery,' <i>Adv. Drug Deliv. Rev.</i>, vol. 46, pp. 3–26, 2001.",
        "[5] D. F. Veber et al., 'Molecular properties that influence the oral bioavailability of drug candidates,' <i>J. Med. Chem.</i>, vol. 45, no. 12, pp. 2615–2623, 2002.",
        "[6] D. Rogers and M. Hahn, 'Extended-connectivity fingerprints,' <i>J. Chem. Inf. Model.</i>, vol. 50, no. 5, pp. 742–754, 2010.",
        "[7] A. Gaulton et al., 'ChEMBL: a large-scale bioactivity database for drug discovery,' <i>Nucleic Acids Res.</i>, vol. 40, pp. D1100–D1107, 2012.",
        "[8] L. Breiman, 'Random Forests,' <i>Machine Learning</i>, vol. 45, no. 1, pp. 5–32, 2001.",
        "[9] R. Sordella et al., 'Gefitinib-sensitizing EGFR mutations in lung cancer activate selective apoptotic pathways,' <i>Science</i>, vol. 305, pp. 1163–1167, 2004.",
        "[10] D. A. Cross et al., 'AZD9291, an irreversible EGFR TKI, overcomes T790M-mediated resistance,' <i>Cancer Discovery</i>, vol. 4, no. 9, pp. 1046–1061, 2014."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle("RefStyle", fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#1e293b"), spaceAfter=5)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Academic Project Report PDF generated at: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_full_pdf()
