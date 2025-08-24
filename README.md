# 🤖 Plateforme de Gestion des Agents IA

Une plateforme moderne et intuitive développée avec Streamlit pour créer, gérer et exécuter des agents d'intelligence artificielle.

## 🚀 Démarrage Rapide

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Initialisation de la démonstration
```bash
python init_demo.py
```

### 3. Lancement de l'application
```bash
streamlit run app.py
```

## 🌐 Accès
Ouvrez votre navigateur et allez sur : **http://localhost:8501**

## ✨ Fonctionnalités

- **Dashboard interactif** avec métriques et graphiques
- **Gestion des agents IA** : création, édition, suppression
- **Support multi-format** : texte, PDF, Word
- **Modèles IA** : GPT-4, Claude-3, Gemini Pro, Llama 2
- **Interface moderne** avec design attrayant

## 📁 Structure

```
ai-agents-platform/
├── app.py                 # Application principale
├── pages/execute_agent.py # Page d'exécution
├── requirements.txt       # Dépendances
├── init_demo.py          # Initialisation
├── demo_agents.json      # Agents de démo
└── run.bat               # Lancement Windows
```

## 🎯 Utilisation

1. **Créer un agent** : Nom, domaine, type, prompt système
2. **Sélectionner un modèle** : Choisir le modèle IA à utiliser
3. **Exécuter l'agent** : Traiter du contenu (texte, PDF, Word)
4. **Analyser les résultats** : Visualiser et télécharger les résultats

## 🔧 Support

- **Windows** : Double-cliquez sur `run.bat`
- **Tests** : `python test_app.py`
- **Aide** : `python init_demo.py --help`

---

**Développé avec ❤️ et Streamlit**
