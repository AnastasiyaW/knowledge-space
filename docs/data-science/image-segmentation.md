---
title: Image Segmentation
category: computer-vision
tags: [segmentation, semantic, instance, unet, mask-rcnn, deeplab, pytorch, computer-vision]
---

# Image Segmentation

Assign a class label to every pixel in an image. Semantic segmentation labels pixels by class (all cars = same label); instance segmentation distinguishes individual objects (car1 vs car2); panoptic segmentation combines both. Extends [[convolutional-neural-networks]] with encoder-decoder architectures.

## Key Facts

- **Semantic segmentation**: pixel-wise classification; output = H x W mask with class ID per pixel; no instance distinction
- **Instance segmentation**: detect + segment individual objects; Mask R-CNN = [[object-detection]] (Faster R-CNN) + mask branch
- **Panoptic segmentation**: semantic (background stuff) + instance (countable things) in one output
- **U-Net**: encoder (downsampling) + decoder (upsampling) + skip connections; designed for medical imaging; works with few training images
- **Skip connections**: copy encoder features to decoder at same resolution; preserves fine spatial details lost during downsampling
- **DeepLab**: atrous (dilated) convolutions for larger receptive field without losing resolution; ASPP module for multi-scale context
- **Transposed convolution** (ConvTranspose2d): learned upsampling; can produce checkerboard artifacts
- **Bilinear upsampling + conv**: smoother alternative to transposed convolution
- **Loss functions**: Cross-entropy (per pixel), Dice loss (overlap-based, handles class imbalance), Focal loss (hard examples)
- **mIoU** (mean Intersection over Union): standard metric; IoU per class averaged across all classes
- **Dice coefficient**: 2*|A intersect B| / (|A| + |B|); equivalent to F1 score for binary segmentation
- **SAM** (Segment Anything Model): foundation model for zero-shot segmentation with prompts (points, boxes, text)
- Common datasets: Cityscapes (driving), ADE20K (scene), COCO-stuff (stuff+things), medical imaging datasets

## Patterns

```python
import torch
import torch.nn as nn

# Simple U-Net architecture
class UNet(nn.Module):
    def __init__(self, in_channels=3, num_classes=2):
        super().__init__()
        # Encoder (downsampling)
        self.enc1 = self._block(in_channels, 64)
        self.enc2 = self._block(64, 128)
        self.enc3 = self._block(128, 256)
        self.pool = nn.MaxPool2d(2)

        # Bottleneck
        self.bottleneck = self._block(256, 512)

        # Decoder (upsampling)
        self.up3 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.dec3 = self._block(512, 256)  # 512 = 256 (up) + 256 (skip)
        self.up2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec2 = self._block(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec1 = self._block(128, 64)

        self.out = nn.Conv2d(64, num_classes, kernel_size=1)

    def _block(self, in_c, out_c):
        return nn.Sequential(
            nn.Conv2d(in_c, out_c, 3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_c, out_c, 3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        b = self.bottleneck(self.pool(e3))
        d3 = self.dec3(torch.cat([self.up3(b), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.out(d1)

# Dice loss (better for imbalanced segmentation)
class DiceLoss(nn.Module):
    def forward(self, pred, target, smooth=1e-6):
        pred = torch.softmax(pred, dim=1)
        target_one_hot = nn.functional.one_hot(target, pred.shape[1]).permute(0, 3, 1, 2).float()
        intersection = (pred * target_one_hot).sum(dim=(2, 3))
        union = pred.sum(dim=(2, 3)) + target_one_hot.sum(dim=(2, 3))
        dice = (2 * intersection + smooth) / (union + smooth)
        return 1 - dice.mean()

# Pretrained segmentation model (torchvision)
from torchvision.models.segmentation import deeplabv3_resnet101
model = deeplabv3_resnet101(weights='DEFAULT')
model.eval()
# Output: model(input)['out'] -> (batch, num_classes, H, W)

# mIoU computation
def compute_miou(pred_mask, true_mask, num_classes):
    ious = []
    for cls in range(num_classes):
        pred_c = (pred_mask == cls)
        true_c = (true_mask == cls)
        intersection = (pred_c & true_c).sum().float()
        union = (pred_c | true_c).sum().float()
        if union == 0:
            continue  # skip classes not present
        ious.append((intersection / union).item())
    return sum(ious) / len(ious) if ious else 0.0
```

## Gotchas

- Segmentation output shape is (batch, num_classes, H, W); apply `argmax(dim=1)` to get class predictions per pixel
- U-Net skip connections require encoder and decoder feature maps to have the SAME spatial size; may need center-crop or padding
- Dice loss is non-differentiable in its discrete form; use soft Dice (with probabilities) for training
- Cross-entropy loss ignores pixels labeled as "ignore" class (e.g., label=255); set `ignore_index=255` in loss
- Transposed convolution with stride=2 and kernel=2 may produce checkerboard artifacts; prefer bilinear upsample + conv
- mIoU can be dominated by small classes; report per-class IoU alongside mean

## See Also

- [[convolutional-neural-networks]] - encoder backbone architecture
- [[object-detection]] - instance segmentation = detection + per-instance masks
- [[transfer-learning]] - pretrained encoders improve segmentation significantly
- [[loss-functions-and-regularization]] - Dice, focal, and weighted cross-entropy for segmentation
- torchvision segmentation: https://pytorch.org/vision/stable/models.html#semantic-segmentation
