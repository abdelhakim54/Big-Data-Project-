import pandas as pd
from kafka import KafkaProducer
import time
import random

import settings
# Configuration du producteur Kafka
producer = KafkaProducer(bootstrap_servers= 'localhost:9092', value_serializer=lambda v: str(v).encode('utf-8'))

settings.init()
measures = settings.measures

if __name__=="__main__":
    # Lire le fichier CSV

    df = pd.read_csv('data/gams_indoor.csv')

    # Parcourir chaque ligne du fichier CSV et publier au topic Kafka
    for _, row in df.iterrows():
        data = row.to_dict()  # Convertir la ligne en dictionnaire
        l = list(measures.items())
        random.shuffle(l)
        shuffled_measures = dict(l)
        for measure, partition in shuffled_measures.items():
            producer.send("topic1", value= data[measure], partition = partition)
            t = random.randint(0, 3)
            time.sleep(t) # Attendre t secondes entre chaque envoi


    producer.close()
