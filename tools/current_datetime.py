import os
import traceback
import ollama
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SPEAK_COMMAND = os.getenv('SPEAK_COMMAND')

def specific_tool(command_text):
    refine_search_prompt = f"""Given the command for current date and time, return a json object in the following schema:
    {{
        "type": "date|time|date,time|none"
    }}

    Example Input: Tell me the current date and time. 
    Output: {{ "type": "date,time" }}
    Example Input: What time is it? 
    Output: {{ "type": "time" }}
    Example Input: How many people are there in the world?
    Output: {{ "type": "none" }}
    Example Input: What is the current date?
    Output: {{ "type": "date" }}

    Respond only with the output. Do not add any additional Notes or Explanations.

    Input: {command_text}"""
    refined_search = ollama.generate(model='gemma2:2b', prompt=refine_search_prompt)
    return refined_search['response']

def current_datetime(command_text):
    try:
        specific_tool_str = specific_tool(command_text)
        specific_tool_str = specific_tool_str.replace('```json', '').replace('`', '').replace('""', '"').strip()
        specific_tool_json = json.loads(specific_tool_str)
        type = specific_tool_json['type']

        if type == 'date':
            current_date = datetime.now().date().strftime("%B %d, %Y")
            print(current_date)
            os.system(f'{SPEAK_COMMAND} "Today is {current_date}."')
        elif type == 'time':
            current_time = datetime.now().time().strftime("%-I %M %p").replace(" 0", " o")
            print(current_time)
            os.system(f'{SPEAK_COMMAND} "The time is {current_time}."')
        elif type == 'date,time':
            current_date = datetime.now().date().strftime("%B %d, %Y")
            current_time = datetime.now().time().strftime("%-I %M %p").replace(" 0", " o")
            print(current_date, current_time)
            os.system(f'{SPEAK_COMMAND} "Today is {current_date} and the time is {current_time}."')
        else:
            current_time = datetime.now().time().strftime("%-I %M %p").replace(" 0", " o")
            print(current_time)
            os.system(f'{SPEAK_COMMAND} "The time is {current_time}."')
    except Exception as e:
        print(e)
        traceback.print_exc()
        os.system(f'{SPEAK_COMMAND} "Failed to say the time."')

if __name__ == "__main__":
    current_datetime("What time is it?")
    # current_datetime("Tell me the current date and time.")
    # current_datetime("What is the current date?")
    # current_datetime("How many people are there in the world?")