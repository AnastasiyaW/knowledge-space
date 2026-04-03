---
title: RNNs and Sequence Models
category: models
tags: [data-science, deep-learning, rnn, lstm, gru, time-series]
---

# RNNs and Sequence Models

Recurrent Neural Networks process sequential data by maintaining hidden state across time steps. While largely superseded by transformers for NLP, they remain relevant for time series and streaming applications.

## Simple RNN

Process one element at a time: h_t = tanh(W_hh * h_(t-1) + W_xh * x_t + b)

**Fatal flaw**: vanishing gradients. For sequences > ~20 tokens, gradients shrink exponentially through backpropagation through time (BPTT). Cannot learn long-range dependencies.

## LSTM (Long Short-Term Memory)

Solves vanishing gradient with gating mechanism:

- **Forget gate**: what to discard from cell state. f_t = sigma(W_f * [h_(t-1), x_t] + b_f)
- **Input gate**: what new information to store. i_t = sigma(W_i * [h_(t-1), x_t] + b_i)
- **Output gate**: what to output. o_t = sigma(W_o * [h_(t-1), x_t] + b_o)
- **Cell state**: long-term memory path with additive updates (gradients flow freely)

Handles sequences of ~200-500 tokens effectively.

```python
import torch.nn as nn

lstm = nn.LSTM(
    input_size=300,      # input feature dimension
    hidden_size=128,     # hidden state dimension
    num_layers=2,        # stacked LSTM layers
    bidirectional=True,  # process forward AND backward
    batch_first=True,    # input shape: (batch, seq, features)
    dropout=0.2          # between layers
)
```

## GRU (Gated Recurrent Unit)

Simplified LSTM with two gates instead of three:
- **Update gate**: combines forget and input gates
- **Reset gate**: controls how much past to ignore

Similar performance to LSTM, fewer parameters, slightly faster.

```python
gru = nn.GRU(input_size=300, hidden_size=128, num_layers=2,
             bidirectional=True, batch_first=True)
```

## Bidirectional

Process sequence forward AND backward, concatenate hidden states. Captures both left and right context.

Output dimension doubles: hidden_size * 2 for bidirectional.

**Use for**: classification, tagging, anything where you see the full sequence.
**Don't use for**: generation (can't look at future tokens during generation).

## Time Series with RNNs

### Forecasting Pattern
```python
class TimeSeriesLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])  # use last time step
```

### AR (AutoRegressive) Models
y_t = phi_1 * y_(t-1) + phi_2 * y_(t-2) + ... + phi_p * y_(t-p)

Features are automatically extracted from lags - no manual target feature engineering needed.

## Sequence-to-Sequence

Encoder processes input sequence -> context vector -> decoder generates output sequence.

**Applications**: machine translation, summarization, chatbots.

**Attention mechanism**: decoder attends to all encoder hidden states instead of just the final one. Solves information bottleneck of fixed-size context vector.

## Gotchas
- RNNs are sequential by nature - cannot parallelize across time steps (slow to train)
- LSTM/GRU help but don't fully solve long-range dependencies for very long sequences
- For most NLP tasks, transformers outperform RNNs significantly
- Gradient clipping is often necessary: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- Variable-length sequences need padding and masking

## See Also
- [[nlp-text-processing]] - transformers largely replaced RNNs for NLP
- [[neural-networks]] - general deep learning foundations
- [[time-series-analysis]] - statistical time series methods
