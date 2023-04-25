all: train chat gui

train:
	python -B src/train.py

chat:
	python -B src/chat.py

gui:
	python -B src/GUI.py
