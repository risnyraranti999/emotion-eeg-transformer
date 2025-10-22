import torch
import torch.nn as nn

class EEGTransformer(nn.Module):
    def __init__(self, input_channels=32, input_length=250, dim_model=128, num_heads=4, num_layers=2, dropout=0.3):
        super(EEGTransformer, self).__init__()
        self.embed = nn.Linear(input_channels, dim_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=dim_model, nhead=num_heads, dropout=dropout)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Linear(dim_model, 2)

    def forward(self, x):
        x = x.permute(0, 2, 1)  # (batch, time, channels)
        x = self.embed(x)       # (batch, time, dim_model)
        x = self.transformer(x)
        x = x.mean(dim=1)
        return self.classifier(x)

