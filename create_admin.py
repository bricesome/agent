# Script de Création du Premier Administrateur
# Exécutez ce script une seule fois au premier déploiement

import os
import sys
import json
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth.auth_manager import AuthManager
from database.db_manager import DatabaseManager

def create_first_admin():
    """Crée le premier compte administrateur de la plateforme"""
    
    print("🔐 Création du Premier Compte Administrateur")
    print("=" * 50)
    
    try:
        # Initialiser les gestionnaires
        auth_manager = AuthManager()
        db_manager = DatabaseManager()
        
        # Demander les informations de l'administrateur
        print("\n📝 Veuillez saisir les informations de l'administrateur :")
        print("-" * 40)
        
        username = input(" Nom d'utilisateur: ").strip()
        email = input(" Email: ").strip()
        password = input("🔒 Mot de passe: ").strip()
        confirm_password = input("🔒 Confirmer le mot de passe: ").strip()
        
        # Validation des données
        if not username or not email or not password:
            print("❌ Tous les champs sont obligatoires !")
            return False
        
        if password != confirm_password:
            print("❌ Les mots de passe ne correspondent pas !")
            return False
        
        if len(password) < 6:
            print("❌ Le mot de passe doit contenir au moins 6 caractères !")
            return False
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = auth_manager.get_user_by_username(username)
        if existing_user:
            print(f"❌ L'utilisateur '{username}' existe déjà !")
            return False
        
        # Créer l'utilisateur administrateur
        print(f"\n Création du compte administrateur '{username}'...")
        
        success = auth_manager.register_user(
            username=username,
            password=password,
            email=email,
            role="admin"
        )
        
        if success:
            print("✅ Compte administrateur créé avec succès !")
            print(f"👤 Username: {username}")
            print(f"📧 Email: {email}")
            print(f" Rôle: Administrateur")
            print(f" Créé le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Créer l'utilisateur dans la base de données
            user_id = db_manager.insert_user(
                username=username,
                email=email,
                password_hash=auth_manager.users[username]["password_hash"],
                role="admin"
            )
            
            if user_id:
                print(f"️ Utilisateur ajouté à la base de données (ID: {user_id})")
            else:
                print("⚠️ Utilisateur créé dans l'auth mais erreur dans la base de données")
            
            print("\n🎉 Configuration terminée !")
            print("Vous pouvez maintenant vous connecter à la plateforme avec ce compte.")
            return True
            
        else:
            print("❌ Erreur lors de la création du compte administrateur !")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Plateforme Agents IA - Création du Premier Administrateur")
    print("=" * 60)
    
    # Vérifier si un administrateur existe déjà
    try:
        auth_manager = AuthManager()
        admin_users = [user for user in auth_manager.users.values() if user.get('role') == 'admin']
        
        if admin_users:
            print("⚠️ Un compte administrateur existe déjà !")
            print("Utilisateurs administrateurs trouvés :")
            for admin in admin_users:
                print(f"  - {admin['username']} ({admin['email']})")
            
            response = input("\nVoulez-vous créer un autre administrateur ? (o/n): ").strip().lower()
            if response not in ['o', 'oui', 'y', 'yes']:
                print("❌ Création annulée.")
                return
        
        # Créer l'administrateur
        if create_first_admin():
            print("\n🎯 Prochaines étapes :")
            print("1. Lancez l'application : streamlit run app_fixed.py")
            print("2. Connectez-vous avec votre compte administrateur")
            print("3. Accédez à la page Administration pour gérer les utilisateurs")
        else:
            print("\n❌ Échec de la création du compte administrateur.")
            print("Vérifiez les erreurs et réessayez.")
    
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        print("Vérifiez que tous les modules sont correctement installés.")

if __name__ == "__main__":
    main()
