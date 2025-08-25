# �� Agent d'Envoi d'Emails
# Agent spécialisé dans l'envoi automatique de résultats par email

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import base64
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailAgent:
    """Agent spécialisé dans l'envoi automatique d'emails"""
    
    def __init__(self):
        self.agent_id = "email_agent_system"
        self.name = "�� Agent d'Envoi d'Emails"
        self.description = "Agent spécialisé dans l'envoi automatique de résultats par email"
        self.version = "1.0.0"
        self.config_file = "data/email_configs.json"
        self.templates_dir = "data/email_templates"
        
        # Créer les répertoires nécessaires
        os.makedirs("data", exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Charger les configurations d'email des utilisateurs
        self.email_configs = self._load_email_configs()
        
        # Créer les templates par défaut
        self._create_default_templates()
    
    def _load_email_configs(self) -> Dict[str, Any]:
        """Charge les configurations d'email des utilisateurs"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Erreur lors du chargement des configurations email: {e}")
            return {}
    
    def _save_email_configs(self):
        """Sauvegarde les configurations d'email"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.email_configs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des configurations email: {e}")
    
    def _create_default_templates(self):
        """Crée les templates d'email par défaut"""
        default_templates = {
            "agent_result": {
                "subject": "Résultat de l'Agent {agent_name}",
                "body": """
                <html>
                <body>
                    <h2>Résultat de l'Agent {agent_name}</h2>
                    <p><strong>Date d'exécution:</strong> {execution_date}</p>
                    <p><strong>Description:</strong> {description}</p>
                    <hr>
                    <h3>Résultat:</h3>
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                        {result}
                    </div>
                    <hr>
                    <p><em>Cet email a été généré automatiquement par la Plateforme Agents IA</em></p>
                </body>
                </html>
                """
            },
            "workflow_result": {
                "subject": "Résultat du Workflow {workflow_name}",
                "body": """
                <html>
                <body>
                    <h2>Résultat du Workflow {workflow_name}</h2>
                    <p><strong>Date d'exécution:</strong> {execution_date}</p>
                    <p><strong>Description:</strong> {description}</p>
                    <p><strong>Agents impliqués:</strong> {agents_involved}</p>
                    <hr>
                    <h3>Résultat:</h3>
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                        {result}
                    </div>
                    <hr>
                    <p><em>Cet email a été généré automatiquement par la Plateforme Agents IA</em></p>
                </body>
                </html>
                """
            },
            "analysis_report": {
                "subject": "Rapport d'Analyse - {report_title}",
                "body": """
                <html>
                <body>
                    <h2>Rapport d'Analyse: {report_title}</h2>
                    <p><strong>Date de génération:</strong> {generation_date}</p>
                    <p><strong>Type d'analyse:</strong> {analysis_type}</p>
                    <hr>
                    <h3>Résumé:</h3>
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                        {summary}
                    </div>
                    <hr>
                    <p><em>Ce rapport a été généré automatiquement par la Plateforme Agents IA</em></p>
                </body>
                </html>
                """
            }
        }
        
        for template_name, template_content in default_templates.items():
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            if not os.path.exists(template_file):
                with open(template_file, 'w', encoding='utf-8') as f:
                    json.dump(template_content, f, indent=2, ensure_ascii=False)
    
    def configure_user_email(self, user_id: str, email_config: Dict[str, Any]) -> Dict[str, Any]:
        """Configure les paramètres d'email pour un utilisateur"""
        try:
            # Validation des paramètres
            required_fields = ["smtp_server", "smtp_port", "email", "password", "use_tls"]
            for field in required_fields:
                if field not in email_config:
                    return {
                        "success": False,
                        "error": f"Champ requis manquant: {field}"
                    }
            
            # Test de connexion SMTP
            if not self._test_smtp_connection(email_config):
                return {
                    "success": False,
                    "error": "Impossible de se connecter au serveur SMTP. Vérifiez vos paramètres."
                }
            
            # Sauvegarder la configuration
            self.email_configs[user_id] = {
                **email_config,
                "configured_at": datetime.now().isoformat(),
                "last_test": datetime.now().isoformat(),
                "status": "active"
            }
            
            self._save_email_configs()
            
            logger.info(f"✅ Configuration email configurée pour l'utilisateur {user_id}")
            
            return {
                "success": True,
                "message": "Configuration email configurée avec succès",
                "config_id": user_id
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la configuration email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _test_smtp_connection(self, email_config: Dict[str, Any]) -> bool:
        """Teste la connexion SMTP avec les paramètres fournis"""
        try:
            smtp_server = email_config["smtp_server"]
            smtp_port = email_config["smtp_port"]
            email = email_config["email"]
            password = email_config["password"]
            use_tls = email_config.get("use_tls", True)
            
            # Connexion au serveur SMTP
            if use_tls:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
            
            # Authentification
            server.login(email, password)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur de test SMTP: {e}")
            return False
    
    def send_agent_result(self, user_id: str, agent_name: str, result: str, 
                         recipients: List[str], template_name: str = "agent_result",
                         custom_subject: str = None, custom_body: str = None) -> Dict[str, Any]:
        """Envoie le résultat d'un agent par email"""
        try:
            # Vérifier que l'utilisateur a configuré son email
            if user_id not in self.email_configs:
                return {
                    "success": False,
                    "error": "Configuration email non trouvée. Veuillez configurer vos paramètres email."
                }
            
            email_config = self.email_configs[user_id]
            
            # Charger le template
            template = self._load_template(template_name)
            if not template:
                return {
                    "success": False,
                    "error": f"Template '{template_name}' non trouvé"
                }
            
            # Préparer le contenu de l'email
            subject = custom_subject or template["subject"].format(agent_name=agent_name)
            body = custom_body or template["body"].format(
                agent_name=agent_name,
                execution_date=datetime.now().strftime("%d/%m/%Y à %H:%M"),
                description=f"Résultat de l'exécution de l'agent {agent_name}",
                result=result
            )
            
            # Envoyer l'email
            success = self._send_email(
                email_config=email_config,
                recipients=recipients,
                subject=subject,
                body=body
            )
            
            if success:
                logger.info(f"✅ Email de résultat d'agent envoyé à {len(recipients)} destinataires")
                return {
                    "success": True,
                    "message": f"Email envoyé avec succès à {len(recipients)} destinataires",
                    "recipients": recipients
                }
            else:
                return {
                    "success": False,
                    "error": "Erreur lors de l'envoi de l'email"
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du résultat d'agent: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_workflow_result(self, user_id: str, workflow_name: str, result: str,
                           agents_involved: List[str], recipients: List[str],
                           template_name: str = "workflow_result",
                           custom_subject: str = None, custom_body: str = None) -> Dict[str, Any]:
        """Envoie le résultat d'un workflow par email"""
        try:
            # Vérifier que l'utilisateur a configuré son email
            if user_id not in self.email_configs:
                return {
                    "success": False,
                    "error": "Configuration email non trouvée. Veuillez configurer vos paramètres email."
                }
            
            email_config = self.email_configs[user_id]
            
            # Charger le template
            template = self._load_template(template_name)
            if not template:
                return {
                    "success": False,
                    "error": f"Template '{template_name}' non trouvé"
                }
            
            # Préparer le contenu de l'email
            subject = custom_subject or template["subject"].format(workflow_name=workflow_name)
            body = custom_body or template["body"].format(
                workflow_name=workflow_name,
                execution_date=datetime.now().strftime("%d/%m/%Y à %H:%M"),
                description=f"Résultat de l'exécution du workflow {workflow_name}",
                agents_involved=", ".join(agents_involved),
                result=result
            )
            
            # Envoyer l'email
            success = self._send_email(
                email_config=email_config,
                recipients=recipients,
                subject=subject,
                body=body
            )
            
            if success:
                logger.info(f"✅ Email de résultat de workflow envoyé à {len(recipients)} destinataires")
                return {
                    "success": True,
                    "message": f"Email envoyé avec succès à {len(recipients)} destinataires",
                    "recipients": recipients
                }
            else:
                return {
                    "success": False,
                    "error": "Erreur lors de l'envoi de l'email"
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du résultat de workflow: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_analysis_report(self, user_id: str, report_title: str, analysis_type: str,
                           summary: str, recipients: List[str], template_name: str = "analysis_report",
                           custom_subject: str = None, custom_body: str = None) -> Dict[str, Any]:
        """Envoie un rapport d'analyse par email"""
        try:
            # Vérifier que l'utilisateur a configuré son email
            if user_id not in self.email_configs:
                return {
                    "success": False,
                    "error": "Configuration email non trouvée. Veuillez configurer vos paramètres email."
                }
            
            email_config = self.email_configs[user_id]
            
            # Charger le template
            template = self._load_template(template_name)
            if not template:
                return {
                    "success": False,
                    "error": f"Template '{template_name}' non trouvé"
                }
            
            # Préparer le contenu de l'email
            subject = custom_subject or template["subject"].format(report_title=report_title)
            body = custom_body or template["body"].format(
                report_title=report_title,
                generation_date=datetime.now().strftime("%d/%m/%Y à %H:%M"),
                analysis_type=analysis_type,
                summary=summary
            )
            
            # Envoyer l'email
            success = self._send_email(
                email_config=email_config,
                recipients=recipients,
                subject=subject,
                body=body
            )
            
            if success:
                logger.info(f"✅ Email de rapport d'analyse envoyé à {len(recipients)} destinataires")
                return {
                    "success": True,
                    "message": f"Email envoyé avec succès à {len(recipients)} destinataires",
                    "recipients": recipients
                }
            else:
                return {
                    "success": False,
                    "error": "Erreur lors de l'envoi de l'email"
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du rapport d'analyse: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _load_template(self, template_name: str) -> Optional[Dict[str, str]]:
        """Charge un template d'email"""
        try:
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            if os.path.exists(template_file):
                with open(template_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Erreur lors du chargement du template: {e}")
            return None
    
    def _send_email(self, email_config: Dict[str, Any], recipients: List[str],
                   subject: str, body: str, attachments: List[str] = None) -> bool:
        """Envoie un email avec les paramètres fournis"""
        try:
            smtp_server = email_config["smtp_server"]
            smtp_port = email_config["smtp_port"]
            sender_email = email_config["email"]
            password = email_config["password"]
            use_tls = email_config.get("use_tls", True)
            
            # Créer le message
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            
            # Ajouter le corps du message
            msg.attach(MIMEText(body, 'html'))
            
            # Ajouter les pièces jointes si présentes
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        with open(attachment_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(attachment_path)}'
                        )
                        msg.attach(part)
            
            # Connexion et envoi
            if use_tls:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
            
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email: {e}")
            return False
    
    def get_user_config(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Récupère la configuration email d'un utilisateur"""
        return self.email_configs.get(user_id)
    
    def update_user_config(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Met à jour la configuration email d'un utilisateur"""
        if user_id not in self.email_configs:
            return False
        
        try:
            # Mettre à jour les champs
            for key, value in updates.items():
                if key in ["smtp_server", "smtp_port", "email", "password", "use_tls"]:
                    self.email_configs[user_id][key] = value
            
            # Mettre à jour la date de modification
            self.email_configs[user_id]["configured_at"] = datetime.now().isoformat()
            
            self._save_email_configs()
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la configuration: {e}")
            return False
    
    def delete_user_config(self, user_id: str) -> bool:
        """Supprime la configuration email d'un utilisateur"""
        if user_id in self.email_configs:
            del self.email_configs[user_id]
            self._save_email_configs()
            return True
        return False
    
    def test_user_config(self, user_id: str) -> Dict[str, Any]:
        """Teste la configuration email d'un utilisateur"""
        if user_id not in self.email_configs:
            return {
                "success": False,
                "error": "Configuration non trouvée"
            }
        
        email_config = self.email_configs[user_id]
        
        if self._test_smtp_connection(email_config):
            # Mettre à jour la date du dernier test
            self.email_configs[user_id]["last_test"] = datetime.now().isoformat()
            self._save_email_configs()
            
            return {
                "success": True,
                "message": "Configuration email testée avec succès"
            }
        else:
            return {
                "success": False,
                "error": "Échec de la connexion SMTP"
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de l'agent email"""
        total_configs = len(self.email_configs)
        active_configs = len([c for c in self.email_configs.values() if c.get("status") == "active"])
        
        return {
            "total_configs": total_configs,
            "active_configs": active_configs,
            "templates_available": len(os.listdir(self.templates_dir))
        }

# Instance globale de l'agent email
email_agent = EmailAgent()
