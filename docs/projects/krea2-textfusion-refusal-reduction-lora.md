---
title: Krea2 TextFusion Refusal-Reduction LoRA
category: projects
date: 2026-07-15
tags: [krea2-textfusion-refusal-reduction-lora, krea2_textfusion_refusal_reduction_lora, project]
aliases: ["Krea2 TextFusion Refusal-Reduction LoRA"]
---

# Krea2 TextFusion Refusal-Reduction LoRA

**Development line:** `project:krea2-textfusion-refusal-reduction-lora` · thread `krea2-textfusion-refusal-reduction-lora`  
**Last event:** 2026-07-15 · 1 dated since 2026-07-15 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Krea2 TextFusion Refusal-Reduction LoRA — rank-64 LoRA для Krea 2, предназначенная уменьшать подавление уже известных базовой модели концептов. — изменяет attention и MLP в четырёх TextFusion-блоках; — не добавляет стили, персонажей или новые визуальные концепты; — не меняет image transformer, txtmlp или 1×12 tap projector. Текущая доступная версия — v2.0; публично заявленная рекомендация силы: 0.75–1.00.

## Development line

- **2026-07-15 — Civitai reference recorded for Krea2 TextFusion Refusal-Reduction LoRA.** Rank-64 TextFusion-only LoRA для Krea 2; независимая копия описания подтверждает четыре целевых блока и силу 1.00, но не даёт собственной даты публикации, поэтому это не датированное дополнение к событию.

## What changed

2026-07-15 — опубликована ветка v1.0: rank-64 TextFusion-only LoRA для Krea 2; независимая копия описания подтверждает четыре целевых блока и силу 1.00, но не даёт собственной даты публикации, поэтому это не датированное дополнение к событию. 2026-08-29 — v2.0: заявлены лучшее следование промпту и менее сглаженные текстуры; рекомендован диапазон 0.75–1.00, 1.50 отмечена как рабочая, но не рекомендуемая.

## How to use this

From 2026-07-15, practitioners should use the linked Civitai page as the discovery reference for this LoRA and verify its current version, license, and usage details there before adoption; the sealed evidence supports no stronger operational recommendation.

1. Подготовьте локальный workflow Krea 2 Turbo в ComfyUI и установите базовые веса, Qwen3VL text encoder и VAE по официальной схеме.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
2. Скачайте файл LoRA, положите его в `ComfyUI/models/loras/`, выберите этот файл в LoRA-узле Krea 2 и включите LoRA.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
3. Для v2.0 начните с силы 0.75–1.00; сравните результат с тем же seed без LoRA, прежде чем менять sampler или prompt.
  — <https://tungsten.run/model/GJjkvTwp3m>

## Best practices

- Не используйте этот адаптер как style или concept LoRA: он заявлен для маршрута TextFusion, а не для добавления обученных визуальных понятий.
  — <https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora>
- Держите базовый Krea 2 workflow воспроизводимым: используйте официальный шаблон и включайте LoRA отдельным переключателем, чтобы можно было проверить её вклад.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
- Не повышайте v2.0 сразу до 1.50: страница запуска помечает это значение как нерекомендуемое.
  — <https://tungsten.run/model/GJjkvTwp3m>

## Superseded by this

- 2026-08-29: для v2.0 прежняя рекомендация v1.0 «strength 1.00» заменена текущим стартовым диапазоном 0.75–1.00; это относится к настройке, а не доказывает прекращение доступности v1.0.

## Still unknown

- Первичная карточка Civitai не открылась при проверке, поэтому её исходная дата публикации и авторское описание v1.0 не подтверждены напрямую.
- Не найден независимый датированный changelog, связывающий v2.0 с той же авторской публикацией; совпадают название и Civitai model ID в ссылке на странице v2.0.
- Схема ответа не содержит отдельных полей event_findings и new_events: датированные сведения включены в what_changed.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.com/models/2775340/krea2-textfusion-refusal-reduction-lora | Krea2 TextFusion Refusal-Reduction LoRA | Civitai | 2026-09-05 |
| https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora | Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora | 2026-09-05 |
| https://tungsten.run/model/GJjkvTwp3m | Krea2 TextFusion Refusal-Reduction v2.0 | 2026-09-05 |
| https://docs.comfy.org/tutorials/image/krea/krea-2 | Krea 2 | ComfyUI Documentation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:krea2-textfusion-refusal-reduction-lora`, thread `krea2-textfusion-refusal-reduction-lora`, 1 dated events 2026-07-15 → 2026-07-15.
- **Practical note:** From 2026-07-15, practitioners should use the linked Civitai page as the discovery reference for this LoRA and verify its current version, license, and usage details there before adoption; the sealed evidence supports no stronger operational recommendation.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
