---
title: ComfyUI-LoraTags
category: projects

tags: [comfyui-loratags, comfyui_loratags, project]
aliases: ["ComfyUI-LoraTags"]
---

# ComfyUI-LoraTags

**Development line:** `project:comfyui-loratags` · thread `comfyui-loratags`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI-LoraTags — пара узлов для пользователей ComfyUI, которым нужно собирать несколько LoRA и не терять их trigger words. — LoRA Loader (LoraTags): загружает стек LoRA и отдаёт MODEL, CLIP и TAGS. — CLIP Text Encode (Auto-Tags): добавляет строку TAGS к текстовому prompt перед кодированием. — Tag Manager: по SHA-256 файла запрашивает у Civitai имя модели, исходные триггеры, до четырёх превью и ссылку на модель; пользовательские теги хранятся рядом. Мера и ограничение: репозиторий показывает 16 коммитов, не публикует релизы, а установка через ComfyUI Manager всё ещё обозначена как будущая. Вердикт: это ранний, пригодный для локальной установки узел, а не замена проверенному LoRA-лоадеру с долгой историей совместимости.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-15 — ранний доступ к ComfyUI-LoraTags был анонсирован автором; это отдельное, более раннее событие. 2026-07-23 — ComfyUI-LoraTags появился как пакет из двух узлов: Loader собирает активные LoRA и их теги в TAGS, а Auto-Tags подаёт их в conditioning. Первичный README уточняет недостающие детали: lookup идёт по SHA-256 `.safetensors`, возвращает до четырёх превью, а база сохраняется в `lora_master_tags.json`. Поздней датированной версии или релиза первичные материалы не показывают.

## How to use this

As of 2026-07-23, treat the linked GitHub repository as a lead for follow-up research only; do not infer a supported installation, release, or feature change from this record.

1. Клонируйте репозиторий в `ComfyUI/custom_nodes/`, затем перезапустите ComfyUI и выполните жёсткое обновление страницы (`Ctrl+Shift+R`).
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>
2. Добавьте `LoRA Loader (LoraTags)` и `CLIP Text Encode (Auto-Tags)`; соедините выход TAGS лоадера со входом `tags` энкодера.
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>
3. Добавьте строки LoRA, выберите файлы `.safetensors`, задайте силу и включите нужные строки; в Tag Manager получите теги с Civitai или добавьте свои.
  — <https://github.com/iiTzMYUNG/ComfyUI-LoraTags>

## Best practices

- Не редактируйте `lora_stack_data` вручную: его сериализует UI узла.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- После обновления узла делайте hard refresh: его интерфейс загружается из JavaScript, и устаревший кэш может сломать отображение.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Проверяйте активные LoRA, их strength и пути к файлам: выключенная строка, strength 0 или перемещённый файл не будут применены.
  — <https://comfy.icu/node/LoraLoaderMasterDB>
- Следите за длиной prompt при большом стеке: Auto-Tags добавляет триггеры в тот же CLIP-контекст.
  — <https://comfy.icu/node/CLIPTextEncodeWithTags>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- GitHub history confirms 16 commits but the accessible primary page did not expose their individual dates or messages; no later dated change is asserted.
- No GitHub release is listed on the repository page, so a versioned release timeline cannot be confirmed.
- The source request asks for `event_findings` and `new_events`, but the required response schema has no fields for them; the dated findings are retained in `what_changed`.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/iiTzMYUNG/ComfyUI-LoraTags | GitHub — iiTzMYUNG/ComfyUI-LoraTags README | 2026-09-05 |
| https://comfy.icu/node/LoraLoaderMasterDB | ComfyUI Cloud — LoRA Loader (LoraTags) | 2026-09-05 |
| https://comfy.icu/node/CLIPTextEncodeWithTags | ComfyUI Cloud — CLIP Text Encode (Auto-Tags) | 2026-09-05 |
| https://www.patreon.com/cw/iiTzMYUNG/sitemap?l=it-IT | iiTzMYUNG Patreon sitemap | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-loratags`, thread `comfyui-loratags`, 0 dated events - → -.
- **Practical note:** As of 2026-07-23, treat the linked GitHub repository as a lead for follow-up research only; do not infer a supported installation, release, or feature change from this record.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
