@echo off
echo ======================================================================
echo Launching EGFR Drug Discovery Assistant [PART 3: Full Explainable AI Platform]
echo ======================================================================
set DEMO_PART=3
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run DrugDiscoveryAI\app.py
pause
