# Modèle utilisateur avec authentification sécurisée
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from config.database import Base

class User(Base):
    """Modèle utilisateur avec authentification JWT"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relations
    agents = relationship("Agent", back_populates="owner")
    workflows = relationship("Workflow", back_populates="owner")
    executions = relationship("Execution", back_populates="user")
    
    def set_password(self, password):
        """Hash le mot de passe de manière sécurisée"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self, expires_in=3600):
        """Génère un token JWT sécurisé"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY', 'your-secret-key'), algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Vérifie et décode un token JWT"""
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire (sans mot de passe)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
