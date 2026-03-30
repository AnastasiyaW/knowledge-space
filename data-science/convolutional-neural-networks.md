---
title: Convolutional Neural Networks
category: deep-learning
tags: [cnn, convolution, pooling, resnet, vgg, image-classification, pytorch, computer-vision]
---

# Convolutional Neural Networks

Specialized [[neural-network-fundamentals]] for grid-structured data (images, time series). Convolutional layers learn local patterns (edges, textures) with shared weights; pooling layers reduce spatial dimensions. Deeper architectures (ResNet, EfficientNet) with skip connections enable training very deep networks. Foundation for [[object-detection]], [[image-segmentation]], and [[transfer-learning]].

## Key Facts

- **Convolution layer**: slides a kernel (filter) across the input; output = feature map; learns edge/texture detectors
- **Kernel size**: typically 3x3 or 5x5; smaller kernels stacked = larger receptive field with fewer params
- **Stride**: step size of kernel movement; stride=2 halves spatial dimensions (alternative to pooling)
- **Padding**: `same` (output same size as input) or `valid` (no padding, output shrinks)
- **Channels**: input channels (RGB=3), output channels = number of filters; each filter detects one pattern
- **Pooling**: MaxPool (take max in window) or AvgPool; reduces dimensions and provides translation invariance
- **Global Average Pooling (GAP)**: average each feature map to a single number; replaces flattening before FC layer; reduces overfitting
- **Receptive field**: the region of input that influences one output neuron; grows with depth
- **1x1 convolution**: changes channel count without changing spatial size; "learns channel combinations"; used in Inception, ResNet bottleneck
- **Batch Normalization**: normalize after conv, before activation; critical for training stability; see [[neural-network-fundamentals]]
- **Skip connections (ResNet)**: output = F(x) + x; solves vanishing gradient in deep networks; enables 100+ layer networks
- **Common architectures**: VGG (simple, deep), ResNet (skip connections), Inception (multi-scale), EfficientNet (compound scaling), MobileNet (depthwise separable convs for mobile)
- **Data augmentation**: random flip, rotation, crop, color jitter; essential for image models; see [[transfer-learning]]
- Parameters of conv layer: kernel_size * kernel_size * in_channels * out_channels + out_channels (bias)

## Patterns

```python
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models

# Basic CNN from scratch
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1: 3 -> 32 channels
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),  # spatial: 32x32 -> 16x16

            # Block 2: 32 -> 64 channels
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 16x16 -> 8x8

            # Block 3: 64 -> 128 channels
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),  # global average pooling -> (128, 1, 1)
        )
        self.classifier = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)  # flatten: (batch, 128)
        return self.classifier(x)

# Conv layer output size formula
# out_size = (in_size - kernel_size + 2*padding) / stride + 1

# Data augmentation for training
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Pretrained ResNet
resnet = models.resnet50(weights='IMAGENET1K_V2')
# Replace final FC layer for custom number of classes
resnet.fc = nn.Linear(resnet.fc.in_features, num_classes)

# Feature extraction (freeze backbone)
for param in resnet.parameters():
    param.requires_grad = False
resnet.fc.requires_grad_(True)

# Count conv vs total parameters
conv_params = sum(p.numel() for name, p in resnet.named_parameters() if 'conv' in name)

# Depthwise separable convolution (MobileNet-style)
depthwise_sep = nn.Sequential(
    nn.Conv2d(64, 64, kernel_size=3, padding=1, groups=64),  # depthwise
    nn.Conv2d(64, 128, kernel_size=1),                        # pointwise
    nn.BatchNorm2d(128),
    nn.ReLU()
)
```

## Gotchas

- Input tensor shape in PyTorch: (batch, channels, height, width) -- NOT (batch, height, width, channels)
- Always normalize images with dataset-specific mean/std (ImageNet: [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
- `nn.CrossEntropyLoss` expects (batch, num_classes) logits, not (batch, 1) -- don't apply softmax before it
- Forgetting `model.eval()` before inference causes BatchNorm and Dropout to behave as training, giving wrong results
- Conv2d kernel counts: 3x3 conv with 64 in, 128 out = 3*3*64*128 = 73,728 parameters (+ 128 bias)
- ResNet skip connection requires matching dimensions; 1x1 conv (projection shortcut) handles dimension mismatch

## See Also

- [[object-detection]] - uses CNN backbone for feature extraction + detection heads
- [[image-segmentation]] - encoder-decoder CNNs (U-Net, DeepLab)
- [[transfer-learning]] - fine-tuning pretrained CNNs on custom datasets
- [[neural-network-fundamentals]] - CNN layers are specialized neural network components
- PyTorch vision models: https://pytorch.org/vision/stable/models.html
