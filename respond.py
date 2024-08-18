import ollama
import dotenv
import emoji
import os
import asyncio
from tools.play_spotify import play_spotify, should_control_spotify, control_spotify
from tools.shopping_list import shopping_list
from tools.smart_switch import smart_switch
from tools.current_datetime import current_datetime
from tools.set_timer import set_timer, should_stop_timer, stop_timer
from listen_for_command import listen_for_command
from predict_tool import predict_tool, load_model

dotenv.load_dotenv()

model, tokenizer = load_model()

SPEAK_COMMAND = os.getenv('SPEAK_COMMAND')
conversation_enders = [
    'stop',
    'exit',
    'quit',
    'goodbye',
    'bye',
    'done',
]

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def respond(message, conversation=[]):
    if should_stop_timer(message):
        stop_timer()
        return
    if should_control_spotify(message):
        control_spotify(message)
        return

    detected_tool = predict_tool(message, model, tokenizer).strip()

    print("Detected Tool: ", detected_tool)
    
    if detected_tool == 'play_spotify':
        play_spotify(message)
        return
    if detected_tool == 'shopping_list':
        shopping_list(message)
        return
    if detected_tool == 'smart_switch':
        asyncio.run(smart_switch(message))
        return
    if detected_tool == 'current_datetime':
        current_datetime(message)
        return
    if detected_tool == 'set_timer':
        set_timer(message)
        return
    
    if any([message.lower().startswith(ender) for ender in conversation_enders]):
        return

    prompt = f"""
        Act as a personal assistant named Onyx. Given a user command, respond with the appropriate action.
        Your response will be said out loud so keep it short no more than 4 sentences. Also do not include any markdown other punctionation that would not be said out loud.

        User command: {message}
    """

    user_message = {
        'role': 'user',
        'content': prompt,
    }

    stream = ollama.chat(model='gemma2:2b', stream=True, keep_alive=-1, options={
        'num_predict': 100
    }, messages=conversation + [user_message])
    response = dictate_ollama_stream(stream)

    if "?" in response:
        os.system(f"play -v .1 sounds/notification.wav")
        command = listen_for_command()
        print("Command: ", command)
        respond(command, conversation=conversation + [user_message, {'role': 'assistant', 'content': response}])

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
            cleaned_sentence = streaming_sentence.replace('"', "").replace("\n", ". ").replace("*", "").replace('-', '').replace(':', '')
            cleaned_sentence = remove_emojis(cleaned_sentence)
            print(cleaned_sentence)
            os.system(f"{SPEAK_COMMAND} \"{cleaned_sentence}\"")
            # wav = tts.tts(text=cleaned_sentence)
            # sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
            # sd.wait() 

            streaming_sentence = ""

    return response
