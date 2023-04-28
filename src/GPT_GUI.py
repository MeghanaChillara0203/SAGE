import openai
import tkinter as tk
from tkinter import ttk

# this key is for cs5100 final project demo purposes only and will be turned off after April 2023
openai.api_key = "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"
# 2024-04-27 note: when this repo was made public to turn in our project,
# the above key was disabled by OpenAI. If you wish to use this code to test,
# you will need to contact Zach N for a new key or create your own OpenAI account
# and obtain your own API key.

def get_gpt_response(user_input, model='gpt-3.5-turbo', tokens=150, temperature=0.5, api_key=None):

    # this message gets prepended to any requests to the API so it has some context for the response
    # without it, you are asking "vanilla" GPT to respond to a prompt with no context
    system_message = "You are a friendly AI assistant that helps users \
        with their questions and tasks, specifically regarding environmental issues, \
            lifestyle choices, and sustainability practices."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
        ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=tokens,
        temperature=temperature,
        n=1
    )

    return response.choices[0].message['content'].strip()

def submit_question():
    user_input = user_entry.get()
    gpt_response = get_gpt_response(user_input, api_key=openai.api_key)
    response_text.set("SAGE: " + gpt_response + "...")

def main():
    global user_entry
    global response_text

    def update_textbox(text):
        answer_textbox.configure(state='normal')
        answer_textbox.delete(1.0, tk.END)
        answer_textbox.insert(tk.END, text)
        answer_textbox.configure(state='disabled')

    def submit_question(event=None):
        user_input = user_entry.get()
        gpt_response = get_gpt_response(user_input, api_key=openai.api_key)
        update_textbox("SAGE: " + gpt_response + "...")

    root = tk.Tk()
    root.title("SAGE with GPT")
    root.geometry("1000x800")

    mainframe = ttk.Frame(root, padding="30 30 30 30")
    mainframe.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Add logo
    logo = tk.PhotoImage(file="figs/sage_gpt.png")
    logo_label = tk.Label(root, image=logo)
    logo_label.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    # Create a custom style for the ttk.Entry widget
    style = ttk.Style()
    style.configure('Custom.TEntry', background='black', foreground='white')

    user_entry = ttk.Entry(mainframe, width=80, font=("Helvetica", 14), style='Custom.TEntry')
    user_entry.grid(column=0, row=1, sticky=(tk.W, tk.E))
    user_entry.focus()
    user_entry.bind('<Return>', submit_question)  # Bind the Return key to submit_question

    ttk.Label(mainframe, text="Enter your question: ", font=("Helvetica", 14)).grid(column=0, row=0, sticky=tk.W)

    # Display answer in a non-editable text box
    answer_textbox = tk.Text(mainframe, wrap=tk.WORD, width=80, height=10, font=("Helvetica", 14), state='disabled', background='black', foreground='white')
    answer_textbox.grid(column=0, row=3, sticky=(tk.W, tk.E))

    ttk.Button(mainframe, text="Submit", command=submit_question, style='TButton').grid(column=0, row=2, sticky=tk.E)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()