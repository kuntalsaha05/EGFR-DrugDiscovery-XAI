"""
Root launcher for EGFR Drug Discovery Assistant.
Invokes DrugDiscoveryAI/app.py.
"""
import os
import sys

# Add DrugDiscoveryAI to sys.path
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DrugDiscoveryAI")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Run the DrugDiscoveryAI application
import runpy
runpy.run_path(os.path.join(BASE_DIR, "app.py"), run_name="__main__")
