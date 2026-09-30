@echo off
echo ======================================================================
echo Launching EGFR Drug Discovery Assistant [PART 2: AI Virtual Screening]
echo ======================================================================
set DEMO_PART=2
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run DrugDiscoveryAI\app.py
pause
