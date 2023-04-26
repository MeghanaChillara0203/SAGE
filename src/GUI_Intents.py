"""
GUI.py
The interface and chatbot aspect of the program
"""

# Imports
import tkinter as tk
from PIL import Image, ImageTk
import json
import random
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# use the available CUDA device (GPU) if available, else the CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# Loads pre-trained model/tags from file "data.pth", Returns loaded model/tags
def load_model_and_tags(model_path="data/data.pth"):
    # Load saved data
    data = torch.load(model_path)

    # create new instance of the DistilBertForSequenceClassification model
    model = DistilBertForSequenceClassification.from_pretrained(
        'distilbert-base-uncased', num_labels=len(data["tags"]))
    # load saved state dictionary for the model
    model.load_state_dict(data["model_state"])
    # Move model
    model.to(device)
    # Set model to evaluation mode
    model.eval()

    # reutn model/tags
    return model, data["tags"]


# Predicts the intent of a given sentence using the loaded model, returns corresponding tag
def predict_intent(sentence, model, tags, tokenizer, max_length=128):
    # Tokenize input sentence
    encoding = tokenizer(sentence, max_length=max_length,
                         padding='max_length', truncation=True, return_tensors='pt')
    # extract input_ids tensor from the encoding and move
    input_ids = encoding['input_ids'].to(device)
    # extract and move
    attention_mask = encoding['attention_mask'].to(device)

    # save memory/ speed up inference by disabling gradient calculations
    with torch.no_grad():
        # get outputs from inputs/mask
        outputs = model(input_ids, attention_mask=attention_mask)
        # Get index of max val in the output logits tensor to predict
        _, predicted = torch.max(outputs.logits, 1)

     # return corresponding tag
    return tags[predicted.item()]


# Reads "intents.json", return a dictionary of intents and responses.
def get_intent_responses(intents_path="data/intents.json"):
    with open(intents_path, "r") as file:
        intents = json.load(file)
    intent_responses = {intent["tag"]: intent["responses"]
                        for intent in intents["intents"]}
    return intent_responses


# Define GUI window, widgets, initialize ChatBot
class ChatGUI:
    def __init__(self, master):
        # Initialize window of GUI
        self.master = master
        master.title("Chatbot")
        master.geometry("1000x800")

        # DistilBertTokenizer created from pre-trained tokenizer
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            'distilbert-base-uncased')
        # model and tag values
        self.model, self.tags = load_model_and_tags()
        # Dictionary of responses for each intent in "intents.json"
        self.intent_responses = get_intent_responses()

        # LOGO
        self.logo = Image.open("figs/sage.png")
        self.logo = self.logo.resize((1000, 200), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(master, image=self.logo)
        self.logo_label.place(x=0, y=0)

        # Question
        self.question_label = tk.Label(master, text="Enter your question:")
        self.question_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.question_entry = tk.Entry(master, width=60)
        self.question_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.question_entry.bind('<Return>', self.chat)

        # Chatbot responses
        self.answer_label = tk.Label(master, text="Chatbot response:")
        self.answer_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.answer_text = tk.Text(master, height=10, width=80, wrap=tk.WORD)
        self.answer_text.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.scrollbar = tk.Scrollbar(master, command=self.answer_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.answer_text.config(yscrollcommand=self.scrollbar.set)

        # Exit
        self.quit_button = tk.Button(master, text="Exit", command=master.quit)
        self.quit_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def chat(self, event):
        # Grab quesiotn form text box
        question = self.question_entry.get()
        self.answer_text.delete('1.0', tk.END)
        # Predict intent of the user's question
        intent = predict_intent(question, self.model,
                                self.tags, self.tokenizer)
        # Randomly select response from intent responses
        response = random.choice(self.intent_responses[intent])
        # Give response
        self.answer_text.insert(tk.END, response)

        # Clear the question entry widget
        self.question_entry.delete(0, tk.END)


# GUI running
root = tk.Tk()
my_gui = ChatGUI(root)
root.mainloop()
