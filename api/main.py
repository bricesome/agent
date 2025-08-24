# API REST professionnelle avec FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from auth.authentication import auth_manager
from models.user import User
from models.agent import Agent
from config.database import db_config
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation FastAPI
app = FastAPI(
    title="AI Agents Platform API",
    description="API REST professionnelle pour la plateforme d'agents IA",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sécurité
security = HTTPBearer()

# Modèles Pydantic
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class AgentCreate(BaseModel):
    name: str
    domain: str
    agent_type: str
    model: str
    system_prompt: str

class AgentResponse(BaseModel):
    id: int
    name: str
    domain: str
    type: str
    model: str
    status: str
    created_at: str

# Dépendances
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Vérifie le token et retourne l'utilisateur"""
    try:
        payload = User.verify_token(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide ou expiré"
            )
        
        with db_config.get_session() as session:
            user = session.query(User).filter(User.id == payload['user_id']).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Utilisateur non trouvé"
                )
            return user
    except Exception as e:
        logger.error(f"❌ Erreur d'authentification: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erreur d'authentification"
        )

# Routes d'authentification
@app.post("/auth/register", response_model=dict)
async def register_user(user_data: UserCreate):
    """Enregistre un nouvel utilisateur"""
    try:
        with db_config.get_session() as session:
            # Vérifier si l'utilisateur existe déjà
            existing_user = session.query(User).filter(
                (User.username == user_data.username) | (User.email == user_data.email)
            ).first()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nom d'utilisateur ou email déjà utilisé"
                )
            
            # Créer le nouvel utilisateur
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name
            )
            new_user.set_password(user_data.password)
            
            session.add(new_user)
            session.commit()
            
            logger.info(f"✅ Nouvel utilisateur enregistré: {user_data.username}")
            return {"message": "Utilisateur créé avec succès", "user_id": new_user.id}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'enregistrement: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@app.post("/auth/login", response_model=dict)
async def login_user(user_data: UserLogin):
    """Authentifie un utilisateur"""
    try:
        with db_config.get_session() as session:
            user = session.query(User).filter(User.username == user_data.username).first()
            
            if user and user.check_password(user_data.password):
                token = user.generate_token()
                return {
                    "access_token": token,
                    "token_type": "bearer",
                    "user": user.to_dict()
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Nom d'utilisateur ou mot de passe incorrect"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la connexion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

# Routes des agents
@app.get("/agents", response_model=List[AgentResponse])
async def get_agents(current_user: User = Depends(get_current_user)):
    """Récupère tous les agents de l'utilisateur"""
    try:
        with db_config.get_session() as session:
            agents = session.query(Agent).filter(Agent.owner_id == current_user.id).all()
            return [AgentResponse(**agent.to_dict()) for agent in agents]
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@app.post("/agents", response_model=dict)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user)
):
    """Crée un nouvel agent"""
    try:
        with db_config.get_session() as session:
            new_agent = Agent(
                name=agent_data.name,
                domain=agent_data.domain,
                agent_type=agent_data.agent_type,
                model=agent_data.model,
                system_prompt=agent_data.system_prompt,
                owner_id=current_user.id
            )
            
            session.add(new_agent)
            session.commit()
            
            logger.info(f"✅ Nouvel agent créé: {agent_data.name} par {current_user.username}")
            return {"message": "Agent créé avec succès", "agent_id": new_agent.id}
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création de l'agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

# Route de santé
@app.get("/health")
async def health_check():
    """Vérification de la santé de l'API"""
    return {"status": "healthy", "timestamp": datetime.datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
