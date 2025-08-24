@echo off
echo ========================================
echo    Plateforme Agents IA - Streamlit
echo ========================================
echo.
echo Installation des dependances...
pip install -r requirements.txt
echo.
echo Lancement de l'application...
echo.
echo L'application sera accessible sur:
echo http://localhost:8501
echo.
echo Appuyez sur Ctrl+C pour arreter l'application
echo.
streamlit run app.py
pause
