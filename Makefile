all: train chat

train:
	python -B src/train.py

chat:
	python -B src/GUI_Intents.py

gpt:
	python -B src/gpt.py

gptui:
	python -B src/GPT_GUI.py
