# Configuration settings
MQTT_BROKER = "broker.hivemq.com"  # Public HiveMQ broker
MQTT_PORT = 1883

# Topics for inter-agent communication
LIGHTING_TOPIC = "home/lighting"
TEMPERATURE_TOPIC = "home/temperature"
SECURITY_TOPIC = "home/security"
INVENTORY_TOPIC = "home/inventory"

# User preferences (example)
USER_PREFERENCES = {
    "preferred_temp": 22,  # Celsius
    "preferred_brightness": 70,  # Percentage
}