from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from numpy import exp, sum

key_tools = ['shopping_list', 'no_tool_needed', 'current_datetime', 'smart_switch', 'play_spotify', 'set_timer']


TOOL_THRESHOLD = .95


def get_id2tool_name(id, key_tools):
    return key_tools[id]


def softmax(x):
    return exp(x) / sum(exp(x), axis=0)


def remove_any_non_alphanumeric_characters(text):
    return ''.join(e for e in text if e.isalnum() or e.isspace())


def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained("clintj42/tool-bert")

    model.eval()
    return model, tokenizer


def predict_tool(question, model, tokenizer):
    question = remove_any_non_alphanumeric_characters(question)
    inputs = tokenizer(question, return_tensors="pt")

    outputs = model(**inputs)

    logits = outputs.logits.detach().numpy()

    probability = softmax(logits[0]).max()

    if probability < TOOL_THRESHOLD:
        return 'no_tool_needed'
    return get_id2tool_name(logits.argmax().item(), key_tools)


if __name__ == "__main__":
    import time

    model, tokenizer = load_model()

    questions = ["Add milk to the shopping list", "Who is the best captain in star trek", "tell me a joke", "Turn off the basement lights",
                "Play blackbird on spotify", "What time is it", "What is your favorite color", "Set a timer for 20 minutes"]
    for question in questions:

        start = time.time()
        print(f"Question: {question}")
        print(f"Tool: {predict_tool(question, model, tokenizer)}")
        stop = time.time()

        print(f"Time taken: {stop-start}")
        print('-----')
