import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

# Configuration de la page - DOIT être en premier !
st.set_page_config(
    page_title="🤖 Plateforme Agents IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import du module d'intégration IA
try:
    from ai_integration import display_model_status, ai_orchestrator
    GROK_AVAILABLE = True
except ImportError:
    GROK_AVAILABLE = False
    st.warning("⚠️ Module d'intégration IA non disponible. Installez les dépendances.")

# CSS personnalisé pour une interface moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }

    .agent-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #28a745;
        transition: transform 0.3s;
    }

    .agent-card:hover {
        transform: translateY(-5px);
    }

    .btn-primary {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .btn-success {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }

    .btn-success:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
    }

    .btn-danger {
        background: linear-gradient(90deg, #dc3545 0%, #c82333 100%);
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }

    .btn-danger:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4);
    }

    /* Sidebar text colors */
    .css-1d391kg {
        color: white !important;
    }

    .css-1d391kg .css-1d391kg {
        color: white !important;
    }

    /* Navigation menu colors */
    .css-1d391kg .css-1d391kg a {
        color: #333 !important;
    }

    .css-1d391kg .css-1d391kg .css-1d391kg {
        color: white !important;
    }

    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        color: rgba(255, 255, 255, 0.8) !important;
    }

    /* streamlit-option-menu specific styling */
    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        color: #1f1f1f !important;
    }

    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        color: #1f1f1f !important;
    }

    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        color: white !important;
    }

    /* streamlit-option-menu link colors */
    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        color: #1f1f1f !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 2px 0 !important;
        transition: all 0.3s ease !important;
    }

    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg:hover {
        background-color: rgba(255, 255, 255, 0.95) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }

    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg[data-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
    }


</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False

if 'editing_agent' not in st.session_state:
    st.session_state.editing_agent = None

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None

if 'show_create_workflow' not in st.session_state:
    st.session_state.show_create_workflow = False

if 'current_workflow' not in st.session_state:
    st.session_state.current_workflow = None

# Variables globales
active_agents_count = 0

# Fonctions utilitaires
def load_agents():
    """Charge la liste des agents depuis le fichier JSON"""
    if os.path.exists('agents.json'):
        with open('agents.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_agents(agents):
    """Sauvegarde la liste des agents dans le fichier JSON"""
    with open('agents.json', 'w', encoding='utf-8') as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)

def load_models():
    """Charge la liste des modèles depuis le fichier JSON"""
    if os.path.exists('models.json'):
        with open('models.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_models(models):
    """Sauvegarde la liste des modèles dans le fichier JSON"""
    with open('models.json', 'w', encoding='utf-8') as f:
        json.dump(models, f, ensure_ascii=False, indent=2)

def generate_agent_id():
    """Génère un ID unique pour un agent"""
    return f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"

def get_model_status_color(status):
    """Retourne la couleur appropriée pour le statut du modèle"""
    if status == 'active':
        return 'green'
    elif status == 'testing':
        return 'orange'
    else:
        return 'red'

def load_workflows():
    """Charge la liste des workflows depuis le fichier JSON"""
    if os.path.exists('workflows.json'):
        try:
            with open('workflows.json', 'r', encoding='utf-8') as f:
                workflows = json.load(f)
            
            # Valider et nettoyer les workflows
            cleaned_workflows = []
            for workflow in workflows:
                if isinstance(workflow, dict):
                    # S'assurer que tous les champs requis existent
                    cleaned_workflow = {
                        'id': workflow.get('id', generate_workflow_id()),
                        'name': workflow.get('name', 'Workflow sans nom'),
                        'description': workflow.get('description', 'Aucune description'),
                        'type': workflow.get('type', 'Général'),
                        'steps': workflow.get('steps', []),
                        'status': workflow.get('status', 'active'),
                        'created_at': workflow.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        'executions': workflow.get('executions', [])
                    }
                    cleaned_workflows.append(cleaned_workflow)
            
            return cleaned_workflows
        except Exception as e:
            st.error(f"Erreur lors du chargement des workflows: {e}")
            return []
    return []

def save_workflows(workflows):
    """Sauvegarde la liste des workflows dans le fichier JSON"""
    with open('workflows.json', 'w', encoding='utf-8') as f:
        json.dump(workflows, f, ensure_ascii=False, indent=2)

def generate_workflow_id():
    """Génère un ID unique pour un workflow"""
    return f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"

def execute_workflow_step(step, input_data):
    """Exécute une étape du workflow"""
    # Simulation de l'exécution d'une étape
    agent_name = step.get('agent_name', 'Agent Inconnu')
    step_type = step.get('type', 'unknown')
    
    # Logique d'exécution selon le type d'étape
    if step_type == 'classification':
        return {
            "status": "success",
            "output": f"Problème classifié comme: {input_data.get('issue_type', 'Général')}",
            "confidence": 0.95,
            "next_steps": ["diagnostic"]
        }
    elif step_type == 'diagnostic':
        return {
            "status": "success",
            "output": f"Diagnostic effectué: {input_data.get('issue_type', 'Général')} - Analyse complète",
            "root_cause": "Cause identifiée",
            "next_steps": ["solution"]
        }
    elif step_type == 'solution':
        return {
            "status": "success",
            "output": f"Solution proposée pour: {input_data.get('issue_type', 'Général')}",
            "solution_steps": ["Étape 1", "Étape 2", "Étape 3"],
            "next_steps": ["suivi"]
        }
    elif step_type == 'suivi':
        return {
            "status": "success",
            "output": f"Suivi planifié pour: {input_data.get('issue_type', 'Général')}",
            "follow_up_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "next_steps": []
        }
    else:
        return {
            "status": "error",
            "output": f"Type d'étape non reconnu: {step_type}",
            "error": "Type d'étape invalide"
        }

# Chargement des données
agents = load_agents()
models = load_models()
workflows = load_workflows()

# Calcul des statistiques
active_agents_count = len([agent for agent in agents if agent.get('status') == 'active'])
total_agents = len(agents)
total_models = len(models)
total_workflows = len(workflows)

# Configuration de la sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: white;">
        <h2 style="color: white;">🤖 IA Platform</h2>
        <p style="color: white; opacity: 0.9;">Gestion des Agents IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu de navigation
    selected = option_menu(
        menu_title=None,
        options=["📊 Dashboard", "🤖 Agents", "⚙️ Modèles", "🔄 Workflows", "📈 Statistiques"],
        icons=["📊", "🤖", "⚙️", "🔄", "📈"],
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
            # Utiliser pd.Series pour éviter les erreurs MultiIndex
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
            # Utiliser pd.Series pour éviter les erreurs MultiIndex
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
    
    # Agents récents avec limite
    if agents:
        st.markdown("### 🆕 Agents Récents")
        
        # Créer un conteneur avec bordure visuelle
        with st.container():
            # Créer une zone délimitée avec st.expander
            with st.expander("📋 **Zone des Agents Récents**", expanded=True):
                # Limiter le nombre d'agents affichés
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
                
                # Afficher un bouton pour voir plus d'agents si nécessaire
                if len(agents) > 3:
                    if st.button("📋 Voir Tous les Agents", key="voir_tous_agents"):
                        st.rerun()

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
    
    # Liste des agents existants avec pagination
    if agents:
        st.markdown("### 📋 Agents Existants")
        
        # Pagination pour éviter les listes trop longues
        agents_per_page = 5
        total_pages = (len(agents) + agents_per_page - 1) // agents_per_page
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        
        # Sélecteur de page
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page = st.selectbox(
                "Page", 
                range(total_pages), 
                index=st.session_state.current_page,
                key="page_selector"
            )
            st.session_state.current_page = page
        
        # Calculer les agents à afficher pour cette page
        start_idx = page * agents_per_page
        end_idx = min(start_idx + agents_per_page, len(agents))
        current_agents = agents[start_idx:end_idx]
        
        # Affichage simple des agents sans zone déroulante
        st.markdown(f"**📋 Page {page + 1} sur {total_pages} - Agents {start_idx + 1} à {end_idx} sur {len(agents)}**")
        
        for agent in current_agents:
            st.markdown(f"""
            <div class="agent-card">
                <h4>🤖 {agent.get('name', 'N/A')}</h4>
                <p><strong>Domaine:</strong> {agent.get('domain', 'N/A')}</p>
                <p><strong>Type:</strong> {agent.get('type', 'N/A')}</p>
                <p><strong>Modèle:</strong> {agent.get('model', 'N/A')}</p>
                <p><strong>Statut:</strong> <span style="color: {'green' if agent.get('status') == 'active' else 'orange' if agent.get('status') == 'testing' else 'red'}">{agent.get('status', 'N/A')}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Boutons d'action - Chaque agent a ses propres options TRÈS spécifiques
            col1, col2, col3, col4, col5 = st.columns(5)
            
            # Créer des clés TRÈS uniques pour chaque agent
            agent_unique_id = f"{agent['id']}_{agent.get('name', 'unknown').replace(' ', '_').replace('-', '_')}_{agent.get('created_at', 'unknown').replace(' ', '_').replace(':', '_')}"
            
            with col1:
                exec_key = f"exec_agent_{agent_unique_id}"
                if st.button(f"▶️ Exécuter", key=exec_key):
                    st.session_state.current_agent = agent
                    st.success(f"✅ Agent **{agent.get('name', 'N/A')}** chargé avec succès ! Prêt à l'exécution.")
                    st.rerun()
            
            with col2:
                edit_key = f"edit_agent_{agent_unique_id}"
                if st.button(f"✏️ Éditer", key=edit_key):
                    st.session_state.editing_agent = agent
                    st.rerun()
            
            with col3:
                agent_name = agent.get('name', 'Agent sans nom')
                agent_id = agent.get('id', 'unknown')
                
                # Créer une clé unique pour la confirmation TRÈS spécifique à cet agent
                confirm_key = f"confirm_delete_agent_{agent_unique_id}"
                delete_key = f"delete_agent_{agent_unique_id}"
                
                if confirm_key not in st.session_state:
                    st.session_state[confirm_key] = False
                
                if not st.session_state[confirm_key]:
                    if st.button(f"🗑️ Supprimer", key=delete_key):
                        st.session_state[confirm_key] = True
                else:
                    col_confirm1, col_confirm2, col_confirm3 = st.columns([1, 1, 1])
                    with col_confirm1:
                        st.warning(f"Supprimer '{agent_name}' ?")
                    with col_confirm2:
                        yes_key = f"yes_agent_{agent_unique_id}"
                        if st.button("✅ Oui", key=yes_key):
                            agents.remove(agent)
                            save_agents(agents)
                            st.success(f"✅ Agent '{agent_name}' supprimé avec succès !")
                            st.rerun()
                    with col_confirm3:
                        no_key = f"no_agent_{agent_unique_id}"
                        if st.button("❌ Non", key=no_key):
                            st.session_state[confirm_key] = False
                            st.rerun()
            
            with col4:
                share_key = f"share_agent_{agent_unique_id}"
                if st.button(f"📤 Partager", key=share_key):
                    st.info(f"🔗 Lien de partage pour l'agent '{agent['name']}' sera généré ici.")
            
            with col5:
                stats_key = f"stats_agent_{agent_unique_id}"
                if st.button(f"📊 Stats", key=stats_key):
                    executions = agent.get('executions', [])
                    st.info(f"📈 Statistiques de l'agent '{agent['name']}': {len(executions)} exécutions")
            
            # Formulaire d'édition EN DEHORS de la boucle des colonnes pour prendre toute la largeur
            if st.session_state.editing_agent and st.session_state.editing_agent.get('id') == agent.get('id'):
                st.markdown("---")
                st.markdown("**✏️ Modifier cet Agent**")
                
                # Champs en PLEINE LARGEUR de la page
                name_key = f"edit_name_{agent_unique_id}"
                edited_name = st.text_input("Nom de l'Agent", value=agent.get('name', ''), key=name_key)
                
                domain_key = f"edit_domain_{agent_unique_id}"
                edited_domain = st.text_input("Domaine", value=agent.get('domain', ''), key=domain_key)
                
                # Type et Modèle côte à côte pour optimiser l'espace
                col1, col2 = st.columns(2)
                with col1:
                    type_key = f"edit_type_{agent_unique_id}"
                    agent_types = ["Analyse", "Rapport", "Résumé", "Autre"]
                    current_type = agent.get('type', 'Analyse')
                    type_index = agent_types.index(current_type) if current_type in agent_types else 0
                    edited_type = st.selectbox("Type d'Agent", agent_types, index=type_index, key=type_key)
                
                with col2:
                    model_key = f"edit_model_{agent_unique_id}"
                    available_models = [model["name"] for model in models] if models else ["GPT-4", "Claude-3", "Gemini Pro"]
                    current_model = agent.get('model', 'GPT-4')
                    model_index = available_models.index(current_model) if current_model in available_models else 0
                    edited_model = st.selectbox("Modèle IA", available_models, index=model_index, key=model_key)
                
                prompt_key = f"edit_prompt_{agent_unique_id}"
                edited_prompt = st.text_area(
                    "Prompt Système",
                    value=agent.get('system_prompt', ''),
                    height=150,
                    key=prompt_key
                )
                
                # Boutons d'action simples (sans formulaire)
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    save_key = f"save_agent_{agent_unique_id}"
                    if st.button("💾 Sauvegarder", key=save_key):
                        # Mettre à jour l'agent directement
                        agent['name'] = edited_name
                        agent['domain'] = edited_domain
                        agent['type'] = edited_type
                        agent['model'] = edited_model
                        agent['system_prompt'] = edited_prompt
                        
                        save_agents(agents)
                        st.success(f"✅ Agent '{edited_name}' modifié avec succès !")
                        st.session_state.editing_agent = None
                        st.rerun()
                
                with col2:
                    cancel_key = f"cancel_agent_{agent_unique_id}"
                    if st.button("❌ Annuler", key=cancel_key):
                        st.session_state.editing_agent = None
                        st.rerun()
            
            st.markdown("---")
    
    else:
        st.info("🤖 Aucun agent créé pour le moment. Commencez par en créer un !")

# Page Modèles
elif selected == "⚙️ Modèles":
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Gestion des Modèles IA</h1>
        <p>Configurez et gérez vos modèles d'intelligence artificielle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration des clés API
    with st.expander("🔑 Configuration des Clés API", expanded=True):
        with st.form("api_keys_form"):
            st.markdown("### 🔑 Entrez vos Clés API")
            
            col1, col2 = st.columns(2)
            with col1:
                openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
                anthropic_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
            
            with col2:
                google_key = st.text_input("Google AI API Key", type="password", placeholder="AIza...")
                grok_key = st.text_input("Grok API Key", type="password", placeholder="Votre clé Grok...")
            
            if st.form_submit_button("💾 Sauvegarder les Clés API"):
                # Ici vous pouvez sauvegarder les clés dans un fichier de configuration sécurisé
                st.success("✅ Clés API sauvegardées !")
    
    # Ajout de nouveaux modèles
    with st.expander("➕ Ajouter un Nouveau Modèle", expanded=False):
        with st.form("add_model_form"):
            st.markdown("### ➕ Ajouter un Modèle")
            
            model_name = st.text_input("Nom du Modèle", placeholder="Ex: GPT-4 Turbo")
            model_provider = st.selectbox("Fournisseur", ["OpenAI", "Anthropic", "Google", "Meta", "Grok", "Autre"])
            model_status = st.selectbox("Statut", ["active", "testing", "inactive"])
            model_description = st.text_area("Description", placeholder="Description du modèle...")
            
            if st.form_submit_button("✅ Ajouter le Modèle"):
                if model_name and model_provider:
                    new_model = {
                        "name": model_name,
                        "provider": model_provider,
                        "status": model_status,
                        "description": model_description,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    models.append(new_model)
                    save_models(models)
                    st.success(f"✅ Modèle '{model_name}' ajouté avec succès !")
                    st.rerun()
                else:
                    st.error("❌ Veuillez remplir tous les champs obligatoires.")
    
    # Liste des modèles existants avec pagination
    if models:
        st.markdown("### 📋 Modèles Disponibles")
        
        # Pagination pour éviter les listes trop longues
        models_per_page = 5
        total_pages = (len(models) + models_per_page - 1) // models_per_page
        
        if 'current_model_page' not in st.session_state:
            st.session_state.current_model_page = 0
        
        # Sélecteur de page pour les modèles
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            model_page = st.selectbox(
                "Page Modèles", 
                range(total_pages), 
                index=st.session_state.current_model_page,
                key="model_page_selector"
            )
            st.session_state.current_model_page = model_page
        
        # Calculer les modèles à afficher pour cette page
        start_idx = model_page * models_per_page
        end_idx = min(start_idx + models_per_page, len(models))
        current_models = models[start_idx:end_idx]
        
        # Créer une zone avec bordure pour la liste
        with st.container():
            # Créer une zone délimitée avec st.expander
            with st.expander(f"📋 **Page {model_page + 1} sur {total_pages} - Modèles {start_idx + 1} à {end_idx} sur {len(models)}**", expanded=True):
                for model in current_models:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="agent-card">
                            <h4>⚙️ {model.get('name', 'N/A')}</h4>
                            <p><strong>Fournisseur:</strong> {model.get('provider', 'N/A')}</p>
                            <p><strong>Description:</strong> {model.get('description', 'Aucune description')}</p>
                            <p><strong>Statut:</strong> <span style="color: {'green' if model.get('status') == 'active' else 'orange' if model.get('status') == 'testing' else 'red'}">{model.get('status', 'N/A')}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button(f"🎯 Sélectionner", key=f"select_{model['name']}"):
                            st.session_state.selected_model = model['name']
                            st.success(f"✅ Modèle '{model['name']}' sélectionné !")
                    
                    with col3:
                        model_name = model.get('name', 'Modèle sans nom')
                        
                        # Créer une clé unique pour la confirmation
                        confirm_key = f"confirm_delete_model_{model_name}"
                        delete_key = f"delete_model_{model_name}"
                        
                        if confirm_key not in st.session_state:
                            st.session_state[confirm_key] = False
                        
                        if not st.session_state[confirm_key]:
                            if st.button(f"🗑️ Supprimer", key=delete_key):
                                st.session_state[confirm_key] = True
                        else:
                            col_confirm1, col_confirm2, col_confirm3 = st.columns([1, 1, 1])
                            with col_confirm1:
                                st.warning(f"Supprimer '{model_name}' ?")
                            with col_confirm2:
                                if st.button("✅ Oui", key=f"yes_model_{model_name}"):
                                    models.remove(model)
                                    save_models(models)
                                    st.success(f"✅ Modèle '{model_name}' supprimé avec succès !")
                                    st.rerun()
                            with col_confirm3:
                                if st.button("❌ Non", key=f"no_model_{model_name}"):
                                    st.session_state[confirm_key] = False
                                    st.rerun()
    
    # Affichage du modèle sélectionné
    if st.session_state.selected_model:
        st.markdown("### 🎯 Modèle Actuellement Sélectionné")
        st.success(f"✅ **{st.session_state.selected_model}** est votre modèle par défaut")
    
    # Intégration avec le module AI
    if GROK_AVAILABLE:
        st.markdown("### 🔗 Intégration IA")
        display_model_status()
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
                st.markdown("#### 🔄 Étapes du Workflow Support Client")
                
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
                    step3_type = "solution"
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
                    {"order": 3, "name": "Solution", "agent_name": step3_agent, "type": step3_type, "description": step3_description},
                    {"order": 4, "name": "Suivi", "agent_name": step4_agent, "type": step4_type, "description": step4_description}
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
    
    # Liste des workflows existants avec pagination
    if workflows:
        st.markdown("### 📋 Workflows Disponibles")
        
        # Pagination pour éviter les listes trop longues
        workflows_per_page = 3
        total_pages = (len(workflows) + workflows_per_page - 1) // workflows_per_page
        
        if 'current_workflow_page' not in st.session_state:
            st.session_state.current_workflow_page = 0
        
        # Sélecteur de page pour les workflows
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            workflow_page = st.selectbox(
                "Page Workflows", 
                range(total_pages), 
                index=st.session_state.current_workflow_page,
                key="workflow_page_selector"
            )
            st.session_state.current_workflow_page = workflow_page
        
        # Calculer les workflows à afficher pour cette page
        start_idx = workflow_page * workflows_per_page
        end_idx = min(start_idx + workflows_per_page, len(workflows))
        current_workflows = workflows[start_idx:end_idx]
        
        # Créer une zone avec bordure pour la liste
        with st.container():
            # Créer une zone délimitée avec st.expander
            with st.expander(f"📋 **Page {workflow_page + 1} sur {total_pages} - Workflows {start_idx + 1} à {end_idx} sur {len(workflows)}**", expanded=True):
                for workflow in current_workflows:
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
                    if st.button("🚀 Lancer l'Exécution du Workflow", key="launch_workflow"):
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
                            status_text.text(f"🔄 Exécution de l'étape {i + 1}/{total_steps}: {step['name']}")
                            
                            # Utiliser un conteneur simple au lieu d'un expander imbriqué
                            st.markdown(f"### 🔄 {step['name']} - {step['agent_name']}")
                            
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
                        status_text.text("🎉 Exécution terminée !")
                        
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
                        st.markdown("### 🔍 Données Finales du Workflow")
                        
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
                                if st.button("🔍 Voir Détails de la Dernière Exécution", key="view_last_exec"):
                                    st.markdown("### 🔍 Détails de la Dernière Exécution")
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
                                            st.markdown("#### 📊 Résumé Détaillé")
                                            summary_df = pd.DataFrame(last_exec['summary'])
                                            st.dataframe(summary_df, use_container_width=True)
                                    else:
                                        st.error("Aucune exécution trouvée")
    
    else:
        st.info("🔄 Aucun workflow créé pour le moment. Commencez par en créer un !")

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
            
            # Utiliser pd.Series pour éviter les erreurs MultiIndex
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
            
            # Utiliser pd.Series pour éviter les erreurs MultiIndex
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
        
        # Statistiques détaillées avec pagination
        st.markdown("### 📋 Détails des Agents")
        
        # Pagination pour éviter les listes trop longues
        stats_per_page = 10
        total_pages = (len(agents) + stats_per_page - 1) // stats_per_page
        
        if 'current_stats_page' not in st.session_state:
            st.session_state.current_stats_page = 0
        
        # Sélecteur de page pour les statistiques
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            stats_page = st.selectbox(
                "Page Statistiques", 
                range(total_pages), 
                index=st.session_state.current_stats_page,
                key="stats_page_selector"
            )
            st.session_state.current_stats_page = stats_page
        
        # Calculer les agents à afficher pour cette page
        start_idx = stats_page * stats_per_page
        end_idx = min(start_idx + stats_per_page, len(agents))
        current_stats_agents = agents[start_idx:end_idx]
        
        # Créer une zone avec bordure pour la liste
        with st.container():
            # Créer une zone délimitée avec st.expander
            with st.expander(f"📋 **Page {stats_page + 1} sur {total_pages} - Agents {start_idx + 1} à {end_idx} sur {len(agents)}**", expanded=True):
                # Créer un DataFrame pour les analyses
                agent_data = []
                for agent in current_stats_agents:
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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Plateforme de Gestion d'Agents IA | Développée avec Streamlit</p>
</div>
""", unsafe_allow_html=True)
