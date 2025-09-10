#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASS";


const char* MQTT_HOST = "192.168.1.50";
const int   MQTT_PORT = 1883;

WiFiClient espClient;
PubSubClient mqtt(espClient);

const char* TOPIC_CMD     = "gate/cmd"; 
const char* TOPIC_STATUS  = "gate/status";
const char* TOPIC_VEHICLE = "vehicle/detected";

const int LED = 2; // Built-in LED (simulates barrier): ON=closed, OFF=open
const int BTN = 0; // BOOT button to simulate vehicle detector

void onMessage(char* topic, byte* payload, unsigned int len) {
  String msg;
  for (unsigned int i=0;i<len;i++) msg += (char)payload[i];

  if (String(topic) == TOPIC_CMD) {
    if (msg == "OPEN") {
      digitalWrite(LED, LOW);
      mqtt.publish(TOPIC_STATUS, "OPENING");
      delay(700);
      mqtt.publish(TOPIC_STATUS, "OPEN");
    } else if (msg == "CLOSE") {
      digitalWrite(LED, HIGH);
      mqtt.publish(TOPIC_STATUS, "CLOSING");
      delay(700);
      mqtt.publish(TOPIC_STATUS, "CLOSED");
    }
  }
}

void ensureMqtt() {
  while (!mqtt.connected()) {
    String cid = "esp32-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    if (mqtt.connect(cid.c_str())) {
      mqtt.subscribe(TOPIC_CMD);
      mqtt.publish(TOPIC_STATUS, "BOOT");
    } else {
      delay(1000);
    }
  }
}

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BTN, INPUT_PULLUP);
  digitalWrite(LED, HIGH); // barrier closed at start

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(onMessage);
}

void loop() {
  if (!mqtt.connected()) ensureMqtt();
  mqtt.loop();

  static unsigned long last = 0;
  if (digitalRead(BTN) == LOW && millis() - last > 1200) {
    mqtt.publish(TOPIC_VEHICLE, "1");
    last = millis();
  }
}