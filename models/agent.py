# Modèle agent avec relations optimisées
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class Agent(Base):
    """Modèle agent avec relations et métadonnées"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    domain = Column(String(100), index=True)
    agent_type = Column(String(50), index=True)
    model = Column(String(100))
    system_prompt = Column(Text)
    status = Column(String(20), default='active')
    metadata = Column(JSON)  # Stockage flexible des métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="agents")
    executions = relationship("Execution", back_populates="agent")
    
    def to_dict(self):
        """Convertit l'agent en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'type': self.agent_type,
            'model': self.model,
            'system_prompt': self.system_prompt,
            'status': self.status,
            'metadata': self.metadata or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'owner_id': self.owner_id
        }
