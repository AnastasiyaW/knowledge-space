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

### Why Vanishing Gradients Happen

The output prediction y_hat(T) is a composite function of all inputs x_1...x_T. Weight matrix W_xh appears multiplied by every input at every time step. When computing the gradient of W_xh via chain rule, this produces a product of many derivatives. If W_hh eigenvalues < 1, the product shrinks exponentially (vanishing). If > 1, it explodes (exploding gradient). This means: the influence of early inputs on the final output becomes negligible - the network "forgets" early tokens.

**Exploding gradients** are manageable via gradient clipping. **Vanishing gradients** are the harder problem - this is what LSTM and GRU were designed to solve.

## LSTM (Long Short-Term Memory)

Solves vanishing gradient with a cell state that uses **additive** updates (not multiplicative), allowing gradients to flow through time without vanishing:

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

## Sequence Data Categories

Different sequence tasks have different I/O shapes:

| Category | Input | Output | Examples |
|----------|-------|--------|----------|
| Many-to-one | Sequence | Single value | Sentiment analysis, activity recognition |
| One-to-many | Single value | Sequence | Music generation, image captioning |
| Many-to-many (equal) | Sequence | Same-length sequence | NER, POS tagging |
| Many-to-many (unequal) | Sequence | Different-length sequence | Translation, summarization |

Note: "one-to-many" may have empty/null input (e.g., unconditional music generation) or a seed value (genre ID, first few notes).

## Sequence-to-Sequence

Encoder processes input sequence -> context vector -> decoder generates output sequence.

**Applications**: machine translation, summarization, chatbots.

**Attention mechanism**: decoder attends to all encoder hidden states instead of just the final one. Solves information bottleneck of fixed-size context vector.

## Training RNNs: Batching and Sequence Length

### Generating Training Batches

For character-level or word-level language models, the full text must be sliced into overlapping input/target pairs:

```python
def generate_batches(encoded_text, seq_length, batch_size):
    """Slice encoded text into (input, target) pairs for RNN training."""
    total_chars = len(encoded_text)
    chars_per_batch = total_chars // batch_size

    for i in range(0, chars_per_batch - seq_length, seq_length):
        x = encoded_text[i:i + seq_length]       # input sequence
        y = encoded_text[i + 1:i + seq_length + 1]  # target = shifted by 1
        yield x, y
```

**Key parameters to tune**:

- **Sequence length**: minimum ~100 characters/tokens. Longer = more context but slower training and more memory
- **Batch size**: typical 64-128. Larger batches = more stable gradients but may converge to sharper minima
- **Epochs**: depends on dataset size and model capacity. Monitor loss - stop when validation loss plateaus

### Training Loop Pattern (PyTorch)

```python
model.train()
if model.use_gpu:
    model.cuda()

for epoch in range(n_epochs):
    hidden = model.init_hidden(batch_size)
    for x_batch, y_batch in generate_batches(data, seq_len, batch_size):
        hidden = tuple(h.detach() for h in hidden)  # detach to prevent BPTT through entire history
        model.zero_grad()
        output, hidden = model(x_batch, hidden)
        loss = criterion(output, y_batch.view(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5)
        optimizer.step()
```

**Critical**: `hidden.detach()` at each batch boundary prevents backpropagation through the entire sequence history (which would be memory-prohibitive). This is truncated BPTT.

## Gotchas
- RNNs are sequential by nature - cannot parallelize across time steps (slow to train)
- LSTM/GRU help but don't fully solve long-range dependencies for very long sequences
- For most NLP tasks, transformers outperform RNNs significantly
- Gradient clipping is often necessary: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- Variable-length sequences need padding and masking
- **Hidden state detach**: forgetting to detach hidden state between batches causes OOM as the computation graph grows unboundedly
- **Sequence length vs memory**: doubling sequence length roughly doubles memory usage and training time per batch

## See Also
- [[nlp-text-processing]] - transformers largely replaced RNNs for NLP
- [[neural-networks]] - general deep learning foundations
- [[time-series-analysis]] - statistical time series methods
