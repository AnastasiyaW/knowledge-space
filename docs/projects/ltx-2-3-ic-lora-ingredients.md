---
title: LTX-2.3 IC-LoRA Ingredients — LTX-2.3
category: projects
date: 2026-06-19
tags: [ltx-2-3, ltx-2-3-ic-lora-ingredients, ltx_2_3, project]
aliases: ["LTX-2.3 IC-LoRA Ingredients"]
---

# LTX-2.3 IC-LoRA Ingredients — LTX-2.3

**Development line:** `project:ltx-2-3-ic-lora-ingredients` · thread `ltx-2-3`  
**Last event:** 2026-06-19 · 1 dated since 2026-06-19 · **Researched:** 2026-09-05 · confidence: medium

## What it is

LTX-2.3 IC-LoRA Ingredients — IC-LoRA для практиков LTX-2.3-22B: он получает композитный reference sheet как статическое видео и генерирует новый клип по текстовому действию. Возможности: согласованность персонажей, костюмов, реквизита и локации; разделение описания листа и действия; работа через специализированный IC-LoRA workflow. Рабочий обучающий бакет: 768×448, 121 кадр, 24 fps. Вердикт: это не общий T2V-модуль и не средство редактирования готового видео, а узкий способ сделать повторяющиеся элементы сцены согласованными.

## Development line

- **2026-06-19 — Lightricks published an LTX-2.3 IC-LoRA Ingredients model page.** On 2026-06-19, a Hugging Face model page for Lightricks' LTX-2.3-22B IC-LoRA Ingredients was recorded in this development line. The dated link establishes a distinct LTX-2.3 model artifact, but the supplied evidence does not establish its release notes, capabilities, or recommended workflow.

## What changed

2026-06-19 — модель появилась в ветке как LTX-2.3-22b-IC-LoRA-Ingredients; карточка уточняет, что это reference-sheet control для dev-версии LTX-2.3-22B, с файлом `ltx-2.3-22b-ic-lora-ingredients-0.9.safetensors`, rank 128 и рекомендованным чекпойнтом на шаге 12 000.

2026-06-17 — сторонний индекс датирует официальный выпуск 17 июня, а не 19 июня; 19 июня остаётся датой зафиксированного события, а не подтверждённой датой релиза.

## How to use this

As of 2026-06-19, practitioners should treat LTX-2.3-22B IC-LoRA Ingredients as a separately tracked LTX-2.3 model artifact and consult its Hugging Face page before selecting it for an ingredients-related workflow.

1. Получите доступ к gated-репозиторию, скачайте Ingredients LoRA и совместимую LTX-2.3-22B базу.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
2. Соберите один reference sheet на чёрном фоне: отдельные чистые панели для персонажей, реквизита и локации; превратите лист в статическое видео, совпадающее с выходом по разрешению и fps и длиной не менее 121 кадра.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
3. В ComfyUI загрузите базовую LTX-2.3-22B модель и Ingredients LoRA через IC-LoRA/reference workflow, затем подайте static-video лист в control/reference-вход.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
4. Пишите промпт в двух секциях: `Reference sheet:` для содержимого панелей и `Generated video:` для действия или кадра.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
5. Для воспроизводимого старта используйте официальный ComfyUI workflow, в котором зафиксированы `ltx-2.3-22b-dev.safetensors` и Ingredients LoRA.
  — <https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.3/LTX-2.3_ICLoRA_Ingredients_Single_Stage_Distilled.json>

## Best practices

- Начинайте с LoRA strength 1.0 для проверки пайплайна; карточка рекомендует 1.4 как рабочее значение.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Оставайтесь в обучающем бакете 768×448, 121 кадр, 24 fps; другие разрешения, значительно более длинные клипы и запуск без reference sheet находятся вне распределения обучения.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Давайте критичным персонажам и предметам крупные, чистые панели; для лица добавляйте фронтальный крупный план и полный разворот, не помещая текст на панели.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Не используйте обычный LoRA loader, если он не передаёт путь reference video: он загрузит веса, но не применит reference conditioning.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>

## Superseded by this

- 2026-06-17 — предположение, что Ingredients является универсальным text-to-video или редактором существующего ролика, неверно: он требует reference-sheet conditioning и генерирует новый клип.
- 2026-06-17 — рекомендация подавать короткий reference-клип устарела: reference static video должен иметь не менее 121 кадра.

## Still unknown

- Официальная карточка, прочитанная 2026-09-05, не показывает собственную дату публикации; дата 2026-06-17 для релиза подтверждена только вторичным индексом.
- Не найден датированный первичный источник, который объясняет разницу между датой события 2026-06-19 и датой 2026-06-17 в индексе.
- Текущая совместимость с LTX-2.5 не подтверждена: официальная документация LTX предупреждает, что LoRA работает только с моделью, на которой она обучалась.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients | Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients model card | 2026-09-05 |
| https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.3/LTX-2.3_ICLoRA_Ingredients_Single_Stage_Distilled.json | LTX-2.3 IC-LoRA Ingredients Single Stage Distilled workflow | 2026-09-05 |
| https://github.com/NitishMamadgi/awesome-ltx2.3-ic_lora | awesome-ltx2.3-ic_lora index | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ltx-2-3-ic-lora-ingredients`, thread `ltx-2-3`, 1 dated events 2026-06-19 → 2026-06-19.
- **Practical note:** As of 2026-06-19, practitioners should treat LTX-2.3-22B IC-LoRA Ingredients as a separately tracked LTX-2.3 model artifact and consult its Hugging Face page before selecting it for an ingredients-related workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
