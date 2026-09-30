"""
Automated PDF Report Generator for EGFR Virtual Screening.
Uses ReportLab to generate publication-grade screening dossiers with
chemical structures, AI predictions, SHAP explainability insights,
Lipinski/Veber drug-likeness scorecards, and similarity benchmarks.
"""

import io
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.units import inch

from chem_engine import draw_molecule_2d_png, evaluate_drug_likeness


def generate_screening_pdf(
    smiles: str,
    prediction_result: Dict[str, Any],
    shap_result: Optional[Dict[str, Any]] = None,
    similarity_matches: Optional[List[Dict[str, Any]]] = None,
    output_path: Optional[str] = None
) -> bytes:
    """
    Builds a professional PDF report and returns PDF bytes.
    If output_path is provided, writes to disk as well.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    bold_body_style = ParagraphStyle(
        "ReportBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    badge_active = ParagraphStyle(
        "ActiveBadge",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#15803d")
    )

    badge_inactive = ParagraphStyle(
        "InactiveBadge",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#b91c1c")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("EGFR Virtual Screening Dossier", title_style))
    story.append(Paragraph(
        f"<b>Target:</b> Human Epidermal Growth Factor Receptor (CHEMBL203) &nbsp;|&nbsp; "
        f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} &nbsp;|&nbsp; "
        f"<b>Engine:</b> Explainable AI Drug Discovery Assistant",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=10))

    # 2. Molecular Structure & Prediction Summary Side-by-Side
    mol = prediction_result.get("mol")
    img_flowable = None
    if mol is not None:
        try:
            png_bytes = draw_molecule_2d_png(mol, size=(300, 220))
            if png_bytes:
                img_buf = io.BytesIO(png_bytes)
                img_flowable = RLImage(img_buf, width=2.8 * inch, height=2.0 * inch)
        except Exception:
            pass

    is_active = prediction_result.get("is_active", False)
    prob_active = prediction_result.get("prob_active", 0.0)
    conf = prediction_result.get("confidence", "N/A")
    model_name = prediction_result.get("model_type", "Random Forest")

    pred_style = badge_active if is_active else badge_inactive
    pred_text = f"ACTIVE (EGFR Inhibitor)" if is_active else "INACTIVE (Non-Inhibitor)"

    summary_data = [
        [Paragraph("<b>SMILES:</b>", body_style), Paragraph(f"<font size=7>{smiles}</font>", body_style)],
        [Paragraph("<b>AI Prediction:</b>", body_style), Paragraph(pred_text, pred_style)],
        [Paragraph("<b>Active Probability:</b>", body_style), Paragraph(f"<b>{prob_active * 100:.1f}%</b>", bold_body_style)],
        [Paragraph("<b>Confidence Tier:</b>", body_style), Paragraph(conf, body_style)],
        [Paragraph("<b>Screening Model:</b>", body_style), Paragraph(model_name, body_style)]
    ]

    summary_table = Table(summary_data, colWidths=[1.3 * inch, 3.2 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    if img_flowable:
        top_grid = Table([[img_flowable, summary_table]], colWidths=[3.0 * inch, 4.2 * inch])
        top_grid.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ]))
        story.append(top_grid)
    else:
        story.append(summary_table)

    story.append(Spacer(1, 10))

    # 3. Physicochemical Descriptors & Drug-Likeness
    story.append(Paragraph("Physicochemical Profiling & Oral Drug-Likeness", h2_style))
    if mol:
        dl = evaluate_drug_likeness(mol)
        desc = dl.get("descriptors", {})
        lip = dl.get("lipinski", {})
        veb = dl.get("veber", {})

        prop_data = [
            [
                Paragraph("<b>Property</b>", bold_body_style),
                Paragraph("<b>Value</b>", bold_body_style),
                Paragraph("<b>Lipinski Ro5 Limit</b>", bold_body_style),
                Paragraph("<b>Veber Limit</b>", bold_body_style),
                Paragraph("<b>Status</b>", bold_body_style)
            ],
            ["Molecular Weight", f"{desc.get('MolWt', 0):.1f} Da", "≤ 500 Da", "-", "Pass" if desc.get('MolWt', 0) <= 500 else "Alert"],
            ["LogP (Octanol/Water)", f"{desc.get('MolLogP', 0):.2f}", "≤ 5.0", "-", "Pass" if desc.get('MolLogP', 0) <= 5.0 else "Alert"],
            ["TPSA", f"{desc.get('TPSA', 0):.1f} Å²", "-", "≤ 140 Å²", "Pass" if desc.get('TPSA', 0) <= 140 else "Alert"],
            ["H-Bond Donors", f"{desc.get('NumHDonors', 0)}", "≤ 5", "-", "Pass" if desc.get('NumHDonors', 0) <= 5 else "Alert"],
            ["H-Bond Acceptors", f"{desc.get('NumHAcceptors', 0)}", "≤ 10", "-", "Pass" if desc.get('NumHAcceptors', 0) <= 10 else "Alert"],
            ["Rotatable Bonds", f"{desc.get('NumRotatableBonds', 0)}", "-", "≤ 10", "Pass" if desc.get('NumRotatableBonds', 0) <= 10 else "Alert"],
            ["QED Drug-Likeness", f"{desc.get('QED', 0):.2f}", "Optimal > 0.5", "-", "High" if desc.get('QED', 0) >= 0.5 else "Moderate"]
        ]

        prop_table = Table(prop_data, colWidths=[1.8 * inch, 1.2 * inch, 1.4 * inch, 1.4 * inch, 1.2 * inch])
        prop_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ]))
        story.append(prop_table)

        story.append(Spacer(1, 4))
        verdict_text = (
            f"<b>Summary:</b> Lipinski Rule of 5: <b>{lip.get('status', 'Pass')}</b> "
            f"({lip.get('violations_count', 0)} violations) | "
            f"Veber Rule: <b>{veb.get('status', 'Pass')}</b> "
            f"({veb.get('violations_count', 0)} violations) | "
            f"Bioavailability Probability: <b>{dl.get('bioavailability_score', 0.85)*100:.0f}%</b>"
        )
        story.append(Paragraph(verdict_text, body_style))

    story.append(Spacer(1, 10))

    # 4. Explainable AI (SHAP) Attribution
    if shap_result and "top_drivers" in shap_result:
        story.append(Paragraph("Explainable AI: Key Molecular Drivers (SHAP)", h2_style))
        drivers = shap_result.get("top_drivers", [])[:6]
        shap_data = [
            [
                Paragraph("<b>Feature</b>", bold_body_style),
                Paragraph("<b>Feature Category</b>", bold_body_style),
                Paragraph("<b>SHAP Impact</b>", bold_body_style),
                Paragraph("<b>Binding Influence</b>", bold_body_style)
            ]
        ]
        for d in drivers:
            val = d.get("shap_value", 0.0)
            color_hex = "#15803d" if val > 0 else "#b91c1c"
            effect_txt = "Favorable (Boosts Inhibition)" if val > 0 else "Unfavorable (Reduces Activity)"
            shap_data.append([
                d.get("feature", "N/A"),
                d.get("type", "Descriptor"),
                f"<font color='{color_hex}'><b>{val:+.4f}</b></font>",
                effect_txt
            ])

        shap_table = Table(shap_data, colWidths=[2.2 * inch, 1.8 * inch, 1.2 * inch, 2.0 * inch])
        shap_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ]))
        story.append(shap_table)

    story.append(Spacer(1, 10))

    # 5. Approved EGFR Inhibitors Similarity Ranking
    if similarity_matches:
        story.append(Paragraph("Tanimoto Similarity to FDA-Approved EGFR Inhibitors", h2_style))
        sim_data = [
            [
                Paragraph("<b>Therapeutic Agent</b>", bold_body_style),
                Paragraph("<b>Similarity</b>", bold_body_style),
                Paragraph("<b>Generation</b>", bold_body_style),
                Paragraph("<b>FDA Approval</b>", bold_body_style),
                Paragraph("<b>Clinical Indication</b>", bold_body_style)
            ]
        ]
        for m in similarity_matches[:4]:
            sim_data.append([
                m.get("name", "N/A"),
                f"<b>{m.get('similarity_pct', 0)}%</b>",
                m.get("generation", "N/A"),
                str(m.get("fda_approval_year", "N/A")),
                m.get("clinical_indication", "N/A")
            ])

        sim_table = Table(sim_data, colWidths=[1.8 * inch, 1.0 * inch, 1.6 * inch, 1.0 * inch, 1.8 * inch])
        sim_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (1, 0), (3, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ]))
        story.append(sim_table)

    # 6. Disclaimer Footer
    story.append(Spacer(1, 14))
    disclaimer = (
        "<i>Disclaimer: This dossier was generated by the Explainable AI Drug Discovery Assistant. "
        "Predictions and physicochemical evaluations are intended for research prioritisation and early virtual screening. "
        "Laboratory assay confirmation is essential before progression into in vitro or in vivo studies.</i>"
    )
    story.append(Paragraph(disclaimer, ParagraphStyle("Disc", parent=body_style, fontSize=7, textColor=colors.HexColor("#64748b"))))

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes
