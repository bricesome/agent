# Système d'authentification professionnel avec JWT
import streamlit as st
from functools import wraps
import jwt
import datetime
import os
from models.user import User
from config.database import db_config
import logging

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Gestionnaire d'authentification centralisé"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
        self.algorithm = 'HS256'
        self.token_expiry = 3600  # 1 heure
    
    def login_user(self, username: str, password: str):
        """Authentifie un utilisateur et génère un token"""
        try:
            with db_config.get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                
                if user and user.check_password(password):
                    # Mettre à jour la dernière connexion
                    user.last_login = datetime.datetime.utcnow()
                    session.commit()
                    
                    # Générer le token
                    token = user.generate_token(self.token_expiry)
                    
                    # Stocker en session Streamlit
                    st.session_state['user_token'] = token
                    st.session_state['user_id'] = user.id
                    st.session_state['username'] = user.username
                    st.session_state['is_admin'] = user.is_admin
                    
                    logger.info(f"✅ Utilisateur {username} connecté avec succès")
                    return True, "Connexion réussie"
                else:
                    logger.warning(f"⚠️ Tentative de connexion échouée pour {username}")
                    return False, "Nom d'utilisateur ou mot de passe incorrect"
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de la connexion: {e}")
            return False, "Erreur interne du serveur"
    
    def logout_user(self):
        """Déconnecte l'utilisateur"""
        for key in ['user_token', 'user_id', 'username', 'is_admin']:
            if key in st.session_state:
                del st.session_state[key]
        logger.info("✅ Utilisateur déconnecté")
    
    def get_current_user(self):
        """Récupère l'utilisateur actuellement connecté"""
        token = st.session_state.get('user_token')
        if not token:
            return None
        
        try:
            payload = User.verify_token(token)
            if payload:
                with db_config.get_session() as session:
                    user = session.query(User).filter(User.id == payload['user_id']).first()
                    return user
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération de l'utilisateur: {e}")
        
        return None
    
    def require_auth(self, func):
        """Décorateur pour protéger les pages"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not st.session_state.get('user_token'):
                st.error("🔒 Accès refusé. Veuillez vous connecter.")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    
    def require_admin(self, func):
        """Décorateur pour les pages admin"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not st.session_state.get('is_admin'):
                st.error("🚫 Accès refusé. Droits administrateur requis.")
                st.stop()
            return func(*args, **kwargs)
        return wrapper

# Instance globale
auth_manager = AuthenticationManager()
