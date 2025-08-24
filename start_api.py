# 🚀 Script de Démarrage de l'API REST
import subprocess
import sys
import os
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_api():
    """Démarre l'API REST"""
    try:
        logger.info("�� Démarrage de l'API REST...")
        
        # Vérifier que les dépendances sont installées
        try:
            import fastapi
            import uvicorn
            logger.info("✅ Dépendances FastAPI installées")
        except ImportError:
            logger.error("❌ Dépendances FastAPI manquantes")
            logger.info("Installation des dépendances...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-prod.txt"], check=True)
        
        # Démarrer l'API
        api_process = subprocess.Popen([
            sys.executable, "api/rest_api.py"
        ])
        
        logger.info("✅ API REST démarrée sur http://localhost:8000")
        logger.info("📚 Documentation: http://localhost:8000/docs")
        logger.info("�� Pour arrêter l'API, appuie sur Ctrl+C")
        
        try:
            api_process.wait()
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt de l'API...")
            api_process.terminate()
            api_process.wait()
            logger.info("✅ API arrêtée")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors du démarrage de l'API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_api()
