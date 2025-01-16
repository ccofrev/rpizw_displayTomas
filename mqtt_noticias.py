# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT
import time
import json

# Configuración del display MAX7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=90, rotate=0, blocks_arranged_in_reverse_order=True)
device.contrast(2)

# Parámetros MQTT
MQTT_BROKER = "broker.hivemq.com"  # Cambia esto por la dirección de tu broker MQTT
MQTT_PORT = 1883
MQTT_TOPIC = "test/displayNoticias"  # Cambia esto por el tópico al que te quieres suscribir

# Mensaje recibido por MQTT
msg = ""
category = ""
repetitions = 0  # Número de repeticiones

# Mapeo de caracteres especiales con sus valores en decimal
special_chars = {
    "á": "\240",
    "é": "\202",
    "í": "\241",
    "ó": "\242",
    "ú": "\243",
    "ñ": "\244",
    "Ñ": "\245"
}

# Función para convertir caracteres especiales
def convert_special_chars(text):
    converted_text = ""
    for char in text:
        if char in special_chars:
            converted_text += special_chars[char]
        else:
            converted_text += char
    return converted_text

# Callback cuando el cliente se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con el código {rc}")
    client.subscribe(MQTT_TOPIC)  # Suscribirse al tópico

# Callback cuando se recibe un mensaje en el tópico
def on_message(client, userdata, msg_data):
    global msg, category, repetitions
    try:
        # Decodificar el mensaje recibido en formato JSON
        payload = json.loads(msg_data.payload.decode())
        msg = payload.get('message', "")  # Obtener el mensaje
        category = payload.get('category', "")  # Obtener la categoría
        repetitions = int(payload.get('repetitions', 0))  # Obtener el número de repeticiones
        print(f"Mensaje recibido: {msg} con categoría {category} y {repetitions} repeticiones")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Iniciar el bucle de trabajo de MQTT
client.loop_start()

# Función para mostrar el texto titilando
def show_titling_text(text):
    # Mostrar la categoría en el display una vez titilando
    show_message(device, text, fill="white", font=proportional(CP437_FONT))
    time.sleep(0.5)  # Mostrar por medio segundo
    device.clear()  # Apagar el display
    time.sleep(0.5)  # Esperar medio segundo antes de mostrarlo nuevamente

# Función principal para manejar el display
def main():
    global msg, category, repetitions
    while True:
        if msg and repetitions > 0:
            # Convertir caracteres especiales antes de mostrar
            converted_category = convert_special_chars(category)
            converted_msg = convert_special_chars(msg)

            # Mostrar la categoría titilando en el display una vez
            show_titling_text(converted_category)  # Mostrar la categoría titilando 1 vez

            # Mostrar el mensaje repetido el número de veces indicado
            for _ in range(repetitions):
                show_message(device, converted_msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)
                time.sleep(1)  # Esperar entre repeticiones

                # Apagar el display después de mostrar el mensaje
                device.clear()

            # Reiniciar las variables para evitar mostrar el mismo mensaje
            msg = ""
            category = ""
            repetitions = 0

        time.sleep(0.1)  # Tiempo para evitar un bucle apretado sin propósito

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
