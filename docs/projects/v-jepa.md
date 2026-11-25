---
title: V-JEPA
category: projects
date: 2026-03-20
tags: [project, v-jepa]
aliases: ["V-JEPA"]
---

# V-JEPA

**Development line:** `project:v-jepa` · thread `v-jepa`  
**Last event:** 2026-03-20 · 1 dated since 2026-03-20 · **Researched:** 2026-09-05 · confidence: high

## What it is

V-JEPA — семейство PyTorch-моделей Meta для разработчиков video understanding и robotics. — извлекает представления из видео без ручной разметки; — прогнозирует действия и состояния в латентном пространстве; — V-JEPA 2-AC добавляет action-conditioned планирование для манипуляторов; — V-JEPA 2.1 ориентирована на пространственно и временно согласованные dense-признаки. Линейка 2.1: ViT-B 80M, ViT-L 300M, ViT-g 1B и ViT-G 2B параметров при 384 px. Вердикт: для новых задач сегментации, depth, трекинга и video features стоит начинать с V-JEPA 2.1; 2-AC нужен только для воспроизведения исследовательского robotics-контура.

## Development line

- **2026-03-20 — V-JEPA was linked to the V-JEPA 2 repository.** Семейство dense video/image encoders с Dense Predictive Loss, deep self-supervision и multimodal tokenizers; первичный анонс в README датирован 2026-03-16, статья опубликована 2026-03-15.

## What changed

2026-03-20 — в репозитории V-JEPA была доступна V-JEPA 2.1: семейство dense video/image encoders с Dense Predictive Loss, deep self-supervision и multimodal tokenizers; первичный анонс в README датирован 2026-03-16, статья опубликована 2026-03-15. 2025-06-11 — Meta представила V-JEPA 2, 1.2B-параметрическую video world model, и V-JEPA 2-AC: action-conditioned вариант, дообученный менее чем на 62 часах неразмеченного видео DROID для zero-shot pick-and-place. 2026-03-15 — статья V-JEPA 2.1 добавила четыре checkpoint-размера от 80M до 2B и заявила улучшение dense-задач, включая 0.307 RMSE на NYUv2 и 77.7% на Something-Something-V2.

## How to use this

As of 2026-03-20, practitioners should treat the linked facebookresearch/vjepa2 repository as the recorded implementation reference for this V-JEPA line; the sealed evidence alone does not justify operational guidance beyond that.

1. Установите PyTorch, timm и einops; для локального запуска предпочтительна сборка PyTorch с CUDA.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
2. Загрузите препроцессор и нужный backbone 2.1 через torch.hub; для меньшего ресурса начните с vjepa2_1_vit_base_384, для максимального качества — с gigantic.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
3. Прогоните видео через encoder и обучите лёгкую голову или linear probe для своей downstream-задачи; готовый demo показывает inference на видео.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
4. Для роботического эксперимента используйте V-JEPA 2-AC с image goals и model-predictive control; это отдельный action-conditioned checkpoint, а не обычный encoder 2.1.
  — <https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/>

## Best practices

- Выбирайте V-JEPA 2.1 для dense-представлений: релиз специально меняет objective и tokenizer для пространственно-временной согласованности, а не только увеличивает модель.
  — <https://arxiv.org/abs/2603.14482>
- Сопоставляйте размер checkpoint с задачей и ресурсами: доступны 80M, 300M, 1B и 2B варианты 2.1 при 384 px.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>
- На macOS заранее замените decord: базовый пакет не поддерживает macOS; авторы не закрепляют один рекомендованный fork.
  — <https://github.com/facebookresearch/vjepa2/blob/main/README.md>

## Superseded by this

- 2026-03-15 — для новых задач dense video/image representation прежний V-JEPA 2 не является предпочтительной стартовой точкой: V-JEPA 2.1 выпущена именно для улучшения dense и temporally consistent features.
- 2026-03-15 — нельзя считать V-JEPA 2.1 новым robotics action-conditioned checkpoint: V-JEPA 2-AC остаётся отдельной post-training веткой V-JEPA 2.

## Still unknown

- Официальный репозиторий не публикует GitHub Releases; датировка шага 2026-03-20 подтверждается как присутствие V-JEPA 2.1 в репозитории, но первичные даты самой статьи и README — 2026-03-15 и 2026-03-16 соответственно.
- Официальные инструкции показывают PyTorch Hub для V-JEPA 2.1, но Transformers-пример в README перечисляет только репозитории V-JEPA 2; поддержка 2.1 через этот путь не подтверждена README.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/facebookresearch/vjepa2 | facebookresearch/vjepa2 — official repository | 2026-09-05 |
| https://github.com/facebookresearch/vjepa2/blob/main/README.md | V-JEPA 2 repository README | 2026-09-05 |
| https://arxiv.org/abs/2603.14482 | V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning | 2026-09-05 |
| https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/ | Introducing the V-JEPA 2 world model and new benchmarks for physical reasoning | 2026-09-05 |
| https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/ | V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:v-jepa`, thread `v-jepa`, 1 dated events 2026-03-20 → 2026-03-20.
- **Practical note:** As of 2026-03-20, practitioners should treat the linked facebookresearch/vjepa2 repository as the recorded implementation reference for this V-JEPA line; the sealed evidence alone does not justify operational guidance beyond that.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
