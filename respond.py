import ollama
import os

def respond(message):
    stream = ollama.chat(model='llama3.1', stream=True, messages=[
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
    return any(text.endswith(punct) for punct in ['.', '!', '?'])

def dictate_ollama_stream(stream, early_stopping=False, max_spoken_tokens=250):
    response = ""
    streaming_sentence = ""
    for i, chunk in enumerate(stream):
        text_chunk = chunk['message']['content']
        streaming_sentence += text_chunk
        response += text_chunk
        if i > max_spoken_tokens:
            early_stopping = True
            break

        if is_complete_sentence(streaming_sentence):
            streaming_sentence_clean = streaming_sentence.replace(
                '"', "").replace("\n", " ").replace("'", "").replace("*", "").replace('-', '').replace(':', '')
            print(streaming_sentence_clean)
            os.system(f"say '{streaming_sentence_clean}'")
            streaming_sentence = ""

    if not early_stopping and streaming_sentence:
        streaming_sentence_clean = streaming_sentence.replace(
            '"', "").replace("\n", " ").replace("'", "").replace("*", "").replace('-', '').replace(':', '')

        os.system(f"say '{streaming_sentence_clean}'")

    return response