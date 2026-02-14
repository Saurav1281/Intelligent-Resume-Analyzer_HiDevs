@echo off
echo Starting Intelligent Resume Analyzer...
echo Ensure you have Python installed and the virtual environment is active (if used).
echo.
pip install -r requirements.txt
cls
streamlit run app.py
pause
