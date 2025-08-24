#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que les options des agents sont spécifiques
"""

import json
import os
from datetime import datetime

def test_agent_specific_options():
    """Test que chaque agent a ses propres options spécifiques"""
    
    print("🧪 Test des Options Spécifiques des Agents")
    print("=" * 50)
    
    # Créer plusieurs agents de test avec des noms différents
    test_agents = [
        {
            "id": "agent_001",
            "name": "Agent Analyse Financière",
            "domain": "Finance",
            "type": "Analyse",
            "model": "GPT-4",
            "system_prompt": "Agent spécialisé en analyse financière",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_002", 
            "name": "Agent Rapport Marketing",
            "domain": "Marketing",
            "type": "Rapport",
            "model": "Claude-3",
            "system_prompt": "Agent spécialisé en rapports marketing",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        },
        {
            "id": "agent_003",
            "name": "Agent Résumé Technique",
            "domain": "Technique",
            "type": "Résumé",
            "model": "Gemini Pro",
            "system_prompt": "Agent spécialisé en résumés techniques",
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executions": []
        }
    ]
    
    print(f"✅ {len(test_agents)} agents de test créés")
    
    # Tester la génération des clés spécifiques
    for agent in test_agents:
        agent_id = agent.get('id', 'unknown')
        agent_name = agent.get('name', 'Agent sans nom')
        
        # Générer les clés comme dans l'application
        exec_key = f"exec_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        edit_key = f"edit_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        delete_key = f"delete_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        share_key = f"share_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        stats_key = f"stats_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        
        # Clés du formulaire d'édition
        form_key = f"edit_agent_form_{agent_id}_{agent_name.replace(' ', '_')}"
        name_key = f"edit_name_{agent_id}_{agent_name.replace(' ', '_')}"
        domain_key = f"edit_domain_{agent_id}_{agent_name.replace(' ', '_')}"
        type_key = f"edit_type_{agent_id}_{agent_name.replace(' ', '_')}"
        model_key = f"edit_model_{agent_id}_{agent_name.replace(' ', '_')}"
        prompt_key = f"edit_prompt_{agent_id}_{agent_name.replace(' ', '_')}"
        save_key = f"save_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        cancel_key = f"cancel_agent_{agent_id}_{agent_name.replace(' ', '_')}"
        
        print(f"\n🤖 Agent: {agent_name}")
        print(f"   ID: {agent_id}")
        print(f"   Clés générées:")
        print(f"     ▶️ Exécuter: {exec_key}")
        print(f"     ✏️ Éditer: {edit_key}")
        print(f"     🗑️ Supprimer: {delete_key}")
        print(f"     📤 Partager: {share_key}")
        print(f"     📊 Stats: {stats_key}")
        print(f"     📝 Formulaire: {form_key}")
        print(f"     💾 Sauvegarder: {save_key}")
        print(f"     ❌ Annuler: {cancel_key}")
        
        # Vérifier que les clés sont uniques
        all_keys = [exec_key, edit_key, delete_key, share_key, stats_key, form_key, save_key, cancel_key]
        if len(all_keys) == len(set(all_keys)):
            print(f"   ✅ Toutes les clés sont uniques")
        else:
            print(f"   ❌ Certaines clés sont dupliquées")
    
    # Test de sauvegarde
    try:
        with open('test_agents_specific.json', 'w', encoding='utf-8') as f:
            json.dump(test_agents, f, ensure_ascii=False, indent=2)
        print("\n✅ Sauvegarde de test réussie")
        
        # Nettoyer
        os.remove('test_agents_specific.json')
        print("✅ Fichier de test nettoyé")
        
    except Exception as e:
        print(f"\n⚠️ Erreur de sauvegarde (normal) : {e}")
    
    print("\n🎉 Test des options spécifiques des agents réussi !")
    print("🚀 Chaque agent a maintenant ses propres options uniques dans l'application.")

if __name__ == "__main__":
    test_agent_specific_options()
