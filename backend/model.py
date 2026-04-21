import torch
import torch.nn as nn

class DeepLogModel(nn.Module):
    def __init__(self, num_classes, embedding_dim=32, hidden_dim=64, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(num_classes, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        out = self.embedding(x)
        out, _ = self.lstm(out)
        return self.fc(out[:, -1, :])