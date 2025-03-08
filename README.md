# Smart Home Assistance Ecosystem

The Smart Home Assistance Ecosystem is a Python-based system designed to automate and manage various aspects of a smart home environment. It integrates multiple agents to control lighting and temperature, monitor security via camera motion detection, and manage pantry inventory with low-stock notifications. The system uses MQTT for inter-agent communication and can be extended to integrate with real smart home hardware.

## Features

- **Lighting Agent**: Simulates control of lights (brightness) and temperature based on user preferences and detected temperature. Includes simulated temperature detection (random values between 15°C and 30°C), adjustable via MQTT messages.
- **Security Agent**: Monitors a camera feed for motion detection using OpenCV and sends alerts when motion is detected, with a 5-second debounce to prevent flooding notifications.
- **Inventory Agent**: Tracks pantry inventory and sends notifications when stock levels fall below defined thresholds.
- **MQTT Integration**: Uses an MQTT broker (local or cloud-based) for communication between agents.
- **Flexible Stopping**: Supports manual stopping (typing 'q' and pressing Enter), automatic stopping (after 5 minutes), and `Ctrl+C` interruption.

## Prerequisites

- **Python 3.12+**: Ensure Python is installed on your system.
- **Required Libraries**:
  - `paho-mqtt`: For MQTT communication (`pip install paho-mqtt`).
  - `opencv-python`: For camera motion detection in the Security Agent (`pip install opencv-python`).
- **MQTT Broker**: Either a local embedded broker (e.g., `gmqtt`, install with `pip install gmqtt`) or a cloud-based broker (e.g., `broker.hivemq.com`).
- **Camera**: A webcam or connected camera (optional, for Security Agent motion detection).

## Project Structure
Smart Home Assistance Ecosystem:
- │
- ├── main.py              # Main script to run all agents
- ├── lighting_agent.py    # Agent for controlling lights and temperature
- ├── security_agent.py    # Agent for security camera motion detection
- ├── inventory_agent.py   # Agent for inventory management
- ├── config.py            # Configuration settings (MQTT broker, topics, preferences)
- └── README.md            # Project documentation (this file)


## Setup

1. **Clone or Download the Project**:
   - Copy the project files to your local machine.

2. **Install Dependencies**:
   - Open a terminal in the project directory and run:
     ```bash
     pip install paho-mqtt opencv-python
     ```
   - If using a local MQTT broker, also install `gmqtt`:
     ```bash
     pip install gmqtt
     ```
   - Note: If using a cloud-based broker, no additional installation is needed beyond `paho-mqtt`.

3. **Configure `config.py`**:
   - Edit `config.py` to set your MQTT broker details and preferences:
     ```python
     # Configuration settings
     MQTT_BROKER = "localhost"  # Use "broker.hivemq.com" for a public cloud broker
     MQTT_PORT = 1883

     # Topics for inter-agent communication
     LIGHTING_TOPIC = "home/lighting"
     TEMPERATURE_TOPIC = "home/temperature"
     SECURITY_TOPIC = "home/security"
     INVENTORY_TOPIC = "home/inventory"

     # User preferences
     USER_PREFERENCES = {
         "preferred_temp": 22,  # Celsius
         "preferred_brightness": 70,  # Percentage
     }
     ```
   - Set `MQTT_BROKER` to your broker's address (e.g., `"localhost"` for a local broker or `"broker.hivemq.com"` for a public cloud broker).

4. **Optional: Set Up a Local MQTT Broker**:
   - If using `gmqtt`, add a `broker.py` file (see "Using a Local MQTT Broker" below) and run it separately before starting `main.py`.

## Running the System

1. **Start the System**:
   - In the project directory, run:
     ```bash
     python main.py
     ```
   - The system will start all agents and display their status:
     ```
     Starting Smart Home Ecosystem...
     Lighting Agent running...
     Security Agent running...
     Inventory Agent running...
     Enter 'q' to stop the system (press Enter after typing 'q')...
     ```

2. **Interact with the System**:
   - **Lighting Agent**: Detects temperature every 10 seconds (simulated) and adjusts it to the preferred temperature (22°C by default). Publish MQTT messages to control lights or temperature:
     ```bash
     mosquitto_pub -h localhost -t home/lighting -m '{"brightness": 80}'
     mosquitto_pub -h localhost -t home/temperature -m '{"temperature": 20.5}'
     ```
   - **Security Agent**: Detects motion in the camera feed and prints alerts (e.g., "Security Alert: Motion detected in camera feed!").
   - **Inventory Agent**: Checks inventory every 10 seconds (for testing; configurable) and prints low-stock notifications (e.g., "Notification: Low stock on bread, eggs. Please restock.").

3. **Stop the System**:
   - Type `q` and press Enter to stop manually.
   - Press `Ctrl+C` to stop immediately.
   - Wait 5 minutes for automatic shutdown (configurable in `main.py`).

## Using a Local MQTT Broker (Optional)

If you prefer a local broker instead of a cloud-based one:

1. **Create `broker.py`**:
   ```python
   import asyncio
   from gmqtt.mqtt import MQTTBroker

   async def start_broker():
       broker = MQTTBroker()
       await broker.start(host="localhost", port=1883)
       print("Embedded MQTT Broker (gmqtt) started on localhost:1883")

   if __name__ == "__main__":
       asyncio.run(start_broker())
2. Run the Broker:
In a separate terminal, run
- python broker.py
3. Run main.py:
- Ensure MQTT_BROKER = "localhost" in config.py, then run main.py as above.

##  Customization
- Temperature Detection: Replace the simulated detect_temperature method in lighting_agent.py with real sensor readings (e.g., using a DHT11/DHT22 sensor on a Raspberry Pi with the Adafruit_DHT library).
- Hardware Integration: Update adjust_lights and adjust_temperature to control real devices (e.g., via APIs for smart lights or thermostats).
- Inventory: Replace the hardcoded inventory in inventory_agent.py with a database or scanner input.
- Intervals: Adjust temp_check_interval in lighting_agent.py (default: 10 seconds) and check_interval in inventory_agent.py (default: 10 seconds) to suit your needs.

### Example Output
- Starting Smart Home Ecosystem...
- Lighting Agent running...
- Security Agent running...
- Inventory Agent running...
- Enter 'q' to stop the system (press Enter after typing 'q')...
- Notification: Low stock on bread, eggs. Please restock.
- Detected temperature: 26.5°C
- Detected temperature (26.5°C) differs from preferred temperature (22°C).
- Adjusting temperature to 22°C
- q
- Stopping Smart Home Ecosystem...
- Inventory Agent stopped.
- Lighting Agent stopped.
- Security Agent stopped.

## Contributing
- Feel free to fork this project, submit pull requests, or suggest improvements!


