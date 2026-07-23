# Guide Complet des Nouvelles Fonctionnalités - Plateforme Agents IA

## **Table des Matières**

1. [ Système d'Authentification](#-système-dauthentification)
2. [ Base de Données Professionnelle](#️-base-de-données-professionnelle)
3. [ API REST](#-api-rest)
4. [ Structure du Projet](#-structure-du-projet)
5. [ Installation et Démarrage](#-installation-et-démarrage)
6. [ Exemples d'Utilisation](#-exemples-dutilisation)
7. [ Configuration Avancée](#-configuration-avancée)
8. [ Documentation API](#-documentation-api)

---

##  **Système d'Authentification**

### **Description**
Système d'authentification professionnel et sécurisé utilisant bcrypt pour le hachage des mots de passe et la gestion des sessions utilisateur.

### **Fonctionnalités**
-  **Inscription utilisateur** avec validation des données
-  **Connexion sécurisée** avec hachage bcrypt
-  **Gestion des sessions** avec expiration automatique
-  **Rôles utilisateur** (admin, user)
-  **Déconnexion** et invalidation des sessions

### **Utilisation**

#### **1. Inscription d'un nouvel utilisateur avec un script**
```python
from auth.auth_manager import AuthManager

auth_manager = AuthManager()

# Créer un nouvel utilisateur
success = auth_manager.register_user(
    username="john_doe",
    password="motdepasse123",
    email="john@example.com",
    role="user"
)

if success:
    print("Utilisateur créé avec succès")
else:
    print("Erreur lors de la création")
```

---

##  **Base de Données Professionnelle**

### **Description**
Gestionnaire de base de données SQLite évolutif avec architecture modulaire, prêt pour la migration vers PostgreSQL/MySQL en production.

### **Tables **
- **`users`** - Gestion des utilisateurs
- **`agents`** - Stockage des agents IA
- **`workflows`** - Gestion des workflows
- **`executions`** - Historique des exécutions
- **`sessions`** - Sessions utilisateur

### **Utilisation**

#### **1. Initialisation de la base de données**
```python
from database.db_manager import DatabaseManager

# Création une instance du gestionnaire
db_manager = DatabaseManager("data/ai_platform.db")

# La base de données automatiquement initialisée
# avec toutes les tables nécessaires
```

#### **2. Gestion des utilisateurs**
```python
# Insertion d'un utilisateur
user_id = db_manager.insert_user(
    username="admin",
    email="admin@example.com",
    password_hash="hash_bcrypt",
    role="admin"
)

# Récupérer un utilisateur
user = db_manager.get_user_by_username("admin")

# Mettre à jour la dernière connexion
db_manager.update_user_last_login(user_id)
```

#### **3. Gestion des agents**
```python
# Créer un nouvel agent
agent_id = db_manager.insert_agent(
    name="Assistant Marketing",
    description="Agent spécialisé en marketing digital",
    model_type="GPT-4",
    api_key="sk-...",
    configuration='{"temperature": 0.7}',
    created_by=user_id
)

# Récupérer tous les agents
agents = db_manager.get_all_agents()
```

#### **4. Suivi des exécutions**
```python
# Enregistrer une exécution
execution_id = db_manager.insert_execution(
    agent_id=agent_id,
    input_data="Analyse du marché français",
    output_data="Résultats de l'analyse...",
    status="completed",
    created_by=user_id
)

# Mettre à jour le statut
db_manager.update_execution_status(
    execution_id, 
    "completed", 
    "Résultats finaux..."
)

# Historique des exécutions
history = db_manager.get_execution_history(user_id, limit=10)
```

---

## **API REST**

### **Description**
API REST professionnelle construite avec FastAPI, offrant une interface moderne et documentée automatiquement pour toutes les opérations de la plateforme.

### **Endpoints Disponibles**

#### ** Authentification**
- `POST /auth/register` - Inscription utilisateur
- `POST /auth/login` - Connexion utilisateur
- `POST /auth/logout` - Déconnexion utilisateur

#### ** Agents**
- `GET /agents` - Liste des agents
- `POST /agents` - Création d'agent

#### ** Exécution**
- `POST /execute` - Exécution d'agent

#### ** Santé**
- `GET /health` - Vérification de la santé de l'API

### **Utilisation**

#### **1. Démarrage de l'API**
```bash
# Démarrer l'API
python start_api.py

# Ou directement
python api/rest_api.py
```

#### **2. Inscription via API**
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "motdepasse123",
       "role": "user"
     }'
```

#### **3. Connexion via API**
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "motdepasse123"
     }'
```

#### **4. Création d'agent via API**
```bash
# D'abord récupérer le token de session
TOKEN="session_john_doe_20241201_143022"

curl -X POST "http://localhost:8000/agents" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Assistant IA",
       "description": "Agent polyvalent",
       "model_type": "GPT-4"
     }'
```

---

##  **Structure du Projet**
```
ai-agents-platform/
├── 📁 auth/                    # Module d'authentification
│   ├── __init__.py
│   └── auth_manager.py        # Gestionnaire d'auth
├── 📁 database/               # Module de base de données
│   ├── __init__.py
│   └── db_manager.py         # Gestionnaire de DB
├── 📁 api/                    # Module API REST
│   ├── __init__.py
│   └── rest_api.py           # API FastAPI
├── 📁 data/                   # Données (créé automatiquement)
│   ├── users.json            # Utilisateurs
│   ├── sessions.json         # Sessions
│   └── ai_platform.db        # Base SQLite
├── 📁 pages/                  # Pages Streamlit existantes
├──  app_fixed.py           # Application principale
├──  ai_integration.py      # Intégration IA
├──  requirements.txt        # Dépendances de base
├──  requirements-prod.txt   # Dépendances production
├──  start_api.py           # Script de démarrage API
└──  README.md              # Documentation
```

---

##  **Installation et Démarrage**

### **1. Installation des Dépendances**
```bash
# Activer l'environnement virtuel
venv\Scripts\activate

# Installer les dépendances de production
pip install -r requirements-prod.txt
```

### **2. Démarrage de l'API REST**
```bash
# Option 1: Utiliser le script de démarrage
python start_api.py

# Option 2: Démarrer directement
python api/rest_api.py
```

### **3. Démarrage de l'Application Streamlit**
```bash
# Dans un autre terminal
streamlit run app_fixed.py
```

### **4. Accès aux Services**
-  **Application Streamlit**: http://localhost:8501
-  **API REST**: http://localhost:8000
-  **Documentation API**: http://localhost:8000/docs
-  **Documentation Alternative**: http://localhost:8000/redoc

---

##  **Exemples d'Utilisation**

### **Exemple 1: Création d'un Utilisateur et Agent**
```python
from auth.auth_manager import AuthManager
from database.db_manager import DatabaseManager

# Initialiser les gestionnaires
auth_manager = AuthManager()
db_manager = DatabaseManager()

# 1. Créer un utilisateur
auth_manager.register_user("alice", "password123", "alice@example.com")

# 2. Authentifier l'utilisateur
user = auth_manager.authenticate_user("alice", "password123")

# 3. Créer un agent
user_id = db_manager.get_user_id("alice")
agent_id = db_manager.insert_agent(
    name="Assistant Créatif",
    description="Agent pour la création de contenu",
    model_type="Claude-3",
    created_by=user_id
)

print(f" Agent créé avec l'ID: {agent_id}")
```

### **Exemple 2: Utilisation de l'API REST**
```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"

# 1. Inscription
register_data = {
    "username": "bob",
    "email": "bob@example.com",
    "password": "password123"
}

response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(f"Inscription: {response.json()}")

# 2. Connexion
login_data = {
    "username": "bob",
    "password": "password123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
session_data = response.json()
token = session_data["session_id"]

# 3. Créer un agent
headers = {"Authorization": f"Bearer {token}"}
agent_data = {
    "name": "Assistant Analytique",
    "description": "Agent pour l'analyse de données",
    "model_type": "GPT-4"
}

response = requests.post(f"{BASE_URL}/agents", json=agent_data, headers=headers)
print(f"Agent créé: {response.json()}")
```

---

##  **Configuration Avancée**

### **1. Configuration de la Base de Données**
```python
# Utiliser une base de données personnalisée
db_manager = DatabaseManager("custom/path/database.db")

# Ou utiliser des paramètres de connexion
db_manager = DatabaseManager(
    db_path="data/production.db",
    # Ajouter des options de configuration
)
```

### **2. Configuration de l'Authentification**
```python
# Personnaliser la durée des sessions
class CustomAuthManager(AuthManager):
    def _create_session(self, username: str) -> str:
        # Sessions de 48h au lieu de 24h
        expires_at = datetime.now() + timedelta(hours=48)
        # ... reste du code
```

### **3. Configuration de l'API**
```python
# Modifier les paramètres de l'API
app = FastAPI(
    title="Mon API Personnalisée",
    version="2.0.0",
    docs_url="/api-docs",  # URL personnalisée
    redoc_url="/api-redoc"
)

# Ajouter des middlewares personnalisés
@app.middleware("http")
async def custom_middleware(request, call_next):
    # Logique personnalisée
    response = await call_next(request)
    return response
```

---

##  **Documentation API**

### **Accès à la Documentation**
Une fois l'API démarrée, accédez à :
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **Tests Interactifs**
La documentation Swagger permet de :
-  Voir tous les endpoints disponibles
-  Tester les API directement depuis le navigateur
-  Voir les modèles de données (Pydantic)
-  Exécuter des requêtes avec des exemples

### **Exemple de Documentation d'Endpoint**
```python
@app.post("/agents", response_model=Dict[str, Any])
async def create_agent(
    agent_data: AgentCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Crée un nouvel agent IA.
    
    **Paramètres:**
    - agent_data: Données de l'agent à créer
    - current_user: Utilisateur authentifié (automatique)
    
    **Retourne:**
    - Dictionnaire avec le statut et l'ID de l'agent
    
    **Erreurs:**
    - 400: Données invalides
    - 401: Non authentifié
    - 500: Erreur serveur
    """
    # ... implémentation
```

---

##  **Dépannage**

### **Erreurs Communes**

#### **1. ModuleNotFoundError**
```bash
# Solution: Installer les dépendances
pip install -r requirements-prod.txt
```

#### **2. Port déjà utilisé**
```bash
# Changer le port dans rest_api.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### **3. Erreur de base de données**
```bash
# Supprimer et recréer la base
rm data/ai_platform.db
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

### **Logs et Debug**
```python
# Activer les logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)

# Vérifier la santé de l'API
curl http://localhost:8000/health
```

---

##  **Support**

Pour toute question ou problème :
1. **Vérifier les logs** de l'API et de l'application
2. **Consulter la documentation** automatique de l'API
3. **Tester les endpoints** avec la documentation Swagger
4. **Vérifier la configuration** des modules

---

##  **Auteur**
- SOME NIBENAON
- Linlkedin : www.linkedin.com/in/nibènaon-some-296175274 
- website : https://lped.info/Influences/?SomeNibenaon/ 
- Email : nibenaons@gmail.com
- TEL : +22661275837
