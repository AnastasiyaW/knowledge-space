---
title: Recurrent Networks and Sequences
category: deep-learning
tags: [rnn, lstm, gru, transformer, attention, time-series, nlp, pytorch, deep-learning]
---

# Recurrent Networks and Sequences

Process sequential data where order matters: time series, text, audio. RNNs maintain hidden state across time steps; LSTMs/GRUs solve vanishing gradient problem with gating mechanisms. Transformers (attention-based) have largely replaced RNNs for NLP but RNNs remain relevant for some time series tasks.

## Key Facts

- **RNN**: h_t = activation(W_h * h_{t-1} + W_x * x_t + b); hidden state carries information across time steps
- **Vanishing/exploding gradients**: RNN gradients shrink/grow exponentially over long sequences; limits effective memory to ~10-20 steps
- **LSTM** (Long Short-Term Memory): cell state + 3 gates (forget, input, output); can learn long-range dependencies (100+ steps)
- **Forget gate**: decides what to remove from cell state; sigmoid output * cell state
- **Input gate**: decides what new information to store; sigmoid * tanh of new candidate values
- **Output gate**: decides what to output as hidden state; sigmoid * tanh(cell state)
- **GRU** (Gated Recurrent Unit): simplified LSTM with 2 gates (reset, update); similar performance, fewer parameters
- **Bidirectional RNN**: process sequence forward AND backward; captures both past and future context; not usable for real-time prediction
- **Sequence-to-sequence (seq2seq)**: encoder RNN -> context vector -> decoder RNN; foundation of old translation models
- **Attention mechanism**: instead of single context vector, attend to all encoder hidden states with learned weights; allows focus on relevant parts
- **Transformer**: self-attention + positional encoding; processes all positions in parallel (no sequential bottleneck); foundation of BERT, GPT
- **Self-attention**: Q, K, V matrices from input; Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V
- **Positional encoding**: sine/cosine functions encode position information since transformers have no inherent order awareness
- For time series: LSTM still competitive; for NLP: transformers dominate completely

## Patterns

```python
import torch
import torch.nn as nn

# Simple LSTM for sequence classification
class LSTMClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, num_classes, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_dim, hidden_dim,
            num_layers=num_layers,
            batch_first=True,       # input: (batch, seq_len, features)
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=True
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 for bidirectional

    def forward(self, x):
        # x: (batch, seq_len, input_dim)
        output, (h_n, c_n) = self.lstm(x)
        # output: (batch, seq_len, hidden_dim * 2)
        # Use last hidden state from both directions
        last_hidden = torch.cat([h_n[-2], h_n[-1]], dim=1)
        return self.fc(last_hidden)

# LSTM for time series forecasting
class LSTMForecaster(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=64, forecast_horizon=1):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2,
                           batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, forecast_horizon)

    def forward(self, x):
        output, _ = self.lstm(x)
        return self.fc(output[:, -1, :])  # use last time step

# Prepare time series data (sliding window)
def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        xs.append(data[i:i+seq_length])
        ys.append(data[i+seq_length])
    return torch.stack(xs), torch.stack(ys)

# Simple Transformer encoder for classification
class TransformerClassifier(nn.Module):
    def __init__(self, input_dim, d_model=128, nhead=8, num_layers=2, num_classes=10):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, d_model)
        self.pos_encoding = nn.Parameter(torch.randn(1, 512, d_model))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=0.1, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(d_model, num_classes)

    def forward(self, x):
        # x: (batch, seq_len, input_dim)
        x = self.input_proj(x) + self.pos_encoding[:, :x.size(1), :]
        x = self.transformer(x)
        x = x.mean(dim=1)  # average pooling over sequence
        return self.fc(x)

# GRU (simpler alternative to LSTM)
gru = nn.GRU(input_size=10, hidden_size=64, num_layers=2,
             batch_first=True, bidirectional=True)

# Packed sequences for variable-length inputs
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
# lengths = [actual sequence lengths]
# packed = pack_padded_sequence(padded_input, lengths, batch_first=True, enforce_sorted=False)
# output, h_n = lstm(packed)
# unpacked, lens = pad_packed_sequence(output, batch_first=True)
```

## Gotchas

- `batch_first=True` changes tensor shape to (batch, seq, features); without it, default is (seq, batch, features)
- LSTM returns `(output, (h_n, c_n))` where h_n shape is (num_layers * directions, batch, hidden); for bidirectional, concatenate last two h_n
- Dropout in LSTM only applies BETWEEN layers (not within); `dropout` param requires `num_layers > 1`
- For variable-length sequences: use `pack_padded_sequence` to avoid computing gradients on padding tokens
- Transformer `nhead` must divide `d_model` evenly; d_model=128, nhead=8 -> head_dim=16
- RNN hidden state carries gradients through time; very long sequences -> gradient accumulation -> OOM; use truncated BPTT or gradient checkpointing

## See Also

- [[neural-network-fundamentals]] - RNN is a neural network with recurrent connections
- [[gradient-descent-and-optimization]] - vanishing gradient problem and solutions
- [[generative-models]] - sequence generation with autoregressive models
- [[convolutional-neural-networks]] - 1D convolutions as alternative for sequence processing
- PyTorch RNN tutorial: https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html
