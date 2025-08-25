# 🤖 Agent Planificateur de Tâches
# Agent spécialisé dans la planification et l'exécution automatique de tâches

import json
import os
from datetime import datetime, timedelta
import schedule
import time
import threading
from typing import Dict, List, Any, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlannerAgent:
    """Agent planificateur de tâches avancé"""
    
    def __init__(self):
        self.agent_id = "planner_agent_system"
        self.name = "�� Planificateur de Tâches"
        self.description = "Agent spécialisé dans la planification et l'exécution automatique de tâches"
        self.version = "1.0.0"
        self.tasks_file = "data/planned_tasks.json"
        self.scheduler_running = False
        
        # Créer le répertoire de données s'il n'existe pas
        os.makedirs("data", exist_ok=True)
        
        # Charger les tâches existantes
        self.planned_tasks = self._load_tasks()
        
        # Démarrer le planificateur en arrière-plan
        self._start_scheduler()
    
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Charge les tâches planifiées depuis le fichier JSON"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Erreur lors du chargement des tâches: {e}")
            return []
    
    def _save_tasks(self):
        """Sauvegarde les tâches planifiées dans le fichier JSON"""
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(self.planned_tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des tâches: {e}")
    
    def _start_scheduler(self):
        """Démarre le planificateur en arrière-plan"""
        if not self.scheduler_running:
            self.scheduler_running = True
            scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            scheduler_thread.start()
            logger.info("🔄 Planificateur de tâches démarré")
    
    def _run_scheduler(self):
        """Exécute le planificateur en continu"""
        while self.scheduler_running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Erreur dans le planificateur: {e}")
                time.sleep(5)
    
    def plan_task(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """Planifie une nouvelle tâche"""
        try:
            # Générer un ID unique pour la tâche
            task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.planned_tasks)}"
            
            # Créer la tâche
            task = {
                "id": task_id,
                "name": task_config.get("name", "Tâche sans nom"),
                "description": task_config.get("description", ""),
                "type": task_config.get("type", "agent_execution"),
                "schedule_type": task_config.get("schedule_type", "datetime"),
                "schedule_config": task_config.get("schedule_config", {}),
                "target": task_config.get("target", {}),
                "status": "planned",
                "created_at": datetime.now().isoformat(),
                "next_execution": None,
                "last_execution": None,
                "execution_count": 0,
                "max_executions": task_config.get("max_executions", -1),  # -1 = illimité
                "enabled": True
            }
            
            # Configurer la planification selon le type
            if task["schedule_type"] == "datetime":
                self._schedule_datetime_task(task)
            elif task["schedule_type"] == "recurring":
                self._schedule_recurring_task(task)
            elif task["schedule_type"] == "conditional":
                self._schedule_conditional_task(task)
            elif task["schedule_type"] == "seasonal":
                self._schedule_seasonal_task(task)
            
            # Ajouter la tâche à la liste
            self.planned_tasks.append(task)
            self._save_tasks()
            
            logger.info(f"✅ Tâche '{task['name']}' planifiée avec succès (ID: {task_id})")
            
            return {
                "success": True,
                "task_id": task_id,
                "message": f"Tâche '{task['name']}' planifiée avec succès",
                "next_execution": task["next_execution"]
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la planification de la tâche: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _schedule_datetime_task(self, task: Dict[str, Any]):
        """Planifie une tâche à une date/heure précise"""
        schedule_config = task["schedule_config"]
        target_datetime = datetime.fromisoformat(schedule_config["datetime"])
        
        # Planifier la tâche
        schedule.every().day.at(target_datetime.strftime("%H:%M")).do(
            self._execute_task, task["id"]
        ).tag(task["id"])
        
        task["next_execution"] = target_datetime.isoformat()
    
    def _schedule_recurring_task(self, task: Dict[str, Any]):
        """Planifie une tâche récurrente"""
        schedule_config = task["schedule_config"]
        frequency = schedule_config.get("frequency", "daily")
        
        if frequency == "daily":
            time_str = schedule_config.get("time", "09:00")
            schedule.every().day.at(time_str).do(
                self._execute_task, task["id"]
            ).tag(task["id"])
        
        elif frequency == "weekly":
            day = schedule_config.get("day", "monday")
            time_str = schedule_config.get("time", "09:00")
            getattr(schedule.every(), day).at(time_str).do(
                self._execute_task, task["id"]
            ).tag(task["id"])
        
        elif frequency == "monthly":
            day = schedule_config.get("day", 1)
            time_str = schedule_config.get("time", "09:00")
            schedule.every().month.at(time_str).do(
                self._execute_task, task["id"]
            ).tag(task["id"])
        
        elif frequency == "weekend":
            time_str = schedule_config.get("time", "10:00")
            schedule.every().saturday.at(time_str).do(
                self._execute_task, task["id"]
            ).tag(task["id"])
            schedule.every().sunday.at(time_str).do(
                self._execute_task, task["id"]
            ).tag(task["id"])
        
        # Calculer la prochaine exécution
        task["next_execution"] = self._calculate_next_execution(task)
    
    def _schedule_conditional_task(self, task: Dict[str, Any]):
        """Planifie une tâche conditionnelle (événement)"""
        # Pour les tâches conditionnelles, on vérifie périodiquement
        schedule.every(5).minutes.do(
            self._check_conditional_task, task["id"]
        ).tag(task["id"])
        
        task["next_execution"] = "Conditionnel"
    
    def _schedule_seasonal_task(self, task: Dict[str, Any]):
        """Planifie une tâche saisonnière"""
        schedule_config = task["schedule_config"]
        season = schedule_config.get("season", "spring")
        time_str = schedule_config.get("time", "09:00")
        
        # Définir les dates de début de saison
        season_dates = {
            "spring": "03-21",
            "summer": "06-21", 
            "autumn": "09-21",
            "winter": "12-21"
        }
        
        if season in season_dates:
            schedule.every().year.at(season_dates[season]).at(time_str).do(
                self._execute_task, task["id"]
            ).tag(task["id"])
            
            task["next_execution"] = f"{datetime.now().year}-{season_dates[season]} {time_str}"
    
    def _calculate_next_execution(self, task: Dict[str, Any]) -> str:
        """Calcule la prochaine exécution d'une tâche"""
        try:
            schedule_config = task["schedule_config"]
            frequency = schedule_config.get("frequency", "daily")
            time_str = schedule_config.get("time", "09:00")
            
            now = datetime.now()
            target_time = datetime.strptime(time_str, "%H:%M").time()
            
            if frequency == "daily":
                next_exec = datetime.combine(now.date(), target_time)
                if next_exec <= now:
                    next_exec += timedelta(days=1)
            
            elif frequency == "weekly":
                day = schedule_config.get("day", "monday")
                days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                current_day = now.strftime("%A").lower()
                target_day_idx = days.index(day)
                current_day_idx = days.index(current_day)
                
                days_ahead = (target_day_idx - current_day_idx) % 7
                if days_ahead == 0 and now.time() > target_time:
                    days_ahead = 7
                
                next_exec = datetime.combine(now.date(), target_time) + timedelta(days=days_ahead)
            
            elif frequency == "weekend":
                # Prochain samedi
                days_until_saturday = (5 - now.weekday()) % 7
                if days_until_saturday == 0 and now.time() > target_time:
                    days_until_saturday = 7
                
                next_exec = datetime.combine(now.date(), target_time) + timedelta(days=days_until_saturday)
            
            else:
                next_exec = datetime.combine(now.date(), target_time)
            
            return next_exec.isoformat()
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la prochaine exécution: {e}")
            return "Erreur de calcul"
    
    def _check_conditional_task(self, task_id: str):
        """Vérifie si une tâche conditionnelle doit être exécutée"""
        task = next((t for t in self.planned_tasks if t["id"] == task_id), None)
        if not task:
            return
        
        schedule_config = task["schedule_config"]
        condition = schedule_config.get("condition", {})
        
        # Vérifier la condition (exemple: arrivée d'un email)
        if self._check_condition(condition):
            self._execute_task(task_id)
    
    def _check_condition(self, condition: Dict[str, Any]) -> bool:
        """Vérifie si une condition est remplie"""
        condition_type = condition.get("type", "email")
        
        if condition_type == "email":
            # Vérifier l'arrivée d'un email spécifique
            email_subject = condition.get("email_subject", "")
            email_sender = condition.get("email_sender", "")
            
            # Ici tu peux implémenter la logique de vérification d'email
            # Pour l'instant, on simule
            return False
        
        elif condition_type == "file":
            # Vérifier l'existence d'un fichier
            file_path = condition.get("file_path", "")
            return os.path.exists(file_path)
        
        elif condition_type == "time":
            # Vérifier une condition temporelle
            time_condition = condition.get("time_condition", {})
            current_time = datetime.now().time()
            
            if "after" in time_condition:
                after_time = datetime.strptime(time_condition["after"], "%H:%M").time()
                if current_time < after_time:
                    return False
            
            if "before" in time_condition:
                before_time = datetime.strptime(time_condition["before"], "%H:%M").time()
                if current_time > before_time:
                    return False
            
            return True
        
        return False
    
    def _execute_task(self, task_id: str):
        """Exécute une tâche planifiée"""
        task = next((t for t in self.planned_tasks if t["id"] == task_id), None)
        if not task or not task.get("enabled", True):
            return
        
        try:
            logger.info(f"�� Exécution de la tâche '{task['name']}' (ID: {task_id})")
            
            # Mettre à jour le statut
            task["status"] = "executing"
            task["last_execution"] = datetime.now().isoformat()
            task["execution_count"] += 1
            
            # Exécuter la tâche selon son type
            if task["type"] == "agent_execution":
                self._execute_agent_task(task)
            elif task["type"] == "workflow_execution":
                self._execute_workflow_task(task)
            elif task["type"] == "email_send":
                self._execute_email_task(task)
            elif task["type"] == "file_operation":
                self._execute_file_task(task)
            elif task["type"] == "custom_action":
                self._execute_custom_task(task)
            
            # Mettre à jour le statut
            task["status"] = "completed"
            
            # Vérifier si la tâche doit être répétée
            if task["max_executions"] > 0 and task["execution_count"] >= task["max_executions"]:
                task["enabled"] = False
                logger.info(f"✅ Tâche '{task['name']}' terminée (limite atteinte)")
            else:
                # Replanifier si nécessaire
                if task["schedule_type"] in ["recurring", "seasonal"]:
                    task["next_execution"] = self._calculate_next_execution(task)
                    logger.info(f"✅ Tâche '{task['name']}' replanifiée")
                else:
                    task["enabled"] = False
                    logger.info(f"✅ Tâche '{task['name']}' terminée (exécution unique)")
            
            self._save_tasks()
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'exécution de la tâche '{task['name']}': {e}")
            task["status"] = "error"
            task["last_error"] = str(e)
            self._save_tasks()
    
    def _execute_agent_task(self, task: Dict[str, Any]):
        """Exécute une tâche d'agent"""
        target = task["target"]
        agent_name = target.get("agent_name", "")
        
        logger.info(f"🤖 Exécution de l'agent '{agent_name}'")
        
        # Ici tu peux implémenter l'exécution réelle de l'agent
        # Pour l'instant, on simule
        time.sleep(2)
        
        logger.info(f"✅ Agent '{agent_name}' exécuté avec succès")
    
    def _execute_workflow_task(self, task: Dict[str, Any]):
        """Exécute une tâche de workflow"""
        target = task["target"]
        workflow_name = target.get("workflow_name", "")
        
        logger.info(f"🔄 Exécution du workflow '{workflow_name}'")
        
        # Ici tu peux implémenter l'exécution réelle du workflow
        # Pour l'instant, on simule
        time.sleep(3)
        
        logger.info(f"✅ Workflow '{workflow_name}' exécuté avec succès")
    
    def _execute_email_task(self, task: Dict[str, Any]):
        """Exécute une tâche d'envoi d'email"""
        target = task["target"]
        recipients = target.get("recipients", [])
        subject = target.get("subject", "")
        
        logger.info(f"📧 Envoi d'email à {len(recipients)} destinataires")
        
        # Ici tu peux implémenter l'envoi réel d'email
        # Pour l'instant, on simule
        time.sleep(1)
        
        logger.info(f"✅ Email envoyé avec succès")
    
    def _execute_file_task(self, task: Dict[str, Any]):
        """Exécute une tâche de manipulation de fichier"""
        target = task["target"]
        operation = target.get("operation", "")
        file_path = target.get("file_path", "")
        
        logger.info(f"📁 Opération '{operation}' sur le fichier '{file_path}'")
        
        # Ici tu peux implémenter les opérations sur fichiers
        # Pour l'instant, on simule
        time.sleep(1)
        
        logger.info(f"✅ Opération fichier terminée avec succès")
    
    def _execute_custom_task(self, task: Dict[str, Any]):
        """Exécute une tâche personnalisée"""
        target = task["target"]
        action = target.get("action", "")
        
        logger.info(f"⚙️ Exécution de l'action personnalisée: {action}")
        
        # Ici tu peux implémenter des actions personnalisées
        # Pour l'instant, on simule
        time.sleep(1)
        
        logger.info(f"✅ Action personnalisée exécutée avec succès")
    
    def get_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère la liste des tâches planifiées"""
        if status:
            return [task for task in self.planned_tasks if task.get("status") == status]
        return self.planned_tasks
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une tâche spécifique"""
        return next((task for task in self.planned_tasks if task["id"] == task_id), None)
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """Met à jour une tâche planifiée"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            # Mettre à jour les champs
            for key, value in updates.items():
                if key in ["name", "description", "enabled", "max_executions"]:
                    task[key] = value
            
            # Si la planification change, replanifier
            if "schedule_config" in updates:
                task["schedule_config"] = updates["schedule_config"]
                
                # Supprimer l'ancienne planification
                schedule.clear(task_id)
                
                # Replanifier
                if task["schedule_type"] == "datetime":
                    self._schedule_datetime_task(task)
                elif task["schedule_type"] == "recurring":
                    self._schedule_recurring_task(task)
                elif task["schedule_type"] == "seasonal":
                    self._schedule_seasonal_task(task)
            
            self._save_tasks()
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la tâche: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """Supprime une tâche planifiée"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            # Supprimer la planification
            schedule.clear(task_id)
            
            # Supprimer de la liste
            self.planned_tasks = [t for t in self.planned_tasks if t["id"] != task_id]
            self._save_tasks()
            
            logger.info(f"✅ Tâche '{task['name']}' supprimée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la tâche: {e}")
            return False
    
    def enable_task(self, task_id: str) -> bool:
        """Active une tâche désactivée"""
        return self.update_task(task_id, {"enabled": True})
    
    def disable_task(self, task_id: str) -> bool:
        """Désactive une tâche"""
        return self.update_task(task_id, {"enabled": False})
    
    def get_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques du planificateur"""
        total_tasks = len(self.planned_tasks)
        enabled_tasks = len([t for t in self.planned_tasks if t.get("enabled", True)])
        completed_tasks = len([t for t in self.planned_tasks if t.get("status") == "completed"])
        error_tasks = len([t for t in self.planned_tasks if t.get("status") == "error"])
        
        return {
            "total_tasks": total_tasks,
            "enabled_tasks": enabled_tasks,
            "completed_tasks": completed_tasks,
            "error_tasks": error_tasks,
            "scheduler_running": self.scheduler_running
        }
    
    def stop_scheduler(self):
        """Arrête le planificateur"""
        self.scheduler_running = False
        schedule.clear()
        logger.info("🛑 Planificateur de tâches arrêté")

# Instance globale de l'agent planificateur
planner_agent = PlannerAgent()
