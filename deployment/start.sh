#!/bin/bash
# Script de démarrage professionnel

echo "🚀 Démarrage de la plateforme AI Agents..."

# Vérification des variables d'environnement
if [ -z "$DB_TYPE" ]; then
    echo "⚠️ DB_TYPE non défini, utilisation de SQLite par défaut"
    export DB_TYPE=sqlite
fi

# Migration de la base de données
echo "📊 Migration de la base de données..."
python -m alembic upgrade head

# Démarrage de l'API REST
echo "�� Démarrage de l'API REST..."
python -m api.main &

# Démarrage de Streamlit
echo "📱 Démarrage de l'interface Streamlit..."
streamlit run app_fixed.py --server.port 8501 --server.address 0.0.0.0
