# 🧪 Guide de Test Rapide - Plateforme Agents IA

## 🚀 Test Immédiat

### 1. Vérification de l'Installation
```bash
# Dans CMD (pas PowerShell)
cd "C:\Users\techa\OneDrive\Documents\Projets\ai-agents-platform"

# Vérifier Python
python --version

# Vérifier Streamlit
streamlit --version
```

### 2. Installation des Dépendances
```bash
# Installer les dépendances
pip install -r requirements.txt

# Ou installer Streamlit uniquement
pip install streamlit streamlit-option-menu pandas plotly
```

### 3. Lancement de l'Application
```bash
# Lancer l'application
streamlit run app.py

# Ou avec port spécifique
streamlit run app.py --server.port 8502
```

## 🌐 Test de l'Interface

### Accès
- **URL** : http://localhost:8501 (ou 8502)
- **Navigateur** : Chrome, Firefox, Edge

### Vérifications Visuelles
✅ **Dashboard** : Métriques et graphiques s'affichent  
✅ **Navigation** : Menu latéral fonctionne  
✅ **Couleurs** : Gradients bleu-violet visibles  
✅ **Responsive** : Interface s'adapte à la taille d'écran  

## 🤖 Test des Fonctionnalités

### 1. Création d'Agent
1. Aller dans "🤖 Agents"
2. Cliquer "➕ Créer un Nouvel Agent"
3. Remplir le formulaire :
   - **Nom** : Test Agent
   - **Domaine** : Test
   - **Type** : Analyse
   - **Prompt** : Vous êtes un agent de test
4. Cliquer "✅ Créer l'Agent"

**Résultat attendu** : Agent créé et visible dans la liste

### 2. Exécution d'Agent
1. Cliquer "▶️ Exécuter" sur l'agent créé
2. Choisir "📝 Texte direct"
3. Entrer du texte : "Bonjour, test de l'agent"
4. Cliquer "🚀 Exécuter l'Agent IA"

**Résultat attendu** : Résultat simulé affiché

### 3. Gestion des Modèles
1. Aller dans "⚙️ Modèles"
2. Vérifier les modèles pré-configurés
3. Sélectionner un modèle dans la sidebar

**Résultat attendu** : Modèles visibles et sélectionnables

## 🔍 Tests Techniques

### Test des Imports
```bash
python test_app.py
```

**Résultat attendu** : Tous les tests passent

### Test des Fichiers
```bash
# Vérifier la structure
dir
dir pages
dir .streamlit
```

**Fichiers requis** :
- ✅ app.py
- ✅ pages/execute_agent.py
- ✅ requirements.txt
- ✅ .streamlit/config.toml

### Test des Données
```bash
# Vérifier les agents
python -c "import json; print(json.load(open('agents.json')))"

# Vérifier les modèles
python -c "import json; print(json.load(open('models.json')))"
```

## 🚨 Problèmes Courants

### Erreur "streamlit not found"
```bash
# Solution
pip install streamlit
```

### Erreur de port
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502
```

### Erreur de modules
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Problème de navigation
- Vérifier que `st.rerun()` fonctionne
- Utiliser la navigation standard de Streamlit

## 📊 Métriques de Succès

### Interface
- ✅ Page se charge en < 5 secondes
- ✅ Tous les éléments visuels s'affichent
- ✅ Navigation fluide entre les sections
- ✅ Formulaires fonctionnels

### Fonctionnalités
- ✅ Création d'agent réussie
- ✅ Exécution d'agent fonctionne
- ✅ Gestion des modèles opérationnelle
- ✅ Export des résultats disponible

### Performance
- ✅ Réactivité de l'interface
- ✅ Chargement rapide des données
- ✅ Graphiques interactifs
- ✅ Pas d'erreurs dans la console

## 🎯 Checklist de Test

- [ ] Application se lance sans erreur
- [ ] Interface s'affiche correctement
- [ ] Navigation fonctionne
- [ ] Création d'agent réussie
- [ ] Exécution d'agent fonctionne
- [ ] Gestion des modèles opérationnelle
- [ ] Export des résultats disponible
- [ ] Pas d'erreurs dans la console
- [ ] Interface responsive
- [ ] Couleurs et design corrects

## 🚀 Prochaines Étapes

1. **Test complet** : Valider toutes les fonctionnalités
2. **Personnalisation** : Adapter l'interface à vos besoins
3. **Intégration IA** : Configurer de vraies clés API
4. **Déploiement** : Mettre en production

---

**🎉 Si tous les tests passent, votre plateforme IA est prête !**
