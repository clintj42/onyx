import ollama

conversation_enders = [
    'Have a great day',
    'Goodbye',
    'Take care',
    'Just let me know'
]

def is_expecting_user_response(assistant_response):
    if any(conversation_ender in assistant_response for conversation_ender in conversation_enders):
        return 'no'
    
    refine_search_prompt = f"""
    Tell me if the user is asking for a response back. Respond with "yes" or "no" and nothing else.

    Example Input: My favorite color is blue, what's yours?
    Output: yes
    Example Input: I'm glad to hear you had a fun vacation. Where did you go on your vacation?
    Output: yes
    Example Input: The answer to life the universe and everything is 42
    Output: no
    Example Input: The first president of the United States was George Washington
    Output: no
    Example Input: I hear you, it can feel overwhelming sometimes with everything going on. Tell me more about what's causing you stress. Let's see if we can make a plan to tackle things one step at a time.
    Output: yes
    Example Input: Alright! No problem at all. Have a great day!
    Output: no

    Respond only with the output. Do not add any additional Notes or Explanations.
    
    Input: {assistant_response}
    """
    refined_search = ollama.generate(model='gemma2:2b', prompt=refine_search_prompt)
    return refined_search['response']

if __name__ == '__main__':
    # print(is_expecting_user_response("Hi there! I'm doing great, how are you?"))
    print(is_expecting_user_response("Alright! No problem at all. Have a great day!"))
    # print(is_expecting_user_response("No pressure! Let me know if you have any questions or need help with anything else."))