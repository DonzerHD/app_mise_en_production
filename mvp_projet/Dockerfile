# Utiliser une image de base Python officielle
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt en premier pour profiter du cache des couches Docker
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source de l'application dans le conteneur
COPY . /app/

# Exécuter collectstatic
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande pour démarrer l'application
# CMD ["python", "mvp_projet/manage.py", "runserver", "0.0.00.0:8000"]

# Utiliser gunicorn comme serveur WSGI au lieu de runserver pour la production
CMD ["gunicorn", "mvp_projet.wsgi:application", "--bind", "0.0.0.0:8000"]

#Command
#az acr login --name thomasprojetmep
#docker build -t thomasprojetmep.azurecr.io/samples/monapp-django:latest .
#docker push thomasprojetmep.azurecr.io/samples/monapp-django:latest
#docker run --env-file .env -p 8000:8000 thomasprojetmep.azurecr.io/samples/monapp-django:latest
