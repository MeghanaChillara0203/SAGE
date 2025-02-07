"""
Train.py - Train deep learning model for SAGE using PyTorch and DistilBERT.
"""

# Imports
import json
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, get_scheduler
import nlpaug.augmenter.word as naw
from sklearn.metrics import f1_score

# Ensure transformers doesn’t load TensorFlow models
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disable warnings
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "true"

# Load intents
intents_path = os.path.abspath("data/intents.json")
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

# Initialize tokenizer and model (PyTorch-only)
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=len(tags), from_tf=False  # Ensures TensorFlow is NOT used
)

# Data Augmentation
# Data Augmentation with WordNet in English
aug = naw.SynonymAug(aug_src='wordnet', lang="eng")  # Explicitly setting language
augmented_patterns = []

for pattern, tag in xy:
    for _ in range(2):  # Generate 2 variations per sentence
        try:
            augmented_patterns.append((aug.augment(pattern), tag))
        except Exception as e:
            print(f"⚠️ Skipping augmentation for '{pattern}' due to error: {e}")

xy.extend(augmented_patterns)


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
num_epochs = 10
batch_size = 16
learning_rate = 5e-5

dataset = ChatDataset(xy, tags, tokenizer)
train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

scheduler = get_scheduler(
    "linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * num_epochs
)

# Training Loop
for epoch in range(num_epochs):
    correct = 0
    total = 0
    true_labels = []
    pred_labels = []

    for i, (input_ids, attention_mask, labels) in enumerate(train_loader):
        input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        scheduler.step()

        _, predicted = torch.max(outputs.logits, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

        true_labels.extend(labels.cpu().numpy())
        pred_labels.extend(predicted.cpu().numpy())

    f1 = f1_score(true_labels, pred_labels, average="weighted")
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}, Accuracy: {correct/total:.4f}, F1-score: {f1:.4f}")

# Save Model
data = {"model_state": model.state_dict(), "tags": tags}
torch.save(data, "data/data.pth")

print("Training complete. Model saved.")
