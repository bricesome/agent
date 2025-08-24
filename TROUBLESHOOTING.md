# 🔧 Guide de Résolution des Problèmes

## 🚨 Problèmes Courants et Solutions

### ❌ Erreur "No module named 'streamlit'"

**Problème** : Streamlit n'est pas installé

**Solution** :
```bash
# Installer Streamlit
pip install streamlit

# Ou installer toutes les dépendances
pip install -r requirements.txt
```

**Vérification** :
```bash
python -c "import streamlit; print('Streamlit installé')"
```

### ❌ Erreur de version Python

**Problème** : Version Python trop ancienne

**Solution** :
- **Windows** : Téléchargez Python 3.8+ depuis [python.org](https://python.org)
- **Linux** : `sudo apt-get install python3.8`
- **Mac** : `brew install python@3.8`

**Vérification** :
```bash
python --version
# Doit afficher Python 3.8.0 ou supérieur
```

### ❌ Erreur de permissions

**Problème** : Accès refusé aux fichiers

**Solution Windows** :
- Exécutez PowerShell en tant qu'administrateur
- Ou double-cliquez sur `run.bat`

**Solution Linux/Mac** :
```bash
chmod +x *.py *.sh
sudo pip install -r requirements.txt
```

### ❌ Port déjà utilisé

**Problème** : Port 8501 occupé

**Solution** :
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502

# Ou tuer le processus utilisant le port
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9
```

### ❌ Erreur de dépendances

**Problème** : Modules manquants ou incompatibles

**Solution** :
```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances avec versions spécifiques
pip install -r requirements.txt --force-reinstall

# Ou installer manuellement
pip install streamlit==1.28.1 pandas==2.1.3
```

### ❌ Erreur de fichiers JSON

**Problème** : Fichiers de données corrompus

**Solution** :
```bash
# Supprimer les fichiers corrompus
rm agents.json models.json

# Réinitialiser la démonstration
python init_demo.py
```

### ❌ Erreur de navigation entre pages

**Problème** : Problème avec `st.switch_page`

**Solution** : Utilisez la navigation standard de Streamlit
```python
# Remplacer
st.switch_page("pages/execute_agent.py")

# Par
st.success("Redirection...")
time.sleep(1)
st.rerun()
```

## 🔍 Diagnostic Avancé

### Test des composants individuels

```bash
# Test des imports
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import pandas; print('✅ Pandas OK')"
python -c "import plotly; print('✅ Plotly OK')"

# Test de l'application
python -c "import app; print('✅ App OK')"
```

### Vérification de l'environnement

```bash
# Variables d'environnement
echo $PATH
echo $PYTHONPATH

# Version des packages
pip list | grep -E "(streamlit|pandas|plotly)"
```

### Logs détaillés

```bash
# Mode debug Streamlit
streamlit run app.py --logger.level debug

# Logs Python
python -u app.py 2>&1 | tee app.log
```

## 🛠️ Solutions Spécifiques par OS

### Windows

**Problème** : Erreur de chemin
```bash
# Utiliser des chemins Windows
set PYTHONPATH=%PYTHONPATH%;C:\Users\techa\ai-agents-platform
```

**Problème** : Encodage des fichiers
```python
# Dans le code Python
with open('file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Linux/Mac

**Problème** : Permissions d'exécution
```bash
chmod +x *.py *.sh
```

**Problème** : Environnement virtuel
```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## 📱 Problèmes de Performance

### Application lente

**Solutions** :
- Utilisez `@st.cache_data` pour les données
- Limitez la taille des fichiers uploadés
- Optimisez les requêtes IA

### Mémoire insuffisante

**Solutions** :
- Redémarrez l'application régulièrement
- Utilisez des fichiers plus petits
- Augmentez la RAM disponible

## 🌐 Problèmes de Réseau

### Proxy/Entreprise

**Solution** :
```bash
# Configuration proxy
pip install --proxy http://proxy.company.com:8080 -r requirements.txt

# Variables d'environnement
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
```

### Firewall

**Solution** :
- Autorisez Python et Streamlit dans le firewall
- Vérifiez que le port 8501 est ouvert

## 📞 Support Avancé

### Collecte d'informations

```bash
# Informations système
python -c "import platform; print(platform.platform())"
python -c "import sys; print(sys.version)"

# Dépendances installées
pip freeze > requirements_installed.txt

# Logs d'erreur
# Copiez les messages d'erreur complets
```

### Ressources utiles

- **Documentation Streamlit** : [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues** : [github.com/streamlit/streamlit/issues](https://github.com/streamlit/streamlit/issues)
- **Stack Overflow** : Tag `streamlit`

### Contact

En cas de problème persistant :
1. Vérifiez que vous avez suivi toutes les étapes
2. Consultez la documentation officielle
3. Recherchez des solutions similaires en ligne
4. Créez une issue détaillée avec les logs d'erreur

---

**💡 Conseil** : Commencez toujours par les solutions les plus simples avant d'essayer les solutions avancées.
