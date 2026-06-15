# IoT-Coal-Mine-Safety-System
An IoT-enabled industrial safety system using an ESP32 micro-webserver to stream real-time environmental data to a Python backend for continuous data logging and automated email emergency alerting.
# IoT Coal Mine Safety & Hazard Monitoring System

This is an IoT-based Industrial Safety System designed to monitor underground mine environments for toxic gas leaks, water seepage, humidity, and extreme temperatures using an ESP32 microcontroller. When the system detects unsafe conditions, it automatically triggers a local buzzer alarm and sends an instant email alert to prevent workplace hazards.
📸 Overview

This project combines embedded hardware development with a software backend application. An ESP32 development board collects data from multiple sensors and exposes it via a local web server. A localized Python script continuously fetches this live data, logs it into a permanent CSV file for audits, and handles emergency communication if safety limits are broken.

Main Components:
* **ESP32** – The core microcontroller managing the Wi-Fi network link and processing sensor logic.
* **DHT11 Sensor** – Tracks environmental temperature and humidity parameters inside the mine shaft.
* **Analog Gas Sensor** – Detects accumulation of toxic or combustible gases.
* **Analog Water Level Sensor** – Monitors for unexpected water accumulation or seepage leaks.
* **Piezo Buzzer** – Issues an immediate on-site audio warning to alert miners of danger.
* **Python Backend Script** – Polls the ESP32 server, processes the records, and dispatches automated emails.

⚙️ Features

* Real-time monitoring of industrial environmental hazards.
* Centralized data logging into a local structured CSV file.
* Hardware-driven immediate warning buzzer alert on-site.
* Automated SMTP emergency email alert configuration.
* Intelligent software throttling mechanism to prevent notification email spam during continuous alerts.

🧠 System Architecture

[Sensors] → [ESP32 JSON Web Server] → [Python Backend Script]
                                            ↓
                                     [CSV Ledger Logging]
                                            ↓
                                   [Asynchronous Email Alerts]

🧩 Hardware Requirements

| Component | Quantity | Description |
| :--- | :--- | :--- |
| ESP32 Development Board | 1 | Main microcontroller with integrated Wi-Fi capabilities |
| DHT11 Sensor | 1 | Digital Temperature & Humidity module |
| Analog Gas Sensor | 1 | Detects combustible/toxic gas concentrations |
| Analog Water Level Sensor | 1 | Detects water accumulation or ambient seepage levels |
| Active Piezo Buzzer | 1 | Emits a high-frequency audible local hazard alarm |
| Connecting Wires & Breadboard | - | Used for establishing hardware circuit loops |

💻 Software Requirements

* **Arduino IDE** (For compiling and flashing C++ firmware to the ESP32)
* **Python 3.x** environment
* Required Python Libraries:
  ```bash
  pip install requests

  Project Structure

  IoT-Coal-Mine-Safety-System/
│
├── ESP32_Firmware/
│   └── esp32_sensor_server.ino
│
├── Backend_Data_Logger/
│   └── logger_alert_system.py
│
├── coal_mine_data.csv
│
└── README.md

🚀 Setup & Usage

🪛 1. Flash the ESP32 Code

Open the .ino firmware file inside your Arduino IDE.

Configure your network hotspot or router credentials in the configuration section:
const char* ssid = "Your_WiFi_Name";
const char* password = "Your_WiFi_Password";

Connect the ESP32 to your machine and click Upload.

Keep the Serial Monitor open (baud rate 115200) to find the assigned IP address once the connection completes.

🐍 2. Launch Python Backend Monitor

Open the script file logger_alert_system.py and input your target IP layout and mailing details:
ESP32_IP = "http://<YOUR_ESP32_IP_ADDRESS>"
SENDER_EMAIL = "your_sender_account@domain.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "safety_officer_account@domain.com"

Execute the script from your terminal:
python logger_alert_system.py

