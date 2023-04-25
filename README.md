# SAGE
Group Project For CS 5100 by Bettina Puzzo Zachary Nicholas and Meghana chillara

## Initial Setup:
This repo currently contains the starter files.

Clone repo and create a virtual environment
```
$ git clone https://github.com/MeghanaChillara0203/SAGE
$ cd SAGE
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies
```
$ (venv) pip install Flask torch torchvision nltk
```
Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```

Run
```
make train
```
This will dump data.pth file. And then run
the following command to test it in the console.
```
make chat
```

For The GUI version of the chatbot
```
make gui
```

Now for deployment follow my tutorial to implement `app.py` and `app.js`.

## Inspiration
[https://youtu.be/a37BL0stIuM](https://youtu.be/a37BL0stIuM)
[this](https://github.com/python-engineer/pytorch-chatbot)

