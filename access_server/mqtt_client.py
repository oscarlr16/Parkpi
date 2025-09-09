import paho.mqtt.client as mqtt
import os
from flask import current_app
from dotenv import load_dotenv

load_dotenv(dotenv_path="access_server/.env")

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))

TOPIC_REQUESTS = "access/requests"
TOPIC_DECISION = "access/decisions"
TOPIC_GATE_CMD = "gate/cmd"


def start_mqtt(app, db, User, log):
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to the MQTT broker")
            client.subscribe(TOPIC_REQUESTS)
            print(f"Subscribed to the topic: {TOPIC_REQUESTS}")
        else:
            print(f"MQTT conection error (code: {rc})")

    client.on_connect = on_connect

    def on_message(client, userdata, msg):
        with app.app_context():
            payload = msg.payload.decode("utf-8").strip()
            code = payload

            # decision
            allow = db.session.query(User).filter_by(code=code).first() is not None
            decision = "ALLOW" if allow else "DENY"

            # log
            db.sesion.add(Log(code=code, decision=decision, msg="from_camera"))
            db.session.commit()

            # action on the barrier
            if allow:
                client.publish(TOPIC_GATE_CMD, "OPEN")
            else:
                client.publish(TOPIC_GATE_CMD, "CLOSE")

    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()
