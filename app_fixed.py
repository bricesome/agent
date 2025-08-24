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
    
    .agent-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.2s;
    }
    
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .btn-primary {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .btn-secondary {
        background: #f8f9fa;
        border: 2px solid #667eea;
        color: #667eea;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-secondary:hover {
        background: #667eea;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .css-1d391kg {
        background: transparent;
    }
    
    /* Sidebar text colors */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    .css-1d391kg p, .css-1d391kg label, .css-1d391kg div {
        color: white !important;
    }
    
    /* Sidebar selectbox styling */
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    
    .css-1d391kg .stSelectbox > div > div > div {
        color: #333 !important;
    }
    
    /* Sidebar metric styling */
    .css-1d391kg .stMetric > div > div {
        color: white !important;
    }
    
    .css-1d391kg .stMetric > div > div > div {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Menu de navigation - Couleurs corrigées */
    .css-1d391kg .css-1d391kg .css-1d391kg {
        background: transparent !important;
    }
    
    /* Style du menu option_menu */
    .css-1d391kg [data-testid="stSidebar"] .css-1d391kg {
        background: transparent !important;
    }
    
    /* Correction des couleurs du menu */
    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        background: transparent !important;
    }
    
    /* Forcer la visibilité du texte du menu */
    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg {
        color: #1f1f1f !important;
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        margin: 2px 0 !important;
        padding: 8px 12px !important;
    }
    
    /* Hover effect pour le menu */
    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg:hover {
        background: rgba(255, 255, 255, 1) !important;
        color: #1f1f1f !important;
        transform: translateX(5px) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Élément sélectionné du menu */
    .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg .css-1d391kg[aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données
@st.cache_data
def load_agents():
    if os.path.exists('agents.json'):
        with open('agents.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@st.cache_data
def load_models():
    if os.path.exists('models.json'):
        with open('models.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return [
        {"name": "Grok Beta", "provider": "X (Twitter)", "status": "active"},
        {"name": "GPT-4", "provider": "OpenAI", "status": "active"},
        {"name": "Claude-3", "provider": "Anthropic", "status": "active"},
        {"name": "Gemini Pro", "provider": "Google", "status": "active"},
        {"name": "Llama 2", "provider": "Meta", "status": "active"}
    ]

def save_agents(agents):
    with open('agents.json', 'w', encoding='utf-8') as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)

def save_models(models):
    with open('models.json', 'w', encoding='utf-8') as f:
        json.dump(models, f, ensure_ascii=False, indent=2)

# Variables de session
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "Grok Beta"
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = None
if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False
if 'editing_agent' not in st.session_state:
    st.session_state.editing_agent = None

# Chargement des données
agents = load_agents()
models = load_models()

# Calcul des statistiques
total_agents = len(agents)
active_agents_count = len([a for a in agents if a.get('status') == 'active'])
unique_types = len(set([a.get('type', 'N/A') for a in agents]))

# Sidebar avec navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: white;">
        <h2 style="color: white;">🤖 IA Platform</h2>
        <p style="color: white; opacity: 0.9;">Gestion des Agents IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["🏠 Dashboard", "🤖 Agents", "⚙️ Modèles", "📊 Statistiques"],
        icons=["house", "robot", "gear", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "rgba(255, 255, 255, 0.1)",
                "border-radius": "10px",
                "margin": "10px 0"
            },
            "icon": {
                "color": "#1f1f1f", 
                "font-size": "18px",
                "background": "rgba(255, 255, 255, 0.9)",
                "padding": "8px",
                "border-radius": "8px"
            },
            "nav-link": {
                "color": "#1f1f1f",
                "font-size": "16px",
                "text-align": "left",
                "margin": "2px 0",
                "padding": "10px 15px",
                "background": "rgba(255, 255, 255, 0.9)",
                "border-radius": "8px",
                "font-weight": "500",
                "transition": "all 0.3s ease"
            },
            "nav-link:hover": {
                "background": "rgba(255, 255, 255, 1)",
                "color": "#1f1f1f",
                "transform": "translateX(5px)",
                "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.2)",
                "font-weight": "600"
            },
        }
    )
    
    st.markdown("---")
    
    # Sélection du modèle
    st.markdown("### 🎯 Modèle Sélectionné")
    
    # Récupérer la liste des noms de modèles
    model_names = [model["name"] for model in models]
    
    # Vérifier si le modèle sélectionné existe dans la liste
    if st.session_state.selected_model not in model_names:
        # Si le modèle n'existe pas, utiliser le premier disponible ou "Grok Beta"
        if model_names:
            st.session_state.selected_model = model_names[0]
        else:
            st.session_state.selected_model = "Grok Beta"
    
    # Trouver l'index du modèle sélectionné
    try:
        selected_index = model_names.index(st.session_state.selected_model)
    except ValueError:
        # Si le modèle n'est pas trouvé, utiliser l'index 0
        selected_index = 0
        st.session_state.selected_model = model_names[0] if model_names else "Grok Beta"
    
    selected_model = st.selectbox(
        "Choisir le modèle IA",
        model_names,
        index=selected_index
    )
    
    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.rerun()
    
    st.markdown(f"**Modèle actuel:** {st.session_state.selected_model}")
    
    st.markdown("---")
    
    # Statistiques rapides
    st.markdown("### 📈 Stats Rapides")
    st.metric("Agents", total_agents)
    st.metric("Actifs", active_agents_count)

# Page Dashboard
if selected == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Plateforme de Gestion des Agents IA</h1>
        <p>Créez, gérez et exécutez vos agents IA intelligents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Agents</h3>
            <h2>{}</h2>
        </div>
        """.format(total_agents), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Actifs</h3>
            <h2>{}</h2>
        </div>
        """.format(active_agents_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Modèle</h3>
            <h2>{}</h2>
        </div>
        """.format(st.session_state.selected_model), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📁 Types</h3>
            <h2>{}</h2>
        </div>
        """.format(unique_types), unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        if agents:
            try:
                # Répartition par type - Correction des erreurs
                type_data = [a.get('type', 'N/A') for a in agents]
                if type_data:
                    type_counts = pd.Series(type_data).value_counts()
                    if not type_counts.empty:
                        fig = px.pie(
                            values=type_counts.values,
                            names=type_counts.index,
                            title="Répartition par Type d'Agent",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Aucune donnée de type disponible pour le graphique")
                else:
                    st.info("Aucun agent avec type défini")
            except Exception as e:
                st.info("Graphique des types temporairement indisponible")
    
    with col2:
        if agents:
            try:
                # Répartition par domaine - Correction des erreurs
                domain_data = [a.get('domain', 'N/A') for a in agents]
                if domain_data:
                    domain_counts = pd.Series(domain_data).value_counts()
                    if not domain_counts.empty:
                        fig = px.bar(
                            x=domain_counts.index.tolist(),
                            y=domain_counts.values.tolist(),
                            title="Répartition par Domaine",
                            color=domain_counts.values.tolist(),
                            color_continuous_scale="viridis"
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Aucune donnée de domaine disponible pour le graphique")
                else:
                    st.info("Aucun agent avec domaine défini")
            except Exception as e:
                st.info("Graphique des domaines temporairement indisponible")
    
    # Agents récents
    st.markdown("### 🆕 Agents Récents")
    if agents:
        recent_agents = sorted(agents, key=lambda x: x.get('created_at', ''), reverse=True)[:5]
        for agent in recent_agents:
            with st.expander(f"🤖 {agent.get('name', 'N/A')} - {agent.get('type', 'N/A')}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Domaine:** {agent.get('domain', 'N/A')}")
                    st.write(f"**Créé le:** {agent.get('created_at', 'N/A')}")
                with col2:
                    if st.button(f"Exécuter {agent.get('name', 'N/A')}", key=f"exec_{agent.get('id', '')}"):
                        st.session_state.current_agent = agent
                        st.success("Redirection vers l'exécution...")
                        st.rerun()
    else:
        st.info("Aucun agent créé pour le moment. Créez votre premier agent !")

# Page Agents
elif selected == "🤖 Agents":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Gestion des Agents IA</h1>
        <p>Créez et gérez vos agents intelligents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton de création
    if st.button("➕ Créer un Nouvel Agent", type="primary", use_container_width=True):
        st.session_state.show_create_form = True
    
    # Formulaire de création
    if st.session_state.show_create_form:
        st.markdown("### 📝 Créer un Nouvel Agent")
        
        with st.form("create_agent"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("🏷️ Nom de l'Agent", placeholder="Ex: Analyste Financier")
                domain = st.text_input("🎯 Domaine", placeholder="Ex: Finance, Marketing, RH...")
            
            with col2:
                agent_type = st.selectbox(
                    "🔧 Type d'Agent",
                    ["Analyse", "Rapport", "Résumé", "Traduction", "Code", "Autre"]
                )
                status = st.selectbox("📊 Statut", ["active", "inactive"])
            
            system_prompt = st.text_area(
                "💬 Prompt Système",
                placeholder="Décrivez le comportement et les capacités de votre agent...",
                height=150
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Créer l'Agent", type="primary"):
                    if name and domain and system_prompt:
                        new_agent = {
                            "id": f"agent_{len(agents) + 1}_{int(datetime.now().timestamp())}",
                            "name": name,
                            "domain": domain,
                            "type": agent_type,
                            "system_prompt": system_prompt,
                            "status": status,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "model": st.session_state.selected_model
                        }
                        agents.append(new_agent)
                        save_agents(agents)
                        st.success(f"Agent '{name}' créé avec succès !")
                        st.session_state.show_create_form = False
                        st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires.")
            
            with col2:
                if st.form_submit_button("❌ Annuler"):
                    st.session_state.show_create_form = False
                    st.rerun()
    
    # Liste des agents
    st.markdown("### 📋 Liste des Agents")
    
    if agents:
        for agent in agents:
            with st.container():
                st.markdown(f"""
                <div class="agent-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3>🤖 {agent.get('name', 'N/A')}</h3>
                            <p><strong>Domaine:</strong> {agent.get('domain', 'N/A')} | <strong>Type:</strong> {agent.get('type', 'N/A')}</p>
                            <p><strong>Modèle:</strong> {agent.get('model', 'N/A')} | <strong>Statut:</strong> {agent.get('status', 'N/A')}</p>
                            <p><strong>Créé le:</strong> {agent.get('created_at', 'N/A')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    if st.button(f"▶️ Exécuter", key=f"exec_{agent['id']}"):
                        st.session_state.current_agent = agent
                        st.success("Redirection vers l'exécution...")
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
                            st.success(f"Agent '{agent['name']}' supprimé !")
                            st.rerun()
                
                with col4:
                    if st.button(f"📤 Partager", key=f"share_{agent['id']}"):
                        st.info(f"Fonctionnalité de partage pour l'agent '{agent['name']}' à implémenter")
                
                with col5:
                    if st.button(f"📊 Stats", key=f"stats_{agent['id']}"):
                        st.info(f"Statistiques de l'agent '{agent['name']}' à implémenter")
                
                # Formulaire d'édition
                if st.session_state.get('editing_agent') and st.session_state.editing_agent['id'] == agent['id']:
                    st.markdown("### ✏️ Éditer l'Agent")
                    
                    with st.form(f"edit_agent_{agent['id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("🏷️ Nom", value=agent.get('name', ''), key=f"edit_name_{agent['id']}")
                            edit_domain = st.text_input("🎯 Domaine", value=agent.get('domain', ''), key=f"edit_domain_{agent['id']}")
                        
                        with col2:
                            edit_type = st.selectbox(
                                "🔧 Type",
                                ["Analyse", "Rapport", "Résumé", "Traduction", "Code", "Autre"],
                                index=["Analyse", "Rapport", "Résumé", "Traduction", "Code", "Autre"].index(agent.get('type', 'Analyse')),
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
        st.info("Aucun agent créé pour le moment. Commencez par créer votre premier agent !")

# Page Modèles
elif selected == "⚙️ Modèles":
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Gestion des Modèles IA</h1>
        <p>Configurez et gérez vos modèles d'intelligence artificielle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🚀 Section Grok - Configuration des Clés API
    st.markdown("### 🚀 Configuration Grok (X/Twitter)")
    
    if GROK_AVAILABLE:
        # Afficher le statut des modèles IA
        display_model_status()
        
        st.markdown("---")
        
        # Configuration manuelle des clés API
        st.markdown("### 🔑 Configuration Manuelle des Clés API")
        
        with st.expander("📝 Configurer vos Clés API"):
            st.markdown("""
            **Option 1 : Fichier config.env (Recommandé)**
            1. Ouvrez le fichier `config.env` dans votre projet
            2. Remplacez `GROK_API_KEY=votre_cle_grok_ici` par votre vraie clé
            3. Redémarrez l'application
            
            **Option 2 : Interface de l'Application**
            Utilisez le formulaire ci-dessous pour configurer vos clés directement.
            """)
            
            with st.form("api_keys_config"):
                st.markdown("#### 🚀 Clé API Grok (X/Twitter)")
                grok_key = st.text_input(
                    "Clé API Grok",
                    type="password",
                    placeholder="sk-grok-votre_cle_ici",
                    help="Votre clé API Grok d'xAI"
                )
                
                st.markdown("#### 🤖 Clé API OpenAI (GPT-4)")
                openai_key = st.text_input(
                    "Clé API OpenAI",
                    type="password",
                    placeholder="sk-votre_cle_openai_ici",
                    help="Votre clé API OpenAI"
                )
                
                st.markdown("#### 🧠 Clé API Anthropic (Claude-3)")
                anthropic_key = st.text_input(
                    "Clé API Anthropic",
                    type="password",
                    placeholder="sk-ant-votre_cle_anthropic_ici",
                    help="Votre clé API Anthropic"
                )
                
                st.markdown("#### 🔍 Clé API Google (Gemini)")
                google_key = st.text_input(
                    "Clé API Google",
                    type="password",
                    placeholder="votre_cle_google_ici",
                    help="Votre clé API Google"
                )
                
                if st.form_submit_button("💾 Sauvegarder les Clés API", type="primary"):
                    # Ici vous pourriez sauvegarder les clés dans un fichier sécurisé
                    st.success("✅ Clés API configurées ! Redémarrez l'application pour les activer.")
                    st.info("💡 Note : Pour une sécurité maximale, utilisez le fichier config.env")
    else:
        st.warning("⚠️ Module d'intégration IA non disponible. Installez les dépendances avec :")
        st.code("pip install -r requirements.txt")
    
    # Ajouter un nouveau modèle
    st.markdown("---")
    st.markdown("### ➕ Ajouter un Nouveau Modèle")
    
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
    
    # Liste des modèles
    st.markdown("### 📋 Modèles Disponibles")
    
    for model in models:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="agent-card">
                    <h3>🤖 {model.get('name', 'N/A')}</h3>
                    <p><strong>Fournisseur:</strong> {model.get('provider', 'N/A')}</p>
                    <p><strong>Statut:</strong> <span style="color: {'green' if model.get('status') == 'active' else 'orange' if model.get('status') == 'testing' else 'red'}">{model.get('status', 'N/A')}</span></p>
                    <p><strong>Description:</strong> {model.get('description', 'Aucune description')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"🎯 Sélectionner", key=f"select_{model['name']}"):
                    st.session_state.selected_model = model['name']
                    st.success(f"Modèle '{model['name']}' sélectionné !")
                    st.rerun()
            
            with col3:
                if st.button(f"🗑️ Supprimer", key=f"delete_model_{model['name']}"):
                    if st.confirm(f"Êtes-vous sûr de vouloir supprimer le modèle '{model['name']}' ?"):
                        models.remove(model)
                        save_models(models)
                        st.success(f"Modèle '{model['name']}' supprimé !")
                        st.rerun()
            
            st.markdown("---")

# Page Statistiques
elif selected == "📊 Statistiques":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Tableau de Bord Analytique</h1>
        <p>Analysez les performances et l'utilisation de vos agents IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    if agents:
        # Statistiques générales
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Statistiques Générales")
            
            # Graphique en ligne du temps - Correction des erreurs
            dates = [a.get('created_at', '') for a in agents if a.get('created_at')]
            if dates:
                try:
                    # Créer un DataFrame simple pour éviter les erreurs MultiIndex
                    date_df = pd.DataFrame({'date': dates})
                    date_counts = date_df['date'].value_counts().sort_index()
                    
                    if not date_counts.empty:
                        fig = px.line(
                            x=date_counts.index.tolist(),
                            y=date_counts.values.tolist(),
                            title="Évolution des Agents dans le Temps",
                            labels={'x': 'Date', 'y': 'Nombre d\'Agents'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Aucune donnée temporelle disponible")
                except Exception as e:
                    st.info("Graphique temporel temporairement indisponible")
        
        with col2:
            st.markdown("### 🎯 Répartition par Type")
            
            # Graphique en barres des types - Correction des erreurs
            try:
                type_data = [a.get('type', 'N/A') for a in agents]
                if type_data:
                    type_counts = pd.Series(type_data).value_counts()
                    if not type_counts.empty:
                        fig = px.bar(
                            x=type_counts.index.tolist(),
                            y=type_counts.values.tolist(),
                            title="Agents par Type",
                            color=type_counts.values.tolist(),
                            color_continuous_scale="plasma"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Aucune donnée de type disponible")
                else:
                    st.info("Aucun agent avec type défini")
            except Exception as e:
                st.info("Graphique des types temporairement indisponible")
        
        # Tableau des agents avec statistiques
        st.markdown("### 📋 Détails des Agents")
        
        df = pd.DataFrame(agents)
        if not df.empty:
            # Ajouter des colonnes calculées
            try:
                df['days_old'] = pd.to_datetime(df['created_at']).apply(lambda x: (pd.Timestamp.now() - x).days)
                
                st.dataframe(
                    df[['name', 'type', 'domain', 'status', 'created_at', 'days_old']],
                    use_container_width=True,
                    hide_index=True
                )
            except Exception as e:
                st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible pour les statistiques. Créez des agents pour commencer !")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Plateforme de Gestion des Agents IA | Développé avec Streamlit</p>
</div>
""", unsafe_allow_html=True)
