---
title: Neural Networks and Deep Learning
category: models
tags: [data-science, deep-learning, neural-networks, pytorch, keras]
---

# Neural Networks and Deep Learning

Deep learning learns features automatically from raw data. Excels at images, text, audio, and sequences where manual feature engineering is impractical.

## Building Blocks

### Dense (Fully Connected) Layer
Every input connected to every output: y = Wx + b

### Activation Functions

| Function | Formula | Range | Use Case |
|----------|---------|-------|----------|
| ReLU | max(0, x) | [0, inf) | Default for hidden layers |
| LeakyReLU | max(0.01x, x) | (-inf, inf) | Fixes dead neuron problem |
| Sigmoid | 1/(1+e^(-x)) | (0, 1) | Binary classification output |
| Tanh | (e^x-e^(-x))/(e^x+e^(-x)) | (-1, 1) | Zero-centered alternative |
| Softmax | e^(x_i) / sum(e^(x_j)) | (0, 1), sum=1 | Multi-class output |

Without activations, stacking linear layers = one linear layer.

## Training

### Loss Functions
- **Binary Cross-Entropy**: L = -[y*log(p) + (1-y)*log(1-p)]
- **Categorical Cross-Entropy**: L = -sum(y_i * log(p_i))
- **MSE**: for regression

### Training Loop (PyTorch)
```python
for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        predictions = model(batch_x)       # forward pass
        loss = criterion(predictions, batch_y)
        optimizer.zero_grad()               # clear gradients
        loss.backward()                     # backpropagation
        optimizer.step()                    # update weights
```

### Optimizers
- **SGD**: w -= lr * gradient. Simple, good with momentum
- **Adam**: adaptive per-parameter learning rates. Default choice for most tasks
- **Learning rate**: most important hyperparameter. Try 1e-3, 3e-4, 1e-4

## Regularization

- **Dropout**: randomly zero out fraction of neurons during training (typical: 0.2-0.5)
- **Batch Normalization**: normalize layer inputs within mini-batch. Allows higher learning rates
- **Early Stopping**: monitor validation loss, stop when it increases
- **Data Augmentation**: random transforms (flip, rotate, crop for images)
- **Weight Decay**: L2 regularization as optimizer parameter

## PyTorch Example

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleNet()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

## Keras/TensorFlow Example

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
```

## Hyperparameters

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Learning rate | 1e-4 to 1e-2 | Most important - tune first |
| Batch size | 32, 64, 128, 256 | Larger = faster, smaller = better generalization |
| Layers/units | Task-dependent | Start small, increase if underfitting |
| Dropout rate | 0.1-0.5 | Higher for larger models |
| Weight init | He (ReLU), Xavier (tanh/sigmoid) | Usually handled by framework |
| Epochs | Use early stopping | Don't fix a number |

## Gotchas
- **Vanishing gradients**: deep networks with sigmoid/tanh. Fix: use ReLU, skip connections, BatchNorm
- **Exploding gradients**: gradient clipping helps. Common in RNNs
- **Dead ReLU neurons**: negative inputs -> zero gradient forever. Fix: LeakyReLU
- Neural networks need MUCH more data than tree-based models for tabular data
- Always normalize inputs (StandardScaler or similar)
- GPU is practically required for non-trivial models

## See Also
- [[cnn-computer-vision]] - convolutional networks for images
- [[rnn-sequences]] - recurrent networks for sequences
- [[nlp-text-processing]] - NLP with transformers
- [[math-for-ml]] - calculus for backpropagation
- [[transfer-learning]] - using pre-trained models
