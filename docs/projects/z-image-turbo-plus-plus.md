---
title: Z-Image Turbo++ — Research reference
category: projects
date: 2026-06-17
tags: [project, research-reference, z-image-turbo-plus-plus, z_image]
aliases: ["Z-Image Turbo++"]
---

# Z-Image Turbo++ — Research reference

**Development line:** `project:z-image-turbo-plus-plus` · thread `research-reference`  
**Last event:** 2026-06-17 · 1 dated since 2026-06-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Z-Image Turbo++ — исследовательская text-to-image модель для команд, проверяющих двухшаговую генерацию вместо восьмишагового Z-Image Turbo. — Distribution-Aligned Adversarial Learning: использует изображения учителя как GAN-таргет. — Step-Decoupled Parameterization: разделяет параметры двух денойзинговых шагов. — End-to-End Training with Iterative Regularization: передаёт финальную оценку качества в первый шаг. 2 шага вместо 8 у учителя; отдельный готовый checkpoint не подтверждён в изученных первичных источниках. Вердикт: это ориентир для воспроизведения исследования, а для рабочего запуска сегодня подтверждён только Z-Image-Turbo.

## Development line

- **2026-06-17 — Z-Image Turbo++ paper reference linked.** On 2026-06-17, a Hugging Face Papers page, identified as paper 2606.12575, was linked in the Z-Image Turbo++ development line. The dated link establishes a research reference for the project, but does not establish the paper's title, technical claims, or release status. This history event records the reference itself rather than any unverified capabilities.

## What changed

2026-06-17 — Z-Image Turbo++ описан как двухшаговая дистилляция от восьмишагового Z-Image Turbo; отличие — число шагов, а не подтверждённый отдельный релиз весов.

## How to use this

From 2026-06-17, practitioners should treat the linked Hugging Face Papers record as a research reference to investigate, not as evidence of unverified technical claims or a product release.

1. Для исследовательского воспроизведения реализовать два независимых денойзинговых шага, обучая их на изображениях восьмишагового учителя и сохраняя вспомогательный loss первого шага.
  — <https://arxiv.org/abs/2606.12575>
2. Для практической генерации не маркировать запуск как Turbo++: использовать отдельно опубликованный восьмишаговый Tongyi-MAI/Z-Image-Turbo.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
3. Для Z-Image-Turbo загрузить ZImagePipeline в bfloat16 на CUDA, задать num_inference_steps=9, что даёт 8 DiT-проходов, и guidance_scale=0.0.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Best practices

- Разделять результаты Turbo++ и Z-Image-Turbo в экспериментах: статья определяет Turbo++ как 2-step, а официальная карточка Turbo — как 8-step.
  — <https://arxiv.org/abs/2606.12575>
- Для опубликованного Turbo не повышать guidance_scale: карточка модели задаёт 0.0.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>
- Использовать bfloat16 на поддерживаемом GPU; CPU offload включать только при дефиците памяти, принимая более медленный запуск.
  — <https://huggingface.co/Tongyi-MAI/Z-Image-Turbo>

## Superseded by this

- 2026-06-10 — исследовательское ограничение линии Z-Image только диапазоном 4–8 шагов: работа демонстрирует двухшаговую дистилляцию.

## Still unknown

- Отдельные официальные веса, код, model card или совместимый runtime для Turbo++ не подтверждены среди изученных первичных источников; отсутствие на проверенных страницах не доказывает, что их не существует.
- В аннотации Turbo++ нет численных таблиц качества или скорости; для решения о внедрении нужен воспроизводимый бенчмарк с теми же промптами и железом.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/papers/2606.12575 | Paper page - High-Fidelity Two-Step Image Generation via Teacher-Aligned End-to-End Distillation | 2026-09-05 |
| https://arxiv.org/abs/2606.12575 | High-Fidelity Two-Step Image Generation via Teacher-Aligned End-to-End Distillation | 2026-09-05 |
| https://arxiv.org/abs/2511.22699 | Z-Image: An Efficient Image Generation Foundation Model with Single-Stream Diffusion Transformer | 2026-09-05 |
| https://huggingface.co/Tongyi-MAI/Z-Image-Turbo | Tongyi-MAI/Z-Image-Turbo | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:z-image-turbo-plus-plus`, thread `research-reference`, 1 dated events 2026-06-17 → 2026-06-17.
- **Practical note:** From 2026-06-17, practitioners should treat the linked Hugging Face Papers record as a research reference to investigate, not as evidence of unverified technical claims or a product release.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
