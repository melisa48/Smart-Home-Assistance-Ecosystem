import paho.mqtt.client as mqtt
import json
import time
import random  # For simulated temperature detection
from config import MQTT_BROKER, MQTT_PORT, LIGHTING_TOPIC, TEMPERATURE_TOPIC, USER_PREFERENCES

class LightingAgent:
    def __init__(self):
        self.client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)  # Use MQTTv5 to avoid deprecation warning
        self.client.on_message = self.on_message
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except ConnectionRefusedError as e:
            print(f"Failed to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}. Error: {e}")
            print("Please ensure the MQTT broker is running and the address/port are correct.")
            exit(1)
        self.client.subscribe(LIGHTING_TOPIC)
        self.client.subscribe(TEMPERATURE_TOPIC)
        self.running = False

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        try:
            data = json.loads(payload)
            if isinstance(data, dict):
                if msg.topic == LIGHTING_TOPIC:
                    self.adjust_lights(data.get("brightness", USER_PREFERENCES["preferred_brightness"]))
                elif msg.topic == TEMPERATURE_TOPIC:
                    self.adjust_temperature(data.get("temperature", USER_PREFERENCES["preferred_temp"]))
            elif isinstance(data, (int, float)):
                if msg.topic == LIGHTING_TOPIC:
                    self.adjust_lights(data)
                elif msg.topic == TEMPERATURE_TOPIC:
                    self.adjust_temperature(data)
        except json.JSONDecodeError:
            print(f"Failed to decode message payload: {payload}. Expected JSON or numeric value.")

    def detect_temperature(self):
        # Simulated temperature detection (replace with real sensor reading if using hardware)
        simulated_temp = random.uniform(15, 30)
        print(f"Detected temperature: {simulated_temp:.1f}°C")
        return simulated_temp

    def adjust_lights(self, brightness):
        print(f"Adjusting lights to {brightness}% brightness")

    def adjust_temperature(self, target_temperature):
        print(f"Adjusting temperature to {target_temperature}°C")

    def run(self):
        print("Lighting Agent running...")
        self.running = True
        self.client.loop_start()  # Start the MQTT loop in a background thread
        last_temp_check = time.time()
        temp_check_interval = 10  # Check temperature every 10 seconds (for testing)
        while self.running:
            current_time = time.time()
            if current_time - last_temp_check >= temp_check_interval:
                detected_temp = self.detect_temperature()
                preferred_temp = USER_PREFERENCES["preferred_temp"]
                if abs(detected_temp - preferred_temp) > 1:  # Adjust if difference > 1°C
                    print(f"Detected temperature ({detected_temp:.1f}°C) differs from preferred temperature ({preferred_temp}°C).")
                    self.adjust_temperature(preferred_temp)
                last_temp_check = current_time
            time.sleep(1)  # Check the running flag every second
        self.client.loop_stop()  # Stop the MQTT loop
        print("Lighting Agent stopped.")

    def stop(self):
        self.running = False

if __name__ == "__main__":
    agent = LightingAgent()
    agent.run()