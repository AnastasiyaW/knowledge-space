---
title: Gradient Descent and Optimization
category: ml-fundamentals
tags: [gradient-descent, sgd, adam, learning-rate, backpropagation, optimization, pytorch]
---

# Gradient Descent and Optimization

Iteratively minimize a loss function by moving parameters in the direction of steepest descent. Foundation of training [[neural-network-fundamentals]], [[regression-models]], and most ML models. Understanding optimizers, learning rates, and convergence is critical for deep learning.

## Key Facts

- **Gradient**: vector of partial derivatives; points in direction of steepest ascent; we move OPPOSITE (descent)
- **Learning rate (lr)**: step size; too large -> diverge/oscillate; too small -> slow convergence
- **Batch Gradient Descent**: compute gradient on ENTIRE dataset; accurate but slow; one update per epoch
- **Stochastic Gradient Descent (SGD)**: compute gradient on ONE sample; noisy but fast; many updates per epoch
- **Mini-batch GD**: gradient on batch of B samples (32-512); best tradeoff; standard in deep learning
- **Momentum**: accumulate gradient history to accelerate in consistent directions and dampen oscillations; v = beta*v - lr*grad; typical beta = 0.9
- **RMSProp**: per-parameter adaptive learning rate; divides by running average of squared gradients; handles different feature scales
- **Adam** (Adaptive Moment Estimation): combines momentum (first moment) + RMSProp (second moment); default optimizer for most deep learning tasks
- **AdamW**: Adam with decoupled weight decay; fixes L2 regularization in Adam; preferred in modern practice
- **Learning rate schedule**: reduce lr during training; StepLR, CosineAnnealing, ReduceLROnPlateau, warmup + decay
- **Backpropagation**: chain rule to compute gradients layer by layer from output to input; O(n) computation via dynamic programming
- **Vanishing gradients**: deep networks with sigmoid/tanh; gradients shrink exponentially; solved by ReLU, skip connections, BatchNorm
- **Exploding gradients**: gradients grow exponentially; solved by gradient clipping (max_norm)

## Patterns

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Simple model
model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 1)
)

# Optimizers
optimizer_sgd = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
optimizer_adam = optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999))
optimizer_adamw = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

# Learning rate schedulers
scheduler_step = optim.lr_scheduler.StepLR(optimizer_adam, step_size=10, gamma=0.1)
scheduler_cosine = optim.lr_scheduler.CosineAnnealingLR(optimizer_adam, T_max=100)
scheduler_plateau = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer_adam, mode='min', factor=0.5, patience=5
)

# Training loop with gradient clipping
criterion = nn.MSELoss()
for epoch in range(100):
    for X_batch, y_batch in dataloader:
        optimizer_adam.zero_grad()            # clear previous gradients
        output = model(X_batch)               # forward pass
        loss = criterion(output, y_batch)     # compute loss
        loss.backward()                       # backpropagation
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # gradient clipping
        optimizer_adam.step()                  # parameter update
    scheduler_step.step()                     # update learning rate
    # For ReduceLROnPlateau: scheduler_plateau.step(val_loss)

# Check current learning rate
current_lr = optimizer_adam.param_groups[0]['lr']

# Gradient accumulation (simulate larger batch size)
accumulation_steps = 4
for i, (X_batch, y_batch) in enumerate(dataloader):
    output = model(X_batch)
    loss = criterion(output, y_batch) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer_adam.step()
        optimizer_adam.zero_grad()

# Manual gradient inspection
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: grad norm = {param.grad.norm():.4f}")
```

```python
# Gradient descent from scratch (educational)
import numpy as np

def gradient_descent(X, y, lr=0.01, epochs=1000):
    n, m = X.shape
    w = np.zeros(m)
    b = 0
    for _ in range(epochs):
        y_pred = X @ w + b
        error = y_pred - y
        dw = (2 / n) * X.T @ error    # gradient w.r.t. weights
        db = (2 / n) * error.sum()     # gradient w.r.t. bias
        w -= lr * dw
        b -= lr * db
    return w, b
```

## Gotchas

- `optimizer.zero_grad()` MUST be called before `.backward()`; otherwise gradients accumulate across batches (unless intentional gradient accumulation)
- Adam default lr=1e-3 works for many tasks; SGD typically needs lr=0.01-0.1 with momentum
- Learning rate too high: loss oscillates or increases; too low: loss decreases very slowly
- AdamW != Adam + L2 regularization; Adam's L2 is broken due to adaptive learning rates; use AdamW for weight decay
- `loss.backward()` computes gradients but does NOT update parameters; `optimizer.step()` does the update
- Batch normalization interacts with learning rate; larger batches allow larger lr

## See Also

- [[neural-network-fundamentals]] - forward/backward pass uses gradient descent
- [[loss-functions-and-regularization]] - what gradient descent is actually minimizing
- [[convolutional-neural-networks]] - architecture-specific optimization considerations
- [[linear-algebra]] - gradients are vectors, Hessians are matrices
- PyTorch optim docs: https://pytorch.org/docs/stable/optim.html
