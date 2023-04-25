import json
import random
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model_and_tags(model_path="SAGE - Without UI/data.pth"):
    data = torch.load(model_path)

    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=len(data["tags"]))
    model.load_state_dict(data["model_state"])
    model.to(device)
    model.eval()

    return model, data["tags"]

def predict_intent(sentence, model, tags, tokenizer, max_length=128):
    encoding = tokenizer(sentence, max_length=max_length, padding='max_length', truncation=True, return_tensors='pt')
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        _, predicted = torch.max(outputs.logits, 1)

    return tags[predicted.item()]

def get_intent_responses(intents_path="SAGE - Without UI/intents.json"):
    with open(intents_path, "r") as file:
        intents = json.load(file)
    intent_responses = {intent["tag"]: intent["responses"] for intent in intents["intents"]}
    return intent_responses

def chat(model, tags):
    print("Let's chat! (type 'quit' to exit)")

    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    intent_responses = get_intent_responses()

    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        intent = predict_intent(sentence, model, tags, tokenizer)
        response = random.choice(intent_responses[intent])
        print(f"SAGE: {response}")

if __name__ == "__main__":
    model, tags = load_model_and_tags()
    chat(model, tags)
