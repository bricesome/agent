#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation des agents de démonstration pour les workflows
"""

import json
import os
from datetime import datetime

def init_demo_agents():
    """Initialise les agents de démonstration pour les workflows"""
    
    # Vérifier si le fichier agents.json existe déjà
    if os.path.exists('agents.json'):
        print("⚠️ Le fichier agents.json existe déjà.")
        response = input("Voulez-vous le remplacer ? (o/n): ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            print("❌ Initialisation annulée.")
            return
    
    # Agents de démonstration pour les workflows
    demo_agents = [
        {
            "id": "agent_classification_demo",
            "name": "Agent Classification",
            "domain": "Support Client",
            "type": "Classification",
            "model": "GPT-4",
            "system_prompt": "Tu es un agent spécialisé dans la classification automatique des problèmes clients. Tu analyses les descriptions et les classe selon leur type, priorité et urgence.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_diagnostic_demo",
            "name": "Agent Diagnostic",
            "domain": "Support Client",
            "type": "Diagnostic",
            "model": "Claude-3",
            "system_prompt": "Tu es un agent expert en diagnostic de problèmes. Tu analyses en profondeur les problèmes classifiés pour identifier les causes racines et les impacts.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_solution_demo",
            "name": "Agent Solution",
            "domain": "Support Client",
            "type": "Solution",
            "model": "Gemini Pro",
            "system_prompt": "Tu es un agent spécialisé dans la proposition de solutions. Tu proposes des solutions adaptées et des procédures de résolution basées sur le diagnostic.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_suivi_demo",
            "name": "Agent Suivi",
            "domain": "Support Client",
            "type": "Suivi",
            "model": "GPT-4",
            "system_prompt": "Tu es un agent de suivi et de vérification. Tu planifies les actions de suivi et vérifies la résolution des problèmes.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_collecte_demo",
            "name": "Agent Collecte",
            "domain": "Finance",
            "type": "Collecte",
            "model": "Claude-3",
            "system_prompt": "Tu es un agent spécialisé dans la collecte de données financières. Tu récupères et valides les informations financières nécessaires à l'analyse.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_analyse_demo",
            "name": "Agent Analyse",
            "domain": "Finance",
            "type": "Analyse",
            "model": "Gemini Pro",
            "system_prompt": "Tu es un agent expert en analyse financière. Tu analyses les données collectées pour identifier les tendances et les insights.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_rapport_demo",
            "name": "Agent Rapport",
            "domain": "Finance",
            "type": "Rapport",
            "model": "GPT-4",
            "system_prompt": "Tu es un agent spécialisé dans la génération de rapports financiers. Tu crées des rapports clairs et structurés basés sur l'analyse.",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        }
    ]
    
    # Sauvegarder les agents de démonstration
    try:
        with open('agents.json', 'w', encoding='utf-8') as f:
            json.dump(demo_agents, f, ensure_ascii=False, indent=2)
        
        print("✅ Agents de démonstration initialisés avec succès !")
        print(f"🤖 {len(demo_agents)} agents créés :")
        
        for agent in demo_agents:
            print(f"   🤖 {agent['name']} ({agent['domain']} - {agent['type']})")
        
        print("\n🚀 Vous pouvez maintenant créer et tester des workflows avec ces agents !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")

if __name__ == "__main__":
    print("🤖 Initialisation des Agents de Démonstration")
    print("=" * 50)
    init_demo_agents()


