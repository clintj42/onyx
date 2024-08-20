import os
import traceback
import ollama
import json
import threading
from dotenv import load_dotenv
from extractors.timer_extractor import timer_extractor

load_dotenv()

SPEAK_COMMAND = os.getenv("SPEAK_COMMAND")
NUM_SECONDS_IN_MINUTE = 60
NUM_SECONDS_IN_HOUR = 60 * NUM_SECONDS_IN_MINUTE
MAX_TIMER_SECONDS = 24 * NUM_SECONDS_IN_HOUR

timer_thread = None

timer_enders = [
    "stop",
    "please stop",
    "cancel",
    "clear",
    "reset",
    "stop timer",
    "cancel timer",
    "clear timer",
    "reset timer",
    "stop the timer",
    "cancel the timer",
    "clear the timer",
    "reset the timer",
]


def should_stop_timer(command_text):
    global timer_thread
    if timer_thread and any(
        [command_text.lower().startswith(ender) for ender in timer_enders]
    ):
        return True
    return False


def stop_timer():
    global timer_thread
    if timer_thread is not None:
        timer_thread.cancel()
        timer_thread = None
        os.system(f'{SPEAK_COMMAND} "Stopping the timer."')
    else:
        os.system(f'{SPEAK_COMMAND} "No timer is currently running."')


def start_timer(seconds):
    global timer_thread

    def timer_done():
        global timer_thread
        timer_thread = None
        os.system(f"play -v .1 sounds/buzzer.wav")

    timer_thread = threading.Timer(seconds, timer_done)
    timer_thread.start()


def set_timer(command_text):
    global timer_thread

    try:
        time_value, time_unit = timer_extractor(command_text)

        print("time_unit", time_unit)
        print("time_value", time_value)

        num_seconds_for_timer = 0

        if time_unit == "seconds":
            num_seconds_for_timer = time_value
        elif time_unit == "minutes":
            num_seconds_for_timer = time_value * NUM_SECONDS_IN_MINUTE
        elif time_unit == "hours":
            num_seconds_for_timer = time_value * NUM_SECONDS_IN_HOUR

        if num_seconds_for_timer > 0 and num_seconds_for_timer <= MAX_TIMER_SECONDS:
            if timer_thread is not None:
                os.system(f'{SPEAK_COMMAND} "A timer is already running."')
                return
            else:
                os.system(f'{SPEAK_COMMAND} "{time_value} {time_unit} starting now"')
                start_timer(num_seconds_for_timer)
        elif num_seconds_for_timer > MAX_TIMER_SECONDS:
            os.system(f'{SPEAK_COMMAND} "The maximum timer value is 24 hours."')
        else:
            os.system(
                f'{SPEAK_COMMAND} "Cannot set timer for {time_value} {time_unit}."'
            )

    except Exception as e:
        print(e)
        traceback.print_exc()
        os.system(f'{SPEAK_COMMAND} "Failed to set the timer."')


if __name__ == "__main__":
    set_timer("Set a timer for 10 seconds.")
    # set_timer("Set a timer for 5 minutes.")
    # set_timer("Set a timer for 3 hours.")
    # set_timer("Set a timer for 1 day.")
    # set_timer("Set a timer for one million seconds")
