"""
Train.py 
Program trains deep learning model for SAGE using PyTorch. 
"""
# Imports
import json
import os
# Troch allows us to work with tensors and build neural networks
import torch
import torch.nn as nn
# Load and Batch data for training the neural networks
from torch.utils.data import Dataset, DataLoader
# pre-trained models for NLP
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


# Get path to out intents.json file (training data for SAGE)
intents_path = os.path.abspath("intents.json")

# Open and read file/ load as dictoinary
with open(intents_path, "r") as file:
    intents = json.load(file)

tags = []  # list to store unique tags from the training data
xy = []  # list storing tuples (a,y) of textual pattern and a corresponding tag
# Iterate over intents
for intent in intents['intents']:
    # Grab tag
    tag = intent['tag']
    # Add tag to list
    tags.append(tag)
    # add pattern/tag to xy list
    for pattern in intent['patterns']:
        xy.append((pattern, tag))

# Sort tags
tags = sorted(set(tags))

# Create instance of DistilBertTokenizer, and DistilBertForSequenceClassification
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=len(tags))


class ChatDataset(Dataset):  # Custom dataset class, inherits from Dataset

    # Chatbot init, takes in training data, tags, tokenizer, and max length
    def __init__(self, xy, tags, tokenizer, max_length=128):
        # Assign Attributes
        self.xy = xy
        self.tags = tags
        self.tokenizer = tokenizer
        self.max_length = max_length

   # Takes in index, returns the tokenized input sequence, attention mask, and label associated with the pattern at index
    def __getitem__(self, index):
        # Extract pattern/tag corresponding to the given index
        pattern, tag = self.xy[index]
        # Tokenize the pattern
        encoding = self.tokenizer(pattern, max_length=self.max_length,
                                  padding='max_length', truncation=True, return_tensors='pt')
        # Remove any extra dimensions
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        label = torch.tensor(self.tags.index(tag))
        return input_ids, attention_mask, label

    # determines total samples in the dataset
    def __len__(self):
        return len(self.xy)


# Hyperparameters

 # Number of times the entire training dataset will be iterated over during training
num_epochs = 3
# Number of samples in each batch of data passed to model during training
batch_size = 16
# Step size used by optimizer to update model parameters during training
learning_rate = 5e-5

# Instance of ChatDataset
dataset = ChatDataset(xy, tags, tokenizer)
# Used to iterate over training dataset in batches
train_loader = DataLoader(
    dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

# use the available CUDA device (GPU) if available, else the CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Move model to device
model.to(device)

# Loss function used during training
criterion = nn.CrossEntropyLoss()

#  Optimization algorithm used to train the model
# Algoirthm = AdamW (Adam with weight decay regularization)
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# Train the model
#  Loop for number of epochs
for epoch in range(num_epochs):
    # iterate over batches in the training data
    for i, (input_ids, attention_mask, labels) in enumerate(train_loader):
        # Moves batch data to device/ computations are performed there
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        # Clears gradients from the previous iteration
        optimizer.zero_grad()

      # Pass the input and attention mask tensors through the model
        outputs = model(input_ids, attention_mask=attention_mask)
        # Compute loss
        loss = criterion(outputs.logits, labels)

        # Computes gradients
        loss.backward()
        # Update gradients
        optimizer.step()

    # Print epoch # and its average loss
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Print final loss after training
print(f'final loss: {loss.item():.4f}')

# Create dictionary containign state of the model parameters and tags used to train the model
data = {
    "model_state": model.state_dict(),
    "tags": tags
}

# Save model state and tags
FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
