import os
import ollama
import json
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import traceback

load_dotenv()

todoist_api_key = os.getenv('TODOIST_API_KEY')
project_id = os.getenv('TODOIST_PROJECT_ID')
SPEAK_COMMAND = os.getenv('SPEAK_COMMAND')

api = TodoistAPI(todoist_api_key)

def shopping_list_command(command_text):
    prompt = f"""
    Given a user command return a json object in the following schema:
    {{
        "action": "add|remove|none",
        "item": "item_name"
    }}

    Example Input: Add milk to my shopping list.
    Output: {{ "action": "add", "item": "milk" }}
    Example Input: Remove eggs from my shopping list.
    Output: {{ "action": "remove", "item": "eggs" }}
    Example Input: Jump puzzle from our shopping list.
    Output: {{ "action": "none", "item": "puzzle" }}

    Do not add any additional Notes or Explanations. Correct any obvious spelling mistakes in the input.

    User command: {command_text}
    """
    retrieved_shopping_list_command = ollama.generate(model='gemma2:2b', prompt=prompt)
    return retrieved_shopping_list_command['response']

def shopping_list(command_text):
    try:
        shopping_list_command_str = shopping_list_command(command_text)
        shopping_list_command_str = shopping_list_command_str.replace('```json', '').replace('`', '').replace('""', '"').strip()
        
        try:
            shopping_list_command_json = json.loads(shopping_list_command_str)
        except Exception as e:
            print("Received: ", shopping_list_command_str)
            print(e)
            traceback.print_exc()
            os.system(f'{SPEAK_COMMAND} "An error occurred while parsing the shopping list command."')
            return
        action = shopping_list_command_json['action']
        item = shopping_list_command_json['item']

        print("Action: ", action)
        print("Item: ", item)

        if action == 'add':
            tasks = api.get_tasks(project_id=project_id)
            for task in tasks:
                if task.content.lower() == item.lower():
                    os.system(f"{SPEAK_COMMAND} 'You already have {item} on your shopping list'")
                    return
            api.add_task(project_id=project_id, content=item)
            os.system(f"{SPEAK_COMMAND} 'I have added {item} to your shopping list'")
        elif action == 'remove':
            tasks = api.get_tasks(project_id=project_id)
            for task in tasks:
                if task.content.lower() == item.lower():
                    api.close_task(task.id)
                    os.system(f"{SPEAK_COMMAND} 'I have removed {item} from your shopping list'")
                    return
            system_response = f"You don't have {item} on your shopping list"
            os.system(f'{SPEAK_COMMAND} "{system_response}"')
        else:
            os.system(f'{SPEAK_COMMAND} "I am not sure what you want me to do with {item}."')
    except Exception as e:
        print(e)
        traceback.print_exc()
        os.system(f'{SPEAK_COMMAND} "An error occurred while modifying shopping list."')


if __name__ == '__main__':
    # print(shopping_list("Add milk to my shopping list"))
    # print(shopping_list("Remove eggs from my shopping list"))
    print(shopping_list("Flex Africa shopping list"))