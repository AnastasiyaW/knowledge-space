---
title: Alibaba — Generative-model research
category: organizations
tags: [alibaba, alibaba:mofusion, alibaba_latent_to_pixel, generative-model-research, humanomniv2, organization]
aliases: ["Alibaba"]
---

# Alibaba — Generative-model research

**Development line:** `organization:alibaba` · thread `generative-model-research`  
**Events:** 3 dated, 2022-12-11 → 2026-08-23 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Alibaba — не единый AI-инструмент, а набор исследовательских результатов для R&D-команд: — MoFusion — diffusion-модель для text-to-motion, motion completion и смешивания управляющих сигналов. — HumanOmniV2 — open-weight модель для рассуждений по изображениям, видео и аудио с учётом полного контекста. — Latent-to-pixel — рецепт обучения text-to-image модели: сначала latent space, затем pixel space. Лимит: из этих трёх работ только HumanOmniV2 имеет опубликованные код, веса и evaluation workflow; карточка указывает 9B BF16 и отсутствие hosted inference provider. Вердикт: HumanOmniV2 можно брать для локального исследовательского запуска, две остальные работы — как исследовательские основы, не как готовую замену production-инструменту.

## Development line

- **2022-12-11 — Alibaba development line recorded the MoFusion project.** On 2022-12-11, the Alibaba development line recorded a link to the MoFusion project. This is treated as a material research-development checkpoint because the sealed evidence identifies a named project artifact. The supplied evidence does not establish the original post's wording, authorship, or deployment status.
- **2025-07-09 — Alibaba development line recorded HumanOmniV2 research resources.** On 2025-07-09, the Alibaba development line recorded links to HumanOmniV2 research resources, including a paper page and source repository. This is treated as a material checkpoint because the dated links identify a named research artifact with associated code. The sealed evidence does not establish the original post's wording, authorship, technical claims, or release status.
- **2026-08-23 — Alibaba development line recorded a Latent-to-Pixel paper.** On 2026-08-23, the Alibaba development line recorded a link to a Latent-to-Pixel paper. This is treated as a material research checkpoint in the generative-model line, rather than as a product-release claim. The supplied evidence does not establish the original post's wording, authorship, technical claims, or availability.

## What changed

Alibaba — линии развиваются параллельно, а не как последовательные версии одного продукта. — 2022-12-11: MoFusion предложил единый pretrained diffusion Transformer для задач синтеза движения, с cross-attention для разных контролей и адаптером скелета. — 2025-07-09: HumanOmniV2 добавил context-first omni-modal reasoning: контекстные и логические rewards, IntentBench и открытый исследовательский стек для video/audio/image задач. — 2026-08-23: работа по pixel-space diffusion показала, что прямой large-scale pre-training в пикселях сходится медленнее; предложен переход latent-to-pixel во время post-training с заявленным ускорением end-to-end inference в 3.18–4.75 раза. — Найдено сегодня, 2026-09-03: MoFusion-репозиторий архивирован и read-only; HumanOmniV2 публикует веса, код и данные; для статьи 2608.16887 на момент проверки не привязаны модель, датасет или Space.

## How to use this

As of 2026-08-23, practitioners tracking Alibaba should treat the dated MoFusion, HumanOmniV2, and Latent-to-Pixel artifacts as a research lineage and verify each paper or repository directly before using it as implementation or deployment guidance.

1. Если нужен работающий артефакт из этой линии, начните с HumanOmniV2: клонируйте авторский репозиторий и получите веса по его ссылкам на Hugging Face или ModelScope.
  — <https://github.com/HumanMLLM/HumanOmniV2>
2. Для воспроизводимой оценки скачайте IntentBench, Daily-Omni и WorldSense, укажите пути к видео и запустите предоставленный distributed evaluation; пример использует 8 процессов.
  — <https://github.com/HumanMLLM/HumanOmniV2>
3. Для обучения скачайте long-CoT данные и указанные наборы, задайте JSON- и video-path в YAML-конфигах, затем выполняйте SFT, Stage 1 RL и Stage 2 RL в документированном порядке.
  — <https://github.com/HumanMLLM/HumanOmniV2>
4. Для нового text-to-image R&D используйте latent-space pre-training, затем отдельно адаптируйте модель к pixel space; это рецепт обучения, а не опубликованный готовый inference endpoint.
  — <https://arxiv.org/pdf/2608.16887>

## Best practices

- Для video/audio reasoning сначала формируйте полный мультимодальный контекст, затем отвечайте: работа специально нацелена на пропущенные визуальные и аудиальные сигналы.
  — <https://arxiv.org/pdf/2506.21277>
- Не оценивайте HumanOmniV2 на одном удобном примере: используйте IntentBench вместе с Daily-Omni и WorldSense, предварительно проверив пути к видео.
  — <https://github.com/HumanMLLM/HumanOmniV2>
- Разделяйте права на код, веса и видео: код и модель заявлены под Apache-2.0, а самособранные видео имеют CC BY-NC-SA 4.0.
  — <https://huggingface.co/PhilipC/HumanOmniV2>
- Считайте IntentBench отдельным non-commercial/no-derivatives набором и проверяйте допустимость использования до обучения или коммерческого применения.
  — <https://huggingface.co/datasets/PhilipC/IntentBench>
- Для latent-to-pixel не переносите noise scale как теоретическую константу: авторы получили лучший результат при gamma=2 в своей установке и прямо требуют эмпирической калибровки.
  — <https://arxiv.org/pdf/2608.16887>

## Superseded by this

- 2023-02-28 — предположение, что MoFusion является активно поддерживаемым официальным implementation path, устарело: репозиторий архивирован и read-only.
- 2025-07-01 — состояние HumanOmniV2 «только статья и часть кода» заменено опубликованными training/evaluation code, weights, IntentBench и training data.
- Не установлено, что MoFusion, HumanOmniV2 и latent-to-pixel работа заменяют друг друга: это разные задачи и модальности, поэтому миграция между ними не является upgrade path.

## Still unknown

- MoFusion, HumanOmniV2 и pixel-space работа связаны общей affiliation Alibaba, но первичные источники не показывают между ними единой модели, API или product roadmap.
- Для статьи 2608.16887 не найден официальный код, веса, датасет или serving endpoint; практическая воспроизводимость требует самостоятельной реализации.
- У HumanOmniV2 опубликованы training и evaluation workflow, но нет авторского end-user inference quickstart; generic Transformers snippet на Hugging Face не был независимо запущен.
- Текущая совместимость архивного MoFusion с современными зависимостями и его пригодность для production не подтверждены.

## Sources

| source | title | read |
|---|---|---|
| https://ofa-sys.github.io/MoFusion/ | MoFusion: Pretrained Diffusion Models for Unified Human Motion Synthesis | 2026-09-03 |
| https://github.com/OFA-Sys/MoFusion | OFA-Sys/MoFusion | 2026-09-03 |
| https://arxiv.org/pdf/2212.02837 | Pretrained Diffusion Models for Unified Human Motion Synthesis | 2026-09-03 |
| https://huggingface.co/papers/2506.21277 | Paper page — HumanOmniV2: From Understanding to Omni-Modal Reasoning with Context | 2026-09-03 |
| https://arxiv.org/pdf/2506.21277 | HumanOmniV2: From Understanding to Omni-Modal Reasoning with Context | 2026-09-03 |
| https://github.com/HumanMLLM/HumanOmniV2 | HumanMLLM/HumanOmniV2 | 2026-09-03 |
| https://huggingface.co/PhilipC/HumanOmniV2 | PhilipC/HumanOmniV2 | 2026-09-03 |
| https://huggingface.co/datasets/PhilipC/IntentBench | PhilipC/IntentBench | 2026-09-03 |
| https://huggingface.co/papers/2608.16887 | Paper page — An Empirical Study of Training Pixel-Space Text-to-Image Diffusion Models | 2026-09-03 |
| https://arxiv.org/pdf/2608.16887 | An Empirical Study of Training Pixel-Space Text-to-Image Diffusion Models | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:alibaba`, thread `generative-model-research`, 3 dated events 2022-12-11 → 2026-08-23.
- **Practical note:** As of 2026-08-23, practitioners tracking Alibaba should treat the dated MoFusion, HumanOmniV2, and Latent-to-Pixel artifacts as a research lineage and verify each paper or repository directly before using it as implementation or deployment guidance.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
