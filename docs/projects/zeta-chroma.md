---
title: Zeta-Chroma
category: projects
date: 2026-03-18
tags: [project, zeta-chroma, zeta-chroma-base-model]
aliases: ["Zeta-Chroma"]
---

# Zeta-Chroma

**Development line:** `project:zeta-chroma` · thread `zeta-chroma-base-model`  
**Last event:** 2026-03-18 · 1 dated since 2026-03-18 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Zeta-Chroma — пиксельный diffusion-transformer для text-to-image, производный от Tongyi-MAI/Z-Image.

- Генерирует изображение напрямую в RGB и не использует VAE.
- Распространяется по Apache-2.0.
- Работает в ComfyUI; SD.Next добавил поддержку 28.04.2026.

Мера: опубликованный BF16-чекпойнт имеет размер около 13 GB.

Вердикт: модель пригодна для экспериментальной генерации, но остаётся WIP с регулярно заменяемыми весами и нестабильным качеством.

## Development line

- **2026-03-18 — Zeta-Chroma base-model artifact recorded.** On 2026-03-18, the Zeta-Chroma development line recorded a link to a Safetensors artifact in the project's Hugging Face repository. Linked social and repository-discussion URLs associate the item with the same project line. The supplied links do not establish the artifact's capabilities, training, licensing, or release terms.

## What changed

18.03.2026 — стал доступен ранний чекпойнт `zeta-chroma-base-x0-pixel-dino-distance.safetensors`; позднее описание репозитория уточняет, что Zeta-Chroma — WIP text-to-image модель на базе Tongyi-MAI/Z-Image.

01.03.2026 — владелец репозитория предписывал перед загрузкой в ComfyUI конвертировать ранний чекпойнт в Comfy-формат.

23.04.2026 — это требование устарело: пользователь ComfyUI сообщил, что актуальная сборка загружает модель без отдельной конвертации.

28.04.2026 — SD.Next выпустил поддержку Zeta-Chroma и зафиксировал, что модели требуется большое число шагов для приемлемого результата.

09–10.06.2026 — репозиторий получил обновлённые BF16-веса `full_1024_20M_dataset_run`; один файл был переименован из варианта с `dino-distance-1024` в `no-dino-1024`.

## How to use this

As of 2026-03-18, practitioners evaluating Zeta-Chroma should track the linked base Safetensors artifact as a dated candidate and verify its repository metadata and discussion before relying on it.

1. Скачайте актуальный checkpoint из репозитория Zeta-Chroma и поместите его в каталог `diffusion_models` выбранной установки.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>
2. В актуальном ComfyUI загрузите модель напрямую; для старых сборок проверяйте совместимость, поскольку ранняя инструкция требовала конвертации весов.
  — <https://huggingface.co/lodestones/Zeta-Chroma/discussions/9>
3. Начните с 1024 px по стороне, Euler, стандартного scheduler, CFG 4–7 и около 20 шагов; при слабом результате увеличивайте число шагов.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>

## Best practices

- Закладывайте модель как экспериментальную: фиксируйте хеш чекпойнта и workflow, потому что веса в репозитории обновляются во время обучения.
  — <https://huggingface.co/lodestones/Zeta-Chroma/tree/main>
- Не подключайте VAE и не переносите LoRA от Z-Image: для Zeta-Chroma это несовместимая схема.
  — <https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md>
- Для текущих весов предпочитайте больше шагов обычному короткому прогону: раннее обучение может давать слабые или галлюцинирующие результаты.
  — <https://github.com/vladmandic/sdnext/discussions/4808>

## Superseded by this

- 01.03.2026 — отдельная конвертация `zeta-chroma-base-x0-pixel-dino-distance.safetensors` в Comfy-формат больше не является актуальной общей рекомендацией: 23.04.2026 сообщено о прямой загрузке в актуальном ComfyUI.
- 09–10.06.2026 — имя `zeta-chroma-base-x0-pixel-dino-distance-1024.safetensors` заменено на `zeta-chroma-base-x0-pixel-no-dino-1024.safetensors`; не выбирайте файл только по старому имени.

## Still unknown

- Пост от 18.03.2026 недоступен для чтения через X, поэтому его точная формулировка не подтверждена; дата подтверждается идентификатором поста, а техническое описание — отдельными источниками.
- У репозитория нет стабильной версии или неизменяемого релизного тега; текущая ветка содержит продолжающиеся обновления весов.
- Сообщение о прямой загрузке без конвертации — практическое свидетельство пользователя, а не документированная гарантия ComfyUI для всех версий.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/lodestones/Zeta-Chroma/blob/main/zeta-chroma-base-x0-pixel-dino-distance.safetensors | zeta-chroma-base-x0-pixel-dino-distance.safetensors — Zeta-Chroma | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/tree/main | lodestones/Zeta-Chroma model repository | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/raw/main/README.md | Zeta-Chroma README | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/discussions/9 | Is there a working workflow for this model? | 2026-09-05 |
| https://github.com/mcmonkeyprojects/SwarmUI/blob/master/docs/Obscure%20Model%20Support.md | SwarmUI obscure model support: Zeta Chroma | 2026-09-05 |
| https://github.com/vladmandic/sdnext/discussions/4808 | SD.Next Release 2026-04-28 | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/commit/53a5aa59f875b3b9ee31ef1a6afb9a480f9c62f1 | full_1024_20M_dataset_run (bf16) | 2026-09-05 |
| https://huggingface.co/lodestones/Zeta-Chroma/commit/eb27e547dcf324b4ecf219ea3fdd9e913422d5cb | Rename zeta-chroma-base-x0-pixel-dino-distance-1024.safetensors to zeta-chroma-base-x0-pixel-no-dino-1024.safetensors | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:zeta-chroma`, thread `zeta-chroma-base-model`, 1 dated events 2026-03-18 → 2026-03-18.
- **Practical note:** As of 2026-03-18, practitioners evaluating Zeta-Chroma should track the linked base Safetensors artifact as a dated candidate and verify its repository metadata and discussion before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
