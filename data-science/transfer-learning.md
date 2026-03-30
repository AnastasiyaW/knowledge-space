---
title: Transfer Learning
category: deep-learning
tags: [transfer-learning, fine-tuning, pretrained, data-augmentation, pytorch, computer-vision]
---

# Transfer Learning

Use a model pretrained on a large dataset (ImageNet, COCO, etc.) as starting point for a new task. Transfer learning is the default approach for computer vision and NLP when you have limited data. Two strategies: feature extraction (freeze backbone, train new head) and fine-tuning (unfreeze some/all layers). Closely tied to [[convolutional-neural-networks]] and [[neural-network-fundamentals]].

## Key Facts

- **Pretrained model**: trained on large dataset (ImageNet: 1.4M images, 1000 classes); early layers learn universal features (edges, textures)
- **Feature extraction**: freeze pretrained layers, replace and train only the classification head; fast, works with very small datasets (100-1000 samples)
- **Fine-tuning**: unfreeze some/all pretrained layers and train with small learning rate; better accuracy but needs more data; risk of catastrophic forgetting
- **Progressive unfreezing**: start with head only, then gradually unfreeze layers from top to bottom; more stable than unfreezing everything at once
- **Learning rate**: use smaller lr for pretrained layers (1e-5 to 1e-4) and larger lr for new head (1e-3); differential learning rates
- **Data augmentation**: artificially expand dataset with random transformations; essential when fine-tuning with small data; see [[convolutional-neural-networks]]
- **Domain shift**: pretrained on natural images (ImageNet) may not transfer well to medical/satellite images; fine-tune more aggressively
- **Model zoo**: torchvision.models, timm (PyTorch Image Models), HuggingFace for NLP; hundreds of pretrained architectures
- **Knowledge distillation**: train a smaller "student" model to mimic a larger "teacher" model's outputs; compress knowledge
- **Augmentation strategies**: RandAugment (random augmentation policy), CutOut/CutMix (occlusion-based), MixUp (interpolate samples)
- Rule of thumb: more similar domains + more data -> unfreeze more layers; different domains + little data -> use feature extraction only

## Patterns

```python
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# Strategy 1: Feature extraction (freeze backbone)
model = models.resnet50(weights='IMAGENET1K_V2')
for param in model.parameters():
    param.requires_grad = False  # freeze all
model.fc = nn.Linear(model.fc.in_features, num_classes)
# Only model.fc parameters will be updated

# Strategy 2: Fine-tuning (unfreeze later layers)
model = models.resnet50(weights='IMAGENET1K_V2')
model.fc = nn.Linear(model.fc.in_features, num_classes)
# Freeze early layers
for name, param in model.named_parameters():
    if 'layer4' not in name and 'fc' not in name:
        param.requires_grad = False

# Differential learning rates
optimizer = torch.optim.Adam([
    {'params': model.layer4.parameters(), 'lr': 1e-4},
    {'params': model.fc.parameters(), 'lr': 1e-3}
])

# Data augmentation for training
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# ImageFolder expects: root/class_name/image.jpg
train_dataset = ImageFolder('data/train', transform=train_transform)
val_dataset = ImageFolder('data/val', transform=val_transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)

# Using timm (PyTorch Image Models) for more architectures
# pip install timm
import timm
model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=num_classes)
# timm handles head replacement automatically

# Progressive unfreezing training schedule
def unfreeze_layers(model, layer_names):
    for name, param in model.named_parameters():
        if any(ln in name for ln in layer_names):
            param.requires_grad = True

# Phase 1: train head only (5 epochs)
# Phase 2: unfreeze_layers(model, ['layer4']) (5 epochs, lr=1e-4)
# Phase 3: unfreeze_layers(model, ['layer3', 'layer4']) (10 epochs, lr=1e-5)

# CutMix / MixUp augmentation
# pip install torchvision  (built-in since v0.15)
from torchvision.transforms.v2 import CutMix, MixUp
cutmix = CutMix(num_classes=num_classes)
mixup = MixUp(num_classes=num_classes)
```

## Gotchas

- ALWAYS use the same normalization as the pretrained model (ImageNet: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Input size matters: ResNet expects 224x224; some models (EfficientNet-B7) expect 600x600; check model docs
- When fine-tuning, use much smaller learning rate (10-100x smaller) than training from scratch
- `model.eval()` is required for inference even with transfer learning -- BatchNorm and Dropout behavior changes
- Freezing BatchNorm layers during fine-tuning is often beneficial; running stats from pretrained data are more stable
- Augmentation should only be applied to training data, NEVER to validation/test

## See Also

- [[convolutional-neural-networks]] - backbone architectures used for transfer learning
- [[object-detection]] - detection models use pretrained backbones
- [[image-segmentation]] - pretrained encoders for segmentation (U-Net, DeepLab)
- [[cross-validation-and-model-selection]] - evaluating fine-tuning strategies
- timm library: https://huggingface.co/docs/timm/
- torchvision models: https://pytorch.org/vision/stable/models.html
