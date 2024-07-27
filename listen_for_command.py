import speech_recognition as sr
import librosa
import soundfile as sf
import subprocess
import re
import os

COMMAND_TIMEOUT = 10
PHRASE_TIME_LIMIT = 7

def check_if_exit(transcription):
    """
    Check if the transcription is an exit command.
    """
    return any([x in transcription.lower() for x in ["stop", "exit", "quit"]])


def check_if_ignore(transcription):
    """
    Check if the transcription should be ignored. 
    This happens if the whisper prediction is "you" or "." or "", or is some sound effect like wind blowing, usually inside parentheses.
    These are things caused by having the fan so close to the microphone, definitely need to fix.
    """
    if transcription.strip().lower() == "you" or transcription.strip() == "." or transcription.strip() == "":
        return True
    if re.match(r"\(.*\)", transcription):
        return True
    return False

def remove_parentheses(transcription):
    """
    Remove parentheses and their contents from the transcription.
    """
    return re.sub(r"\(.*\)", "", transcription).strip()

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
                            model_path="/Users/clintjohnson/personal_projects/whisper.cpp/models/ggml-base.en.bin",
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
            
            if check_if_ignore(transcription):
                continue

            if check_if_exit(transcription):
                os.system(
                    f"espeak 'Program stopped. See you later!'")
                # set message history to empty
                # self.message_history = [self.message_history[0]]
                return

            else:
                transcription = remove_parentheses(transcription)
                return transcription
                # _, self.message_history = get_llm_response(
                #     transcription, self.message_history, model_name=self.ollama_model)

            # save appended message history to json
            # if self.store_conversations:
            #     with open(f"storage/{self.conversation_id}.json", "w") as f:
            #         json.dump(self.message_history, f, indent=4)

        except sr.UnknownValueError:
            print("Could not understand audio")
