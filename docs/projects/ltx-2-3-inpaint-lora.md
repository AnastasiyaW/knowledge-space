---
title: LTX-2.3 inpaint LoRA
category: projects
date: 2026-03-24
tags: [ltx-2-3-inpaint-lora, ltx_2_3_inpaint_lora, project]
aliases: ["LTX-2.3 inpaint LoRA"]
---

# LTX-2.3 inpaint LoRA

**Development line:** `project:ltx-2-3-inpaint-lora` · thread `ltx-2-3-inpaint-lora`  
**Last event:** 2026-03-24 · 1 dated since 2026-03-24 · **Researched:** 2026-09-05 · confidence: medium

## What it is

LTX-2.3 inpaint LoRA — набор community LoRA для видеомаскирования в Lightricks/LTX-2.3: text-only inpaint, inpaint с референсом и выбор checkpoint по следованию промпту или использованию маски. — заменяет или добавляет объекты только внутри подготовленной области; — MR2V-вариант принимает визуальный референс либо пустой референс для text-only режима; — это не официальный LTX In-Outpainting IC-LoRA и не заявленное решение для face/body swap. Лимит: для MR2V критичны размер и подготовка маски; автор указывает, что ниже FP8 качество заметно падает. Вердикт: подходит для объектных правок короткого видео, если workflow воспроизводит его цветовую разметку; для лиц и официального LTX-2.5 in/outpainting нужен другой адаптер.

## Development line

- **2026-03-24 — LTX LoRA distribution links recorded.** On March 24, 2026, this development line recorded links to an LTX-LoRAs repository on Hugging Face and an LTX LoRAs page on Civitai. The links indicate a public distribution or discovery step relevant to the project, but the record does not establish the exact model variant, inpainting behavior, compatibility, provenance, or release details.

## What changed

2026-03-24 — LTX-2.3 inpaint LoRA был показан как готовый workflow для замены объектов, локальной правки кадров и исправления отдельной области без перегенерации всего клипа. 2026-04-06 — опубликован экспериментальный MR2V-вариант `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors`: reference-guided inpaint внутри маски, ориентированный на объекты, не face/body swap. 2026-04-08 — README исправил имена двух text-to-video checkpoint: прежние `ltx23_inpaint_rank128...` заменены на `ltx23_inpaint_masked_t2v_rank128...`.

## How to use this

As of 2026-03-24, practitioners should treat the linked Hugging Face and Civitai locations as sources to inspect and verify before use, rather than assuming they provide a confirmed LTX-2.3 inpainting LoRA or a particular compatibility claim.

1. Установить LTX-2 pipeline через `uv sync --frozen`, скачать набор LoRA и Gemma text encoder.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main>
2. Для native pipeline загрузить нужный файл через `--lora` и начать с веса 1.0; для image-to-video добавить `--image`.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main>
3. Для inpaint не передавать маску отдельным каналом: встроить её в guide video и подать через `LTXVAddGuideMulti`; маска — magenta `(255,0,255)`, reference area — chroma-key green `(0,255,0)`.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
4. Для замены объекта с референсом выбрать `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors`; для text-only режима использовать пустой reference и подробный prompt.
  — <https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/>

## Best practices

- Сначала сравнить 2500-step и 10000-step варианты: первый ориентирован на следование промпту, второй — на заполнение маски; не считать один checkpoint универсально лучшим.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
- Для MR2V начать с Blockify Mask size 8 и при необходимости расширять маску: training distribution использовал блочную разметку, а тесная маска ухудшает замену объекта.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
- Не применять MR2V как face/body-swap модель; она обучалась преимущественно на объектах. Проверять результат как минимум в FP8, поскольку более низкая точность у автора дала заметное падение качества.
  — <https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/>

## Superseded by this

- 2026-04-08: имена `ltx23_inpaint_rank128_v1_02500steps.safetensors` и `ltx23_inpaint_rank128_v1_10000steps.safetensors` в примерах заменены на `ltx23_inpaint_masked_t2v_rank128_v1_02500steps.safetensors` и `ltx23_inpaint_masked_t2v_rank128_v1_10000steps.safetensors`.
- Официальный LTX-2.5 In-Outpainting IC-LoRA не заменяет автоматически этот community-набор: это отдельный checkpoint и workflow.

## Still unknown

- Civitai returned no readable page content during research, поэтому его наличие подтверждено только как ссылка из события, без независимой проверки текущих файлов или версии.
- Временная метка первоначальной загрузки каждого файла Hugging Face не получена; 24.03.2026 подтверждает публичное представление workflow, а не Git timestamp конкретного weight.
- Официальный `ltx-2.3-22b-ic-lora-in-outpainting-0.9.safetensors`, который LTX использует в LTX-2.5, не доказан как совместимый или взаимозаменяемый с community-файлами Alissonerdx.
- event_findings:[{"event_date":"2026-03-24","finding":"В этот день набор был описан как workflow для удаления или замены объектов, точечной правки кадров и исправления одной области без перегенерации всего клипа.","source_date":"2026-03-24","source_url":"https://www.youtube.com/watch?v=PX3-OqOz6rE"}]
- new_events:[{"date":"2026-04-06","finding":"Автор назвал точный экспериментальный MR2V-файл `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors`; он делает reference-based inpaint внутри маски, ориентирован на объекты и не предназначен для face/body swap.","source_date":"2026-04-06","source_url":"https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/"},{"date":"2026-04-08","finding":"README переименовал два T2V inpaint checkpoint в варианты с `masked_t2v`, исправив ранее показанные имена файлов.","source_date":"2026-04-08","source_url":"https://huggingface.co/Alissonerdx/LTX-LoRAs/commit/345088ffcbda7ea9680bd73e145371e527450ff6"}]

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main | Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md | README.md · Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://civitai.com/models/2484952/ltx-loras | LTX LoRAs - LTX-2.3 Inpainting | Civitai | 2026-09-05 |
| https://www.youtube.com/watch?v=PX3-OqOz6rE | LTX23 Inpainting Is Here: Alissonerdx Inpaint LoRA + Ready Workflows | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/ | Inpainting with reference to LTX-2.3 (MR2V) | 2026-09-05 |
| https://huggingface.co/Alissonerdx/LTX-LoRAs/commit/345088ffcbda7ea9680bd73e145371e527450ff6 | Update README.md · Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://docs.ltx.io/open-source-model/feature-guides/editing-effects/in-outpainting | Inpainting and Outpainting | LTX Documentation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ltx-2-3-inpaint-lora`, thread `ltx-2-3-inpaint-lora`, 1 dated events 2026-03-24 → 2026-03-24.
- **Practical note:** As of 2026-03-24, practitioners should treat the linked Hugging Face and Civitai locations as sources to inspect and verify before use, rather than assuming they provide a confirmed LTX-2.3 inpainting LoRA or a particular compatibility claim.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
