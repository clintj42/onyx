import spacy
from spacy.matcher import PhraseMatcher
import numerizer


def timer_extractor(command):
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab)
    time_unit_patterns = list(
        nlp.pipe(["second", "seconds", "minute", "minutes", "hour", "hours"])
    )
    matcher.add("TIME_UNIT", time_unit_patterns)

    doc = nlp(command)

    duration = None
    unit = None

    for i, token in enumerate(doc):
        if token.like_num:
            duration = int(numerizer.numerize(token.text))
            break

    matches = matcher(doc)
    for match_id, start, end in matches:
        unit = f"{doc[start:end].lemma_}s"

    return duration, unit


if __name__ == "__main__":
    import time

    commands = [
        "Add milk to the shopping list",
        "Who is the best captain in star trek",
        "tell me a joke",
        "Turn off the basement lights",
        "Play blackbird on spotify",
        "What time is it",
        "What is your favorite color",
        "Set a timer for 20 minutes",
    ]
    for command in commands:

        start = time.time()
        print(f"Command: {command}")
        duration, time_unit = timer_extractor(command)
        print(f"Duration: {duration}, Time Unit: {time_unit}")
        stop = time.time()

        print(f"Time taken: {stop-start}")
        print("-----")
