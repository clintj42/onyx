import os
import ollama
import json
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import traceback
from extractors.shopping_list_extractor import shopping_list_extractor

load_dotenv()

todoist_api_key = os.getenv("TODOIST_API_KEY")
project_id = os.getenv("TODOIST_PROJECT_ID")
SPEAK_COMMAND = os.getenv("SPEAK_COMMAND")

api = TodoistAPI(todoist_api_key)


def shopping_list(command_text):
    try:
        action, item = shopping_list_extractor(command_text)

        print("Action: ", action)
        print("Item: ", item)

        if action == "add":
            tasks = api.get_tasks(project_id=project_id)
            for task in tasks:
                if task.content.lower() == item.lower():
                    os.system(
                        f'{SPEAK_COMMAND} "You already have {item} on your shopping list"'
                    )
                    return
            api.add_task(project_id=project_id, content=item)
            os.system(f'{SPEAK_COMMAND} "I have added {item} to your shopping list"')
        elif action == "remove":
            tasks = api.get_tasks(project_id=project_id)
            for task in tasks:
                if task.content.lower() == item.lower():
                    api.close_task(task.id)
                    os.system(
                        f'{SPEAK_COMMAND} "I have removed {item} from your shopping list"'
                    )
                    return
            system_response = f"You don't have {item} on your shopping list"
            os.system(f'{SPEAK_COMMAND} "{system_response}"')
        else:
            os.system(
                f'{SPEAK_COMMAND} "I am not sure what you want me to do with {item}."'
            )
    except Exception as e:
        print(e)
        traceback.print_exc()
        os.system(f'{SPEAK_COMMAND} "An error occurred while modifying shopping list."')


if __name__ == "__main__":
    print(shopping_list("Add milk to my shopping list"))
    # print(shopping_list("Remove eggs from my shopping list"))
    # print(shopping_list("Flex Africa shopping list"))
