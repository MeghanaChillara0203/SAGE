import json
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

intents_path = os.path.abspath("SAGE - Without UI/intents.json")

with open(intents_path, "r") as file:
    intents = json.load(file)

tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        xy.append((pattern, tag))

tags = sorted(set(tags))

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=len(tags))

class ChatDataset(Dataset):

    def __init__(self, xy, tags, tokenizer, max_length=128):
        self.xy = xy
        self.tags = tags
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __getitem__(self, index):
        pattern, tag = self.xy[index]
        encoding = self.tokenizer(pattern, max_length=self.max_length, padding='max_length', truncation=True, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        label = torch.tensor(self.tags.index(tag))
        return input_ids, attention_mask, label

    def __len__(self):
        return len(self.xy)

# Hyperparameters
num_epochs = 3
batch_size = 16
learning_rate = 5e-5

dataset = ChatDataset(xy, tags, tokenizer)
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for i, (input_ids, attention_mask, labels) in enumerate(train_loader):
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels)

        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f'final loss: {loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "tags": tags
}

FILE = "SAGE - Without UI/data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
