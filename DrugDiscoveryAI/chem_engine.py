"""
Chemoinformatics Engine for EGFR Virtual Screening.
Handles molecule validation, descriptor calculation, ECFP4 fingerprint generation,
2D structure visualization, 3D conformer generation, and Lipinski/Veber drug-likeness rules.
"""

from typing import Dict, Any, Tuple, Optional, List
import io
import base64
import numpy as np

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, Descriptors, Lipinski, QED, Draw
from rdkit.Chem.Draw import rdMolDraw2D

# Suppress verbose RDKit warnings
RDLogger.DisableLog("rdApp.*")


DESCRIPTOR_NAMES = [
    "MolWt",
    "MolLogP",
    "TPSA",
    "NumHDonors",
    "NumHAcceptors",
    "NumRotatableBonds",
    "HeavyAtomCount",
    "NumAromaticRings",
    "FractionCSP3",
    "QED"
]


def validate_smiles(smiles: str) -> Tuple[bool, Optional[Chem.Mol], str]:
    """
    Validates and parses a SMILES string.
    Returns: (is_valid, mol_object, error_or_canonical_smiles)
    """
    if not smiles or not isinstance(smiles, str) or not smiles.strip():
        return False, None, "Empty SMILES string provided."
    
    clean_smiles = smiles.strip()
    try:
        mol = Chem.MolFromSmiles(clean_smiles)
        if mol is None:
            return False, None, "Invalid SMILES syntax: RDKit could not parse molecule."
        canonical_smiles = Chem.MolToSmiles(mol, isomericSmiles=True)
        return True, mol, canonical_smiles
    except Exception as e:
        return False, None, f"Parsing error: {str(e)}"


def canonicalize_smiles(smiles: str) -> Optional[str]:
    """Returns canonical isomeric SMILES or None if invalid."""
    valid, mol, can_smiles = validate_smiles(smiles)
    return can_smiles if valid else None


def calculate_descriptors(mol: Chem.Mol) -> Dict[str, float]:
    """
    Calculates key physicochemical descriptors for a valid RDKit molecule.
    """
    if mol is None:
        return {}
    
    try:
        qed_val = float(QED.qed(mol))
    except Exception:
        qed_val = 0.5

    return {
        "MolWt": round(float(Descriptors.MolWt(mol)), 3),
        "MolLogP": round(float(Descriptors.MolLogP(mol)), 3),
        "TPSA": round(float(Descriptors.TPSA(mol)), 3),
        "NumHDonors": int(Lipinski.NumHDonors(mol)),
        "NumHAcceptors": int(Lipinski.NumHAcceptors(mol)),
        "NumRotatableBonds": int(Lipinski.NumRotatableBonds(mol)),
        "HeavyAtomCount": int(mol.GetNumHeavyAtoms()),
        "NumAromaticRings": int(Lipinski.NumAromaticRings(mol)),
        "FractionCSP3": round(float(Descriptors.FractionCSP3(mol)), 3),
        "QED": round(qed_val, 3)
    }


def compute_morgan_fingerprint(
    mol: Chem.Mol,
    radius: int = 2,
    n_bits: int = 2048,
    return_bitinfo: bool = False
) -> Tuple[np.ndarray, Optional[Dict[int, tuple]]]:
    """
    Generates ECFP4 (Morgan fingerprint, radius 2) binary bit vector.
    Optionally returns bitInfo mapping bits to atom environments.
    """
    if mol is None:
        empty_fp = np.zeros(n_bits, dtype=np.int8)
        return (empty_fp, {}) if return_bitinfo else (empty_fp, None)
    
    bit_info: Dict[int, tuple] = {}
    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius=radius,
        nBits=n_bits,
        bitInfo=bit_info if return_bitinfo else None
    )
    
    arr = np.zeros(n_bits, dtype=np.int8)
    # Convert RDKit ExplicitBitVect to numpy array
    for bit in fp.GetOnBits():
        arr[bit] = 1
        
    return (arr, bit_info) if return_bitinfo else (arr, None)


def evaluate_drug_likeness(mol: Chem.Mol) -> Dict[str, Any]:
    """
    Evaluates Lipinski's Rule of Five and Veber's Rule for oral bioavailability.
    """
    desc = calculate_descriptors(mol)
    if not desc:
        return {"error": "Invalid molecule"}

    # Lipinski's Rule of Five checks
    mw_pass = desc["MolWt"] <= 500
    logp_pass = desc["MolLogP"] <= 5.0
    hbd_pass = desc["NumHDonors"] <= 5
    hba_pass = desc["NumHAcceptors"] <= 10

    lipinski_violations = sum([not mw_pass, not logp_pass, not hbd_pass, not hba_pass])
    lipinski_status = "Pass" if lipinski_violations <= 1 else "Fail"

    # Veber's Rule checks
    rb_pass = desc["NumRotatableBonds"] <= 10
    tpsa_pass = desc["TPSA"] <= 140.0
    veber_violations = sum([not rb_pass, not tpsa_pass])
    veber_status = "Pass" if veber_violations == 0 else "Fail"

    return {
        "descriptors": desc,
        "lipinski": {
            "status": lipinski_status,
            "violations_count": lipinski_violations,
            "rules": {
                "MolWt <= 500 Da": {"value": desc["MolWt"], "pass": mw_pass, "threshold": "≤ 500"},
                "LogP <= 5.0": {"value": desc["MolLogP"], "pass": logp_pass, "threshold": "≤ 5.0"},
                "H-Bond Donors <= 5": {"value": desc["NumHDonors"], "pass": hbd_pass, "threshold": "≤ 5"},
                "H-Bond Acceptors <= 10": {"value": desc["NumHAcceptors"], "pass": hba_pass, "threshold": "≤ 10"}
            }
        },
        "veber": {
            "status": veber_status,
            "violations_count": veber_violations,
            "rules": {
                "Rotatable Bonds <= 10": {"value": desc["NumRotatableBonds"], "pass": rb_pass, "threshold": "≤ 10"},
                "TPSA <= 140 Å²": {"value": desc["TPSA"], "pass": tpsa_pass, "threshold": "≤ 140"}
            }
        },
        "bioavailability_score": 0.85 if (lipinski_violations == 0 and veber_violations == 0) else (0.56 if lipinski_violations <= 1 else 0.17)
    }


def draw_molecule_2d_svg(
    mol: Chem.Mol,
    highlight_atoms: Optional[List[int]] = None,
    highlight_atom_colors: Optional[Dict[int, Tuple[float, float, float]]] = None,
    size: Tuple[int, int] = (450, 320)
) -> str:
    """
    Renders 2D structure as SVG with optional atom highlights and color schemes.
    """
    if mol is None:
        return "<svg width='450' height='320'><text x='50' y='50'>Invalid Molecule</text></svg>"
    
    # Generate clean 2D coordinates
    mol_copy = Chem.Mol(mol)
    try:
        AllChem.Compute2DCoords(mol_copy)
    except Exception:
        pass
    
    drawer = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
    opts = drawer.drawOptions()
    opts.addStereoAnnotation = True
    opts.comicMode = False
    
    if highlight_atoms:
        drawer.DrawMolecule(
            mol_copy,
            highlightAtoms=highlight_atoms,
            highlightAtomColors=highlight_atom_colors or {}
        )
    else:
        drawer.DrawMolecule(mol_copy)
        
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    return svg


def draw_molecule_2d_png(
    mol: Chem.Mol,
    highlight_atoms: Optional[List[int]] = None,
    size: Tuple[int, int] = (450, 320)
) -> bytes:
    """
    Renders 2D structure as PNG bytes (ideal for ReportLab PDF reports).
    """
    if mol is None:
        return b""
    mol_copy = Chem.Mol(mol)
    try:
        AllChem.Compute2DCoords(mol_copy)
    except Exception:
        pass
    
    drawer = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
    if highlight_atoms:
        drawer.DrawMolecule(mol_copy, highlightAtoms=highlight_atoms)
    else:
        drawer.DrawMolecule(mol_copy)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def generate_3d_conformer_block(mol: Chem.Mol) -> Tuple[bool, str, str]:
    """
    Generates a 3D conformer using ETKDGv3 and MMFF94 force-field energy minimization.
    Returns: (success, mol_block_or_error, pdb_block)
    """
    if mol is None:
        return False, "Invalid molecule", ""
    
    try:
        mol_h = Chem.AddHs(mol)
        params = AllChem.ETKDGv3()
        params.randomSeed = 42
        
        embed_result = AllChem.EmbedMolecule(mol_h, params)
        if embed_result != 0:
            # Fallback to standard embed
            AllChem.EmbedMolecule(mol_h, randomSeed=42)
        
        # Optimize with MMFF94 force field
        try:
            AllChem.MMFFOptimizeMolecule(mol_h, maxIters=500)
        except Exception:
            try:
                AllChem.UFFOptimizeMolecule(mol_h, maxIters=500)
            except Exception:
                pass
        
        mol_block = Chem.MolToMolBlock(mol_h)
        pdb_block = Chem.MolToPDBBlock(mol_h)
        return True, mol_block, pdb_block
    except Exception as e:
        return False, f"3D generation error: {str(e)}", ""
