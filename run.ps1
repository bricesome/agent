# Script PowerShell pour lancer la Plateforme Agents IA
# Exécutez ce script en tant qu'administrateur si nécessaire

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Plateforme Agents IA - Streamlit" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python depuis https://python.org" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Vérifier si pip est disponible
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip détecté: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip n'est pas disponible" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host ""
Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow

# Installer les dépendances
try {
    pip install -r requirements.txt
    Write-Host "✅ Dépendances installées avec succès" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors de l'installation des dépendances" -ForegroundColor Red
    Write-Host "Vérifiez votre connexion internet et réessayez" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host ""
Write-Host "🚀 Lancement de l'application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "L'application sera accessible sur:" -ForegroundColor White
Write-Host "http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter l'application" -ForegroundColor Yellow
Write-Host ""

# Lancer Streamlit
try {
    streamlit run app.py
} catch {
    Write-Host "❌ Erreur lors du lancement de Streamlit" -ForegroundColor Red
    Write-Host "Vérifiez que toutes les dépendances sont installées" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Appuyez sur Entrée pour quitter"
