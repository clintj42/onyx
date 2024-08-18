import os
import traceback
import ollama
import json
from datetime import datetime
from dotenv import load_dotenv
from predict_datetime_tool import predict_datetime_tool, load_model

load_dotenv()

SPEAK_COMMAND = os.getenv("SPEAK_COMMAND")

model, tokenizer = load_model()


def current_datetime(command_text):
    try:
        type = predict_datetime_tool(command_text, model, tokenizer)

        if type == "date_tool_action":
            current_date = datetime.now().date().strftime("%B %d, %Y")
            print(current_date)
            os.system(f'{SPEAK_COMMAND} "Today is {current_date}."')
        elif type == "time_tool_action":
            current_time = (
                datetime.now().time().strftime("%-I %M %p").replace(" 0", " o")
            )
            print(current_time)
            os.system(f'{SPEAK_COMMAND} "The time is {current_time}."')
        elif type == "datetime_tool_action":
            current_date = datetime.now().date().strftime("%B %d, %Y")
            current_time = (
                datetime.now().time().strftime("%-I %M %p").replace(" 0", " o")
            )
            print(current_date, current_time)
            os.system(
                f'{SPEAK_COMMAND} "Today is {current_date} and the time is {current_time}."'
            )
        else:
            current_time = (
                datetime.now().time().strftime("%-I %M %p").replace(" 0", " o")
            )
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
