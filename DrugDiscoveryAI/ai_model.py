"""
AI Inference Engine for EGFR Virtual Screening.
Loads trained Random Forest and Gradient Boosting models.
Preprocesses query SMILES, extracts features, scales descriptors,
and delivers Active/Inactive predictions with calibrated probabilities and confidence bands.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, Tuple
import joblib
import numpy as np

from rdkit import Chem
from chem_engine import validate_smiles, calculate_descriptors, compute_morgan_fingerprint, DESCRIPTOR_NAMES

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")


class EGFRModelPredictor:
    """
    Inference wrapper for EGFR bioactivity models.
    """
    def __init__(self, models_dir: str = MODELS_DIR):
        self.models_dir = models_dir
        self.rf_model = None
        self.gb_model = None
        self.scaler = None
        self.meta = {}
        self.is_loaded = False
        self._load_models()

    def _load_models(self) -> bool:
        """Loads serialized models, scaler, and metadata."""
        rf_path = os.path.join(self.models_dir, "rf_model.pkl")
        gb_path = os.path.join(self.models_dir, "gb_model.pkl")
        scaler_path = os.path.join(self.models_dir, "scaler.pkl")
        meta_path = os.path.join(self.models_dir, "model_meta.json")

        if os.path.exists(rf_path) and os.path.exists(gb_path) and os.path.exists(scaler_path):
            try:
                self.rf_model = joblib.load(rf_path)
                self.gb_model = joblib.load(gb_path)
                self.scaler = joblib.load(scaler_path)
                if os.path.exists(meta_path):
                    with open(meta_path, "r") as f:
                        self.meta = json.load(f)
                self.is_loaded = True
                logger.info("EGFR models and scalers successfully loaded.")
                return True
            except Exception as e:
                logger.error(f"Failed to load model artifacts: {e}")
                self.is_loaded = False
                return False
        return False

    def featurize_molecule(self, mol: Chem.Mol) -> Tuple[np.ndarray, np.ndarray, Dict[str, float], Dict[int, tuple]]:
        """
        Featurizes a valid RDKit molecule:
        Returns: (full_feature_vector, unscaled_desc_vec, desc_dict, bit_info)
        """
        desc_dict = calculate_descriptors(mol)
        desc_raw = np.array([[desc_dict.get(name, 0.0) for name in DESCRIPTOR_NAMES]], dtype=np.float32)
        
        # Scale descriptors using the trained scaler
        if self.scaler is not None:
            desc_scaled = self.scaler.transform(desc_raw)
        else:
            desc_scaled = desc_raw

        # Morgan fingerprint (ECFP4, 2048 bits) with bitInfo for explainability
        fp_vec, bit_info = compute_morgan_fingerprint(mol, radius=2, n_bits=2048, return_bitinfo=True)
        fp_vec_2d = np.array([fp_vec], dtype=np.float32)

        # Concatenate: [Scaled Descriptors (10), Morgan Bits (2048)]
        features = np.hstack([desc_scaled, fp_vec_2d])
        return features, desc_raw[0], desc_dict, bit_info

    def predict(
        self,
        smiles: str,
        model_type: str = "Random Forest",
        threshold: float = 0.50
    ) -> Dict[str, Any]:
        """
        Runs inference on input SMILES.
        Returns prediction details, probabilities, and featurized vectors.
        """
        if not self.is_loaded:
            loaded = self._load_models()
            if not loaded:
                return {
                    "success": False,
                    "error": "Models not yet trained or loaded. Please run model training first."
                }

        valid, mol, can_smiles = validate_smiles(smiles)
        if not valid or mol is None:
            return {
                "success": False,
                "error": f"Invalid SMILES structure: {can_smiles}"
            }

        features, raw_desc, desc_dict, bit_info = self.featurize_molecule(mol)

        # Select model
        selected_model = self.rf_model if model_type == "Random Forest" else self.gb_model
        
        probs = selected_model.predict_proba(features)[0]
        prob_active = float(probs[1])
        prob_inactive = float(probs[0])
        
        is_active = prob_active >= threshold
        predicted_label = "Active" if is_active else "Inactive"

        # Confidence category
        if prob_active >= 0.85:
            confidence = "High Confidence Active"
            confidence_level = "High"
        elif prob_active >= 0.65:
            confidence = "Moderate Confidence Active"
            confidence_level = "Moderate"
        elif prob_active >= 0.45:
            confidence = "Borderline / Intermediate"
            confidence_level = "Low"
        elif prob_active >= 0.20:
            confidence = "Moderate Confidence Inactive"
            confidence_level = "Moderate"
        else:
            confidence = "High Confidence Inactive"
            confidence_level = "High"

        return {
            "success": True,
            "smiles": can_smiles,
            "mol": mol,
            "model_type": model_type,
            "prediction": predicted_label,
            "is_active": is_active,
            "prob_active": round(prob_active, 4),
            "prob_inactive": round(prob_inactive, 4),
            "confidence": confidence,
            "confidence_level": confidence_level,
            "threshold": threshold,
            "features": features,
            "raw_descriptors": desc_dict,
            "bit_info": bit_info
        }


# Singleton instance
_predictor_instance = None

def get_predictor() -> EGFRModelPredictor:
    """Returns singleton instance of EGFRModelPredictor."""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = EGFRModelPredictor()
    return _predictor_instance
