---
title: Color Checker and White Balance Correction
category: techniques
tags: [color-checker, white-balance, color-constancy, illumination, calibration, datasets, jewelry-photography]
aliases: ["Color Constancy", "White Balance"]
---

# Color Checker and White Balance Correction

Automated color calibration using color checker cards and white balance correction models. Critical for product/jewelry photography standardization — consistent metal color, gemstone hue across different lighting.

## Core Concept

Color checker cards (X-Rite 24-patch, 140-patch Digital ColorChecker SG) provide known color references. Pipeline:
1. Detect color checker in image
2. Compute color transform (3x3 matrix, polynomial, or neural) from measured → reference values
3. Apply transform to entire image

## Datasets

| Dataset | Content | Use |
|---------|---------|-----|
| **Middlebury Color** | 35 cameras × 2 lighting conditions (3200K/4800K), RAW + JPEG | Camera-specific calibration |
| **ccHarmony** | 4260 pairs synthetic composites + real images | Image harmonization training |
| **Color Checkers (Roboflow)** | 214 images + pretrained detection model | Checker detection |
| **I-HAZE** | 35 pairs (haze/clean) with MacBeth checker | Haze + color correction |
| **CroP** | Synthetic RAW generator with checkers | Training data generation |
| **Gehler, NUS-8, Cube++** | Standard color constancy benchmarks | White balance evaluation |

Links:
- vision.middlebury.edu/color/data/
- github.com/bcmi/Image-Harmonization-Dataset-ccHarmony
- universe.roboflow.com/nahom-5dyof/color-checkers

## Detection Tools

| Tool | Approach | Notes |
|------|----------|-------|
| colour-checker-detection | YOLOv8 + segmentation | Python package, github.com/colour-science/colour-checker-detection |
| Roboflow pretrained | API-based detection | Pre-trained, ready to use |
| Custom YOLO | Train on checker dataset | Best for specific shooting setups |

## White Balance Correction Models

| Model | Approach | License | Notes |
|-------|----------|---------|-------|
| **WB_sRGB** | Deep WB correction for already-rendered sRGB | Has datasets, idea reproducible | github.com/mahmoudnafifi/WB_sRGB |
| **WB_color_augmenter** | Emulates wrong WB for training data augmentation | Pairs generation | github.com/mahmoudnafifi/WB_color_augmenter |

## Primary Pipeline: Diffusion-Generated Color Checker

**Главный подход:** обучить диффузионную модель СТАБИЛЬНО генерировать виртуальный color checker внутри изображения, согласованный с освещением сцены. Потом детекция + цветокоррекция по точкам — это уже классический алгоритм.

### Архитектура (3 стадии)

```bash
Stage 1: GENERATE — диффузионная модель вписывает чекер в изображение
  Input: фото без чекера + маска (где разместить чекер)
  Output: фото с чекером, где цвета чекера отражают реальное освещение сцены
  Model: SD2 Inpainting fine-tune / [[SANA]] / [[Step1X-Edit|Qwen-Image-Edit]] LoRA

Stage 2: DETECT — найти сгенерированный чекер и считать значения патчей
  Model: YOLO или colour-checker-detection (простая задача — чекер всегда есть)
  Output: 24 измеренных RGB значений

Stage 3: CORRECT — классический алгоритм цветокоррекции
  Compute: 3×3 color matrix (measured → reference D65 values)
  Apply: transform entire image
  Method: least squares, polynomial, или colour-science library
```

### Почему генерация а не детекция

Реальные фото **не содержат** color checker — фотографы убирают его перед финальной обработкой. Нам нужна модель которая может **восстановить** как бы выглядел чекер в данной сцене при данном освещении. Это задача illumination estimation через generative inpainting.

### Датасет для обучения Stage 1

| Источник | Что берём | Как используем |
|----------|----------|---------------|
| Middlebury Color | Фото С чекером + фото БЕЗ (кроп/маска) | Before/after пары |
| I-HAZE | Фото с MacBeth чекером | Paired training data |
| CroP (synthetic) | Генерируем любое количество | Augmentation |
| ccHarmony | Пары с known illumination | Validation |
| **Собственные фото** | Снять ювелирку С чекером и БЕЗ | Gold standard pairs |

**Формат пар:**
```text
input/0001.png    → фото БЕЗ чекера (маска на месте чекера)
target/0001.png   → фото С чекером (реальный, в том же освещении)
mask/0001.png     → бинарная маска позиции чекера
```

### Критичный момент: стабильность генерации

Модель должна генерировать **узнаваемый** X-Rite 24-patch чекер, а не абстрактные цветные пятна. Подходы:
1. **ControlNet** с шаблоном чекера (фиксированный layout) + inpainting для цветов
2. **LoRA** обученная на парах (сцена без чекера → сцена с чекером)
3. **Prompt conditioning**: "X-Rite ColorChecker Classic, 24 patches, 4×6 grid" + маска

### Альтернативный подход: прямая WB коррекция

Без генерации чекера — обучить модель предсказывать цветовую матрицу напрямую:
- Input: фото
- Output: 3×3 color correction matrix (или illuminant estimation)
- Training: на RAW→final парах из DNG sidecar файлов (Lightroom WB corrections)

Проще, но менее interpretable и менее точно для нестандартных условий.

## Relevance for Jewelry Photography

- Standardize metal color (gold, silver, rose gold) across different studio setups
- Consistent gemstone color under varying illumination
- Batch processing: photographer shoots 700+ RAW files → automated color correction
- Solar curves technique (see discussions) for revealing subtle color/edge differences invisible to naked eye

## Related Techniques

- **Intrinsic image decomposition:** separate illumination from reflectance (github.com/vinavfx/Intrinsic-for-Nuke — good implementation, restrictive license but paper is reproducible)
- **Shadow removal:** SP-Net/M-Net for shadow decomposition (ICCV 2019, ISTD dataset 4800 pairs)
- **Reflectance filtering:** github.com/tnestmeyer/reflectance-filtering
