# Guide Complet - Configuration des Clés API

##  **Objectif**
Configurer les vraies clés API pour que vos agents IA puissent fonctionner avec de vrais modèles d'intelligence artificielle.

##  **Prérequis**
- Compte actif sur les plateformes IA
- Clés API valides
- Crédits suffisants sur votre compte

---

##  **Étape 1 : Obtenir vos Clés API**

### **OpenAI (GPT-4, GPT-3.5-turbo)**
1. **Aller sur** : https://platform.openai.com/
2. **Se connecter** avec votre compte
3. **Cliquer sur** "API Keys" dans le menu
4. **Créer une nouvelle clé** : "Create new secret key"
5. **Copier la clé** (commence par `sk-...`)
6. ** Important** : Gardez cette clé secrète !

### **Anthropic (Claude-3)**
1. **Aller sur** : https://console.anthropic.com/
2. **Se connecter** avec votre compte
3. **Cliquer sur** "Get API Key"
4. **Créer une nouvelle clé** : "Create Key"
5. **Copier la clé** (commence par `sk-ant-...`)
6. **Important** : Gardez cette clé secrète !

### **Google (Gemini Pro)**
1. **Aller sur** : https://makersuite.google.com/app/apikey
2. **Se connecter** avec votre compte Google
3. **Cliquer sur** "Create API Key"
4. **Copier la clé** (longue chaîne de caractères)
5. ** Important** : Gardez cette clé secrète !

### **Meta (Llama 2) - Optionnel**
1. **Aller sur** : https://huggingface.co/
2. **Se connecter** avec votre compte
3. **Aller dans** "Settings" → "Access Tokens"
4. **Créer un nouveau token** : "New token"
5. **Copier le token** (commence par `hf_...`)
6. ** Important** : Gardez ce token secrète !

---

## 🔧 **Étape 2 : Configurer vos Clés**

### **Option A : Fichier config.env (Recommandé)**

1. **On ouvre le fichier** `config.env` dans votre projet
2. **Remplace les valeurs** par vos vraies clés :

```env
#  Configuration des Clés API pour les Agents IA

# OpenAI (GPT-4)
OPENAI_API_KEY=sk-votre_vraie_cle_openai_ici

# Anthropic (Claude-3)
ANTHROPIC_API_KEY=sk-ant-votre_vraie_cle_anthropic_ici

# Google (Gemini Pro)
GOOGLE_API_KEY=votre_vraie_cle_google_ici

# Meta (Llama 2) - Optionnel
META_API_KEY=hf_votre_vraie_cle_huggingface_ici

# Configuration de l'Application
DEFAULT_MODEL=GPT-4
MAX_TOKENS=4000
TEMPERATURE=0.7
```

3. **Sauvegarder** le fichier
4. **Redémarrer** l'application

### **Option B : Interface de l'Application**

1. **On lance l'application** : `streamlit run app_fixed.py`
2. **Aller dans** " Modèles"
3. **Cliquer sur** " Ajouter un Nouveau Modèle"
4. **Remplir le formulaire** :
   - **Nom** : GPT-4
   - **Fournisseur** : OpenAI
   - **Clé API** : `sk-votre_cle_ici`
   - **Statut** : active
5. **Cliquer** " Ajouter le Modèle"
6. **Répéter** pour chaque fournisseur

---

##  **Étape 3 : Tester vos Clés**

### **Test Automatique**
1. **Redémarrer l'application** après avoir configuré les clés
2. **Aller dans** " Modèles"
3. **Vérifier** que vos modèles sont marqués comme "active"
4. **Cliquer** sur " Tester" pour chaque modèle

### **Test Manuel**
1. **Créer un agent** dans " Agents"
2. **Sélectionner** un modèle avec clé API valide
3. **Cliquer** " Exécuter"
4. **Vérifier** que la réponse vient du vrai modèle

---

##  **Sécurité et Bonnes Pratiques**

### ** Ne JAMAIS partager vos clés API**
- Ne les commitez pas dans Git
- Ne les partagez pas dans des messages
- Ne les affichez pas publiquement

### ** Bonnes pratiques**
- Utilisez des variables d'environnement
- Limitez les permissions de vos clés
- Surveillez votre usage et vos coûts
- Désactivez les clés non utilisées

### ** Fichier .gitignore**
Ajoutez dans votre `.gitignore` :
```gitignore
# Clés API
config.env
.env
*.key
api_keys.txt
```

---

##  **Dépannage**

### **Erreur : "Module non installé"**
```bash
pip install openai anthropic google-generativeai python-dotenv
```

### **Erreur : "Clé API invalide"**
- Vérifiez que la clé est correctement copiée
- Vérifiez que la clé est active
- Vérifiez que vous avez des crédits

### **Erreur : "Limite de taux dépassée"**
- Attendez quelques minutes
- Vérifiez vos limites d'API
- Considérez un plan payant

### **Erreur : "Modèle non disponible"**
- Vérifiez que le modèle est activé
- Vérifiez que votre compte a accès au modèle
- Vérifiez la configuration du fournisseur

---

##  **Vérification du Fonctionnement**

### **Indicateurs de Succès**
-  Modèles marqués comme "active" dans l'interface
-  Tests de connexion réussis
-  Agents qui répondent avec de vraies réponses IA
-  Pas d'erreurs "Module non installé"

### **Indicateurs de Problème**
-  Modèles marqués comme "inactive"
-  Erreurs de connexion lors des tests
-  Messages d'erreur dans la console
-  Agents qui ne répondent pas

---

## **Étapes suivant**

1. **Configurer vos clés API**
2. ** Tester la connexion**
3. ** Créer vos premiers agents**
4. ** Utiliser vos agents avec de vrais modèles IA**
5. ** Surveiller l'usage et les coûts**

---

##  **Support**

### **En cas de problème**
1. **Vérifiez** ce guide étape par étape
2. **Consultez** la documentation des fournisseurs
3. **Vérifiez** vos comptes et crédits
4. **Testez** avec des clés d'exemple

### **Liens utiles**
- **OpenAI** : https://platform.openai.com/docs
- **Anthropic** : https://docs.anthropic.com/
- **Google** : https://ai.google.dev/docs
- **Hugging Face** : https://huggingface.co/docs

---

## Auteur :*
- SOME NIBENAON
- Linlkedin : www.linkedin.com/in/nibènaon-some-296175274 
- website : https://lped.info/Influences/?SomeNibenaon/ 
- Email : nibenaons@gmail.com
- TEL : +22661275837

