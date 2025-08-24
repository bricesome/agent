# 🌐 API REST Professionnelle avec FastAPI
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import json
import logging
from datetime import datetime

# Import des modules locaux
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'API
app = FastAPI(
    title="🤖 Plateforme Agents IA API",
    description="API REST professionnelle pour la gestion des agents IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des gestionnaires
db_manager = DatabaseManager()
auth_manager = AuthManager()
security = HTTPBearer()

# Modèles Pydantic
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=6)
    role: str = Field(default="user")

class UserLogin(BaseModel):
    username: str
    password: str

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    model_type: str
    api_key: Optional[str] = None
    configuration: Optional[str] = None

class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    steps: str

class ExecutionRequest(BaseModel):
    agent_id: int
    input_data: str
    workflow_id: Optional[int] = None

# Dépendances
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Valide le token d'authentification et retourne l'utilisateur"""
    try:
        session_id = credentials.credentials
        session = auth_manager.validate_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session invalide ou expirée"
            )
        return session
    except Exception as e:
        logger.error(f"Erreur d'authentification: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide"
        )

# Routes d'authentification
@app.post("/auth/register", response_model=Dict[str, Any])
async def register_user(user_data: UserCreate):
    """Enregistre un nouvel utilisateur"""
    try:
        success = auth_manager.register_user(
            user_data.username,
            user_data.password,
            user_data.email,
            user_data.role
        )
        
        if success:
            return {
                "success": True,
                "message": "Utilisateur enregistré avec succès",
                "username": user_data.username
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nom d'utilisateur déjà existant"
            )
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@app.post("/auth/login", response_model=Dict[str, Any])
async def login_user(user_data: UserLogin):
    """Authentifie un utilisateur"""
    try:
        user = auth_manager.authenticate_user(user_data.username, user_data.password)
        
        if user:
            # Mettre à jour la base de données
            user_id = db_manager.get_user_id(user_data.username)
            if user_id:
                db_manager.update_user_last_login(user_id)
            
            return {
                "success": True,
                "message": "Connexion réussie",
                "session_id": user["session_id"],
                "user": {
                    "username": user["username"],
                    "role": user["role"]
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nom d'utilisateur ou mot de passe incorrect"
            )
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@app.post("/auth/logout")
async def logout_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Déconnecte un utilisateur"""
    try:
        session_id = current_user.get("session_id")
        if session_id:
            auth_manager.logout_user(session_id)
        
        return {
            "success": True,
            "message": "Déconnexion réussie"
        }
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

# Routes des agents
@app.get("/agents", response_model=List[Dict[str, Any]])
async def get_agents(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Récupère tous les agents"""
    try:
        agents = db_manager.get_all_agents()
        return agents
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@app.post("/agents", response_model=Dict[str, Any])
async def create_agent(
    agent_data: AgentCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Crée un nouvel agent"""
    try:
        user_id = db_manager.get_user_id(current_user["username"])
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Utilisateur non trouvé"
            )
        
        agent_id = db_manager.insert_agent(
            agent_data.name,
            agent_data.description or "",
            agent_data.model_type,
            agent_data.api_key or "",
            agent_data.configuration or "{}",
            user_id
        )
        
        if agent_id:
            return {
                "success": True,
                "message": "Agent créé avec succès",
                "agent_id": agent_id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la création de l'agent"
            )
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

# Routes des exécutions
@app.post("/execute", response_model=Dict[str, Any])
async def execute_agent(
    execution_data: ExecutionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Exécute un agent"""
    try:
        user_id = db_manager.get_user_id(current_user["username"])
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Utilisateur non trouvé"
            )
        
        # Créer l'exécution
        execution_id = db_manager.insert_execution(
            execution_data.agent_id,
            execution_data.input_data,
            "",  # output_data sera mis à jour après exécution
            "running",
            user_id,
            execution_data.workflow_id
        )
        
        if execution_id:
            # Ici, tu peux ajouter la logique d'exécution réelle de l'agent
            # Pour l'instant, on simule un résultat
            simulated_output = f"Résultat simulé pour l'agent {execution_data.agent_id}"
            
            # Mettre à jour le statut
            db_manager.update_execution_status(execution_id, "completed", simulated_output)
            
            return {
                "success": True,
                "message": "Exécution terminée avec succès",
                "execution_id": execution_id,
                "output": simulated_output
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la création de l'exécution"
            )
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

# Route de santé
@app.get("/health")
async def health_check():
    """Vérification de la santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Point d'entrée principal
if __name__ == "__main__":
    uvicorn.run(
        "rest_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
