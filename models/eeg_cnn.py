import torch
import torch.nn as nn

class EEGCNN(nn.Module):
    def __init__(self, input_channels=32, input_length=250, dropout=0.5):
        super(EEGCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, (1, 5), padding=0)
        self.bn1 = nn.BatchNorm2d(16)
        self.pool = nn.AvgPool2d((1, 2))
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(16 * input_channels * ((input_length - 4) // 2), 2)

    def forward(self, x):
        x = x.unsqueeze(1)  # add channel dim
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        return self.fc(x)

