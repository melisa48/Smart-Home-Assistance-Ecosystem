import cv2
import paho.mqtt.client as mqtt
import json
import time
from config import MQTT_BROKER, MQTT_PORT, SECURITY_TOPIC

class SecurityAgent:
    def __init__(self, camera_index=0):
        self.client = mqtt.Client()
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except ConnectionRefusedError as e:
            print(f"Failed to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}. Error: {e}")
            print("Please ensure the MQTT broker is running and the address/port are correct.")
            exit(1)
        self.camera = cv2.VideoCapture(camera_index)
        self.prev_frame = None
        self.running = False
        self.last_alert_time = 0
        self.alert_cooldown = 5  # Seconds between alerts (adjustable)

    def detect_motion(self):
        ret, frame = self.camera.read()
        if not ret:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.prev_frame is None:
            self.prev_frame = gray
            return False

        frame_delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.prev_frame = gray
        return len(contours) > 0

    def publish_alert(self, alert_message):
        current_time = time.time()
        if current_time - self.last_alert_time >= self.alert_cooldown:
            message = json.dumps({"alert": alert_message})
            self.client.publish(SECURITY_TOPIC, message)
            print(f"Security Alert: {alert_message}")
            self.last_alert_time = current_time

    def run(self):
        print("Security Agent running...")
        self.running = True
        self.client.loop_start()  # Start the MQTT loop in a background thread
        while self.running:
            if self.detect_motion():
                self.publish_alert("Motion detected in camera feed!")
            if cv2.waitKey(100) & 0xFF == ord('q'):  # Allow stopping via 'q' key in OpenCV window (optional)
                self.stop()
                break
        self.client.loop_stop()  # Stop the MQTT loop
        self.camera.release()  # Release the camera
        cv2.destroyAllWindows()  # Close any OpenCV windows
        print("Security Agent stopped.")

    def stop(self):
        self.running = False

if __name__ == "__main__":
    agent = SecurityAgent()
    agent.run()