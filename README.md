# SAGE the AI Chatbot
# Authors: Meghana Chillara, Zach Nichols, Tina Puzzo
Date: April 2023

# Steps to compile and run code:

Requirements:

- Python 3.6 or above
- PyTorch
- Transformers
- tkinter
- pillow
- openai

To Train: 
## To Run the chatbot ( with OpenAi API)
``` 
make all
```
To run it in multiple steps:
### First train the Bot
```
make train
```

### Run the ChatBot
```
make chat
```

## To check the gpt version of our chatbot
```
make gptui
```


# About

SAGE stands for "Sustainable Advisory & Guidance Expert". SAGE is a simple chatbot program that uses the DistilBERT model for natural language processing. SAGE can answer questions related to sustainability.

The program uses a combination of natural language processing (NLP) and machine learning techniques to create an interactive chatbot that can simulate a conversation about sustainability.

# How the program works:

When you run make the program will load our pre-trained machine learning model and the file containing pre-defined intent/response pairs for the SAGE, and will initialize the GUI. When a user types a question and presses enter, SAGE uses the model to predict the user's intent, and based on that will generate a response to give.

# What you should see when you run:

When this is run you should see a GUI pop up. The GUI will have a logo, a question entry box, an answer text box, a scrollbar, and a button to exit.

If you type a question into the text box and hit enter you should see the question disappear and SAGE's response to that question come into the answer box. If you hit exit, you should see the GUI exit.


