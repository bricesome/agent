#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que les clés des agents sont vraiment uniques
"""

import json
import os
from datetime import datetime

def test_unique_agent_keys():
    """Test que chaque agent a des clés vraiment uniques"""
    
    print("🧪 Test des Clés TRÈS Uniques des Agents")
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
            "created_at": "2024-01-15 10:30:00",
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
            "created_at": "2024-01-15 11:45:00",
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
            "created_at": "2024-01-15 14:20:00",
            "executions": []
        }
    ]
    
    print(f"✅ {len(test_agents)} agents de test créés")
    
    all_keys = []
    
    # Tester la génération des clés TRÈS uniques
    for agent in test_agents:
        agent_id = agent.get('id', 'unknown')
        agent_name = agent.get('name', 'Agent sans nom')
        
        # Générer l'ID unique comme dans l'application
        agent_unique_id = f"{agent_id}_{agent_name.replace(' ', '_').replace('-', '_')}_{agent.get('created_at', 'unknown').replace(' ', '_').replace(':', '_')}"
        
        # Générer les clés comme dans l'application
        exec_key = f"exec_agent_{agent_unique_id}"
        edit_key = f"edit_agent_{agent_unique_id}"
        delete_key = f"delete_agent_{agent_unique_id}"
        share_key = f"share_agent_{agent_unique_id}"
        stats_key = f"stats_agent_{agent_unique_id}"
        
        # Clés du formulaire d'édition
        form_key = f"edit_agent_form_{agent_unique_id}"
        name_key = f"edit_name_{agent_unique_id}"
        domain_key = f"edit_domain_{agent_unique_id}"
        type_key = f"edit_type_{agent_unique_id}"
        model_key = f"edit_model_{agent_unique_id}"
        prompt_key = f"edit_prompt_{agent_unique_id}"
        save_key = f"save_agent_{agent_unique_id}"
        cancel_key = f"cancel_agent_{agent_unique_id}"
        
        # Clés de confirmation
        confirm_key = f"confirm_delete_agent_{agent_unique_id}"
        yes_key = f"yes_agent_{agent_unique_id}"
        no_key = f"no_agent_{agent_unique_id}"
        
        # Ajouter toutes les clés à la liste
        agent_keys = [exec_key, edit_key, delete_key, share_key, stats_key, form_key, 
                     name_key, domain_key, type_key, model_key, prompt_key, save_key, 
                     cancel_key, confirm_key, yes_key, no_key]
        all_keys.extend(agent_keys)
        
        print(f"\n🤖 Agent: {agent_name}")
        print(f"   ID: {agent_id}")
        print(f"   ID Unique: {agent_unique_id}")
        print(f"   Clés générées:")
        print(f"     ▶️ Exécuter: {exec_key}")
        print(f"     ✏️ Éditer: {edit_key}")
        print(f"     🗑️ Supprimer: {delete_key}")
        print(f"     📤 Partager: {share_key}")
        print(f"     📊 Stats: {stats_key}")
        print(f"     📝 Formulaire: {form_key}")
        print(f"     💾 Sauvegarder: {save_key}")
        print(f"     ❌ Annuler: {cancel_key}")
        print(f"     ✅ Confirmation: {confirm_key}")
        print(f"     ✅ Oui: {yes_key}")
        print(f"     ❌ Non: {no_key}")
        
        # Vérifier que les clés de cet agent sont uniques
        if len(agent_keys) == len(set(agent_keys)):
            print(f"   ✅ Toutes les clés de cet agent sont uniques")
        else:
            print(f"   ❌ Certaines clés de cet agent sont dupliquées")
    
    # Vérifier que toutes les clés de tous les agents sont uniques
    print(f"\n🔍 Vérification globale des clés:")
    print(f"   Total des clés générées: {len(all_keys)}")
    print(f"   Clés uniques: {len(set(all_keys))}")
    
    if len(all_keys) == len(set(all_keys)):
        print(f"   ✅ TOUTES les clés sont uniques !")
    else:
        print(f"   ❌ Il y a des clés dupliquées entre agents")
        duplicates = [key for key in all_keys if all_keys.count(key) > 1]
        print(f"   Clés dupliquées: {duplicates}")
    
    # Test de sauvegarde
    try:
        with open('test_agents_unique.json', 'w', encoding='utf-8') as f:
            json.dump(test_agents, f, ensure_ascii=False, indent=2)
        print("\n✅ Sauvegarde de test réussie")
        
        # Nettoyer
        os.remove('test_agents_unique.json')
        print("✅ Fichier de test nettoyé")
        
    except Exception as e:
        print(f"\n⚠️ Erreur de sauvegarde (normal) : {e}")
    
    print("\n🎉 Test des clés uniques des agents terminé !")
    print("🚀 Chaque agent a maintenant des options TRÈS spécifiques dans l'application.")

if __name__ == "__main__":
    test_unique_agent_keys()
