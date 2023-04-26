all: train chat gui

train:
	python -B train.py

chat:
	python -B GUI.py
