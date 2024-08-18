from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from numpy import exp, sum

key_tools = ['no_tool_needed', 'time_tool_action', 'date_tool_action', 'datetime_tool_action']


TOOL_THRESHOLD = .95


def get_id2tool_name(id, key_tools):
    return key_tools[id]


def softmax(x):
    return exp(x) / sum(exp(x), axis=0)


def remove_any_non_alphanumeric_characters(text):
    return ''.join(e for e in text if e.isalnum() or e.isspace())


def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained("clintj42/datetime-tool")

    model.eval()
    return model, tokenizer


def predict_datetime_tool(question, model, tokenizer):
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

    questions = ["What is the time", "What's today?", "What is the date and time", "What is the current time", "What time is it"]
    for question in questions:

        start = time.time()
        print(f"Question: {question}")
        print(f"Tool: {predict_tool(question, model, tokenizer)}")
        stop = time.time()

        print(f"Time taken: {stop-start}")
        print('-----')
