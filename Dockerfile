# Image de base Python 3.9
FROM python:3.9-slim

# Métadonnées
LABEL maintainer="Arnaud Rambourg"
LABEL description="Assistant FAQ Intelligent pour Collectivité Territoriale"

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY src/ ./src/
COPY data/ ./data/

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exposer le port (pour une future API FastAPI)
EXPOSE 8000

# Commande par défaut (peut être surchargée)
CMD ["python", "-m", "src.strategies.strategie_b_rag"]
