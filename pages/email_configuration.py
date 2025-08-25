import streamlit as st
from agents.email_agent import email_agent

st.set_page_config(page_title="📧 Configuration Email", page_icon="📧", layout="wide")

if not st.session_state.get('authenticated', False):
    st.error("🔐 Accès restreint. Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.markdown("""
### 📧 Configuration Email Utilisateur
Chaque utilisateur doit configurer son propre SMTP pour envoyer des emails (inspiration n8n: flux orientés utilisateur `https://app.n8n.cloud/`).
""")

user_id = str(st.session_state.get('user_id', 'local_user'))

with st.form("email_config_form"):
    st.subheader("Paramètres SMTP")
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
        cfg = {
            "smtp_server": smtp_server,
            "smtp_port": int(smtp_port),
            "email": email_addr,
            "password": password,
            "use_tls": bool(use_tls)
        }
        res = email_agent.configure_user_email(user_id, cfg)
        if res.get("success"):
            st.success("Configuration enregistrée et testée avec succès.")
        else:
            st.error(res.get("error", "Erreur de configuration"))

st.markdown("---")

st.subheader("📊 Statut & Test")
cfg = email_agent.get_user_config(user_id)
if cfg:
    st.json({k: ("******" if k == "password" else v) for k, v in cfg.items()})
    if st.button("🔌 Re-tester la connexion"):
        test = email_agent.test_user_config(user_id)
        if test.get("success"):
            st.success(test.get("message", "OK"))
        else:
            st.error(test.get("error", "Échec"))
else:
    st.info("Aucune configuration trouvée pour cet utilisateur.")


