#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>

// === Pin Configuration ===
#define DHTPIN 4
#define DHTTYPE DHT11
#define GAS_SENSOR_PIN 34
#define WATER_SENSOR_PIN 35
#define BUZZER_PIN 27
#define WIFI_LED 2  // Optional: onboard LED for WiFi status

// === WiFi credentials ===
const char* ssid = "Varun";
const char* password = "varung216";

// === Create server & sensor objects ===
WebServer server(80);
DHT dht(DHTPIN, DHTTYPE);

// === Function Declaration ===
void handleSensorData();

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(WIFI_LED, OUTPUT);
  dht.begin();

  Serial.println("🔌 Starting WiFi connection...");
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ Connected to WiFi!");
    Serial.print("📶 IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(WIFI_LED, HIGH);  // Turn on LED if connected
  } else {
    Serial.println("\n❌ Failed to connect to WiFi. Check credentials or hotspot.");
    digitalWrite(WIFI_LED, LOW);
    return;
  }

  server.on("/", handleSensorData);
  server.begin();
  Serial.println("🌐 Web server started...");
}

void loop() {
  server.handleClient();
}

void handleSensorData() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int gasValue = analogRead(GAS_SENSOR_PIN);
  int waterValue = analogRead(WATER_SENSOR_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    server.send(500, "application/json", "{\"error\":\"Sensor read failed\"}");
    return;
  }

  bool danger = false;
  String alertMsg = "";

  if (gasValue > 600) {
    danger = true;
    alertMsg += "High Gas Level! ";
  }
  if (waterValue > 700) {
    danger = true;
    alertMsg += "Water Seepage Detected! ";
  }
  if (temperature > 50) {
    danger = true;
    alertMsg += "High Temperature! ";
  }

  digitalWrite(BUZZER_PIN, danger ? HIGH : LOW);

  Serial.println("====== Sensor Readings ======");
  Serial.printf("Temperature: %.1f °C\n", temperature);
  Serial.printf("Humidity: %.1f %%\n", humidity);
  Serial.printf("Gas Level: %d\n", gasValue);
  Serial.printf("Water Level: %d\n", waterValue);
  if (danger) Serial.println("⚠️ ALERT: " + alertMsg);
  else Serial.println("✅ Environment Safe");

  String json = "{";
  json += "\"temperature\":" + String(temperature, 1) + ",";
  json += "\"humidity\":" + String(humidity, 1) + ",";
  json += "\"gas\":" + String(gasValue) + ",";
  json += "\"water\":" + String(waterValue) + ",";
  json += "\"danger\":" + String(danger ? 1 : 0);
  json += "}";

  server.send(200, "application/json", json);
}