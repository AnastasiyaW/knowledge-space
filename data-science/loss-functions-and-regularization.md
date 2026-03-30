---
title: Loss Functions and Regularization
category: ml-fundamentals
tags: [loss-function, regularization, cross-entropy, mse, l1, l2, dropout, early-stopping, pytorch]
---

# Loss Functions and Regularization

Loss functions define what the model optimizes during training; regularization prevents overfitting by constraining model complexity. Choosing the right loss and regularization scheme is critical -- it directly impacts what patterns the model learns and how well it generalizes. Connects to [[gradient-descent-and-optimization]] (optimizer minimizes loss) and [[model-evaluation-metrics]] (evaluation metric may differ from training loss).

## Key Facts

### Loss Functions
- **MSE** (Mean Squared Error): regression; penalizes large errors quadratically; sensitive to outliers
- **MAE** (Mean Absolute Error / L1 Loss): regression; linear penalty; robust to outliers but non-differentiable at zero
- **Huber loss**: MSE for small errors, MAE for large errors; combines best of both; delta controls threshold
- **Cross-entropy** (log loss): classification; measures difference between predicted probabilities and true labels; standard for [[classification-algorithms]]
- **Binary cross-entropy**: for binary classification; `nn.BCEWithLogitsLoss` (includes sigmoid) or `nn.BCELoss` (expects probabilities)
- **Categorical cross-entropy**: for multi-class; `nn.CrossEntropyLoss` in PyTorch (includes log_softmax)
- **Focal loss**: down-weights easy examples, focuses on hard ones; designed for extreme class imbalance ([[object-detection]])
- **Dice loss**: overlap-based; used for [[image-segmentation]] when class imbalance is severe
- **Contrastive / Triplet loss**: metric learning; push similar samples together, dissimilar apart in embedding space
- Training loss != evaluation metric: train with cross-entropy, evaluate with F1/AUC

### Regularization
- **L2 regularization** (weight decay): adds lambda * sum(w^2) to loss; shrinks weights toward zero; equivalent to Gaussian prior
- **L1 regularization**: adds lambda * sum(|w|) to loss; drives some weights exactly to zero -> sparsity / feature selection
- **ElasticNet**: alpha * L1 + (1-alpha) * L2; combines sparsity and shrinkage; see [[regression-models]]
- **Dropout**: randomly zero out neurons during training (rate 0.1-0.5); forces redundant representations; see [[neural-network-fundamentals]]
- **Early stopping**: monitor validation loss; stop training when it starts increasing; prevents training too long
- **Data augmentation**: increase effective dataset size; regularizes by exposing model to variations; see [[transfer-learning]]
- **Batch normalization**: acts as slight regularizer due to noise from mini-batch statistics
- **Weight decay in Adam vs SGD**: AdamW implements correct weight decay; Adam's L2 regularization is mathematically different

## Patterns

```python
import torch
import torch.nn as nn

# --- Loss Functions ---

# Regression losses
mse_loss = nn.MSELoss()           # default: mean over batch
mae_loss = nn.L1Loss()
huber_loss = nn.HuberLoss(delta=1.0)

# Classification losses
ce_loss = nn.CrossEntropyLoss()   # expects raw logits, NOT softmax
bce_logits = nn.BCEWithLogitsLoss()  # binary; expects raw logits
bce_loss = nn.BCELoss()           # binary; expects probabilities (after sigmoid)

# Weighted cross-entropy for class imbalance
class_weights = torch.tensor([1.0, 5.0])  # 5x weight on minority class
ce_weighted = nn.CrossEntropyLoss(weight=class_weights)

# Label smoothing
ce_smooth = nn.CrossEntropyLoss(label_smoothing=0.1)
# Replaces hard labels [0, 1] with soft [0.05, 0.95]

# Focal loss (manual implementation)
class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, logits, targets):
        bce = nn.functional.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        pt = torch.exp(-bce)  # p_t
        focal = self.alpha * (1 - pt) ** self.gamma * bce
        return focal.mean()

# --- Regularization ---

# L2 regularization (weight decay) via optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
# For SGD:
optimizer_sgd = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

# Manual L1 regularization (add to loss)
l1_lambda = 1e-5
l1_norm = sum(p.abs().sum() for p in model.parameters())
total_loss = loss + l1_lambda * l1_norm

# Dropout in model
model = nn.Sequential(
    nn.Linear(100, 256),
    nn.ReLU(),
    nn.Dropout(0.3),      # 30% dropout rate
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 10)
)

# Early stopping (manual implementation)
best_val_loss = float('inf')
patience_counter = 0
patience = 10

for epoch in range(1000):
    train_loss = train_one_epoch(model, train_loader, optimizer)
    val_loss = evaluate(model, val_loader)

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'best_model.pt')
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch}")
            break

# Load best model
model.load_state_dict(torch.load('best_model.pt'))

# Combining losses
def combined_loss(pred, target, pred_mask, target_mask):
    cls_loss = nn.functional.cross_entropy(pred, target)
    seg_loss = dice_loss(pred_mask, target_mask)
    return cls_loss + 0.5 * seg_loss  # weighted combination
```

## Gotchas

- `nn.CrossEntropyLoss` expects raw logits, NOT softmax-ed output; it applies log_softmax internally
- `nn.BCELoss` expects probabilities (after sigmoid); `nn.BCEWithLogitsLoss` expects raw logits -- safer, more numerically stable
- Weight decay in `torch.optim.Adam` is NOT correct L2 regularization; use `AdamW` for proper weight decay
- Early stopping requires saving model checkpoint at each improvement; otherwise you end up with the overfitted version
- Dropout rate 0.5 means the effective layer width is halved; at inference time, outputs are automatically scaled (no manual adjustment needed in PyTorch)
- Label smoothing reduces overconfidence but slightly hurts accuracy on clean datasets; helps with noisy labels
- Combining multiple losses: relative scales matter; losses with different magnitudes need weighting or normalization

## See Also

- [[gradient-descent-and-optimization]] - optimizer minimizes the loss function
- [[model-evaluation-metrics]] - evaluation metrics vs training loss distinction
- [[regression-models]] - L1/L2 regularization (Lasso/Ridge)
- [[neural-network-fundamentals]] - where loss functions and regularization are applied
- [[image-segmentation]] - Dice and focal loss for segmentation
- PyTorch loss functions: https://pytorch.org/docs/stable/nn.html#loss-functions
