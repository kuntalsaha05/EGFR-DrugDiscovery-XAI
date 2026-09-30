"""
End-to-End Pipeline Verification Test for EGFR Drug Discovery Assistant.
Tests:
1. Molecule loading and validation (Gefitinib, Erlotinib, Osimertinib, Aspirin)
2. Descriptor calculation & Lipinski/Veber drug-likeness rules
3. AI model prediction (RF & Gradient Boosting)
4. SHAP TreeExplainer calculation and atom-level attribution mapping
5. Tanimoto similarity search against approved cancer therapeutics
6. ReportLab PDF report generation
"""

import os
import sys

# Ensure DrugDiscoveryAI is on path
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DrugDiscoveryAI")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from chem_engine import validate_smiles, calculate_descriptors, evaluate_drug_likeness, draw_molecule_2d_png
from ai_model import get_predictor
from explainability import SHAPExplainerEngine
from similarity_engine import get_similarity_engine
from report_generator import generate_screening_pdf


def run_tests():
    print("=" * 60)
    print("RUNNING END-TO-END PIPELINE VERIFICATION")
    print("=" * 60)

    # Test molecules
    test_cases = [
        {"name": "Gefitinib (Known Active EGFR TKI)", "smiles": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1", "expected_active": True},
        {"name": "Erlotinib (Known Active EGFR TKI)", "smiles": "COCCOc1cc2c(Nc3cccc(c3)C#C)ncnc2cc1OCCOC", "expected_active": True},
        {"name": "Osimertinib (Known Active 3rd-Gen TKI)", "smiles": "CN(C)CC=CC(=O)Nc1cc(Nc2ncc(c(n2)C(F)(F)F)Nc3ccccc3N(C)C)c(OC)cc1NC(=O)C=C", "expected_active": True},
        {"name": "Aspirin (Known Inactive Control)", "smiles": "CC(=O)Oc1ccccc1C(=O)O", "expected_active": False}
    ]

    predictor = get_predictor()
    assert predictor.is_loaded, "Predictor failed to load models!"
    print("[PASS] Models and scalers loaded successfully.")

    similarity_engine = get_similarity_engine()

    for tc in test_cases:
        name = tc["name"]
        smiles = tc["smiles"]
        print(f"\n--- Testing: {name} ---")

        # 1. Validation & Descriptors
        valid, mol, can_smiles = validate_smiles(smiles)
        assert valid, f"SMILES validation failed for {name}"
        desc = calculate_descriptors(mol)
        print(f"Descriptors: MW={desc['MolWt']}, LogP={desc['MolLogP']}, TPSA={desc['TPSA']}, QED={desc['QED']}")

        # 2. Drug-likeness
        dl = evaluate_drug_likeness(mol)
        print(f"Lipinski: {dl['lipinski']['status']} (Violations: {dl['lipinski']['violations_count']}), Veber: {dl['veber']['status']}")

        # 3. AI Prediction (Random Forest)
        rf_pred = predictor.predict(can_smiles, model_type="Random Forest")
        print(f"RF Prediction: {rf_pred['prediction']} (P(Active) = {rf_pred['prob_active']*100:.1f}%, Confidence: {rf_pred['confidence']})")

        # 4. AI Prediction (Gradient Boosting)
        gb_pred = predictor.predict(can_smiles, model_type="Gradient Boosting")
        print(f"GB Prediction: {gb_pred['prediction']} (P(Active) = {gb_pred['prob_active']*100:.1f}%)")

        if tc["expected_active"]:
            assert rf_pred["prob_active"] >= 0.50, f"Expected active for {name}, got {rf_pred['prob_active']}"
        else:
            assert rf_pred["prob_active"] < 0.50, f"Expected inactive for {name}, got {rf_pred['prob_active']}"

        # 5. Similarity search
        sim_matches = similarity_engine.search_similar_drugs(mol, top_k=3)
        print(f"Top Similarity Match: {sim_matches[0]['name']} ({sim_matches[0]['similarity_pct']}%)")

    # 6. SHAP Explainer Test on Gefitinib
    print("\n--- Testing SHAP Explainer & Atom Highlights on Gefitinib ---")
    gefitinib_smiles = test_cases[0]["smiles"]
    _, gef_mol, _ = validate_smiles(gefitinib_smiles)
    gef_pred = predictor.predict(gefitinib_smiles, model_type="Random Forest")
    explainer = SHAPExplainerEngine(predictor.rf_model)
    shap_res = explainer.explain_instance(
        gef_pred["features"],
        gef_mol,
        bit_info=gef_pred["bit_info"],
        top_k=5
    )
    print(f"Base Value: {shap_res['base_value']}")
    print(f"Top Favorable Drivers: {[d['feature'] for d in shap_res['positive_drivers'][:3]]}")
    assert len(shap_res["highlighted_svg"]) > 100, "Highlighted SVG generation failed"
    print("[PASS] SHAP atom-level highlights generated successfully.")

    # 7. PDF Report Generation Test
    print("\n--- Testing ReportLab PDF Generation ---")
    pdf_out = os.path.join(os.path.dirname(__file__), "test_screening_report.pdf")
    pdf_bytes = generate_screening_pdf(
        smiles=gefitinib_smiles,
        prediction_result=gef_pred,
        shap_result=shap_res,
        similarity_matches=similarity_engine.search_similar_drugs(gef_mol),
        output_path=pdf_out
    )
    assert len(pdf_bytes) > 1000, "PDF generation failed or returned empty bytes"
    assert os.path.exists(pdf_out), "PDF file not saved"
    print(f"[PASS] PDF report compiled successfully ({len(pdf_bytes)} bytes) at {pdf_out}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
