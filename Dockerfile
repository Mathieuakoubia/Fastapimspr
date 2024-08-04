# Utiliser une image de base officielle de Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copie des fichiers des dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'app
COPY . .

# Exposer le port de l'app
EXPOSE 8000

# démarrage de l'app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
