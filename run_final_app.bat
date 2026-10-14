@echo off
echo ======================================================================
echo Launching Explainable AI Drug Discovery Assistant [FINAL FULL SYSTEM]
echo ======================================================================
set DEMO_PART=final
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run DrugDiscoveryAI\app.py
pause
