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
