@echo off
echo ======================================================================
echo Launching EGFR Drug Discovery Assistant [PART 1: Chemoinformatics Engine]
echo ======================================================================
set DEMO_PART=1
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run DrugDiscoveryAI\app.py
pause
