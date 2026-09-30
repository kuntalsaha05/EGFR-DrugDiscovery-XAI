"""
Similarity Engine for EGFR Therapeutics.
Computes Morgan fingerprint (ECFP4) Tanimoto similarity against
FDA-approved and clinically established EGFR kinase inhibitors.
Provides clinical intelligence, inhibitor generation, approval year, and indications.
"""

from typing import List, Dict, Any, Optional
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import AllChem

RDLogger.DisableLog("rdApp.*")

APPROVED_EGFR_DRUGS = [
    {
        "name": "Gefitinib (Iressa)",
        "smiles": "COc1cc2ncnc(Nc3ccc(F)c(Cl)c3)c2cc1OCCCN1CCOCC1",
        "generation": "1st Generation (Reversible)",
        "fda_approval_year": 2003,
        "mechanism": "Reversible competitive ATP inhibitor of EGFR tyrosine kinase domain.",
        "target_mutations": "EGFR Exon 19 Deletion, L858R",
        "clinical_indication": "Non-Small Cell Lung Cancer (NSCLC)",
        "formula": "C22H24ClFN4O3"
    },
    {
        "name": "Erlotinib (Tarceva)",
        "smiles": "COCCOc1cc2c(Nc3cccc(c3)C#C)ncnc2cc1OCCOC",
        "generation": "1st Generation (Reversible)",
        "fda_approval_year": 2004,
        "mechanism": "Reversible quinazoline-based EGFR ATP-site kinase inhibitor.",
        "target_mutations": "EGFR Exon 19 Deletions, L858R",
        "clinical_indication": "NSCLC, Advanced Pancreatic Cancer",
        "formula": "C22H23N3O4"
    },
    {
        "name": "Afatinib (Gilotrif)",
        "smiles": "CN(C)C/C=C/C(=O)Nc1cc2c(Nc3ccc(Cl)c(F)c3)ncnc2cc1O[C@H]1CCOC1",
        "generation": "2nd Generation (Irreversible)",
        "fda_approval_year": 2013,
        "mechanism": "Covalent irreversible ErbB family blocker (EGFR, HER2, HER4) binding Cys797.",
        "target_mutations": "EGFR Exon 19 Deletions, L858R, S768I, L861Q, G719X",
        "clinical_indication": "Metastatic NSCLC",
        "formula": "C24H25ClFN5O3"
    },
    {
        "name": "Osimertinib (Tagrisso)",
        "smiles": "CN(C)CC=CC(=O)Nc1cc(Nc2ncc(c(n2)C(F)(F)F)Nc3ccccc3N(C)C)c(OC)cc1NC(=O)C=C",
        "generation": "3rd Generation (Mutant-Selective)",
        "fda_approval_year": 2015,
        "mechanism": "Covalently targets Cys797 while sparing wild-type EGFR; overcomes T790M gatekeeper mutation.",
        "target_mutations": "EGFR T790M resistance mutation, Exon 19 Del, L858R",
        "clinical_indication": "EGFR T790M-positive metastatic NSCLC, 1st-line EGFR-mutated NSCLC",
        "formula": "C28H33N7O2"
    },
    {
        "name": "Lapatinib (Tykerb)",
        "smiles": "CS(=O)(=O)CCNCc1ccc(o1)c2ccc3c(c2)c(ncn3)Nc4ccc(c(c4)Cl)OCc5cccc(c5)F",
        "generation": "1st/2nd Gen Dual TKI",
        "fda_approval_year": 2007,
        "mechanism": "Dual reversible inhibitor of both EGFR (ErbB1) and HER2 (ErbB2) tyrosine kinases.",
        "target_mutations": "EGFR / HER2 overexpression",
        "clinical_indication": "HER2-positive Advanced or Metastatic Breast Cancer",
        "formula": "C29H26ClFN4O4S"
    },
    {
        "name": "Dacomitinib (Vizimpro)",
        "smiles": "CN(C)CC=CC(=O)Nc1cc2c(Nc3ccc(F)c(Cl)c3)ncnc2cc1OCC4CCN(C)CC4",
        "generation": "2nd Generation (Irreversible)",
        "fda_approval_year": 2018,
        "mechanism": "Second-generation irreversible pan-HER (EGFR, HER2, HER4) tyrosine kinase inhibitor.",
        "target_mutations": "EGFR Exon 19 Deletion, L858R",
        "clinical_indication": "First-line treatment of metastatic NSCLC",
        "formula": "C24H25ClFN5O2"
    }
]


class EGFRSimilarityEngine:
    """
    Computes Tanimoto similarity between query molecule and approved EGFR inhibitors.
    """
    def __init__(self):
        self.reference_drugs = []
        self._prepare_reference_fingerprints()

    def _prepare_reference_fingerprints(self):
        """Precomputes Morgan fingerprints for reference drugs."""
        for drug in APPROVED_EGFR_DRUGS:
            mol = Chem.MolFromSmiles(drug["smiles"])
            if mol:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
                self.reference_drugs.append({
                    **drug,
                    "mol": mol,
                    "fp": fp
                })

    def search_similar_drugs(
        self,
        query_mol: Chem.Mol,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Calculates Tanimoto similarity against approved EGFR drugs and ranks them.
        """
        if query_mol is None or not self.reference_drugs:
            return []

        query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, radius=2, nBits=2048)
        results = []

        for drug in self.reference_drugs:
            similarity = float(DataStructs.TanimotoSimilarity(query_fp, drug["fp"]))
            results.append({
                "name": drug["name"],
                "similarity": round(similarity, 4),
                "similarity_pct": round(similarity * 100.0, 1),
                "generation": drug["generation"],
                "fda_approval_year": drug["fda_approval_year"],
                "mechanism": drug["mechanism"],
                "target_mutations": drug["target_mutations"],
                "clinical_indication": drug["clinical_indication"],
                "smiles": drug["smiles"]
            })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


# Singleton
_similarity_engine_instance = None

def get_similarity_engine() -> EGFRSimilarityEngine:
    global _similarity_engine_instance
    if _similarity_engine_instance is None:
        _similarity_engine_instance = EGFRSimilarityEngine()
    return _similarity_engine_instance
