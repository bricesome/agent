# 🗄️ Gestionnaire de Base de Données Professionnel
import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from contextlib import contextmanager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestionnaire de base de données SQLite professionnel et évolutif"""
    
    def __init__(self, db_path: str = "data/ai_platform.db"):
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self):
        """Crée le répertoire de données s'il n'existe pas"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Table des utilisateurs
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """)
                
                # Table des agents
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        model_type TEXT NOT NULL,
                        api_key TEXT,
                        configuration TEXT,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1,
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                """)
                
                # Table des workflows
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS workflows (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        steps TEXT NOT NULL,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1,
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                """)
                
                # Table des exécutions
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS executions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        agent_id INTEGER,
                        workflow_id INTEGER,
                        input_data TEXT,
                        output_data TEXT,
                        status TEXT NOT NULL,
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP,
                        execution_time REAL,
                        created_by INTEGER,
                        FOREIGN KEY (agent_id) REFERENCES agents (id),
                        FOREIGN KEY (workflow_id) REFERENCES workflows (id),
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                """)
                
                # Table des sessions
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        user_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                conn.commit()
                logger.info("Base de données initialisée avec succès")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
    
    @contextmanager
    def _get_connection(self):
        """Contexte pour gérer les connexions à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Exécute une requête SELECT et retourne les résultats"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """Exécute une requête UPDATE/INSERT/DELETE"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la mise à jour: {e}")
            return False
    
    def insert_user(self, username: str, email: str, password_hash: str, role: str = "user") -> Optional[int]:
        """Insère un nouvel utilisateur"""
        query = """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """
        if self.execute_update(query, (username, email, password_hash, role)):
            return self.get_user_id(username)
        return None
    
    def get_user_id(self, username: str) -> Optional[int]:
        """Récupère l'ID d'un utilisateur par son nom d'utilisateur"""
        query = "SELECT id FROM users WHERE username = ?"
        results = self.execute_query(query, (username,))
        return results[0]["id"] if results else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Récupère un utilisateur par son nom d'utilisateur"""
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        results = self.execute_query(query, (username,))
        return results[0] if results else None
    
    def update_user_last_login(self, user_id: int):
        """Met à jour la dernière connexion d'un utilisateur"""
        query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?"
        self.execute_update(query, (user_id,))
    
    def insert_agent(self, name: str, description: str, model_type: str, 
                     api_key: str, configuration: str, created_by: int) -> Optional[int]:
        """Insère un nouvel agent"""
        query = """
            INSERT INTO agents (name, description, model_type, api_key, configuration, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        if self.execute_update(query, (name, description, model_type, api_key, configuration, created_by)):
            return self.get_agent_id(name)
        return None
    
    def get_agent_id(self, name: str) -> Optional[int]:
        """Récupère l'ID d'un agent par son nom"""
        query = "SELECT id FROM agents WHERE name = ?"
        results = self.execute_query(query, (name,))
        return results[0]["id"] if results else None
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Récupère tous les agents actifs"""
        query = "SELECT * FROM agents WHERE is_active = 1 ORDER BY created_at DESC"
        return self.execute_query(query)
    
    def insert_execution(self, agent_id: int, input_data: str, output_data: str, 
                        status: str, created_by: int, workflow_id: int = None) -> Optional[int]:
        """Insère une nouvelle exécution"""
        query = """
            INSERT INTO executions (agent_id, workflow_id, input_data, output_data, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        if self.execute_update(query, (agent_id, workflow_id, input_data, output_data, status, created_by)):
            return self.get_last_execution_id()
        return None
    
    def get_last_execution_id(self) -> Optional[int]:
        """Récupère l'ID de la dernière exécution"""
        query = "SELECT id FROM executions ORDER BY id DESC LIMIT 1"
        results = self.execute_query(query)
        return results[0]["id"] if results else None
    
    def update_execution_status(self, execution_id: int, status: str, output_data: str = None):
        """Met à jour le statut d'une exécution"""
        if output_data:
            query = "UPDATE executions SET status = ?, output_data = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?"
            self.execute_update(query, (status, output_data, execution_id))
        else:
            query = "UPDATE executions SET status = ? WHERE id = ?"
            self.execute_update(query, (status, execution_id))
    
    def get_execution_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupère l'historique des exécutions d'un utilisateur"""
        query = """
            SELECT e.*, a.name as agent_name 
            FROM executions e 
            JOIN agents a ON e.agent_id = a.id 
            WHERE e.created_by = ? 
            ORDER BY e.started_at DESC 
            LIMIT ?
        """
        return self.execute_query(query, (user_id, limit))


