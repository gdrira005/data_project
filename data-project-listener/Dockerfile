# Utiliser l'image officielle Python comme base
FROM python:3.9

ADD listener.py .
RUN pip install psycopg2-binary requests

CMD ["python", "./listener.py"]

# Définir le répertoire de travail dans le conteneur
#WORKDIR /app

# Copier tous les fichiers locaux dans le conteneur (y compris le code Python)
#COPY . /app

# Installer les dépendances nécessaires (si vous avez un fichier requirements.txt)
#RUN pip install --no-cache-dir -r requirements.txt
# Installer les dépendances nécessaires

#RUN pip install --no-cache-dir psycopg2-binary requests

# Si vous n'avez pas de fichier requirements.txt, installez directement les dépendances nécessaires comme psycopg2 et requests
# RUN pip install --no-cache-dir psycopg2-binary requests

# Exécuter le script Python lorsque le conteneur est démarré
#CMD ["python", "./listener.py"]
