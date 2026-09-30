"""
Explainable AI (XAI) Engine for EGFR Virtual Screening.
Implements SHAP (SHapley Additive exPlanations) TreeExplainer for Random Forest and Gradient Boosting.
Provides:
  1. Global descriptor importance analysis.
  2. Local prediction breakdown (waterfall & feature bar plots).
  3. Atom-level and fragment-level substructure attribution mapping.
  4. Favorable (green) vs unfavorable (red) atom highlights on 2D chemical structures.
"""

import os
import logging
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import shap

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
from chem_engine import DESCRIPTOR_NAMES, draw_molecule_2d_svg

logger = logging.getLogger(__name__)


class SHAPExplainerEngine:
    """
    Manages SHAP explanations for EGFR virtual screening models.
    """
    def __init__(self, model, background_data: Optional[np.ndarray] = None):
        self.model = model
        self.background_data = background_data
        self.feature_names = DESCRIPTOR_NAMES + [f"Morgan_Bit_{i}" for i in range(2048)]
        
        try:
            # TreeExplainer is optimal for RF and Gradient Boosting
            if background_data is not None and len(background_data) > 0:
                self.explainer = shap.TreeExplainer(self.model, data=background_data)
            else:
                self.explainer = shap.TreeExplainer(self.model)
            logger.info("SHAP TreeExplainer initialized successfully.")
        except Exception as e:
            logger.warning(f"Fallback TreeExplainer initialization: {e}")
            self.explainer = shap.TreeExplainer(self.model)

    def explain_instance(
        self,
        features: np.ndarray,
        mol: Chem.Mol,
        bit_info: Optional[Dict[int, tuple]] = None,
        top_k: int = 8
    ) -> Dict[str, Any]:
        """
        Calculates local SHAP explanation for a single molecule instance.
        Maps fingerprint bits back to molecular atoms for structural highlights.
        """
        if features.ndim == 1:
            features_2d = np.array([features])
        else:
            features_2d = features

        shap_values = self.explainer.shap_values(features_2d)

        # Handle different SHAP output formats (binary classification)
        if isinstance(shap_values, list):
            # Binary classifier: shap_values[1] corresponds to class 1 (Active)
            sv = shap_values[1][0]
            base_val = float(self.explainer.expected_value[1]) if isinstance(self.explainer.expected_value, (list, np.ndarray)) else float(self.explainer.expected_value)
        elif hasattr(shap_values, "values"):
            # Explanation object
            if shap_values.values.ndim == 3:
                sv = shap_values.values[0, :, 1]
            else:
                sv = shap_values.values[0]
            base_val = float(shap_values.base_values[0]) if hasattr(shap_values, "base_values") else 0.5
        elif isinstance(shap_values, np.ndarray):
            if shap_values.ndim == 3:
                sv = shap_values[0, :, 1]
            else:
                sv = shap_values[0]
            base_val = float(self.explainer.expected_value[1]) if isinstance(self.explainer.expected_value, (list, np.ndarray)) else float(self.explainer.expected_value)
        else:
            sv = np.zeros(features_2d.shape[1])
            base_val = 0.5

        # 1. Separate Physicochemical Descriptors
        num_desc = len(DESCRIPTOR_NAMES)
        desc_shap = []
        for i, name in enumerate(DESCRIPTOR_NAMES):
            val = float(features_2d[0, i])
            s_val = float(sv[i])
            desc_shap.append({
                "feature": name,
                "type": "Descriptor",
                "shap_value": round(s_val, 4),
                "feature_value": round(val, 3),
                "effect": "Favorable (Increases Activity)" if s_val > 0 else "Unfavorable (Decreases Activity)"
            })
        
        desc_shap.sort(key=lambda x: abs(x["shap_value"]), reverse=True)

        # 2. Extract Top Morgan Fingerprint Bits
        fp_shap = []
        on_bits = []
        for i in range(num_desc, len(sv)):
            bit_idx = i - num_desc
            bit_val = int(features_2d[0, i])
            s_val = float(sv[i])
            if bit_val == 1:
                on_bits.append(bit_idx)
                fp_shap.append({
                    "feature": f"ECFP4_Bit_{bit_idx}",
                    "type": "Fingerprint Fragment",
                    "bit_id": bit_idx,
                    "shap_value": round(s_val, 4),
                    "effect": "Favorable (Binding Anchor)" if s_val > 0 else "Unfavorable (Clash/Penalty)"
                })

        fp_shap.sort(key=lambda x: abs(x["shap_value"]), reverse=True)

        # 3. Overall Top Drivers
        all_features = desc_shap + fp_shap
        all_features.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        top_drivers = all_features[:top_k]

        # 4. Atom-level Attribution via Morgan bitInfo
        atom_scores, atom_colors, highlighted_svg = self._map_shap_to_atoms(
            mol, sv[num_desc:], bit_info
        )

        return {
            "base_value": round(base_val, 4),
            "top_drivers": top_drivers,
            "descriptor_contributions": desc_shap,
            "top_fingerprint_bits": fp_shap[:top_k],
            "atom_scores": atom_scores,
            "highlighted_svg": highlighted_svg,
            "positive_drivers": [f for f in all_features if f["shap_value"] > 0][:5],
            "negative_drivers": [f for f in all_features if f["shap_value"] < 0][:5]
        }

    def _map_shap_to_atoms(
        self,
        mol: Chem.Mol,
        fp_shap_values: np.ndarray,
        bit_info: Optional[Dict[int, tuple]]
    ) -> Tuple[Dict[int, float], Dict[int, Tuple[float, float, float]], str]:
        """
        Maps fingerprint SHAP values back to individual atoms and generates a highlighted SVG.
        Favorable binding regions: Green
        Unfavorable / steric penalty regions: Red
        """
        if mol is None:
            return {}, {}, ""

        num_atoms = mol.GetNumAtoms()
        atom_scores = np.zeros(num_atoms, dtype=np.float32)

        if bit_info:
            for bit_id, occurrences in bit_info.items():
                if bit_id < len(fp_shap_values):
                    s_val = fp_shap_values[bit_id]
                    if abs(s_val) > 0.0001:
                        for atom_idx, radius in occurrences:
                            if 0 <= atom_idx < num_atoms:
                                # Central atom receives primary weight
                                atom_scores[atom_idx] += s_val
                                
                                # Atoms within radius receive proportional weight
                                if radius > 0:
                                    env = Chem.FindAtomEnvironmentOfRadiusN(mol, radius, atom_idx)
                                    for bond_idx in env:
                                        bond = mol.GetBondWithIdx(bond_idx)
                                        atom_scores[bond.GetBeginAtomIdx()] += s_val * 0.4
                                        atom_scores[bond.GetEndAtomIdx()] += s_val * 0.4

        # Normalize atom scores for color rendering
        max_abs = np.max(np.abs(atom_scores)) if len(atom_scores) > 0 else 0
        highlight_colors: Dict[int, Tuple[float, float, float]] = {}
        highlight_atoms: List[int] = []

        if max_abs > 1e-5:
            norm_scores = atom_scores / max_abs
            for idx, score in enumerate(norm_scores):
                f_score = float(score)
                i_idx = int(idx)
                if abs(f_score) >= 0.15:
                    highlight_atoms.append(i_idx)
                    if f_score > 0:
                        # Emerald Green gradient (favorable for EGFR inhibition)
                        intensity = float(min(1.0, 0.4 + 0.6 * f_score))
                        highlight_colors[i_idx] = (0.1, intensity, 0.3)
                    else:
                        # Crimson Red gradient (unfavorable for EGFR inhibition)
                        intensity = float(min(1.0, 0.4 + 0.6 * abs(f_score)))
                        highlight_colors[i_idx] = (intensity, 0.15, 0.15)

        # Render 2D SVG with highlights
        try:
            mol_copy = Chem.Mol(mol)
            from rdkit.Chem import AllChem
            AllChem.Compute2DCoords(mol_copy)
            drawer = rdMolDraw2D.MolDraw2DSVG(480, 340)
            opts = drawer.drawOptions()
            opts.addStereoAnnotation = True
            opts.highlightRadius = 0.35
            
            if highlight_atoms:
                drawer.DrawMolecule(
                    mol_copy,
                    highlightAtoms=highlight_atoms,
                    highlightAtomColors=highlight_colors
                )
            else:
                drawer.DrawMolecule(mol_copy)
            drawer.FinishDrawing()
            svg_text = drawer.GetDrawingText()
        except Exception as e:
            logger.warning(f"Error rendering highlighted SVG: {e}")
            svg_text = draw_molecule_2d_svg(mol)

        atom_dict = {i: round(float(atom_scores[i]), 4) for i in range(num_atoms)}
        return atom_dict, highlight_colors, svg_text
