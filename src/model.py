""" 
Model.py
A Neural Network model for SAGE built using the PyTorch library"""

# Torch imports
import torch
import torch.nn as nn


# Base class for all neural network modules in PyTorch
class NeuralNet(nn.Module):

    #  Initializes the layers of the neural network given:
    #     --> input size, hidden size, and number of output classes
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    # Defines how input data is propagated through the layers of network in forward pass
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out
