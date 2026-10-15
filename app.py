"""
Root launcher for EGFR Drug Discovery Assistant (Herbarium Alpinum Design System).
Invokes DrugDiscoveryAI/app.py.
"""
import os
import sys
import runpy

# Add DrugDiscoveryAI to sys.path
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DrugDiscoveryAI")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Run the unified DrugDiscoveryAI application
runpy.run_path(os.path.join(BASE_DIR, "app.py"), run_name="__main__")