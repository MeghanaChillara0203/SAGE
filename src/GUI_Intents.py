import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import random
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import time
import os

# Use CUDA if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load pre-trained model/tags
def load_model_and_tags(model_path="data/data.pth"):
    if not os.path.exists(model_path):
        print("⚠️ Model file not found! Please check the path:", model_path)
        return None, None

    data = torch.load(model_path, map_location=device)

    try:
        model = DistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased', num_labels=len(data["tags"])
        )
        model.load_state_dict(data["model_state"])
        model.to(device)
        model.eval()
    except Exception as e:
        print("⚠️ Error loading model:", e)
        return None, None

    return model, data["tags"]

# Predict intent with rate limiting
def predict_intent(sentence, model, tags, tokenizer, max_length=128):
    time.sleep(1)  # Prevent overloading

    if model is None or tags is None:
        return "I'm having trouble understanding you right now."

    encoding = tokenizer(sentence, max_length=max_length, padding='max_length', truncation=True, return_tensors='pt')
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        _, predicted = torch.max(outputs.logits, 1)

    return tags[predicted.item()]

# Read intents.json
def get_intent_responses(intents_path="data/intents.json"):
    if not os.path.exists(intents_path):
        print("⚠️ Intents file not found! Please check:", intents_path)
        return {}

    with open(intents_path, "r") as file:
        intents = json.load(file)
    return {intent["tag"]: intent["responses"] for intent in intents["intents"]}

# Chatbot GUI
class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("SAGE AI Chatbot")
        master.geometry("400x600")
        master.configure(bg="white")

        # Load chatbot icon
        self.bot_icon = Image.open("figs/sage.png")  # Ensure this file exists
        self.bot_icon = self.bot_icon.resize((30, 30), Image.LANCZOS)
        self.bot_photo = ImageTk.PhotoImage(self.bot_icon)

        # Header
        self.header = tk.Label(master, text="SAGE AI Chatbot", font=("Helvetica", 14, "bold"), fg="white", bg="#0078D4", padx=10, pady=10)
        self.header.pack(fill="x")

        # Chat Display (Bubble Messages)
        self.chat_frame = tk.Frame(master, bg="white")
        self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.chat_canvas = tk.Canvas(self.chat_frame, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, command=self.chat_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_canvas.config(yscrollcommand=self.scrollbar.set)

        self.chat_box = tk.Frame(self.chat_canvas, bg="white")
        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_box, anchor="nw")
        self.chat_box.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        # User Input
        self.input_frame = tk.Frame(master, bg="white")
        self.input_frame.pack(pady=5, fill="x", padx=10)

        self.entry = ttk.Entry(self.input_frame, font=("Helvetica", 12))
        self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.entry.bind("<Return>", self.chat)

        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.chat, style="TButton")
        self.send_button.pack(side="right", padx=5)

        # Exit Button
        self.exit_button = ttk.Button(master, text="Exit", command=master.quit, style="TButton")
        self.exit_button.pack(pady=5)

        # Load chatbot model
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model, self.tags = load_model_and_tags()
        self.intent_responses = get_intent_responses()

        # Chatbot greets first
        self.display_message("SAGE", "Hi there! I'm SAGE, your AI assistant. How can I help you today?")

    def chat(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return

        # Display user message
        self.display_message("You", user_message)

        # Predict bot response
        intent = predict_intent(user_message, self.model, self.tags, self.tokenizer)
        bot_response = random.choice(self.intent_responses.get(intent, ["I'm not sure how to respond."]))

        # Display bot response
        self.display_message("SAGE", bot_response)

        # Clear input box after sending message
        self.entry.delete(0, tk.END)

        # Auto-scroll chat to latest message
        self.chat_canvas.yview_moveto(1)

    def display_message(self, sender, message):
        """Display chat messages in a bubble format."""

        bubble_frame = tk.Frame(self.chat_box, bg="#E3F2FD" if sender == "SAGE" else "#E0E0E0", padx=10, pady=5)
        bubble_label = tk.Label(bubble_frame, text=message, font=("Helvetica", 12), wraplength=280,
                                bg="#E3F2FD" if sender == "SAGE" else "#E0E0E0", fg="black", justify="left")
        
        if sender == "SAGE":
            # Bot's message with an icon
            icon_label = tk.Label(bubble_frame, image=self.bot_photo, bg="#E3F2FD")
            icon_label.pack(side="left", padx=5)
            bubble_label.pack(side="right", padx=5)
        else:
            # User message
            bubble_label.pack(side="right", padx=5)

        bubble_frame.pack(anchor="w" if sender == "SAGE" else "e", pady=5)

        # Update chat window
        self.chat_box.update_idletasks()
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

# Run GUI
root = tk.Tk()
chat_gui = ChatGUI(root)
root.mainloop()
