#!/usr/bin/env python3
"""
Script d'initialisation de la démonstration
Charge des agents IA pré-configurés pour tester la plateforme
"""

import json
import os
import shutil
from datetime import datetime

def init_demo():
    """Initialise la démonstration avec des agents pré-configurés"""
    
    print("🚀 Initialisation de la démonstration...")
    
    # Vérifier si le fichier de démonstration existe
    demo_file = "demo_agents.json"
    if not os.path.exists(demo_file):
        print(f"❌ Fichier {demo_file} non trouvé")
        return False
    
    # Charger les agents de démonstration
    try:
        with open(demo_file, 'r', encoding='utf-8') as f:
            demo_agents = json.load(f)
        print(f"✅ {len(demo_agents)} agents de démonstration chargés")
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {demo_file}: {e}")
        return False
    
    # Vérifier si des agents existent déjà
    agents_file = "agents.json"
    if os.path.exists(agents_file):
        try:
            with open(agents_file, 'r', encoding='utf-8') as f:
                existing_agents = json.load(f)
            
            if existing_agents:
                print(f"⚠️ {len(existing_agents)} agents existants détectés")
                response = input("Voulez-vous remplacer les agents existants ? (o/n): ").lower()
                if response != 'o':
                    print("❌ Initialisation annulée")
                    return False
        except Exception as e:
            print(f"⚠️ Erreur lors de la lecture des agents existants: {e}")
    
    # Sauvegarder les agents de démonstration
    try:
        with open(agents_file, 'w', encoding='utf-8') as f:
            json.dump(demo_agents, f, ensure_ascii=False, indent=2)
        print(f"✅ Agents de démonstration sauvegardés dans {agents_file}")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False
    
    # Créer le fichier des modèles s'il n'existe pas
    models_file = "models.json"
    if not os.path.exists(models_file):
        default_models = [
            {
                "name": "GPT-4",
                "provider": "OpenAI",
                "status": "active",
                "description": "Modèle de langage avancé d'OpenAI",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "name": "Claude-3",
                "provider": "Anthropic",
                "status": "active",
                "description": "Assistant IA conversationnel d'Anthropic",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "name": "Gemini Pro",
                "provider": "Google",
                "status": "active",
                "description": "Modèle multimodal de Google",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "name": "Llama 2",
                "provider": "Meta",
                "status": "active",
                "description": "Modèle open source de Meta",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        
        try:
            with open(models_file, 'w', encoding='utf-8') as f:
                json.dump(default_models, f, ensure_ascii=False, indent=2)
            print(f"✅ Modèles par défaut créés dans {models_file}")
        except Exception as e:
            print(f"⚠️ Erreur lors de la création des modèles: {e}")
    
    print("\n🎉 Démonstration initialisée avec succès !")
    print("\n📋 Agents disponibles:")
    for agent in demo_agents:
        print(f"  • {agent['name']} ({agent['type']}) - {agent['domain']}")
    
    print(f"\n🚀 Pour lancer l'application:")
    print(f"  streamlit run app.py")
    print(f"  ou double-cliquez sur run.bat (Windows)")
    
    return True

def show_help():
    """Affiche l'aide du script"""
    print("""
🤖 Script d'initialisation de la démonstration

Usage:
  python init_demo.py          # Initialise la démonstration
  python init_demo.py --help   # Affiche cette aide

Ce script:
  • Charge des agents IA pré-configurés
  • Crée la structure de données initiale
  • Configure les modèles par défaut
  • Prépare la plateforme pour la démonstration

Fichiers créés:
  • agents.json     - Base de données des agents
  • models.json     - Configuration des modèles IA

Agents de démonstration:
  • Analyste Financier Pro
  • Rédacteur Marketing
  • Traducteur Multilingue
  • Développeur Code
  • Résumeur de Documents
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_help()
    else:
        init_demo()
