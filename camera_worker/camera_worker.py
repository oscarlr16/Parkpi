import cv2
from pyzbar.pyzbar import decode
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import os
import time
import signal
import sys
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
TOPIC_REQUESTS = "access/requests"

client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Successfully connected to the MQTT broker")
    else:
        print(f"MQTT connection error (code: {reason_code})")


def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message published successfully (mid: {mid})")


client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
    print("MQTT client started")
except Exception as e:
    print(f"Error connecting to MQTT: {e}")
    exit(1)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    for i in range(1, 4):
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera opened at index {i}")
            break
    else:
        print("No available camera found")
        exit(1)
else:
    print("Camera opened successfully")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

seen = set()
frame_count = 0
last_status_time = time.time()

while True:
    ok, frame = cap.read()
    frame_count += 1

    if not ok:
        print(f"Frame {frame_count}: Could not read from camera")
        time.sleep(0.1)
        continue

    current_time = time.time()
    if current_time - last_status_time >= 5:
        print(f"Status: Frame {frame_count}, Unique QRs detected: {len(seen)}")
        last_status_time = current_time

    codes = decode(frame)

    if codes:
        print(f"Frame {frame_count}: Detected {len(codes)} code(s)")

    for obj in codes:
        try:
            text = obj.data.decode("utf-8")
            print(f"📱 QR detected: '{text}' (type: {obj.type})")

            if text not in seen:
                print(f"Publishing new code: {text}")
                result = client.publish(TOPIC_REQUESTS, text)
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print("Code sent successfully")
                    seen.add(text)
                else:
                    print(f"Error sending code: {result.rc}")
            else:
                print(f"Code already seen before: {text}")

        except Exception as e:
            print(f"Error processing QR: {e}")

cap.release()
client.loop_stop()
client.disconnect()
