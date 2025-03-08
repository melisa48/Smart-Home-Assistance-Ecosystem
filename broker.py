import asyncio
from hbmqtt.broker import Broker

async def start_broker():
    config = {
        "listeners": {
            "default": {
                "type": "tcp",
                "bind": "localhost:1883",  # Same as your config
            },
        },
        "sys_interval": 0,  # Disable system interval to reduce overhead
        "auth": {
            "allow-anonymous": True,  # Allow anonymous connections (for simplicity)
        },
    }
    broker = Broker(config)
    await broker.start()
    print("Embedded MQTT Broker started on localhost:1883")

if __name__ == "__main__":
    asyncio.run(start_broker())