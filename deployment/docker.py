# Configuration Docker professionnelle
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .
COPY requirements-prod.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copie du code source
COPY . .

# Création de l'utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exposition des ports
EXPOSE 8501 8000

# Script de démarrage
COPY deployment/start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
```

