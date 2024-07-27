import ollama
import os

def respond(message):
    responseObj = ollama.chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': message,
    }])
    response = responseObj['message']['content']
    streaming_word_clean = response.replace(
            '"', "").replace("\n", " ").replace("'", "").replace("*", "").replace('-', '').replace(':', '').replace('!', '')
    os.system(f"espeak '{streaming_word_clean}'")
    # stream = ollama.chat(model='llama3.1', stream=True, messages=[
    # {
    #     'role': 'user',
    #     'content': message,
    # }])
    # dictate_ollama_stream(stream)

def is_complete_word(text_chunk):
    """
    Given the subword outputs from streaming, as these chunks are added together, check if they form a coherent word. If so, return the word.
    """

    if ' ' in text_chunk or all([x not in text_chunk for x in ['a', 'e', 'i', 'o', 'u']]):
        return True
    return False

def dictate_ollama_stream(stream, early_stopping=False, max_spoken_tokens=250):
    response = ""
    streaming_word = ""
    for i, chunk in enumerate(stream):
        text_chunk = chunk['message']['content']
        streaming_word += text_chunk
        response += text_chunk
        if i > max_spoken_tokens:
            early_stopping = True
            break

        if is_complete_word(text_chunk):
            streaming_word_clean = streaming_word.replace(
                '"', "").replace("\n", " ").replace("'", "").replace("*", "").replace('-', '').replace(':', '').replace('!', '')
            print(streaming_word_clean)
            os.system(f"espeak '{streaming_word_clean}'")
            streaming_word = ""
    if not early_stopping:
        streaming_word_clean = streaming_word.replace(
            '"', "").replace("\n", " ").replace("'", "").replace("*", "").replace('-', '').replace(':', '').replace('!', '')

        os.system(f"espeak '{streaming_word_clean}'")

    return response