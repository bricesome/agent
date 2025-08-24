# 🚀 Guide de Démarrage Rapide

## ⚡ Démarrage en 3 Étapes

### 1️⃣ Installation des Dépendances
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialisation de la Démonstration
```bash
python init_demo.py
```

### 3️⃣ Lancement de l'Application
```bash
streamlit run app.py
```

## 🌐 Accès à l'Application
Ouvrez votre navigateur et allez sur : **http://localhost:8501**

## 🎯 Première Utilisation

### Créer un Agent IA
1. Allez dans "🤖 Agents"
2. Cliquez sur "➕ Créer un Nouvel Agent"
3. Remplissez les informations :
   - **Nom** : Mon Premier Agent
   - **Domaine** : Marketing
   - **Type** : Analyse
   - **Prompt Système** : Vous êtes un expert en marketing digital...
4. Cliquez sur "✅ Créer l'Agent"

### Exécuter un Agent
1. Cliquez sur "▶️ Exécuter" pour votre agent
2. Choisissez le type de contenu (texte, PDF, Word)
3. Ajoutez vos instructions
4. Cliquez sur "🚀 Exécuter l'Agent IA"

## 📁 Fichiers Importants

- **`app.py`** : Application principale
- **`pages/execute_agent.py`** : Page d'exécution
- **`agents.json`** : Base de données des agents
- **`models.json`** : Configuration des modèles
- **`requirements.txt`** : Dépendances Python

## 🔧 Scripts de Lancement

### Windows
- **`run.bat`** : Double-cliquez pour lancer
- **`run.ps1`** : Exécutez dans PowerShell

### Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

## 🐛 Dépannage Rapide

**Erreur de port** : `streamlit run app.py --server.port 8502`

**Erreur de dépendances** : `pip install --upgrade -r requirements.txt`

**Problème de permissions** : Exécutez en tant qu'administrateur

## 📞 Support
Consultez le `README.md` complet pour plus de détails et d'options avancées.

---

**🎉 Votre plateforme est prête ! Bonne exploration !**
