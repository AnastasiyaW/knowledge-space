# Segmentation Dataset Preparation — Binary Small-Object

Reference for binary semantic segmentation datasets with 0.1-5% positive-pixel coverage (small defects, lesions, anomalies). Three critical errors consistently cause inflated metrics and model collapse.

## Critical Errors (Fix These First)

### 1. Split at Crop Level Instead of Source Image Level

**Symptom:** Near-equal train/val sample counts (e.g. 6077 train / 6091 val for acne). Correct image-level splits never produce this ratio.

**Fix:** GroupKFold grouped by `source_image_id`. All crops, scales, and instances from one source image → one fold.

```python
from sklearn.model_selection import GroupKFold
import pandas as pd

df = pd.read_csv("instances.csv")  # cols: sample_path, source_image_id, class_id, scale
gkf = GroupKFold(n_splits=5)
df['fold'] = -1
for fold_idx, (_, val_idx) in enumerate(gkf.split(df, groups=df['source_image_id'])):
    df.loc[val_idx, 'fold'] = fold_idx

# Assert no leakage
for f in range(5):
    train_imgs = set(df[df.fold != f]['source_image_id'])
    val_imgs   = set(df[df.fold == f]['source_image_id'])
    assert not (train_imgs & val_imgs), f"Fold {f} leak: {len(train_imgs & val_imgs)} images"
```

### 2. Loss Scale Mismatch with Class Imbalance

**Symptom:** Model converges to all-background. `class_weight=2.5` is wildly undercalibrated for 1% coverage (correct weight ≈ 99).

**Fix:** Switch to compound Dice + Focal or FocalTversky.

```python
import segmentation_models_pytorch as smp
import torch.nn as nn

class CompoundLoss(nn.Module):
    def __init__(self, ignore_index=255):
        super().__init__()
        self.dice  = smp.losses.DiceLoss(mode='binary', from_logits=True,
                                          ignore_index=ignore_index)
        self.focal = smp.losses.FocalLoss(mode='binary', alpha=0.25, gamma=2.0,
                                           ignore_index=ignore_index)

    def forward(self, logits, target):
        return 0.5 * self.dice(logits, target) + 0.5 * self.focal(logits, target)

# Or for recall-biased (missed defect worse than false alarm):
tversky = smp.losses.TverskyLoss(mode='binary', alpha=0.3, beta=0.7, gamma=1.0)
```

**Loss selection guide:**

| Loss | Use when | Caveat |
|------|----------|--------|
| `DiceLoss` | Default binary medical seg | Unstable with no positives in batch |
| `TverskyLoss` (α=0.3, β=0.7) | Recall >> precision (missed defect = bad) | More hyperparams |
| `FocalLoss` | Hard examples matter | Needs γ tuning |
| Compound 0.5×Dice + 0.5×Focal | Production default (nnU-Net style) | Requires both correct |
| `CE + class_weight` | Only if weight = `1/coverage` | `2.5` for 1% coverage is wrong; correct ≈ 99 |

### 3. CoarseDropout Silently Erasing Targets

**Symptom:** Train image has no positive pixels but mask still says defect present → semi-supervised noise.

**Fix:** Set `fill_mask=0` in Albumentations 2.0+, or remove CoarseDropout for rare-small classes.

```python
import albumentations as A

# Albumentations 2.0+ API
A.CoarseDropout(
    num_holes_range=(1, 8),
    hole_height_range=(0.02, 0.08),  # keep small for small-object seg
    hole_width_range=(0.02, 0.08),
    fill=0,
    fill_mask=0,  # CRITICAL: black out mask too, consistent erasure
    p=0.3,
)
```

## Canonical Dataset Class

```python
import albumentations as A
import cv2, numpy as np, torch
from torch.utils.data import Dataset

class SkinDefectDataset(Dataset):
    def __init__(self, df, imgsz=768, mode='train'):
        self.df = df
        self.imgsz = imgsz
        self.transform = self._build_transform(mode)

    def _build_transform(self, mode):
        if mode == 'train':
            return A.Compose([
                A.LongestMaxSize(max_size=self.imgsz),
                A.PadIfNeeded(min_height=self.imgsz, min_width=self.imgsz,
                              border_mode=cv2.BORDER_REFLECT_101,
                              mask_value=255),     # 255 = ignore_index for padded regions
                A.HorizontalFlip(p=0.5),
                A.RandomRotate90(p=0.5),
                A.Affine(translate_percent=(-0.05,0.05), scale=(0.85,1.15),
                         rotate=(-15,15), p=0.5),  # replaces deprecated ShiftScaleRotate
                A.RandomBrightnessContrast(0.2, 0.2, p=0.3),
                A.HueSaturationValue(10, 15, 10, p=0.3),
                A.OneOf([A.GaussianBlur(blur_limit=(3,5)),
                         A.GaussNoise(var_limit=(5,20))], p=0.2),
                # CoarseDropout omitted for <5% coverage classes
                A.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
            ])
        else:   # val: deterministic only
            return A.Compose([
                A.LongestMaxSize(max_size=self.imgsz),
                A.PadIfNeeded(min_height=self.imgsz, min_width=self.imgsz,
                              border_mode=cv2.BORDER_REFLECT_101,
                              mask_value=255),
                A.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
            ])

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img  = cv2.cvtColor(cv2.imread(row['img_path']), cv2.COLOR_BGR2RGB)
        mask = cv2.imread(row['mask_path'], cv2.IMREAD_GRAYSCALE)
        mask = (mask > 127).astype(np.uint8)   # canonicalize to 0/1 on load
        out  = self.transform(image=img, mask=mask)
        img_t  = torch.from_numpy(out['image'].transpose(2,0,1)).float()
        mask_t = torch.from_numpy(out['mask']).long()   # values: 0, 1, or 255
        return img_t, mask_t
```

## Model Setup

```python
import segmentation_models_pytorch as smp

# Binary segmentation: single output channel + sigmoid (NOT 2 channels + softmax)
model = smp.Unet(
    encoder_name='resnet101',
    encoder_weights='imagenet',
    in_channels=3,
    classes=1,      # binary → sigmoid at inference, not softmax
)
```

## Validation Loop

```python
def validate(model, loader, device):
    model.eval()
    tp, fp, fn, tn = 0, 0, 0, 0
    with torch.no_grad():
        for img, mask in loader:
            img, mask = img.to(device), mask.to(device)
            logits = model(img)
            pred   = (logits.sigmoid() > 0.5).long().squeeze(1)
            valid  = mask != 255          # exclude padded pixels
            t, f, fn_, tn_ = smp.metrics.get_stats(pred[valid], mask[valid], mode='binary')
            tp += t.sum(); fp += f.sum(); fn += fn_.sum(); tn += tn_.sum()
    return smp.metrics.iou_score(tp, fp, fn, tn, reduction='micro').item()
```

## Leakage Verification Script

```python
def sanity_check(train_df, val_df):
    train_imgs = set(train_df['source_image_id'])
    val_imgs   = set(val_df['source_image_id'])
    assert not (train_imgs & val_imgs), f"LEAKAGE: {len(train_imgs & val_imgs)} images overlap"
    for split, df in [('train', train_df), ('val', val_df)]:
        ratio = len(df) / df['source_image_id'].nunique()
        print(f"{split}: {df['source_image_id'].nunique()} imgs, {len(df)} samples, ratio={ratio:.2f}")
        if 0.9 < ratio < 1.1 and df['source_image_id'].nunique() > 500:
            print(f"WARN: ~1:1 ratio suggests crop-level split, not image-level")
```

## Mask Conventions

- **On disk:** any format (0/255 PNG OK for viewing)
- **In memory (PyTorch):** 0=background, 1=target, 255=ignore (padded regions)
- **Canonicalize at load:** `mask = (mask > 127).astype(np.int64)`
- **Model output:** `classes=1` (not 2). Apply `sigmoid` at inference, not `softmax`.

## Multi-Scale Crop Strategy

Pre-generating tight/512/1024 crops per instance as independent samples:
- Triples effective weight of each instance
- Combined with crop-level split → silent oversampling + leakage

**Better:** Dynamic `RandomResizedCrop(scale=(0.3, 1.0))` at train time (nnU-Net pattern). One sample per instance per epoch.

## Preprocessing

- **Padding:** use `reflect` mode + `ignore_index=255` in mask for padded pixels
- **Mask resize: NEAREST always.** For upscaling predictions: bilinear on logits then threshold.
- **Val augmentation: deterministic only.** No flips, rotates, dropout on validation.

## Gotchas

- **Issue:** `0/1` vs `0/255` mask inconsistency → silent NaN after 3 steps. -> **Fix:** Assert `mask.max() <= 1` in `__getitem__`. Canonicalize at load: `(mask > 127).astype(np.int64)`.
- **Issue:** `DiceLoss` with `from_logits=True` expects raw logits. Applying `sigmoid` before loss gives wrong gradient surface. -> **Fix:** Pass raw logits, let the loss apply `sigmoid` internally. Check `from_logits` flag matches.
- **Issue:** Val set too small for rare classes → unstable metrics. Single run variance > effect size. -> **Fix:** 5-fold GroupKFold, report mean±std. Drop classes with < 30 source images.
- **Issue:** `ShiftScaleRotate` deprecated in Albumentations 2.0. -> **Fix:** Replace with `A.Affine(translate_percent=..., scale=..., rotate=...)`.

## See Also
- [[skin-retouch-pipeline]]
