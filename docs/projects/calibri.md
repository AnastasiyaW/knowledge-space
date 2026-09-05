---
title: Calibri
category: projects
date: 2026-03-29
tags: [calibri, project]
aliases: ["Calibri"]
---

# Calibri

**Development line:** `project:calibri` · thread `calibri`  
**Last event:** 2026-03-29 · 1 dated since 2026-03-29 · **Researched:** 2026-09-05 · confidence: high

## What it is

Calibri: open-source метод калибровки Diffusion Transformer для разработчиков text-to-image пайплайнов. — добавляет коэффициенты на выходах блоков DiT; — подбирает их CMA-ES по reward-модели; — поддерживает FLUX.1-dev, Stable Diffusion 3.5 и Qwen-Image. Лимит: готовые веса опубликованы только для FLUX.1-dev и Qwen-Image; официального hosted inference нет. Вывод: это инструмент для ускорения и настройки существующей DiT-модели, не новая базовая модель.

## Development line

- **2026-03-29 — Calibri project resources became publicly discoverable.** 12B `v-gen-ai/flux-calibri-gates` и 20B `v-gen-ai/qwen-calibri`; статья была впервые отправлена в arXiv 2026-03-25.

## What changed

2026-03-29 — появились две готовые BF16-модели Calibri: 12B `v-gen-ai/flux-calibri-gates` и 20B `v-gen-ai/qwen-calibri`; статья была впервые отправлена в arXiv 2026-03-25. 2026-04-13 — опубликованы открытые calibration weights для FLUX.1-dev и Qwen-Image. 2026-07-29 — статья обновлена до arXiv v2; репозиторий не описывает отдельный новый runtime-релиз для этой редакции.

## How to use this

From 2026-03-29, practitioners should use the linked project page, repository, and Hugging Face collection as the starting points for evaluating Calibri; exact version and usage guidance remain unverified.

1. Для готовой генерации с FLUX загрузите `v-gen-ai/flux-calibri-gates` через Diffusers в BF16 на CUDA и используйте 15 шагов, guidance scale 3.5 и базовое разрешение 512×512.
  — <https://huggingface.co/v-gen-ai/flux-calibri-gates>
2. Для готовой генерации с Qwen используйте `v-gen-ai/qwen-calibri` с указанным в model card custom pipeline; стартовые параметры — 15 шагов, `true_cfg_scale=4.0`, 512×512.
  — <https://huggingface.co/v-gen-ai/qwen-calibri>
3. Для собственной калибровки клонируйте репозиторий, создайте окружение через `uv sync`, запустите нужный reward server и стартуйте CMA-ES через Accelerate с конфигурацией из `configs/calibri.py`.
  — <https://github.com/v-gen-ai/Calibri>

## Best practices

- Начинайте с опубликованных весов и их штатных параметров, а не с обучения: для FLUX карточка задаёт 15 шагов, guidance scale 3.5 и 512×512.
  — <https://huggingface.co/v-gen-ai/flux-calibri-gates>
- При обучении сначала поднимите HPSv3 или Q-Align reward server; основной training script без выбранной reward-службы не является воспроизводимым запуском.
  — <https://github.com/v-gen-ai/Calibri>
- Выбирайте гранулярность поиска по задаче: block scaling около 57 параметров, layer scaling около 76, gate scaling около 114.
  — <https://github.com/v-gen-ai/Calibri>
- Проверяйте калибровку на своём validation dataset: запуск inference без `--prompt` генерирует валидационные изображения и считает reward-метрики.
  — <https://github.com/v-gen-ai/Calibri>

## Superseded by this

- 2026-04-13 — для FLUX.1-dev и Qwen-Image устарело предположение, что Calibri можно получить только через самостоятельную CMA-ES-калибровку: опубликованы готовые calibration weights.
- 2026-07-29 — arXiv v1 от 2026-03-25 заменён редакцией v2; содержание изменений между версиями в просмотренных источниках не раскрыто.

## Still unknown

- `event_findings`: 2026-03-29 — Hugging Face collection, updated 2026-03-27, уточняет, что релиз состоял из `v-gen-ai/flux-calibri-gates` (12B) и `v-gen-ai/qwen-calibri` (20B); arXiv v1 датирован 2026-03-25. Источники: https://huggingface.co/collections/v-gen-ai/calibri-models; https://arxiv.org/abs/2603.24800.
- `new_events`: 2026-04-13 — открыты calibration weights для FLUX.1-dev и Qwen-Image. Источник: https://github.com/v-gen-ai/Calibri.
- `new_events`: 2026-07-29 — arXiv v2 обновил статью; просмотренная запись не даёт списка содержательных различий с v1. Источник: https://arxiv.org/abs/2603.24800.
- Автогенерируемый фрагмент Diffusers в карточке Qwen отличается от отдельного раздела Guide to run: второй указывает `makriot/qwen-calibri`, `custom_pipeline` и `trust_remote_code=True`. Нельзя подтвердить по просмотренным источникам, какой из двух путей сейчас является каноническим.

## Sources

| source | title | read |
|---|---|---|
| https://v-gen-ai.github.io/Calibri-page/ | Calibri: Parameter-Efficient Calibration of Diffusion Transformers | 2026-09-05 |
| https://github.com/v-gen-ai/Calibri | v-gen-ai/Calibri — official implementation and README | 2026-09-05 |
| https://huggingface.co/collections/v-gen-ai/calibri-models | Calibri models — v-gen-ai Collection | 2026-09-05 |
| https://huggingface.co/v-gen-ai/flux-calibri-gates | v-gen-ai/flux-calibri-gates model card | 2026-09-05 |
| https://huggingface.co/v-gen-ai/qwen-calibri | v-gen-ai/qwen-calibri model card | 2026-09-05 |
| https://arxiv.org/abs/2603.24800 | Calibri: Enhancing Diffusion Transformers via Parameter-Efficient Calibration | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:calibri`, thread `calibri`, 1 dated events 2026-03-29 → 2026-03-29.
- **Practical note:** From 2026-03-29, practitioners should use the linked project page, repository, and Hugging Face collection as the starting points for evaluating Calibri; exact version and usage guidance remain unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
