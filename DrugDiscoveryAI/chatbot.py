"""
Ollama-Powered Educational Chatbot for EGFR Virtual Screening.
Provides simple, student-friendly explanations of molecular descriptors,
AI predictions, Lipinski rules, and SHAP interpretability.
Includes streaming local LLM generation and an intelligent offline fallback.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Generator
import requests

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = "gemma3:1b"


def check_ollama_status() -> Dict[str, Any]:
    """
    Checks if local Ollama service is reachable and returns installed models.
    """
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            model_names = [m.get("name", "") for m in models_data if m.get("name")]
            return {
                "available": True,
                "models": model_names,
                "selected_model": DEFAULT_MODEL if DEFAULT_MODEL in model_names else (model_names[0] if model_names else DEFAULT_MODEL)
            }
    except Exception as e:
        logger.debug(f"Ollama check failed: {e}")
    
    return {
        "available": False,
        "models": [],
        "selected_model": DEFAULT_MODEL
    }


def build_system_context(
    smiles: str,
    descriptors: Dict[str, Any],
    drug_likeness: Dict[str, Any],
    prediction_result: Optional[Dict[str, Any]] = None,
    shap_result: Optional[Dict[str, Any]] = None,
    similarity_matches: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Builds a rich, concise context prompt about the current molecule for Ollama.
    """
    mol_wt = descriptors.get("MolWt", "N/A")
    logp = descriptors.get("MolLogP", "N/A")
    tpsa = descriptors.get("TPSA", "N/A")
    qed = descriptors.get("QED", "N/A")

    lip = drug_likeness.get("lipinski", {})
    lip_status = lip.get("status", "N/A")
    lip_viol = lip.get("violations_count", 0)

    pred_text = "N/A"
    prob_text = "N/A"
    if prediction_result and prediction_result.get("success"):
        pred_text = prediction_result.get("prediction", "N/A")
        prob_text = f"{prediction_result.get('prob_active', 0)*100:.1f}%"

    top_pos_shap = []
    top_neg_shap = []
    if shap_result:
        top_pos_shap = [d.get("feature", "") for d in shap_result.get("positive_drivers", [])[:3]]
        top_neg_shap = [d.get("feature", "") for d in shap_result.get("negative_drivers", [])[:3]]

    sim_text = "N/A"
    if similarity_matches:
        top_sim = similarity_matches[0]
        sim_text = f"{top_sim.get('name', 'N/A')} ({top_sim.get('similarity_pct', 0)}% Tanimoto similarity)"

    context = f"""You are an enthusiastic AI Chemoinformatics Tutor helping a college student explain their project on Human EGFR (CHEMBL203) cancer drug discovery to their teacher.
Always explain things simply, using everyday analogies (like locks and keys, coffee filters, or pill absorption in the body). Avoid jargon where possible, or define it immediately. Keep answers concise (2-4 short paragraphs or bullet points).

Current Molecule Being Inspected:
- SMILES: {smiles}
- Molecular Weight: {mol_wt} Da (Ideal <= 500 Da)
- LogP (Lipophilicity/Greasy-ness): {logp} (Ideal <= 5.0)
- Polar Surface Area (TPSA): {tpsa} Å² (Ideal <= 140 Å²)
- Oral Drug-Likeness (Lipinski Rule of 5): {lip_status} ({lip_viol} violations)
- AI Virtual Screening Prediction: {pred_text} (Inhibition Probability: {prob_text})
- Favorable SHAP Substructures (+Binding): {', '.join(top_pos_shap) if top_pos_shap else 'Aromatic rings / core fragments'}
- Unfavorable SHAP Substructures (-Binding): {', '.join(top_neg_shap) if top_neg_shap else 'None significant'}
- Top Approved Drug Similarity: {sim_text}
"""
    return context


def get_rule_based_fallback_response(user_query: str, context_str: str) -> str:
    """
    Intelligent fallback response generator if Ollama is not running or times out.
    Ensures the student NEVER faces an error or empty chat during a presentation!
    """
    q = user_query.lower()
    
    if "teacher" in q or "explain" in q or "simple" in q or "presentation" in q:
        return (
            "🎓 **How to Explain This to Your Teacher:**\n\n"
            "1. **The Biological Lock:** Think of cancer cells as having a faulty 'ON' switch called **EGFR**. When active, it tells the tumor to divide uncontrollably.\n"
            "2. **Our Molecule as a Key:** This molecule is tested as a candidate 'key' to fit inside that EGFR lock and turn it OFF.\n"
            "3. **What the AI Did:** Our Random Forest model analyzed the molecule's 2048-bit digital fingerprint (ECFP4) and predicted whether it will bind tightly (**Active**) or bounce off (**Inactive**).\n"
            "4. **Oral Bioavailability:** We checked **Lipinski's Rule of 5** to verify whether a patient could swallow this as an oral pill rather than needing intravenous injection."
        )
    elif "active" in q or "inactive" in q or "prediction" in q or "why" in q:
        return (
            "🎯 **Why the AI Made This Prediction:**\n\n"
            "The model evaluates molecular geometry and electronic charge distributions:\n"
            "- **Active Compounds:** Typically contain a flat, aromatic nitrogen-containing scaffold (like a quinazoline core) that forms critical hydrogen bonds inside the ATP-binding pocket of EGFR.\n"
            "- **Inactive Compounds (like Aspirin or Caffeine):** Are either too small, lack the essential aromatic anchors, or have shapes that cannot reach key amino acid residues in the kinase domain."
        )
    elif "lipinski" in q or "rule" in q or "bioavailability" in q:
        return (
            "💊 **Understanding Lipinski's Rule of Five:**\n\n"
            "In 1997, scientist Christopher Lipinski analyzed thousands of successful medicines and found that orally active pills usually follow 4 simple rules of thumb:\n"
            "1. **Weight <= 500 Da:** Not too bulky to pass through gut membranes.\n"
            "2. **LogP <= 5:** Not too greasy (oil-like) and not too watery.\n"
            "3. **H-Bond Donors <= 5 & Acceptors <= 10:** Allows the molecule to shed water molecules and cross into the bloodstream.\n\n"
            "If a molecule has 0 or 1 violation, it has a high chance of being an effective oral tablet!"
        )
    elif "shap" in q or "green" in q or "red" in q or "color" in q:
        return (
            "💡 **Understanding the SHAP Highlights (Explainable AI):**\n\n"
            "- 🟢 **Green Atoms (+SHAP):** These are 'Good Anchors'. They fit snugly into the EGFR protein pocket and boosted the AI's confidence that this molecule will inhibit cancer growth.\n"
            "- 🔴 **Red Atoms (-SHAP):** These are 'Clashing Atoms'. They may create steric strain, excessive bulk, or unfavorable charges that weaken binding.\n\n"
            "*Key point for your teacher:* SHAP converts a black-box AI into a transparent tool that medicinal chemists can actually trust and modify!"
        )
    else:
        return (
            "🧬 **Summary of This Compound:**\n\n"
            "This molecule is being evaluated as an EGFR tyrosine kinase inhibitor for lung cancer therapy. "
            "Our chemoinformatics engine validates its 3D shape and oral drug-likeness, our machine learning model predicts its binding probability, "
            "and SHAP provides an atom-by-atom explanation of why it works. "
            "\n\nFeel free to ask me:\n"
            "- *'How do I explain this to my teacher?'*\n"
            "- *'What does Lipinski Rule of 5 mean?'*\n"
            "- *'Why are some atoms highlighted green and red?'*"
        )


def stream_ollama_chat(
    prompt: str,
    system_context: str,
    model_name: str = DEFAULT_MODEL,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Generator[str, None, None]:
    """
    Streams response tokens from local Ollama LLM, falling back seamlessly if unavailable.
    """
    messages = [{"role": "system", "content": system_context}]
    
    if conversation_history:
        for msg in conversation_history[-4:]:  # Keep recent turns
            messages.append({"role": msg["role"], "content": msg["content"]})
            
    messages.append({"role": "user", "content": prompt})

    try:
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.4,
                "top_p": 0.9,
                "num_predict": 350
            }
        }
        
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            stream=True,
            timeout=10
        )
        
        if resp.status_code == 200:
            for line in resp.iter_lines(decode_unicode=True):
                if line:
                    chunk = json.loads(line)
                    msg = chunk.get("message", {})
                    token = msg.get("content", "")
                    if token:
                        yield token
                    if chunk.get("done", False):
                        return
        else:
            fallback = get_rule_based_fallback_response(prompt, system_context)
            yield fallback
            return
            
    except Exception as e:
        logger.info(f"Ollama stream fallback triggered: {e}")
        fallback = get_rule_based_fallback_response(prompt, system_context)
        yield fallback
        return
