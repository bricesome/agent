# Configuration de base de données professionnelle
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging

# Configuration du logging professionnel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Configuration centralisée de la base de données"""
    
    def __init__(self):
        self.db_type = os.getenv('DB_TYPE', 'sqlite')  # sqlite, postgresql, mysql
        self.db_url = self._get_database_url()
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _get_database_url(self):
        """Récupère l'URL de base de données selon l'environnement"""
        if self.db_type == 'postgresql':
            return f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'ai_agents')}"
        elif self.db_type == 'mysql':
            return f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'ai_agents')}"
        else:
            # SQLite par défaut pour le développement
            return "sqlite:///./ai_agents.db"
    
    def _initialize_engine(self):
        """Initialise le moteur de base de données avec configuration optimisée"""
        try:
            if self.db_type == 'sqlite':
                self.engine = create_engine(
                    self.db_url,
                    connect_args={"check_same_thread": False},
                    pool_pre_ping=True,
                    echo=False
                )
            else:
                self.engine = create_engine(
                    self.db_url,
                    pool_size=20,
                    max_overflow=30,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    echo=False
                )
            
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info(f"✅ Base de données {self.db_type} initialisée avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur d'initialisation de la base de données: {e}")
            # Fallback vers SQLite
            self.db_type = 'sqlite'
            self.db_url = "sqlite:///./ai_agents.db"
            self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.warning("⚠️ Fallback vers SQLite activé")
    
    @contextmanager
    def get_session(self):
        """Contexte manager pour les sessions de base de données"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erreur de session: {e}")
            raise
        finally:
            session.close()

# Instance globale
db_config = DatabaseConfig()
Base = declarative_base()
