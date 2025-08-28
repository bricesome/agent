# 🔐 Gestionnaire d'Authentification Professionnel
import streamlit as st
import bcrypt
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthManager:
    """Gestionnaire d'authentification professionnel et sécurisé"""
    
    def __init__(self):
        self.users_file = "data/users.json"
        self.sessions_file = "data/sessions.json"
        self._ensure_data_directory()
        self._load_users()
        self._load_sessions()
    
    def _ensure_data_directory(self):
        """Crée le répertoire de données s'il n'existe pas"""
        os.makedirs("data", exist_ok=True)
    
    def _load_users(self):
        """Charge les utilisateurs depuis le fichier JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                # Créer un utilisateur admin par défaut
                self.users = {
                    "admin": {
                        "username": "Triolo",
                        "password_hash": self._hash_password("admin123"),
                        "email": "admin@example.com",
                        "role": "First2001@",
                        "created_at": datetime.now().isoformat(),
                        "last_login": None
                    }
                }
                self._save_users()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des utilisateurs: {e}")
            self.users = {}
    
    def _save_users(self):
        """Sauvegarde les utilisateurs dans le fichier JSON"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des utilisateurs: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash un mot de passe avec bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Vérifie un mot de passe"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def register_user(self, username: str, password: str, email: str, role: str = "user") -> bool:
        """Enregistre un nouvel utilisateur"""
        if username in self.users:
            return False
        
        self.users[username] = {
            "username": username,
            "password_hash": self._hash_password(password),
            "email": email,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        self._save_users()
        logger.info(f"Nouvel utilisateur enregistré: {username}")
        return True
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authentifie un utilisateur"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        if self.verify_password(password, user["password_hash"]):
            # Mettre à jour la dernière connexion
            user["last_login"] = datetime.now().isoformat()
            self._save_users()
            
            # Créer une session
            session_id = self._create_session(username)
            return {
                "username": username,
                "role": user["role"],
                "session_id": session_id,
                "user_data": user
            }
        return None
    
    def _create_session(self, username: str) -> str:
        """Crée une nouvelle session utilisateur"""
        session_id = f"session_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_data = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        if not hasattr(self, 'sessions'):
            self.sessions = {}
        
        self.sessions[session_id] = session_data
        self._save_sessions()
        return session_id
    
    def _load_sessions(self):
        """Charge les sessions depuis le fichier JSON"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            else:
                self.sessions = {}
        except Exception as e:
            logger.error(f"Erreur lors du chargement des sessions: {e}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Sauvegarde les sessions dans le fichier JSON"""
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des sessions: {e}")
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Valide une session utilisateur"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        expires_at = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires_at:
            # Session expirée, la supprimer
            del self.sessions[session_id]
            self._save_sessions()
            return None
        
        return session
    
    def logout_user(self, session_id: str):
        """Déconnecte un utilisateur"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self._save_sessions()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Récupère un utilisateur par son nom d'utilisateur"""
        return self.users.get(username)
    
    def update_user_profile(self, username: str, **kwargs) -> bool:
        """Met à jour le profil d'un utilisateur"""
        if username not in self.users:
            return False
        
        for key, value in kwargs.items():
            if key in ["email", "role"] and key != "password_hash":
                self.users[username][key] = value
        
        self._save_users()
        return True