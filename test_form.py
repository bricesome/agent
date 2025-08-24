#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test simple pour vérifier que le formulaire fonctionne
"""

import streamlit as st

def test_simple_form():
    st.title("🧪 Test de Formulaire Simple")
    
    with st.form("test_form"):
        st.text_input("Nom", value="Test")
        st.text_input("Email", value="test@example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted_save = st.form_submit_button("💾 Sauvegarder")
        with col2:
            submitted_cancel = st.form_submit_button("❌ Annuler")
        
        if submitted_save:
            st.success("✅ Formulaire soumis avec succès !")
        elif submitted_cancel:
            st.info("❌ Formulaire annulé")

if __name__ == "__main__":
    test_simple_form()

