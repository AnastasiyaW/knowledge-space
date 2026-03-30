---
title: Neural Network Fundamentals
category: deep-learning
tags: [neural-network, perceptron, activation, mlp, backpropagation, pytorch, deep-learning]
---

# Neural Network Fundamentals

A neural network is a composition of linear transformations and non-linear activations. Universal approximation theorem: a single hidden layer with enough neurons can approximate any continuous function. In practice, deeper networks with fewer neurons per layer generalize better. Foundation for [[convolutional-neural-networks]], [[recurrent-networks-and-sequences]], and [[generative-models]].

## Key Facts

- **Neuron**: weighted sum of inputs + bias + activation function; output = activation(w*x + b)
- **Layer types**: Dense/Linear (fully connected), Conv2d, LSTM, Attention, BatchNorm, Dropout
- **Activation functions**: ReLU (max(0, x)), Sigmoid (0-1), Tanh (-1 to 1), GELU, Swish
- **ReLU**: default for hidden layers; fast, avoids vanishing gradient; "dying ReLU" problem (neurons stuck at 0)
- **Leaky ReLU**: f(x) = x if x > 0, else alpha*x; prevents dying ReLU; alpha typically 0.01
- **Sigmoid**: output layer for binary classification; suffers from vanishing gradients in hidden layers
- **Softmax**: output layer for multi-class; outputs probability distribution
- **Forward pass**: input -> layer1 -> activation -> layer2 -> ... -> output; chain of matrix multiplications and activations
- **Backward pass (backpropagation)**: compute loss gradient w.r.t. each parameter using chain rule; see [[gradient-descent-and-optimization]]
- **Batch Normalization**: normalize activations within a mini-batch; stabilizes training, allows higher lr
- **Dropout**: randomly zero out neurons during training (rate 0.1-0.5); regularization; disabled at inference
- **Weight initialization**: Xavier/Glorot for sigmoid/tanh; He/Kaiming for ReLU; critical for deep networks
- **Epoch**: one full pass through training data; **batch**: one gradient update step; **iteration** = batch
- Typical training loop: forward pass -> compute loss -> backward pass -> optimizer step

## Patterns

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Define a simple MLP
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)

# Instantiate
model = MLP(input_dim=20, hidden_dim=128, output_dim=2)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()  # for classification
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# DataLoader
X_tensor = torch.randn(1000, 20)
y_tensor = torch.randint(0, 2, (1000,))
dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Training loop
model.train()
for epoch in range(50):
    total_loss = 0
    for X_batch, y_batch in dataloader:
        optimizer.zero_grad()
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if epoch % 10 == 0:
        print(f"Epoch {epoch}: loss = {total_loss / len(dataloader):.4f}")

# Evaluation mode (disables dropout, changes BatchNorm behavior)
model.eval()
with torch.no_grad():
    logits = model(X_test_tensor)
    preds = torch.argmax(logits, dim=1)
    accuracy = (preds == y_test_tensor).float().mean()

# Save and load model
torch.save(model.state_dict(), 'model.pt')
model.load_state_dict(torch.load('model.pt'))

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

# Weight initialization (Kaiming for ReLU)
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
        nn.init.zeros_(m.bias)
model.apply(init_weights)
```

## Gotchas

- `model.train()` vs. `model.eval()` is CRITICAL -- dropout and batchnorm behave differently; always switch before training/inference
- `torch.no_grad()` during evaluation saves memory and speeds up inference; otherwise computation graph is built
- `CrossEntropyLoss` expects raw logits, NOT softmax output; it applies log_softmax internally
- BatchNorm with batch_size=1 fails; use `nn.InstanceNorm` or `nn.GroupNorm` for small/single-sample batches
- Learning rate 1e-3 (Adam) or 0.01-0.1 (SGD + momentum) are common starting points
- Deeper != always better; without skip connections, gradients vanish in networks > 10-20 layers

## See Also

- [[gradient-descent-and-optimization]] - how neural network parameters are updated
- [[loss-functions-and-regularization]] - choosing loss function and preventing overfitting
- [[convolutional-neural-networks]] - neural networks specialized for images
- [[transfer-learning]] - leveraging pretrained neural networks
- PyTorch tutorials: https://pytorch.org/tutorials/beginner/basics/intro.html
