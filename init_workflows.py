#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation des workflows de démonstration
"""

import json
import os
from datetime import datetime

def init_demo_workflows():
    """Initialise les workflows de démonstration"""
    
    # Vérifier si le fichier workflows.json existe déjà
    if os.path.exists('workflows.json'):
        print("⚠️ Le fichier workflows.json existe déjà.")
        response = input("Voulez-vous le remplacer ? (o/n): ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            print("❌ Initialisation annulée.")
            return
    
    # Workflows de démonstration
    demo_workflows = [
        {
            "id": "workflow_support_client_demo",
            "name": "Support Client - Résolution de Problème",
            "description": "Workflow automatisé pour la résolution de problèmes clients en 4 étapes",
            "type": "Support Client - Résolution de Problème",
            "steps": [
                {
                    "order": 1,
                    "name": "Classification",
                    "agent_name": "Agent Classification",
                    "type": "classification",
                    "description": "Classification automatique du problème client"
                },
                {
                    "order": 2,
                    "name": "Diagnostic",
                    "agent_name": "Agent Diagnostic",
                    "type": "diagnostic",
                    "description": "Analyse approfondie et diagnostic du problème"
                },
                {
                    "order": 3,
                    "name": "Solution",
                    "agent_name": "Agent Solution",
                    "type": "solution",
                    "description": "Proposition de solution adaptée"
                },
                {
                    "order": 4,
                    "name": "Suivi",
                    "agent_name": "Agent Suivi",
                    "type": "suivi",
                    "description": "Planification du suivi et vérification"
                }
            ],
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "workflow_analyse_financiere_demo",
            "name": "Analyse Financière Complète",
            "description": "Workflow d'analyse financière en 3 étapes",
            "type": "Analyse Financière",
            "steps": [
                {
                    "order": 1,
                    "name": "Collecte de Données",
                    "agent_name": "Agent Collecte",
                    "type": "collecte",
                    "description": "Récupération des données financières"
                },
                {
                    "order": 2,
                    "name": "Analyse",
                    "agent_name": "Agent Analyse",
                    "type": "analyse",
                    "description": "Analyse approfondie des données"
                },
                {
                    "order": 3,
                    "name": "Rapport",
                    "agent_name": "Agent Rapport",
                    "type": "rapport",
                    "description": "Génération du rapport final"
                }
            ],
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        }
    ]
    
    # Sauvegarder les workflows de démonstration
    try:
        with open('workflows.json', 'w', encoding='utf-8') as f:
            json.dump(demo_workflows, f, ensure_ascii=False, indent=2)
        
        print("✅ Workflows de démonstration initialisés avec succès !")
        print(f"📋 {len(demo_workflows)} workflows créés :")
        
        for workflow in demo_workflows:
            print(f"   🔄 {workflow['name']} ({len(workflow['steps'])} étapes)")
        
        print("\n🚀 Vous pouvez maintenant lancer l'application et tester les workflows !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")

if __name__ == "__main__":
    print("🔄 Initialisation des Workflows de Démonstration")
    print("=" * 50)
    init_demo_workflows()
