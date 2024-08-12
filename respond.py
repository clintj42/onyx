import ollama
import dotenv
import emoji
import os
import asyncio
from detect_tool import detect_tool
from play_spotify import play_spotify
from shopping_list import shopping_list
from smart_switch import smart_switch

dotenv.load_dotenv()

SPEAK_COMMAND = os.getenv('SPEAK_COMMAND')

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def respond(message):
    detected_tool = detect_tool(message).strip()
    
    if detected_tool == 'play_spotify':
        play_spotify(message)
        return
    if detected_tool == 'shopping_list':
        shopping_list(message)
        return
    if detected_tool == 'smart_switch':
        asyncio.run(smart_switch(message))
        return

    prompt = f"""
        Act as a personal assistant named Onyx. Given a user command, respond with the appropriate action.
        Your response will be said out loud so keep it short no more than 4 sentences. Also do not include any markdown other punctionation that would not be said out loud.

        User command: {message}
    """
    stream = ollama.chat(model='gemma2:2b', stream=True, options={
        'num_predict': 100
    }, messages=[
    {
        'role': 'user',
        'content': prompt,
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
    is_first_chunk = True
    for i, chunk in enumerate(stream):
        text_chunk = chunk['message']['content']
        streaming_sentence += text_chunk
        response += text_chunk

        if is_complete_sentence(streaming_sentence):
            cleaned_sentence = streaming_sentence.replace('"', "").replace("\n", ". ").replace("*", "").replace('-', '').replace(':', '')
            cleaned_sentence = remove_emojis(cleaned_sentence)
            print(cleaned_sentence)
            if is_first_chunk:
                is_first_chunk = False
                os.system(f"{SPEAK_COMMAND} \"{cleaned_sentence}\"")
            else:
                os.system(f"{SPEAK_COMMAND} \"{cleaned_sentence}\"")
            # wav = tts.tts(text=cleaned_sentence)
            # sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
            # sd.wait() 

            streaming_sentence = ""

    return response
