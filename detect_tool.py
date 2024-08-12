import ollama

def detect_tool(command_text):
    refine_search_prompt = f"""You are a voice assistant similar to Alexa named Onyx. 
    Given a user command, tell me which tool is needed to complete the task. 
    The tools are: no_tool_needed, play_spotify, shopping_list, smart_switch, current_datetime.
    If none of these are needed, return no_tool_needed.
    Return only the tool name. Do not add any additional Notes or Explanations.

    Example Input: Listen to Billy Joel on Spotify. 
    Output: play_spotify
    Example Input: Add milk to my shopping list.
    Output: shopping_list
    Example Input: What is the weather today?
    Output: no_tool_needed
    Example Input: Play Under the Bridge by Red Hot Chili Peppers.
    Output: play_spotify
    Example Input: Remove eggs from my shopping list.
    Output: shopping_list
    Example Input: Turn on the office lamp.
    Output: smart_switch
    Example Input: What time is it?
    Output: current_datetime

    Input: {command_text}"""
    detected_tool = ollama.generate(model='gemma2:2b', prompt=refine_search_prompt)
    return detected_tool['response']

if __name__ == '__main__':
    print(detect_tool("What is the weather today?"))
    print(detect_tool("Play a song on spotify"))
    print(detect_tool("Add cinnamon to my shopping list"))
    print(detect_tool("What is the capital of France?"))
    print(detect_tool("How are you today?"))
    print(detect_tool("Can you play Jupiter Nights on Spotify?"))
    print(detect_tool("Turn off the lights"))
    print(detect_tool("What time is it?"))