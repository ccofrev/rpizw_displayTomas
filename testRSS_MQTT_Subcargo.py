# -*- coding: utf-8 -*-

import feedparser
import random
import paho.mqtt.client as mqtt
import time
import json

# URL del RSS feed de Cooperativa y sus categorías asociadas
rss_urls = [
    ("https://www.cooperativa.cl/noticias/site/tax/port/all/rss_1___1.xml", "Deportes"),  # deportes
    ("https://www.cooperativa.cl/noticias/site/tax/port/all/rss_2___1.xml", "Mundo"),    # mundo
    ("https://www.cooperativa.cl/noticias/site/tax/port/all/rss_3___1.xml", "País"),     # pais
    ("https://www.cooperativa.cl/noticias/site/tax/port/all/rss_4___1.xml", "Entretenimiento"), # entretencion
    ("https://www.cooperativa.cl/noticias/site/tax/port/all/rss_6___1.xml", "Economía"),  # economia
    ("https://www.cooperativa.cl/noticias/site/tax/port/all/rss_8___1.xml", "Tecnología"), # tecnologia
]

# Parámetros MQTT
MQTT_BROKER = "142.93.8.41"  # Cambia esto por la dirección de tu broker MQTT
MQTT_PORT = 1883
MQTT_TOPIC = "tvsubcargo/config"  # Cambia esto por el tópico al que te quieres suscribir

# Función para obtener titulares aleatorios del RSS feed
def get_random_headline():
    # Seleccionar una URL RSS y su categoría asociada aleatoriamente
    rss_url, category = random.choice(rss_urls)

    # Parsear el RSS feed
    feed = feedparser.parse(rss_url)

    # Verifica si hay entradas en el feed
    if feed.entries:
        # Elegir un titular aleatorio de las entradas del feed
        random_entry = random.choice(feed.entries)
        return random_entry.title, category
    else:
        return "No se pudieron obtener titulares.", ""

# Callback cuando el cliente se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código {}".format(rc))
    # No es necesario subscribirse, ya que solo publicaremos

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conectar al broker MQTT
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Iniciar el bucle de trabajo de MQTT
client.loop_start()

# Función principal que obtiene y publica el titular
def main():
    while True:
        # Obtener un titular aleatorio y su categoría
        headline, category = get_random_headline()

        # Si no se obtuvieron titulares, intentar de nuevo
        if headline == "No se pudieron obtener titulares.":
            print("Error: No se obtuvieron titulares. Intentando de nuevo...")
            continue

        # Crear el mensaje como un diccionario
        message = {
            "id_dispositivo": "573350de9160c36c",
            "message": "[" + category.upper() + "] " + headline,  # Convertir la categoría a mayúsculas
            "period": 15  # Número de repeticiones
        }



        # Publicar el mensaje en formato JSON en MQTT
        client.publish(MQTT_TOPIC, json.dumps(message))  # Convertimos el diccionario a JSON
        print("Publicado: {}".format(message))

        # Esperar antes de obtener otro titular
        time.sleep(120)  # Puedes ajustar el tiempo de espera según lo necesites

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
