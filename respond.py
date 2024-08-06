import ollama
import dotenv
from TTS.api import TTS
import sounddevice as sd
import emoji

dotenv.load_dotenv()

tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def respond(message):
    stream = ollama.chat(model='gemma2:2b', stream=True, messages=[
    {
        'role': 'user',
        'content': message,
    }])
    dictate_ollama_stream(stream)

def is_complete_word(text_chunk):
    """
    Given the subword outputs from streaming, as these chunks are added together, check if they form a coherent word. If so, return the word.
    """

    if ' ' in text_chunk or all([x not in text_chunk for x in ['a', 'e', 'i', 'o', 'u']]):
        return True
    return False

def is_complete_sentence(text):
    return any(text.strip().endswith(punct) for punct in ['.', '!', '?'])

def dictate_ollama_stream(stream):
    response = ""
    streaming_sentence = ""
    for i, chunk in enumerate(stream):
        text_chunk = chunk['message']['content']
        streaming_sentence += text_chunk
        response += text_chunk

        if is_complete_sentence(streaming_sentence):
            cleaned_sentence = remove_emojis(streaming_sentence)
            print(cleaned_sentence)
            wav = tts.tts(text=cleaned_sentence)
            sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
            sd.wait() 

            streaming_sentence = ""

    return response
