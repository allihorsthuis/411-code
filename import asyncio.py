import asyncio
from bt_python_api import BLEClient

SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214"
SENSOR_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"

DEVICE_NAME = "ESP32 alli"

def on_sensor(_sender, data):
    try:
        print(int(data.decode()))
    except:
        print(data)

#main function
async def main ():
    client = BLEClient(
        name=DEVICE_NAME, 
        service_uuid=SERVICE_UUID,
        connect_timeout=15.0,
        scan_timeout=15.0,
        )
    try:
        await client.connect()
        print("connected")
        await client.start_notify(SENSOR_UUID, on_sensor)
        await asyncio.Event().wait()
    finally:
        await client.disconnect()

asyncio.run(main())