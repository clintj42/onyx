import asyncio
import os
from kasa import Discover
from dotenv import load_dotenv
from extractors.smart_switch_extractor import smart_switch_extractor

# To add a new smart switch:
# 1. Run kasa devices
# 2. Add the device name and ip address to the kasa_devices dictionary

load_dotenv()

kasa_username = os.getenv("KASA_USERNAME")
kasa_password = os.getenv("KASA_PASSWORD")
SPEAK_COMMAND = os.getenv("SPEAK_COMMAND")

kasa_devices = {
    "lights": "192.168.0.102",
    "theater lights": "192.168.0.102",
    "basement lights": "192.168.0.102",
    "office lamp": "192.168.0.8",
}


async def find_device_by_name(target_name):
    try:
        ip = kasa_devices.get(target_name)
        if ip is None:
            return None
        return await Discover.discover_single(
            ip, username=kasa_username, password=kasa_password
        )
    except Exception as e:
        print(e)
        return None


async def smart_switch(command_text):
    action, device_name = smart_switch_extractor(command_text)

    print("Device Name: ", device_name)
    print("Action: ", action)

    device = await find_device_by_name(device_name)

    if device is None:
        os.system(
            f'{SPEAK_COMMAND} "Could not find the device named {device_name}. Make sure your voice assistant is on the same network as the device."'
        )
        return

    if action == "on":
        await device.turn_on()
        await device.update()
    elif action == "off":
        await device.turn_off()
        await device.update()
    else:
        os.system(
            f'{SPEAK_COMMAND} "I am not sure what you want me to do with {device_name}."'
        )


if __name__ == "__main__":
    asyncio.run(smart_switch("Turn on the office lamp."))
    # asyncio.run(smart_switch("Turn off the theater lights."))
