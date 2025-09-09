import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTT_ERR_SUCCESS
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="access_server/.env")

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))

TOPIC_REQUESTS = "access/requests"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Successfully connected to the MQTT broker")
        client.subscribe(TOPIC_REQUESTS)
        print(f"Subscribed to the topic: {TOPIC_REQUESTS}")
    else:
        print(f"MQTT connection error (code: {reason_code})")


def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message published successfully (mid: {mid})")


def create_mqtt_client():
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    return client, MQTT_HOST, MQTT_PORT, TOPIC_REQUESTS


def publish_message(client, topic, message):
    result = client.publish(topic, message)
    return result.rc == MQTT_ERR_SUCCESS
