import spacy
from spacy.matcher import Matcher


def shopping_list_extractor(command):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    add_pattern = [
        {"LOWER": {"IN": ["add", "put"]}},
        {"OP": "+"},
        {"LOWER": {"IN": ["to", "on"]}},
        {"OP": "*"},
        {"LOWER": "shopping"},
        {"LOWER": "list"},
    ]
    remove_pattern = [
        {"LOWER": "remove"},
        {"OP": "+"},
        {"LOWER": "from"},
        {"OP": "*"},
        {"LOWER": "shopping"},
        {"LOWER": "list"},
    ]

    matcher.add("ADD", [add_pattern])
    matcher.add("REMOVE", [remove_pattern])

    doc = nlp(command)
    matches = matcher(doc)

    if matches:
        match_id, start, end = matches[0]
        action = "add" if nlp.vocab.strings[match_id] == "ADD" else "remove"

        # Extract the item (all tokens between the action verb and "to/from/on")
        item_start = start + 1  # Start after the action verb
        item_end = next(
            i
            for i, token in enumerate(doc[item_start:], start=item_start)
            if token.text.lower() in ["to", "from", "on"]
        )
        item = " ".join([token.text for token in doc[item_start:item_end]])
        item = item.replace(" '", "'").strip()

        return action, item
    else:
        return None, None


# Test the function
if __name__ == "__main__":
    import time

    commands = [
        "Add milk to the shopping list",
        "Put eggs to the shopping list",
        "Remove trampoline from our shopping list",
        "Can you add bread to the shopping list please?",
        "I need to remove apples from the shopping list",
        "Let's put yellow bananas on our shopping list",
        "Add Weston's pants on our shopping list",
        "Add parents' octopus on our shopping list",
    ]

    for command in commands:

        start = time.time()
        print(f"Command: {command}")
        action, item = shopping_list_extractor(command)
        print(f"Action: {action}, Item: {item}")
        stop = time.time()

        print(f"Time taken: {stop-start}")
        print("-----")
