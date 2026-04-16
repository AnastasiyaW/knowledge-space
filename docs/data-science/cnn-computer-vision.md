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

Slide small filter (kernel) across input. Each filter detects one pattern (edge, texture, shape). Convolution reduces to two operations: multiply element-wise, then sum. Three objects: input image, filter (kernel), output image (feature map).

- **Kernel size**: 3x3, 5x5 typical. Small kernels stacked = large receptive field
- **Stride**: step size. Stride 2 halves spatial dimensions
- **Padding**: "same" preserves size, "valid" reduces
- **Channels**: input channels matched by filter depth; output channels = number of filters
- **1x1 convolution**: linear combination of channels (bottleneck, dimensionality reduction)
- **Bias term**: each filter has a scalar bias added after the convolution sum, before activation

### Convolution as Feature Detection

Different kernels detect different features:
- **Blur kernel**: averaging filter smooths the image (noise reduction)
- **Edge detection**: Sobel-style filters highlight boundaries between regions
- **Sharpen kernel**: amplifies differences between adjacent pixels

In a trained CNN, kernels are not hand-crafted - they are learned via backpropagation. Early layers learn edge/texture detectors; deeper layers learn complex pattern detectors (eyes, wheels, text).

### Pooling

Reduce spatial dimensions (downsampling). **Max pooling** (take max in window) most common. Typical: 2x2, stride 2.

- Pool size 2 with stride 2: 100x100 -> 50x50 (halves each dimension)
- Achieves translation invariance - small shifts in input don't change pooled output
- **Average pooling**: take mean instead of max. Used in some architectures (GoogLeNet)
- **Global Average Pooling**: reduce entire feature map to single value per channel. Replaces flatten+dense in modern architectures (fewer parameters, less overfitting)

### CNN Two-Stage Architecture

A CNN has two stages:

1. **Feature extraction stage**: alternating Conv + Pool layers. Hierarchical - each layer detects features from the previous layer's output. This stage is a specialized image feature transformer
2. **Classification stage**: standard dense (fully connected) layers that take extracted features and perform classification/regression

```php
Input -> [Conv -> BN -> ReLU -> Pool] x N -> Flatten -> Dense -> Output
```

This separation explains why transfer learning works: stage 1 learns general image features (edges, textures, shapes) while stage 2 learns task-specific classification.

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
```php
input -> Conv -> BN -> ReLU -> Conv -> BN -> (+input) -> ReLU
```
The identity shortcut lets gradients flow directly through the network. ResNet demonstrated that with skip connections, training a 152-layer network is feasible and outperforms shallower alternatives.

### Why Study Architecture Case Studies

Neural network architectures that work well on one computer vision task typically transfer to others. Key cross-pollination patterns:
- **ResNet's skip connections** appeared in transformer architectures
- **Inception's multi-scale processing** influenced feature pyramid networks
- **ViT showed** that transformer attention can replace convolution entirely

Reading architecture papers builds intuition similar to how programmers learn by reading others' code.

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

## Convolution on Color Images (3D Kernels)

Grayscale convolution: 2D filter slides over 2D image. Color images: **3D filter** slides over 3D input (H x W x C).

- Input: (H, W, 3) for RGB. Kernel: (k, k, 3) - same depth as input channels
- Sum across all three channels at each position -> single scalar output
- A 3D kernel acts as a **color pattern detector**: a filter for "red circle" will not match blue circles
- Multiple filters -> multiple output channels: N filters of (k, k, 3) produce output of (H', W', N)
- Each successive conv layer: input channels = previous layer's filter count, not 3

This is why the first conv layer has few parameters (3 input channels) but deeper layers have many (64, 128, 256 input channels from previous filter counts).

## CNNs for Time Series Classification

CNNs are not limited to images - they work on any data with local spatial/temporal structure.

### 1D Convolution for Time Series

Input shape: (batch, timesteps, features) = (N, T, D). Use Conv1D instead of Conv2D.

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=5, activation='relu',
                           input_shape=(128, 9)),  # T=128, D=9
    tf.keras.layers.MaxPooling1D(pool_size=3),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.GlobalMaxPooling1D(),  # alternatives: Flatten, GlobalAvgPooling1D
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
```

**Kernel size selection**: for longer sequences (T=128+), use larger initial kernels (5-7). For short sequences (T~10), smaller kernels (3). Larger T justifies larger kernels, same principle as larger images.

### Human Activity Recognition (HAR)

Classic CNN application on sensor time series. Input: accelerometer/gyroscope readings from smartphone (T=128 timesteps, D=9 channels for x/y/z from 3 sensors).

**Multi-input architecture**: combine time-series CNN with tabular features (statistics, FFT features) via concatenation:

```python
# Time series branch
ts_input = tf.keras.Input(shape=(128, 9))
x = tf.keras.layers.Conv1D(32, 5, activation='relu')(ts_input)
x = tf.keras.layers.MaxPooling1D(3)(x)
x = tf.keras.layers.GlobalMaxPooling1D()(x)

# Tabular branch
tab_input = tf.keras.Input(shape=(num_tabular_features,))
y = tf.keras.layers.Dense(64, activation='relu')(tab_input)

# Combine
combined = tf.keras.layers.Concatenate()([x, y])
output = tf.keras.layers.Dense(num_classes, activation='softmax')(combined)
model = tf.keras.Model(inputs=[ts_input, tab_input], outputs=output)
```

### CNN for Time Series Forecasting

Use CNN as feature extractor, then dense layer for prediction. Reshape univariate series into (T, 1) input.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, kernel_size=3, activation='relu',
                           input_shape=(window_size, 1)),
    tf.keras.layers.Conv1D(64, kernel_size=3, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)  # single step forecast
])
```

Note: values don't divide evenly through pooling layers - always check `model.summary()` to verify output shapes at each layer.

## Gotchas
- Always normalize images (ImageNet stats: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Data augmentation is almost always beneficial for vision tasks
- Larger input resolution = better accuracy but quadratic compute cost
- Pre-trained models expect specific input sizes and normalization
- YOLO versions vary widely - check which variant for fair comparison
- **Conv1D for time series**: kernel slides along time axis only, not spatial. Input shape differs from Conv2D
- **GlobalMaxPooling vs Flatten**: GlobalMaxPooling reduces to fixed-size regardless of input length. Flatten requires fixed input size
- **Multi-input models** need `tf.keras.Model` (functional API), not `Sequential`

## See Also
- [[neural-networks]] - general deep learning foundations
- [[transfer-learning]] - detailed pre-training/fine-tuning strategies
- [[data-augmentation]] - augmentation techniques for vision
- [[generative-models]] - GANs, VAEs, diffusion in depth
- [[time-series-analysis]] - classical time series models
- [[rnn-sequences]] - RNN alternative for sequence data
