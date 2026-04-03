---
title: Data Augmentation
category: techniques
tags: [data-science, deep-learning, augmentation, computer-vision, regularization]
---

# Data Augmentation

Artificially increase training data by applying random transformations. Reduces overfitting, improves generalization. Virtually free performance improvement for vision and NLP tasks.

## Image Augmentation

### Basic Transforms

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Validation: NO augmentation (except resize + normalize)
val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

### Advanced Techniques

- **Cutout/Random Erasing**: randomly mask rectangular regions
- **Mixup**: blend two images and their labels: x = lambda*x1 + (1-lambda)*x2
- **CutMix**: paste patch from one image onto another, mix labels by area ratio
- **AutoAugment**: learned augmentation policies

## Text Augmentation

- **Synonym replacement**: replace words with synonyms
- **Back-translation**: translate to another language and back
- **Random insertion/deletion/swap**: perturb word order
- **Contextual augmentation**: use language model to replace words

## Tabular Data Augmentation

- **SMOTE**: generate synthetic minority samples for imbalanced classes
- **Noise injection**: add Gaussian noise to features
- **Mixup**: blend feature vectors and labels

```python
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_train, y_train)
```

## Principles

- Apply augmentation **only to training data**, never validation/test
- Augmentations should be label-preserving (flipping a "6" may create a "9")
- Domain-appropriate: don't flip text horizontally, don't rotate medical images if orientation matters
- More aggressive augmentation for smaller datasets
- Combine multiple augmentations for maximum effect

## Gotchas
- Over-aggressive augmentation can harm performance (model learns to handle noise instead of signal)
- Vertical flips rarely appropriate (most natural images have gravity)
- Color augmentation can destroy important color information (medical imaging)
- SMOTE generates synthetic points in feature space - may create unrealistic samples
- Augmentation adds training time - balance benefit vs cost

## See Also
- [[cnn-computer-vision]] - primary beneficiary of image augmentation
- [[nlp-text-processing]] - text augmentation techniques
- [[feature-engineering]] - SMOTE for tabular data
- [[model-evaluation]] - measuring augmentation impact
