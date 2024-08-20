import os
import struct
import dotenv
import ollama
from datetime import datetime
from listen_for_command import listen_for_command
from respond import respond
import pvporcupine
from pvrecorder import PvRecorder
from tools.play_spotify import turn_volume_back_up

dotenv.load_dotenv()

PORCUPINE_ACCESS_KEY = os.environ["PORCUPINE_ACCESS_KEY"]
KEYWORD_FILE_PATH = os.environ["KEYWORD_FILE_PATH"]
SPEAK_COMMAND = os.environ["SPEAK_COMMAND"]


def main():
    # Preload gemma2:2b model
    print("Preloading gemma2:2b model")
    ollama.chat(model="gemma2:2b", messages=[], keep_alive=-1)

    try:
        porcupine = pvporcupine.create(
            access_key=PORCUPINE_ACCESS_KEY, keyword_paths=[KEYWORD_FILE_PATH]
        )
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine")
        raise e

    print("Porcupine version: %s" % porcupine.version)

    recorder = PvRecorder(frame_length=porcupine.frame_length, device_index=-1)
    recorder.start()

    wav_file = None

    os.system(f"{SPEAK_COMMAND} 'Ready for action sir!'")
    print("Listening ... (press Ctrl+C to exit)")

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

            if result >= 0:
                print("[%s] Detected Onyx" % (str(datetime.now())))
                command, spotify_volume = listen_for_command()
                print("Command: ", command)
                respond(command)
                if spotify_volume is not None and spotify_volume > 0:
                    turn_volume_back_up(spotify_volume)
                print("Listening ... (press Ctrl+C to exit)")
    except KeyboardInterrupt:
        print("Stopping ...")
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()


if __name__ == "__main__":
    main()
