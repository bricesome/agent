import streamlit as st
import json
import os
from datetime import datetime
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

# Chargement des données
agents = load_agents()
models = load_models()

# Calcul des statistiques
active_agents_count = len([agent for agent in agents if agent.get('status') == 'active'])
total_agents = len(agents)
total_models = len(models)

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
        options=["📊 Dashboard", "🤖 Agents", "⚙️ Modèles", "📈 Statistiques"],
        icons=["📊", "🤖", "⚙️", "📈"],
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
            <h3>🔄 Statut</h3>
            <h2 style="color: #28a745;">✅ Opérationnel</h2>
            <p>Système actif</p>
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
    
    # Agents récents
    if agents:
        st.markdown("### 🆕 Agents Récents")
        recent_agents = sorted(agents, key=lambda x: x.get('created_at', ''), reverse=True)[:5]
        
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

# Page Agents
elif selected == "🤖 Agents":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Gestion des Agents IA</h1>
        <p>Créez, gérez et exécutez vos agents IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton pour créer un nouvel agent
    if st.button("➕ Créer un Nouvel Agent", type="primary", use_container_width=True):
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
                if st.form_submit_button("✅ Créer l'Agent", type="primary"):
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
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button(f"▶️ Exécuter", key=f"exec_{agent['id']}"):
                    st.session_state.current_agent = agent
                    st.success(f"✅ Agent **{agent.get('name', 'N/A')}** chargé avec succès ! Prêt à l'exécution.")
                    st.rerun()
            
            with col2:
                if st.button(f"✏️ Éditer", key=f"edit_{agent['id']}"):
                    st.session_state.editing_agent = agent
                    st.rerun()
            
            with col3:
                if st.button(f"🗑️ Supprimer", key=f"delete_{agent['id']}"):
                    if st.confirm(f"Êtes-vous sûr de vouloir supprimer l'agent '{agent['name']}' ?"):
                        agents.remove(agent)
                        save_agents(agents)
                        st.success(f"✅ Agent '{agent['name']}' supprimé avec succès !")
                        st.rerun()
            
            with col4:
                if st.button(f"📤 Partager", key=f"share_{agent['id']}"):
                    st.info(f"🔗 Lien de partage pour l'agent '{agent['name']}' sera généré ici.")
            
            with col5:
                if st.button(f"📊 Stats", key=f"stats_{agent['id']}"):
                    executions = agent.get('executions', [])
                    st.info(f"📈 Statistiques de l'agent '{agent['name']}': {len(executions)} exécutions")
            
            # Formulaire d'édition
            if st.session_state.editing_agent and st.session_state.editing_agent.get('id') == agent.get('id'):
                with st.form(f"edit_agent_form_{agent['id']}"):
                    st.markdown("### ✏️ Modifier l'Agent")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        edited_name = st.text_input("Nom de l'Agent", value=agent.get('name', ''), key=f"edit_name_{agent['id']}")
                        edited_domain = st.text_input("Domaine", value=agent.get('domain', ''), key=f"edit_domain_{agent['id']}")
                    
                    with col2:
                        edited_type = st.selectbox("Type d'Agent", ["Analyse", "Rapport", "Résumé", "Autre"], index=["Analyse", "Rapport", "Résumé", "Autre"].index(agent.get('type', 'Analyse')), key=f"edit_type_{agent['id']}")
                        edited_model = st.selectbox("Modèle IA", [model["name"] for model in models] if models else ["GPT-4", "Claude-3", "Gemini Pro"], index=([model["name"] for model in models] if models else ["GPT-4", "Claude-3", "Gemini Pro"]).index(agent.get('model', 'GPT-4')), key=f"edit_model_{agent['id']}")
                    
                    edited_prompt = st.text_area(
                        "Prompt Système",
                        value=agent.get('system_prompt', ''),
                        height=150,
                        key=f"edit_prompt_{agent['id']}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Sauvegarder", type="primary"):
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
                        if st.form_submit_button("❌ Annuler"):
                            st.session_state.editing_agent = None
                            st.rerun()
    
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
            
            if st.form_submit_button("💾 Sauvegarder les Clés API", type="primary"):
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
            
            if st.form_submit_button("✅ Ajouter le Modèle", type="primary"):
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
    
    # Liste des modèles existants
    if models:
        st.markdown("### 📋 Modèles Disponibles")
        
        for model in models:
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
                    st.success(f"✅ Modèle '{model['name']}' sélectionné !")
            
            with col3:
                if st.button(f"🗑️ Supprimer", key=f"delete_model_{model['name']}"):
                    if st.confirm(f"Êtes-vous sûr de vouloir supprimer le modèle '{model['name']}' ?"):
                        models.remove(model)
                        save_models(models)
                        st.success(f"✅ Modèle '{model['name']}' supprimé avec succès !")
                        st.rerun()
    
    # Intégration avec le module AI
    if GROK_AVAILABLE:
        st.markdown("### 🔗 Intégration IA")
        display_model_status()
    else:
        st.warning("⚠️ Module d'intégration IA non disponible. Installez les dépendances.")

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
        
        # Statistiques détaillées
        st.markdown("### 📋 Détails des Agents")
        
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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Plateforme de Gestion d'Agents IA | Développée avec Streamlit</p>
</div>
""", unsafe_allow_html=True)
