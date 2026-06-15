import requests
import time
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === Configuration ===

ESP32_IP = "http://192.168.137.116"  # Replace with your ESP32 IP
CSV_FILE = "coal_mine_data.csv"

# Email settings
SENDER_EMAIL = "varun@comtranse.in"         # Replace with your Gmail
SENDER_PASSWORD = "*~1l=uW^+D2^" # Replace with your Gmail app password
RECEIVER_EMAIL = "varunwason1@gmail.com"   # Replace with recipient email
SMTP_SERVER = "mail.comtranse.in"
SMTP_PORT = 465  # SSL port

# === CSV Functions ===

def initialize_csv():
    """Create the CSV file with headers if not exists."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "ESP32_IP", "Timestamp", "Temperature(°C)",
                "Humidity(%)", "Gas_Level", "Water_Level", "Danger"
            ])
        print(f"✅ Created new data file: {CSV_FILE}")

def save_to_csv(data):
    """Append sensor data to CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            ESP32_IP, timestamp, data["temperature"],
            data["humidity"], data["gas"],
            data["water"], data["danger"]
        ])
    print(f"💾 Data saved at {timestamp}")

# === Email Alert Function ===

def send_email_alert(subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("📧 Email alert sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

# === Main Program ===

def main():
    initialize_csv()
    last_alert_time = 0
    alert_cooldown = 60  # seconds

    while True:
        try:
            response = requests.get(ESP32_IP + "/")
            if response.status_code == 200:
                data = response.json()
                print(f"🌡 Temp: {data['temperature']} °C | 💧 Humidity: {data['humidity']} % | "
                      f"🧪 Gas: {data['gas']} | 🌊 Water: {data['water']} | 🚨 Danger: {data['danger']}")

                save_to_csv(data)

                # Check danger conditions
                current_time = time.time()
                if data["danger"] == 1 and (current_time - last_alert_time > alert_cooldown):
                    alert_msg = (
                        f"⚠️ COAL MINE ALERT!\n\n"
                        f"Temperature: {data['temperature']} °C\n"
                        f"Humidity: {data['humidity']} %\n"
                        f"Gas Level: {data['gas']}\n"
                        f"Water Level: {data['water']}\n"
                        f"\nImmediate action recommended!"
                    )
                    send_email_alert("🚨 Coal Mine Safety Alert!", alert_msg)
                    last_alert_time = current_time
            else:
                print("⚠️ Bad response:", response.status_code)

        except requests.exceptions.ConnectionError:
            print("🌐 Cannot connect to ESP32, retrying...")
        except Exception as e:
            print("❌ Error:", e)

        time.sleep(5)

if __name__ == "__main__":
    main()
