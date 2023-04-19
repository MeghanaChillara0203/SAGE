import tkinter as tk
from PIL import Image, ImageTk
import json
import random
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_model_and_tags(model_path="data.pth"):
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


def get_intent_responses(intents_path="intents.json"):
    with open(intents_path, "r") as file:
        intents = json.load(file)
    intent_responses = {intent["tag"]: intent["responses"] for intent in intents["intents"]}
    return intent_responses


class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        master.geometry("600x800")

        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model, self.tags = load_model_and_tags()
        self.intent_responses = get_intent_responses()

        self.logo = Image.open("logo.png")
        self.logo = self.logo.resize((600, 200), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(master, image=self.logo)
        self.logo_label.pack()

        self.question_label = tk.Label(master, text="Enter your question:")
        self.question_label.pack()

        self.question_entry = tk.Entry(master)
        self.question_entry.pack()
        self.question_entry.bind('<Return>', self.chat)

        self.answer_label = tk.Label(master, text="Chatbot response:")
        self.answer_label.pack()

        self.answer_text = tk.Text(master, height=20, width=80, wrap=tk.WORD)
        self.answer_text.pack()

        self.scrollbar = tk.Scrollbar(master, command=self.answer_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.answer_text.config(yscrollcommand=self.scrollbar.set)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(side=tk.BOTTOM)

    def chat(self, event):
        question = self.question_entry.get()
        self.answer_text.delete('1.0', tk.END)
        intent = predict_intent(question, self.model, self.tags, self.tokenizer)
        response = random.choice(self.intent_responses[intent])
        self.answer_text.insert(tk.END, response)

        # Clear the question entry widget
        self.question_entry.delete(0, tk.END)


root = tk.Tk()
my_gui = ChatGUI(root)
root.mainloop()
