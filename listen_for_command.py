import speech_recognition as sr
import librosa
import soundfile as sf
import subprocess
import re
import os
import dotenv

dotenv.load_dotenv()

COMMAND_TIMEOUT = 10
PHRASE_TIME_LIMIT = 7
WHISPER_MODEL_PATH = os.environ['WHISPER_MODEL_PATH']

def transcribe_gguf(whisper_cpp_path, model_path, file_path):
    command = f"./{whisper_cpp_path}main -m {model_path} -f {file_path}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.read()
    output = output.decode('utf-8')
    output = re.sub(r'\[.*?\]', '', output)
    output = re.sub(' +', ' ', output)
    output = output.replace('\n', ' ')
    output = output.strip()

    return output

def transcribe_audio(file_path):
    return transcribe_gguf(whisper_cpp_path="../whisper.cpp/",
                            model_path=WHISPER_MODEL_PATH,
                            file_path=file_path)

def listen_for_command():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Awaiting query...")
            try:
                audio = recognizer.listen(
                    source, timeout=COMMAND_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
            except sr.WaitTimeoutError:
                continue

        try:
            with open(f"sounds/command.wav", "wb") as f:
                f.write(audio.get_wav_data())
            speech, rate = librosa.load(
                f"sounds/command.wav", sr=16000)
            sf.write(f"sounds/command.wav", speech, rate)

            transcription = transcribe_audio(
                file_path=f"sounds/command.wav")

            return transcription
        
        except sr.UnknownValueError:
            print("Could not understand audio")
