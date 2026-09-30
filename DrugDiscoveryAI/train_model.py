"""
Model Training & Evaluation Pipeline for EGFR Virtual Screening.
Extracts 2048-bit Morgan Fingerprints + Standardized RDKit Descriptors.
Trains Random Forest and Gradient Boosting classifiers.
Evaluates Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix.
Serializes trained models, scalers, and evaluation metrics into models/.
"""

import os
import json
import logging
from typing import Tuple, Dict, Any, List
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix
)

from rdkit import Chem
from chem_engine import calculate_descriptors, compute_morgan_fingerprint, DESCRIPTOR_NAMES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "egfr_chembl203_bioactivity.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")


def extract_features_from_smiles(
    smiles_list: List[str],
    radius: int = 2,
    n_bits: int = 2048
) -> Tuple[np.ndarray, np.ndarray, List[int]]:
    """
    Extracts concatenated feature matrix: [Descriptors (10), Morgan Fingerprints (2048)].
    Returns: (descriptors_matrix, fingerprints_matrix, valid_indices)
    """
    desc_rows = []
    fp_rows = []
    valid_indices = []

    for idx, smi in enumerate(smiles_list):
        if not smi or not isinstance(smi, str):
            continue
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        
        # Descriptors
        desc_dict = calculate_descriptors(mol)
        desc_vec = [desc_dict.get(name, 0.0) for name in DESCRIPTOR_NAMES]
        
        # Morgan Fingerprints
        fp_vec, _ = compute_morgan_fingerprint(mol, radius=radius, n_bits=n_bits)
        
        desc_rows.append(desc_vec)
        fp_rows.append(fp_vec)
        valid_indices.append(idx)

    return np.array(desc_rows, dtype=np.float32), np.array(fp_rows, dtype=np.float32), valid_indices


def train_and_evaluate(data_path: str = DATA_PATH) -> Dict[str, Any]:
    """
    Full pipeline to load data, featurize, split, scale, train RF & GBDT, and save models.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run fetch_data.py first.")

    os.makedirs(MODELS_DIR, exist_ok=True)
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} compounds from {data_path}")

    # Ensure required columns
    if "canonical_smiles" not in df.columns or "class" not in df.columns:
        raise ValueError("Dataset missing 'canonical_smiles' or 'class' columns.")

    # Featurization
    logger.info("Extracting molecular descriptors and 2048-bit Morgan fingerprints...")
    desc_matrix, fp_matrix, valid_idx = extract_features_from_smiles(df["canonical_smiles"].tolist())
    
    y = df["class"].iloc[valid_idx].values.astype(int)
    logger.info(f"Successfully featurized {len(y)} molecules. Active: {(y == 1).sum()}, Inactive: {(y == 0).sum()}")

    # Stratified Train/Test split: 80% train, 20% test
    # Following strict ML best practices: split FIRST before fitting any scaler
    indices = np.arange(len(y))
    train_idx, test_idx = train_test_split(indices, test_size=0.20, random_state=42, stratify=y)

    train_desc, test_desc = desc_matrix[train_idx], desc_matrix[test_idx]
    train_fp, test_fp = fp_matrix[train_idx], fp_matrix[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Fit scaler strictly on training descriptors
    scaler = StandardScaler()
    train_desc_scaled = scaler.fit_transform(train_desc)
    test_desc_scaled = scaler.transform(test_desc)

    # Concatenate scaled descriptors and binary Morgan fingerprints
    X_train = np.hstack([train_desc_scaled, train_fp])
    X_test = np.hstack([test_desc_scaled, test_fp])

    feature_names = DESCRIPTOR_NAMES + [f"Morgan_Bit_{i}" for i in range(train_fp.shape[1])]

    # 1. Random Forest Classifier
    logger.info("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=250,
        max_depth=18,
        min_samples_split=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    # 2. Gradient Boosting Classifier
    logger.info("Training Gradient Boosting Classifier...")
    gb_model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.08,
        max_depth=5,
        random_state=42
    )
    gb_model.fit(X_train, y_train)

    # Evaluate models on test set
    models = {
        "Random Forest": rf_model,
        "Gradient Boosting": gb_model
    }

    metrics_results = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        roc_auc = float(roc_auc_score(y_test, y_prob))
        cm = confusion_matrix(y_test, y_pred).tolist()

        fpr, tpr, _ = roc_curve(y_test, y_prob)

        metrics_results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": cm,
            "roc_curve": {
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist()
            }
        }
        logger.info(f"{name} Results -> Accuracy: {acc:.4f}, F1: {f1:.4f}, ROC-AUC: {roc_auc:.4f}")

    # Serialize artifacts
    joblib.dump(rf_model, os.path.join(MODELS_DIR, "rf_model.pkl"))
    joblib.dump(gb_model, os.path.join(MODELS_DIR, "gb_model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
    joblib.dump(X_train[:100], os.path.join(MODELS_DIR, "background_samples.pkl"))  # for SHAP explainer baseline

    meta = {
        "target": "Human EGFR (CHEMBL203)",
        "num_samples_total": len(y),
        "num_train": len(y_train),
        "num_test": len(y_test),
        "num_features": len(feature_names),
        "descriptor_names": DESCRIPTOR_NAMES,
        "metrics": metrics_results,
        "class_distribution": {
            "Active": int((y == 1).sum()),
            "Inactive": int((y == 0).sum())
        }
    }

    with open(os.path.join(MODELS_DIR, "model_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    logger.info(f"Model training complete. Artifacts saved to {MODELS_DIR}")
    return meta


if __name__ == "__main__":
    train_and_evaluate()
