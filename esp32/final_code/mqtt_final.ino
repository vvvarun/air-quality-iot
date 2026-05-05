#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22
#define MQ135_PIN 34

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "######";
const char* password = "#######";

const char* mqtt_server = "######";

WiFiClient espClient;
PubSubClient client(espClient);

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");

    if (client.connect("ESP32_Device")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying...");
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  dht.begin();

  connectWiFi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int air = analogRead(MQ135_PIN);

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT read failed, skipping message");
    delay(500);
    return;
  }

  if (air < 0) {
    Serial.println("Invalid air value, skipping");
    delay(500);
    return;
  }

  String payload = "{";
  payload += "\"temp\":" + String(temp, 2) + ",";
  payload += "\"hum\":" + String(hum, 2) + ",";
  payload += "\"air\":" + String(air);
  payload += "}";

  client.publish("airquality/esp32", payload.c_str());

  Serial.println(payload);

  delay(2000);  
}