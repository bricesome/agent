import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import io
import base64

# Import des nouveaux modules d'authentification et base de données
from auth.auth_manager import AuthManager
from database.db_manager import DatabaseManager
from agents.email_agent import email_agent
from agents.planner_agent import planner_agent
from datetime import datetime

# Configuration de la page - DOIT être en premier !
st.set_page_config(
    page_title="🤖 Plateforme Agents IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des gestionnaires
auth_manager = AuthManager()
db_manager = DatabaseManager()

# Import du module d'intégration IA
try:
    import ai_integration
    GROK_AVAILABLE = True
except ImportError:
    GROK_AVAILABLE = False
    st.warning("⚠️ Module d'intégration IA non disponible. Installez les dépendances.")

# Fonctions utilitaires existantes
def generate_agent_id():
    return f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def generate_workflow_id():
    return f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def load_agents():
    try:
        if os.path.exists("agents.json"):
            with open("agents.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Erreur lors du chargement des agents: {e}")
        return []

def ensure_system_agents(agents_list):
    """Ajoute les agents système (non supprimables) s'ils sont absents."""
    system_agents = {
        "planner_agent_system": {
            "id": "planner_agent_system",
            "name": "Planificateur de Tâches",
            "domain": "Système",
            "type": "Outil",
            "model": "System",
            "system_prompt": "Agent système de planification (date/heure, week-ends, saisons, conditions).",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": [],
            "system": True
        },
        "email_agent_system": {
            "id": "email_agent_system",
            "name": "Agent d'Envoi d'Emails",
            "domain": "Système",
            "type": "Outil",
            "model": "System",
            "system_prompt": "Agent système d'envoi par email des résultats d'agents/workflows (config SMTP par utilisateur).",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": [],
            "system": True
        }
    }
    existing_ids = {a.get("id") for a in agents_list}
    added = False
    for sys_id, agent in system_agents.items():
        if sys_id not in existing_ids:
            agents_list.append(agent)
            added = True
    if added:
        save_agents(agents_list)
    return agents_list

def save_agents(agents):
    try:
        with open("agents.json", "w", encoding="utf-8") as f:
            json.dump(agents, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des agents: {e}")

def load_models():
    try:
        if os.path.exists("models.json"):
            with open("models.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Erreur lors du chargement des modèles: {e}")
        return []

def save_models(models):
    try:
        with open("models.json", "w", encoding="utf-8") as f:
            json.dump(models, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des modèles: {e}")

def load_workflows():
    try:
        if os.path.exists("workflows.json"):
            with open("workflows.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Erreur lors du chargement des workflows: {e}")
        return []

def save_workflows(workflows):
    try:
        with open("workflows.json", "w", encoding="utf-8") as f:
            json.dump(workflows, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des workflows: {e}")

def execute_workflow_step(step, input_data):
    """Simule l'exécution d'une étape de workflow"""
    import time
    time.sleep(0.5)  # Simulation de délai
    
    step_name = step.get('name', 'Étape')
    agent_name = step.get('agent_name', 'Agent')
    
    # Simulation de résultats selon le type d'étape
    if step.get('type') == 'classification':
        return {
            "status": "success",
            "output": f"Problème classifié comme technique avec priorité moyenne",
            "issue_type": "Problème Technique",
            "priority": "Moyenne"
        }
    elif step.get('type') == 'diagnostic':
        return {
            "status": "success",
            "output": f"Diagnostic: Problème de configuration réseau",
            "root_cause": "Configuration réseau incorrecte",
            "confidence": "85%"
        }
    elif step.get('type') == 'solution':
        return {
            "status": "success",
            "output": f"Solution proposée: Vérifier la configuration réseau",
            "solution_steps": [
                "Vérifier les paramètres DHCP",
                "Tester la connectivité",
                "Redémarrer le service réseau"
            ]
        }
    elif step.get('type') == 'suivi':
        return {
            "status": "success",
            "output": f"Plan de suivi établi",
            "follow_up_date": "2024-01-15"
        }
    else:
        return {
            "status": "success",
            "output": f"Étape {step_name} exécutée par {agent_name}"
        }

# Gestion de l'authentification
def main():
    # Vérifier si l'utilisateur est connecté
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    """Affiche la page de connexion"""
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Connexion - Plateforme Agents IA</h1>
        <p>Connectez-vous pour accéder à la plateforme</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", key="login_username")
            password = st.text_input("Mot de passe", type="password", key="login_password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🔐 Se connecter", use_container_width=True)
            with col_b:
                register_button = st.form_submit_button("📝 S'inscrire", use_container_width=True)
            
            if login_button and username and password:
                user = auth_manager.authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user = user
                    st.rerun()
                else:
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect")
            
            elif register_button:
                st.session_state.show_register = True
                st.rerun()
    
    # Formulaire d'inscription
    if st.session_state.get('show_register', False):
        with col2:
            with st.form("register_form"):
                st.markdown("###  Créer un compte")
                new_username = st.text_input("Nom d'utilisateur", key="reg_username")
                new_email = st.text_input("Email", key="reg_email")
                new_password = st.text_input("Mot de passe", type="password", key="reg_password")
                confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="reg_confirm")
                
                if st.form_submit_button("📝 Créer le compte", use_container_width=True):
                    if new_password != confirm_password:
                        st.error("❌ Les mots de passe ne correspondent pas")
                    elif len(new_password) < 6:
                        st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
                    else:
                        success = auth_manager.register_user(new_username, new_password, new_email)
                        if success:
                            st.success("✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error("❌ Nom d'utilisateur déjà existant")

def show_main_app():
    """Affiche l'application principale"""
    # Charger les données
    agents = load_agents()
    agents = ensure_system_agents(agents)
    models = load_models()
    workflows = load_workflows()
    
    # Calcul des statistiques
    active_agents_count = len([agent for agent in agents if agent.get('status') == 'active'])
    total_agents = len(agents)
    total_models = len(models)
    total_workflows = len(workflows)
    
    # Initialisation des variables de session
    if 'show_create_form' not in st.session_state:
        st.session_state.show_create_form = False
    
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
    
    if 'current_workflow' not in st.session_state:
        st.session_state.current_workflow = None
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "Grok Beta"
    
    # Vues intégrées
    def render_email_configuration_view():
        st.markdown("""
        <div class="main-header">
            <h1>📧 Configuration Email</h1>
            <p>Configurez votre SMTP personnel pour l'envoi des résultats.</p>
        </div>
        """, unsafe_allow_html=True)
        user_id = (st.session_state.current_user.get('username') if st.session_state.get('current_user') else 'local_user') or 'local_user'
        with st.form("email_config_form_inline"):
            col1, col2 = st.columns(2)
            with col1:
                smtp_server = st.text_input("Serveur SMTP", placeholder="smtp.gmail.com")
                email_addr = st.text_input("Adresse Email", placeholder="you@example.com")
                use_tls = st.checkbox("Utiliser TLS", value=True)
            with col2:
                smtp_port = st.number_input("Port SMTP", value=587, step=1)
                password = st.text_input("Mot de passe/Token App", type="password")
            submitted = st.form_submit_button("💾 Sauvegarder & Tester")
            if submitted:
                cfg = {"smtp_server": smtp_server, "smtp_port": int(smtp_port), "email": email_addr, "password": password, "use_tls": bool(use_tls)}
                res = email_agent.configure_user_email(str(user_id), cfg)
                if res.get("success"):
                    st.success("Configuration enregistrée et testée avec succès.")
                else:
                    st.error(res.get("error", "Erreur de configuration"))
        st.markdown("---")
        cfg = email_agent.get_user_config(str(user_id))
        if cfg:
            safe = {k: ("******" if k == "password" else v) for k, v in cfg.items()}
            st.json(safe)

    def render_planning_view():
        st.markdown("""
        <div class="main-header">
            <h1>📆 Planification des Tâches</h1>
            <p>Planifiez l'exécution d'agents, workflows, emails.</p>
        </div>
        """, unsafe_allow_html=True)
        non_system_agents = [a for a in agents if not a.get('system')]
        with st.form("plan_task_form_inline"):
            name = st.text_input("Nom de la tâche", placeholder="Ex: Rapport du samedi")
            description = st.text_area("Description", placeholder="Détails…")
            task_type = st.selectbox("Type d'action", ["agent_execution", "workflow_execution", "email_send", "file_operation", "custom_action"])
            schedule_type = st.selectbox("Type de planification", ["datetime", "recurring", "seasonal", "conditional"])
            schedule_config = {}
            if schedule_type == "datetime":
                c1, c2 = st.columns(2)
                with c1:
                    date_val = st.date_input("Date d'exécution")
                with c2:
                    time_val = st.time_input("Heure d'exécution")
                if date_val and time_val:
                    schedule_config["datetime"] = datetime.combine(date_val, time_val).isoformat()
            elif schedule_type == "recurring":
                frequency = st.selectbox("Fréquence", ["daily", "weekly", "monthly", "weekend"])
                schedule_config["frequency"] = frequency
                if frequency in ("daily", "weekly", "weekend"):
                    schedule_config["time"] = st.time_input("Heure").strftime("%H:%M")
                if frequency == "weekly":
                    schedule_config["day"] = st.selectbox("Jour", ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"])
                if frequency == "monthly":
                    schedule_config["day"] = st.number_input("Jour du mois", min_value=1, max_value=28, value=1)
                    schedule_config["time"] = st.time_input("Heure").strftime("%H:%M")
            elif schedule_type == "seasonal":
                schedule_config["season"] = st.selectbox("Saison", ["spring","summer","autumn","winter"])
                schedule_config["time"] = st.time_input("Heure").strftime("%H:%M")
            elif schedule_type == "conditional":
                cond_type = st.selectbox("Condition", ["email","file","time"]) 
                condition = {"type": cond_type}
                if cond_type == "file":
                    condition["file_path"] = st.text_input("Chemin du fichier à surveiller")
                elif cond_type == "time":
                    a, b = st.columns(2)
                    with a:
                        after = st.text_input("Après (HH:MM)", placeholder="08:00")
                    with b:
                        before = st.text_input("Avant (HH:MM)", placeholder="18:00")
                    condition["time_condition"] = {"after": after, "before": before}
                schedule_config["condition"] = condition

            target = {}
            if task_type == "agent_execution":
                target["agent_name"] = st.selectbox("Agent à exécuter", [a.get('name') for a in non_system_agents]) if non_system_agents else st.text_input("Nom de l'agent")
            elif task_type == "workflow_execution":
                # Charger les workflows
                try:
                    workflows_data = load_workflows()
                except Exception:
                    workflows_data = []
                target["workflow_name"] = st.selectbox("Workflow à exécuter", [w.get('name') for w in workflows_data]) if workflows_data else st.text_input("Nom du workflow")
            elif task_type == "email_send":
                target["subject"] = st.text_input("Sujet")
                target["recipients"] = [e.strip() for e in st.text_input("Destinataires (emails séparés par des virgules)").split(",") if e.strip()]
            elif task_type == "file_operation":
                target["operation"] = st.text_input("Opération (copy/move/etc.)")
                target["file_path"] = st.text_input("Chemin du fichier")
            elif task_type == "custom_action":
                target["action"] = st.text_input("Action personnalisée")

            max_exec = st.number_input("Nombre max d'exécutions (-1 illimité)", value=-1)
            submitted = st.form_submit_button("📅 Planifier")
            if submitted:
                payload = {"name": name, "description": description, "type": task_type, "schedule_type": schedule_type, "schedule_config": schedule_config, "target": target, "max_executions": int(max_exec)}
                res = planner_agent.plan_task(payload)
                if res.get("success"):
                    st.success(res.get("message", "Tâche planifiée"))
                else:
                    st.error(res.get("error", "Erreur"))
    # Alerte globale si l'email n'est pas configuré pour l'utilisateur
    current_username = (st.session_state.current_user.get('username') if st.session_state.get('current_user') else 'local_user') or 'local_user'
    if not email_agent.get_user_config(str(current_username)):
        st.warning("📧 Email non configuré. Configurez votre SMTP pour envoyer des résultats.")
        st.info("Ouvrez la page '📧 Configuration Email' dans la barre latérale")
        try:
            if st.button("Ouvrir la page 📧 Configuration Email →"):
                render_email_configuration_view()
                return
        except Exception:
            pass

    # Configuration de la sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; color: white;">
            <h2 style="color: white;">🤖 IA Platform</h2>
            <p style="color: white; opacity: 0.9;">Gestion des Agents IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu de navigation
        base_options = ["📊 Dashboard", "🤖 Agents", "⚙️ Modèles", "🔄 Workflows", "📈 Statistiques"]
        base_icons = ["📊", "🤖", "⚙️", "🔄", "📈"]
        if st.session_state.get('authenticated', False):
            base_options += ["📧 Configuration Email", "📆 Planification", "👑 Administration"]
            base_icons += ["📧", "📆", "👑"]
        else:
            base_options += ["👑 Administration"]
            base_icons += ["👑"]

        selected = option_menu(
            menu_title=None,
            options=base_options,
            icons=base_icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "background-color": "rgba(255, 255, 255, 0.1)",
                    "padding": "0.5rem",
                    "border-radius": "10px",
                    "margin": "0.5rem 0"
                },
                "nav-link": {
                    "color": "#1f1f1f",
                    "font-size": "1rem",
                    "text-align": "left",
                    "margin": "0.2rem 0",
                    "border-radius": "8px",
                    "padding": "0.5rem 1rem"
                },
                "nav-link:hover": {
                    "color": "#1f1f1f",
                    "background-color": "rgba(255, 255, 255, 0.2)"
                },
                "nav-link-selected": {
                    "color": "white",
                    "background-color": "rgba(102, 126, 234, 0.8)"
                }
            }
        )
        
        # Rien ici: rendu géré plus bas pour conserver un flux clair

        # Raccourcis vers les nouvelles pages
        st.markdown("---")
        st.markdown("### Raccourcis")
        if st.button("📧 Configuration Email"):
            render_email_configuration_view()
            return
        if st.button("📆 Planification des Tâches"):
            render_planning_view()
            return
        
        # Vérifier les permissions d'administration
        current_user_role = st.session_state.current_user.get('role', 'user') if st.session_state.current_user else 'user'
        is_admin = current_user_role == 'admin'
        
        # Bouton de déconnexion
        st.markdown("---")
        if st.button("🚪 Se déconnecter", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
        
        # Afficher les informations de l'utilisateur connecté
        if st.session_state.current_user:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <p style="color: white; margin: 0;"><strong>👤 Connecté en tant que:</strong> {st.session_state.current_user.get('username', 'N/A')}</p>
                <p style="color: white; margin: 0;"><strong>👤 Rôle:</strong> {st.session_state.current_user.get('role', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Page Dashboard
    if selected == "📊 Dashboard":
        st.markdown("""
        <div class="main-header">
            <h1>📊 Dashboard - Plateforme Agents IA</h1>
            <p>Vue d'ensemble de votre plateforme de gestion d'agents IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🤖 Agents Actifs</h3>
                <h2 style="color: #28a745;">{active_agents_count}</h2>
                <p>sur {total_agents} total</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚙️ Modèles IA</h3>
                <h2 style="color: #667eea;">{total_models}</h2>
                <p>disponibles</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 Exécutions</h3>
                <h2 style="color: #ffc107;">{sum(len(agent.get('executions', [])) for agent in agents)}</h2>
                <p>total</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔄 Workflows</h3>
                <h2 style="color: #ffc107;">{total_workflows}</h2>
                <p>disponibles</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Répartition par Type d'Agent")
            if agents:
                type_data = [agent.get('type', 'Autre') for agent in agents]
                type_counts = pd.Series(type_data).value_counts()
                
                if not type_counts.empty:
                    fig = px.pie(
                        values=type_counts.values.tolist(),
                        names=type_counts.index.tolist(),
                        title="Types d'Agents",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune donnée disponible pour les types d'agents")
            else:
                st.info("Aucun agent créé pour le moment")
        
        with col2:
            st.markdown("### 🌐 Répartition par Domaine")
            if agents:
                domain_data = [agent.get('domain', 'Autre') for agent in agents]
                domain_counts = pd.Series(domain_data).value_counts()
                
                if not domain_counts.empty:
                    fig = px.bar(
                        x=domain_counts.index.tolist(),
                        y=domain_counts.values.tolist(),
                        title="Domaines d'Agents",
                        color=domain_counts.values.tolist(),
                        color_continuous_scale="viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune donnée disponible pour les domaines")
            else:
                st.info("Aucun agent créé pour le moment")
        
        # Agents récents
        if agents:
            st.markdown("### 🆕 Agents Récents")
            recent_agents = sorted(agents, key=lambda x: x.get('created_at', ''), reverse=True)[:3]
            
            for agent in recent_agents:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>🤖 {agent.get('name', 'N/A')}</h4>
                        <p><strong>Domaine:</strong> {agent.get('domain', 'N/A')}</p>
                        <p><strong>Type:</strong> {agent.get('type', 'N/A')}</p>
                        <p><strong>Modèle:</strong> {agent.get('model', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button(f"▶️ Exécuter", key=f"exec_{agent['id']}"):
                        st.session_state.current_agent = agent
                        st.success("✅ Agent chargé avec succès ! Redirection vers l'exécution...")
                        st.rerun()

        # Actions rapides
        st.markdown("---")
        st.markdown("### ⚡ Actions rapides")
        user_id = (st.session_state.current_user.get('username') if st.session_state.get('current_user') else 'local_user') or 'local_user'
        user_cfg = email_agent.get_user_config(str(user_id))

        colA, colB = st.columns(2)
        with colA:
            if user_cfg:
                st.success("📧 Email configuré pour cet utilisateur")
            else:
                st.warning("📧 Email non configuré. Configurez votre SMTP pour envoyer des résultats.")
                try:
                    st.page_link("pages/email_configuration.py", label="Configurer l'Email maintenant →", icon="📧")
                except Exception:
                    st.info("Ouvrez la page '📧 Configuration Email' dans la barre latérale")

        with colB:
            st.markdown("#### 🗓️ Planifier rapidement une exécution d'agent")
            non_system_agents = [a for a in agents if not a.get('system')]
            if not non_system_agents:
                st.info("Aucun agent utilisateur disponible.")
            else:
                with st.form("quick_plan_form"):
                    agent_name = st.selectbox("Agent à exécuter", [a.get('name') for a in non_system_agents])
                    plan_type = st.selectbox("Type", ["datetime", "weekend"])
                    if plan_type == "datetime":
                        date_val = st.date_input("Date")
                        time_val = st.time_input("Heure")
                    else:
                        date_val = None
                        time_val = st.time_input("Heure", key="weekend_time")
                    submit_plan = st.form_submit_button("📅 Planifier")
                    if submit_plan:
                        if plan_type == "datetime" and (not date_val or not time_val):
                            st.error("Veuillez sélectionner une date et une heure.")
                        else:
                            if plan_type == "datetime":
                                dt_iso = datetime.combine(date_val, time_val).isoformat()
                                payload = {
                                    "name": f"Exécution {agent_name}",
                                    "description": "Planification rapide depuis Dashboard",
                                    "type": "agent_execution",
                                    "schedule_type": "datetime",
                                    "schedule_config": {"datetime": dt_iso},
                                    "target": {"agent_name": agent_name},
                                    "max_executions": 1
                                }
                            else:
                                payload = {
                                    "name": f"Exécution {agent_name} (week-end)",
                                    "description": "Planification week-end depuis Dashboard",
                                    "type": "agent_execution",
                                    "schedule_type": "recurring",
                                    "schedule_config": {"frequency": "weekend", "time": time_val.strftime("%H:%M")},
                                    "target": {"agent_name": agent_name},
                                    "max_executions": -1
                                }
                            res = planner_agent.plan_task(payload)
                            if res.get("success"):
                                st.success(res.get("message", "Tâche planifiée"))
                            else:
                                st.error(res.get("error", "Erreur lors de la planification"))
    
    # Page Agents
    elif selected == "🤖 Agents":
        st.markdown("""
        <div class="main-header">
            <h1>🤖 Gestion des Agents IA</h1>
            <p>Créez, gérez et exécutez vos agents IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton pour créer un nouvel agent
        if st.button("➕ Créer un Nouvel Agent", use_container_width=True):
            st.session_state.show_create_form = True
        
        # Formulaire de création d'agent
        if st.session_state.show_create_form:
            with st.form("create_agent_form"):
                st.markdown("### 📝 Créer un Nouvel Agent")
                
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Nom de l'Agent", placeholder="Ex: Analyste Financier")
                    domain = st.text_input("Domaine", placeholder="Ex: Finance, Marketing, RH...")
                
                with col2:
                    agent_type = st.selectbox("Type d'Agent", ["Analyse", "Rapport", "Résumé", "Autre"])
                    model = st.selectbox("Modèle IA", [model["name"] for model in models] if models else ["GPT-4", "Claude-3", "Gemini Pro"])
                
                system_prompt = st.text_area(
                    "Prompt Système",
                    placeholder="Définissez le comportement et les capacités de votre agent...",
                    height=150
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Créer l'Agent"):
                        if name and domain and system_prompt:
                            new_agent = {
                                "id": generate_agent_id(),
                                "name": name,
                                "domain": domain,
                                "type": agent_type,
                                "model": model,
                                "system_prompt": system_prompt,
                                "status": "active",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "executions": []
                            }
                            
                            agents.append(new_agent)
                            save_agents(agents)
                            st.success(f"✅ Agent '{name}' créé avec succès !")
                            st.session_state.show_create_form = False
                            st.rerun()
                        else:
                            st.error("❌ Veuillez remplir tous les champs obligatoires.")
                
                with col2:
                    if st.form_submit_button("❌ Annuler"):
                        st.session_state.show_create_form = False
                        st.rerun()
        
        # Liste des agents existants
        if agents:
            st.markdown("### 📋 Agents Existants")
            
            for agent in agents:
                st.markdown(f"""
                <div class="agent-card">
                    <h4>🤖 {agent.get('name', 'N/A')}</h4>
                    <p><strong>Domaine:</strong> {agent.get('domain', 'N/A')}</p>
                    <p><strong>Type:</strong> {agent.get('type', 'N/A')}</p>
                    <p><strong>Modèle:</strong> {agent.get('model', 'N/A')}</p>
                    <p><strong>Statut:</strong> <span style="color: {'green' if agent.get('status') == 'active' else 'orange' if agent.get('status') == 'testing' else 'red'}">{agent.get('status', 'N/A')}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Boutons d'action
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"▶️ Exécuter", key=f"exec_{agent['id']}"):
                        st.session_state.current_agent = agent
                        st.success(f"✅ Agent **{agent.get('name', 'N/A')}** chargé avec succès ! Prêt à l'exécution.")
                        st.rerun()
                
                with col2:
                    if agent.get('system'):
                        st.button(f"✏️ Éditer", key=f"edit_{agent['id']}", disabled=True)
                        st.caption("Agent système non éditable")
                    else:
                        if st.button(f"✏️ Éditer", key=f"edit_{agent['id']}"):
                            st.session_state.editing_agent = agent
                            st.rerun()
                
                with col3:
                    if agent.get('system'):
                        st.button(f"🗑️ Supprimer", key=f"delete_{agent['id']}", disabled=True)
                        st.caption("Agent système non supprimable")
                    else:
                        if st.button(f"🗑️ Supprimer", key=f"delete_{agent['id']}"):
                            agents.remove(agent)
                            save_agents(agents)
                            st.success(f"✅ Agent '{agent.get('name', 'N/A')}' supprimé avec succès !")
                            st.rerun()

                if st.session_state.get('editing_agent') and st.session_state.editing_agent['id'] == agent['id']:
                    st.markdown("### ✏️ Éditer l'Agent")

                    with st.form(f"edit_agent_{agent['id']}"):
                        col1, col2 = st.columns(2)

                        with col1:
                            edit_name = st.text_input("🏷️ Nom", value=agent.get('name', ''),
                                                      key=f"edit_name_{agent['id']}")
                            edit_domain = st.text_input("🎯 Domaine", value=agent.get('domain', ''),
                                                        key=f"edit_domain_{agent['id']}")

                        with col2:
                            edit_type = st.selectbox(
                                "🔧 Type",
                                ["Analyse", "Rapport", "Résumé", "Traduction", "Code", "Autre"],
                                index=["Analyse", "Rapport", "Résumé", "Traduction", "Code", "Autre"].index(
                                    agent.get('type', 'Analyse')),
                                key=f"edit_type_{agent['id']}"
                            )
                            edit_status = st.selectbox(
                                "📊 Statut",
                                ["active", "inactive"],
                                index=["active", "inactive"].index(agent.get('status', 'active')),
                                key=f"edit_status_{agent['id']}"
                            )

                        edit_prompt = st.text_area(
                            "💬 Prompt Système",
                            value=agent.get('system_prompt', ''),
                            height=150,
                            key=f"edit_prompt_{agent['id']}"
                        )

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Sauvegarder", type="primary"):
                                agent.update({
                                    "name": edit_name,
                                    "domain": edit_domain,
                                    "type": edit_type,
                                    "status": edit_status,
                                    "system_prompt": edit_prompt
                                })
                                save_agents(agents)
                                st.success("Agent mis à jour avec succès !")
                                st.session_state.editing_agent = None
                                st.rerun()

                        with col2:
                            if st.form_submit_button("❌ Annuler"):
                                st.session_state.editing_agent = None
                                st.rerun()

                st.markdown("---")
        else:
            st.info("🤖 Aucun agent créé pour le moment. Commencez par en créer un !")
    
    # Vue Configuration Email intégrée
    if selected == "📧 Configuration Email":
        render_email_configuration_view()
        return

    # Vue Planification intégrée
    if selected == "📆 Planification":
        render_planning_view()
        return

    # Page Modèles
    elif selected == "⚙️ Modèles":
        st.markdown("""
        <div class="main-header">
            <h1>⚙️ Gestion des Modèles IA</h1>
            <p>Configurez et gérez vos modèles d'intelligence artificielle</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuration des clés API
        with st.expander("➕ Ajouter un Nouveau Modèle"):
            with st.form("add_model"):
                col1, col2 = st.columns(2)

                with col1:
                    model_name = st.text_input("🏷️ Nom du Modèle", placeholder="Ex: GPT-5")
                    provider = st.text_input("🏢 Fournisseur", placeholder="Ex: OpenAI")

                with col2:
                    api_key = st.text_input("🔑 Clé API", type="password", placeholder="sk-...")
                    status = st.selectbox("📊 Statut", ["active", "inactive", "testing"])

                description = st.text_area("📝 Description", placeholder="Description du modèle...")

                if st.form_submit_button("✅ Ajouter le Modèle", type="primary"):
                    if model_name and provider:
                        new_model = {
                            "name": model_name,
                            "provider": provider,
                            "api_key": api_key,
                            "status": status,
                            "description": description,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        models.append(new_model)
                        save_models(models)
                        st.success(f"Modèle '{model_name}' ajouté avec succès !")
                        st.rerun()
                    else:
                        st.error("Veuillez remplir les champs obligatoires.")
        
        # Intégration avec le module AI
        if GROK_AVAILABLE:
            st.markdown("### 🔗 Intégration IA")
            ai_integration.display_model_status()
        else:
            st.warning("⚠️ Module d'intégration IA non disponible. Installez les dépendances.")
    
    # Page Workflows
    elif selected == "🔄 Workflows":
        st.markdown("""
        <div class="main-header">
            <h1>🔄 Gestion des Workflows Multi-Agents</h1>
            <p>Créez et gérez des workflows complexes impliquant plusieurs agents IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton pour créer un nouveau workflow
        if st.button("➕ Créer un Nouveau Workflow", use_container_width=True):
            st.session_state.show_create_workflow = True
        
        # Formulaire de création de workflow
        if st.session_state.get('show_create_workflow', False):
            with st.form("create_workflow_form"):
                st.markdown("### 📝 Créer un Nouveau Workflow")
                
                workflow_name = st.text_input("Nom du Workflow", placeholder="Ex: Support Client - Résolution de Problème")
                workflow_description = st.text_area("Description", placeholder="Description du workflow et de son objectif...")
                
                # Sélection du type de workflow
                workflow_type = st.selectbox("Type de Workflow", [
                    "Support Client - Résolution de Problème",
                    "Analyse Financière",
                    "Rédaction de Contenu",
                    "Recherche et Analyse",
                    "Personnalisé"
                ])
                
                # Configuration des étapes selon le type
                if workflow_type == "Support Client - Résolution de Problème":
                    st.markdown("####  Étapes du Workflow Support Client")
                    
                    # Étape 1: Classification
                    col1, col2 = st.columns(2)
                    with col1:
                        step1_agent = st.selectbox("Agent Classification", [agent["name"] for agent in agents] if agents else ["Agent Classification"])
                        step1_type = "classification"
                    with col2:
                        step1_description = "Classification automatique du problème client"
                    
                    # Étape 2: Diagnostic
                    col1, col2 = st.columns(2)
                    with col1:
                        step2_agent = st.selectbox("Agent Diagnostic", [agent["name"] for agent in agents] if agents else ["Agent Diagnostic"])
                        step2_type = "diagnostic"
                    with col2:
                        step2_description = "Analyse approfondie et diagnostic du problème"
                    
                    # Étape 3: Solution
                    col1, col2 = st.columns(2)
                    with col1:
                        step3_agent = st.selectbox("Agent Solution", [agent["name"] for agent in agents] if agents else ["Agent Solution"])
                        step2_type = "solution"
                    with col2:
                        step3_description = "Proposition de solution adaptée"
                    
                    # Étape 4: Suivi
                    col1, col2 = st.columns(2)
                    with col1:
                        step4_agent = st.selectbox("Agent Suivi", [agent["name"] for agent in agents] if agents else ["Agent Suivi"])
                        step4_type = "suivi"
                    with col2:
                        step4_description = "Planification du suivi et vérification"
                    
                    workflow_steps = [
                        {"order": 1, "name": "Classification", "agent_name": step1_agent, "type": step1_type, "description": step1_description},
                        {"order": 2, "name": "Diagnostic", "agent_name": step2_agent, "type": step2_type, "description": step2_description},
                        {"order": 3, "name": "Solution", "agent_name": step3_agent, "type": step2_type, "description": step3_description},
                        {"order": 4, "name": "Suivi", "agent_name": step4_agent, "type": step4_type, "description": step4_description}
                    ]
                
                elif workflow_type == "Analyse Financière":
                    st.markdown("####  Étapes du Workflow Analyse Financière")
                    
                    # Étape 1: Collecte de données
                    col1, col2 = st.columns(2)
                    with col1:
                        step1_agent = st.selectbox("Agent Collecte", [agent["name"] for agent in agents] if agents else ["Agent Collecte"])
                        step1_type = "collecte"
                    with col2:
                        step1_description = "Collecte et validation des données financières"
                    
                    # Étape 2: Analyse
                    col1, col2 = st.columns(2)
                    with col1:
                        step2_agent = st.selectbox("Agent Analyse", [agent["name"] for agent in agents] if agents else ["Agent Analyse"])
                        step2_type = "analyse"
                    with col2:
                        step2_description = "Analyse approfondie des indicateurs financiers"
                    
                    # Étape 3: Rapport
                    col1, col2 = st.columns(2)
                    with col1:
                        step3_agent = st.selectbox("Agent Rapport", [agent["name"] for agent in agents] if agents else ["Agent Rapport"])
                        step3_type = "rapport"
                    with col2:
                        step3_description = "Génération du rapport d'analyse"
                    
                    workflow_steps = [
                        {"order": 1, "name": "Collecte", "agent_name": step1_agent, "type": step1_type, "description": step1_description},
                        {"order": 2, "name": "Analyse", "agent_name": step2_agent, "type": step2_type, "description": step2_description},
                        {"order": 3, "name": "Rapport", "agent_name": step3_agent, "type": step3_type, "description": step3_description}
                    ]
                
                elif workflow_type == "Rédaction de Contenu":
                    st.markdown("####  Étapes du Workflow Rédaction de Contenu")
                    
                    # Étape 1: Recherche
                    col1, col2 = st.columns(2)
                    with col1:
                        step1_agent = st.selectbox("Agent Recherche", [agent["name"] for agent in agents] if agents else ["Agent Recherche"])
                        step1_type = "recherche"
                    with col2:
                        step1_description = "Recherche et collecte d'informations"
                    
                    # Étape 2: Planification
                    col1, col2 = st.columns(2)
                    with col1:
                        step2_agent = st.selectbox("Agent Planification", [agent["name"] for agent in agents] if agents else ["Agent Planification"])
                        step2_type = "planification"
                    with col2:
                        step2_description = "Planification de la structure du contenu"
                    
                    # Étape 3: Rédaction
                    col1, col2 = st.columns(2)
                    with col1:
                        step3_agent = st.selectbox("Agent Rédaction", [agent["name"] for agent in agents] if agents else ["Agent Rédaction"])
                        step3_type = "redaction"
                    with col2:
                        step3_description = "Rédaction du contenu final"
                    
                    # Étape 4: Révision
                    col1, col2 = st.columns(2)
                    with col1:
                        step4_agent = st.selectbox("Agent Révision", [agent["name"] for agent in agents] if agents else ["Agent Révision"])
                        step4_type = "revision"
                    with col2:
                        step4_description = "Révision et amélioration du contenu"
                    
                    workflow_steps = [
                        {"order": 1, "name": "Recherche", "agent_name": step1_agent, "type": step1_type, "description": step1_description},
                        {"order": 2, "name": "Planification", "agent_name": step2_agent, "type": step2_type, "description": step2_description},
                        {"order": 3, "name": "Rédaction", "agent_name": step3_agent, "type": step3_type, "description": step3_description},
                        {"order": 4, "name": "Révision", "agent_name": step4_agent, "type": step4_type, "description": step4_description}
                    ]
                
                else:
                    st.info("Configuration personnalisée des étapes à implémenter")
                    workflow_steps = []
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Créer le Workflow"):
                        if workflow_name and workflow_description:
                            new_workflow = {
                                "id": generate_workflow_id(),
                                "name": workflow_name,
                                "description": workflow_description,
                                "type": workflow_type,
                                "steps": workflow_steps,
                                "status": "active",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "executions": []
                            }
                            
                            workflows.append(new_workflow)
                            save_workflows(workflows)
                            st.success(f"✅ Workflow '{workflow_name}' créé avec succès !")
                            st.session_state.show_create_workflow = False
                            st.rerun()
                        else:
                            st.error("❌ Veuillez remplir tous les champs obligatoires.")
                
                with col2:
                    if st.form_submit_button("❌ Annuler"):
                        st.session_state.show_create_workflow = False
                        st.rerun()
        
        # Liste des workflows existants
        if workflows:
            st.markdown("### 📋 Workflows Disponibles")
            
            for workflow in workflows:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>🔄 {workflow.get('name', 'N/A')}</h4>
                        <p><strong>Type:</strong> {workflow.get('type', 'N/A')}</p>
                        <p><strong>Description:</strong> {workflow.get('description', 'Aucune description')}</p>
                        <p><strong>Étapes:</strong> {len(workflow.get('steps', []))} étapes</p>
                        <p><strong>Statut:</strong> <span style="color: {'green' if workflow.get('status') == 'active' else 'orange' if workflow.get('status') == 'testing' else 'red'}">{workflow.get('status', 'N/A')}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    workflow_id = workflow.get('id', 'unknown')
                    if st.button(f"▶️ Exécuter", key=f"exec_workflow_{workflow_id}"):
                        st.session_state.current_workflow = workflow
                        st.success(f"✅ Workflow **{workflow.get('name', 'N/A')}** prêt à l'exécution !")
                
                with col3:
                    workflow_name = workflow.get('name', 'Workflow sans nom')
                    workflow_id = workflow.get('id', 'unknown')
                    
                    # Créer une clé unique pour la confirmation
                    confirm_key = f"confirm_delete_{workflow_id}"
                    delete_key = f"delete_workflow_{workflow_id}"
                    
                    if confirm_key not in st.session_state:
                        st.session_state[confirm_key] = False
                    
                    if not st.session_state[confirm_key]:
                        if st.button(f"🗑️ Supprimer", key=delete_key):
                            st.session_state[confirm_key] = True
                    else:
                        col_confirm1, col_confirm2, col_confirm3 = st.columns([1, 1, 1])
                        with col_confirm1:
                            st.warning(f"Supprimer '{workflow_name}' ?")
                        with col_confirm2:
                            if st.button("✅ Oui", key=f"yes_{workflow_id}"):
                                workflows.remove(workflow)
                                save_workflows(workflows)
                                st.success(f"✅ Workflow '{workflow_name}' supprimé avec succès !")
                                st.rerun()
                        with col_confirm3:
                            if st.button("❌ Non", key=f"no_{workflow_id}"):
                                st.session_state[confirm_key] = False
                                st.rerun()
            
            # Afficher les détails des étapes si un workflow est sélectionné
            if st.session_state.get('current_workflow'):
                workflow = st.session_state.current_workflow
                st.markdown("### 🔍 Détails du Workflow Sélectionné")
                
                # Afficher les étapes
                for step in workflow.get('steps', []):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"**Étape {step['order']}:** {step['name']}")
                    with col2:
                        st.markdown(f"Agent: {step['agent_name']} - {step['description']}")
                
                # Bouton pour exécuter le workflow
                if st.button(" Lancer l'Exécution du Workflow", key="launch_workflow"):
                    # Initialiser l'état d'exécution
                    if 'workflow_executing' not in st.session_state:
                        st.session_state.workflow_executing = False
                    
                    st.session_state.workflow_executing = True
                    
                    # Animation pendant l'exécution
                    st.markdown("### 🔄 Exécution du Workflow en Cours...")
                    
                    # Barre de progression animée
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulation de l'exécution avec animation
                    input_data = {"issue_type": "Problème Technique", "priority": "Moyenne"}
                    total_steps = len(workflow.get('steps', []))
                    results_summary = []
                    
                    for i, step in enumerate(workflow.get('steps', [])):
                        # Mettre à jour la barre de progression
                        progress = (i + 1) / total_steps
                        progress_bar.progress(progress)
                        status_text.text(f" Exécution de l'étape {i + 1}/{total_steps}: {step['name']}")
                        
                        # Utiliser un conteneur simple au lieu d'un expander imbriqué
                        st.markdown(f"###  {step['name']} - {step['agent_name']}")
                        
                        # Créer une zone délimitée pour chaque étape
                        st.info(f"**Agent en cours:** {step['agent_name']}")
                        
                        # Simuler l'exécution avec délai pour l'animation
                        import time
                        time.sleep(0.5)  # Délai pour voir l'animation
                        
                        result = execute_workflow_step(step, input_data)
                        
                        if result["status"] == "success":
                            st.success(f"✅ {step['name']} terminé avec succès")
                            st.info(f"**Résultat:** {result['output']}")
                            
                            # Stocker le résultat pour le résumé
                            results_summary.append({
                                "étape": step['name'],
                                "agent": step['agent_name'],
                                "statut": "✅ Succès",
                                "résultat": result['output']
                            })
                            
                            # Mettre à jour les données d'entrée pour l'étape suivante
                            input_data.update(result)
                        else:
                            st.error(f"❌ Erreur lors de {step['name']}: {result.get('error', 'Erreur inconnue')}")
                            results_summary.append({
                                "étape": step['name'],
                                "agent": step['agent_name'],
                                "statut": "❌ Erreur",
                                "résultat": result.get('error', 'Erreur inconnue')
                            })
                            break
                    
                    # Finaliser l'animation
                    progress_bar.progress(1.0)
                    status_text.text(" Exécution terminée !")
                    
                    # Animation de succès
                    st.balloons()
                    
                    # Afficher le résumé final
                    st.markdown("### 📊 Résumé de l'Exécution")
                    
                    # Créer un tableau des résultats avec style
                    if results_summary:
                        summary_df = pd.DataFrame(results_summary)
                        
                        # Appliquer un style au DataFrame
                        st.markdown("""
                        <style>
                        .dataframe {
                            font-size: 14px;
                            border-collapse: collapse;
                            width: 100%;
                        }
                        .dataframe th {
                            background-color: #f0f2f6;
                            color: #262730;
                            font-weight: bold;
                            padding: 12px;
                            text-align: left;
                            border: 1px solid #ddd;
                        }
                        .dataframe td {
                            padding: 12px;
                            border: 1px solid #ddd;
                            text-align: left;
                        }
                        .dataframe tr:nth-child(even) {
                            background-color: #f9f9f9;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        st.dataframe(summary_df, use_container_width=True)
                    
                    # Afficher les données finales de manière plus claire
                    st.markdown("###  Données Finales du Workflow")
                    
                    # Créer des colonnes pour afficher les données de manière organisée
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 📋 Informations de Base")
                        st.info(f"**Type de problème:** {input_data.get('issue_type', 'N/A')}")
                        st.info(f"**Priorité:** {input_data.get('priority', 'N/A')}")
                        
                        if 'confidence' in input_data:
                            st.info(f"**Confiance:** {input_data.get('confidence', 'N/A')}")
                        
                        if 'root_cause' in input_data:
                            st.info(f"**Cause racine:** {input_data.get('root_cause', 'N/A')}")
                    
                    with col2:
                        st.markdown("#### 🎯 Solutions et Actions")
                        if 'solution_steps' in input_data:
                            st.markdown("**Étapes de résolution:**")
                            for i, step in enumerate(input_data.get('solution_steps', []), 1):
                                st.markdown(f"{i}. {step}")
                        
                        if 'follow_up_date' in input_data:
                            st.info(f"**Date de suivi:** {input_data.get('follow_up_date', 'N/A')}")
                    
                    st.success("🎉 Workflow exécuté avec succès !")
                    
                    # Sauvegarder l'exécution
                    execution_record = {
                        "id": f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "completed",
                        "results": input_data,
                        "summary": results_summary
                    }
                    
                    if 'executions' not in workflow:
                        workflow['executions'] = []
                    workflow['executions'].append(execution_record)
                    save_workflows(workflows)
                    
                    # Réinitialiser l'état d'exécution
                    st.session_state.workflow_executing = False
                    
                    # Afficher l'historique des exécutions
                    if workflow.get('executions'):
                        st.markdown("### 📚 Historique des Exécutions")
                        
                        # Créer un DataFrame de l'historique
                        history_data = []
                        for exec_record in workflow.get('executions', []):
                            history_data.append({
                                "ID": exec_record.get('id', 'N/A'),
                                "Date": exec_record.get('start_time', 'N/A'),
                                "Statut": exec_record.get('status', 'N/A'),
                                "Étapes": len(exec_record.get('summary', []))
                            })
                        
                        if history_data:
                            history_df = pd.DataFrame(history_data)
                            st.dataframe(history_df, use_container_width=True)
                            
                            # Bouton pour voir les détails de la dernière exécution
                            if st.button(" Voir Détails de la Dernière Exécution", key="view_last_exec"):
                                st.markdown("###  Détails de la Dernière Exécution")
                                executions = workflow.get('executions', [])
                                if executions:
                                    last_exec = executions[-1]
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.info(f"**ID:** {last_exec.get('id', 'N/A')}")
                                        st.info(f"**Date:** {last_exec.get('start_time', 'N/A')}")
                                        st.info(f"**Statut:** {last_exec.get('status', 'N/A')}")
                                    
                                    with col2:
                                        st.info(f"**Étapes exécutées:** {len(last_exec.get('summary', []))}")
                                        st.info(f"**Données finales:** {len(last_exec.get('results', {}))} champs")
                                    
                                    # Afficher le résumé détaillé
                                    if last_exec.get('summary'):
                                        st.markdown("####  Résumé Détaillé")
                                        summary_df = pd.DataFrame(last_exec['summary'])
                                        st.dataframe(summary_df, use_container_width=True)
                                else:
                                    st.error("Aucune exécution trouvée")
        
        else:
            st.info(" Aucun workflow créé pour le moment. Commencez par en créer un !")
    
    # Page Statistiques
    elif selected == "📈 Statistiques":
        st.markdown("""
        <div class="main-header">
            <h1>📈 Statistiques et Analyses</h1>
            <p>Analysez les performances et l'utilisation de vos agents IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        if agents:
            # Statistiques générales
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Statistiques Générales")
                type_data = [agent.get('type', 'Autre') for agent in agents]
                type_counts = pd.Series(type_data).value_counts()
                
                if not type_counts.empty:
                    fig = px.pie(
                        values=type_counts.values.tolist(),
                        names=type_counts.index.tolist(),
                        title="Répartition par Type",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune donnée disponible pour les types d'agents")
            
            with col2:
                st.markdown("### 🌐 Répartition par Domaine")
                domain_data = [agent.get('domain', 'Autre') for agent in agents]
                domain_counts = pd.Series(domain_data).value_counts()
                
                if not domain_counts.empty:
                    fig = px.bar(
                        x=domain_counts.index.tolist(),
                        y=domain_counts.values.tolist(),
                        title="Domaines d'Agents",
                        color=domain_counts.values.tolist(),
                        color_continuous_scale="plasma"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune donnée disponible pour les domaines")
            
            # Statistiques détaillées
            st.markdown("### 📊 Détails des Agents")
            
            # Créer un DataFrame pour les analyses
            agent_data = []
            for agent in agents:
                executions = agent.get('executions', [])
                agent_data.append({
                    'Nom': agent.get('name', 'N/A'),
                    'Domaine': agent.get('domain', 'N/A'),
                    'Type': agent.get('type', 'N/A'),
                    'Statut': agent.get('status', 'N/A'),
                    'Exécutions': len(executions),
                    'Créé le': agent.get('created_at', 'N/A')
                })
            
            if agent_data:
                df = pd.DataFrame(agent_data)
                st.dataframe(df, use_container_width=True)
                
                # Ajouter des colonnes calculées
                st.markdown("### 📈 Métriques Avancées")
                
                total_executions = sum(len(agent.get('executions', [])) for agent in agents)
                avg_executions = total_executions / len(agents) if agents else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Exécutions", total_executions)
                with col2:
                    st.metric("Moyenne par Agent", f"{avg_executions:.1f}")
                with col3:
                    st.metric("Agents Actifs", active_agents_count)
            else:
                st.info("Aucune donnée disponible pour l'analyse")
        
        else:
            st.info("🤖 Aucun agent créé pour le moment. Les statistiques seront disponibles une fois que vous aurez créé des agents.")

    # Page Administration (Accès restreint aux administrateurs)
    elif selected == "👑 Administration":
        # Vérifier les permissions d'administration
        if not is_admin:
            st.error("🚫 Accès refusé. Cette page est réservée aux administrateurs.")
            st.info("Contactez votre administrateur pour obtenir les privilèges nécessaires.")
            return
        
        st.markdown("""
        <div class="main-header">
            <h1>👑 Administration de la Plateforme</h1>
            <p>Gérez les utilisateurs, les permissions et la configuration système</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Onglets d'administration
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["👥 Gestion Utilisateurs", "🔐 Permissions", "⚙️ Configuration Système"])
        
        with admin_tab1:
            st.markdown("### 👥 Gestion des Utilisateurs")
            
            # Créer un nouvel utilisateur
            with st.expander("➕ Créer un Nouvel Utilisateur", expanded=False):
                with st.form("create_user_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_username = st.text_input("Nom d'utilisateur", key="admin_new_username")
                        new_email = st.text_input("Email", key="admin_new_email")
                    
                    with col2:
                        new_password = st.text_input("Mot de passe", type="password", key="admin_new_password")
                        new_role = st.selectbox("Rôle", ["user", "admin"], key="admin_new_role")
                    
                    if st.form_submit_button("✅ Créer l'Utilisateur"):
                        if new_username and new_email and new_password:
                            if len(new_password) < 6:
                                st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
                            else:
                                success = auth_manager.register_user(
                                    new_username, 
                                    new_password, 
                                    new_email, 
                                    new_role
                                )
                                
                                if success:
                                    # Ajouter à la base de données
                                    user_id = db_manager.insert_user(
                                        new_username,
                                        new_email,
                                        auth_manager.users[new_username]["password_hash"],
                                        new_role
                                    )
                                    
                                    if user_id:
                                        st.success(f"✅ Utilisateur '{new_username}' créé avec succès ! (ID: {user_id})")
                                    else:
                                        st.warning(f"⚠️ Utilisateur créé dans l'auth mais erreur dans la base de données")
                                    
                                    st.rerun()
                                else:
                                    st.error("❌ Nom d'utilisateur déjà existant")
                        else:
                            st.error("❌ Tous les champs sont obligatoires")
            
            # Liste des utilisateurs existants
            st.markdown("###  Utilisateurs Existants")
            
            if auth_manager.users:
                # Créer un DataFrame pour l'affichage
                users_data = []
                for username, user_data in auth_manager.users.items():
                    users_data.append({
                        "Nom d'utilisateur": username,
                        "Email": user_data.get('email', 'N/A'),
                        "Rôle": user_data.get('role', 'N/A'),
                        "Statut": "🟢 Actif" if user_data.get('is_active', True) else "🔴 Inactif",
                        "Créé le": user_data.get('created_at', 'N/A'),
                        "Dernière connexion": user_data.get('last_login', 'Jamais') or 'Jamais'
                    })
                
                users_df = pd.DataFrame(users_data)
                st.dataframe(users_df, use_container_width=True)
                
                # Actions sur les utilisateurs
                st.markdown("### 🎯 Actions sur les Utilisateurs")
                
                selected_user = st.selectbox(
                    "Sélectionner un utilisateur",
                    options=list(auth_manager.users.keys()),
                    key="admin_user_selector"
                )
                
                if selected_user and selected_user != st.session_state.current_user.get('username'):
                    user_data = auth_manager.users[selected_user]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Modifier le Rôle", key=f"edit_role_{selected_user}"):
                            st.session_state.editing_user_role = selected_user
                    
                    with col2:
                        if st.button(" Désactiver", key=f"deactivate_{selected_user}"):
                            # Désactiver l'utilisateur
                            if 'is_active' not in user_data:
                                user_data['is_active'] = True
                            
                            user_data['is_active'] = not user_data['is_active']
                            auth_manager._save_users()
                            
                            status = "activé" if user_data['is_active'] else "désactivé"
                            st.success(f"✅ Utilisateur '{selected_user}' {status} avec succès !")
                            st.rerun()
                    
                    with col3:
                        if st.button("️ Supprimer", key=f"delete_user_{selected_user}"):
                            # Demander confirmation
                            if st.checkbox(f"Confirmer la suppression de '{selected_user}' ?", key=f"confirm_delete_{selected_user}"):
                                del auth_manager.users[selected_user]
                                auth_manager._save_users()
                                st.success(f"✅ Utilisateur '{selected_user}' supprimé avec succès !")
                                st.rerun()
                    
                    # Édition du rôle
                    if st.session_state.get('editing_user_role') == selected_user:
                        st.markdown("#### ✏️ Modifier le Rôle")
                        
                        new_role = st.selectbox(
                            "Nouveau rôle",
                            options=["user", "admin"],
                            index=0 if user_data.get('role') == 'user' else 1,
                            key=f"new_role_{selected_user}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("💾 Sauvegarder", key=f"save_role_{selected_user}"):
                                user_data['role'] = new_role
                                auth_manager._save_users()
                                st.success(f"✅ Rôle de '{selected_user}' modifié en '{new_role}' !")
                                st.session_state.editing_user_role = None
                                st.rerun()
                        
                        with col2:
                            if st.button("❌ Annuler", key=f"cancel_role_{selected_user}"):
                                st.session_state.editing_user_role = None
                                st.rerun()
                
                else:
                    if selected_user == st.session_state.current_user.get('username'):
                        st.info("ℹ️ Vous ne pouvez pas modifier votre propre compte depuis cette interface.")
            else:
                st.info("👥 Aucun utilisateur trouvé.")
        
        with admin_tab2:
            st.markdown("### 🔐 Gestion des Permissions")
            
            st.info("""
            **Rôles et Permissions :**
            
             **Administrateur :**
            - Accès complet à toutes les fonctionnalités
            - Gestion des utilisateurs (créer, modifier, supprimer)
            - Configuration système
            - Accès à la page d'administration
            
             **Utilisateur :**
            - Création et gestion de ses propres agents
            - Exécution des agents et workflows
            - Accès aux statistiques personnelles
            - Pas d'accès à l'administration
            """)
            
            # Statistiques des permissions
            if auth_manager.users:
                admin_count = len([u for u in auth_manager.users.values() if u.get('role') == 'admin'])
                user_count = len([u for u in auth_manager.users.values() if u.get('role') == 'user'])
                active_count = len([u for u in auth_manager.users.values() if u.get('is_active', True)])
                inactive_count = len([u for u in auth_manager.users.values() if not u.get('is_active', True)])
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("👑 Administrateurs", admin_count)
                
                with col2:
                    st.metric("👤 Utilisateurs", user_count)
                
                with col3:
                    st.metric("🟢 Actifs", active_count)
                
                with col4:
                    st.metric("🔴 Inactifs", inactive_count)
        
        with admin_tab3:
            st.markdown("### ⚙️ Configuration Système")
            
            st.warning("⚠️ Cette section sera développée dans les prochaines versions.")
            
            st.info("""
            **Fonctionnalités à venir :**
            - Configuration des paramètres de sécurité
            - Gestion des clés API système
            - Configuration de la base de données
            - Logs et monitoring
            - Sauvegarde et restauration
            """)

# Styles CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: bold;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    margin: 1rem 0;
}

.metric-card h3 {
    color: #667eea;
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
}

.metric-card h2 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: bold;
}

.metric-card p {
    margin: 0.5rem 0 0 0;
    color: #666;
    font-size: 0.9rem;
}

.agent-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    border-left: 5px solid #667eea;
}

.agent-card h4 {
    color: #667eea;
    margin: 0 0 1rem 0;
    font-size: 1.3rem;
}

.agent-card p {
    margin: 0.3rem 0;
    color: #333;
}

.agent-card strong {
    color: #667eea;
}
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
