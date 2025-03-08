import threading
import time
import sys
from lighting_agent import LightingAgent
from security_agent import SecurityAgent
from inventory_agent import InventoryAgent

# Global flag to control running state
running = True

def start_lighting_agent(agent):
    agent.run()

def start_security_agent(agent):
    agent.run()

def start_inventory_agent(agent):
    agent.run()

def stop_system(agents):
    global running
    running = False
    for agent in agents:
        agent.stop()
    print("Stopping Smart Home Ecosystem...")

def auto_stop(agents, duration_seconds):
    """Automatically stop the system after a set duration."""
    time.sleep(duration_seconds)
    stop_system(agents)

def manual_stop(agents):
    """Stop the system when the user enters 'q'."""
    global running
    print("Enter 'q' to stop the system (press Enter after typing 'q')...")
    while running:
        try:
            user_input = input().strip().lower()
            if user_input == 'q':
                stop_system(agents)
                break
        except EOFError:
            pass  # Handle EOF errors in some terminals
        time.sleep(0.1)

if __name__ == "__main__":
    print("Starting Smart Home Ecosystem...")
    # Create agent instances
    lighting_agent = LightingAgent()
    security_agent = SecurityAgent()
    inventory_agent = InventoryAgent()
    agents = [lighting_agent, security_agent, inventory_agent]

    # Start each agent in a separate thread
    lighting_thread = threading.Thread(target=start_lighting_agent, args=(lighting_agent,))
    security_thread = threading.Thread(target=start_security_agent, args=(security_agent,))
    inventory_thread = threading.Thread(target=start_inventory_agent, args=(inventory_agent,))

    # Set threads as daemon so they exit when the main thread exits
    lighting_thread.daemon = True
    security_thread.daemon = True
    inventory_thread.daemon = True

    lighting_thread.start()
    security_thread.start()
    inventory_thread.start()

    # Option 1: Automatic stop after 5 minutes (300 seconds)
    auto_stop_thread = threading.Thread(target=auto_stop, args=(agents, 300))
    auto_stop_thread.daemon = True
    auto_stop_thread.start()

    # Option 2: Manual stop by entering 'q'
    try:
        manual_stop(agents)
    except KeyboardInterrupt:
        print("\nReceived Ctrl+C, stopping the system...")
        stop_system(agents)

    # Wait for all threads to complete (though daemon threads will exit when main thread exits)
    for thread in [lighting_thread, security_thread, inventory_thread, auto_stop_thread]:
        thread.join()

    print("Smart Home Ecosystem stopped.")