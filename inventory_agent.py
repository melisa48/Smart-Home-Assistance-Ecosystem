import paho.mqtt.client as mqtt
import json
import time
from config import MQTT_BROKER, MQTT_PORT, INVENTORY_TOPIC

class InventoryAgent:
    def __init__(self):
        self.client = mqtt.Client()
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except ConnectionRefusedError as e:
            print(f"Failed to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}. Error: {e}")
            print("Please ensure the MQTT broker is running and the address/port are correct.")
            exit(1)
        # Simulated pantry inventory (item: quantity)
        self.inventory = {
            "milk": 2,  # Liters
            "bread": 1,  # Loaves
            "eggs": 6   # Count
        }
        self.thresholds = {
            "milk": 1,
            "bread": 1,
            "eggs": 6
        }
        self.running = False

    def check_inventory(self):
        low_items = []
        for item, quantity in self.inventory.items():
            if quantity <= self.thresholds[item]:
                low_items.append(item)
        if low_items:
            self.notify_user(low_items)

    def notify_user(self, low_items):
        message = json.dumps({"low_stock": low_items})
        self.client.publish(INVENTORY_TOPIC, message)
        print(f"Notification: Low stock on {', '.join(low_items)}. Please restock.")

    def run(self):
        print("Inventory Agent running...")
        self.running = True
        self.client.loop_start()  # Start the MQTT loop in a background thread
        last_check = time.time()
        check_interval = 10  # Check every 10 seconds (for testing; set to 3600 for production)
        while self.running:
            current_time = time.time()
            if current_time - last_check >= check_interval:
                self.check_inventory()
                last_check = current_time
            time.sleep(1)  # Check the running flag every second (more responsive)
        self.client.loop_stop()  # Stop the MQTT loop
        print("Inventory Agent stopped.")

    def stop(self):
        self.running = False

if __name__ == "__main__":
    agent = InventoryAgent()
    agent.run()