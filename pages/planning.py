import streamlit as st
from agents.planner_agent import planner_agent
from datetime import datetime

st.set_page_config(page_title="📆 Planification des Tâches", page_icon="📆", layout="wide")

if not st.session_state.get('authenticated', False):
    st.error("🔐 Accès restreint. Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.markdown("""
### 📆 Planification des Tâches
Planifiez l'exécution d'actions: exécuter un agent, lancer un workflow, envoyer des emails, etc. Options: date/heure précise, récurrence (journalière, hebdo, week-end), saison, ou conditionnel (événement).
""")

with st.expander("➕ Planifier une nouvelle tâche", expanded=True):
    with st.form("plan_task_form"):
        name = st.text_input("Nom de la tâche", placeholder="Ex: Rapport du samedi")
        description = st.text_area("Description", placeholder="Détails…")
        task_type = st.selectbox("Type d'action", [
            "agent_execution", "workflow_execution", "email_send", "file_operation", "custom_action"
        ])
        schedule_type = st.selectbox("Type de planification", [
            "datetime", "recurring", "seasonal", "conditional"
        ])

        schedule_config = {}
        if schedule_type == "datetime":
            col_dt1, col_dt2 = st.columns(2)
            with col_dt1:
                date_val = st.date_input("Date d'exécution")
            with col_dt2:
                time_val = st.time_input("Heure d'exécution")
            if date_val and time_val:
                schedule_config["datetime"] = datetime.combine(date_val, time_val).isoformat()
        elif schedule_type == "recurring":
            frequency = st.selectbox("Fréquence", ["daily", "weekly", "monthly", "weekend"])
            schedule_config["frequency"] = frequency
            if frequency in ("daily", "weekly", "weekend"):
                schedule_config["time"] = st.time_input("Heure").strftime("%H:%M")
            if frequency == "weekly":
                schedule_config["day"] = st.selectbox("Jour", [
                    "monday","tuesday","wednesday","thursday","friday","saturday","sunday"
                ])
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
                colA, colB = st.columns(2)
                with colA:
                    after = st.text_input("Après (HH:MM)", placeholder="08:00")
                with colB:
                    before = st.text_input("Avant (HH:MM)", placeholder="18:00")
                condition["time_condition"] = {"after": after, "before": before}
            schedule_config["condition"] = condition

        target = {}
        if task_type == "agent_execution":
            target["agent_name"] = st.text_input("Nom de l'agent à exécuter")
        elif task_type == "workflow_execution":
            target["workflow_name"] = st.text_input("Nom du workflow à exécuter")
        elif task_type == "email_send":
            target["recipients"] = [e.strip() for e in st.text_input("Destinataires (emails)").split(",") if e.strip()]
            target["subject"] = st.text_input("Sujet")
        elif task_type == "file_operation":
            target["operation"] = st.text_input("Opération (copy/move/etc.)")
            target["file_path"] = st.text_input("Chemin du fichier")
        elif task_type == "custom_action":
            target["action"] = st.text_input("Action personnalisée")

        max_exec = st.number_input("Nombre max d'exécutions (-1 illimité)", value=-1)

        submitted = st.form_submit_button("📅 Planifier")
        if submitted:
            payload = {
                "name": name,
                "description": description,
                "type": task_type,
                "schedule_type": schedule_type,
                "schedule_config": schedule_config,
                "target": target,
                "max_executions": int(max_exec)
            }
            res = planner_agent.plan_task(payload)
            if res.get("success"):
                st.success(res.get("message", "Tâche planifiée"))
            else:
                st.error(res.get("error", "Erreur"))

st.markdown("---")
st.subheader("🗂️ Tâches planifiées")
tasks = planner_agent.get_tasks()
if tasks:
    for t in tasks:
        with st.expander(f"{t['name']} — {t['status']} — Prochaine: {t.get('next_execution','-')}"):
            st.json(t)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("▶️ Activer", key=f"enable_{t['id']}"):
                    planner_agent.enable_task(t['id'])
                    st.experimental_rerun()
            with col2:
                if st.button("⏸️ Désactiver", key=f"disable_{t['id']}"):
                    planner_agent.disable_task(t['id'])
                    st.experimental_rerun()
            with col3:
                if st.button("🗑️ Supprimer", key=f"delete_{t['id']}"):
                    planner_agent.delete_task(t['id'])
                    st.experimental_rerun()
else:
    st.info("Aucune tâche planifiée pour le moment.")


