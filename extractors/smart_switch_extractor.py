import spacy
from spacy.matcher import Matcher


def smart_switch_extractor(command):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    # Define patterns for turning devices on and off
    turn_on_pattern = [{"LOWER": "turn"}, {"LOWER": "on"}, {"OP": "*"}]
    turn_off_pattern = [{"LOWER": "turn"}, {"LOWER": "off"}, {"OP": "*"}]

    matcher.add("TURN_ON", [turn_on_pattern])
    matcher.add("TURN_OFF", [turn_off_pattern])

    doc = nlp(command)
    matches = matcher(doc)

    if matches:
        match_id, start, end = matches[0]
        action = "on" if nlp.vocab.strings[match_id] == "TURN_ON" else "off"

        # Extract the device name (all tokens after "on/off")
        device_start = start + 2  # Start after "turn on/off"
        device_name = " ".join(
            [
                token.text
                for token in doc[device_start:]
                if token.text.lower() not in ["the", "a", "an", "?", "."]
            ]
        )

        return action, device_name.strip()
    else:
        return None, None


# Test the function
if __name__ == "__main__":
    import time

    commands = [
        "Turn on the office lamp.",
        "Turn off the home theater lights",
        "Can you turn on the kitchen light?",
        "Please turn off the bedroom lamp",
        "Turn on the living room lights",
        "Turn off all the lights in the house",
        "Turn on the TV",
        "Turn off the projector",
        "Can you turn on the smart speaker?",
        "Turn off the thermostat",
        "Please turn on the ceiling fan",
        "Turn on the coffee maker",
        "Turn off the garage door",
    ]

    for command in commands:

        start = time.time()
        print(f"Command: {command}")
        action, item = smart_switch_extractor(command)
        print(f"Action: {action}, Item: {item}")
        stop = time.time()

        print(f"Time taken: {stop-start}")
        print("-----")
