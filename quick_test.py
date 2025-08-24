#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide de la syntaxe Python
"""

def test_syntax():
    """Test de la syntaxe Python"""
    print("🧪 Test de Syntaxe Python")
    print("=" * 30)
    
    try:
        # Test des imports de base
        import json
        import os
        from datetime import datetime
        print("✅ Imports de base réussis")
        
        # Test de création d'objets
        test_data = {
            'id': 'test_123',
            'name': 'Test',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print("✅ Création d'objets réussie")
        
        # Test de sauvegarde JSON
        with open('test_syntax.json', 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        print("✅ Sauvegarde JSON réussie")
        
        # Nettoyer
        os.remove('test_syntax.json')
        print("✅ Nettoyage réussi")
        
        print("\n🎉 Syntaxe Python OK !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de syntaxe : {e}")
        return False

if __name__ == "__main__":
    test_syntax()

