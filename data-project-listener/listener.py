import psycopg2
import select
import requests
from datetime import datetime, timezone
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Connexion à PostgreSQL
conn = psycopg2.connect(
    database='backup',
    user='postgres',
    password='postgres',
    host='data-project_282346-postgres-1',
    port='5432'
)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()
# 🔔 Écoute des deux canaux
cur.execute("LISTEN events_channel;")
cur.execute("LISTEN events_channel_comment;") #ajouter
cur.execute("LISTEN events_channel_question;")

logging.info("🔄 En attente sur 'events_channel' et 'events_channel_comment' et events_channel_question ...") #ajouter

# Déclenchement du DAG indicateur_3
def trigger_dag_3():
    url = "http://webserver:8080/api/v1/dags/indicateur_3/dagRuns"
    auth = ('admin', 'admin')
    payload = {
        "conf": {"key": "value"},
        "execution_date": datetime.now(timezone.utc).isoformat()
    }
    try:
        response = requests.post(url, json=payload, auth=auth)
        if response.status_code in [200, 201]:
            logging.info("✅ DAG 'indicateur_3' déclenché avec succès.")
        else:
            logging.warning(f"❌ Échec DAG 3 : {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Erreur DAG 3 : {e}")

# Déclenchement du DAG indicateur_2  
def trigger_dag_2(): 
    url = "http://webserver:8080/api/v1/dags/indicateur_2/dagRuns"
    auth = ('admin', 'admin')
    payload = {
        "conf": {"key": "value"},
        "execution_date": datetime.now(timezone.utc).isoformat()
    }
    try:
        response = requests.post(url, json=payload, auth=auth)
        if response.status_code in [200, 201]:
            logging.info("✅ DAG 'indicateur_2' déclenché avec succès.")
        else:
            logging.warning(f"❌ Échec DAG 2 : {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Erreur DAG 2 : {e}")

def trigger_dag_1():
    url = "http://webserver:8080/api/v1/dags/indicateur_1/dagRuns"
    auth = ('admin', 'admin')
    payload = {
        "conf": {"key": "value"},
        "execution_date": datetime.now(timezone.utc).isoformat()
    }
    try:
        response = requests.post(url, json=payload, auth=auth)
        if response.status_code in [200, 201]:
            logging.info("✅ DAG 'indicateur_1' déclenché avec succès.")
        else:
            logging.warning(f"❌ Échec DAG 1 : {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Erreur DAG 1 : {e}")

# Boucle d’écoute continue
try:
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            logging.info(f"📢 Notification reçue sur {notify.channel} : {notify.payload}")

            # Dispatcher selon le canal
            if notify.channel == 'events_channel':
                trigger_dag_3()
            elif notify.channel == 'events_channel_comment':#ajouter
                trigger_dag_2()#ajouter
            elif notify.channel == 'events_channel_question':
                trigger_dag_1()

except KeyboardInterrupt:
    logging.info("🛑 Arrêt manuel demandé.")
finally:
    cur.close()
    conn.close()
