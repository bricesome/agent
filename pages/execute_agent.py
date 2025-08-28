import streamlit as st
import json
import os
from datetime import datetime
import PyPDF2
from docx import Document
import io
import base64
from agents.email_agent import email_agent
import time

current_agent = st.session_state.current_agent

# Configuration de la page
st.set_page_config(
    page_title="🚀 Exécuter Agent IA",
    page_icon="🚀",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .execution-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .agent-info-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .file-upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        margin: 1rem 0;
        transition: all 0.3s;
    }
    
    .file-upload-area:hover {
        border-color: #764ba2;
        background: #e9ecef;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #28a745;
    }
    
    .btn-execute {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        border: none;
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .btn-execute:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
    }
    
    .btn-back {
        background: #6c757d;
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-back:hover {
        background: #5a6268;
    }
</style>
""", unsafe_allow_html=True)


# Fonctions utilitaires
def load_agents():
    if os.path.exists('agents.json'):
        with open('agents.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_agents(agents):
    with open('agents.json', 'w', encoding='utf-8') as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)


def extract_text_from_pdf(pdf_file):
    """Extrait le texte d'un fichier PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Erreur lors de la lecture du PDF: {str(e)}")
        return None


def extract_text_from_docx(docx_file):
    """Extrait le texte d'un fichier Word"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier Word: {str(e)}")
        return None


def simulate_ai_processing(agent, content, user_prompt):
    """Simule le traitement IA (remplacez par votre vraie API)"""


    # Simulation du traitement
    with st.spinner("🤖 L'agent IA traite votre demande..."):
        time.sleep(2)  # Simulation du délai de traitement

    # Génération d'une réponse simulée basée sur le type d'agent
    agent_type = agent.get('type', 'Analyse')

    if agent_type == "Analyse":
        response = f"""
        ## 📊 Analyse Générée par {agent.get('name')}

        ### 🔍 Résumé du Contenu
        {content[:200]}...

        ### 💡 Points Clés Identifiés
        - Point important 1
        - Point important 2
        - Point important 3

        ### 📈 Observations
        L'analyse révèle plusieurs éléments intéressants qui méritent une attention particulière.
                """

    elif agent_type == "Rapport":
        response = f"""
        ## 📋 Rapport Généré par {agent.get('name')}
        
        ### 📊 Données Analysées
        {content[:200]}...
        
        ### 📈 Résultats
        - Résultat 1: [Description]
        - Résultat 2: [Description]
        - Résultat 3: [Description]

        ### 📝 Conclusion
        Ce rapport présente une vue d'ensemble complète des informations analysées.
                """

    elif agent_type == "Résumé":
        response = f"""
        ## 📝 Résumé Généré par {agent.get('name')}
        
        ### 🎯 Contenu Principal
        {content[:300]}...
        
        ### 🔑 Points Essentiels
        1. **Point clé 1**: [Description]
        2. **Point clé 2**: [Description]
        3. **Point clé 3**: [Description]
        
        ### 📊 Synthèse
        Résumé concis des informations principales extraites du document.
                """

    else:
        response = f"""
        ## 🤖 Traitement Effectué par {agent.get('name')}
        
        ### 📄 Contenu Traité
        {content[:200]}...
        
        ### 🎯 Demande Utilisateur
        {user_prompt}
        
        ### ✅ Résultat
        Traitement terminé avec succès selon les spécifications de l'agent.
                """

        return response


# Vérification de l'agent sélectionné
if 'current_agent' not in st.session_state or not st.session_state.current_agent:
    st.error("❌ Aucun agent sélectionné. Veuillez retourner à la page principale.")
    if st.button("🏠 Retour au Dashboard"):
        st.rerun()
    st.stop()



# En-tête de la page
st.markdown(f"""
<div class="execution-header">
    <h1>🚀 Exécuter l'Agent IA</h1>
    <p>Agent: <strong>{current_agent.get('name', 'N/A')}</strong> | Type: <strong>{current_agent.get('type', 'N/A')}</strong></p>
</div>
""", unsafe_allow_html=True)

# Bouton de retour
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Retour au Dashboard", use_container_width=True):
        st.rerun()

# Informations sur l'agent
st.markdown("### 📋 Informations de l'Agent")
st.markdown(f"""
<div class="agent-info-card">
    <h4>🤖 {current_agent.get('name', 'N/A')}</h4>
    <p><strong>Domaine:</strong> {current_agent.get('domain', 'N/A')}</p>
    <p><strong>Type:</strong> {current_agent.get('type', 'N/A')}</p>
    <p><strong>Modèle IA:</strong> {current_agent.get('model', 'N/A')}</p>
</div>
""", unsafe_allow_html=True)

# Section d'exécution
st.markdown("### 🚀 Exécution de l'Agent")

# Sélection du type de contenu
content_type = st.radio(
    "Choisissez le type de contenu à traiter:",
    ["📝 Texte direct", "📄 Fichier PDF", "📘 Fichier Word", "🔗 URL/Lien"],
    horizontal=True
)

content = ""
file_uploaded = False

if content_type == "📝 Texte direct":
    content = st.text_area(
        "Entrez le texte à analyser:",
        placeholder="Collez ici le texte que vous souhaitez faire traiter par l'agent IA...",
        height=200
    )
    file_uploaded = bool(content.strip())
    #return content

elif content_type == "📄 Fichier PDF":
    st.markdown("""
    <div class="file-upload-area">
        <h4>📄 Téléchargez votre fichier PDF</h4>
        <p>Formats acceptés: PDF</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choisir un fichier PDF",
        type=['pdf'],
        key="pdf_uploader"
    )

    if uploaded_file is not None:
        file_uploaded = True
        content = extract_text_from_pdf(uploaded_file)
        if content:
            st.success(f"✅ Fichier PDF chargé: {uploaded_file.name}")

elif content_type == "📘 Fichier Word":
    st.markdown("""
    <div class="file-upload-area">
        <h4>📘 Téléchargez votre fichier Word</h4>
        <p>Formats acceptés: DOCX</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choisir un fichier Word",
        type=['docx'],
        key="docx_uploader"
    )

    if uploaded_file is not None:
        file_uploaded = True
        content = extract_text_from_docx(uploaded_file)
        if content:
            st.success(f"✅ Fichier Word chargé: {uploaded_file.name}")


elif content_type == "🔗 URL/Lien":
    url = st.text_input("Entrez l'URL à analyser:", placeholder="https://...")
    if url:
        st.info("⚠️ La fonctionnalité d'analyse d'URL sera implémentée dans une version future.")
        content = f"URL à analyser: {url}"
        file_uploaded = True

# Instructions supplémentaires
user_prompt = st.text_area(
    "💬 Instructions supplémentaires (optionnel):",
    placeholder="Ajoutez des instructions spécifiques pour l'agent...",
    height=100
)

# Bouton d'exécution
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(
            "🚀 Exécuter l'Agent IA",
            type="primary",
            use_container_width=True,
            disabled=not file_uploaded
    ):
        if content:
            # Exécution de l'agent
            result = simulate_ai_processing(current_agent, content, user_prompt)

            # Affichage du résultat
            st.markdown("### 🎯 Résultat du Traitement")
            st.markdown(f"""
            <div class="result-card">
                {result}
            </div>
            """, unsafe_allow_html=True)

            # Options de téléchargement
            st.markdown("### 💾 Télécharger le Résultat")
            col1, col2 = st.columns(2)

            with col1:
                # Téléchargement en format texte
                st.download_button(
                    label="📄 Télécharger en TXT",
                    data=result,
                    file_name=f"resultat_{current_agent.get('name', 'agent')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

            with col2:
                # Téléchargement en format Markdown
                st.download_button(
                    label="📝 Télécharger en MD",
                    data=result,
                    file_name=f"resultat_{current_agent.get('name', 'agent')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )

            # Envoi par email via l'agent email
            st.markdown("### 📧 Envoyer par Email")
            with st.form("send_email_form"):
                recipients_str = st.text_input("Destinataires (emails séparés par des virgules)")
                subject = st.text_input("Sujet", value=f"Résultat - {current_agent.get('name', 'Agent')}")
                submit_email = st.form_submit_button("📤 Envoyer le Résultat par Email")
                if submit_email:
                    recipients = [e.strip() for e in recipients_str.split(",") if e.strip()]
                    if not recipients:
                        st.error("Veuillez saisir au moins un destinataire valide.")
                    else:
                        # user_id pourrait venir de la session/auth; on fallback sur 'local_user'
                        user_id = str(st.session_state.get('user_id', 'local_user'))
                        send_res = email_agent.send_agent_result(
                            user_id=user_id,
                            agent_name=current_agent.get('name', 'Agent'),
                            result=result,
                            recipients=recipients
                        )
                        if send_res.get("success"):
                            st.success(send_res.get("message", "Email envoyé."))
                        else:
                            st.error(send_res.get("error",
                                                  "Échec d'envoi. Configurez votre email dans la page Modèles/Configuration."))

            # Historique des exécutions
            if 'execution_history' not in st.session_state:
                st.session_state.execution_history = []

            execution_record = {
                "agent_id": current_agent.get('id'),
                "agent_name": current_agent.get('name'),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content_type": content_type,
                "content_length": len(content),
                "user_prompt": user_prompt
            }

            st.session_state.execution_history.append(execution_record)

            # Sauvegarde dans le fichier des agents
            agents = load_agents()
            for agent in agents:
                if agent.get('id') == current_agent.get('id'):
                    if 'executions' not in agent:
                        agent['executions'] = []
                    agent['executions'].append(execution_record)
                    break

            save_agents(agents)

            st.success("✅ Exécution terminée avec succès !")
        else:
            st.error("❌ Veuillez fournir du contenu à traiter.")

# Affichage de l'historique des exécutions
if 'execution_history' in st.session_state and st.session_state.execution_history:
    st.markdown("### 📚 Historique des Exécutions")

    for record in st.session_state.execution_history[-5:]:  # Afficher les 5 dernières
        with st.expander(f"🕒 {record['timestamp']} - {record['agent_name']}"):
            st.write(f"**Type de contenu:** {record['content_type']}")
            st.write(f"**Taille du contenu:** {record['content_length']} caractères")
            if record['user_prompt']:
                st.write(f"**Instructions:** {record['user_prompt']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 Exécution d'Agent IA | {}</p>
</div>
""".format(current_agent.get('name', 'Agent')), unsafe_allow_html=True)
