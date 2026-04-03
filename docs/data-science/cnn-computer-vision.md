---
title: CNNs and Computer Vision
category: models
tags: [data-science, deep-learning, cnn, computer-vision, image-classification]
---

# CNNs and Computer Vision

Convolutional Neural Networks exploit spatial structure in images through local pattern detection and translation invariance. From classification to generation, CNNs revolutionized visual understanding.

## Image as Data

Image = 3D tensor (height x width x channels). Grayscale: 1 channel. RGB: 3 channels. Each pixel = integer [0, 255].

For simple models: flatten to 1D (28x28 -> 784 features). Problem: loses spatial structure. CNNs solve this.

## Convolution Layer

Slide small filter (kernel) across input. Each filter detects one pattern (edge, texture, shape).

- **Kernel size**: 3x3, 5x5 typical. Small kernels stacked = large receptive field
- **Stride**: step size. Stride 2 halves spatial dimensions
- **Padding**: "same" preserves size, "valid" reduces
- **Channels**: input channels matched by filter depth; output channels = number of filters
- **1x1 convolution**: linear combination of channels (bottleneck, dimensionality reduction)

### Pooling

Reduce spatial dimensions. **Max pooling** (take max in window) most common. Typical: 2x2, stride 2.

### CNN Pattern

Input -> [Conv -> BN -> ReLU -> (Pool)] x N -> Flatten -> Dense -> Output

## Architecture Evolution

| Architecture | Year | Key Innovation |
|-------------|------|----------------|
| **AlexNet** | 2012 | First deep CNN to win ImageNet. ReLU, dropout, data augmentation |
| **VGG** | 2014 | Only 3x3 convs stacked deeply. Simple, uniform |
| **GoogLeNet/Inception** | 2014 | Parallel convs of different sizes, concatenated. 1x1 bottlenecks |
| **ResNet** | 2015 | Skip connections: output = F(x) + x. 50-152 layers |
| **DenseNet** | 2017 | Each layer connected to all previous layers |
| **MobileNet** | 2017 | Depthwise separable convolutions for mobile/edge |
| **EfficientNet** | 2019 | Compound scaling (width, depth, resolution) |
| **ViT** | 2020 | Vision Transformer - apply transformer to image patches |

### ResNet Skip Connections

Solve vanishing gradient for deep networks:
```
input -> Conv -> BN -> ReLU -> Conv -> BN -> (+input) -> ReLU
```
The identity shortcut lets gradients flow directly through the network.

## Transfer Learning

Use pre-trained model (ImageNet: 1.2M images, 1000 classes) as starting point.

```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet50(pretrained=True)

# Option A: Feature extraction (freeze everything, replace head)
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(2048, num_classes)

# Option B: Fine-tune last layers
for param in model.layer4.parameters():
    param.requires_grad = True
model.fc = nn.Linear(2048, num_classes)
```

**Rule of thumb**: smaller dataset = freeze more layers; larger dataset = fine-tune more.

## Object Detection

Locate objects with bounding boxes + class labels.

### Two-Stage Detectors
- **R-CNN**: region proposals (selective search) -> CNN per region -> classify
- **Fast R-CNN**: CNN on full image, extract features per region from feature map
- **Faster R-CNN**: learned Region Proposal Network (RPN). Fully end-to-end

### One-Stage Detectors
- **YOLO**: divide image into SxS grid, each cell predicts boxes + classes. Single forward pass. Real-time
- **SSD**: multi-scale feature maps for objects at different sizes

### Detection Metrics
- **IoU**: intersection / union of predicted and ground truth box. >= 0.5 = correct
- **mAP@0.5**: mean Average Precision at IoU threshold 0.5
- **mAP@0.5:0.95**: averaged over IoU thresholds 0.5 to 0.95 (step 0.05)
- **NMS** (Non-Maximum Suppression): remove overlapping detections, keep highest confidence

## Segmentation

### Semantic Segmentation
Classify every pixel. No instance distinction.
- **FCN**: replace FC layers with convolutions, upsample back
- **U-Net**: encoder-decoder with skip connections. Excellent for medical imaging
- **DeepLab**: atrous (dilated) convolutions for larger receptive field

### Instance Segmentation
Detect objects AND segment pixel boundaries.
- **Mask R-CNN**: Faster R-CNN + mask prediction branch per detected box

### Segmentation Metrics
- **mIoU**: mean IoU across classes (primary metric)
- **Dice coefficient**: 2*|A intersect B| / (|A| + |B|). Equivalent to F1

## Generative Models

- **GAN**: Generator vs Discriminator adversarial training. Challenges: mode collapse, instability
- **VAE**: encode to latent distribution, sample, decode. Smooth interpolation
- **Diffusion**: iteratively denoise from pure noise. Current state-of-the-art for image quality
- **CycleGAN**: unpaired image-to-image translation (style transfer, domain adaptation)

## 3D Vision
- **Depth estimation**: predict distance per pixel from 2D image
- **Point cloud processing**: PointNet for 3D point data
- **NeRF**: learn 3D scene from 2D images, render novel views

## Gotchas
- Always normalize images (ImageNet stats: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Data augmentation is almost always beneficial for vision tasks
- Larger input resolution = better accuracy but quadratic compute cost
- Pre-trained models expect specific input sizes and normalization
- YOLO versions vary widely - check which variant for fair comparison

## See Also
- [[neural-networks]] - general deep learning foundations
- [[transfer-learning]] - detailed pre-training/fine-tuning strategies
- [[data-augmentation]] - augmentation techniques for vision
- [[generative-models]] - GANs, VAEs, diffusion in depth
