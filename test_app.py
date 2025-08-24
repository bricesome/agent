#!/usr/bin/env python3
"""
Script de test pour la Plateforme Agents IA
Vérifie que tous les composants fonctionnent correctement
"""

import os
import sys
import json
import importlib

def test_imports():
    """Teste l'importation des modules requis"""
    print("🧪 Test des imports...")
    
    required_modules = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'PIL'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} modules manquants")
        return False
    else:
        print("✅ Tous les imports sont réussis")
        return True

def test_files():
    """Teste l'existence des fichiers requis"""
    print("\n📁 Test des fichiers...")
    
    required_files = [
        'app.py',
        'pages/execute_agent.py',
        'requirements.txt',
        'demo_agents.json'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} fichiers manquants")
        return False
    else:
        print("✅ Tous les fichiers sont présents")
        return True

def test_data_files():
    """Teste les fichiers de données"""
    print("\n💾 Test des fichiers de données...")
    
    data_files = ['agents.json', 'models.json']
    
    for file_path in data_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  ✅ {file_path} ({len(data)} entrées)")
            except Exception as e:
                print(f"  ❌ {file_path}: Erreur de lecture - {e}")
        else:
            print(f"  ⚠️ {file_path}: Fichier non trouvé (sera créé au premier lancement)")
    
    return True

def test_streamlit_config():
    """Teste la configuration Streamlit"""
    print("\n⚙️ Test de la configuration Streamlit...")
    
    config_file = '.streamlit/config.toml'
    
    if os.path.exists(config_file):
        print(f"  ✅ {config_file}")
        return True
    else:
        print(f"  ❌ {config_file}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 Démarrage des tests de la Plateforme Agents IA")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Fichiers", test_files),
        ("Données", test_data_files),
        ("Config Streamlit", test_streamlit_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont réussis ! La plateforme est prête.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

def show_help():
    """Affiche l'aide du script"""
    print("""
🧪 Script de test pour la Plateforme Agents IA

Usage:
  python test_app.py          # Exécute tous les tests
  python test_app.py --help   # Affiche cette aide

Ce script vérifie:
  • Importation des modules requis
  • Présence des fichiers essentiels
  • Intégrité des fichiers de données
  • Configuration Streamlit

En cas d'échec, consultez le README.md pour la résolution des problèmes.
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_help()
    else:
        success = run_all_tests()
        
        if success:
            print("\n🚀 Pour lancer l'application:")
            print("  streamlit run app.py")
            print("  ou double-cliquez sur run.bat (Windows)")
        else:
            print("\n🔧 Pour résoudre les problèmes:")
            print("  1. Vérifiez que Python 3.8+ est installé")
            print("  2. Exécutez: pip install -r requirements.txt")
            print("  3. Consultez le README.md pour plus de détails")
        
        sys.exit(0 if success else 1)
