import openai
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# OpenAI API Key (Replace with your key)
openai.api_key = 'xxxxxx'  # Replace with your OpenAI API key
#openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt_response(user_input, model="gpt-3.5-turbo", tokens=150, temperature=0.5):
    client = openai.OpenAI(api_key=openai.api_key)  # Explicitly passing API key
  # Updated OpenAI client

    # Define system message
    system_message = {
        "role": "system",
        "content": "You are a friendly AI assistant that helps users \
            with their questions and tasks, specifically regarding environmental issues, \
                lifestyle choices, and sustainability practices."
    }

    # Define conversation
    messages = [
        system_message,
        {"role": "user", "content": user_input}
    ]

    # Get GPT response
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=tokens,
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("SAGE with GPT")
        master.geometry("400x600")
        master.configure(bg="white")

        # Load chatbot icon
        self.bot_icon = Image.open("figs/sage_gpt.png")  # Make sure this image exists
        self.bot_icon = self.bot_icon.resize((30, 30), Image.LANCZOS)
        self.bot_photo = ImageTk.PhotoImage(self.bot_icon)

        # Header
        self.header = tk.Label(master, text="SAGE - GPT", font=("Helvetica", 14, "bold"), fg="white", bg="#0078D4", padx=10, pady=10)
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

        # Chatbot greets first
        self.display_message("SAGE", "Hi there! I'm SAGE-GPT, your AI assistant. How can I help you today?")

    def chat(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return

        # Display user message
        self.display_message("You", user_message)

        # Get GPT response
        bot_response = get_gpt_response(user_message)

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
if __name__ == "__main__":
    root = tk.Tk()
    chat_gui = ChatGUI(root)
    root.mainloop()
