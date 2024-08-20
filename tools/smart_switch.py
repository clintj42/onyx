import asyncio
import ollama
import os
import json
import traceback
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

# def command_request(command_text):
#     prompt = f"""
#     Given a user command return a json object in the following schema:
#     {{
#         "device_name": "device_name",
#         "action": "on|off|none"
#     }}

#     Example Input: Turn on the office lamp.
#     Output: {{ "device_name": "office lamp", "action": "on" }}
#     Example Input: Turn off the living room tv
#     Output: {{ "device_name": "living room tv", "action": "off" }}
#     Example Input: Turn over the entire house
#     Output: {{ "device_name": "entire house", "action": "none" }}

#     Do not add any additional Notes or Explanations. Correct any obvious spelling mistakes in the input.

#     User command: {command_text}
#     """
#     retrieved_smart_switch_command = ollama.generate(model='gemma2:2b', prompt=prompt)
#     return retrieved_smart_switch_command['response']


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
    # command_request_str = command_request(command_text)
    # command_request_str = command_request_str.replace('```json', '').replace('`', '').replace('""', '"').strip()

    # try:
    #     smart_switch_command_json = json.loads(command_request_str)
    # except Exception as e:
    #     print("Received: ", command_request_str)
    #     print(e)
    #     traceback.print_exc()
    #     os.system(f'{SPEAK_COMMAND} "An error occurred while parsing the smart switch command."')
    #     return

    # device_name = smart_switch_command_json['device_name']
    # action = smart_switch_command_json['action']

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
